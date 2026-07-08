"""
BB(28,1.5) + BB(28,2.0) dengan price filter:
  - price nyentuh/turun ke STH Realized Price  (px/STH_RP <= threshold)
  - price nyentuh/turun ke MVRV 0sigma         (px/MVRV0s <= threshold)
Filter window: berapa hari sekitar signal tanggal harga menyentuh level
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding="utf-8")

# ── Load & merge ──────────────────────────────────────────────────────────────
mom = pd.read_csv("data_momentum.csv",    parse_dates=["date"])
pl  = pd.read_csv("data_price_level.csv", parse_dates=["date"])

mom = mom.sort_values("date").reset_index(drop=True)
pl  = pl.sort_values("date").reset_index(drop=True)

# Rename level columns (encoding-safe by position)
pl_cols = pl.columns.tolist()
# col 2=sth_cost_basis, col 7=MVRV_0sigma, col 12=cum_pl_price
pl = pl.rename(columns={
    pl_cols[2]:  "sth_rp",
    pl_cols[7]:  "mvrv_0s",
    pl_cols[12]: "cum_pl",
})

df = mom[["date","btc_price","sth_sopr"]].merge(
     pl[["date","sth_rp","mvrv_0s","cum_pl"]], on="date", how="inner")
df = df.dropna().reset_index(drop=True)

# ── Market regimes ────────────────────────────────────────────────────────────
PERIOD_DEFS = {
    "2023-2025": dict(
        start="2023-01-01", end="2026-06-17",
        bull=[("2023-01-01","2025-10-31")],
        bear=[("2025-11-01","2026-06-17")],
    ),
    "2016-2022": dict(
        start="2016-01-01", end="2022-12-31",
        bull=[("2016-01-01","2017-12-17"),("2019-01-01","2019-06-26"),("2020-03-13","2021-11-10")],
        bear=[("2017-12-18","2019-01-31"),("2021-11-11","2022-12-31")],
    ),
}

BULL_DIPS = {
    "2023-2025": [
        "2023-03-10","2023-04-21","2023-05-24","2023-06-14","2023-08-26","2023-09-11",
        "2024-01-22","2024-03-19","2024-04-17","2024-05-01","2024-07-07","2024-08-05",
        "2024-09-06","2025-01-09","2025-03-10","2025-04-08","2025-08-31","2025-10-17",
    ],
    "2016-2022": [
        "2016-01-15","2016-01-31","2016-06-22","2016-07-07","2016-08-02",
        "2017-01-11","2017-03-10","2017-03-24","2017-05-27","2017-06-15",
        "2017-07-16","2017-09-14","2017-11-12","2017-12-10",
        "2019-02-07","2019-05-18","2019-06-09",
        "2020-03-16","2020-05-11","2020-05-26","2020-06-27",
        "2020-09-08","2020-09-23","2020-11-27",
        "2021-01-12","2021-01-27","2021-02-28","2021-03-25",
        "2021-04-25","2021-06-08","2021-07-20","2021-09-21","2021-10-27",
    ],
}

def in_ranges(d, ranges):
    return any(pd.Timestamp(s) <= d <= pd.Timestamp(e) for s,e in ranges)

def compute_bb(s, period, std):
    sma = s.rolling(period, min_periods=period).mean()
    sig = s.rolling(period, min_periods=period).std()
    return sma - std*sig

def get_signals(df_in, period, std, bull_ranges, bear_ranges, dedup=7):
    lower = compute_bb(df_in["sth_sopr"], period, std)
    below = df_in["sth_sopr"] < lower
    first = below & ~below.shift(1, fill_value=False)
    bull_mask = first & df_in["date"].apply(lambda d: in_ranges(d, bull_ranges))
    bear_mask = first & df_in["date"].apply(lambda d: in_ranges(d, bear_ranges))
    def dd(dates):
        out = []
        for d in dates:
            if not out or (d-out[-1]).days > dedup: out.append(d)
        return out
    return dd(df_in[bull_mask]["date"].tolist()), dd(df_in[bear_mask]["date"].tolist())

def fwd_gain(df_in, sig_date, days=30):
    entry = df_in[df_in["date"]==sig_date]["btc_price"]
    if entry.empty: return None
    fut = df_in[(df_in["date"]>sig_date)&(df_in["date"]<=sig_date+pd.Timedelta(days=days))]
    if fut.empty: return None
    return (fut["btc_price"].max()/entry.iloc[0]-1)*100

def price_touched_level(df_in, sig_date, col, threshold=1.05, window=14):
    """
    Check if price/col <= threshold anywhere in [sig_date - window, sig_date + window].
    Returns True jika harga nyentuh/di bawah level * threshold.
    """
    t1 = sig_date - pd.Timedelta(days=window)
    t2 = sig_date + pd.Timedelta(days=window)
    sub = df_in[(df_in["date"]>=t1)&(df_in["date"]<=t2)].copy()
    if sub.empty: return False
    ratio = sub["btc_price"] / sub[col]
    return ratio.min() <= threshold

def evaluate_with_filter(df_in, period, std, bull_ranges, bear_ranges, dip_dates,
                          filter_cols=None, filter_threshold=1.05, filter_window=14):
    """
    filter_cols: None (no filter), or list of column names (OR logic — any one is enough).
    """
    bull_sigs, bear_sigs = get_signals(df_in, period, std, bull_ranges, bear_ranges)

    # Apply price filter to bull signals
    if filter_cols:
        filtered_bull = [s for s in bull_sigs
                         if any(price_touched_level(df_in, s, col,
                                                    filter_threshold, filter_window)
                                for col in filter_cols)]
    else:
        filtered_bull = bull_sigs

    # Bear FP — apply same filter
    if filter_cols:
        filtered_bear = [s for s in bear_sigs
                         if any(price_touched_level(df_in, s, col,
                                                    filter_threshold, filter_window)
                                for col in filter_cols)]
    else:
        filtered_bear = bear_sigs

    # Recall & precision
    dips_covered, true_sigs, gains = set(), 0, []
    for s in filtered_bull:
        for i, dip_dt in enumerate(dip_dates):
            delta = (dip_dt - s).days
            if -7 <= delta <= 21:
                dips_covered.add(i); true_sigs += 1; break
        g = fwd_gain(df_in, s, 30)
        if g is not None: gains.append(g)

    recall = len(dips_covered)/len(dip_dates)*100 if len(dip_dates)>0 else 0
    prec   = true_sigs/len(filtered_bull)*100 if filtered_bull else 0
    return dict(
        recall=round(recall,1), precision=round(prec,1),
        n_bull=len(filtered_bull), n_bear_fp=len(filtered_bear),
        avg_g30=round(np.mean(gains),1) if gains else None,
        sigs=filtered_bull
    )

# ── Run analysis ──────────────────────────────────────────────────────────────
CONFIGS = [
    # (label, period, std, filter_cols, threshold, window)
    ("No filter (baseline)",                       28, 1.5, None,               1.05, 14),
    ("+ STH RP only  (px/STH ≤ 1.05, ±14d)",      28, 1.5, ["sth_rp"],         1.05, 14),
    ("+ MVRV 0σ only  (px/MVRV0s ≤ 1.05, ±14d)", 28, 1.5, ["mvrv_0s"],        1.05, 14),
    ("+ STH OR MVRV  (≤ 1.05, ±14d)",             28, 1.5, ["sth_rp","mvrv_0s"],1.05, 14),
    ("+ STH OR MVRV  (≤ 1.02, ±14d)",             28, 1.5, ["sth_rp","mvrv_0s"],1.02, 14),
    ("+ STH OR MVRV  (≤ 1.05, ±7d)",              28, 1.5, ["sth_rp","mvrv_0s"],1.05,  7),
    ("+ STH OR MVRV  (≤ 1.10, ±14d)",             28, 1.5, ["sth_rp","mvrv_0s"],1.10, 14),
    ("─────────── BB(28,2.0) ───────────",         None, None, None, None, None),
    ("No filter (baseline)",                       28, 2.0, None,               1.05, 14),
    ("+ STH RP only  (px/STH ≤ 1.05, ±14d)",      28, 2.0, ["sth_rp"],         1.05, 14),
    ("+ MVRV 0σ only  (px/MVRV0s ≤ 1.05, ±14d)", 28, 2.0, ["mvrv_0s"],        1.05, 14),
    ("+ STH OR MVRV  (≤ 1.05, ±14d)",             28, 2.0, ["sth_rp","mvrv_0s"],1.05, 14),
    ("+ STH OR MVRV  (≤ 1.02, ±14d)",             28, 2.0, ["sth_rp","mvrv_0s"],1.02, 14),
    ("+ STH OR MVRV  (≤ 1.05, ±7d)",              28, 2.0, ["sth_rp","mvrv_0s"],1.05,  7),
    ("+ STH OR MVRV  (≤ 1.10, ±14d)",             28, 2.0, ["sth_rp","mvrv_0s"],1.10, 14),
]

for pname, pdef in PERIOD_DEFS.items():
    df_p = df[(df["date"]>=pdef["start"])&(df["date"]<=pdef["end"])].copy().reset_index(drop=True)
    dip_dates = pd.to_datetime(BULL_DIPS[pname])

    print(f"\n{'='*90}")
    print(f"  PERIOD: {pname}  |  {len(dip_dates)} identified bull dips")
    print(f"{'='*90}")
    print(f"  {'Config':<48} {'Recall':>7} {'Prec':>7} {'G30d':>7} {'Sigs':>6} {'BearFP':>8}")
    print(f"  {'-'*48} {'-'*7} {'-'*7} {'-'*7} {'-'*6} {'-'*8}")

    for cfg in CONFIGS:
        label, period, std, fcols, fthresh, fwin = cfg
        if period is None:
            print(f"\n  {label}")
            continue
        r = evaluate_with_filter(df_p, period, std, pdef["bull"], pdef["bear"],
                                  dip_dates, fcols, fthresh, fwin)
        g30 = f"+{r['avg_g30']}%" if r["avg_g30"] else "—"
        fp_delta = ""
        print(f"  {label:<48} {r['recall']:>6}% {r['precision']:>6}% {g30:>7} {r['n_bull']:>6} {r['n_bear_fp']:>8}")

# ── Bonus: per-signal breakdown untuk kombinasi terbaik ──────────────────────
print(f"\n{'='*90}")
print("  DETAIL — BB(28,1.5) + STH OR MVRV (≤1.05, ±14d)  |  2023-2025")
print(f"{'='*90}")
pdef = PERIOD_DEFS["2023-2025"]
df_p = df[(df["date"]>=pdef["start"])&(df["date"]<=pdef["end"])].copy().reset_index(drop=True)
dip_dates = pd.to_datetime(BULL_DIPS["2023-2025"])

r = evaluate_with_filter(df_p, 28, 1.5, pdef["bull"], pdef["bear"], dip_dates,
                          ["sth_rp","mvrv_0s"], 1.05, 14)

print(f"\n  Bull signals yang LOLOS filter ({r['n_bull']}):")
print(f"  {'Date':12} {'Price':>10} {'px/STH':>8} {'px/MVRV0s':>10} {'Filter trigger':20} {'G30d':>7}")
print(f"  {'-'*12} {'-'*10} {'-'*8} {'-'*10} {'-'*20} {'-'*7}")
for s in r["sigs"]:
    win = df_p[(df_p["date"]>=s-pd.Timedelta(days=14))&(df_p["date"]<=s+pd.Timedelta(days=14))]
    if win.empty: continue
    px    = df_p[df_p["date"]==s]["btc_price"].iloc[0]
    ratio_sth  = (win["btc_price"]/win["sth_rp"]).min()
    ratio_mvrv = (win["btc_price"]/win["mvrv_0s"]).min()
    trig = []
    if ratio_sth  <= 1.05: trig.append(f"STH({ratio_sth:.3f})")
    if ratio_mvrv <= 1.05: trig.append(f"MVRV0s({ratio_mvrv:.3f})")
    g = fwd_gain(df_p, s, 30)
    g_str = f"+{g:.0f}%" if g and g>=0 else (f"{g:.0f}%" if g else "—")
    print(f"  {str(s.date()):12} ${px:>9,.0f} {ratio_sth:>8.3f} {ratio_mvrv:>10.3f} {', '.join(trig):<20} {g_str:>7}")

# Signals yang DITOLAK filter
bull_raw, _ = get_signals(df_p, 28, 1.5, pdef["bull"], pdef["bear"])
rejected = [s for s in bull_raw if s not in r["sigs"]]
print(f"\n  Signals yang DITOLAK filter ({len(rejected)}) — price tidak nyentuh level:")
print(f"  {'Date':12} {'Price':>10} {'px/STH_min':>12} {'px/MVRV0s_min':>14}")
for s in rejected:
    win = df_p[(df_p["date"]>=s-pd.Timedelta(days=14))&(df_p["date"]<=s+pd.Timedelta(days=14))]
    if win.empty: continue
    px         = df_p[df_p["date"]==s]["btc_price"].iloc[0]
    ratio_sth  = (win["btc_price"]/win["sth_rp"]).min()
    ratio_mvrv = (win["btc_price"]/win["mvrv_0s"]).min()
    print(f"  {str(s.date()):12} ${px:>9,.0f} {ratio_sth:>12.3f} {ratio_mvrv:>14.3f}")
