"""
Test 3 kondisi (threshold disesuaikan Z4/Z5) sebagai trigger tambahan K2
(bull dip) — pakai 14 episode bull dip ke Z4 yang sama dari
analyze_bull_dip_z4_conditions.py, threshold baru:

  F&G <= 35  (vs 50 di versi K5)
  STH Loss >= 70%  (vs 60% di versi K5)
  min(aSOPR, STH-SOPR) <= 0.98  (sama)

Tujuan: cek apakah kondisi ini bisa jadi genuine BUY signal K2 (fire di
episode yang RECOVERED) atau tetap cuma warning flag (fire di episode yang
BREAKDOWN).
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load & merge (identik dengan analyze_bull_dip_z4_conditions.py) ────────
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])
av = pd.read_csv('data_aviv.csv', parse_dates=['date'])
fg = pd.read_csv('data_fg.csv', parse_dates=['date']).rename(columns={'Fear & Greed': 'fg'})
sp = pd.read_csv('data_supply.csv', parse_dates=['date'])
mo = pd.read_csv('data_momentum.csv', parse_dates=['date'])

df = pl[['date', 'btc_price']].merge(
    av[['date', 'price_at_aviv_mean', 'price_at_aviv_plus_1_sigma']], on='date', how='inner'
).merge(
    fg[['date', 'fg']], on='date', how='left'
).merge(
    sp[['date', 'pct_sth_in_profit', 'pct_sth_in_loss']], on='date', how='inner'
).merge(
    mo[['date', 'asopr', 'sth_sopr']], on='date', how='inner'
)
df = df.rename(columns={'btc_price': 'price', 'price_at_aviv_mean': 'aviv_mean'})
df['aviv_upper'] = df['aviv_mean'] + 0.5 * (df['price_at_aviv_plus_1_sigma'] - df['aviv_mean'])
df['min_sopr'] = df[['asopr', 'sth_sopr']].min(axis=1)
df = df.dropna(subset=['price', 'aviv_mean', 'aviv_upper', 'pct_sth_in_loss', 'min_sopr'])
df = df.sort_values('date').reset_index(drop=True)

def zone(row):
    if row['price'] >= row['aviv_upper']:
        return 'Z5'
    elif row['price'] >= row['aviv_mean']:
        return 'Z4'
    else:
        return 'below'

df['zone'] = df.apply(zone, axis=1)

def find_bull_dip_episodes(d, search_start, search_end, resolve_buffer_end, episode_start_cutoff):
    win = d[(d['date'] >= search_start) & (d['date'] <= resolve_buffer_end)].reset_index(drop=True)
    n = len(win)
    episodes = []
    i = 1
    while i < n:
        if win.loc[i, 'zone'] == 'Z4' and win.loc[i - 1, 'zone'] == 'Z5':
            j = i
            while j < n and win.loc[j, 'zone'] == 'Z4':
                j += 1
            seg = win.iloc[i:j]
            trough_idx = seg['price'].idxmin()
            end_zone = win.loc[j, 'zone'] if j < n else 'END OF DATA'
            start_date = win.loc[i, 'date']
            if start_date > pd.Timestamp(episode_start_cutoff):
                i = j
                continue
            episodes.append({
                'start_date': start_date, 'end_date': win.loc[j - 1, 'date'],
                'n_days': j - i,
                'from_price': win.loc[i - 1, 'price'], 'from_date': win.loc[i - 1, 'date'],
                'trough_date': win.loc[trough_idx, 'date'], 'trough_price': win.loc[trough_idx, 'price'],
                'resolved_as': ('RECOVERED' if end_zone == 'Z5' else
                                'BREAKDOWN' if end_zone == 'below' else 'END OF DATA'),
                'seg_idx': (win.index[i], win.index[j - 1]),
                'win': win,
            })
            i = j
        else:
            i += 1
    return episodes

periods = [
    ('BULL 2019-2020', '2019-01-01', '2020-12-31', '2021-03-31', '2020-12-31'),
    ('BULL 2023-2024', '2023-01-01', '2024-12-31', '2025-03-31', '2024-12-31'),
]

all_episodes = []
for name, ws, we, buf, cutoff in periods:
    eps = find_bull_dip_episodes(df, ws, we, buf, cutoff)
    for ep in eps:
        ep['period'] = name
        all_episodes.append(ep)

print("=" * 78)
print(f"TOTAL {len(all_episodes)} EPISODE BULL DIP KE Z4 (2019-2020 & 2023-2024)")
print("=" * 78)

# ── Test 3 kondisi dengan THRESHOLD K2 (disesuaikan Z4/Z5) ──────────────────
FG_THR = 35
STH_LOSS_THR = 70
SOPR_THR = 0.98

print(f"\nThreshold K2: F&G <= {FG_THR}  |  STH Loss >= {STH_LOSS_THR}%  |  min(aSOPR,STH-SOPR) <= {SOPR_THR}")
print("=" * 78)

results = []
for ep in all_episodes:
    win = ep['win']
    i0, i1 = ep['seg_idx']
    seg = win.loc[i0:i1]

    fg_ok = bool((seg['fg'] <= FG_THR).any()) if seg['fg'].notna().any() else None
    fg_min = seg['fg'].min() if seg['fg'].notna().any() else None
    sth_loss_max = 100 - seg['pct_sth_in_profit'].min()
    sth_loss_ok = bool(sth_loss_max >= STH_LOSS_THR)
    sopr_min = seg['min_sopr'].min()
    sopr_ok = bool(sopr_min <= SOPR_THR)

    n_met = sum([bool(fg_ok), bool(sth_loss_ok), bool(sopr_ok)])

    print(f"\n[{ep['period']}] Episode {ep['start_date'].date()}->{ep['end_date'].date()} "
          f"({ep['resolved_as']}):")
    print(f"  1. F&G <= {FG_THR}?  {'YA' if fg_ok else 'TIDAK'}  (F&G min = {fg_min:.0f})" if fg_min is not None
          else f"  1. F&G <= {FG_THR}?  N/A")
    print(f"  2. STH Loss >= {STH_LOSS_THR}%?  {'YA' if sth_loss_ok else 'TIDAK'}  (STH Loss max = {sth_loss_max:.1f}%)")
    print(f"  3. min(aSOPR,STH-SOPR) <= {SOPR_THR}?  {'YA' if sopr_ok else 'TIDAK'}  (min = {sopr_min:.4f})")
    print(f"  -> {n_met}/3 kondisi terpenuhi")

    results.append({
        'period': ep['period'], 'start': ep['start_date'].date(), 'end': ep['end_date'].date(),
        'n_days': ep['n_days'], 'drop_pct': (ep['trough_price']/ep['from_price']-1)*100,
        'fg_ok': fg_ok, 'sth_loss_ok': sth_loss_ok, 'sopr_ok': sopr_ok,
        'n_met': n_met, 'resolved_as': ep['resolved_as'],
    })

# ── Tabel ringkasan ───────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("TABEL RINGKASAN PER EPISODE (THRESHOLD K2)")
print("=" * 78)
print(f"{'Period':<16}{'Start':<12}{'End':<12}{'Days':>6}{'Drop%':>8}{'F&G<=35':>9}{'STHLoss>=70':>13}{'SOPR<=0.98':>12}{'N/3':>5}{'Resolusi':>12}")
for r in results:
    fg_s = 'YA' if r['fg_ok'] else ('TIDAK' if r['fg_ok'] is not None else 'N/A')
    sl_s = 'YA' if r['sth_loss_ok'] else 'TIDAK'
    so_s = 'YA' if r['sopr_ok'] else 'TIDAK'
    print(f"{r['period']:<16}{str(r['start']):<12}{str(r['end']):<12}{r['n_days']:>6}{r['drop_pct']:>7.1f}%"
          f"{fg_s:>9}{sl_s:>13}{so_s:>12}{r['n_met']:>5}{r['resolved_as']:>12}")

# ── Persentase per kondisi ────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("PERSENTASE EPISODE YANG MEMENUHI TIAP KONDISI (n=14)")
print("=" * 78)
n_total = len(results)
n_fg = sum(1 for r in results if r['fg_ok'])
n_sl = sum(1 for r in results if r['sth_loss_ok'])
n_so = sum(1 for r in results if r['sopr_ok'])
print(f"  F&G <= {FG_THR}:              {n_fg}/{n_total} ({n_fg/n_total*100:.0f}%)")
print(f"  STH Loss >= {STH_LOSS_THR}%:          {n_sl}/{n_total} ({n_sl/n_total*100:.0f}%)")
print(f"  min(aSOPR,STH-SOPR) <= {SOPR_THR}:  {n_so}/{n_total} ({n_so/n_total*100:.0f}%)")

dist = pd.Series([r['n_met'] for r in results]).value_counts().sort_index()
print(f"\nDistribusi jumlah kondisi terpenuhi (0-3):")
for k in range(4):
    c = dist.get(k, 0)
    print(f"  {k}/3 kondisi: {c} episode ({c/n_total*100:.0f}%)")

# ── Cross-tab: n_met vs resolusi ─────────────────────────────────────────────
print("\n" + "=" * 78)
print("BREAKDOWN RESOLUSI PER JUMLAH KONDISI TERPENUHI")
print("=" * 78)
print(f"{'N kondisi':>10}{'#Episode':>10}{'#RECOVERED':>12}{'#BREAKDOWN':>12}{'% RECOVERED':>13}")
for k in range(4):
    grp = [r for r in results if r['n_met'] == k]
    n = len(grp)
    if n == 0:
        continue
    n_rec = sum(1 for r in grp if r['resolved_as'] == 'RECOVERED')
    n_bd = sum(1 for r in grp if r['resolved_as'] == 'BREAKDOWN')
    pct_rec = f"{n_rec/n*100:.0f}%" if n > 0 else "N/A"
    print(f"{k:>10}{n:>10}{n_rec:>12}{n_bd:>12}{pct_rec:>13}")

# ── Hit rate: episode dengan >=1 kondisi -> berapa yang RECOVERED ───────────
print("\n" + "=" * 78)
print("HIT RATE UNTUK K2: DARI EPISODE DENGAN >=1 KONDISI, BERAPA YANG RECOVERED?")
print("=" * 78)
ge1 = [r for r in results if r['n_met'] >= 1]
zero = [r for r in results if r['n_met'] == 0]
n_ge1 = len(ge1)
n_ge1_rec = sum(1 for r in ge1 if r['resolved_as'] == 'RECOVERED')
n_ge1_bd = sum(1 for r in ge1 if r['resolved_as'] == 'BREAKDOWN')
n_zero = len(zero)
n_zero_rec = sum(1 for r in zero if r['resolved_as'] == 'RECOVERED')

print(f"Episode dengan >=1 kondisi terpenuhi: {n_ge1}")
print(f"  -> RECOVERED: {n_ge1_rec}/{n_ge1} ({n_ge1_rec/n_ge1*100:.0f}%)" if n_ge1 > 0 else "  -> tidak ada episode")
print(f"  -> BREAKDOWN: {n_ge1_bd}/{n_ge1} ({n_ge1_bd/n_ge1*100:.0f}%)" if n_ge1 > 0 else "")
print(f"\nEpisode dengan 0 kondisi terpenuhi: {n_zero}")
print(f"  -> RECOVERED: {n_zero_rec}/{n_zero} ({n_zero_rec/n_zero*100:.0f}%)" if n_zero > 0 else "")

print("\nDetail episode dengan >=1 kondisi terpenuhi:")
for r in ge1:
    print(f"  [{r['period']}] {r['start']}->{r['end']}  N={r['n_met']}/3  -> {r['resolved_as']}")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
