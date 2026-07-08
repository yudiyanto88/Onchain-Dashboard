import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────────
mom  = pd.read_csv("data_momentum.csv",    parse_dates=["date"])
aviv = pd.read_csv("data_aviv.csv",        parse_dates=["date"])

df = mom[["date", "btc_price", "sth_sopr"]].merge(
     aviv[["date", "aviv_upper_0.5sd", "price_at_aviv_upper_0.5sd"]], on="date", how="inner")
df = df.sort_values("date").reset_index(drop=True)

# ── Signal B/C: STH-SOPR MA90 cross below MA90-MA60 ──────────────────────────
df["ma90"]    = df["sth_sopr"].rolling(90,  min_periods=90).mean()
df["ma90_60"] = df["ma90"].rolling(60, min_periods=60).mean()
df["gap"]     = df["ma90"] - df["ma90_60"]

# Bearish cross = gap goes from positive to negative
df["bear_cross"] = (df["gap"] < 0) & (df["gap"].shift(1) >= 0)

# ── AVIV Upper 0.5sd break: price drops below price_at_aviv_upper_0.5sd ──────
df["aviv_break"] = (df["btc_price"] < df["price_at_aviv_upper_0.5sd"]) & \
                   (df["btc_price"].shift(1) >= df["price_at_aviv_upper_0.5sd"].shift(1))

# ── Cycle peaks to analyze ────────────────────────────────────────────────────
peaks = [
    ("2017 Cycle Peak", "2017-12-17", "2018-01-01", "2019-03-01"),
    ("2021 Cycle Peak", "2021-11-10", "2021-11-01", "2023-01-01"),
    ("2025 Cycle Peak", "2025-10-20", "2025-10-01", "2026-06-22"),  # approximate
]

print("=" * 75)
print("SIGNAL B/C vs AVIV UPPER 0.5sd BREAK — Timing After Cycle Peak")
print("Signal B/C : STH-SOPR MA90 bearish cross (crosses below MA90-60)")
print("AVIV Break : BTC price drops below AVIV Upper 0.5sd level")
print("=" * 75)

for name, peak_date, window_start, window_end in peaks:
    peak_dt = pd.Timestamp(peak_date)
    ws = pd.Timestamp(window_start)
    we = pd.Timestamp(window_end)

    window = df[(df["date"] >= ws) & (df["date"] <= we)].copy()
    post   = df[(df["date"] >= peak_dt) & (df["date"] <= we)].copy()

    # Find signal B/C fires after peak
    sig_bc = post[post["bear_cross"] == True]["date"].tolist()

    # Find AVIV breaks after peak
    aviv_breaks = post[post["aviv_break"] == True]["date"].tolist()

    print(f"\n{'─' * 75}")
    print(f"  {name}  |  Peak date: {peak_date}")
    print(f"  Peak price: ${post.iloc[0]['btc_price']:,.0f}")
    print()

    if sig_bc:
        for i, d in enumerate(sig_bc[:5]):
            days = (d - peak_dt).days
            price = post[post["date"] == d]["btc_price"].values[0]
            print(f"  Signal B/C  #{i+1}:  {d.strftime('%Y-%m-%d')}  (+{days}d post-peak)  price: ${price:,.0f}")
    else:
        print("  Signal B/C  : -- tidak ada dalam window ini")

    print()

    if aviv_breaks:
        for i, d in enumerate(aviv_breaks[:5]):
            days = (d - peak_dt).days
            price = post[post["date"] == d]["btc_price"].values[0]
            level = post[post["date"] == d]["price_at_aviv_upper_0.5sd"].values[0]
            print(f"  AVIV Break  #{i+1}:  {d.strftime('%Y-%m-%d')}  (+{days}d post-peak)  price: ${price:,.0f}  level: ${level:,.0f}")
    else:
        print("  AVIV Break  : -- tidak ada dalam window ini")

    # Who was first?
    if sig_bc and aviv_breaks:
        first_bc   = min(sig_bc)
        first_aviv = min(aviv_breaks)
        diff = (first_aviv - first_bc).days
        if diff > 0:
            print(f"\n  >> SIGNAL B/C LEBIH DULU  ({abs(diff)} hari sebelum AVIV break)")
        elif diff < 0:
            print(f"\n  >> AVIV BREAK LEBIH DULU  ({abs(diff)} hari sebelum Signal B/C)")
        else:
            print(f"\n  >> SAMA HARI")
    elif sig_bc and not aviv_breaks:
        print(f"\n  >> SIGNAL B/C LEBIH DULU (AVIV break tidak terjadi dalam window)")
    elif aviv_breaks and not sig_bc:
        print(f"\n  >> AVIV BREAK LEBIH DULU (Signal B/C tidak terjadi dalam window)")

# ── Also show full list of all bearish crosses ────────────────────────────────
print(f"\n{'=' * 75}")
print("SEMUA BEARISH CROSSES (Signal B/C Candidates) dalam data:")
all_bc = df[df["bear_cross"] == True][["date", "btc_price", "ma90", "ma90_60", "gap"]].copy()
all_bc = all_bc[all_bc["date"] >= "2014-01-01"]
for _, row in all_bc.iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}  price: ${row['btc_price']:>10,.0f}  gap: {row['gap']:.5f}")

print(f"\n{'=' * 75}")
print("SEMUA AVIV UPPER 0.5sd BREAKS dalam data (dari 2016):")
all_aviv = df[df["aviv_break"] == True][["date", "btc_price", "price_at_aviv_upper_0.5sd"]].copy()
all_aviv = all_aviv[all_aviv["date"] >= "2016-01-01"]
for _, row in all_aviv.iterrows():
    print(f"  {row['date'].strftime('%Y-%m-%d')}  price: ${row['btc_price']:>10,.0f}  AVIV level: ${row['price_at_aviv_upper_0.5sd']:>10,.0f}")
