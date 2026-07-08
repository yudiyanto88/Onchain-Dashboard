"""
Local high harga vs STH-MVRV — deteksi divergence di Z2+Z3, cycle 2019 & 2023

Z2 mulai: STH RP cross ke atas RP.
Z3 berakhir: Price cross ke atas AVIV Upper (0.5 sigma), sustained >=3 hari.
STH-MVRV = Price / STH_RP.

Local high: price[t] lebih tinggi dari 5 hari sebelum DAN sesudahnya (strict).
Untuk tiap pasangan local high berurutan (H_k -> H_k+1):
  - price higher high?  (price naik dibanding H_k)
  - STH-MVRV higher high? (STH-MVRV naik dibanding H_k)
  - kalau price HH tapi STH-MVRV TIDAK HH -> divergence (bearish)
Lalu cek: apakah setelah H_k+1 terjadi koreksi >=5% dalam 14 hari, bandingkan
hit rate antara grup "confirmed" (price HH + MVRV HH) vs grup "divergence"
(price HH tanpa MVRV HH).
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load & merge (window detection identik dengan analisis sebelumnya) ─────
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])
av = pd.read_csv('data_aviv.csv', parse_dates=['date'])

df = pl[['date', 'btc_price', 'realized_price', 'sth_cost_basis']].merge(
    av[['date', 'price_at_aviv_mean', 'price_at_aviv_plus_1_sigma']], on='date', how='inner'
)
df = df.rename(columns={
    'btc_price': 'price', 'realized_price': 'rp', 'sth_cost_basis': 'sth_rp',
    'price_at_aviv_mean': 'aviv_mean',
})
df['aviv_upper'] = df['aviv_mean'] + 0.5 * (df['price_at_aviv_plus_1_sigma'] - df['aviv_mean'])
df['sth_mvrv'] = df['price'] / df['sth_rp']
df = df.dropna(subset=['price', 'rp', 'sth_rp', 'aviv_mean', 'aviv_upper', 'sth_mvrv'])
df = df.sort_values('date').reset_index(drop=True)

sth_above_rp = df['sth_rp'] > df['rp']
z2_cross_mask = sth_above_rp & ~sth_above_rp.shift(1, fill_value=False)

def find_episode_window(search_start, search_end, z3_search_end):
    win = df[(df['date'] >= search_start) & (df['date'] <= search_end)]
    cross = win[z2_cross_mask.loc[win.index]]
    if cross.empty:
        return None
    z2_start_idx = cross.index[0]
    z2_start_date = df.loc[z2_start_idx, 'date']
    sub = df[(df['date'] >= z2_start_date) & (df['date'] <= z3_search_end)].reset_index(drop=True)
    above_upper = sub['price'] >= sub['aviv_upper']
    z3_end_idx = None
    n = len(sub)
    for i in range(n):
        if above_upper.iloc[i]:
            if i + 3 <= n and above_upper.iloc[i:i + 3].all():
                z3_end_idx = i
                break
    z3_end_date = sub.loc[z3_end_idx, 'date'] if z3_end_idx is not None else sub['date'].iloc[-1]
    return z2_start_date, z3_end_date

episodes_meta = [
    ('2019 CYCLE', '2019-01-01', '2019-12-31', '2021-12-31'),
    ('2023 CYCLE', '2023-01-01', '2023-12-31', '2025-12-31'),
]

episodes = []
for name, ws, we, z3end in episodes_meta:
    win = find_episode_window(ws, we, z3end)
    if win is None:
        print(f"SKIP {name}")
        continue
    z2_start, z3_end = win
    ep_df = df[(df['date'] >= z2_start) & (df['date'] <= z3_end)].reset_index(drop=True)
    episodes.append({'name': name, 'z2_start': z2_start, 'z3_end': z3_end, 'df': ep_df})

print("=" * 78)
print("WINDOW Z2+Z3 PER CYCLE")
print("=" * 78)
for ep in episodes:
    print(f"\n{ep['name']}: Z2 start = {ep['z2_start'].date()}  |  Z3 end = {ep['z3_end'].date()}  "
          f"({len(ep['df'])} hari)")

# ── 1. Identifikasi local high ──────────────────────────────────────────────
def find_local_highs(ep_df, margin=5):
    d = ep_df.reset_index(drop=True)
    n = len(d)
    highs = []
    for i in range(margin, n - margin):
        left = d['price'].iloc[i - margin:i]
        right = d['price'].iloc[i + 1:i + 1 + margin]
        if d.loc[i, 'price'] > left.max() and d.loc[i, 'price'] > right.max():
            highs.append(i)
    return highs

def min_price_within(idx_global, days, global_df):
    ref_date = global_df.loc[idx_global, 'date']
    end_date = ref_date + pd.Timedelta(days=days)
    seg = global_df[(global_df['date'] > ref_date) & (global_df['date'] <= end_date)]
    if seg.empty:
        return None
    return seg['price'].min()

print("\n" + "=" * 78)
print("1. LOCAL HIGH TERIDENTIFIKASI (price > 5 hari sebelum & sesudah)")
print("=" * 78)

for ep in episodes:
    highs = find_local_highs(ep['df'])
    ep['highs'] = highs
    print(f"\n{ep['name']}: {len(highs)} local high")
    for i in highs:
        row = ep['df'].loc[i]
        print(f"  {row['date'].date()}  price=${row['price']:,.0f}  STH-MVRV={row['sth_mvrv']:.3f}")

# ── 2-4. Pasangan local high berurutan ──────────────────────────────────────
print("\n" + "=" * 78)
print("2-4. PASANGAN LOCAL HIGH BERURUTAN — PRICE HH vs STH-MVRV HH")
print("=" * 78)

confirmed_group = []   # price HH + MVRV HH
divergence_group = []  # price HH tanpa MVRV HH
no_price_hh_group = [] # price bukan HH (sanity check)

for ep in episodes:
    d = ep['df']
    highs = ep['highs']
    print(f"\n{ep['name']}: {len(highs)} local high -> {max(0, len(highs)-1)} pasangan berurutan")
    for k in range(len(highs) - 1):
        i1, i2 = highs[k], highs[k + 1]
        p1, p2 = d.loc[i1, 'price'], d.loc[i2, 'price']
        m1, m2 = d.loc[i1, 'sth_mvrv'], d.loc[i2, 'sth_mvrv']
        price_hh = p2 > p1
        mvrv_hh = m2 > m1

        global_idx = df.index[df['date'] == d.loc[i2, 'date']][0]
        min_p = min_price_within(global_idx, 14, df)
        if min_p is not None:
            drop = (min_p / p2 - 1) * 100
            corrected = bool(drop <= -5)
        else:
            drop, corrected = None, None

        tag = ("PRICE_HH+MVRV_HH (confirmed)" if (price_hh and mvrv_hh) else
               "PRICE_HH tanpa MVRV_HH (divergence)" if (price_hh and not mvrv_hh) else
               "PRICE TIDAK HH")

        print(f"  H{k+1}->H{k+2}: {d.loc[i1,'date'].date()}(${p1:,.0f}, MVRV={m1:.3f}) -> "
              f"{d.loc[i2,'date'].date()}(${p2:,.0f}, MVRV={m2:.3f})  "
              f"price_HH={'YA' if price_hh else 'TIDAK'}  mvrv_HH={'YA' if mvrv_hh else 'TIDAK'}  "
              f"[{tag}]  koreksi14d={f'{drop:+.1f}%' if drop is not None else 'N/A'}  "
              f"corrected>=5%={'YA' if corrected else ('TIDAK' if corrected is False else 'N/A')}")

        record = {'episode': ep['name'], 'h1_date': d.loc[i1,'date'], 'h2_date': d.loc[i2,'date'],
                  'drop': drop, 'corrected': corrected}
        if price_hh and mvrv_hh:
            confirmed_group.append(record)
        elif price_hh and not mvrv_hh:
            divergence_group.append(record)
        else:
            no_price_hh_group.append(record)

# ── Ringkasan ────────────────────────────────────────────────────────────────
def summarize(group, label):
    n = len(group)
    valid = [g for g in group if g['corrected'] is not None]
    n_valid = len(valid)
    n_corr = sum(1 for g in valid if g['corrected'])
    hr = f"{n_corr/n_valid*100:.0f}%" if n_valid > 0 else "N/A"
    print(f"\n{label}: n={n} (valid={n_valid})  ->  {n_corr} koreksi>=5%  hit rate={hr}")
    return n, n_valid, n_corr

print("\n" + "=" * 78)
print("RINGKASAN — CONFIRMED (price HH + MVRV HH) vs DIVERGENCE (price HH tanpa MVRV HH)")
print("=" * 78)
summarize(confirmed_group, "GRUP CONFIRMED (price HH + STH-MVRV HH)")
summarize(divergence_group, "GRUP DIVERGENCE (price HH TANPA STH-MVRV HH)")
summarize(no_price_hh_group, "GRUP PRICE TIDAK HH (sanity check, harusnya jarang di uptrend)")

print("\nPer cycle:")
for ep in episodes:
    print(f"\n  {ep['name']}:")
    c = [g for g in confirmed_group if g['episode'] == ep['name']]
    dv = [g for g in divergence_group if g['episode'] == ep['name']]
    summarize(c, "    Confirmed")
    summarize(dv, "    Divergence")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
