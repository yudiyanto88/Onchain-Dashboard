"""
Bandingkan proxy Median MVRV (dari HODL waves 12-band, lihat
estimate_median_mvrv_from_hodl_waves.py) vs angka resmi ChartInspect
(endpoint /api/onchain/median-mvrv?timeframe=all&isProUser=false, historis penuh
sejak 2010, dihitung dari URPD asli).

Tujuan: cek apakah proxy 12-band cukup akurat dipakai sebagai pengganti backfill
historis (karena URPD asli cuma snapshot hari-ini, gak ada historinya via API free).
"""

import json
import sys
import pandas as pd

if sys.stdout.encoding != "utf-8":
    sys.stdout.reconfigure(encoding="utf-8")

BANDS = [
    "0-1d", "1d-1w", "1w-1m", "1m-3m", "3m-6m", "6m-12m",
    "1y-2y", "2y-3y", "3y-5y", "5y-7y", "7y-10y", "10y+",
]

OFFICIAL_JSON = r"C:\Users\yudiy\AppData\Local\Temp\claude\D--Claude-Code-Projects-Onchain-Dashboard\99d1e1c8-494a-417a-b721-6a629c97c253\scratchpad\median_mvrv_official.json"


def compute_proxy_row(row_hodl, realized_price_total, btc_price):
    points = []
    for band in BANDS:
        supply_pct = row_hodl[f"supply_{band}"]
        rcap_pct = row_hodl[f"realized_cap_{band}"]
        if pd.isna(supply_pct) or supply_pct <= 0:
            continue
        avg_cost_basis = (rcap_pct / supply_pct) * realized_price_total
        points.append((avg_cost_basis, supply_pct))

    points.sort(key=lambda x: x[0])
    total = sum(p[1] for p in points)
    target = total / 2
    cum = 0.0
    for cost_basis, supply_pct in points:
        cum += supply_pct
        if cum >= target:
            return btc_price / cost_basis
    return None


def main():
    with open(OFFICIAL_JSON, "r", encoding="utf-8") as f:
        official_raw = json.load(f)["data"]
    df_official = pd.DataFrame(official_raw)[["date", "median_mvrv", "median_realized_price", "btc_price"]]
    df_official = df_official.rename(columns={
        "median_mvrv": "official_median_mvrv",
        "median_realized_price": "official_median_rp",
        "btc_price": "official_btc_price",
    })

    df_hodl = pd.read_csv("data_hodl_waves.csv")
    df_price = pd.read_csv("data_price_level.csv")[["date", "realized_price"]]
    df_hodl = df_hodl.merge(df_price, on="date", how="inner")

    proxy_rows = []
    for _, r in df_hodl.iterrows():
        proxy_mvrv = compute_proxy_row(r, r["realized_price"], r["btc_price"])
        proxy_rows.append({"date": r["date"], "proxy_median_mvrv": proxy_mvrv, "proxy_btc_price": r["btc_price"]})
    df_proxy = pd.DataFrame(proxy_rows)

    df_cmp = df_proxy.merge(df_official, on="date", how="inner").dropna(subset=["proxy_median_mvrv", "official_median_mvrv"])

    df_cmp["abs_diff"] = (df_cmp["proxy_median_mvrv"] - df_cmp["official_median_mvrv"]).abs()
    df_cmp["pct_diff"] = df_cmp["abs_diff"] / df_cmp["official_median_mvrv"] * 100

    print(f"Jumlah tanggal overlap (data_hodl_waves.csv ada & official ada): {len(df_cmp)}")
    print(f"Rentang tanggal: {df_cmp['date'].min()} s/d {df_cmp['date'].max()}\n")

    print("--- Statistik selisih (proxy vs official) ---")
    print(f"Mean Absolute Error (MVRV point): {df_cmp['abs_diff'].mean():.4f}")
    print(f"Median Absolute Error: {df_cmp['abs_diff'].median():.4f}")
    print(f"Mean % diff: {df_cmp['pct_diff'].mean():.2f}%")
    print(f"Median % diff: {df_cmp['pct_diff'].median():.2f}%")
    print(f"Max abs diff: {df_cmp['abs_diff'].max():.4f} (tanggal {df_cmp.loc[df_cmp['abs_diff'].idxmax(), 'date']})")
    print(f"Correlation (Pearson): {df_cmp['proxy_median_mvrv'].corr(df_cmp['official_median_mvrv']):.6f}\n")

    print("--- Sample 10 baris terakhir ---")
    print(df_cmp[["date", "proxy_median_mvrv", "official_median_mvrv", "abs_diff", "pct_diff"]].tail(10).to_string(index=False))

    print("\n--- Sample baris dengan selisih TERBESAR (top 10) ---")
    print(df_cmp.nlargest(10, "abs_diff")[["date", "proxy_median_mvrv", "official_median_mvrv", "abs_diff", "pct_diff"]].to_string(index=False))

    df_cmp.to_csv("research/findings/_median_mvrv_proxy_vs_official.csv", index=False)
    print("\n✅ Full comparison disimpan ke research/findings/_median_mvrv_proxy_vs_official.csv")

    print("\n--- Statistik per periode (cek apakah era awal 2011-2013 yang paling ngaco) ---")
    for label, start in [("2 tahun terakhir", "2024-09-18"), ("3 tahun terakhir", "2023-09-18"),
                          ("5 tahun terakhir", "2021-09-18"), ("sejak 2014", "2014-01-01"),
                          ("2011-2013 saja", "2011-01-01")]:
        if label == "2011-2013 saja":
            sub = df_cmp[(df_cmp["date"] >= "2011-01-01") & (df_cmp["date"] < "2014-01-01")]
        else:
            sub = df_cmp[df_cmp["date"] >= start]
        if len(sub) == 0:
            continue
        print(f"{label} (n={len(sub)}): mean abs diff={sub['abs_diff'].mean():.4f}, "
              f"median % diff={sub['pct_diff'].median():.2f}%, mean % diff={sub['pct_diff'].mean():.2f}%, "
              f"corr={sub['proxy_median_mvrv'].corr(sub['official_median_mvrv']):.4f}")


if __name__ == "__main__":
    main()
