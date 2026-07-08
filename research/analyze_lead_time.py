"""
aSOPR Crossover — Lead Time Analysis
Goal: which pair fires EARLIEST before major bottoms (UP cross) and peaks (DOWN cross)?
Lead time = event_date - crossover_date (days). Higher = earlier warning = better.
"""

import pandas as pd
import numpy as np

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"],
    usecols=["date", "btc_price", "asopr"]
)
df = (df.dropna(subset=["btc_price","asopr"])
       .query("btc_price > 0 and date >= '2013-01-01'")
       .sort_values("date")
       .reset_index(drop=True))

# ── Moving Averages ────────────────────────────────────────────────────────
for span in [30, 35, 40, 45, 50, 55, 60, 65, 90]:
    df[f"EMA{span}"] = df["asopr"].ewm(span=span, adjust=False).mean()
for win in [15, 20, 25, 30, 35, 80]:
    df[f"SMA{win}"] = df["asopr"].rolling(window=win, min_periods=win).mean()

PAIRS = [
    ("EMA30","SMA15"), ("EMA35","SMA20"), ("EMA40","SMA25"), ("EMA45","SMA25"),
    ("EMA50","SMA30"), ("EMA55","SMA35"), ("EMA60","SMA30"),
    ("EMA65","SMA35"), ("EMA90","SMA80"),
]

# ── Crossover Detection ────────────────────────────────────────────────────
MIN_GAP = 30

def detect_crossovers(df, fast, slow):
    diff = df[fast] - df[slow]
    prev = diff.shift(1)
    up   = (diff > 0) & (prev <= 0)
    down = (diff < 0) & (prev >= 0)
    events, last_up, last_down = [], pd.Timestamp("2000-01-01"), pd.Timestamp("2000-01-01")
    for i in df.index:
        if pd.isna(df.at[i, fast]) or pd.isna(df.at[i, slow]):
            continue
        d = df.at[i, "date"]
        if up[i] and (d - last_up).days >= MIN_GAP:
            events.append({"date": d, "direction": "UP", "price": df.at[i,"btc_price"]})
            last_up = d
        elif down[i] and (d - last_down).days >= MIN_GAP:
            events.append({"date": d, "direction": "DOWN", "price": df.at[i,"btc_price"]})
            last_down = d
    return pd.DataFrame(events) if events else pd.DataFrame(columns=["date","direction","price"])

# ── Major Cycle Event Detection ────────────────────────────────────────────
def find_major_events(df, window=90, min_drawdown=0.28, min_runup=0.65, merge_days=60):
    prices = df["btc_price"].values
    dates  = df["date"].values
    n = len(prices)
    bottoms, peaks = [], []

    for i in range(window, n - window):
        p    = prices[i]
        prev = prices[i-window:i]
        nxt  = prices[i+1:i+window+1]
        # local minimum
        if p <= prev.min() and p <= nxt.min():
            dd = (prev.max() - p) / prev.max()
            if dd >= min_drawdown:
                bottoms.append({"date": pd.Timestamp(dates[i]), "price": float(p), "dd_pct": round(dd*100,1)})
        # local maximum
        if p >= prev.max() and p >= nxt.max():
            ru = (p - prev.min()) / prev.min()
            if ru >= min_runup:
                peaks.append({"date": pd.Timestamp(dates[i]), "price": float(p), "runup_pct": round(ru*100,1)})

    def merge(evts, keep):
        if not evts: return []
        evts = sorted(evts, key=lambda x: x["date"])
        merged, grp = [], [evts[0]]
        for e in evts[1:]:
            if (e["date"] - grp[-1]["date"]).days <= merge_days:
                grp.append(e)
            else:
                merged.append(min(grp, key=lambda x: x["price"]) if keep=="min"
                              else max(grp, key=lambda x: x["price"]))
                grp = [e]
        merged.append(min(grp, key=lambda x: x["price"]) if keep=="min"
                      else max(grp, key=lambda x: x["price"]))
        return merged

    return pd.DataFrame(merge(bottoms,"min")), pd.DataFrame(merge(peaks,"max"))

bottoms_df, peaks_df = find_major_events(df)

print("="*70)
print("MAJOR CYCLE BOTTOMS DETECTED")
print("="*70)
b_show = bottoms_df.copy()
b_show["price"] = b_show["price"].apply(lambda x: f"${x:,.0f}")
b_show["date"]  = b_show["date"].dt.strftime("%Y-%m-%d")
print(b_show.to_string(index=False))

print("\n" + "="*70)
print("MAJOR CYCLE PEAKS DETECTED")
print("="*70)
p_show = peaks_df.copy()
p_show["price"]      = p_show["price"].apply(lambda x: f"${x:,.0f}")
p_show["date"]       = p_show["date"].dt.strftime("%Y-%m-%d")
print(p_show.to_string(index=False))

# ── Lead Time Computation ──────────────────────────────────────────────────
LOOKBACK = 365  # search window before each event

def compute_lead(events_df, crosses_df, direction):
    """
    For each major event, find the LAST crossover of [direction]
    that fired BEFORE the event (within LOOKBACK days).
    Returns per-event lead times (days). Positive = earlier warning.
    """
    rows = []
    dir_crosses = crosses_df[crosses_df["direction"] == direction].copy()

    for _, ev in events_df.iterrows():
        ev_date    = ev["date"]
        ev_price   = ev["price"]
        win_start  = ev_date - pd.Timedelta(days=LOOKBACK)

        before = dir_crosses[(dir_crosses["date"] >= win_start) &
                             (dir_crosses["date"] <  ev_date)]

        if before.empty:
            rows.append({"event_date": ev_date, "event_price": ev_price,
                         "cross_date": pd.NaT, "lead_days": np.nan, "hit": False})
        else:
            # last crossover before the event (final confirmation before price turns)
            last = before.iloc[-1]
            lead = (ev_date - last["date"]).days
            rows.append({"event_date": ev_date, "event_price": ev_price,
                         "cross_date": last["date"], "lead_days": lead, "hit": True})
    return pd.DataFrame(rows)

# ── Run for All Pairs ──────────────────────────────────────────────────────
bottom_summary = []
peak_summary   = []

# Store per-event details for the detail table
bottom_detail_cols = ["event"] + [f"{f}/{s}" for f, s in PAIRS]
peak_detail_cols   = ["event"] + [f"{f}/{s}" for f, s in PAIRS]

bottom_detail = {str(row["date"].date()): {} for _, row in bottoms_df.iterrows()}
peak_detail   = {str(row["date"].date()): {} for _, row in peaks_df.iterrows()}

for fast, slow in PAIRS:
    pair = f"{fast}/{slow}"
    crosses = detect_crossovers(df, fast, slow)

    # Bottoms
    b = compute_lead(bottoms_df, crosses, "UP")
    b_hit  = b["hit"].sum()
    b_leads = b.loc[b["hit"], "lead_days"]
    b_avg  = b_leads.mean()
    b_med  = b_leads.median()
    b_min  = b_leads.min()
    bottom_summary.append({
        "Pair": pair,
        "Events": len(b),
        "Hit": b_hit,
        "Miss": len(b) - b_hit,
        "Avg Lead (d)": round(b_avg, 0) if not np.isnan(b_avg) else np.nan,
        "Med Lead (d)": round(b_med, 0) if not np.isnan(b_med) else np.nan,
        "Min Lead (d)": round(b_min, 0) if not np.isnan(b_min) else np.nan,
    })
    for _, row in b.iterrows():
        key = str(row["event_date"].date())
        bottom_detail[key][pair] = f"{int(row['lead_days'])}d" if row["hit"] else "MISS"

    # Peaks
    p = compute_lead(peaks_df, crosses, "DOWN")
    p_hit  = p["hit"].sum()
    p_leads = p.loc[p["hit"], "lead_days"]
    p_avg  = p_leads.mean()
    p_med  = p_leads.median()
    p_min  = p_leads.min()
    peak_summary.append({
        "Pair": pair,
        "Events": len(p),
        "Hit": p_hit,
        "Miss": len(p) - p_hit,
        "Avg Lead (d)": round(p_avg, 0) if not np.isnan(p_avg) else np.nan,
        "Med Lead (d)": round(p_med, 0) if not np.isnan(p_med) else np.nan,
        "Min Lead (d)": round(p_min, 0) if not np.isnan(p_min) else np.nan,
    })
    for _, row in p.iterrows():
        key = str(row["event_date"].date())
        peak_detail[key][pair] = f"{int(row['lead_days'])}d" if row["hit"] else "MISS"

# ── Summary Tables ─────────────────────────────────────────────────────────
print("\n\n" + "="*70)
print("BOTTOM LEAD TIME — UP Crossover (days before bottom)")
print("Higher = signal fires earlier = more time to accumulate")
print("="*70)
b_df = pd.DataFrame(bottom_summary).sort_values("Avg Lead (d)", ascending=False)
print(b_df.to_string(index=False))

print("\n\n" + "="*70)
print("PEAK LEAD TIME — DOWN Crossover (days before peak)")
print("Higher = signal fires earlier = more time to start selling")
print("="*70)
p_df = pd.DataFrame(peak_summary).sort_values("Avg Lead (d)", ascending=False)
print(p_df.to_string(index=False))

# ── Per-Event Detail ───────────────────────────────────────────────────────
print("\n\n" + "="*70)
print("BOTTOM DETAIL — lead days per pair per event")
print("="*70)
all_pairs_labels = [f"{f}/{s}" for f, s in PAIRS]

# Header
hdr = f"{'Bottom Date':12s} {'BTC Price':>10s}"
for pl in all_pairs_labels:
    hdr += f"  {pl:>12s}"
print(hdr)
print("-" * (24 + len(all_pairs_labels)*14))

for _, ev in bottoms_df.iterrows():
    key = str(ev["date"].date())
    row_str = f"{key:12s} ${ev['price']:>9,.0f}"
    for pl in all_pairs_labels:
        val = bottom_detail[key].get(pl, "?")
        row_str += f"  {val:>12s}"
    print(row_str)

print("\n\n" + "="*70)
print("PEAK DETAIL — lead days per pair per event")
print("="*70)
hdr = f"{'Peak Date':12s} {'BTC Price':>10s}"
for pl in all_pairs_labels:
    hdr += f"  {pl:>12s}"
print(hdr)
print("-" * (24 + len(all_pairs_labels)*14))

for _, ev in peaks_df.iterrows():
    key = str(ev["date"].date())
    row_str = f"{key:12s} ${ev['price']:>9,.0f}"
    for pl in all_pairs_labels:
        val = peak_detail[key].get(pl, "?")
        row_str += f"  {val:>12s}"
    print(row_str)

# ── Final Ranking ──────────────────────────────────────────────────────────
print("\n\n" + "="*70)
print("FINAL RANKING — Combined Score (Avg Lead Bottom + Avg Lead Peak)")
print("="*70)
b_rank = pd.DataFrame(bottom_summary)[["Pair","Avg Lead (d)"]].rename(columns={"Avg Lead (d)":"Bottom Lead"})
p_rank = pd.DataFrame(peak_summary)[["Pair","Avg Lead (d)"]].rename(columns={"Avg Lead (d)":"Peak Lead"})
combined = b_rank.merge(p_rank, on="Pair")
combined["Combined"] = combined["Bottom Lead"] + combined["Peak Lead"]
combined = combined.sort_values("Combined", ascending=False)
print(combined.to_string(index=False))
