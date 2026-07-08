"""
Fetch total stablecoin circulating supply (USD-pegged) dari DefiLlama.
Dipakai sebagai proxy untuk Stablecoin Supply Ratio (SSR) component
di DCM Short-Term Risk Score (lihat build_short_term_risk_score.py).

Sumber: https://stablecoins.llama.fi/stablecoincharts/all (public, no API key)
"""

import requests
import pandas as pd

URL = "https://stablecoins.llama.fi/stablecoincharts/all"

print("Fetching stablecoin supply history dari DefiLlama...")
res = requests.get(URL, timeout=60)
res.raise_for_status()
raw = res.json()

rows = []
for entry in raw:
    date = pd.to_datetime(int(entry["date"]), unit="s").normalize()
    supply_usd = entry.get("totalCirculatingUSD", {}).get("peggedUSD")
    if supply_usd is not None:
        rows.append((date, supply_usd))

df = pd.DataFrame(rows, columns=["date", "stablecoin_supply_usd"])
df = df.sort_values("date").drop_duplicates(subset="date").reset_index(drop=True)

df.to_csv("data_stablecoin_supply.csv", index=False)
print(f"Saved data_stablecoin_supply.csv: {len(df)} rows, {df['date'].min().date()} to {df['date'].max().date()}")
print(df.tail(3))
