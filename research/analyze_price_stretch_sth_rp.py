"""
Jarak (stretch) harga dari STH RP selama Z2+Z3 — cycle 2019 & 2023

Z2 mulai: STH RP cross ke atas RP (LTH/realized price).
Z3 berakhir: Price cross ke atas AVIV Upper (0.5 sigma), bertahan >=3 hari.
Stretch = (Price - STH_RP) / STH_RP * 100%

Window detection direplikasi dari analyze_k5_dip_entry_trigger.py (metodologi
yang sama dipakai sebelumnya untuk K5 dip-entry validation).
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load & merge ─────────────────────────────────────────────────────────────
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
df['stretch_pct'] = (df['price'] - df['sth_rp']) / df['sth_rp'] * 100
df = df.dropna(subset=['price', 'rp', 'sth_rp', 'aviv_mean', 'aviv_upper', 'stretch_pct'])
df = df.sort_values('date').reset_index(drop=True)

# ── Locate Z2 start / Z3 end per cycle (sama seperti K5 dip-entry script) ───
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
    ('2019 CYCLE (bottom Des 2018)', '2019-01-01', '2019-12-31', '2021-12-31'),
    ('2023 CYCLE (bottom Nov 2022)', '2023-01-01', '2023-12-31', '2025-12-31'),
]

episodes = []
for name, ws, we, z3end in episodes_meta:
    win = find_episode_window(ws, we, z3end)
    if win is None:
        print(f"SKIP {name} — Z2 start tidak ditemukan")
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

# ── 1. Distribusi stretch harian ─────────────────────────────────────────────
print("\n" + "=" * 78)
print("1. DISTRIBUSI JARAK (STRETCH) HARIAN — (Price - STH_RP)/STH_RP x 100%")
print("=" * 78)

all_stretch = []
for ep in episodes:
    s = ep['df']['stretch_pct']
    all_stretch.append(s)
    print(f"\n{ep['name']} ({len(s)} hari):")
    print(f"  Min={s.min():.1f}%  P25={s.quantile(.25):.1f}%  Median={s.median():.1f}%  "
          f"Mean={s.mean():.1f}%  P75={s.quantile(.75):.1f}%  P90={s.quantile(.90):.1f}%  Max={s.max():.1f}%")

combined = pd.concat(all_stretch)
print(f"\nGABUNGAN KEDUA CYCLE ({len(combined)} hari):")
print(f"  Min={combined.min():.1f}%  P25={combined.quantile(.25):.1f}%  Median={combined.median():.1f}%  "
      f"Mean={combined.mean():.1f}%  P75={combined.quantile(.75):.1f}%  P90={combined.quantile(.90):.1f}%  "
      f"Max={combined.max():.1f}%")

# ── 2. Scatter: stretch >=20/30/40% -> berapa yang diikuti koreksi >=5% ────
print("\n" + "=" * 78)
print("2. STRETCH THRESHOLD vs KOREKSI >=5% SETELAHNYA (window forward 14 hari)")
print("=" * 78)

def min_price_within(idx_global, days, global_df):
    ref_date = global_df.loc[idx_global, 'date']
    end_date = ref_date + pd.Timedelta(days=days)
    seg = global_df[(global_df['date'] > ref_date) & (global_df['date'] <= end_date)]
    if seg.empty:
        return None
    return seg['price'].min()

thresholds = [20, 30, 40]
scatter_summary = []
for ep in episodes:
    ep_df = ep['df']
    print(f"\n{ep['name']}:")
    for thr in thresholds:
        days = ep_df[ep_df['stretch_pct'] >= thr]
        n_days = len(days)
        n_corrected = 0
        n_valid = 0
        for _, row in days.iterrows():
            global_idx = df.index[df['date'] == row['date']][0]
            min_p = min_price_within(global_idx, 14, df)
            if min_p is None:
                continue
            n_valid += 1
            drop = (min_p / row['price'] - 1) * 100
            if drop <= -5:
                n_corrected += 1
        pct = f"{n_corrected/n_valid*100:.0f}%" if n_valid > 0 else "N/A"
        print(f"  Stretch >= {thr}%: {n_days} hari (valid={n_valid})  ->  "
              f"{n_corrected} diikuti koreksi >=5% dalam 14 hari ({pct})")
        scatter_summary.append({'episode': ep['name'], 'threshold': thr, 'n_days': n_days,
                                 'n_valid': n_valid, 'n_corrected': n_corrected})

print(f"\nGABUNGAN KEDUA CYCLE:")
for thr in thresholds:
    rows = [r for r in scatter_summary if r['threshold'] == thr]
    n_days = sum(r['n_days'] for r in rows)
    n_valid = sum(r['n_valid'] for r in rows)
    n_corrected = sum(r['n_corrected'] for r in rows)
    pct = f"{n_corrected/n_valid*100:.0f}%" if n_valid > 0 else "N/A"
    print(f"  Stretch >= {thr}%: {n_days} hari (valid={n_valid})  ->  "
          f"{n_corrected} diikuti koreksi >=5% dalam 14 hari ({pct})")

# ── 3. Rata-rata stretch tertinggi sebelum tiap koreksi >=5% ────────────────
print("\n" + "=" * 78)
print("3. STRETCH TERTINGGI (DI LOCAL PEAK) SEBELUM SETIAP KOREKSI >=5% DI Z2/Z3")
print("=" * 78)

def find_pullbacks(ep_df, min_drop_pct=5.0):
    d = ep_df.copy().reset_index(drop=True)
    d['run_peak'] = d['price'].cummax()
    d['run_peak_idx'] = d['price'].expanding().apply(lambda x: x.values.argmax()).astype(int)
    d['dd_pct'] = (d['price'] / d['run_peak'] - 1) * 100
    in_pb = d['dd_pct'] <= -min_drop_pct

    pullbacks = []
    i, n = 0, len(d)
    while i < n:
        if in_pb.iloc[i]:
            peak_idx = int(d.loc[i, 'run_peak_idx'])
            j = i
            while j < n and in_pb.iloc[j] and d.loc[j, 'run_peak_idx'] == peak_idx:
                j += 1
            trough_slice = d.iloc[i:j]
            trough_pos = trough_slice['price'].idxmin()
            pullbacks.append({
                'peak_idx': peak_idx, 'peak_date': d.loc[peak_idx, 'date'],
                'peak_price': d.loc[peak_idx, 'price'], 'peak_stretch': d.loc[peak_idx, 'stretch_pct'],
                'trough_date': d.loc[trough_pos, 'date'], 'trough_price': d.loc[trough_pos, 'price'],
                'drop_pct': d.loc[trough_pos, 'dd_pct'],
            })
            i = j
        else:
            i += 1
    return pullbacks

all_peak_stretches = []
for ep in episodes:
    pullbacks = find_pullbacks(ep['df'])
    print(f"\n{ep['name']}: {len(pullbacks)} koreksi >=5% terdeteksi")
    for k, pb in enumerate(pullbacks, 1):
        print(f"  #{k}: peak {pb['peak_date'].date()} (${pb['peak_price']:,.0f}, "
              f"stretch={pb['peak_stretch']:+.1f}%) -> trough {pb['trough_date'].date()} "
              f"(${pb['trough_price']:,.0f}), drop {pb['drop_pct']:.1f}%")
        all_peak_stretches.append(pb['peak_stretch'])
    if pullbacks:
        avg_stretch = np.mean([pb['peak_stretch'] for pb in pullbacks])
        print(f"  Rata-rata stretch di peak sebelum koreksi (cycle ini): {avg_stretch:+.1f}%")

if all_peak_stretches:
    print(f"\nRATA-RATA STRETCH TERTINGGI SEBELUM KOREKSI >=5% (GABUNGAN, n={len(all_peak_stretches)}): "
          f"{np.mean(all_peak_stretches):+.1f}%  (median={np.median(all_peak_stretches):+.1f}%)")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
