import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pandas as pd
import numpy as np

df = pd.read_csv("data_price_level.csv", parse_dates=["date"])
df = df[["date", "btc_price", "MVRV 0σ"]].dropna()
df = df[df["date"] >= "2016-01-01"].copy()

# Bull market periods (approximate, based on cycle structure)
bull_periods = [
    ("2016 Bull",    "2016-01-01", "2018-01-07"),
    ("2019 Mini",    "2019-01-01", "2019-07-26"),
    ("2020-2021 Bull","2020-10-01", "2021-11-10"),
    ("2023-2024 Bull","2023-01-01", "2024-12-17"),
]

print("=" * 70)
print("MVRV 0std ANALYSIS - Hari BTC Price < MVRV 0std saat Bull Market")
print("=" * 70)

all_dips = []

for name, start, end in bull_periods:
    mask = (df["date"] >= start) & (df["date"] <= end)
    period = df[mask].copy()

    below = period[period["btc_price"] < period["MVRV 0σ"]]
    total_days = len(period)
    below_days = len(below)
    pct = below_days / total_days * 100 if total_days > 0 else 0

    print(f"\n{'─'*70}")
    print(f"Period   : {name} ({start} → {end})")
    print(f"Total    : {total_days} hari")
    print(f"< MVRV 0σ: {below_days} hari ({pct:.1f}%)")

    if below_days > 0:
        # Group consecutive days into dip episodes
        below_idx = below.index.tolist()
        episodes = []
        if below_idx:
            ep_start = below_idx[0]
            ep_end = below_idx[0]
            for i in below_idx[1:]:
                if i - ep_end <= 3:  # allow 3-day gap
                    ep_end = i
                else:
                    episodes.append((ep_start, ep_end))
                    ep_start = i
                    ep_end = i
            episodes.append((ep_start, ep_end))

        print(f"Episodes : {len(episodes)} dip episode")
        for ep_s, ep_e in episodes:
            ep_data = period.loc[ep_s:ep_e]
            ep_below = ep_data[ep_data["btc_price"] < ep_data["MVRV 0σ"]]
            min_ratio = (ep_data["btc_price"] / ep_data["MVRV 0σ"]).min()
            d_start = ep_data["date"].iloc[0].strftime("%Y-%m-%d")
            d_end   = ep_data["date"].iloc[-1].strftime("%Y-%m-%d")
            n_below = len(ep_below)
            print(f"   {d_start} → {d_end} | {n_below} hari di bawah | min ratio {min_ratio:.3f}")

    all_dips.append({
        "period": name,
        "total_days": total_days,
        "below_days": below_days,
        "pct": pct
    })

print(f"\n{'='*70}")
print("SUMMARY")
print(f"{'Period':<22} {'Total':>7} {'< 0σ':>7} {'%':>6}")
print(f"{'─'*22} {'─'*7} {'─'*7} {'─'*6}")
total_all = sum(d["total_days"] for d in all_dips)
below_all = sum(d["below_days"] for d in all_dips)
for d in all_dips:
    print(f"{d['period']:<22} {d['total_days']:>7} {d['below_days']:>7} {d['pct']:>5.1f}%")
print(f"{'─'*22} {'─'*7} {'─'*7} {'─'*6}")
print(f"{'TOTAL':<22} {total_all:>7} {below_all:>7} {below_all/total_all*100:>5.1f}%")
print()
