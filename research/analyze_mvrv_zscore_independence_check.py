"""
Independence check: MVRV level (raw ratio) vs MVRV Z-Score rolling 1Y.
Scan SEMUA local top di seluruh histori data (bukan cherry-pick), grouped per cycle
(dipisah oleh bear-market bottom yang terkonfirmasi), lalu cek apakah arah perubahan
Z-score (naik/turun) selalu searah dengan arah perubahan MVRV raw antar local top
berurutan dalam cycle yang sama, atau ada kasus divergensi arah.
"""
import pandas as pd

mvrv = pd.read_csv('data_mvrv.csv', parse_dates=['date']).rename(
    columns={'date': 'Date', 'btc_price': 'BTC Price', 'mvrv_ratio': 'MVRV'})
price = pd.read_csv('data_price_level.csv', parse_dates=['date']).rename(
    columns={'date': 'Date', 'realized_price': 'Realized Price'})

df = mvrv[['Date', 'BTC Price', 'MVRV']].merge(
    price[['Date', 'Realized Price']], on='Date', how='inner'
).sort_values('Date').reset_index(drop=True)

roll_mean = df['MVRV'].rolling(365, min_periods=30).mean()
roll_std = df['MVRV'].rolling(365, min_periods=30).std()
df['RollMean'] = roll_mean
df['RollStd'] = roll_std
df['Z'] = (df['MVRV'] - roll_mean) / roll_std

# ── Cycle boundaries: bear-market bottom yang terkonfirmasi ─────────────────
cycles = [
    ('2011',              None,           '2011-11-18'),
    ('2013',              '2011-11-18',   '2015-01-14'),
    ('2017',              '2015-01-14',   '2018-12-14'),
    ('2019 (mini-cycle)', '2018-12-14',   '2020-03-12'),
    ('2021',              '2020-03-12',   '2022-11-21'),
    ('2023-2025 (current)', '2022-11-21', None),
]

MARGIN = 5  # sama dengan definisi K6: 5 hari sebelum & sesudah


def find_local_tops(seg_df, margin=MARGIN):
    d = seg_df.reset_index(drop=True)
    n = len(d)
    idxs = []
    for i in range(margin, n - margin):
        left = d['BTC Price'].iloc[i - margin:i]
        right = d['BTC Price'].iloc[i + 1:i + 1 + margin]
        if d.loc[i, 'BTC Price'] > left.max() and d.loc[i, 'BTC Price'] > right.max():
            idxs.append(i)
    return d.loc[idxs].reset_index(drop=True)


def direction(val_prev, val_curr, thresh, is_pct):
    if is_pct:
        chg = (val_curr - val_prev) / val_prev
        if chg > thresh:
            return 'NAIK'
        elif chg < -thresh:
            return 'TURUN'
        else:
            return 'FLAT'
    else:
        chg = val_curr - val_prev
        if chg > thresh:
            return 'NAIK'
        elif chg < -thresh:
            return 'TURUN'
        else:
            return 'FLAT'


all_rows = []
pair_rows = []

for name, d0, d1 in cycles:
    seg = df.copy()
    if d0 is not None:
        seg = seg[seg['Date'] > d0]
    if d1 is not None:
        seg = seg[seg['Date'] <= d1]
    seg = seg.dropna(subset=['Z']).reset_index(drop=True)

    tops = find_local_tops(seg)
    tops['Cycle'] = name
    all_rows.append(tops)

    for i in range(1, len(tops)):
        prev = tops.iloc[i - 1]
        curr = tops.iloc[i]
        dir_mvrv = direction(prev['MVRV'], curr['MVRV'], thresh=0.02, is_pct=True)   # >2% = naik/turun
        dir_z = direction(prev['Z'], curr['Z'], thresh=0.10, is_pct=False)           # >0.10 abs = naik/turun

        if dir_mvrv == 'NAIK' and dir_z == 'NAIK':
            cls = 'SEARAH (naik-naik)'
        elif dir_mvrv == 'TURUN' and dir_z == 'TURUN':
            cls = 'SEARAH (turun-turun)'
        elif dir_mvrv in ('NAIK', 'FLAT') and dir_z == 'TURUN':
            cls = 'DIVERGEN (MVRV naik/flat, Z turun)'
        elif dir_mvrv == 'TURUN' and dir_z in ('NAIK', 'FLAT'):
            cls = 'DIVERGEN (MVRV turun, Z naik/flat)'
        else:
            cls = 'FLAT/FLAT (tidak ada perubahan berarti)'

        pair_rows.append({
            'Cycle': name,
            'Date_prev': prev['Date'].date(), 'Date_curr': curr['Date'].date(),
            'Price_prev': prev['BTC Price'], 'Price_curr': curr['BTC Price'],
            'MVRV_prev': prev['MVRV'], 'MVRV_curr': curr['MVRV'], 'Dir_MVRV': dir_mvrv,
            'Z_prev': prev['Z'], 'Z_curr': curr['Z'], 'Dir_Z': dir_z,
            'RollMean_prev': prev['RollMean'], 'RollMean_curr': curr['RollMean'],
            'RollStd_prev': prev['RollStd'], 'RollStd_curr': curr['RollStd'],
            'Class': cls,
        })

all_tops = pd.concat(all_rows, ignore_index=True)
pairs = pd.DataFrame(pair_rows)

print('=' * 100)
print(f'TOTAL LOCAL TOP DITEMUKAN: {len(all_tops)}  |  TOTAL PASANGAN BERURUTAN: {len(pairs)}')
print('=' * 100)
for name, _, _ in cycles:
    n_top = (all_tops['Cycle'] == name).sum()
    n_pair = (pairs['Cycle'] == name).sum()
    print(f'{name:24s} local top={n_top:4d}  pasangan={n_pair:4d}')

print()
print('=' * 100)
print('DISTRIBUSI KLASIFIKASI PASANGAN')
print('=' * 100)
print(pairs['Class'].value_counts())

print()
print('=' * 100)
print('DETAIL SEMUA KASUS DIVERGEN')
print('=' * 100)
div = pairs[pairs['Class'].str.startswith('DIVERGEN')]
pd.set_option('display.width', 200)
pd.set_option('display.max_rows', None)
for _, r in div.iterrows():
    print(f"\n[{r['Cycle']}] {r['Date_prev']} -> {r['Date_curr']}")
    print(f"  Price: \${r['Price_prev']:,.0f} -> \${r['Price_curr']:,.0f}")
    print(f"  MVRV:  {r['MVRV_prev']:.3f} -> {r['MVRV_curr']:.3f}  ({r['Dir_MVRV']})")
    print(f"  Z:     {r['Z_prev']:.3f} -> {r['Z_curr']:.3f}  ({r['Dir_Z']})")
    print(f"  RollMean: {r['RollMean_prev']:.3f} -> {r['RollMean_curr']:.3f}   RollStd: {r['RollStd_prev']:.3f} -> {r['RollStd_curr']:.3f}")
    print(f"  Class: {r['Class']}")

# Save full raw tables to CSV for reference
all_tops.to_csv('research/findings/mvrv_zscore_independence_all_local_tops.csv', index=False)
pairs.to_csv('research/findings/mvrv_zscore_independence_pairs.csv', index=False)
print('\\nSaved: research/findings/mvrv_zscore_independence_all_local_tops.csv')
print('Saved: research/findings/mvrv_zscore_independence_pairs.csv')
