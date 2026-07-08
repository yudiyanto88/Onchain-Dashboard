"""
Combined trigger: BB(28,1.5) atau BB(28,2.0) fire SAAT price <= STH RP
Logika: STH-SOPR tertekan + STH aggregate underwater = double stress
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
pl  = pl.rename(columns={pl.columns[2]: "sth_rp", pl.columns[7]: "mvrv_0s"})

df = mom[["date","btc_price","sth_sopr"]].merge(
     pl[["date","sth_rp","mvrv_0s"]], on="date", how="inner")
df = df.dropna().reset_index(drop=True)
df["px_sth_ratio"] = df["btc_price"] / df["sth_rp"]

# ── Regime definitions ────────────────────────────────────────────────────────
PERIODS = {
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
    "2023-2025": pd.to_datetime([
        "2023-03-10","2023-04-21","2023-05-24","2023-06-14","2023-08-26","2023-09-11",
        "2024-01-22","2024-03-19","2024-04-17","2024-05-01","2024-07-07","2024-08-05",
        "2024-09-06","2025-01-09","2025-03-10","2025-04-08","2025-08-31","2025-10-17",
    ]),
    "2016-2022": pd.to_datetime([
        "2016-01-15","2016-01-31","2016-06-22","2016-07-07","2016-08-02",
        "2017-01-11","2017-03-10","2017-03-24","2017-05-27","2017-06-15",
        "2017-07-16","2017-09-14","2017-11-12","2017-12-10",
        "2019-02-07","2019-05-18","2019-06-09",
        "2020-03-16","2020-05-11","2020-05-26","2020-06-27",
        "2020-09-08","2020-09-23","2020-11-27",
        "2021-01-12","2021-01-27","2021-02-28","2021-03-25",
        "2021-04-25","2021-06-08","2021-07-20","2021-09-21","2021-10-27",
    ]),
}

def in_ranges(d, ranges):
    return any(pd.Timestamp(s) <= d <= pd.Timestamp(e) for s,e in ranges)

def compute_bb_lower(series, period, std):
    sma = series.rolling(period, min_periods=period).mean()
    sig = series.rolling(period, min_periods=period).std()
    return sma - std * sig

def get_first_episodes(df_in, period, std, bull_ranges, bear_ranges, dedup=7):
    lower = compute_bb_lower(df_in["sth_sopr"], period, std)
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

def fwd(df_in, sig_date, days):
    entry = df_in[df_in["date"]==sig_date]["btc_price"]
    if entry.empty: return None
    fut = df_in[(df_in["date"]>sig_date)&(df_in["date"]<=sig_date+pd.Timedelta(days=days))]
    if fut.empty: return None
    return (fut["btc_price"].max()/entry.iloc[0]-1)*100

def evaluate(df_in, period, std, bull_ranges, bear_ranges, dip_dates,
             px_sth_threshold=None):
    """
    px_sth_threshold: None = no filter
                      float = price/STH_RP must be <= this at signal date
    """
    bull_raw, bear_raw = get_first_episodes(df_in, period, std, bull_ranges, bear_ranges)

    def apply_filter(sig_dates):
        if px_sth_threshold is None:
            return sig_dates
        out = []
        for s in sig_dates:
            row = df_in[df_in["date"]==s]
            if row.empty: continue
            ratio = row["px_sth_ratio"].iloc[0]
            if ratio <= px_sth_threshold:
                out.append(s)
        return out

    bull_sigs = apply_filter(bull_raw)
    bear_sigs = apply_filter(bear_raw)

    dips_covered, true_sigs, g14, g30, g60 = set(), 0, [], [], []
    for s in bull_sigs:
        for i, dip_dt in enumerate(dip_dates):
            if -7 <= (dip_dt-s).days <= 21:
                dips_covered.add(i); true_sigs += 1; break
        for gd, gl in [(14,g14),(30,g30),(60,g60)]:
            g = fwd(df_in, s, gd)
            if g is not None: gl.append(g)

    n = len(dip_dates)
    recall = len(dips_covered)/n*100 if n>0 else 0
    prec   = true_sigs/len(bull_sigs)*100 if bull_sigs else 0
    return dict(
        recall=round(recall,1), precision=round(prec,1),
        n_bull=len(bull_sigs), n_bear_fp=len(bear_sigs),
        avg_g14=round(np.mean(g14),1) if g14 else None,
        avg_g30=round(np.mean(g30),1) if g30 else None,
        avg_g60=round(np.mean(g60),1) if g60 else None,
        bull_sigs=bull_sigs, bear_sigs=bear_sigs,
    )

# ── Main comparison table ─────────────────────────────────────────────────────
CONFIGS = [
    ("BB(28,1.5) — no filter",              28, 1.5, None),
    ("BB(28,1.5) + price ≤ STH RP",         28, 1.5, 1.00),
    ("BB(28,1.5) + price ≤ 1.02×STH RP",   28, 1.5, 1.02),
    ("──────────────────────────────────────────────────", None, None, None),
    ("BB(28,2.0) — no filter",              28, 2.0, None),
    ("BB(28,2.0) + price ≤ STH RP",         28, 2.0, 1.00),
    ("BB(28,2.0) + price ≤ 1.02×STH RP",   28, 2.0, 1.02),
    ("──────────────────────────────────────────────────", None, None, None),
    ("DUAL — BB(28,1.5) early, (28,2.0) confirm — both price ≤ STH RP",
     "dual", None, 1.00),
]

for pname, pdef in PERIODS.items():
    df_p = df[(df["date"]>=pdef["start"])&(df["date"]<=pdef["end"])].copy().reset_index(drop=True)
    dips = BULL_DIPS[pname]

    print(f"\n{'='*95}")
    print(f"  {pname}  |  {len(dips)} bull dips")
    print(f"{'='*95}")
    print(f"  {'Config':<52} {'Recall':>7} {'Prec':>7} {'G14d':>6} {'G30d':>6} {'G60d':>6} {'Sigs':>5} {'BearFP':>7}")
    print(f"  {'-'*52} {'-'*7} {'-'*7} {'-'*6} {'-'*6} {'-'*6} {'-'*5} {'-'*7}")

    for cfg in CONFIGS:
        label, period, std, thresh = cfg
        if period is None:
            print(f"\n  {label}")
            continue
        if period == "dual":
            # Dual: union of BB(28,1.5) and BB(28,2.0) both filtered
            r1 = evaluate(df_p, 28, 1.5, pdef["bull"], pdef["bear"], dips, thresh)
            r2 = evaluate(df_p, 28, 2.0, pdef["bull"], pdef["bear"], dips, thresh)
            # For dual, treat BB(28,2.0) as "upgrade" — evaluate separately
            # Dips covered by either
            dips_covered = set()
            for s in r1["bull_sigs"]+r2["bull_sigs"]:
                for i,d in enumerate(dips):
                    if -7<=(d-s).days<=21: dips_covered.add(i)
            recall = len(dips_covered)/len(dips)*100 if len(dips)>0 else 0
            print(f"\n  {label}")
            print(f"    Early (BB28,1.5): {r1['n_bull']} sigs | Recall {r1['recall']}% | Prec {r1['precision']}% | G30d +{r1['avg_g30']}%")
            print(f"    Confirm(BB28,2.0): {r2['n_bull']} sigs | Recall {r2['recall']}% | Prec {r2['precision']}% | G30d +{r2['avg_g30']}%")
            print(f"    Combined coverage: {round(recall,1)}% of {len(dips)} dips")
            print(f"    Bear FP early: {r1['n_bear_fp']}  |  Bear FP confirm: {r2['n_bear_fp']}")
            continue

        r = evaluate(df_p, period, std, pdef["bull"], pdef["bear"], dips, thresh)
        g14 = f"+{r['avg_g14']}%" if r["avg_g14"] else "—"
        g30 = f"+{r['avg_g30']}%" if r["avg_g30"] else "—"
        g60 = f"+{r['avg_g60']}%" if r["avg_g60"] else "—"
        print(f"  {label:<52} {r['recall']:>6}% {r['precision']:>6}% {g14:>6} {g30:>6} {g60:>6} {r['n_bull']:>5} {r['n_bear_fp']:>7}")

# ── Per-signal detail untuk BB(28,1.5) + price ≤ STH RP, 2023-2025 ──────────
print(f"\n{'='*95}")
print("  DETAIL  BB(28,1.5) + price ≤ STH RP  |  2023-2025")
print(f"{'='*95}")

pdef = PERIODS["2023-2025"]
df_p = df[(df["date"]>=pdef["start"])&(df["date"]<=pdef["end"])].copy().reset_index(drop=True)
dips = BULL_DIPS["2023-2025"]
r = evaluate(df_p, 28, 1.5, pdef["bull"], pdef["bear"], dips, 1.00)

# Identify which dips were MISSED
matched_dip_idx = set()
for s in r["bull_sigs"]:
    for i, d in enumerate(dips):
        if -7 <= (d-s).days <= 21:
            matched_dip_idx.add(i); break
missed_dips = [dips[i] for i in range(len(dips)) if i not in matched_dip_idx]

print(f"\n  Bull signals yang LOLOS ({r['n_bull']}):")
print(f"  {'Date':12} {'Price':>10} {'px/STH':>8} {'BB_lower':>9} {'STH-SOPR':>10} {'G14d':>6} {'G30d':>6} {'G60d':>6}")
print(f"  {'-'*12} {'-'*10} {'-'*8} {'-'*9} {'-'*10} {'-'*6} {'-'*6} {'-'*6}")
for s in r["bull_sigs"]:
    row = df_p[df_p["date"]==s].iloc[0]
    lower_val = compute_bb_lower(df_p["sth_sopr"], 28, 1.5)[df_p[df_p["date"]==s].index[0]]
    g14 = fwd(df_p, s, 14); g30 = fwd(df_p, s, 30); g60 = fwd(df_p, s, 60)
    regime = "BULL" if in_ranges(s, pdef["bull"]) else "BEAR"
    print(f"  {str(s.date()):12} ${row['btc_price']:>9,.0f} {row['px_sth_ratio']:>8.3f} "
          f"{lower_val:>9.4f} {row['sth_sopr']:>10.4f} "
          f"{'+'+str(round(g14,0))[:-2]+'%' if g14 else '—':>6} "
          f"{'+'+str(round(g30,0))[:-2]+'%' if g30 else '—':>6} "
          f"{'+'+str(round(g60,0))[:-2]+'%' if g60 else '—':>6}")

print(f"\n  Dips yang TIDAK tercakup ({len(missed_dips)}) — price masih > STH RP saat BB fire:")
for d in missed_dips:
    row = df_p[df_p["date"]==d]
    if row.empty: row = df_p[df_p["date"]<=d].tail(1)
    r2 = row.iloc[0]
    print(f"  {str(d.date()):12} ${r2['btc_price']:>9,.0f} | px/STH at dip date = {r2['px_sth_ratio']:.3f}")

print(f"\n  Bear FPs yang masih fire ({r['n_bear_fp']}) — price sudah < STH RP di bear:")
print(f"  {'Date':12} {'Price':>10} {'px/STH':>8} {'STH-SOPR':>10}")
for s in r["bear_sigs"]:
    row = df_p[df_p["date"]==s].iloc[0]
    print(f"  {str(s.date()):12} ${row['btc_price']:>9,.0f} {row['px_sth_ratio']:>8.3f} {row['sth_sopr']:>10.4f}")

# ── BB(28,2.0) detail juga ────────────────────────────────────────────────────
print(f"\n{'='*95}")
print("  DETAIL  BB(28,2.0) + price ≤ STH RP  |  2023-2025")
print(f"{'='*95}")
r2 = evaluate(df_p, 28, 2.0, pdef["bull"], pdef["bear"], dips, 1.00)
print(f"\n  Bull signals yang LOLOS ({r2['n_bull']}):")
print(f"  {'Date':12} {'Price':>10} {'px/STH':>8} {'STH-SOPR':>10} {'G14d':>6} {'G30d':>6} {'G60d':>6}")
print(f"  {'-'*12} {'-'*10} {'-'*8} {'-'*10} {'-'*6} {'-'*6} {'-'*6}")
for s in r2["bull_sigs"]:
    row = df_p[df_p["date"]==s].iloc[0]
    g14 = fwd(df_p, s, 14); g30 = fwd(df_p, s, 30); g60 = fwd(df_p, s, 60)
    print(f"  {str(s.date()):12} ${row['btc_price']:>9,.0f} {row['px_sth_ratio']:>8.3f} "
          f"{row['sth_sopr']:>10.4f} "
          f"{'+'+str(round(g14,0))[:-2]+'%' if g14 else '—':>6} "
          f"{'+'+str(round(g30,0))[:-2]+'%' if g30 else '—':>6} "
          f"{'+'+str(round(g60,0))[:-2]+'%' if g60 else '—':>6}")
print(f"\n  Bear FPs ({r2['n_bear_fp']}):")
for s in r2["bear_sigs"]:
    row = df_p[df_p["date"]==s].iloc[0]
    print(f"  {str(s.date()):12} ${row['btc_price']:>9,.0f} px/STH={row['px_sth_ratio']:.3f}  STH-SOPR={row['sth_sopr']:.4f}")
