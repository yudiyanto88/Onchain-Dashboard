"""
Cek 4 metrik kandidat untuk deteksi V-shape correction (dip-buy signal) di
6 tanggal referensi:
  - STH SOPR <= 0.98
  - aSOPR <= 0.98
  - STH % supply in loss >= 40%
  - RSI-14 + Bollinger Bands (SMA 30, 1.5 sigma) - RSI menyentuh/menembus lower band
"""

import pandas as pd
import numpy as np

EVENTS = [
    ("6-9 Mar 2023", "2023-03-06", "2023-03-09"),
    ("21 Jan 2024", "2024-01-21", "2024-01-21"),
    ("5 Sep 2020", "2020-09-05", "2020-09-05"),
    ("14-16 Jul 2017", "2017-07-14", "2017-07-16"),
    ("13-15 Sep 2017", "2017-09-13", "2017-09-15"),
    ("21 Sep 2021", "2021-09-21", "2021-09-21"),
]


def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


df = pd.read_csv("../data_master_all_metrics.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price"]).reset_index(drop=True)

df["rsi14"] = rsi(df["btc_price"], period=14)
bb_mid = df["rsi14"].rolling(30).mean()
bb_std = df["rsi14"].rolling(30).std()
df["rsi_bb_lower"] = bb_mid - 1.5 * bb_std
df["rsi_bb_upper"] = bb_mid + 1.5 * bb_std

for label, d0, d1 in EVENTS:
    mask = (df["date"] >= d0) & (df["date"] <= d1)
    sub = df.loc[mask, ["date", "btc_price", "sth_sopr", "asopr", "pct_sth_in_loss",
                         "rsi14", "rsi_bb_lower"]].copy()
    sub["sth_sopr_hit"] = sub["sth_sopr"] <= 0.98
    sub["asopr_hit"] = sub["asopr"] <= 0.98
    sub["sth_loss_hit"] = sub["pct_sth_in_loss"] >= 40
    sub["rsi_bb_hit"] = sub["rsi14"] <= sub["rsi_bb_lower"]

    print(f"=== {label} ===")
    for _, row in sub.iterrows():
        yn = lambda b: "YES" if b else "no"
        print(f"  {row['date'].date()} | price=${row['btc_price']:>9,.0f} | "
              f"STH-SOPR={row['sth_sopr']:.3f} [{yn(row['sth_sopr_hit'])}] | "
              f"aSOPR={row['asopr']:.3f} [{yn(row['asopr_hit'])}] | "
              f"STH%loss={row['pct_sth_in_loss']:.1f}% [{yn(row['sth_loss_hit'])}] | "
              f"RSI14={row['rsi14']:.1f} vs BB_low={row['rsi_bb_lower']:.1f} "
              f"[{yn(row['rsi_bb_hit'])}]")
    print()
