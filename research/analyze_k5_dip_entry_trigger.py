"""
K5 Dip-Entry Trigger Validation
Validasi dua kondisi sebagai dip-entry trigger untuk deploy loan
di awal bull recovery (periode Z2 dan Z3).

Z2: STH RP cross ke atas RP (ordering normal restore), Price < AVIV Mean
Z3: RP <= Price < AVIV Upper (0.5 sigma), ordering normal

TRIGGER:    STH Supply in Loss >= X%  (<=> STH Supply in Profit <= 100-X%)
KONFIRMASI: min(aSOPR, STH-SOPR) <= Y

Episode: 2018-2019 recovery, 2022-2023 recovery
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

pd.set_option('display.width', 160)

# ── Load & merge ────────────────────────────────────────────────────────────
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
)

df = df.rename(columns={
    'btc_price': 'price',
    'realized_price': 'rp',
    'sth_cost_basis': 'sth_rp',
    'lth_cost_basis': 'lth_rp',
    'price_at_aviv_mean': 'aviv_mean',
})
df['aviv_upper'] = df['aviv_mean'] + 0.5 * (df['price_at_aviv_plus_1_sigma'] - df['aviv_mean'])
df['min_sopr'] = df[['asopr', 'sth_sopr']].min(axis=1)
df = df.dropna(subset=['price', 'rp', 'sth_rp', 'aviv_mean', 'aviv_upper',
                        'pct_sth_in_profit', 'asopr', 'sth_sopr'])
df = df.sort_values('date').reset_index(drop=True)

# ── Locate Z2 start / Z3 end per episode ────────────────────────────────────
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
            # check sustained >= 3 days
            if i + 3 <= n and above_upper.iloc[i:i + 3].all():
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
    if win is None:
        print(f"SKIP {name} — Z2 start tidak ditemukan")
        continue
    z2_start, z3_end = win
    ep_df = df[(df['date'] >= z2_start) & (df['date'] <= z3_end)].reset_index(drop=True)
    episodes.append({'name': name, 'z2_start': z2_start, 'z3_end': z3_end, 'df': ep_df})

print("=" * 78)
print("K5 DIP-ENTRY TRIGGER VALIDATION")
print("=" * 78)
for ep in episodes:
    print(f"\n{ep['name']}: Z2 start = {ep['z2_start'].date()}  |  Z3 end = {ep['z3_end'].date()}  "
          f"({len(ep['df'])} hari)")

# ── Pullback detection: >=5% drop from running local high ──────────────────
def find_pullbacks(ep_df, min_drop_pct=5.0):
    d = ep_df.copy().reset_index(drop=True)
    d['run_peak'] = d['price'].cummax()
    d['run_peak_idx'] = d['price'].expanding().apply(lambda x: x.values.argmax()).astype(int)
    d['dd_pct'] = (d['price'] / d['run_peak'] - 1) * 100
    in_pb = d['dd_pct'] <= -min_drop_pct

    pullbacks = []
    i = 0
    n = len(d)
    while i < n:
        if in_pb.iloc[i]:
            peak_idx = int(d.loc[i, 'run_peak_idx'])
            j = i
            while j < n and in_pb.iloc[j] and d.loc[j, 'run_peak_idx'] == peak_idx:
                j += 1
            trough_slice = d.iloc[i:j]
            trough_pos = trough_slice['price'].idxmin()
            pullbacks.append({
                'peak_idx': peak_idx,
                'peak_date': d.loc[peak_idx, 'date'],
                'peak_price': d.loc[peak_idx, 'price'],
                'start_idx': i,
                'start_date': d.loc[i, 'date'],
                'end_idx': j - 1,
                'trough_idx': trough_pos,
                'trough_date': d.loc[trough_pos, 'date'],
                'trough_price': d.loc[trough_pos, 'price'],
                'drop_pct': d.loc[trough_pos, 'dd_pct'],
            })
            i = j
        else:
            i += 1
    return d, pullbacks


# ── Evaluate one pullback against a given threshold combo ──────────────────
def evaluate_pullback(d, pb, sth_loss_thr, sopr_thr):
    """d: full episode df with derived cols. pb: pullback dict.
    sth_loss_thr: STH in Loss >= thr (%)  -> profit <= 100-thr
    sopr_thr: min(aSOPR, STH-SOPR) <= thr
    """
    profit_thr = 100 - sth_loss_thr
    seg = d.iloc[pb['start_idx']:pb['end_idx'] + 1]

    trig_mask = seg['pct_sth_in_profit'] <= profit_thr
    result = {'trigger_hit': False, 'confirm_hit': False}
    if not trig_mask.any():
        return result

    trig_idx = seg.index[trig_mask][0]
    result['trigger_hit'] = True
    result['trigger_date'] = d.loc[trig_idx, 'date']
    result['trigger_price'] = d.loc[trig_idx, 'price']
    result['trigger_sth_profit'] = d.loc[trig_idx, 'pct_sth_in_profit']
    # min STH-in-loss reached during pullback (for reporting)
    result['sth_loss_max'] = 100 - seg['pct_sth_in_profit'].min()

    # confirm: min_sopr <= sopr_thr on/after trigger date, still within pullback segment
    seg_after = d.iloc[trig_idx:pb['end_idx'] + 1]
    result['sopr_min'] = seg_after['min_sopr'].min() if len(seg_after) else np.nan
    conf_mask = seg_after['min_sopr'] <= sopr_thr
    if not conf_mask.any():
        return result

    conf_idx = seg_after.index[conf_mask][0]
    result['confirm_hit'] = True
    result['confirm_date'] = d.loc[conf_idx, 'date']
    result['entry_price'] = d.loc[conf_idx, 'price']
    result['entry_min_sopr'] = d.loc[conf_idx, 'min_sopr']
    result['entry_idx'] = conf_idx

    return result


def days_to_recover(d, entry_idx, entry_price, search_end_idx):
    # start the day AFTER entry — entry day trivially satisfies price >= entry_price
    seg = d.iloc[entry_idx + 1:search_end_idx + 1]
    hit = seg[seg['price'] >= entry_price]
    if hit.empty:
        return None
    rec_idx = hit.index[0]
    return (d.loc[rec_idx, 'date'] - d.loc[entry_idx, 'date']).days


def gain_after(d, entry_idx, entry_price, days, global_df):
    entry_date = d.loc[entry_idx, 'date']
    target_date = entry_date + pd.Timedelta(days=days)
    fut = global_df[global_df['date'] >= target_date]
    if fut.empty:
        return None
    price_then = fut.iloc[0]['price']
    return (price_then / entry_price - 1) * 100


# ── Base-case analysis (TRIGGER=50%, CONFIRM=0.98) ──────────────────────────
BASE_LOSS_THR = 50.0
BASE_SOPR_THR = 0.98

summary_rows = []

for ep in episodes:
    d, pullbacks = find_pullbacks(ep['df'])
    print("\n" + "=" * 78)
    print(f"EPISODE: {ep['name']}")
    print("=" * 78)
    print(f"Total pullback (>=5% drop dari local high) terdeteksi: {len(pullbacks)}")

    for k, pb in enumerate(pullbacks, 1):
        print(f"\n  Pullback #{k}: peak {pb['peak_date'].date()} (${pb['peak_price']:,.0f}) "
              f"-> trough {pb['trough_date'].date()} (${pb['trough_price']:,.0f}), "
              f"drop {pb['drop_pct']:.1f}%")

        res = evaluate_pullback(d, pb, BASE_LOSS_THR, BASE_SOPR_THR)

        if not res['trigger_hit']:
            print(f"    3a. STH in Profit tidak pernah <= {100-BASE_LOSS_THR:.0f}% selama pullback ini -> TRIGGER TIDAK FIRE")
            summary_rows.append({
                'episode': ep['name'], 'pullback': k,
                'peak_date': pb['peak_date'].date(), 'trough_date': pb['trough_date'].date(),
                'sth_loss_max': 100 - d.iloc[pb['start_idx']:pb['end_idx']+1]['pct_sth_in_profit'].min(),
                'sopr_min': np.nan, 'entry_price': np.nan,
                'gain_30d': np.nan, 'gain_60d': np.nan, 'gain_90d': np.nan,
                'outcome': 'NO TRIGGER',
            })
            continue

        print(f"    3a. STH in Profit turun <= {100-BASE_LOSS_THR:.0f}% pada {res['trigger_date'].date()}, "
              f"price=${res['trigger_price']:,.0f}, STH in Profit={res['trigger_sth_profit']:.1f}% "
              f"(STH in Loss max selama pullback: {res['sth_loss_max']:.1f}%)")

        if not res['confirm_hit']:
            print(f"    3b. min(aSOPR,STH-SOPR) tidak pernah <= {BASE_SOPR_THR} setelah trigger, "
                  f"selama pullback ini -> KONFIRMASI TIDAK FIRE")
            summary_rows.append({
                'episode': ep['name'], 'pullback': k,
                'peak_date': pb['peak_date'].date(), 'trough_date': pb['trough_date'].date(),
                'sth_loss_max': res['sth_loss_max'], 'sopr_min': np.nan, 'entry_price': np.nan,
                'gain_30d': np.nan, 'gain_60d': np.nan, 'gain_90d': np.nan,
                'outcome': 'TRIGGER ONLY (no confirm)',
            })
            continue

        print(f"    3b. min(aSOPR,STH-SOPR) <= {BASE_SOPR_THR} pada {res['confirm_date'].date()}, "
              f"nilai={res['entry_min_sopr']:.4f}  -> ENTRY di ${res['entry_price']:,.0f}")

        rec_days = days_to_recover(d, res['entry_idx'], res['entry_price'], pb['end_idx'] + 60)
        if rec_days is not None:
            print(f"    3c. Recover ke atas entry price dalam {rec_days} hari")
        else:
            print(f"    3c. Belum recover ke atas entry price dalam window yang tersedia")

        g30 = gain_after(d, res['entry_idx'], res['entry_price'], 30, df)
        g60 = gain_after(d, res['entry_idx'], res['entry_price'], 60, df)
        g90 = gain_after(d, res['entry_idx'], res['entry_price'], 90, df)
        g30s = f"{g30:+.1f}%" if g30 is not None else "N/A"
        g60s = f"{g60:+.1f}%" if g60 is not None else "N/A"
        g90s = f"{g90:+.1f}%" if g90 is not None else "N/A"
        print(f"    3d. Gain 30d={g30s}  60d={g60s}  90d={g90s}")

        # false-signal check 4a: after entry, price falls below LTH RP (regress to Z1)?
        lookahead = d.iloc[res['entry_idx']:min(res['entry_idx'] + 120, len(d))]
        regressed = (lookahead['price'] < lookahead['lth_rp']).any()
        outcome = 'CLEAN' if (g30 or 0) >= 0 else 'ENTRY THEN DRAWDOWN'
        if regressed:
            outcome = 'FALSE SIGNAL (regressed to Z1)'
        print(f"    4a. Regresi ke Z1 (price < LTH RP) dalam 120 hari setelah entry? "
              f"{'YA' if regressed else 'TIDAK'}")

        summary_rows.append({
            'episode': ep['name'], 'pullback': k,
            'peak_date': pb['peak_date'].date(), 'trough_date': pb['trough_date'].date(),
            'sth_loss_max': res['sth_loss_max'], 'sopr_min': res['entry_min_sopr'],
            'entry_price': res['entry_price'],
            'gain_30d': g30, 'gain_60d': g60, 'gain_90d': g90,
            'outcome': outcome,
        })

    # ── 4b. Confirm condition firing OUTSIDE any pullback (false context) ───
    print(f"\n  4b. min(aSOPR,STH-SOPR) <= {BASE_SOPR_THR} DI LUAR konteks pullback (harga sedang naik):")
    pullback_idx_set = set()
    for pb in pullbacks:
        pullback_idx_set.update(range(pb['start_idx'], pb['end_idx'] + 1))
    outside_confirm = d[(d['min_sopr'] <= BASE_SOPR_THR) & (~d.index.isin(pullback_idx_set))]
    if outside_confirm.empty:
        print("     Tidak ditemukan — semua kejadian SOPR <= threshold terjadi dalam konteks pullback.")
    else:
        # collapse consecutive dates into runs
        idxs = outside_confirm.index.to_list()
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
        for a, b in runs:
            print(f"     {d.loc[a,'date'].date()} → {d.loc[b,'date'].date()}  "
                  f"price ${d.loc[a,'price']:,.0f}→${d.loc[b,'price']:,.0f}  "
                  f"min_sopr low={d.loc[a:b,'min_sopr'].min():.4f}")

print("\n" + "=" * 78)
print("RINGKASAN TABEL (base case: STH in Loss >= 50%, SOPR konfirmasi <= 0.98)")
print("=" * 78)
srow = pd.DataFrame(summary_rows)
if not srow.empty:
    for _, r in srow.iterrows():
        ep_s = f"{r['episode']}"
        pd_s = f"{r['trough_date']}"
        sthl = f"{r['sth_loss_max']:.1f}%" if pd.notna(r['sth_loss_max']) else "N/A"
        sopr = f"{r['sopr_min']:.3f}" if pd.notna(r['sopr_min']) else "N/A"
        entry = f"${r['entry_price']:,.0f}" if pd.notna(r['entry_price']) else "N/A"
        g30 = f"{r['gain_30d']:+.1f}%" if pd.notna(r['gain_30d']) else "N/A"
        g60 = f"{r['gain_60d']:+.1f}%" if pd.notna(r['gain_60d']) else "N/A"
        print(f"  [{ep_s}] PB#{r['pullback']} pullback~{pd_s} | STHloss_max={sthl} | SOPRmin={sopr} | "
              f"entry={entry} | 30d={g30} | 60d={g60} | {r['outcome']}")

# ── Threshold sensitivity grid ───────────────────────────────────────────────
print("\n" + "=" * 78)
print("SENSITIVITY GRID — STH in Loss [40,50,60] x SOPR confirm [0.95,0.98,1.00]")
print("=" * 78)

grid_results = []
for ep in episodes:
    d, pullbacks = find_pullbacks(ep['df'])
    for loss_thr in [40.0, 50.0, 60.0]:
        for sopr_thr in [0.95, 0.98, 1.00]:
            n_trigger = 0
            n_confirm = 0
            n_clean = 0
            n_false_regress = 0
            gains30 = []
            for pb in pullbacks:
                res = evaluate_pullback(d, pb, loss_thr, sopr_thr)
                if res['trigger_hit']:
                    n_trigger += 1
                if res.get('confirm_hit'):
                    n_confirm += 1
                    g30 = gain_after(d, res['entry_idx'], res['entry_price'], 30, df)
                    if g30 is not None:
                        gains30.append(g30)
                    lookahead = d.iloc[res['entry_idx']:min(res['entry_idx'] + 120, len(d))]
                    if (lookahead['price'] < lookahead['lth_rp']).any():
                        n_false_regress += 1
                    else:
                        n_clean += 1
            avg_g30 = np.mean(gains30) if gains30 else np.nan
            grid_results.append({
                'episode': ep['name'], 'loss_thr': loss_thr, 'sopr_thr': sopr_thr,
                'n_pullback': len(pullbacks), 'n_trigger': n_trigger, 'n_confirm': n_confirm,
                'n_clean': n_clean, 'n_false_regress': n_false_regress, 'avg_gain_30d': avg_g30,
            })

grid_df = pd.DataFrame(grid_results)
for ep in episodes:
    print(f"\n  {ep['name']}:")
    sub = grid_df[grid_df['episode'] == ep['name']]
    print(f"  {'LossThr':>8} {'SOPRThr':>8} {'#Trig':>6} {'#Conf':>6} {'#Clean':>7} {'#FalseRegress':>14} {'AvgGain30d':>11}")
    for _, r in sub.iterrows():
        ag = f"{r['avg_gain_30d']:+.1f}%" if pd.notna(r['avg_gain_30d']) else "N/A"
        print(f"  {r['loss_thr']:>7.0f}% {r['sopr_thr']:>8.2f} {r['n_trigger']:>6} {r['n_confirm']:>6} "
              f"{r['n_clean']:>7} {r['n_false_regress']:>14} {ag:>11}")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
