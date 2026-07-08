"""
STH-MVRV (Price/STH_RP) sebagai proxy K6 trigger — Z2+Z3, cycle 2019 & 2023

Z2 mulai: STH RP cross ke atas RP (Realized Price).
Z3 berakhir: Price cross ke atas AVIV Upper (0.5 sigma), bertahan >=3 hari.
STH-MVRV = Price / STH_RP

Window detection direplikasi dari analyze_k5_dip_entry_trigger.py /
analyze_price_stretch_sth_rp.py (metodologi konsisten).
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
df['sth_mvrv'] = df['price'] / df['sth_rp']
df = df.dropna(subset=['price', 'rp', 'sth_rp', 'aviv_mean', 'aviv_upper', 'sth_mvrv'])
df = df.sort_values('date').reset_index(drop=True)

# ── Locate Z2 start / Z3 end per cycle ──────────────────────────────────────
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

# ── 1. Distribusi STH-MVRV harian ───────────────────────────────────────────
print("\n" + "=" * 78)
print("1. DISTRIBUSI STH-MVRV HARIAN (Price / STH_RP)")
print("=" * 78)

all_series = []
for ep in episodes:
    s = ep['df']['sth_mvrv']
    all_series.append(s)
    print(f"\n{ep['name']} ({len(s)} hari):")
    print(f"  Min={s.min():.3f}  P25={s.quantile(.25):.3f}  Median={s.median():.3f}  "
          f"Mean={s.mean():.3f}  P75={s.quantile(.75):.3f}  P90={s.quantile(.90):.3f}  Max={s.max():.3f}")

combined = pd.concat(all_series)
print(f"\nGABUNGAN KEDUA CYCLE ({len(combined)} hari):")
print(f"  Min={combined.min():.3f}  P25={combined.quantile(.25):.3f}  Median={combined.median():.3f}  "
      f"Mean={combined.mean():.3f}  P75={combined.quantile(.75):.3f}  P90={combined.quantile(.90):.3f}  "
      f"Max={combined.max():.3f}")

# ── 2. Threshold test (signal = consecutive days collapsed to first day) ───
print("\n" + "=" * 78)
print("2. THRESHOLD STH-MVRV vs KOREKSI >=5% DALAM 14 HARI (signal = touch, konsekutif digabung)")
print("=" * 78)

def min_price_within(idx_global, days, global_df):
    ref_date = global_df.loc[idx_global, 'date']
    end_date = ref_date + pd.Timedelta(days=days)
    seg = global_df[(global_df['date'] > ref_date) & (global_df['date'] <= end_date)]
    if seg.empty:
        return None
    return seg['price'].min()

def detect_signals(ep_df, threshold):
    d = ep_df.reset_index(drop=True)
    touch = d['sth_mvrv'] >= threshold
    signals = []
    i, n = 0, len(d)
    while i < n:
        if touch.iloc[i]:
            j = i
            while j < n and touch.iloc[j]:
                j += 1
            signals.append(d.loc[i, 'date'])
            i = j
        else:
            i += 1
    return signals

thresholds = [1.10, 1.15, 1.20, 1.25, 1.30, 1.40, 1.50]
threshold_summary = []

for ep in episodes:
    print(f"\n{ep['name']}:")
    for thr in thresholds:
        sig_dates = detect_signals(ep['df'], thr)
        n_sig = len(sig_dates)
        n_valid, n_corrected = 0, 0
        for sd in sig_dates:
            global_idx = df.index[df['date'] == sd][0]
            sig_price = df.loc[global_idx, 'price']
            min_p = min_price_within(global_idx, 14, df)
            if min_p is None:
                continue
            n_valid += 1
            drop = (min_p / sig_price - 1) * 100
            if drop <= -5:
                n_corrected += 1
        hit_rate = f"{n_corrected/n_valid*100:.0f}%" if n_valid > 0 else "N/A"
        print(f"  STH-MVRV >= {thr:.2f}: {n_sig} signal (valid={n_valid})  -> "
              f"{n_corrected} koreksi>=5% ({hit_rate})")
        threshold_summary.append({'episode': ep['name'], 'threshold': thr, 'n_signal': n_sig,
                                   'n_valid': n_valid, 'n_corrected': n_corrected})

print(f"\nGABUNGAN KEDUA CYCLE:")
combined_rows = []
for thr in thresholds:
    rows = [r for r in threshold_summary if r['threshold'] == thr]
    n_sig = sum(r['n_signal'] for r in rows)
    n_valid = sum(r['n_valid'] for r in rows)
    n_corrected = sum(r['n_corrected'] for r in rows)
    hit_rate = f"{n_corrected/n_valid*100:.0f}%" if n_valid > 0 else "N/A"
    print(f"  STH-MVRV >= {thr:.2f}: {n_sig} signal (valid={n_valid})  -> "
          f"{n_corrected} koreksi>=5% ({hit_rate})")
    combined_rows.append({'threshold': thr, 'n_signal': n_sig, 'n_valid': n_valid,
                           'n_corrected': n_corrected,
                           'hit_rate': (n_corrected/n_valid*100) if n_valid > 0 else None})

# ── 3. Rata-rata STH-MVRV di local peak sebelum tiap koreksi >=5% ──────────
print("\n" + "=" * 78)
print("3. STH-MVRV DI LOCAL PEAK SEBELUM SETIAP KOREKSI >=5% DI Z2/Z3")
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
                'peak_price': d.loc[peak_idx, 'price'], 'peak_mvrv': d.loc[peak_idx, 'sth_mvrv'],
                'trough_date': d.loc[trough_pos, 'date'], 'trough_price': d.loc[trough_pos, 'price'],
                'drop_pct': d.loc[trough_pos, 'dd_pct'],
            })
            i = j
        else:
            i += 1
    return pullbacks

all_peak_mvrv = []
for ep in episodes:
    pullbacks = find_pullbacks(ep['df'])
    print(f"\n{ep['name']}: {len(pullbacks)} koreksi >=5% terdeteksi")
    for k, pb in enumerate(pullbacks, 1):
        print(f"  #{k}: peak {pb['peak_date'].date()} (${pb['peak_price']:,.0f}, "
              f"STH-MVRV={pb['peak_mvrv']:.3f}) -> trough {pb['trough_date'].date()} "
              f"(${pb['trough_price']:,.0f}), drop {pb['drop_pct']:.1f}%")
        all_peak_mvrv.append(pb['peak_mvrv'])
    if pullbacks:
        avg_mvrv = np.mean([pb['peak_mvrv'] for pb in pullbacks])
        print(f"  Rata-rata STH-MVRV di peak sebelum koreksi (cycle ini): {avg_mvrv:.3f}")

if all_peak_mvrv:
    print(f"\nRATA-RATA STH-MVRV DI PEAK SEBELUM KOREKSI >=5% (GABUNGAN, n={len(all_peak_mvrv)}): "
          f"{np.mean(all_peak_mvrv):.3f}  (median={np.median(all_peak_mvrv):.3f})")

# ── Tabel ringkasan threshold ────────────────────────────────────────────────
print("\n" + "=" * 78)
print("TABEL RINGKASAN THRESHOLD (GABUNGAN KEDUA CYCLE)")
print("=" * 78)
print(f"{'Threshold':>10}{'#Signal':>10}{'#Koreksi>=5%':>15}{'Hit Rate':>11}")
for r in combined_rows:
    hr = f"{r['hit_rate']:.0f}%" if r['hit_rate'] is not None else "N/A"
    print(f"{r['threshold']:>10.2f}{r['n_signal']:>10}{r['n_corrected']:>15}{hr:>11}")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
