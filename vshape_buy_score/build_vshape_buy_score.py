"""
V-Shape Buy Score - skema final N-of-3 boolean untuk deteksi koreksi V-shape
yang layak dibeli (referensi: 6-9 Mar 2023, 21 Jan 2024, 5 Sep 2020,
14-16 Jul 2017, 13-15 Sep 2017, 21 Sep 2021).

BEDA metodologi dari DCM Short-Term Risk Score: bukan komposit kontinu
(percentile rank), tapi 3 metrik BOOLEAN yang di-count, karena V-shape
correction itu tajam & singkat - composite kontinu terbukti gagal
(persistence filter membunuh recall, percentile rank tidak otomatis
menghasilkan kelangkaan). Threshold final: >=2-dari-3 confirm.

3 metrik final:
  c1: MIN(aSOPR, STH-SOPR) <= 0.98
  c2: STH % supply in loss >= 40% DAN naik >= 10pt dalam 5 hari (filter
      rate-of-change - level saja terlalu noisy, fires di 51% hari sejarah)
  c3: RSI14 tembus di bawah Bollinger Band(30, 1.5) lower band

(MVRV Monthly Delta diuji juga - 5/6 event di bawah percentile 15% - tapi
di-drop karena N-of-3 sudah solid tanpa dia)
"""

import numpy as np
import pandas as pd

EVENTS = [
    ("6-9 Mar 2023", "2023-03-06", "2023-03-09"),
    ("21 Jan 2024", "2024-01-21", "2024-01-21"),
    ("5 Sep 2020", "2020-09-05", "2020-09-05"),
    ("14-16 Jul 2017", "2017-07-14", "2017-07-16"),
    ("13-15 Sep 2017", "2017-09-13", "2017-09-15"),
    ("21 Sep 2021", "2021-09-21", "2021-09-21"),
]

CONFIRM_THRESHOLD = 2  # >=2-dari-3, tervalidasi: precision 75.8%, recall 38.0%, 6/6 tanggal referensi


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
df = df.dropna(subset=["btc_price"]).reset_index(drop=True)

# ─── 3 METRIK BOOLEAN ────────────────────────────────────────────────────────

df["min_sopr"] = df[["asopr", "sth_sopr"]].min(axis=1)
df["c1_sopr"] = df["min_sopr"] <= 0.98

df["sth_loss_chg5"] = df["pct_sth_in_loss"].diff(5)
df["c2_sth_loss"] = (df["pct_sth_in_loss"] >= 40) & (df["sth_loss_chg5"] >= 10)

df["rsi14"] = rsi(df["btc_price"], period=14)
bb_mid = df["rsi14"].rolling(30).mean()
bb_std = df["rsi14"].rolling(30).std()
df["rsi_bb_lower"] = bb_mid - 1.5 * bb_std
df["c3_rsi_bb"] = df["rsi14"] <= df["rsi_bb_lower"]

c_cols = ["c1_sopr", "c2_sth_loss", "c3_rsi_bb"]
df["confirm_count"] = df[c_cols].sum(axis=1)
df["zone"] = np.where(df["confirm_count"] >= CONFIRM_THRESHOLD, "BUY_ZONE", "NEUTRAL")

# ─── GROUND TRUTH (untuk precision/recall) ──────────────────────────────────

df["drawdown_10d"] = df["btc_price"] / df["btc_price"].rolling(10).max() - 1
df["is_correction"] = df["drawdown_10d"] <= -0.08

# ─── SAVE ────────────────────────────────────────────────────────────────────

out_cols = (["date", "btc_price", "min_sopr", "pct_sth_in_loss", "sth_loss_chg5",
             "rsi14", "rsi_bb_lower"] + c_cols
            + ["confirm_count", "zone", "drawdown_10d", "is_correction"])
df[out_cols].to_csv("data_vshape_buy_score.csv", index=False)

valid = df.dropna(subset=["rsi_bb_lower"])
print(f"\nSaved data_vshape_buy_score.csv: {len(valid)} valid rows "
      f"({valid['date'].min().date()} to {valid['date'].max().date()})")

# ─── CURRENT STATE ───────────────────────────────────────────────────────────

latest = df.iloc[-1]
print("\n" + "=" * 60)
print("CURRENT STATE")
print("=" * 60)
print(f"Date          : {latest['date'].date()}")
print(f"BTC Price     : ${latest['btc_price']:,.0f}")
print(f"c1 MIN-SOPR   : {latest['min_sopr']:.3f} [{'YES' if latest['c1_sopr'] else 'no'}]")
print(f"c2 STH%loss   : {latest['pct_sth_in_loss']:.1f}% (chg5d {latest['sth_loss_chg5']:+.1f}pt) "
      f"[{'YES' if latest['c2_sth_loss'] else 'no'}]")
print(f"c3 RSI14+BB   : {latest['rsi14']:.1f} vs {latest['rsi_bb_lower']:.1f} "
      f"[{'YES' if latest['c3_rsi_bb'] else 'no'}]")
print(f"Confirm count : {int(latest['confirm_count'])}/3")
print(f"Zone          : {latest['zone']}")

# ─── VALIDASI DI 6 TANGGAL REFERENSI ─────────────────────────────────────────

print("\n" + "=" * 60)
print("VALIDASI DI 6 TANGGAL REFERENSI")
print("=" * 60)
for label, d0, d1 in EVENTS:
    mask = (df["date"] >= d0) & (df["date"] <= d1)
    sub = df.loc[mask, ["date", "confirm_count", "zone"]]
    if len(sub):
        peak = sub["confirm_count"].max()
        confirmed = (sub["zone"] == "BUY_ZONE").any()
        print(f"  {label:<18} peak confirm_count = {peak}/3  | >=2-dari-3 confirmed: "
              f"{'YES' if confirmed else 'no'}")
    else:
        print(f"  {label:<18} no data")

# ─── PRECISION/RECALL PER THRESHOLD ──────────────────────────────────────────

print("\n" + "=" * 60)
print("PRECISION/RECALL (ground truth: drawdown_10d <= -8%)")
print("=" * 60)
valid_gt = df.dropna(subset=["is_correction", "confirm_count"])
for thresh in (1, 2, 3):
    fires = valid_gt["confirm_count"] >= thresh
    pct_fire = fires.mean()
    precision = valid_gt.loc[fires, "is_correction"].mean() if fires.any() else np.nan
    recall = valid_gt.loc[valid_gt["is_correction"], "confirm_count"].ge(thresh).mean()
    print(f"  >={thresh}-dari-3   fires {pct_fire:.1%} hari | precision {precision:.1%} | recall {recall:.1%}")

# ─── FREKUENSI / SELEKTIVITAS (skema final >=2-dari-3) ──────────────────────

z = (df["zone"] == "BUY_ZONE").astype(int).values
episodes = ((z[1:] - z[:-1]) == 1).sum() + (1 if len(z) and z[0] == 1 else 0)
pct_days = (df["zone"] == "BUY_ZONE").mean()
print("\n" + "=" * 60)
print(f"FREKUENSI (skema final >={CONFIRM_THRESHOLD}-dari-3)")
print("=" * 60)
print(f"Persentase hari BUY_ZONE : {pct_days:.1%}")
print(f"Jumlah episode terpisah  : {episodes}")
if episodes:
    print(f"Rata-rata durasi episode : {z.sum()/episodes:.1f} hari")
