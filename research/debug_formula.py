import pandas as pd
import numpy as np
import requests

print("=== STEP 1: Tarik data realized-profit-by-age ===")
r = requests.get("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
df = pd.DataFrame(r.json()['data'])
df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
df = df.sort_values('date').reset_index(drop=True)
print(f"Rows: {len(df)}, Date range: {df['date'].iloc[0]} to {df['date'].iloc[-1]}")

print("\n=== STEP 2: Hitung cum_net_pl dan rolling windows ===")
lth_net = (
    df[[f'band_{i}_profit_usd' for i in range(5, 12)]].sum(axis=1) -
    df[[f'band_{i}_loss_usd' for i in range(5, 12)]].sum(axis=1)
)
df['cum_net_pl'] = lth_net.cumsum()

# Test rolling windows untuk cari mana yang CI pakai
windows = [90, 180, 365, 730, 1095]
for w in windows:
    df[f'roll_{w}d'] = lth_net.rolling(window=w, min_periods=1).sum()

print("\n=== STEP 3: Merge supply dan price ===")
df_s = pd.read_csv("data_supply.csv")
df_p = pd.read_csv("data_price_level.csv")
df_s['date'] = pd.to_datetime(df_s['date'], errors='coerce').dt.strftime('%Y-%m-%d')
df_p['date'] = pd.to_datetime(df_p['date'], errors='coerce').dt.strftime('%Y-%m-%d')

df = df.merge(df_p[['date', 'lth_cost_basis', 'realized_price']], on='date', how='inner')
df = df.merge(df_s[['date', 'lth_supply_btc', 'sth_supply_btc']], on='date', how='inner')
df['circulating_btc'] = df['lth_supply_btc'] + df['sth_supply_btc']

# ============================================================
# STEP 4: Test rolling windows di 3 titik validasi
# ============================================================
print("\n=== STEP 4: Test rolling windows ===")
print("Format: realized_price + roll_Xd / lth_supply_btc\n")

checkpoints = [
    ('2013-11-30', 1200),
    ('2017-12-17', 6000),
    ('2021-11-09', 39900),
    ('2026-06-07', 103500),
]

print(f"{'Date':<14} {'CI Target':>10} {'cumsum':>10} {'90d':>10} {'180d':>10} {'365d':>10} {'730d':>10} {'1095d':>10}")
print("-" * 90)

for date_str, ci_target in checkpoints:
    rows = df[df['date'] == date_str]
    if rows.empty:
        # try nearest date
        df['date_dt'] = pd.to_datetime(df['date'])
        target_dt = pd.to_datetime(date_str)
        idx = (df['date_dt'] - target_dt).abs().idxmin()
        row = df.iloc[idx]
        actual_date = row['date']
    else:
        row = rows.iloc[0]
        actual_date = date_str

    rp = row['realized_price']
    supply = row['lth_supply_btc']

    results = {}
    results['cumsum'] = rp + row['cum_net_pl'] / supply
    for w in windows:
        results[f'{w}d'] = rp + row[f'roll_{w}d'] / supply

    line = f"{actual_date:<14} ${ci_target:>9,}"
    for key in ['cumsum', '90d', '180d', '365d', '730d', '1095d']:
        val = results[key]
        marker = "✅" if abs(val - ci_target) / ci_target < 0.05 else "  "
        line += f"  {marker}${val:>7,.0f}"
    print(line)

print("\nKeterangan: ✅ = dalam 5% dari target CI")

# Cek nilai realized_price dan lth_cost_basis di 2013
for date_str in ['2013-11-30', '2013-06-01', '2013-01-01', '2012-01-01', '2011-01-01']:
    rows = df[df['date'] == date_str]
    if not rows.empty:
        row = rows.iloc[0]
        print(f"{date_str}: btc_price=${row['btc_price']:,.2f}  realized_price=${row['realized_price']:,.2f}  lth_cost_basis=${row['lth_cost_basis']:,.2f}")
        
