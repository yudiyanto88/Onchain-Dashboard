"""
aSOPR Crossover Analysis
Pairs: EMA55/SMA35, EMA65/SMA35, EMA90/SMA80
Metrics: hit rate & lead time optimization
"""

import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"],
    usecols=["date", "btc_price", "asopr"]
)
df = df.dropna(subset=["btc_price", "asopr"])
df = df[df["btc_price"] > 0].sort_values("date").reset_index(drop=True)

# Start from 2013 onwards (enough data for MA90)
df = df[df["date"] >= "2013-01-01"].reset_index(drop=True)

print(f"Rows after filter: {len(df)}  ({df['date'].min().date()} to {df['date'].max().date()})")

# ── Moving Averages ────────────────────────────────────────────────────────
def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

def sma(series, window):
    return series.rolling(window=window, min_periods=window).mean()

df["EMA30"] = ema(df["asopr"], 30)
df["EMA35"] = ema(df["asopr"], 35)
df["EMA40"] = ema(df["asopr"], 40)
df["EMA45"] = ema(df["asopr"], 45)
df["EMA50"] = ema(df["asopr"], 50)
df["EMA55"] = ema(df["asopr"], 55)
df["EMA60"] = ema(df["asopr"], 60)
df["SMA15"] = sma(df["asopr"], 15)
df["SMA20"] = sma(df["asopr"], 20)
df["SMA25"] = sma(df["asopr"], 25)
df["SMA30"] = sma(df["asopr"], 30)
df["SMA35"] = sma(df["asopr"], 35)

# ── Crossover Detection ────────────────────────────────────────────────────
PAIRS = [
    ("EMA30", "SMA15"),
    ("EMA35", "SMA20"),
    ("EMA40", "SMA25"),
    ("EMA45", "SMA25"),
    ("EMA50", "SMA30"),
    ("EMA55", "SMA35"),
    ("EMA60", "SMA30"),
]

LEAD_TIMES = [7, 14, 21, 30, 45, 60, 90, 120, 180]

MIN_GAP_DAYS = 30   # minimum days between same-direction crossovers (cooldown)

def detect_crossovers(df, fast_col, slow_col):
    """Return DataFrame of crossover events with direction."""
    diff = df[fast_col] - df[slow_col]
    # crossover UP: diff goes from negative/zero to positive
    # crossover DOWN: diff goes from positive/zero to negative
    prev_diff = diff.shift(1)
    cross_up   = (diff > 0) & (prev_diff <= 0)
    cross_down = (diff < 0) & (prev_diff >= 0)

    events = []
    last_up   = pd.Timestamp("2000-01-01")
    last_down = pd.Timestamp("2000-01-01")

    for i in df.index:
        if pd.isna(df.at[i, fast_col]) or pd.isna(df.at[i, slow_col]):
            continue
        date = df.at[i, "date"]
        price = df.at[i, "btc_price"]

        if cross_up[i] and (date - last_up).days >= MIN_GAP_DAYS:
            events.append({"date": date, "direction": "UP", "price": price, "row_idx": i})
            last_up = date
        elif cross_down[i] and (date - last_down).days >= MIN_GAP_DAYS:
            events.append({"date": date, "direction": "DOWN", "price": price, "row_idx": i})
            last_down = date

    return pd.DataFrame(events)

# ── Forward Return Calculation ─────────────────────────────────────────────
def forward_return(df, row_idx, days):
    """Return % price change from crossover date to +days."""
    target_date = df.at[row_idx, "date"] + pd.Timedelta(days=days)
    future = df[df["date"] >= target_date]
    if future.empty:
        return np.nan
    future_price = future.iloc[0]["btc_price"]
    entry_price  = df.at[row_idx, "price"] if "price" in df.columns else df.at[row_idx, "btc_price"]
    return (future_price / df.at[row_idx, "btc_price"] - 1) * 100

# ── Analysis per Pair ──────────────────────────────────────────────────────
all_results = []

for fast_col, slow_col in PAIRS:
    pair_label = f"{fast_col}/{slow_col}"
    events = detect_crossovers(df, fast_col, slow_col)
    events = events.reset_index(drop=True)

    up_events   = events[events["direction"] == "UP"].copy()
    down_events = events[events["direction"] == "DOWN"].copy()

    for direction, subset in [("UP", up_events), ("DOWN", down_events)]:
        if subset.empty:
            continue

        row = {
            "Pair": pair_label,
            "Direction": direction,
            "Events": len(subset),
        }

        best_hit  = 0
        best_lead = 0

        for days in LEAD_TIMES:
            returns = subset["row_idx"].apply(
                lambda idx: forward_return(df, idx, days)
            ).dropna()

            n = len(returns)
            if n == 0:
                row[f"Hit{days}d"] = "—"
                row[f"Med{days}d"] = "—"
                continue

            if direction == "UP":
                hits = (returns > 0).sum()
            else:
                hits = (returns < 0).sum()

            hit_rate = hits / n * 100
            median_ret = returns.median()

            row[f"Hit{days}d"]  = f"{hit_rate:.0f}%"
            row[f"Med{days}d"]  = f"{median_ret:+.1f}%"
            row[f"n{days}d"]    = n

            if hit_rate > best_hit:
                best_hit  = hit_rate
                best_lead = days

        row["Best Lead"] = f"{best_lead}d"
        row["Best Hit"]  = f"{best_hit:.0f}%"
        all_results.append(row)

# ── Summary Table ──────────────────────────────────────────────────────────
print("\n\n" + "="*80)
print("SUMMARY TABLE — Hit Rate per Lead Time")
print("="*80)

# Compact table: just hit rates + median at each lead time
cols_hit = ["Pair", "Direction", "Events"] + [f"Hit{d}d" for d in LEAD_TIMES] + ["Best Lead", "Best Hit"]
summary = pd.DataFrame(all_results)[cols_hit]
print(summary.to_string(index=False))

print("\n\n" + "="*80)
print("SUMMARY TABLE — Median Return per Lead Time")
print("="*80)

cols_med = ["Pair", "Direction", "Events"] + [f"Med{d}d" for d in LEAD_TIMES]
summary_med = pd.DataFrame(all_results)[cols_med]
print(summary_med.to_string(index=False))

# ── Best Configuration per Direction ──────────────────────────────────────
print("\n\n" + "="*80)
print("OPTIMAL CONFIG per Pair × Direction")
print("="*80)

for r in all_results:
    hits_by_lead = {}
    for d in LEAD_TIMES:
        val = r.get(f"Hit{d}d", "—")
        if val != "—":
            hits_by_lead[d] = float(val.replace("%",""))

    if not hits_by_lead:
        continue

    sorted_leads = sorted(hits_by_lead.items(), key=lambda x: -x[1])
    top3 = sorted_leads[:3]
    top3_str = " | ".join([f"{d}d={h:.0f}%" for d, h in top3])

    print(f"  {r['Pair']:15s} {r['Direction']:5s}  Events={r['Events']:3d}  Top leads: {top3_str}")

# Event detail suppressed — summary tables only
