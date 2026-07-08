"""
False Positive / Noise Analysis per Pair
False positive = crossover fired but no major bottom/peak within N days after it
"""

import pandas as pd
import numpy as np

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"], usecols=["date","btc_price","asopr"]
)
df = (df.dropna(subset=["btc_price","asopr"])
       .query("btc_price > 0 and date >= '2013-01-01'")
       .sort_values("date").reset_index(drop=True))

# ── MAs ───────────────────────────────────────────────────────────────────
for span in [30,35,40,45,50,55,60,65,90]:
    df[f"EMA{span}"] = df["asopr"].ewm(span=span, adjust=False).mean()
for win in [15,20,25,30,35,80]:
    df[f"SMA{win}"] = df["asopr"].rolling(window=win, min_periods=win).mean()

PAIRS = [
    ("EMA30","SMA15"),("EMA35","SMA20"),("EMA40","SMA25"),("EMA45","SMA25"),
    ("EMA50","SMA30"),("EMA55","SMA35"),("EMA60","SMA30"),
    ("EMA65","SMA35"),("EMA90","SMA80"),
]

MIN_GAP = 30

def detect_crossovers(df, fast, slow):
    diff = df[fast] - df[slow]
    prev = diff.shift(1)
    up   = (diff > 0) & (prev <= 0)
    down = (diff < 0) & (prev >= 0)
    events, last_up, last_down = [], pd.Timestamp("2000-01-01"), pd.Timestamp("2000-01-01")
    for i in df.index:
        if pd.isna(df.at[i,fast]) or pd.isna(df.at[i,slow]): continue
        d = df.at[i,"date"]
        if up[i] and (d-last_up).days >= MIN_GAP:
            events.append({"date":d,"direction":"UP","price":df.at[i,"btc_price"]})
            last_up = d
        elif down[i] and (d-last_down).days >= MIN_GAP:
            events.append({"date":d,"direction":"DOWN","price":df.at[i,"btc_price"]})
            last_down = d
    return pd.DataFrame(events) if events else pd.DataFrame(columns=["date","direction","price"])

def find_major_events(df, window=90, min_drawdown=0.28, min_runup=0.65, merge_days=60):
    prices = df["btc_price"].values
    dates  = df["date"].values
    n = len(prices)
    bottoms, peaks = [], []
    for i in range(window, n-window):
        p    = prices[i]
        prev = prices[i-window:i]
        nxt  = prices[i+1:i+window+1]
        if p <= prev.min() and p <= nxt.min():
            dd = (prev.max()-p)/prev.max()
            if dd >= min_drawdown:
                bottoms.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
        if p >= prev.max() and p >= nxt.max():
            ru = (p-prev.min())/prev.min()
            if ru >= min_runup:
                peaks.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
    def merge(evts, keep):
        if not evts: return []
        evts = sorted(evts, key=lambda x: x["date"])
        merged, grp = [], [evts[0]]
        for e in evts[1:]:
            if (e["date"]-grp[-1]["date"]).days <= merge_days:
                grp.append(e)
            else:
                merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                              else max(grp,key=lambda x:x["price"]))
                grp = [e]
        merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                      else max(grp,key=lambda x:x["price"]))
        return merged
    return pd.DataFrame(merge(bottoms,"min")), pd.DataFrame(merge(peaks,"max"))

bottoms_df, peaks_df = find_major_events(df)
bottom_dates = bottoms_df["date"].values
peak_dates   = peaks_df["date"].values

# ── False Positive Logic ───────────────────────────────────────────────────
# A crossover is a TRUE POSITIVE if a major event occurs within WINDOW days AFTER it
# A crossover is a FALSE POSITIVE if no event occurs in that window
AFTER_WINDOW = 120  # days after crossover to look for event

def classify_crossovers(crosses, direction, event_dates, window=AFTER_WINDOW):
    dir_crosses = crosses[crosses["direction"]==direction].copy()
    results = []
    for _, row in dir_crosses.iterrows():
        cdate = row["date"]
        look_end = cdate + pd.Timedelta(days=window)
        # any event after this crossover within window?
        nearby = [d for d in event_dates
                  if pd.Timestamp(d) >= cdate and pd.Timestamp(d) <= look_end]
        results.append({
            "date": cdate,
            "price": row["price"],
            "true_positive": len(nearby) > 0,
            "days_to_event": (pd.Timestamp(nearby[0])-cdate).days if nearby else np.nan
        })
    return pd.DataFrame(results)

# ── Run for all pairs ──────────────────────────────────────────────────────
summary = []

for fast, slow in PAIRS:
    pair  = f"{fast}/{slow}"
    cross = detect_crossovers(df, fast, slow)

    # UP crossovers vs bottoms
    up   = classify_crossovers(cross, "UP",   bottom_dates)
    # DOWN crossovers vs peaks
    down = classify_crossovers(cross, "DOWN", peak_dates)

    def stats(cl):
        if cl.empty:
            return dict(total=0, tp=0, fp=0, precision=np.nan,
                        avg_days=np.nan, med_days=np.nan)
        tp  = cl["true_positive"].sum()
        fp  = len(cl) - tp
        avg = cl.loc[cl["true_positive"],"days_to_event"].mean()
        med = cl.loc[cl["true_positive"],"days_to_event"].median()
        return dict(total=len(cl), tp=int(tp), fp=int(fp),
                    precision=round(tp/len(cl)*100,1),
                    avg_days=round(avg,0), med_days=round(med,0))

    su = stats(up)
    sd = stats(down)

    summary.append({
        "Pair"          : pair,
        # UP (bottom)
        "UP Total"      : su["total"],
        "UP True+"      : su["tp"],
        "UP False+"     : su["fp"],
        "UP Precision"  : f"{su['precision']}%",
        "UP Avg Days"   : su["avg_days"],
        # DOWN (peak)
        "DN Total"      : sd["total"],
        "DN True+"      : sd["tp"],
        "DN False+"     : sd["fp"],
        "DN Precision"  : f"{sd['precision']}%",
        "DN Avg Days"   : sd["avg_days"],
    })

df_sum = pd.DataFrame(summary)

print("="*90)
print(f"FALSE POSITIVE ANALYSIS — window = {AFTER_WINDOW} days after crossover")
print("True+ = crossover followed by a major event within window")
print("False+ = crossover NOT followed by any major event within window")
print("Precision = True+ / Total crossovers")
print("="*90)

print("\n--- UP Crossover (looking for major BOTTOM within window) ---")
up_cols = ["Pair","UP Total","UP True+","UP False+","UP Precision","UP Avg Days"]
up_df = df_sum[up_cols].sort_values("UP False+", ascending=True)
print(up_df.to_string(index=False))

print("\n--- DOWN Crossover (looking for major PEAK within window) ---")
dn_cols = ["Pair","DN Total","DN True+","DN False+","DN Precision","DN Avg Days"]
dn_df = df_sum[dn_cols].sort_values("DN False+", ascending=True)
print(dn_df.to_string(index=False))

# ── Detail: setiap UP false+ dari EMA30/SMA15 ─────────────────────────────
print("\n\n" + "="*90)
print("DETAIL — EMA30/SMA15 UP crossovers yang FALSE POSITIVE (tidak diikuti bottom)")
print("="*90)
cross30 = detect_crossovers(df, "EMA30", "SMA15")
up30    = classify_crossovers(cross30, "UP", bottom_dates)
fp30    = up30[~up30["true_positive"]].copy()
fp30["date"]  = fp30["date"].dt.strftime("%Y-%m-%d")
fp30["price"] = fp30["price"].apply(lambda x: f"${x:,.0f}")
fp30 = fp30[["date","price"]].rename(columns={"date":"Cross Date","price":"BTC Price"})
print(fp30.to_string(index=False))

print(f"\nTotal UP false positives EMA30/SMA15: {len(fp30)}")
print(f"Total UP false positives EMA55/SMA35: ", end="")
cross55 = detect_crossovers(df, "EMA55", "SMA35")
up55    = classify_crossovers(cross55, "UP", bottom_dates)
print(int((~up55["true_positive"]).sum()))
print(f"Total UP false positives EMA90/SMA80: ", end="")
cross90 = detect_crossovers(df, "EMA90", "SMA80")
up90    = classify_crossovers(cross90, "UP", bottom_dates)
print(int((~up90["true_positive"]).sum()))

print("\n\n" + "="*90)
print("DETAIL — EMA30/SMA15 DOWN crossovers yang FALSE POSITIVE (tidak diikuti peak)")
print("="*90)
dn30 = classify_crossovers(cross30, "DOWN", peak_dates)
fp30d = dn30[~dn30["true_positive"]].copy()
fp30d["date"]  = fp30d["date"].dt.strftime("%Y-%m-%d")
fp30d["price"] = fp30d["price"].apply(lambda x: f"${x:,.0f}")
fp30d = fp30d[["date","price"]].rename(columns={"date":"Cross Date","price":"BTC Price"})
print(fp30d.to_string(index=False))
print(f"\nTotal DOWN false positives EMA30/SMA15: {len(fp30d)}")
