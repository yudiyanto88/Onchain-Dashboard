"""
Dual-Pair Confirmation Analysis
Signal fires only when BOTH pairs crossover in the same direction within AGREE_WINDOW days.
Signal date = the LATER crossover (both confirmed).
Measures: precision improvement vs single pair, and lead time to major events.
"""

import pandas as pd
import numpy as np
from itertools import combinations

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"], usecols=["date","btc_price","asopr"]
)
df = (df.dropna(subset=["btc_price","asopr"])
       .query("btc_price > 0 and date >= '2013-01-01'")
       .sort_values("date").reset_index(drop=True))

for span in [30,35,40,45,50,55,60,65,90]:
    df[f"EMA{span}"] = df["asopr"].ewm(span=span, adjust=False).mean()
for win in [15,20,25,30,35,80]:
    df[f"SMA{win}"] = df["asopr"].rolling(window=win, min_periods=win).mean()

PAIRS = [
    ("EMA30","SMA15"), ("EMA35","SMA20"), ("EMA40","SMA25"), ("EMA45","SMA25"),
    ("EMA50","SMA30"), ("EMA55","SMA35"), ("EMA60","SMA30"),
    ("EMA65","SMA35"), ("EMA90","SMA80"),
]
PAIR_LABELS = [f"{f}/{s}" for f, s in PAIRS]

MIN_GAP     = 30   # min days between same-direction crossovers per pair
AGREE_WIN   = 14   # max days between the two crossovers to count as "simultaneous"
AFTER_WIN   = 120  # window after signal to look for major event

# ── Crossover detection ────────────────────────────────────────────────────
def detect_crossovers(df, fast, slow):
    diff = df[fast] - df[slow]
    prev = diff.shift(1)
    up   = (diff > 0) & (prev <= 0)
    down = (diff < 0) & (prev >= 0)
    events, last_up, last_dn = [], pd.Timestamp("2000-01-01"), pd.Timestamp("2000-01-01")
    for i in df.index:
        if pd.isna(df.at[i,fast]) or pd.isna(df.at[i,slow]): continue
        d = df.at[i,"date"]
        if up[i] and (d-last_up).days >= MIN_GAP:
            events.append({"date":d,"direction":"UP","price":df.at[i,"btc_price"]})
            last_up = d
        elif down[i] and (d-last_dn).days >= MIN_GAP:
            events.append({"date":d,"direction":"DOWN","price":df.at[i,"btc_price"]})
            last_dn = d
    return pd.DataFrame(events) if events else pd.DataFrame(columns=["date","direction","price"])

# Pre-compute all crossovers
all_crosses = {}
for fast, slow in PAIRS:
    all_crosses[f"{fast}/{slow}"] = detect_crossovers(df, fast, slow)

# ── Major events ──────────────────────────────────────────────────────────
def find_major_events(df, window=90, min_dd=0.28, min_ru=0.65, merge=60):
    prices, dates, n = df["btc_price"].values, df["date"].values, len(df)
    bottoms, peaks = [], []
    for i in range(window, n-window):
        p, prev, nxt = prices[i], prices[i-window:i], prices[i+1:i+window+1]
        if p <= prev.min() and p <= nxt.min() and (prev.max()-p)/prev.max() >= min_dd:
            bottoms.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
        if p >= prev.max() and p >= nxt.max() and (p-prev.min())/prev.min() >= min_ru:
            peaks.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
    def mg(evts, keep):
        if not evts: return []
        evts = sorted(evts, key=lambda x: x["date"])
        merged, grp = [], [evts[0]]
        for e in evts[1:]:
            if (e["date"]-grp[-1]["date"]).days <= merge:
                grp.append(e)
            else:
                merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                              else max(grp,key=lambda x:x["price"]))
                grp = [e]
        merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                      else max(grp,key=lambda x:x["price"]))
        return merged
    return pd.DataFrame(mg(bottoms,"min")), pd.DataFrame(mg(peaks,"max"))

bottoms_df, peaks_df = find_major_events(df)
bottom_dates = list(bottoms_df["date"])
peak_dates   = list(peaks_df["date"])

# ── Dual-pair signal generation ────────────────────────────────────────────
def dual_signals(crosses_a, crosses_b, direction, agree_window=AGREE_WIN):
    """
    Find all dates where pair A and pair B BOTH crossed in [direction]
    within agree_window days of each other.
    Signal date = the LATER crossover (both confirmed at that point).
    """
    a = crosses_a[crosses_a["direction"]==direction].reset_index(drop=True)
    b = crosses_b[crosses_b["direction"]==direction].reset_index(drop=True)
    if a.empty or b.empty:
        return pd.DataFrame(columns=["date","price_a","price_b"])

    signals = []
    used_b  = set()

    for _, ra in a.iterrows():
        da = ra["date"]
        # find b crossovers within agree_window of da
        matches = b[
            (b["date"] >= da - pd.Timedelta(days=agree_window)) &
            (b["date"] <= da + pd.Timedelta(days=agree_window))
        ]
        for idx_b, rb in matches.iterrows():
            db = rb["date"]
            signal_date = max(da, db)   # later = both confirmed
            # deduplicate: keep only one signal per agree_window cluster
            if signals and (signal_date - signals[-1]["date"]).days < agree_window:
                continue
            if idx_b not in used_b:
                signals.append({
                    "date": signal_date,
                    "date_a": da, "date_b": db,
                    "price": df.loc[df["date"]==signal_date,"btc_price"].values[0]
                    if signal_date in df["date"].values else np.nan
                })
                used_b.add(idx_b)
                break

    return pd.DataFrame(signals) if signals else pd.DataFrame(columns=["date","price"])

# ── Classify signals ───────────────────────────────────────────────────────
def classify(signals, event_dates, after_win=AFTER_WIN):
    if signals.empty or "date" not in signals.columns:
        return dict(total=0, tp=0, fp=0, precision=np.nan,
                    avg_lead=np.nan, med_lead=np.nan, min_lead=np.nan)
    rows = []
    for _, row in signals.iterrows():
        sd  = row["date"]
        end = sd + pd.Timedelta(days=after_win)
        nearby = [d for d in event_dates if d >= sd and d <= end]
        if nearby:
            lead = (nearby[0] - sd).days
            rows.append({"tp":True,"lead":lead})
        else:
            rows.append({"tp":False,"lead":np.nan})
    res = pd.DataFrame(rows)
    tp  = res["tp"].sum()
    leads = res.loc[res["tp"],"lead"]
    return dict(
        total     = len(res),
        tp        = int(tp),
        fp        = int(len(res)-tp),
        precision = round(tp/len(res)*100,1) if len(res) else np.nan,
        avg_lead  = round(leads.mean(),0) if not leads.empty else np.nan,
        med_lead  = round(leads.median(),0) if not leads.empty else np.nan,
        min_lead  = round(leads.min(),0) if not leads.empty else np.nan,
    )

# ── Single-pair baseline ───────────────────────────────────────────────────
single_up   = {}
single_down = {}
for label in PAIR_LABELS:
    c = all_crosses[label]
    up_c   = c[c["direction"]=="UP"].copy()
    dn_c   = c[c["direction"]=="DOWN"].copy()
    # classify single
    def classify_single(sigs, event_dates, after_win=AFTER_WIN):
        rows = []
        for _, row in sigs.iterrows():
            sd  = row["date"]
            end = sd + pd.Timedelta(days=after_win)
            nearby = [d for d in event_dates if d >= sd and d <= end]
            rows.append({"tp":bool(nearby),
                         "lead":(nearby[0]-sd).days if nearby else np.nan})
        res = pd.DataFrame(rows) if rows else pd.DataFrame(columns=["tp","lead"])
        if res.empty:
            return dict(total=0,tp=0,fp=0,precision=np.nan,avg_lead=np.nan)
        tp = res["tp"].sum()
        leads = res.loc[res["tp"],"lead"]
        return dict(total=len(res),tp=int(tp),fp=int(len(res)-tp),
                    precision=round(tp/len(res)*100,1),
                    avg_lead=round(leads.mean(),0) if not leads.empty else np.nan)
    single_up[label]   = classify_single(up_c, bottom_dates)
    single_down[label] = classify_single(dn_c, peak_dates)

# ── All pair combinations ──────────────────────────────────────────────────
up_results   = []
down_results = []

for (la, lb) in combinations(PAIR_LABELS, 2):
    ca = all_crosses[la]
    cb = all_crosses[lb]

    # UP
    sigs_up = dual_signals(ca, cb, "UP")
    su = classify(sigs_up, bottom_dates)
    up_results.append({
        "Pair A": la, "Pair B": lb,
        "Signals": su["total"], "True+": su["tp"], "False+": su["fp"],
        "Precision": su["precision"],
        "Avg Lead": su["avg_lead"], "Med Lead": su["med_lead"],
        "Min Lead": su["min_lead"],
    })

    # DOWN
    sigs_dn = dual_signals(ca, cb, "DOWN")
    sd = classify(sigs_dn, peak_dates)
    down_results.append({
        "Pair A": la, "Pair B": lb,
        "Signals": sd["total"], "True+": sd["tp"], "False+": sd["fp"],
        "Precision": sd["precision"],
        "Avg Lead": sd["avg_lead"], "Med Lead": sd["med_lead"],
        "Min Lead": sd["min_lead"],
    })

up_df   = pd.DataFrame(up_results).dropna(subset=["Precision"])
down_df = pd.DataFrame(down_results).dropna(subset=["Precision"])

# ── Print results ──────────────────────────────────────────────────────────
print("="*90)
print(f"DUAL CONFIRMATION — agree window = {AGREE_WIN}d, event window = {AFTER_WIN}d")
print("="*90)

print("\n--- UP (Bottom signal) — sorted by Precision desc ---")
up_sorted = up_df.sort_values(["Precision","Avg Lead"], ascending=[False,False])
print(up_sorted.to_string(index=False))

print("\n--- DOWN (Peak signal) — sorted by Precision desc ---")
dn_sorted = down_df.sort_values(["Precision","Avg Lead"], ascending=[False,False])
print(dn_sorted.to_string(index=False))

# ── Top 15 by precision for each direction ────────────────────────────────
print("\n\n" + "="*90)
print("TOP 15 COMBINATIONS — UP (Bottom), by Precision")
print("="*90)
top_up = up_sorted.head(15)
print(top_up[["Pair A","Pair B","Signals","True+","False+","Precision","Avg Lead","Med Lead"]].to_string(index=False))

print("\n\n" + "="*90)
print("TOP 15 COMBINATIONS — DOWN (Peak), by Precision")
print("="*90)
top_dn = dn_sorted.head(15)
print(top_dn[["Pair A","Pair B","Signals","True+","False+","Precision","Avg Lead","Med Lead"]].to_string(index=False))

# ── Baseline comparison ───────────────────────────────────────────────────
print("\n\n" + "="*90)
print("SINGLE PAIR BASELINE — UP Precision")
print("="*90)
for lbl, s in sorted(single_up.items(), key=lambda x: -x[1]["precision"]):
    print(f"  {lbl:15s}  Total={s['total']:3d}  FP={s['fp']:3d}  Precision={s['precision']}%  AvgLead={s['avg_lead']}d")

print("\nSINGLE PAIR BASELINE — DOWN Precision")
for lbl, s in sorted(single_down.items(), key=lambda x: -x[1]["precision"]):
    print(f"  {lbl:15s}  Total={s['total']:3d}  FP={s['fp']:3d}  Precision={s['precision']}%  AvgLead={s['avg_lead']}d")

# ── Best combo that also has good lead time ───────────────────────────────
print("\n\n" + "="*90)
print("BEST COMBOS — Precision >= 40% AND Avg Lead >= 30d (UP)")
print("="*90)
filtered_up = up_df[(up_df["Precision"]>=40) & (up_df["Avg Lead"]>=30)].sort_values("Precision", ascending=False)
if filtered_up.empty:
    print("None found — relaxing to Precision >= 35%")
    filtered_up = up_df[up_df["Precision"]>=35].sort_values(["Precision","Avg Lead"], ascending=[False,False])
print(filtered_up[["Pair A","Pair B","Signals","True+","False+","Precision","Avg Lead"]].to_string(index=False))

print("\n\n" + "="*90)
print("BEST COMBOS — Precision >= 35% AND Avg Lead >= 25d (DOWN)")
print("="*90)
filtered_dn = down_df[(down_df["Precision"]>=35) & (down_df["Avg Lead"]>=25)].sort_values("Precision", ascending=False)
if filtered_dn.empty:
    print("None found — relaxing to Precision >= 30%")
    filtered_dn = down_df[down_df["Precision"]>=30].sort_values(["Precision","Avg Lead"], ascending=[False,False])
print(filtered_dn[["Pair A","Pair B","Signals","True+","False+","Precision","Avg Lead"]].to_string(index=False))
