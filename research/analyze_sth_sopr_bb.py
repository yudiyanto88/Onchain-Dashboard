"""
STH-SOPR Bollinger Band Grid Search — Bull Dip Signal Optimization
Logic: lower band touch on STH-SOPR = potential bull dip entry
"""

import pandas as pd
import numpy as np
from itertools import product

# ── Load data ────────────────────────────────────────────────────────────────
df = pd.read_csv("data_momentum.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[["date", "btc_price", "sth_sopr"]].dropna()

BULL_START   = pd.Timestamp("2023-01-01")
BULL_END     = pd.Timestamp("2025-10-31")
BEAR_START   = pd.Timestamp("2025-11-01")
ANALYSIS_END = df["date"].max()

df_bull = df[(df["date"] >= BULL_START) & (df["date"] <= BULL_END)].copy()

# ── Find actual bull dip bottoms ──────────────────────────────────────────────
def find_dip_bottoms(prices, dates, lookback=30, min_drop_pct=10, merge_days=14):
    """Local price minima: rolling lookback peak → drop ≥ min_drop_pct."""
    prices = prices.reset_index(drop=True)
    dates  = dates.reset_index(drop=True)
    rolling_max = prices.rolling(lookback, min_periods=1).max()
    pct_from_peak = (prices / rolling_max - 1) * 100

    bottoms, in_dip, best_px, best_dt = [], False, np.inf, None
    for i in range(len(prices)):
        if pct_from_peak.iloc[i] <= -min_drop_pct:
            if not in_dip:
                in_dip = True
            if prices.iloc[i] < best_px:
                best_px, best_dt = prices.iloc[i], dates.iloc[i]
        else:
            if in_dip:
                bottoms.append({"date": best_dt, "price": best_px})
                in_dip, best_px, best_dt = False, np.inf, None

    # merge nearby bottoms
    merged = []
    for b in bottoms:
        if merged and (b["date"] - merged[-1]["date"]).days < merge_days:
            if b["price"] < merged[-1]["price"]:
                merged[-1] = b
        else:
            merged.append(b)
    return pd.DataFrame(merged) if merged else pd.DataFrame(columns=["date", "price"])


bull_dips = find_dip_bottoms(df_bull["btc_price"], df_bull["date"])
dip_dates = pd.to_datetime(bull_dips["date"].tolist())

print(f"\n=== BULL DIPS IDENTIFIED ({BULL_START.date()} – {BULL_END.date()}) — {len(bull_dips)} events ===")
for _, r in bull_dips.iterrows():
    print(f"  {r['date'].date()} | ${r['price']:>9,.0f}")


# ── Bollinger Band & signal detection ────────────────────────────────────────
def get_signals(df_in, period, std_dev):
    """Return df with lower_bb and signal columns."""
    d = df_in.copy()
    sma   = d["sth_sopr"].rolling(period, min_periods=period).mean()
    sigma = d["sth_sopr"].rolling(period, min_periods=period).std()
    d["lower_bb"] = sma - std_dev * sigma
    d["upper_bb"] = sma + std_dev * sigma
    below = d["sth_sopr"] < d["lower_bb"]
    d["signal"] = below & ~below.shift(1, fill_value=False)   # first-day of episode
    return d


# ── Core evaluator ────────────────────────────────────────────────────────────
def evaluate(df_full, dip_dates_ts, period, std_dev,
             pre_window=21,     # signal must fire ≤ pre_window days BEFORE dip bottom
             post_window=7,     # or ≤ post_window days AFTER (signal fires at/near bottom)
             gain_windows=(14, 30, 60),
             bear_start=BEAR_START):

    d = get_signals(df_full, period, std_dev)

    # ── Bull period ───────────────────────────────────────────────────────────
    d_bull = d[(d["date"] >= BULL_START) & (d["date"] <= BULL_END)]
    bull_sig_dates = d_bull[d_bull["signal"]]["date"].tolist()
    n_bull_sigs = len(bull_sig_dates)

    # De-duplicate consecutive signals within 7 days (same episode)
    deduped = []
    for s in bull_sig_dates:
        if not deduped or (s - deduped[-1]).days > 7:
            deduped.append(s)
    bull_sig_deduped = deduped
    n_bull_deduped = len(deduped)

    # Recall: for each dip, was there at least one signal in [-pre_window, +post_window]?
    dips_covered = set()
    for s_date in bull_sig_deduped:
        for i, dip_dt in enumerate(dip_dates_ts):
            delta = (dip_dt - s_date).days
            if -post_window <= delta <= pre_window:
                dips_covered.add(i)

    recall = len(dips_covered) / len(dip_dates_ts) * 100 if len(dip_dates_ts) > 0 else 0

    # Precision: for each deduped signal, did it precede a dip within pre_window days?
    true_sigs = 0
    gains_14, gains_30, gains_60 = [], [], []
    lead_days = []

    for s_date in bull_sig_deduped:
        sig_row = d[d["date"] == s_date]
        if sig_row.empty:
            continue
        entry_px = sig_row["btc_price"].iloc[0]

        matched_dip = None
        for dip_dt, dip_px in zip(dip_dates_ts, bull_dips["price"].tolist()):
            delta = (dip_dt - s_date).days
            if -post_window <= delta <= pre_window:
                if matched_dip is None or abs(delta) < abs((matched_dip[0] - s_date).days):
                    matched_dip = (dip_dt, dip_px, delta)

        if matched_dip:
            true_sigs += 1
            lead_days.append(matched_dip[2])

        # Forward gains from signal date
        for gw, glist in zip(gain_windows, [gains_14, gains_30, gains_60]):
            fut = d[(d["date"] > s_date) & (d["date"] <= s_date + pd.Timedelta(days=gw))]
            if not fut.empty:
                glist.append((fut["btc_price"].max() / entry_px - 1) * 100)

    precision = true_sigs / n_bull_deduped * 100 if n_bull_deduped > 0 else 0

    # ── Bear period (false positives to ignore) ───────────────────────────────
    d_bear = d[d["date"] >= bear_start]
    bear_sig_dates = d_bear[d_bear["signal"]]["date"].tolist()
    bear_deduped = []
    for s in bear_sig_dates:
        if not bear_deduped or (s - bear_deduped[-1]).days > 7:
            bear_deduped.append(s)
    n_bear_fp = len(bear_deduped)
    bear_months = max((ANALYSIS_END - bear_start).days / 30, 0.1)
    fp_per_month = n_bear_fp / bear_months

    return {
        "period":          period,
        "std_dev":         std_dev,
        "n_signals":       n_bull_deduped,      # de-duplicated signals in bull
        "recall_%":        round(recall, 1),
        "precision_%":     round(precision, 1),
        "avg_lead_d":      round(np.mean(lead_days), 1) if lead_days else None,
        "avg_g14d":        round(np.mean(gains_14), 1) if gains_14 else None,
        "avg_g30d":        round(np.mean(gains_30), 1) if gains_30 else None,
        "avg_g60d":        round(np.mean(gains_60), 1) if gains_60 else None,
        "bear_fp":         n_bear_fp,
        "fp/mo":           round(fp_per_month, 2),
    }


# ── Grid search ───────────────────────────────────────────────────────────────
periods  = [14, 20, 28, 30, 50, 60]
std_devs = [1.5, 1.75, 2.0, 2.25, 2.5]

results = []
for period, std_dev in product(periods, std_devs):
    results.append(evaluate(df, dip_dates, period, std_dev))

rdf = pd.DataFrame(results)

# Composite score: high recall, high precision, good 30d gain, low bear FP
rdf["score"] = (
    rdf["recall_%"]    * 0.35 +
    rdf["precision_%"] * 0.30 +
    rdf["avg_g30d"].fillna(0) * 1.5 +
    rdf["avg_lead_d"].fillna(0).clip(lower=0) * 0.5 -  # earlier warning = good
    rdf["fp/mo"] * 8.0
)
rdf = rdf.sort_values("score", ascending=False).reset_index(drop=True)

pd.set_option("display.width", 220)
pd.set_option("display.max_columns", 20)

print("\n=== FULL GRID SEARCH (sorted by composite score) ===")
print(rdf.to_string(index=False))

# ── Requested comparisons ─────────────────────────────────────────────────────
targets = [(28, 2.0), (14, 1.75), (50, 1.5), (50, 2.0)]
print("\n=== REQUESTED COMPARISONS vs IMAGE BASELINE (28,2) ===")
cmp = rdf[rdf.apply(lambda r: (r["period"], r["std_dev"]) in targets, axis=1)]
print(cmp.to_string(index=False))

# ── Top 5 ─────────────────────────────────────────────────────────────────────
print("\n=== TOP 5 BY COMPOSITE SCORE ===")
print(rdf.head(5).to_string(index=False))

# ── Worst 5 (for reference) ───────────────────────────────────────────────────
print("\n=== BOTTOM 5 ===")
print(rdf.tail(5).to_string(index=False))

# ── Signal list for top 3 settings ───────────────────────────────────────────
for rank in range(3):
    row = rdf.iloc[rank]
    p, s = int(row["period"]), row["std_dev"]
    d_sig = get_signals(df, p, s)
    bull_sigs = d_sig[
        (d_sig["date"] >= BULL_START) & (d_sig["date"] <= BULL_END) & d_sig["signal"]
    ].copy()
    # Deduplicate
    deduped_rows = []
    last_d = None
    for _, r in bull_sigs.iterrows():
        if last_d is None or (r["date"] - last_d).days > 7:
            deduped_rows.append(r)
            last_d = r["date"]
    deduped_df = pd.DataFrame(deduped_rows)

    print(f"\n=== BB({p},{s}) — Rank #{rank+1} — Bull Dip Signals ===")
    print(f"{'Date':12} {'Price':>10} {'STH-SOPR':>10} {'LowerBB':>10} {'Spread':>8} {'G30d%':>7}")
    for _, r in deduped_df.iterrows():
        fut = d_sig[(d_sig["date"] > r["date"]) &
                    (d_sig["date"] <= r["date"] + pd.Timedelta(days=30))]
        g30 = (fut["btc_price"].max() / r["btc_price"] - 1) * 100 if not fut.empty else float("nan")
        spread = (r["sth_sopr"] - r["lower_bb"]) * 1000  # in milli units
        print(f"  {str(r['date'].date()):12} ${r['btc_price']:>9,.0f}  {r['sth_sopr']:>8.4f}  {r['lower_bb']:>8.4f}  {spread:>+7.2f}  {g30:>+6.1f}%")

    bear_sigs = d_sig[(d_sig["date"] >= BEAR_START) & d_sig["signal"]]
    bear_deduped = []
    last_d = None
    for _, r in bear_sigs.iterrows():
        if last_d is None or (r["date"] - last_d).days > 7:
            bear_deduped.append(r)
            last_d = r["date"]
    print(f"  Bear FPs (ignore — S2 latch active): {len(bear_deduped)}")
    for r in bear_deduped:
        print(f"    {str(r['date'].date()):12} ${r['btc_price']:>9,.0f}  STH-SOPR {r['sth_sopr']:.4f}")
