import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pandas as pd

pl   = pd.read_csv('data_price_level.csv', parse_dates=['date'])
aviv = pd.read_csv('data_aviv.csv',        parse_dates=['date'])

df = pl[['date', 'btc_price', 'MVRV 0σ']].merge(
     aviv[['date', 'price_at_aviv_mean']], on='date', how='inner')
df = df.dropna().sort_values('date').reset_index(drop=True)
df = df[df['date'] >= '2016-01-01'].copy()

# diff_pct: berapa persen MVRV 0sigma di atas/bawah AVIV mean
df['diff_pct']  = (df['MVRV 0σ'] / df['price_at_aviv_mean'] - 1) * 100
df['ratio']     = df['MVRV 0σ'] / df['price_at_aviv_mean']
df['year']      = df['date'].dt.year

print("diff_pct = (MVRV_0sigma / AVIV_mean - 1) x 100%")
print("Positif  = MVRV 0std LEBIH TINGGI dari AVIV mean")
print("Negatif  = MVRV 0std LEBIH RENDAH dari AVIV mean")
print()
print(f"{'Year':<6} {'Mean%':>8} {'Med%':>8} {'Min%':>8} {'Max%':>8} {'Std%':>8}")
print("-" * 46)
for yr, g in df.groupby('year'):
    p = g['diff_pct']
    print(f"{yr:<6} {p.mean():>8.2f} {p.median():>8.2f} {p.min():>8.2f} {p.max():>8.2f} {p.std():>8.2f}")

# --- cycle period breakdown ---
print()
print("--- Per Market Phase ---")
phases = [
    ("2016 Acc",       "2016-01-01", "2016-12-01"),
    ("2017 Bull",      "2016-12-01", "2018-01-07"),
    ("2018 Bear",      "2018-01-07", "2018-12-15"),
    ("2019 Recovery",  "2018-12-15", "2020-03-12"),
    ("COVID Crash",    "2020-03-12", "2020-10-01"),
    ("2020-21 Bull",   "2020-10-01", "2021-11-10"),
    ("2021-22 Bear",   "2021-11-10", "2022-11-21"),
    ("2022-23 Bear",   "2022-11-21", "2023-01-01"),
    ("2023 Recovery",  "2023-01-01", "2023-10-01"),
    ("2023-24 Bull",   "2023-10-01", "2025-10-20"),
    ("2025 Bear Now",  "2025-10-20", "2026-06-22"),
]
print(f"{'Phase':<20} {'Mean%':>8} {'Med%':>8} {'Min%':>8} {'Max%':>8}")
print("-" * 52)
for name, s, e in phases:
    g = df[(df['date'] >= s) & (df['date'] < e)]
    if len(g) == 0:
        continue
    p = g['diff_pct']
    print(f"{name:<20} {p.mean():>8.2f} {p.median():>8.2f} {p.min():>8.2f} {p.max():>8.2f}")

# --- key dates ---
print()
print("--- Nilai di Key Events ---")
events = [
    ("2017 Peak",   "2017-12-17"),
    ("2018 Bottom", "2018-12-15"),
    ("2021 Peak",   "2021-11-10"),
    ("2022 Bottom", "2022-11-21"),
    ("2024 ATH",    "2024-03-14"),
    ("2025 Peak~",  "2025-10-20"),
    ("Today",       df['date'].max().strftime('%Y-%m-%d')),
]
print(f"{'Event':<16} {'Date':<12} {'MVRV_0s':>12} {'AVIV_mean':>12} {'Diff%':>8} {'Ratio':>7}")
print("-" * 68)
for name, dt in events:
    row = df[df['date'] == dt]
    if len(row) == 0:
        # find closest
        idx = (df['date'] - pd.Timestamp(dt)).abs().idxmin()
        row = df.loc[[idx]]
    r = row.iloc[0]
    print(f"{name:<16} {r['date'].strftime('%Y-%m-%d'):<12} "
          f"${r['MVRV 0σ']:>11,.0f} ${r['price_at_aviv_mean']:>11,.0f} "
          f"{r['diff_pct']:>7.2f}% {r['ratio']:>6.4f}x")

print()
print("--- Saat ini ---")
last = df.iloc[-1]
print(f"Date       : {last['date'].strftime('%Y-%m-%d')}")
print(f"BTC Price  : ${last['btc_price']:>10,.0f}")
print(f"MVRV 0std  : ${last['MVRV 0σ']:>10,.0f}")
print(f"AVIV Mean  : ${last['price_at_aviv_mean']:>10,.0f}")
print(f"Diff       : {last['diff_pct']:+.2f}%  (MVRV 0std {abs(last['diff_pct']):.1f}% lebih tinggi)")
print(f"Ratio      : {last['ratio']:.4f}x")
