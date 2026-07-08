"""
Verify signal ordering: does Stage 1 always fire before Stage 2?
Also check: EMA30/SMA15 noise in 2-stage context.

Bottom: Stage1=EMA55/SMA35, Stage2=EMA30/SMA15
Peak  : Stage1=EMA90/SMA80, Stage2=EMA30/SMA15
"""

import pandas as pd
import numpy as np

df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"], usecols=["date","btc_price","asopr"]
)
df = (df.dropna(subset=["btc_price","asopr"])
       .query("btc_price > 0 and date >= '2013-01-01'")
       .sort_values("date").reset_index(drop=True))

for span in [30,55,90]:
    df[f"EMA{span}"] = df["asopr"].ewm(span=span, adjust=False).mean()
for win in [15,35,80]:
    df[f"SMA{win}"] = df["asopr"].rolling(win, min_periods=win).mean()

MIN_GAP = 30

def detect_crossovers(df, fast, slow):
    diff = df[fast] - df[slow]
    prev = diff.shift(1)
    up, down = (diff > 0) & (prev <= 0), (diff < 0) & (prev >= 0)
    events, lu, ld = [], pd.Timestamp("2000-01-01"), pd.Timestamp("2000-01-01")
    for i in df.index:
        if pd.isna(df.at[i,fast]) or pd.isna(df.at[i,slow]): continue
        d = df.at[i,"date"]
        if up[i] and (d-lu).days >= MIN_GAP:
            events.append({"date":d,"direction":"UP","price":df.at[i,"btc_price"]})
            lu = d
        elif down[i] and (d-ld).days >= MIN_GAP:
            events.append({"date":d,"direction":"DOWN","price":df.at[i,"btc_price"]})
            ld = d
    return pd.DataFrame(events) if events else pd.DataFrame()

def find_major_events(df):
    window, min_dd, min_ru, merge = 90, 0.28, 0.65, 60
    prices, dates, n = df["btc_price"].values, df["date"].values, len(df)
    bottoms, peaks = [], []
    for i in range(window, n-window):
        p, prev, nxt = prices[i], prices[i-window:i], prices[i+1:i+window+1]
        if p<=prev.min() and p<=nxt.min() and (prev.max()-p)/prev.max()>=min_dd:
            bottoms.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
        if p>=prev.max() and p>=nxt.max() and (p-prev.min())/prev.min()>=min_ru:
            peaks.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
    def mg(evts, keep):
        if not evts: return []
        evts = sorted(evts, key=lambda x: x["date"])
        merged, grp = [], [evts[0]]
        for e in evts[1:]:
            if (e["date"]-grp[-1]["date"]).days <= merge: grp.append(e)
            else:
                merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                              else max(grp,key=lambda x:x["price"]))
                grp = [e]
        merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                      else max(grp,key=lambda x:x["price"]))
        return merged
    return pd.DataFrame(mg(bottoms,"min")), pd.DataFrame(mg(peaks,"max"))

bottoms_df, peaks_df = find_major_events(df)

c55_35 = detect_crossovers(df, "EMA55", "SMA35")
c90_80 = detect_crossovers(df, "EMA90", "SMA80")
c30_15 = detect_crossovers(df, "EMA30", "SMA15")

LOOKBACK = 365

def last_cross_before(crosses, direction, event_date):
    """Last crossover of given direction within LOOKBACK days before event."""
    pool = crosses[
        (crosses["direction"]==direction) &
        (crosses["date"] >= event_date - pd.Timedelta(days=LOOKBACK)) &
        (crosses["date"] <  event_date)
    ]
    if pool.empty: return None, None
    row = pool.iloc[-1]
    return row["date"], row["price"]

# ── BOTTOM: Stage1=EMA55/SMA35, Stage2=EMA30/SMA15 ───────────────────────
print("="*80)
print("BOTTOM ORDERING — Stage1=EMA55/SMA35 (UP)  |  Stage2=EMA30/SMA15 (UP)")
print("Positive lead = crossover fired N days BEFORE actual bottom")
print("="*80)
print(f"\n{'Bottom':12s} {'BTC Low':>9s}  {'Stage1 Date':12s} {'S1 Lead':>8s} {'S1 Price':>10s}  "
      f"{'Stage2 Date':12s} {'S2 Lead':>8s} {'S2 Price':>10s}  {'Order':>8s}  {'Gap S1>S2':>10s}")
print("-"*120)

b_order_ok, b_order_flip, b_miss = 0, 0, 0

for _, ev in bottoms_df.iterrows():
    ed, ep = ev["date"], ev["price"]
    d1, p1 = last_cross_before(c55_35, "UP", ed)
    d2, p2 = last_cross_before(c30_15, "UP", ed)

    lead1 = (ed - d1).days if d1 else None
    lead2 = (ed - d2).days if d2 else None

    if d1 and d2:
        if d1 < d2:
            order = "OK"
            gap   = (d2 - d1).days
            b_order_ok += 1
        elif d1 > d2:
            order = "FLIP"
            gap   = (d1 - d2).days
            b_order_flip += 1
        else:
            order = "SAME"
            gap   = 0
            b_order_ok += 1
    elif d1 and not d2:
        order, gap = "S2 MISS", None
        b_miss += 1
    elif d2 and not d1:
        order, gap = "S1 MISS", None
        b_miss += 1
    else:
        order, gap = "BOTH MISS", None
        b_miss += 1

    d1s  = d1.strftime("%Y-%m-%d")  if d1   else "—"
    d2s  = d2.strftime("%Y-%m-%d")  if d2   else "—"
    l1s  = f"{lead1}d"              if lead1 else "—"
    l2s  = f"{lead2}d"              if lead2 else "—"
    p1s  = f"${p1:,.0f}"           if p1   else "—"
    p2s  = f"${p2:,.0f}"           if p2   else "—"
    gaps = f"{gap}d"               if gap is not None else "—"

    flag = " <-- FLIP" if order=="FLIP" else (" <-- S2 MISS" if "MISS" in order else "")
    print(f"{ed.strftime('%Y-%m-%d'):12s} ${ep:>8,.0f}  {d1s:12s} {l1s:>8s} {p1s:>10s}  "
          f"{d2s:12s} {l2s:>8s} {p2s:>10s}  {order:>8s}  {gaps:>10s}{flag}")

print(f"\nOrder OK (S1 before S2): {b_order_ok}/{len(bottoms_df)}")
print(f"FLIP    (S2 before S1): {b_order_flip}/{len(bottoms_df)}")
print(f"MISS   (one missing)  : {b_miss}/{len(bottoms_df)}")

# ── PEAK: Stage1=EMA90/SMA80, Stage2=EMA30/SMA15 ─────────────────────────
print("\n\n" + "="*80)
print("PEAK ORDERING — Stage1=EMA90/SMA80 (DOWN)  |  Stage2=EMA30/SMA15 (DOWN)")
print("="*80)
print(f"\n{'Peak':12s} {'BTC Top':>9s}  {'Stage1 Date':12s} {'S1 Lead':>8s} {'S1 Price':>10s}  "
      f"{'Stage2 Date':12s} {'S2 Lead':>8s} {'S2 Price':>10s}  {'Order':>8s}  {'Gap S1>S2':>10s}")
print("-"*120)

p_order_ok, p_order_flip, p_miss = 0, 0, 0

for _, ev in peaks_df.iterrows():
    ed, ep = ev["date"], ev["price"]
    d1, p1 = last_cross_before(c90_80, "DOWN", ed)
    d2, p2 = last_cross_before(c30_15, "DOWN", ed)

    lead1 = (ed - d1).days if d1 else None
    lead2 = (ed - d2).days if d2 else None

    if d1 and d2:
        if d1 < d2:
            order = "OK"
            gap   = (d2 - d1).days
            p_order_ok += 1
        elif d1 > d2:
            order = "FLIP"
            gap   = (d1 - d2).days
            p_order_flip += 1
        else:
            order, gap = "SAME", 0
            p_order_ok += 1
    elif d1 and not d2:
        order, gap = "S2 MISS", None
        p_miss += 1
    elif d2 and not d1:
        order, gap = "S1 MISS", None
        p_miss += 1
    else:
        order, gap = "BOTH MISS", None
        p_miss += 1

    d1s  = d1.strftime("%Y-%m-%d")  if d1   else "—"
    d2s  = d2.strftime("%Y-%m-%d")  if d2   else "—"
    l1s  = f"{lead1}d"              if lead1 else "—"
    l2s  = f"{lead2}d"              if lead2 else "—"
    p1s  = f"${p1:,.0f}"           if p1   else "—"
    p2s  = f"${p2:,.0f}"           if p2   else "—"
    gaps = f"{gap}d"               if gap is not None else "—"

    flag = " <-- FLIP" if order=="FLIP" else (" <-- MISS" if "MISS" in order else "")
    print(f"{ed.strftime('%Y-%m-%d'):12s} ${ep:>9,.0f}  {d1s:12s} {l1s:>8s} {p1s:>10s}  "
          f"{d2s:12s} {l2s:>8s} {p2s:>10s}  {order:>8s}  {gaps:>10s}{flag}")

print(f"\nOrder OK (S1 before S2): {p_order_ok}/{len(peaks_df)}")
print(f"FLIP    (S2 before S1): {p_order_flip}/{len(peaks_df)}")
print(f"MISS   (one missing)  : {p_miss}/{len(peaks_df)}")

# ── EMA30/SMA15 orphan signals (fires without Stage1) ────────────────────
print("\n\n" + "="*80)
print("ORPHAN SIGNALS — EMA30/SMA15 fires WITHOUT Stage1 having fired in prior 90d")
print("(these are the 'noise' signals in a 2-stage context)")
print("="*80)

def orphan_signals(fast_cross, slow_cross, direction, gate_window=90):
    """
    Count how many fast_cross signals have NO preceding slow_cross
    within gate_window days before them.
    """
    fast = fast_cross[fast_cross["direction"]==direction].reset_index(drop=True)
    slow = slow_cross[slow_cross["direction"]==direction].reset_index(drop=True)
    orphans = []
    for _, row in fast.iterrows():
        d = row["date"]
        preceding = slow[
            (slow["date"] >= d - pd.Timedelta(days=gate_window)) &
            (slow["date"] <  d)
        ]
        if preceding.empty:
            orphans.append({"date": d, "price": row["price"]})
    return pd.DataFrame(orphans)

# Bottom: Stage1=EMA55, Stage2=EMA30
orp_up = orphan_signals(c30_15, c55_35, "UP", gate_window=90)
total_up30 = (c30_15["direction"]=="UP").sum()
print(f"\nUP (bottom): EMA30/SMA15 total={total_up30} | "
      f"orphans (no EMA55/SMA35 in prior 90d)={len(orp_up)} "
      f"({len(orp_up)/total_up30*100:.0f}%)")
if not orp_up.empty:
    orp_up["date"]  = orp_up["date"].dt.strftime("%Y-%m-%d")
    orp_up["price"] = orp_up["price"].apply(lambda x: f"${x:,.0f}")
    print(orp_up.to_string(index=False))

# Peak: Stage1=EMA90, Stage2=EMA30
orp_dn = orphan_signals(c30_15, c90_80, "DOWN", gate_window=90)
total_dn30 = (c30_15["direction"]=="DOWN").sum()
print(f"\nDOWN (peak): EMA30/SMA15 total={total_dn30} | "
      f"orphans (no EMA90/SMA80 in prior 90d)={len(orp_dn)} "
      f"({len(orp_dn)/total_dn30*100:.0f}%)")
if not orp_dn.empty:
    orp_dn["date"]  = orp_dn["date"].dt.strftime("%Y-%m-%d")
    orp_dn["price"] = orp_dn["price"].apply(lambda x: f"${x:,.0f}")
    print(orp_dn.to_string(index=False))
