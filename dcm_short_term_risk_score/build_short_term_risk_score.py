"""
DCM Short-Term Risk Score (replikasi) - komposit 8 faktor terinspirasi video
On-Chain Mind "This Bitcoin Signal Has Nailed EVERY Dip".

Formula asli tidak diungkap (proprietary, dijual sebagai indicator suite).
Ini adalah rekonstruksi berbasis definisi standar tiap metrik on-chain/TA,
dengan normalisasi rolling-percentile dan equal-weight blending sebagai
starting baseline (bisa di-tune nanti).

8 komponen (semua diarahkan: nilai raw lebih tinggi = risk lebih tinggi):
  1. Sharpe Ratio (30d rolling, annualized)
  2. SSR proxy (btc_price / total stablecoin supply)
  3. MVRV Monthly Delta (mvrv_ratio, delta 30 hari)
  4. STH-MVRV (langsung dari data)
  5. SOPR Z-score (aSOPR, rolling z-score 155 hari)
  6. Mayer Multiple (btc_price / 200 DMA)
  7. Velocity RSI (RSI-14 dari 14-day rate-of-change harga)
  8. Microstructural Risk (blend realized volatility 14d + jarak absolut ke 200DMA)

Setiap komponen dinormalisasi ke 0-1 via rolling percentile rank (window 730 hari,
min_periods 365) lalu di-blend equal-weight dan di-smooth EMA-7 untuk skor akhir.
"""

import numpy as np
import pandas as pd
from scipy.stats import percentileofscore

PCT_WINDOW = 730
PCT_MIN_PERIODS = 365
SMOOTH_SPAN = 7

HIGH_RISK = 0.70
LOW_RISK = 0.30


def rolling_percentile(series, window=PCT_WINDOW, min_periods=PCT_MIN_PERIODS):
    """Percentile rank (0-100) dari nilai current dalam rolling window hari."""
    arr = series.values
    n = len(arr)
    result = np.full(n, np.nan)
    for i in range(n):
        if i + 1 < min_periods:
            continue
        lo = max(0, i - window + 1)
        window_data = arr[lo:i + 1]
        valid = window_data[~np.isnan(window_data)]
        if len(valid) < min_periods:
            continue
        result[i] = percentileofscore(valid, arr[i], kind="rank")
    return result / 100.0


def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


# ─── LOAD DATA ───────────────────────────────────────────────────────────────

print("Loading data...")
df = pd.read_csv("../data_master_all_metrics.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["btc_price"]).reset_index(drop=True)  # drop trailing placeholder row

stable = pd.read_csv("data_stablecoin_supply.csv", parse_dates=["date"])
df = df.merge(stable, on="date", how="left")

# ─── RAW COMPONENTS ──────────────────────────────────────────────────────────

log_ret = np.log(df["btc_price"] / df["btc_price"].shift(1))

# 1. Sharpe Ratio (30d rolling, annualized)
roll_mean = log_ret.rolling(30).mean()
roll_std = log_ret.rolling(30).std()
df["raw_sharpe"] = (roll_mean / roll_std) * np.sqrt(365)

# 2. SSR proxy
df["raw_ssr"] = df["btc_price"] / df["stablecoin_supply_usd"]

# 3. MVRV Monthly Delta
df["raw_mvrv_delta"] = df["mvrv_ratio"].diff(30)

# 4. STH-MVRV (direct)
df["raw_sth_mvrv"] = df["sth_mvrv"]

# 5. SOPR Z-score (155d rolling, ~STH holding window)
sopr_mean_155 = df["asopr"].rolling(155).mean()
sopr_std_155 = df["asopr"].rolling(155).std()
df["raw_sopr_z"] = (df["asopr"] - sopr_mean_155) / sopr_std_155

# 6. Mayer Multiple
df["raw_mayer"] = df["btc_price"] / df["200_dma"]

# 7. Velocity RSI (RSI-14 of 14d rate-of-change)
roc_14 = df["btc_price"].pct_change(14)
df["raw_velocity_rsi"] = rsi(roc_14, period=14)

# 8. Microstructural Risk: blend realized vol (14d) + abs distance from 200DMA
vol_14 = log_ret.rolling(14).std()
dist_200dma = ((df["btc_price"] - df["200_dma"]) / df["200_dma"]).abs()
vol_pct = rolling_percentile(vol_14)
dist_pct = rolling_percentile(dist_200dma)
df["raw_microstructural"] = 0.5 * vol_pct + 0.5 * dist_pct  # already 0-1, treated as pre-normalized

# ─── NORMALIZE (rolling percentile 0-1) ──────────────────────────────────────

print("Computing rolling percentiles... (bisa ~30-60 detik)")
component_cols = {
    "sharpe": "raw_sharpe",
    "ssr": "raw_ssr",
    "mvrv_delta": "raw_mvrv_delta",
    "sth_mvrv": "raw_sth_mvrv",
    "sopr_z": "raw_sopr_z",
    "mayer": "raw_mayer",
    "velocity_rsi": "raw_velocity_rsi",
}

pct_data = {f"pct_{name}": rolling_percentile(df[col]) for name, col in component_cols.items()}
pct_data["pct_microstructural"] = df["raw_microstructural"].values  # already 0-1
df = pd.concat([df, pd.DataFrame(pct_data, index=df.index)], axis=1)

pct_cols = [f"pct_{name}" for name in component_cols] + ["pct_microstructural"]

# ─── BLEND (equal-weight) + SMOOTH ──────────────────────────────────────────
# skipna=True: sebelum SSR tersedia (stablecoin supply mulai Nov 2017, valid
# baru Nov 2018 setelah pemanasan window), skor dihitung dari 7 komponen
# lainnya yang sudah valid sejak pertengahan 2011. n_components melacak ini.

df["n_components"] = df[pct_cols].notna().sum(axis=1)
df["risk_raw"] = df[pct_cols].mean(axis=1, skipna=True)
df.loc[df["n_components"] == 0, "risk_raw"] = np.nan
df["risk_score"] = df["risk_raw"].ewm(span=SMOOTH_SPAN, adjust=False).mean()

df["zone"] = np.select(
    [df["risk_score"] >= HIGH_RISK, df["risk_score"] <= LOW_RISK],
    ["HIGH_RISK", "LOW_RISK"],
    default="NEUTRAL",
)

# ─── SAVE ────────────────────────────────────────────────────────────────────

out_cols = (["date", "btc_price"] + list(component_cols.values()) + ["raw_microstructural"]
            + pct_cols + ["n_components", "risk_raw", "risk_score", "zone"])
df[out_cols].to_csv("data_short_term_risk_score.csv", index=False)

valid = df.dropna(subset=["risk_score"])
print(f"\nSaved data_short_term_risk_score.csv: {len(valid)} valid rows "
      f"({valid['date'].min().date()} to {valid['date'].max().date()})")

# ─── CURRENT STATE SUMMARY ───────────────────────────────────────────────────

latest = valid.iloc[-1]
print("\n" + "=" * 60)
print("CURRENT STATE")
print("=" * 60)
print(f"Date        : {latest['date'].date()}")
print(f"BTC Price   : ${latest['btc_price']:,.0f}")
print(f"Risk Score  : {latest['risk_score']:.1%}  (raw: {latest['risk_raw']:.1%})")
print(f"Zone        : {latest['zone']}")
print(f"Components  : {int(latest['n_components'])}/8")

first_8 = valid.loc[valid["n_components"] == 8, "date"].min()
print(f"\nFull 8-factor coverage starts: {first_8.date() if pd.notna(first_8) else 'N/A'}")
print(f"7-factor coverage (pre-SSR) starts: {valid['date'].min().date()}")
print("\nPer-component percentile (0=low risk, 1=high risk):")
for name in list(component_cols.keys()) + ["microstructural"]:
    print(f"  {name:<15}: {latest[f'pct_{name}']:.1%}")
