"""
Percobaan: estimasi Median Realized Price / Median MVRV dari data_hodl_waves.csv
(12 age band, tiap band punya supply_pct dan realized_cap_pct), dibandingkan dengan
angka URPD asli (500 price bucket) dari fetch_urpd.py.

Formula per band:
  avg_cost_basis_band = (realized_cap_pct_band / supply_pct_band) * realized_price_total

Lalu treat 12 band ini sebagai 12 titik distribusi (bobot = supply_pct), urutkan
NAIK berdasarkan avg_cost_basis (bukan berdasarkan umur), cari titik cumulative
supply_pct = 50% (interpolasi linear) -> itu proxy Median Realized Price.

CATATAN KETERBATASAN (penting):
HODL wave band dikelompokkan berdasarkan UMUR, bukan HARGA. Satu band umur bisa
berisi koin yang dibeli di harga sangat berbeda-beda kalau band itu mencakup
periode panjang dengan volatilitas tinggi (paling parah band "10y+" yang
merentang seluruh sejarah Bitcoin). Jadi avg_cost_basis per band adalah RATA-RATA,
bukan distribusi harga asli — hasil median dari 12 titik rata-rata ini HANYA
proxy kasar, bukan pengganti URPD asli (yang granular per bucket harga).
"""

import pandas as pd

BANDS = [
    "0-1d", "1d-1w", "1w-1m", "1m-3m", "3m-6m", "6m-12m",
    "1y-2y", "2y-3y", "3y-5y", "5y-7y", "7y-10y", "10y+",
]


def main():
    df_hodl = pd.read_csv("data_hodl_waves.csv")
    df_price = pd.read_csv("data_price_level.csv")

    row_hodl = df_hodl.iloc[-1]
    row_price = df_price[df_price["date"] == row_hodl["date"]].iloc[-1]

    date = row_hodl["date"]
    btc_price = row_price["btc_price"]
    realized_price_total = row_price["realized_price"]

    print(f"Tanggal: {date}")
    print(f"BTC Price: ${btc_price:,.2f}")
    print(f"Realized Price (total, dari MVRV standar): ${realized_price_total:,.2f}\n")

    points = []
    for band in BANDS:
        supply_pct = row_hodl[f"supply_{band}"]
        rcap_pct = row_hodl[f"realized_cap_{band}"]
        if supply_pct <= 0:
            continue
        avg_cost_basis = (rcap_pct / supply_pct) * realized_price_total
        points.append({"band": band, "supply_pct": supply_pct, "avg_cost_basis": avg_cost_basis})

    df_points = pd.DataFrame(points).sort_values("avg_cost_basis").reset_index(drop=True)
    df_points["cum_supply_pct"] = df_points["supply_pct"].cumsum()

    print("Per age-band, diurutkan berdasarkan avg cost basis (BUKAN umur):")
    print(df_points.to_string(index=False))

    total_supply_pct = df_points["supply_pct"].sum()
    target = total_supply_pct / 2  # 50% dari total yang terhitung (band 10y+ dst bisa hilang presisi float kecil)

    prev_cum = 0.0
    median_cost_basis = None
    for _, r in df_points.iterrows():
        if r["cum_supply_pct"] >= target:
            span = r["cum_supply_pct"] - prev_cum
            frac = (target - prev_cum) / span if span > 0 else 0
            lo = prev_cum  # placeholder, interpolasi pakai avg_cost_basis band sblm & skrg
            median_cost_basis = r["avg_cost_basis"]  # band-level, tidak sub-interpolasi harga dalam band
            break
        prev_cum = r["cum_supply_pct"]

    median_mvrv_proxy = btc_price / median_cost_basis

    print(f"\n--- HASIL PROXY (dari HODL waves, 12 band) ---")
    print(f"Median cost basis (band tempat cum_supply_pct nembus 50%): ${median_cost_basis:,.2f}")
    print(f"Median MVRV proxy: {median_mvrv_proxy:.4f}")

    print(f"\n--- PEMBANDING: URPD asli hari ini (2026-09-18, dari fetch_urpd.py) ---")
    print(f"Median Realized Price (URPD, 500 bucket): $63,298.36")
    print(f"Median MVRV (URPD): 1.2659  (pakai live price $80,129.86, bukan $77,471.6)")

    df_mvrv = pd.read_csv("data_median_mvrv.csv")
    row_urpd = df_mvrv.iloc[-1]
    median_mvrv_urpd_same_price = btc_price / row_urpd["median_realized_price"]
    print(f"Median MVRV (URPD) kalau dihitung ulang pakai btc_price yg sama (${btc_price:,.2f}): "
          f"{median_mvrv_urpd_same_price:.4f}")


if __name__ == "__main__":
    main()
