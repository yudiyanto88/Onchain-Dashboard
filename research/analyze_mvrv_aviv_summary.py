import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
import pandas as pd
import numpy as np

pl   = pd.read_csv('data_price_level.csv', parse_dates=['date'])
aviv = pd.read_csv('data_aviv.csv',        parse_dates=['date'])

df = pl[['date', 'btc_price', 'MVRV 0σ']].merge(
     aviv[['date', 'price_at_aviv_mean']], on='date', how='inner')
df = df.dropna().sort_values('date').reset_index(drop=True)
df = df[df['date'] >= '2015-01-01'].copy()

df['diff_pct'] = (df['MVRV 0σ'] / df['price_at_aviv_mean'] - 1) * 100

# Rolling 90-day average of the diff
df['diff_pct_ma90'] = df['diff_pct'].rolling(90).mean()

# Distribution
p = df['diff_pct']
print("=" * 55)
print("MVRV 0std vs AVIV Mean — Gap Distribution (2015-2026)")
print("diff = MVRV_0sigma / AVIV_mean - 1")
print("=" * 55)
print()
print(f"  Rata-rata (mean)  : {p.mean():>+7.2f}%")
print(f"  Median            : {p.median():>+7.2f}%")
print(f"  Std Dev           : {p.std():>7.2f}%")
print()
print(f"  Min ever          : {p.min():>+7.2f}%  ({df.loc[p.idxmin(),'date'].strftime('%Y-%m-%d')})")
print(f"  Max ever          : {p.max():>+7.2f}%  ({df.loc[p.idxmax(),'date'].strftime('%Y-%m-%d')})")
print()
print("  Percentile distribution:")
for pct in [5, 10, 25, 50, 75, 90, 95]:
    print(f"    P{pct:<3}  : {np.percentile(p, pct):>+7.2f}%")

# How often MVRV 0s > AVIV mean (positive diff)
above = (df['diff_pct'] > 0).sum()
total = len(df)
print()
print(f"  MVRV 0std > AVIV mean : {above}/{total} hari ({above/total*100:.1f}%)")
print(f"  MVRV 0std < AVIV mean : {total-above}/{total} hari ({(total-above)/total*100:.1f}%)")

# Narrow gap zone (< 2%) = historically near peaks
near_zero = ((df['diff_pct'] > -2) & (df['diff_pct'] < 2)).sum()
print()
print(f"  Gap dalam -2% s/d +2% : {near_zero} hari ({near_zero/total*100:.1f}%)")
print(f"  Nilai sekarang         : {df['diff_pct'].iloc[-1]:>+.2f}%")
print()

# Breakdown by range bucket
print("  Distribusi per range:")
buckets = [
    ("< -5%  (AVIV jauh lebih tinggi)",  -999,  -5),
    ("-5% s/d -2%",                        -5,  -2),
    ("-2% s/d 0%  (konvergen, AVIV > MVRV)", -2,   0),
    ("0% s/d +2%  (konvergen, MVRV > AVIV)",  0,   2),
    ("+2% s/d +5%",                         2,   5),
    ("+5% s/d +10%",                        5,  10),
    ("+10% s/d +15%",                      10,  15),
    ("> +15%",                             15, 999),
]
for label, lo, hi in buckets:
    n = ((p > lo) & (p <= hi)).sum()
    bar = '#' * int(n / total * 40)
    print(f"    {label:<42} {n:>4}d  {n/total*100:>5.1f}%  {bar}")
