"""
Bull dip ke Z4 — identifikasi episode + test 3 kondisi (F&G<50, STH Loss>=60%,
min(aSOPR,STH-SOPR)<=0.98) selama bull market 2019-2020 dan 2023-2024.

Zona:
  Z5 = Price >= AVIV Upper (0.5 sigma)
  Z4 = AVIV Mean <= Price < AVIV Upper
  (di bawah Z4 = di luar cakupan, bukan bagian dari definisi bull dip ke Z4)

Episode bull dip ke Z4 = run hari konsekutif zona Z4 yang PERSIS mengikuti
hari-hari zona Z5 sebelumnya (price baru saja turun dari Z5 ke Z4).
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load & merge ─────────────────────────────────────────────────────────────
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

# ── Identifikasi episode bull dip ke Z4 (Z5 -> Z4 transition) ───────────────
def find_bull_dip_episodes(d, search_start, search_end, resolve_buffer_end, episode_start_cutoff):
    # search window extended by resolve_buffer_end supaya episode yang mulai
    # sebelum episode_start_cutoff tapi baru resolve setelahnya tetap akurat
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
                'resolved_as': ('RECOVERED ke Z5' if end_zone == 'Z5' else
                                'BREAKDOWN di bawah Z4' if end_zone == 'below' else 'END OF DATA'),
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
print("=" * 78)
print("EPISODE BULL DIP KE Z4 TERIDENTIFIKASI")
print("=" * 78)
for name, ws, we, buf, cutoff in periods:
    eps = find_bull_dip_episodes(df, ws, we, buf, cutoff)
    print(f"\n{name}: {len(eps)} episode")
    for k, ep in enumerate(eps, 1):
        drop_pct = (ep['trough_price'] / ep['from_price'] - 1) * 100
        print(f"  #{k}: {ep['start_date'].date()} -> {ep['end_date'].date()} ({ep['n_days']} hari)  "
              f"dari Z5 (${ep['from_price']:,.0f} @ {ep['from_date'].date()})  "
              f"trough ${ep['trough_price']:,.0f} @ {ep['trough_date'].date()} ({drop_pct:+.1f}%)  "
              f"-> {ep['resolved_as']}")
        ep['period'] = name
        all_episodes.append(ep)

# ── Test 3 kondisi per episode ───────────────────────────────────────────────
print("\n" + "=" * 78)
print("TEST 3 KONDISI PER EPISODE (selama durasi dip di Z4)")
print("=" * 78)

results = []
for ep in all_episodes:
    win = ep['win']
    i0, i1 = ep['seg_idx']
    seg = win.loc[i0:i1]

    fg_below50 = bool((seg['fg'] < 50).any()) if seg['fg'].notna().any() else None
    fg_min = seg['fg'].min() if seg['fg'].notna().any() else None
    sth_loss_max = 100 - seg['pct_sth_in_profit'].min() if 'pct_sth_in_profit' in seg else None
    sth_loss_ge60 = bool(sth_loss_max >= 60) if sth_loss_max is not None else None
    sopr_min = seg['min_sopr'].min()
    sopr_le098 = bool(sopr_min <= 0.98)

    n_met = sum([bool(fg_below50), bool(sth_loss_ge60), bool(sopr_le098)])

    print(f"\n[{ep['period']}] Episode {ep['start_date'].date()}->{ep['end_date'].date()}:")
    print(f"  1. F&G < 50 selama dip?  {'YA' if fg_below50 else 'TIDAK' if fg_below50 is not None else 'N/A'}"
          f"  (F&G min = {fg_min:.0f})" if fg_min is not None else "  (F&G data N/A)")
    print(f"  2. STH Loss >= 60%?      {'YA' if sth_loss_ge60 else 'TIDAK'}  (STH Loss max = {sth_loss_max:.1f}%)")
    print(f"  3. min(aSOPR,STH-SOPR) <= 0.98?  {'YA' if sopr_le098 else 'TIDAK'}  (min = {sopr_min:.4f})")
    print(f"  -> {n_met}/3 kondisi terpenuhi")

    results.append({
        'period': ep['period'], 'start': ep['start_date'].date(), 'end': ep['end_date'].date(),
        'n_days': ep['n_days'], 'drop_pct': (ep['trough_price']/ep['from_price']-1)*100,
        'fg_below50': fg_below50, 'sth_loss_ge60': sth_loss_ge60, 'sopr_le098': sopr_le098,
        'n_met': n_met,
    })

# ── Tabel ringkasan ───────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("TABEL RINGKASAN PER EPISODE")
print("=" * 78)
print(f"{'Period':<16}{'Start':<12}{'End':<12}{'Days':>6}{'Drop%':>8}{'F&G<50':>8}{'STHLoss>=60':>13}{'SOPR<=0.98':>12}{'N/3':>5}")
for r in results:
    fg_s = 'YA' if r['fg_below50'] else ('TIDAK' if r['fg_below50'] is not None else 'N/A')
    sl_s = 'YA' if r['sth_loss_ge60'] else 'TIDAK'
    so_s = 'YA' if r['sopr_le098'] else 'TIDAK'
    print(f"{r['period']:<16}{str(r['start']):<12}{str(r['end']):<12}{r['n_days']:>6}{r['drop_pct']:>7.1f}%"
          f"{fg_s:>8}{sl_s:>13}{so_s:>12}{r['n_met']:>5}")

print("\n" + "=" * 78)
print("PERSENTASE EPISODE YANG MEMENUHI TIAP KONDISI")
print("=" * 78)
n_total = len(results)
n_fg = sum(1 for r in results if r['fg_below50'])
n_sl = sum(1 for r in results if r['sth_loss_ge60'])
n_so = sum(1 for r in results if r['sopr_le098'])
print(f"Total episode: {n_total}")
print(f"  F&G < 50 selama dip:            {n_fg}/{n_total} ({n_fg/n_total*100:.0f}%)")
print(f"  STH Loss >= 60%:                {n_sl}/{n_total} ({n_sl/n_total*100:.0f}%)")
print(f"  min(aSOPR,STH-SOPR) <= 0.98:    {n_so}/{n_total} ({n_so/n_total*100:.0f}%)")

dist = pd.Series([r['n_met'] for r in results]).value_counts().sort_index()
print(f"\nDistribusi jumlah kondisi terpenuhi (0-3):")
for k in range(4):
    c = dist.get(k, 0)
    print(f"  {k}/3 kondisi: {c} episode ({c/n_total*100:.0f}%)")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
