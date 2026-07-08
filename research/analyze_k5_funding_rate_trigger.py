"""
K5 Funding Rate as Additional Confirmation — Dip-Entry Validation
Validasi Funding Rate sebagai tambahan konfirmasi dip-entry di K5
(deploy loan saat pullback di Z2/Z3).

Z2: STH RP cross ke atas RP, Price < AVIV Mean
Z3: RP <= Price < AVIV Upper (0.5 sigma), ordering normal
(sama dengan analisis K5 sebelumnya — analyze_k5_dip_entry_trigger.py)

FR drop tajam = funding_rate <= -0.01 (unit sesuai kolom mentah di data_derivatives.csv)
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

SEP = "=" * 78

# ── LANGKAH 0: cek ketersediaan kolom funding rate ──────────────────────────
print(SEP)
print("LANGKAH 0 — CEK KOLOM DATA")
print(SEP)

deriv = pd.read_csv('data_derivatives.csv', parse_dates=['date'])
print(f"\ndata_derivatives.csv kolom: {list(deriv.columns)}")
print(f"Ditemukan kolom funding rate: 'funding_rate' -> LANJUT ANALISIS\n")

print(f"Range data funding_rate : {deriv['date'].min().date()} -> {deriv['date'].max().date()}")
nn = deriv[deriv['funding_rate'].notna()]
print(f"First non-null funding_rate  : {nn['date'].min().date()}")
print(f"Total baris dengan FR non-null: {len(nn)} dari {len(deriv)}")

# ── Load & merge semua data ──────────────────────────────────────────────────
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])
av = pd.read_csv('data_aviv.csv', parse_dates=['date'])
sp = pd.read_csv('data_supply.csv', parse_dates=['date'])
mo = pd.read_csv('data_momentum.csv', parse_dates=['date'])

df = pl[['date', 'btc_price', 'realized_price', 'sth_cost_basis', 'lth_cost_basis']].merge(
    av[['date', 'price_at_aviv_mean', 'price_at_aviv_plus_1_sigma']], on='date', how='inner'
).merge(
    sp[['date', 'pct_sth_in_profit', 'pct_sth_in_loss']], on='date', how='inner'
).merge(
    mo[['date', 'asopr', 'sth_sopr']], on='date', how='inner'
).merge(
    deriv[['date', 'funding_rate']], on='date', how='left'
)

df = df.rename(columns={
    'btc_price': 'price', 'realized_price': 'rp', 'sth_cost_basis': 'sth_rp',
    'lth_cost_basis': 'lth_rp', 'price_at_aviv_mean': 'aviv_mean',
})
df['aviv_upper'] = df['aviv_mean'] + 0.5 * (df['price_at_aviv_plus_1_sigma'] - df['aviv_mean'])
df['min_sopr'] = df[['asopr', 'sth_sopr']].min(axis=1)
df = df.dropna(subset=['price', 'rp', 'sth_rp', 'aviv_mean', 'aviv_upper',
                        'pct_sth_in_profit', 'asopr', 'sth_sopr'])
df = df.sort_values('date').reset_index(drop=True)

# ── Z2/Z3 window per episode (identik dengan analyze_k5_dip_entry_trigger.py) ─
sth_above_rp = df['sth_rp'] > df['rp']
z2_cross_mask = sth_above_rp & ~sth_above_rp.shift(1, fill_value=False)


def find_episode_window(search_start, search_end, z3_search_end):
    win = df[(df['date'] >= search_start) & (df['date'] <= search_end)]
    cross = win[z2_cross_mask.loc[win.index]]
    if cross.empty:
        return None
    z2_start_date = df.loc[cross.index[0], 'date']
    sub = df[(df['date'] >= z2_start_date) & (df['date'] <= z3_search_end)].reset_index(drop=True)
    above_upper = sub['price'] >= sub['aviv_upper']
    z3_end_idx = None
    n = len(sub)
    for i in range(n):
        if above_upper.iloc[i] and i + 3 <= n and above_upper.iloc[i:i + 3].all():
            z3_end_idx = i
            break
    z3_end_date = sub.loc[z3_end_idx, 'date'] if z3_end_idx is not None else sub['date'].iloc[-1]
    return z2_start_date, z3_end_date


episodes_meta = [
    ('2018-2019 RECOVERY', '2019-01-01', '2019-12-31', '2021-12-31'),
    ('2022-2023 RECOVERY', '2023-01-01', '2023-12-31', '2025-12-31'),
]

episodes = []
for name, ws, we, z3end in episodes_meta:
    win = find_episode_window(ws, we, z3end)
    z2_start, z3_end = win
    ep_df = df[(df['date'] >= z2_start) & (df['date'] <= z3_end)].reset_index(drop=True)
    fr_available = ep_df['funding_rate'].notna().sum() > 0
    episodes.append({'name': name, 'z2_start': z2_start, 'z3_end': z3_end,
                      'df': ep_df, 'fr_available': fr_available})

print(f"\n{SEP}\nZ2/Z3 WINDOW PER EPISODE\n{SEP}")
for ep in episodes:
    n_fr = ep['df']['funding_rate'].notna().sum()
    print(f"\n{ep['name']}: Z2 start={ep['z2_start'].date()}  Z3 end={ep['z3_end'].date()}  "
          f"({len(ep['df'])} hari) | FR data tersedia: {n_fr}/{len(ep['df'])} hari "
          f"{'-> ADA' if ep['fr_available'] else '-> TIDAK ADA SAMA SEKALI'}")

# ── STEP 1: FR summary stats per episode ────────────────────────────────────
print(f"\n{SEP}\nSTEP 1 — FUNDING RATE SUMMARY PER EPISODE (harian, Z2+Z3)\n{SEP}")
for ep in episodes:
    d = ep['df']
    fr = d['funding_rate'].dropna()
    print(f"\n{ep['name']}:")
    if fr.empty:
        print("  TIDAK ADA DATA FUNDING RATE dalam window ini -> analisis FR untuk episode ini DIHENTIKAN, dilaporkan sbg data tidak tersedia.")
        continue
    n_neg = (fr < 0).sum()
    print(f"  N hari (FR non-null) : {len(fr)}")
    print(f"  Mean                 : {fr.mean():.5f}")
    print(f"  Min                  : {fr.min():.5f}  (pada {d.loc[d['funding_rate'].idxmin(),'date'].date()})")
    print(f"  Max                  : {fr.max():.5f}")
    print(f"  Hari FR negatif      : {n_neg} ({n_neg/len(fr)*100:.1f}%)")
    print(f"  Hari FR <= -0.01     : {(fr <= -0.01).sum()} ({(fr <= -0.01).sum()/len(fr)*100:.1f}%)")
    print(f"  Percentile 10 / 25   : {fr.quantile(0.10):.5f} / {fr.quantile(0.25):.5f}")

# ── Pullback detection (identik dgn skrip sebelumnya) ───────────────────────
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
                'trough_date': d.loc[trough_pos, 'date'], 'trough_price': d.loc[trough_pos, 'price'],
                'drop_pct': d.loc[trough_pos, 'dd_pct'],
            })
            i = j
        else:
            i += 1
    return d, pullbacks


FR_THR = -0.01


def gain_after(d, ref_idx, ref_price, days, global_df):
    ref_date = d.loc[ref_idx, 'date']
    target_date = ref_date + pd.Timedelta(days=days)
    fut = global_df[global_df['date'] >= target_date]
    if fut.empty:
        return None
    return (fut.iloc[0]['price'] / ref_price - 1) * 100


def evaluate_sth_sopr(d, pb, sth_loss_thr=50.0, sopr_thr=0.98):
    profit_thr = 100 - sth_loss_thr
    seg = d.iloc[pb['start_idx']:pb['end_idx'] + 1]
    trig_mask = seg['pct_sth_in_profit'] <= profit_thr
    res = {'trigger_hit': False, 'confirm_hit': False}
    if not trig_mask.any():
        return res
    trig_idx = seg.index[trig_mask][0]
    res['trigger_hit'] = True
    seg_after = d.iloc[trig_idx:pb['end_idx'] + 1]
    conf_mask = seg_after['min_sopr'] <= sopr_thr
    if not conf_mask.any():
        return res
    conf_idx = seg_after.index[conf_mask][0]
    res['confirm_hit'] = True
    res['confirm_idx'] = conf_idx
    res['confirm_date'] = d.loc[conf_idx, 'date']
    res['entry_price'] = d.loc[conf_idx, 'price']
    return res


# ── STEP 2 & 3: per-pullback FR analysis ────────────────────────────────────
print(f"\n{SEP}\nSTEP 2 & 3 — PULLBACK ANALYSIS (>=5% drop) + FR PER PULLBACK\n{SEP}")

summary_rows = []
false_no_bounce = 0
false_outside_pullback_count = {}

for ep in episodes:
    d, pullbacks = find_pullbacks(ep['df'])
    print(f"\n{ep['name']}: {len(pullbacks)} pullback terdeteksi")

    if not ep['fr_available']:
        print("  -> FR TIDAK TERSEDIA untuk episode ini. Analisis FR dihentikan, dilaporkan sbg data tidak tersedia.")
        for k, pb in enumerate(pullbacks, 1):
            summary_rows.append({
                'episode': ep['name'], 'pullback': k, 'trough_date': pb['trough_date'].date(),
                'price': pb['trough_price'], 'fr_min': None, 'sth_loss': None, 'sopr_min': None,
                'gain_14d': None, 'gain_30d': None, 'fr_helps': 'N/A (no FR data)',
            })
        continue

    for k, pb in enumerate(pullbacks, 1):
        seg = d.iloc[pb['start_idx']:pb['end_idx'] + 1]
        fr_seg = seg['funding_rate'].dropna()
        print(f"\n  Pullback #{k}: peak {pb['peak_date'].date()} (${pb['peak_price']:,.0f}) -> "
              f"trough {pb['trough_date'].date()} (${pb['trough_price']:,.0f}), drop {pb['drop_pct']:.1f}%")

        if fr_seg.empty:
            print("    Tidak ada data FR dalam window pullback ini.")
            continue

        fr_min = fr_seg.min()
        fr_min_idx = seg['funding_rate'].idxmin()
        fr_min_date = d.loc[fr_min_idx, 'date']
        fr_min_price = d.loc[fr_min_idx, 'price']
        sharp_drop = fr_min <= FR_THR

        print(f"    3a. FR turun tajam (<= {FR_THR})? {'YA' if sharp_drop else 'TIDAK'} "
              f"(FR min = {fr_min:.5f})")

        if sharp_drop:
            neg_run = (seg['funding_rate'] < 0)
            print(f"    3b. Hari FR negatif dalam pullback ini: {neg_run.sum()} dari {len(seg)} hari")
            print(f"    3c. FR minimum: {fr_min:.5f} pada {fr_min_date.date()}")
            print(f"    3d. Price di titik FR paling negatif: ${fr_min_price:,.0f}")

            g7 = gain_after(d, fr_min_idx, fr_min_price, 7, df)
            g14 = gain_after(d, fr_min_idx, fr_min_price, 14, df)
            g30 = gain_after(d, fr_min_idx, fr_min_price, 30, df)
            g7s = f"{g7:+.1f}%" if g7 is not None else "N/A"
            g14s = f"{g14:+.1f}%" if g14 is not None else "N/A"
            g30s = f"{g30:+.1f}%" if g30 is not None else "N/A"
            print(f"    3e. Gain 7d={g7s}  14d={g14s}  30d={g30s}")

            # false signal: FR sharp drop tapi harga terus turun >10% lebih lanjut
            lookahead = df[(df['date'] > fr_min_date) & (df['date'] <= fr_min_date + pd.Timedelta(days=30))]
            further_drop = None
            if not lookahead.empty:
                further_drop = (lookahead['price'].min() / fr_min_price - 1) * 100
            no_bounce = further_drop is not None and further_drop <= -10
            if no_bounce:
                false_no_bounce += 1
            print(f"    Harga turun lebih lanjut >=10% setelah FR min (30d)? "
                  f"{'YA (' + f'{further_drop:.1f}%' + ')' if no_bounce else 'TIDAK'}")

            sth_sopr_res = evaluate_sth_sopr(d, pb)
            sth_loss_val = 100 - seg['pct_sth_in_profit'].min()
            sopr_min_val = seg['min_sopr'].min()

            summary_rows.append({
                'episode': ep['name'], 'pullback': k, 'trough_date': fr_min_date.date(),
                'price': fr_min_price, 'fr_min': fr_min, 'sth_loss': sth_loss_val,
                'sopr_min': sopr_min_val, 'gain_14d': g14, 'gain_30d': g30,
                'fr_helps': None,  # filled in scenario comparison step
                'sth_sopr_confirm': sth_sopr_res.get('confirm_hit', False),
            })
        else:
            print("    -> FR tidak menyentuh threshold di pullback ini, dilewati dari tabel ringkasan FR.")

    # ── STEP 5b: FR sharp drop OUTSIDE pullback context (price naik) ────────
    if ep['fr_available']:
        pullback_idx_set = set()
        for pb in pullbacks:
            pullback_idx_set.update(range(pb['start_idx'], pb['end_idx'] + 1))
        outside = d[(d['funding_rate'] <= FR_THR) & (~d.index.isin(pullback_idx_set))]
        print(f"\n  STEP 5b. FR <= {FR_THR} DI LUAR konteks pullback (harga tidak sedang -5%+ dari local high):")
        if outside.empty:
            print("     Tidak ditemukan.")
            false_outside_pullback_count[ep['name']] = 0
        else:
            idxs = outside.index.to_list()
            runs, run_start, prev = [], idxs[0], idxs[0]
            for ix in idxs[1:]:
                if ix == prev + 1:
                    prev = ix
                    continue
                runs.append((run_start, prev))
                run_start, prev = ix, ix
            runs.append((run_start, prev))
            false_outside_pullback_count[ep['name']] = len(runs)
            for a, b in runs:
                print(f"     {d.loc[a,'date'].date()} -> {d.loc[b,'date'].date()}  "
                      f"price ${d.loc[a,'price']:,.0f}->${d.loc[b,'price']:,.0f}  "
                      f"FR low={d.loc[a:b,'funding_rate'].min():.5f}")

# ── STEP 4: Scenario comparison (STH+SOPR alone vs +FR) — 2023 only ─────────
print(f"\n{SEP}\nSTEP 4 — SCENARIO COMPARISON (STH>=50%+SOPR<=0.98)  vs  (+ FR<={FR_THR})\n{SEP}")

for ep in episodes:
    if not ep['fr_available']:
        print(f"\n{ep['name']}: FR tidak tersedia -> perbandingan skenario tidak bisa dilakukan untuk episode ini.")
        continue
    d, pullbacks = find_pullbacks(ep['df'])
    print(f"\n{ep['name']}:")
    n_a, n_b = 0, 0
    for k, pb in enumerate(pullbacks, 1):
        res = evaluate_sth_sopr(d, pb)
        if res.get('confirm_hit'):
            n_a += 1
            conf_idx = res['confirm_idx']
            # cek FR dalam window +-5 hari dari tanggal konfirmasi, dalam pullback yg sama
            win_start = max(pb['start_idx'], conf_idx - 5)
            win_end = min(pb['end_idx'], conf_idx + 5)
            fr_win = d.loc[win_start:win_end, 'funding_rate'].dropna()
            fr_confirms = (fr_win <= FR_THR).any() if not fr_win.empty else False
            if fr_confirms:
                n_b += 1
            print(f"  Pullback #{k}: STH+SOPR confirm di {res['confirm_date'].date()} "
                  f"(${res['entry_price']:,.0f}) | FR <= {FR_THR} dalam +-5 hari? "
                  f"{'YA' if fr_confirms else 'TIDAK'}")
            # update summary_rows fr_helps flag
            for row in summary_rows:
                if row['episode'] == ep['name'] and row['pullback'] == k:
                    row['fr_helps'] = 'YA' if fr_confirms else 'TIDAK'
    print(f"\n  Skenario A (STH+SOPR saja)      : {n_a} sinyal fire")
    print(f"  Skenario B (STH+SOPR + FR confirm): {n_b} sinyal fire")
    if n_a > 0:
        print(f"  -> Menambahkan FR {'MENGURANGI' if n_b < n_a else 'TIDAK mengurangi'} jumlah sinyal "
              f"({n_a} -> {n_b})")

# ── STEP 6: catatan khusus 2019 ──────────────────────────────────────────────
print(f"\n{SEP}\nSTEP 6 — CATATAN KHUSUS 2019 vs 2023\n{SEP}")
ep19 = episodes[0]
ep23 = episodes[1]
n19 = ep19['df']['funding_rate'].notna().sum()
n23 = ep23['df']['funding_rate'].notna().sum()
print(f"\n2018-2019 episode: {n19} hari dengan data FR dari total {len(ep19['df'])} hari window.")
print(f"2022-2023 episode: {n23} hari dengan data FR dari total {len(ep23['df'])} hari window.")
if n19 == 0:
    print("\n-> 2019: BUKAN soal magnitude kecil/noise — metric funding_rate di data_derivatives.csv")
    print(f"   secara historis baru mulai tercatat {nn['date'].min().date()}, jauh setelah window Z2/Z3 2019")
    print("   (Mei-Jul 2019) selesai. Tidak ada dasar numerik apapun untuk menilai FR di cycle 2019.")

# ── STEP 7: Ringkasan tabel ──────────────────────────────────────────────────
print(f"\n{SEP}\nSTEP 7 — RINGKASAN TABEL PER PULLBACK\n{SEP}")
for row in summary_rows:
    price_s = f"${row['price']:,.0f}" if row['price'] is not None else "N/A"
    fr_s = f"{row['fr_min']:.5f}" if row.get('fr_min') is not None else "N/A"
    sth_s = f"{row['sth_loss']:.1f}%" if row.get('sth_loss') is not None else "N/A"
    sopr_s = f"{row['sopr_min']:.3f}" if row.get('sopr_min') is not None else "N/A"
    g14_s = f"{row['gain_14d']:+.1f}%" if row.get('gain_14d') is not None else "N/A"
    g30_s = f"{row['gain_30d']:+.1f}%" if row.get('gain_30d') is not None else "N/A"
    fr_helps_s = row.get('fr_helps', 'N/A')
    print(f"  [{row['episode']}] PB#{row['pullback']} {row['trough_date']} | price={price_s} | "
          f"FRmin={fr_s} | STHloss={sth_s} | SOPRmin={sopr_s} | 14d={g14_s} | 30d={g30_s} | "
          f"FR membantu? {fr_helps_s}")

print(f"\n{SEP}\nFALSE SIGNAL SUMMARY\n{SEP}")
print(f"FR sharp-drop tapi harga tidak bounce (turun >=10% lanjut dalam 30d): {false_no_bounce}")
for name, cnt in false_outside_pullback_count.items():
    print(f"FR sharp-drop di luar konteks pullback [{name}]: {cnt} kejadian")

print(f"\n{SEP}\nSELESAI\n{SEP}")
