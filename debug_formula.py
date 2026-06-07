import pandas as pd
import numpy as np
import requests

r = requests.get("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
df = pd.DataFrame(r.json()['data'])
df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
df = df.sort_values('date').reset_index(drop=True)

lth_net = df[[f'band_{i}_profit_usd' for i in range(5,12)]].sum(axis=1) - df[[f'band_{i}_loss_usd' for i in range(5,12)]].sum(axis=1)
df['cum_net_pl'] = lth_net.cumsum()

df_s = pd.read_csv("data_supply.csv")
df_p = pd.read_csv("data_price_level.csv")
df_s['date'] = pd.to_datetime(df_s['date'], errors='coerce').dt.strftime('%Y-%m-%d')
df_p['date'] = pd.to_datetime(df_p['date'], errors='coerce').dt.strftime('%Y-%m-%d')

df = df.merge(df_p[['date','lth_cost_basis','realized_price']], on='date', how='inner')
df = df.merge(df_s[['date','lth_supply_btc','supply_btc']], on='date', how='inner')

target = '2021-11-09'
row = df[df['date'] == target].iloc[0]
print(f"cum_net_pl       : ${row['cum_net_pl']:,.0f}")
print(f"lth_supply_btc   : {row['lth_supply_btc']:,.0f} BTC")
print(f"supply_btc       : {row['supply_btc']:,.0f} BTC")
print(f"lth_cost_basis   : ${row['lth_cost_basis']:,.2f}")
print(f"realized_price   : ${row['realized_price']:,.2f}")
print()

for baseline_name, baseline in [('lth_cost_basis', row['lth_cost_basis']), ('realized_price', row['realized_price'])]:
    for supply_name, supply in [('lth_supply_btc', row['lth_supply_btc']), ('supply_btc', row['supply_btc'])]:
        result = baseline + row['cum_net_pl'] / supply
        match = "✅ MATCH" if abs(result - 39900) < 2000 else "❌"
        print(f"{baseline_name} + cum/({supply_name}) = ${result:,.0f}  {match}")
