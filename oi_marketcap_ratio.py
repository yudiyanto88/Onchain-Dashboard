"""
Rasio Open Interest terhadap Market Cap BTC.

Sumber:
- total_oi        -> data_derivatives.csv (via data_master_all_metrics.csv)
- market cap      -> btc_price * (lth_supply_btc + sth_supply_btc)

Output: data_oi_marketcap.csv
Kolom ratio dalam persen. Ratio = OI / Market Cap * 100.

Catatan: ini bukan bagian dari pipeline auto_update.py. Jalankan manual.
"""

import pandas as pd

SRC = "data_master_all_metrics.csv"
OUT = "data_oi_marketcap.csv"

df = pd.read_csv(SRC, low_memory=False)
df = df[["date", "btc_price", "total_oi", "lth_supply_btc", "sth_supply_btc"]].copy()
df["date"] = pd.to_datetime(df["date"])

df["circulating_supply_btc"] = df["lth_supply_btc"] + df["sth_supply_btc"]
df["market_cap_usd"] = df["btc_price"] * df["circulating_supply_btc"]
df["oi_mcap_pct"] = df["total_oi"] / df["market_cap_usd"] * 100

df = df.dropna(subset=["oi_mcap_pct"]).sort_values("date").reset_index(drop=True)

df["oi_mcap_ma30"] = df["oi_mcap_pct"].rolling(30).mean()
df["oi_mcap_ma90"] = df["oi_mcap_pct"].rolling(90).mean()
# posisi relatif terhadap 1 tahun terakhir, 0-100
df["oi_mcap_pctile_1y"] = (
    df["oi_mcap_pct"].rolling(365).rank(pct=True) * 100
)

cols = [
    "date", "btc_price", "total_oi", "circulating_supply_btc",
    "market_cap_usd", "oi_mcap_pct", "oi_mcap_ma30", "oi_mcap_ma90",
    "oi_mcap_pctile_1y",
]
df[cols].to_csv(OUT, index=False)

last = df.iloc[-1]
print(f"Data terakhir: {last['date'].date()}")
print(f"OI            : ${last['total_oi']/1e9:,.2f} B")
print(f"Market cap    : ${last['market_cap_usd']/1e12:,.3f} T")
print(f"Rasio OI/mcap : {last['oi_mcap_pct']:.2f}%  (MA30 {last['oi_mcap_ma30']:.2f}%)")
print(f"Persentil 1 th: {last['oi_mcap_pctile_1y']:.0f}")
print(f"\nDisimpan ke {OUT} ({len(df)} baris, {df['date'].min().date()} - {df['date'].max().date()})")
