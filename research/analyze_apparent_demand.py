"""
Uji empiris klaim video "Bitcoin Whales Are Accumulating Right Now" soal apparent_demand.

H1 (baseline): apparent_demand negatif = asosiasi bear/drawdown besar, positif = bull/uptrend?
H2 (klaim inti): deceleration pada apparent_demand SMOOTHED (masih positif, price masih
    uptrend) diikuti forward return lebih lemah dibanding baseline?
H3 (redundansi): apparent_demand smoothed berkorelasi tinggi dengan realized_cap_usd growth
    dan/atau net_realized_pl_usd (sudah dipakai framework)?

Anti-lookahead: definisi "peak" pakai pola sama seperti research/analyze_k3_stage_comparison.py
    -- titik naik lokal (backward: v[i] > v[i-1]), lalu dikonfirmasi turun terus-menerus selama
    CONFIRM_DAYS ke depan. SIGNAL DATE = i + CONFIRM_DAYS (bukan tanggal peak-nya sendiri), jadi
    semua data yang dipakai untuk "keputusan" di signal date sudah tersedia pada tanggal itu.
"""

import pandas as pd
import numpy as np
import sys

sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

MASTER = r"D:\Claude Code\Projects\Onchain-Dashboard\data_master_all_metrics.csv"

# ─── Load ────────────────────────────────────────────────────────────────────
df = pd.read_csv(MASTER, parse_dates=['date'])
cols = ['date', 'btc_price', 'apparent_demand', 'realized_cap_usd', 'net_realized_pl_usd', '200_dma']
df = df[cols].dropna().sort_values('date').reset_index(drop=True)
df = df[df['btc_price'] > 0].reset_index(drop=True)

print("=" * 100)
print(f"Data range: {df['date'].min().date()} s/d {df['date'].max().date()}  |  n hari = {len(df)}")
print("=" * 100)

# ─── Cycle definition (dipakai konsisten untuk sebaran n per cycle) ─────────
CYCLES = [
    ("2011-2013", "2010-07-17", "2013-11-30"),
    ("2013-2015 (bear)", "2013-12-01", "2015-08-31"),
    ("2015-2017", "2015-09-01", "2017-12-31"),
    ("2018-2019 (bear)", "2018-01-01", "2019-06-30"),
    ("2019-2021", "2019-07-01", "2021-11-30"),
    ("2022 (bear)", "2021-12-01", "2022-12-31"),
    ("2023-2025", "2023-01-01", "2025-12-31"),
    ("2026+", "2026-01-01", "2030-01-01"),
]

def label_cycle(date):
    for name, start, end in CYCLES:
        if pd.Timestamp(start) <= date <= pd.Timestamp(end):
            return name
    return "UNLABELED"

df['cycle'] = df['date'].apply(label_cycle)

# ─── Smoothing ───────────────────────────────────────────────────────────────
df['ad_ma30'] = df['apparent_demand'].rolling(30, min_periods=30).mean()
df['ad_ma90'] = df['apparent_demand'].rolling(90, min_periods=90).mean()

# Trend regime proxy: price vs 200_dma (available at-date, no lookahead)
df['above_200dma'] = df['btc_price'] > df['200_dma']

# Drawdown dari rolling 365-hari trailing high (backward only, no lookahead)
df['roll_high_365'] = df['btc_price'].rolling(365, min_periods=30).max()
df['drawdown_365'] = df['btc_price'] / df['roll_high_365'] - 1.0

# =============================================================================
# H1 — SIGN-BASED BASELINE CHECK
# =============================================================================
print("\n" + "=" * 100)
print("H1 -- apparent_demand (smoothed 30d) sign vs regime (uptrend/drawdown)")
print("=" * 100)

h1 = df.dropna(subset=['ad_ma30', 'drawdown_365']).copy()
h1['ad_sign'] = np.where(h1['ad_ma30'] > 0, 'POSITIF', 'NEGATIF')
h1['regime_trend'] = np.where(h1['above_200dma'], 'UPTREND (>200dma)', 'DOWNTREND (<200dma)')
h1['regime_dd'] = np.where(h1['drawdown_365'] <= -0.20, 'BEAR (drawdown>=20%)', 'NORMAL/BULL (<20% dd)')

print(f"\nn hari valid (ad_ma30 tersedia) = {len(h1)}")
print("\n-- Crosstab: ad_ma30 sign vs price trend (200 DMA) --")
ct1 = pd.crosstab(h1['ad_sign'], h1['regime_trend'], normalize='index') * 100
print(ct1.round(1))
print("\n-- Crosstab: ad_ma30 sign vs drawdown regime (>=20% dari rolling 365d high) --")
ct2 = pd.crosstab(h1['ad_sign'], h1['regime_dd'], normalize='index') * 100
print(ct2.round(1))

print("\n-- Raw count crosstab (trend) --")
print(pd.crosstab(h1['ad_sign'], h1['regime_trend']))
print("\n-- Raw count crosstab (drawdown) --")
print(pd.crosstab(h1['ad_sign'], h1['regime_dd']))

print("\n-- Per cycle: % hari ad_ma30 positif, dan avg drawdown_365 saat ad_ma30 negatif --")
for name, _, _ in CYCLES:
    sub = h1[h1['cycle'] == name]
    if len(sub) == 0:
        continue
    pct_pos = (sub['ad_ma30'] > 0).mean() * 100
    neg = sub[sub['ad_ma30'] <= 0]
    avg_dd_neg = neg['drawdown_365'].mean() * 100 if len(neg) else np.nan
    pos = sub[sub['ad_ma30'] > 0]
    avg_dd_pos = pos['drawdown_365'].mean() * 100 if len(pos) else np.nan
    print(f"  {name:<18} n={len(sub):>5}  %positif={pct_pos:5.1f}%  "
          f"avg_dd_saat_negatif={avg_dd_neg:7.1f}%  avg_dd_saat_positif={avg_dd_pos:7.1f}%")

# =============================================================================
# H2 — DECELERATION CLAIM (klaim inti video)
# =============================================================================
print("\n" + "=" * 100)
print("H2 -- Deceleration ad_ma30 dari local high (masih positif, price uptrend) vs forward return")
print("=" * 100)

CONFIRM_DAYS = 30  # hari konfirmasi decline setelah backward turning point (selaras skala 30d MA)
COOLDOWN_DAYS = 60  # merge event berdekatan (pola existing)

d2 = df.dropna(subset=['ad_ma30']).reset_index(drop=True)
vals = d2['ad_ma30'].values
dates = d2['date'].values
n = len(d2)

peak_events = []  # (peak_idx, signal_idx)
for i in range(1, n - CONFIRM_DAYS):
    if vals[i] <= 0:  # syarat: peak harus di zona demand positif
        continue
    if vals[i] <= vals[i - 1]:  # bukan backward turning point (titik naik lokal)
        continue
    future = vals[i + 1: i + 1 + CONFIRM_DAYS]
    if len(future) < CONFIRM_DAYS:
        continue
    if all(future[j] < vals[i] for j in range(len(future))):
        sig_idx = i + CONFIRM_DAYS
        if sig_idx < n:
            peak_events.append((i, sig_idx))

print(f"\nRaw peak+decline events (sebelum cooldown merge): n = {len(peak_events)}")

# Merge/cooldown: kalau signal_idx berikutnya dalam COOLDOWN_DAYS dari signal sebelumnya, drop
merged = []
last_sig_date = None
for peak_idx, sig_idx in peak_events:
    sig_date = pd.Timestamp(dates[sig_idx])
    if last_sig_date is not None and (sig_date - last_sig_date).days < COOLDOWN_DAYS:
        continue
    merged.append((peak_idx, sig_idx))
    last_sig_date = sig_date

print(f"Setelah cooldown merge ({COOLDOWN_DAYS}d): n = {len(merged)}")

# Filter tambahan sesuai klaim H2: pada SIGNAL DATE, ad_ma30 masih positif DAN price > 200dma (uptrend)
events = []
for peak_idx, sig_idx in merged:
    row = d2.loc[sig_idx]
    peak_row = d2.loc[peak_idx]
    still_positive = row['ad_ma30'] > 0
    uptrend = row['above_200dma']
    pct_decline = (row['ad_ma30'] / peak_row['ad_ma30'] - 1) * 100 if peak_row['ad_ma30'] != 0 else np.nan
    events.append({
        'peak_date': peak_row['date'], 'peak_ad_ma30': peak_row['ad_ma30'],
        'signal_date': row['date'], 'signal_ad_ma30': row['ad_ma30'],
        'pct_decline_from_peak': pct_decline,
        'still_positive_at_signal': still_positive,
        'uptrend_at_signal': uptrend,
        'price_at_signal': row['btc_price'],
        'cycle': row['cycle'],
        'qualifies_h2': bool(still_positive and uptrend),
    })

ev_df = pd.DataFrame(events)
print(f"\nSemua event peak+decline (setelah cooldown): n = {len(ev_df)}")
if len(ev_df):
    print(ev_df[['peak_date', 'signal_date', 'peak_ad_ma30', 'signal_ad_ma30',
                  'pct_decline_from_peak', 'still_positive_at_signal', 'uptrend_at_signal', 'cycle']]
          .to_string(index=False))

qual = ev_df[ev_df['qualifies_h2']].copy() if len(ev_df) else ev_df
print(f"\nEvent yang QUALIFY klaim H2 (masih positif + price masih uptrend di signal date): n = {len(qual)}")
if len(qual):
    print("\nSebaran per cycle:")
    print(qual['cycle'].value_counts())

# Forward returns dari signal date
def forward_return(sig_date, days):
    target = sig_date + pd.Timedelta(days=days)
    fut = df[df['date'] >= target]
    if fut.empty:
        return np.nan
    price_now = df.loc[df['date'] == sig_date, 'btc_price']
    if price_now.empty:
        # cari harga terdekat <= sig_date
        cur = df[df['date'] <= sig_date]
        if cur.empty:
            return np.nan
        price_now_val = cur.iloc[-1]['btc_price']
    else:
        price_now_val = price_now.values[0]
    price_fut = fut.iloc[0]['btc_price']
    return (price_fut / price_now_val - 1) * 100

for horizon in [30, 60, 90]:
    ev_df[f'fwd_ret_{horizon}d'] = ev_df['signal_date'].apply(lambda d: forward_return(d, horizon))

if len(qual):
    for horizon in [30, 60, 90]:
        qual[f'fwd_ret_{horizon}d'] = qual['signal_date'].apply(lambda d: forward_return(d, horizon))

print("\n-- Forward return event QUALIFY H2 (per event) --")
if len(qual):
    print(qual[['signal_date', 'cycle', 'fwd_ret_30d', 'fwd_ret_60d', 'fwd_ret_90d']].to_string(index=False))

# Baseline forward return: unconditional overall, DAN conditional saat price uptrend (apples-to-apples)
print("\n-- Baseline forward return (unconditional, semua hari 2010-2026) --")
baseline_rows = []
for horizon in [30, 60, 90]:
    df[f'fwd_ret_{horizon}d_all'] = df['btc_price'].shift(-horizon * 1) / df['btc_price'] - 1
    # Pakai kalender-day shift approx: index harian, cukup akurat karena data harian kontinu
for horizon in [30, 60, 90]:
    col = f'fwd_ret_{horizon}d_all'
    mean_all = df[col].mean() * 100
    med_all = df[col].median() * 100
    # baseline uptrend-only (apples to apples dengan syarat H2: price > 200dma)
    up_mask = df['above_200dma']
    mean_up = df.loc[up_mask, col].mean() * 100
    med_up = df.loc[up_mask, col].median() * 100
    baseline_rows.append((horizon, mean_all, med_all, mean_up, med_up))
    print(f"  {horizon}d: mean_all={mean_all:6.1f}%  median_all={med_all:6.1f}%  |  "
          f"mean_uptrend_only={mean_up:6.1f}%  median_uptrend_only={med_up:6.1f}%")

print("\n-- Ringkasan event QUALIFY H2 vs baseline --")
if len(qual):
    for horizon in [30, 60, 90]:
        col = f'fwd_ret_{horizon}d'
        vals_h2 = qual[col].dropna()
        print(f"  {horizon}d: n={len(vals_h2)}  mean_event={vals_h2.mean():6.1f}%  "
              f"median_event={vals_h2.median():6.1f}%  "
              f"(baseline uptrend-only mean={dict((h, m) for h, _, _, m, _ in baseline_rows)[horizon]:6.1f}%)")
else:
    print("  Tidak ada event yang qualify -- H2 tidak bisa diuji dengan sample ini.")

# Leave-one-cycle-out check kalau n cukup
if len(qual) >= 3:
    print("\n-- Leave-one-cycle-out (exclude 1 cycle, cek median fwd_ret_90d) --")
    for cyc in qual['cycle'].unique():
        rest = qual[qual['cycle'] != cyc]
        if len(rest) == 0:
            continue
        print(f"  exclude {cyc}: n_sisa={len(rest)}  median_fwd90d={rest['fwd_ret_90d'].median():6.1f}%")

# Simpan CSV
ev_df.to_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\research\findings\_apparent_demand_h2_events.csv", index=False)

# =============================================================================
# H3 — REDUNDANSI vs realized_cap_usd growth & net_realized_pl_usd
# =============================================================================
print("\n" + "=" * 100)
print("H3 -- Redundansi: apparent_demand (smoothed) vs realized_cap_usd growth & net_realized_pl_usd")
print("=" * 100)

d3 = df.copy()
d3['realized_cap_chg_30d'] = d3['realized_cap_usd'].diff(30)
d3['realized_cap_pctchg_30d'] = d3['realized_cap_usd'].pct_change(30) * 100
d3['net_pl_ma30'] = d3['net_realized_pl_usd'].rolling(30, min_periods=30).mean()

pairs = [
    ('ad_ma30', 'realized_cap_chg_30d', 'ad_ma30 vs realized_cap 30d-change (USD)'),
    ('ad_ma30', 'realized_cap_pctchg_30d', 'ad_ma30 vs realized_cap 30d-%change'),
    ('ad_ma30', 'net_pl_ma30', 'ad_ma30 vs net_realized_pl_usd (MA30)'),
    ('ad_ma90', 'realized_cap_chg_30d', 'ad_ma90 vs realized_cap 30d-change (USD)'),
    ('ad_ma90', 'net_pl_ma30', 'ad_ma90 vs net_realized_pl_usd (MA30)'),
    ('apparent_demand', 'net_realized_pl_usd', 'raw apparent_demand vs raw net_realized_pl_usd'),
]

print("\nFull-history correlation (Pearson & Spearman), n hari valid dicantumkan per pair:")
for a, b, label in pairs:
    sub = d3[[a, b]].dropna()
    if len(sub) < 30:
        print(f"  {label}: n terlalu kecil ({len(sub)})")
        continue
    pear = sub[a].corr(sub[b], method='pearson')
    spear = sub[a].corr(sub[b], method='spearman')
    print(f"  {label:<55}  n={len(sub):>5}  pearson={pear:6.3f}  spearman={spear:6.3f}")

print("\nPer-cycle correlation ad_ma30 vs net_pl_ma30 (cek konsistensi lintas cycle):")
for name, _, _ in CYCLES:
    sub = d3[d3['cycle'] == name][['ad_ma30', 'net_pl_ma30']].dropna()
    if len(sub) < 30:
        continue
    pear = sub['ad_ma30'].corr(sub['net_pl_ma30'], method='pearson')
    print(f"  {name:<18} n={len(sub):>5}  pearson={pear:6.3f}")

print("\nPer-cycle correlation ad_ma30 vs realized_cap_chg_30d:")
for name, _, _ in CYCLES:
    sub = d3[d3['cycle'] == name][['ad_ma30', 'realized_cap_chg_30d']].dropna()
    if len(sub) < 30:
        continue
    pear = sub['ad_ma30'].corr(sub['realized_cap_chg_30d'], method='pearson')
    print(f"  {name:<18} n={len(sub):>5}  pearson={pear:6.3f}")

print("\n" + "=" * 100)
print("SELESAI")
print("=" * 100)
