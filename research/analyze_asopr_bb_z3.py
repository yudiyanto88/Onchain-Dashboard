"""
aSOPR Bollinger Band — sinyal koreksi selama Z3 (bear recovery 2019 & 2023)

Z3 def: RP (Realized Price) <= Price <= AVIV Mean.
BB dihitung dari full historical aSOPR series (rolling MA + rolling std),
lalu signal dicek hanya saat berada di dalam window Z3 pada tahun 2019 / 2023-2024.

MA period: 14, 20, 30 hari. Std multiplier: 1.5, 2.0. (6 kombinasi)
Signal = aSOPR menyentuh/melewati upper band (>=). Konsekutif hari dikumpulkan
jadi satu signal (tanggal signal = hari pertama menyentuh upper band).
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load & merge ─────────────────────────────────────────────────────────────
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])
av = pd.read_csv('data_aviv.csv', parse_dates=['date'])
mo = pd.read_csv('data_momentum.csv', parse_dates=['date'])

df = pl[['date', 'btc_price', 'realized_price']].merge(
    av[['date', 'price_at_aviv_mean']], on='date', how='inner'
).merge(
    mo[['date', 'asopr']], on='date', how='inner'
)
df = df.rename(columns={'price_at_aviv_mean': 'aviv_mean'})
df = df.dropna(subset=['btc_price', 'realized_price', 'aviv_mean', 'asopr']).sort_values('date').reset_index(drop=True)

df['in_z3'] = (df['btc_price'] >= df['realized_price']) & (df['btc_price'] <= df['aviv_mean'])

# ── Locate Z3 windows within each bear-recovery period ──────────────────────
def find_z3_windows(d, search_start, search_end):
    win = d[(d['date'] >= search_start) & (d['date'] <= search_end)].reset_index(drop=True)
    mask = win['in_z3']
    windows = []
    i, n = 0, len(win)
    while i < n:
        if mask.iloc[i]:
            j = i
            while j < n and mask.iloc[j]:
                j += 1
            windows.append((win.loc[i, 'date'], win.loc[j - 1, 'date']))
            i = j
        else:
            i += 1
    return windows

periods = [
    ('2019 BEAR RECOVERY', '2019-01-01', '2019-12-31'),
    ('2023 BEAR RECOVERY', '2023-01-01', '2024-12-31'),
]

print("=" * 78)
print("Z3 WINDOWS DITEMUKAN (RP <= Price <= AVIV Mean)")
print("=" * 78)
episode_windows = []
for name, ws, we in periods:
    wins = find_z3_windows(df, ws, we)
    print(f"\n{name}:")
    if not wins:
        print("  Tidak ada window Z3 ditemukan.")
        continue
    for a, b in wins:
        ndays = (df[(df['date'] >= a) & (df['date'] <= b)]).shape[0]
        print(f"  {a.date()} -> {b.date()}  ({ndays} hari)")
    # pakai SEMUA window Z3 (>=3 hari, buang noise super pendek) di periode ini
    usable = [w for w in wins if (w[1] - w[0]).days >= 2]
    if name == '2019 BEAR RECOVERY':
        # filter ke leg awal recovery saja (harga naik dari bottom, bukan fase
        # jatuh balik ke Z3 setelah peak Juni 2019)
        usable = [w for w in usable if w[0] <= pd.Timestamp('2019-06-30')]
    for w in usable:
        episode_windows.append({'name': name, 'start': w[0], 'end': w[1]})
    print(f"  -> Dipakai ({len(usable)} window, total {sum((w[1]-w[0]).days+1 for w in usable)} hari): "
          + ", ".join(f"{w[0].date()}->{w[1].date()}" for w in usable))

# ── Bollinger Band combos ────────────────────────────────────────────────────
ma_periods = [14, 20, 30]
std_mults = [1.5, 2.0]

for p in ma_periods:
    df[f'ma_{p}'] = df['asopr'].rolling(p).mean()
    df[f'std_{p}'] = df['asopr'].rolling(p).std()

def gain_after(idx, days, global_df):
    ref_date = global_df.loc[idx, 'date']
    target_date = ref_date + pd.Timedelta(days=days)
    fut = global_df[global_df['date'] >= target_date]
    if fut.empty:
        return None
    return fut.iloc[0]['btc_price']

def min_price_within(idx, days, global_df):
    ref_date = global_df.loc[idx, 'date']
    end_date = ref_date + pd.Timedelta(days=days)
    seg = global_df[(global_df['date'] > ref_date) & (global_df['date'] <= end_date)]
    if seg.empty:
        return None
    return seg['btc_price'].min()

combo_summary = []
detail_rows = []

print("\n" + "=" * 78)
print("SIGNAL DETECTION PER KOMBINASI (aSOPR touch/cross upper band, dalam Z3)")
print("=" * 78)

for ma_p in ma_periods:
    for mult in std_mults:
        upper_col = f'upper_{ma_p}_{mult}'
        df[upper_col] = df[f'ma_{ma_p}'] + mult * df[f'std_{ma_p}']

        combo_signals = []
        for ep in episode_windows:
            ep_df = df[(df['date'] >= ep['start']) & (df['date'] <= ep['end'])].reset_index(drop=True)
            ep_df = ep_df.dropna(subset=[upper_col])
            touch = ep_df['asopr'] >= ep_df[upper_col]

            i, n = 0, len(ep_df)
            while i < n:
                if touch.iloc[i]:
                    j = i
                    while j < n and touch.iloc[j]:
                        j += 1
                    sig_idx_local = i  # first day of touch
                    global_idx = df.index[df['date'] == ep_df.loc[sig_idx_local, 'date']][0]
                    sig_date = df.loc[global_idx, 'date']
                    sig_price = df.loc[global_idx, 'btc_price']
                    price_7d = gain_after(global_idx, 7, df)
                    price_14d = gain_after(global_idx, 14, df)
                    min_14d = min_price_within(global_idx, 14, df)
                    if min_14d is not None:
                        drop_pct = (min_14d / sig_price - 1) * 100
                        corrected = bool(drop_pct <= -5)
                    else:
                        drop_pct = None
                        corrected = None
                    combo_signals.append({
                        'episode': ep['name'], 'date': sig_date, 'price': sig_price,
                        'price_7d': price_7d, 'price_14d': price_14d,
                        'min_drop_14d_pct': drop_pct, 'corrected_5pct': corrected,
                    })
                    i = j
                else:
                    i += 1

        n_total = len(combo_signals)
        n_valid = sum(1 for s in combo_signals if s['corrected_5pct'] is not None)
        n_correct = sum(1 for s in combo_signals if s['corrected_5pct'] is True)
        n_false = n_valid - n_correct

        combo_summary.append({
            'ma_period': ma_p, 'std_mult': mult,
            'n_signal': n_total, 'n_valid': n_valid,
            'n_correction_ge5pct': n_correct, 'n_false': n_false,
        })
        for s in combo_signals:
            s['ma_period'] = ma_p
            s['std_mult'] = mult
            detail_rows.append(s)

        print(f"\nMA={ma_p}  Std={mult}  -> total signal={n_total}, koreksi>=5%={n_correct}, false={n_false}")
        for s in combo_signals:
            p7 = f"${s['price_7d']:,.0f}" if s['price_7d'] is not None else "N/A"
            p14 = f"${s['price_14d']:,.0f}" if s['price_14d'] is not None else "N/A"
            dd = f"{s['min_drop_14d_pct']:+.1f}%" if s['min_drop_14d_pct'] is not None else "N/A"
            flag = "YA" if s['corrected_5pct'] else ("TIDAK" if s['corrected_5pct'] is False else "N/A")
            print(f"  [{s['episode']}] {s['date'].date()}  price=${s['price']:,.0f}  "
                  f"+7d={p7}  +14d={p14}  max_drop_14d={dd}  koreksi>=5%? {flag}")

# ── Summary table ─────────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("TABEL RINGKASAN PER KOMBINASI")
print("=" * 78)
print(f"{'MA':>5}{'Std':>7}{'#Signal':>10}{'#Koreksi>=5%':>15}{'#False':>9}{'Hit Rate':>11}")
for r in combo_summary:
    hit_rate = f"{r['n_correction_ge5pct']/r['n_valid']*100:.0f}%" if r['n_valid'] > 0 else "N/A"
    print(f"{r['ma_period']:>5}{r['std_mult']:>7.1f}{r['n_signal']:>10}{r['n_correction_ge5pct']:>15}"
          f"{r['n_false']:>9}{hit_rate:>11}")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
