"""
K5 Dip-Entry Trigger — Fear & Greed Index sebagai sinyal tambahan
Test: Fear & Greed turun ke bawah 50 (alt: di bawah 45) sebagai dip-entry
signal untuk buy dip di Z2/Z3 (early bull recovery).

Z2/Z3 windows (given, sama dengan analisis K5 sebelumnya):
  Episode 1 (2019): 2019-05-07 -> 2019-07-08
  Episode 2 (2023-2024): 2023-03-01 -> 2024-02-27

Dibandingkan terhadap kondisi yang sudah divalidasi sebelumnya:
  STH Supply in Loss >= 50% DAN min(aSOPR, STH-SOPR) <= 0.98
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load ─────────────────────────────────────────────────────────────────────
fg = pd.read_csv('data_fg.csv', parse_dates=['date']).rename(columns={'Fear & Greed': 'fg'})
sp = pd.read_csv('data_supply.csv', parse_dates=['date'])
mo = pd.read_csv('data_momentum.csv', parse_dates=['date'])
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])

df = pl[['date', 'btc_price', 'lth_cost_basis']].merge(
    fg[['date', 'fg']], on='date', how='inner'
).merge(
    sp[['date', 'pct_sth_in_profit', 'pct_sth_in_loss']], on='date', how='inner'
).merge(
    mo[['date', 'asopr', 'sth_sopr']], on='date', how='inner'
)
df = df.rename(columns={'btc_price': 'price', 'lth_cost_basis': 'lth_rp'})
df['min_sopr'] = df[['asopr', 'sth_sopr']].min(axis=1)
df = df.dropna(subset=['price', 'fg', 'pct_sth_in_loss', 'min_sopr']).sort_values('date').reset_index(drop=True)

print("=" * 78)
print("LANGKAH 0 — CEK DATA")
print("=" * 78)
print("Kolom data_fg.csv:", list(pd.read_csv('data_fg.csv', nrows=0).columns))
print(f"Fear & Greed tersedia: {fg['date'].min().date()} s/d {fg['date'].max().date()}")

episodes_def = [
    ('EPISODE 1 (2019)', '2019-05-07', '2019-07-08'),
    ('EPISODE 2 (2023-2024)', '2023-03-01', '2024-02-27'),
]

episodes = []
for name, ws, we in episodes_def:
    ep_df = df[(df['date'] >= ws) & (df['date'] <= we)].reset_index(drop=True)
    episodes.append({'name': name, 'start': ws, 'end': we, 'df': ep_df})

# ── 1. F&G descriptive stats per episode ────────────────────────────────────
print("\n" + "=" * 78)
print("1. FEAR & GREED DESCRIPTIVE STATS PER EPISODE (Z2/Z3)")
print("=" * 78)
for ep in episodes:
    d = ep['df']
    if d.empty:
        print(f"\n{ep['name']}: TIDAK ADA DATA F&G di window {ep['start']} -> {ep['end']}")
        continue
    n = len(d)
    below50 = (d['fg'] < 50).sum()
    below45 = (d['fg'] < 45).sum()
    print(f"\n{ep['name']}  [{ep['start']} -> {ep['end']}]  ({n} hari)")
    print(f"  Mean F&G = {d['fg'].mean():.1f}  |  Min = {d['fg'].min():.0f}  |  Max = {d['fg'].max():.0f}")
    print(f"  Hari F&G < 50: {below50}/{n} ({below50/n*100:.1f}%)")
    print(f"  Hari F&G < 45: {below45}/{n} ({below45/n*100:.1f}%)")
    # simple daily print (compact, every 5th day + local extremes) to keep output readable
    print(f"  Sample harian (setiap 5 hari):")
    for i in range(0, n, 5):
        r = d.iloc[i]
        print(f"    {r['date'].date()}  price=${r['price']:,.0f}  F&G={r['fg']:.0f}")

# ── 2. Pullback detection (>=5% drop from running local high) ──────────────
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
                'peak_date': d.loc[peak_idx, 'date'], 'peak_price': d.loc[peak_idx, 'price'],
                'start_idx': i, 'end_idx': j - 1,
                'trough_idx': trough_pos, 'trough_date': d.loc[trough_pos, 'date'],
                'trough_price': d.loc[trough_pos, 'price'], 'drop_pct': d.loc[trough_pos, 'dd_pct'],
            })
            i = j
        else:
            i += 1
    return d, pullbacks

def gain_after(d, ref_idx, ref_price, days, global_df):
    ref_date = d.loc[ref_idx, 'date']
    target_date = ref_date + pd.Timedelta(days=days)
    fut = global_df[global_df['date'] >= target_date]
    if fut.empty:
        return None
    return (fut.iloc[0]['price'] / ref_price - 1) * 100

STH_LOSS_THR = 50.0   # STH in Loss >= 50%
SOPR_THR = 0.98        # min(aSOPR, STH-SOPR) <= 0.98

print("\n" + "=" * 78)
print("2-3. PULLBACK IDENTIFICATION + F&G / STH+SOPR ALIGNMENT CHECK")
print("=" * 78)

all_rows = []
for ep in episodes:
    d, pullbacks = find_pullbacks(ep['df'])
    print(f"\n{ep['name']}: {len(pullbacks)} pullback (>=5% drop) terdeteksi")

    for k, pb in enumerate(pullbacks, 1):
        seg = d.iloc[pb['start_idx']:pb['end_idx'] + 1]
        fg_min_idx = seg['fg'].idxmin()
        fg_min = d.loc[fg_min_idx, 'fg']
        fg_min_date = d.loc[fg_min_idx, 'date']
        fg_min_price = d.loc[fg_min_idx, 'price']
        below50 = (seg['fg'] < 50).any()
        below45 = (seg['fg'] < 45).any()

        # STH+SOPR condition anywhere within this pullback
        sth_loss_max = 100 - seg['pct_sth_in_profit'].min()
        sopr_min = seg['min_sopr'].min()
        sth_hit = seg['pct_sth_in_profit'] <= (100 - STH_LOSS_THR)
        sopr_hit_mask = seg['min_sopr'] <= SOPR_THR
        sth_sopr_confirmed = bool((sth_hit & sopr_hit_mask).any()) or bool(sth_hit.any() and sopr_hit_mask.any())
        # stricter: both conditions true on same day at some point
        combo_mask = (seg['pct_sth_in_profit'] <= (100 - STH_LOSS_THR)) & (seg['min_sopr'] <= SOPR_THR)
        combo_confirmed = bool(combo_mask.any())

        g7 = gain_after(d, fg_min_idx, fg_min_price, 7, df)
        g14 = gain_after(d, fg_min_idx, fg_min_price, 14, df)
        g30 = gain_after(d, fg_min_idx, fg_min_price, 30, df)

        print(f"\n  Pullback #{k}: peak {pb['peak_date'].date()} (${pb['peak_price']:,.0f}) -> "
              f"trough {pb['trough_date'].date()} (${pb['trough_price']:,.0f}), drop {pb['drop_pct']:.1f}%")
        print(f"    a. F&G < 50 selama pullback? {'YA' if below50 else 'TIDAK'}  |  "
              f"F&G < 45? {'YA' if below45 else 'TIDAK'}  (F&G terendah = {fg_min:.0f} pada {fg_min_date.date()})")
        print(f"    b. Harga saat F&G terendah: ${fg_min_price:,.0f}")
        g7s = f"{g7:+.1f}%" if g7 is not None else "N/A"
        g14s = f"{g14:+.1f}%" if g14 is not None else "N/A"
        g30s = f"{g30:+.1f}%" if g30 is not None else "N/A"
        print(f"    c. Gain sejak F&G-terendah: 7d={g7s}  14d={g14s}  30d={g30s}")
        print(f"    d. STH in Loss max selama pullback = {sth_loss_max:.1f}%  |  min(aSOPR,STH-SOPR) = {sopr_min:.4f}  "
              f"|  STH>=50%+SOPR<=0.98 align (same day)? {'YA' if combo_confirmed else 'TIDAK'}")

        all_rows.append({
            'episode': ep['name'], 'pullback': k,
            'trough_date': pb['trough_date'].date(), 'drop_pct': pb['drop_pct'],
            'fg_min_date': fg_min_date.date(), 'price_at_fg_min': fg_min_price,
            'fg_min': fg_min, 'below50': below50, 'below45': below45,
            'sth_loss_max': sth_loss_max, 'sopr_min': sopr_min,
            'sth_sopr_combo_align': combo_confirmed,
            'gain_7d': g7, 'gain_14d': g14, 'gain_30d': g30,
        })

# ── 4. False signal checks ──────────────────────────────────────────────────
print("\n" + "=" * 78)
print("4. FALSE SIGNAL CHECK")
print("=" * 78)

for ep in episodes:
    d = ep['df']
    print(f"\n{ep['name']}:")
    below50_mask = d['fg'] < 50
    if not below50_mask.any():
        print("  F&G tidak pernah < 50 di window ini.")
        continue

    # collapse consecutive below-50 days into runs
    idxs = d.index[below50_mask].to_list()
    runs = []
    run_start = idxs[0]
    prev = idxs[0]
    for ix in idxs[1:]:
        if ix == prev + 1:
            prev = ix
            continue
        runs.append((run_start, prev))
        run_start = ix
        prev = ix
    runs.append((run_start, prev))

    n_no_bounce = 0
    n_during_uptrend = 0
    for a, b in runs:
        run_start_price = d.loc[a, 'price']
        run_end_idx = b
        lookahead_end = min(b + 30, len(d) - 1)
        lookahead = d.iloc[b:lookahead_end + 1]
        min_price_after = lookahead['price'].min()
        further_drop = (min_price_after / d.loc[b, 'price'] - 1) * 100
        no_bounce = further_drop <= -10
        if no_bounce:
            n_no_bounce += 1

        # is this run occurring while price is trending up (5 days before run_start price also rising)?
        pre_idx = max(a - 5, 0)
        trending_up = d.loc[a, 'price'] > d.loc[pre_idx, 'price'] if a > 0 else False
        # check if it's inside a >=5% drawdown from recent local high at run start
        recent_peak = d['price'].iloc[max(0, a - 30):a + 1].max() if a > 0 else d.loc[a, 'price']
        in_drawdown = (d.loc[a, 'price'] / recent_peak - 1) * 100 <= -3
        if trending_up and not in_drawdown:
            n_during_uptrend += 1

        print(f"  Run: {d.loc[a,'date'].date()} -> {d.loc[b,'date'].date()}  "
              f"F&G low={d.loc[a:b,'fg'].min():.0f}  price ${d.loc[a,'price']:,.0f}->${d.loc[b,'price']:,.0f}  "
              f"further drop within 30d after={further_drop:+.1f}%  "
              f"{'[NO BOUNCE >10%]' if no_bounce else ''} {'[DURING UPTREND, bukan pullback]' if (trending_up and not in_drawdown) else ''}")

    print(f"  Total run F&G<50: {len(runs)}  |  Tanpa bounce (>10% further drop): {n_no_bounce}  |  "
          f"Terjadi saat uptrend (bukan pullback): {n_during_uptrend}")

# ── 5. Summary table ─────────────────────────────────────────────────────────
print("\n" + "=" * 78)
print("5. RINGKASAN TABEL PER PULLBACK")
print("=" * 78)
print(f"{'Episode':<24}{'Trough':<12}{'Price@FGmin':>12}{'F&G min':>9}{'STHLoss%':>10}{'SOPRmin':>9}{'Gain14d':>10}{'Gain30d':>10}{'Align?':>8}")
for r in all_rows:
    align = 'YA' if r['sth_sopr_combo_align'] else 'TIDAK'
    g14 = f"{r['gain_14d']:+.1f}%" if r['gain_14d'] is not None else "N/A"
    g30 = f"{r['gain_30d']:+.1f}%" if r['gain_30d'] is not None else "N/A"
    print(f"{r['episode']:<24}{str(r['trough_date']):<12}{'$'+format(r['price_at_fg_min'],',.0f'):>12}"
          f"{r['fg_min']:>9.0f}{r['sth_loss_max']:>9.1f}%{r['sopr_min']:>9.3f}{g14:>10}{g30:>10}{align:>8}")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
