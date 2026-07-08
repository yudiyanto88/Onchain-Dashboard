"""
OCM STH Accumulation Bands - replikasi indikator ke-2 dari video YouTube
"This Bitcoin Signal Has Nailed EVERY Dip" (On-Chain Mind, dmxGLVVh3cc).

**Dikoreksi 5 Juli 2026 setelah nonton ulang video (v1 awal salah arah).**
Chart asli di video (title on-screen: "OCM STH Accumulation Bands") HANYA
punya band ke BAWAH dari cost basis - bukan cloud simetris ±sd seperti versi
pertama script ini. Struktur visual dari video:
  - Garis PUTIH (atas)  = STH Cost Basis, mengikuti price dengan lag
  - Garis KUNING/EMAS   = band pertama di bawah cost basis
  - Garis MERAH/PINK    = band kedua, lebih jauh di bawah cost basis
  - Fill olive antara putih-kuning, fill maroon antara kuning-merah
  - TIDAK ADA band di atas cost basis sama sekali (dicek: bahkan di cycle
    peak Okt 2025, tidak ada shading di atas candle) - indikator ini murni
    buy-zone detector, bukan overbought/distribution detector.
Formula asli tetap tidak diungkap (proprietary) - band width di sini
direkonstruksi pakai rolling std log-ratio (metodologi sama dgn OCM
Short-Term Risk Score), tapi HANYA diterapkan ke sisi bawah.

Metodologi:
  1. ratio = btc_price / sth_cost_basis
  2. log_ratio = ln(ratio)
  3. rolling std log_ratio, window 730 hari (2yr), min_periods 365
  4. Band (bawah saja): sth_cost_basis * exp(-k * rolling_std), k = 1, 2

Zona:
  - Price >= sth_cost_basis                    -> NEUTRAL (di atas cost basis)
  - lower_1sd <= Price < sth_cost_basis         -> MILD_ACCUMULATION (olive/orange)
  - lower_2sd <= Price < lower_1sd              -> DEEP_ACCUMULATION (maroon/red)
  - Price < lower_2sd                           -> EXTREME_ACCUMULATION
"""

import numpy as np
import pandas as pd

PCT_WINDOW = 730
PCT_MIN_PERIODS = 365

# Reference events untuk sanity-check arah band (dari realized_prices_knowledge_base.md)
CYCLE_PEAKS = [
    ("Cycle Peak 2017", "2017-12-08", "2017-12-19"),
    ("Cycle Peak 2021", "2021-10-20", "2021-11-09"),
    ("Cycle Peak 2025", "2025-10-05", "2025-10-07"),
]
BEAR_BOTTOMS = [
    ("Bear Bottom 2018", "2018-12-11", "2018-12-17"),
    ("Bear Bottom 2022 (FTX low)", "2022-11-08", "2022-11-21"),
    ("Bear Bottom 2022 (final low)", "2022-12-15", "2022-12-19"),
    ("COVID Flash Crash 2020", "2020-03-13", "2020-03-17"),
]


def rolling_std(series, window=PCT_WINDOW, min_periods=PCT_MIN_PERIODS):
    return series.rolling(window=window, min_periods=min_periods).std()


# ─── LOAD DATA ───────────────────────────────────────────────────────────────

print("Loading data...")
df = pd.read_csv("../data_master_all_metrics.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price", "sth_cost_basis"]).reset_index(drop=True)

# ─── BAND CONSTRUCTION (downside only) ──────────────────────────────────────

df["ratio"] = df["btc_price"] / df["sth_cost_basis"]
df["log_ratio"] = np.log(df["ratio"])
df["rolling_std"] = rolling_std(df["log_ratio"])

for k in (1, 2):
    df[f"lower_{k}sd"] = df["sth_cost_basis"] * np.exp(-k * df["rolling_std"])

conditions = [
    df["btc_price"] < df["lower_2sd"],
    df["btc_price"] < df["lower_1sd"],
    df["btc_price"] < df["sth_cost_basis"],
]
choices = ["EXTREME_ACCUMULATION", "DEEP_ACCUMULATION", "MILD_ACCUMULATION"]
df["zone"] = np.select(conditions, choices, default="NEUTRAL")
df.loc[df["rolling_std"].isna(), "zone"] = np.nan

# ─── SAVE ────────────────────────────────────────────────────────────────────

out_cols = ["date", "btc_price", "sth_cost_basis", "ratio", "rolling_std",
            "lower_1sd", "lower_2sd", "zone"]
df[out_cols].to_csv("data_sth_accumulation_bands.csv", index=False)

valid = df.dropna(subset=["rolling_std"])
print(f"\nSaved data_sth_accumulation_bands.csv: {len(valid)} valid rows "
      f"({valid['date'].min().date()} to {valid['date'].max().date()})")

# ─── CURRENT STATE ───────────────────────────────────────────────────────────

latest = valid.iloc[-1]
print("\n" + "=" * 60)
print("CURRENT STATE")
print("=" * 60)
print(f"Date          : {latest['date'].date()}")
print(f"BTC Price     : ${latest['btc_price']:,.0f}")
print(f"STH Cost Basis: ${latest['sth_cost_basis']:,.0f}  (ratio {latest['ratio']:.3f})")
print(f"Band -1sd/-2sd: ${latest['lower_1sd']:,.0f} / ${latest['lower_2sd']:,.0f}")
print(f"Zone          : {latest['zone']}")

# ─── VALIDASI ARAH BAND DI CYCLE PEAKS (harusnya NEUTRAL, tidak ada band atas) ──

print("\n" + "=" * 60)
print("CEK CYCLE PEAKS (indikator ini tidak punya band atas -> harusnya NEUTRAL)")
print("=" * 60)
for label, d0, d1 in CYCLE_PEAKS:
    mask = (df["date"] >= d0) & (df["date"] <= d1)
    sub = df.loc[mask, ["date", "ratio", "zone"]].dropna(subset=["zone"])
    if len(sub):
        max_ratio = sub["ratio"].max()
        all_neutral = (sub["zone"] == "NEUTRAL").all()
        print(f"  {label:<28} max Price/STH-RP = {max_ratio:.2f} | all NEUTRAL: "
              f"{'YES' if all_neutral else 'no'}")
    else:
        print(f"  {label:<28} no data")

print("\n" + "=" * 60)
print("VALIDASI DI BEAR BOTTOMS (harusnya breach accumulation bands)")
print("=" * 60)
for label, d0, d1 in BEAR_BOTTOMS:
    mask = (df["date"] >= d0) & (df["date"] <= d1)
    sub = df.loc[mask, ["date", "ratio", "zone"]].dropna(subset=["zone"])
    if len(sub):
        min_ratio = sub["ratio"].min()
        extreme_hit = (sub["zone"] == "EXTREME_ACCUMULATION").any()
        deep_hit = sub["zone"].isin(["DEEP_ACCUMULATION", "EXTREME_ACCUMULATION"]).any()
        mild_hit = sub["zone"] != "NEUTRAL"
        mild_hit = mild_hit.any()
        print(f"  {label:<28} min Price/STH-RP = {min_ratio:.2f} | "
              f"mild+: {'YES' if mild_hit else 'no'} | deep+: {'YES' if deep_hit else 'no'} | "
              f"extreme: {'YES' if extreme_hit else 'no'}")
    else:
        print(f"  {label:<28} no data")

# ─── FREKUENSI / SELEKTIVITAS ────────────────────────────────────────────────

print("\n" + "=" * 60)
print("FREKUENSI PER ZONA (seluruh histori valid)")
print("=" * 60)
print(valid["zone"].value_counts(normalize=True).mul(100).round(1).astype(str) + "%")
