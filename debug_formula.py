import pandas as pd
import numpy as np
import requests

print("=== STEP 1: Tarik data realized-profit-by-age ===")
r = requests.get("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
df = pd.DataFrame(r.json()['data'])
df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
df = df.sort_values('date').reset_index(drop=True)
print(f"Rows: {len(df)}, Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")

print("\n=== STEP 2: Hitung cum_net_pl (bands 5-11) ===")
lth_net = (
    df[[f'band_{i}_profit_usd' for i in range(5, 12)]].sum(axis=1) -
    df[[f'band_{i}_loss_usd' for i in range(5, 12)]].sum(axis=1)
)
df['cum_net_pl_5_11'] = lth_net.cumsum()

# Juga hitung versi all bands (0-11) untuk perbandingan
all_net = (
    df[[f'band_{i}_profit_usd' for i in range(0, 12)]].sum(axis=1) -
    df[[f'band_{i}_loss_usd' for i in range(0, 12)]].sum(axis=1)
)
df['cum_net_pl_0_11'] = all_net.cumsum()

# Dan versi bands 6-11 (strict LTH >1 tahun)
lth_strict_net = (
    df[[f'band_{i}_profit_usd' for i in range(6, 12)]].sum(axis=1) -
    df[[f'band_{i}_loss_usd' for i in range(6, 12)]].sum(axis=1)
)
df['cum_net_pl_6_11'] = lth_strict_net.cumsum()

print("\n=== STEP 3: Merge supply dan price ===")
df_s = pd.read_csv("data_supply.csv")
df_p = pd.read_csv("data_price_level.csv")
df_s['date'] = pd.to_datetime(df_s['date'], errors='coerce').dt.strftime('%Y-%m-%d')
df_p['date'] = pd.to_datetime(df_p['date'], errors='coerce').dt.strftime('%Y-%m-%d')

df = df.merge(df_p[['date', 'lth_cost_basis', 'realized_price']], on='date', how='inner')
df = df.merge(df_s[['date', 'lth_supply_btc', 'sth_supply_btc']], on='date', how='inner')
df['circulating_btc'] = df['lth_supply_btc'] + df['sth_supply_btc']

print("\n=== STEP 4: Test semua kombinasi di Nov 9, 2021 (target: $39,900) ===")
target = '2021-11-09'
row = df[df['date'] == target].iloc[0]

print(f"\nRaw values di {target}:")
print(f"  cum_net_pl (bands 5-11) : ${row['cum_net_pl_5_11']:,.0f}")
print(f"  cum_net_pl (bands 6-11) : ${row['cum_net_pl_6_11']:,.0f}")
print(f"  cum_net_pl (bands 0-11) : ${row['cum_net_pl_0_11']:,.0f}")
print(f"  lth_supply_btc          : {row['lth_supply_btc']:,.0f} BTC")
print(f"  circulating_btc         : {row['circulating_btc']:,.0f} BTC")
print(f"  lth_cost_basis          : ${row['lth_cost_basis']:,.2f}")
print(f"  realized_price          : ${row['realized_price']:,.2f}")

print(f"\nTest kombinasi (target $39,900):")
print(f"{'Baseline':<20} {'Net P/L bands':<18} {'Supply':<20} {'Result':>10}  Match?")
print("-" * 80)

baselines = [('lth_cost_basis', row['lth_cost_basis']), ('realized_price', row['realized_price'])]
cum_cols = [('bands 5-11', row['cum_net_pl_5_11']), ('bands 6-11', row['cum_net_pl_6_11']), ('bands 0-11', row['cum_net_pl_0_11'])]
supplies = [('lth_supply_btc', row['lth_supply_btc']), ('circulating_btc', row['circulating_btc'])]

for b_name, b_val in baselines:
    for c_name, c_val in cum_cols:
        for s_name, s_val in supplies:
            result = b_val + c_val / s_val
            match = "✅ MATCH" if abs(result - 39900) < 3000 else ""
            print(f"{b_name:<20} {c_name:<18} {s_name:<20} ${result:>9,.0f}  {match}")

print("\n=== STEP 5: Cek nilai latest (target ~$103,500) ===")
latest = df.iloc[-1]
print(f"\nRaw values di {latest['date']}:")
print(f"  cum_net_pl (bands 5-11) : ${latest['cum_net_pl_5_11']:,.0f}")
print(f"  cum_net_pl (bands 6-11) : ${latest['cum_net_pl_6_11']:,.0f}")
print(f"  cum_net_pl (bands 0-11) : ${latest['cum_net_pl_0_11']:,.0f}")
print(f"  lth_supply_btc          : {latest['lth_supply_btc']:,.0f} BTC")
print(f"  circulating_btc         : {latest['circulating_btc']:,.0f} BTC")
print(f"  lth_cost_basis          : ${latest['lth_cost_basis']:,.2f}")
print(f"  realized_price          : ${latest['realized_price']:,.2f}")

print(f"\nTest kombinasi (target ~$103,500):")
print(f"{'Baseline':<20} {'Net P/L bands':<18} {'Supply':<20} {'Result':>10}  Match?")
print("-" * 80)

for b_name, b_val in [('lth_cost_basis', latest['lth_cost_basis']), ('realized_price', latest['realized_price'])]:
    for c_name, c_val in [('bands 5-11', latest['cum_net_pl_5_11']), ('bands 6-11', latest['cum_net_pl_6_11']), ('bands 0-11', latest['cum_net_pl_0_11'])]:
        for s_name, s_val in [('lth_supply_btc', latest['lth_supply_btc']), ('circulating_btc', latest['circulating_btc'])]:
            result = b_val + c_val / s_val
            match = "✅ MATCH" if abs(result - 103500) < 5000 else ""
            print(f"{b_name:<20} {c_name:<18} {s_name:<20} ${result:>9,.0f}  {match}")
