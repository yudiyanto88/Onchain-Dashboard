"""
Verify Z3 definition for Bitcoin on-chain routing framework.
Qualified cycles: 2018-2019 and 2022-2023 (full Z1+Z2 traversal)

Z2 ends / Z3 starts: STH RP cross UP above RP
Z3 early: RP <= Price < AVIV Mean, STH RP between RP and AVIV Mean
Z3 late:  AVIV Mean <= Price < AVIV Upper, STH RP still < AVIV Mean
Z3 ends:  Price cross up AVIV Upper (valid/sustained >= N days)
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ── Load & merge ───────────────────────────────────────────────────────────────
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])
av = pd.read_csv('data_aviv.csv', parse_dates=['date'])

df = pl.merge(av[['date','price_at_aviv_mean','price_at_aviv_upper_0.5sd']], on='date', how='inner')
df = df.rename(columns={
    'btc_price':                    'price',
    'realized_price':               'rp',
    'sth_cost_basis':               'sth_rp',
    'lth_cost_basis':               'lth_rp',
    'price_at_aviv_mean':           'aviv_mean',
    'price_at_aviv_upper_0.5sd':    'aviv_upper',
})
df = df[['date','price','rp','sth_rp','lth_rp','aviv_mean','aviv_upper']].dropna()
df = df.sort_values('date').reset_index(drop=True)
df = df[(df['date'] >= '2016-01-01') & (df['date'] <= '2026-12-31')].reset_index(drop=True)

print("="*70)
print("Z3 DEFINITION VERIFICATION — Bitcoin On-Chain Routing Framework")
print("="*70)
print(f"Data: {df['date'].min().date()} → {df['date'].max().date()}, {len(df)} hari\n")

# ── Find Z2-end events (STH RP cross UP above RP) ─────────────────────────────
sth_above_rp = df['sth_rp'] > df['rp']
z2_cross_mask = sth_above_rp & ~sth_above_rp.shift(1, fill_value=False)

print("Z2-END EVENTS (STH RP cross up RP):")
print("-"*55)
for _, r in df[z2_cross_mask].iterrows():
    print(f"  {r['date'].date()}  Price=${r['price']:>8,.0f}  "
          f"STH RP=${r['sth_rp']:>8,.0f}  RP=${r['rp']:>8,.0f}  "
          f"LTH RP=${r['lth_rp']:>8,.0f}  "
          f"STH/RP={r['sth_rp']/r['rp']:.4f}")
print()

# ── Qualified cycles ───────────────────────────────────────────────────────────
qualified = [
    {
        'name':          '2019 CYCLE (2018-2019 bear → 2021 peak)',
        'z2_end_window': ('2019-01-01', '2019-12-31'),
        'z3_search_end': '2021-12-31',
    },
    {
        'name':          '2023 CYCLE (2022-2023 bear → 2025 peak)',
        'z2_end_window': ('2023-01-01', '2023-12-31'),
        'z3_search_end': '2025-12-31',
    },
]

SEP = "="*70

def get_first_z2_end(window_start, window_end):
    mask = (df['date'] >= window_start) & (df['date'] <= window_end) & z2_cross_mask
    rows = df[mask]
    return rows.iloc[0] if not rows.empty else None


def count_days_above_upper(sub_df, start_idx):
    """Count consecutive days price >= aviv_upper starting from start_idx."""
    count = 0
    for j in range(start_idx, len(sub_df)):
        if sub_df.iloc[j]['price'] >= sub_df.iloc[j]['aviv_upper']:
            count += 1
        else:
            break
    return count


for cycle in qualified:
    z2_row = get_first_z2_end(*cycle['z2_end_window'])
    if z2_row is None:
        print(f"SKIP {cycle['name']} — no Z2 end found")
        continue

    print(SEP)
    print(f"CYCLE: {cycle['name']}")
    print(f"Z2 ENDS: {z2_row['date'].date()}  "
          f"Price=${z2_row['price']:,.0f}  "
          f"STH RP=${z2_row['sth_rp']:,.0f}  "
          f"RP=${z2_row['rp']:,.0f}  "
          f"LTH RP=${z2_row['lth_rp']:,.0f}")
    print(SEP)

    # Data window from Z2 end to Z3 search limit
    sub = df[(df['date'] >= z2_row['date']) &
             (df['date'] <= cycle['z3_search_end'])].reset_index(drop=True)

    # ── 1. ENTRY Z3 EARLY ─────────────────────────────────────────────────────
    cond_early = (
        (sub['price'] >= sub['rp']) &
        (sub['price'] < sub['aviv_mean']) &
        (sub['sth_rp'] > sub['rp']) &
        (sub['sth_rp'] < sub['aviv_mean'])
    )

    z3_early_start = None
    z3_early_start_idx = None
    print("\n── 1. ENTRY Z3 EARLY ──────────────────────────────────────────────")
    for idx in sub.index:
        if cond_early[idx]:
            z3_early_start = sub.loc[idx]
            z3_early_start_idx = idx
            break

    if z3_early_start is not None:
        r = z3_early_start
        rp_ok  = r['rp'] < r['sth_rp'] < r['aviv_mean']
        print(f"  Tanggal : {r['date'].date()}")
        print(f"  Price   : ${r['price']:,.0f}")
        print(f"  RP      : ${r['rp']:,.0f}")
        print(f"  STH RP  : ${r['sth_rp']:,.0f}")
        print(f"  LTH RP  : ${r['lth_rp']:,.0f}")
        print(f"  AVIV Mean: ${r['aviv_mean']:,.0f}")
        print(f"  Konfirmasi RP < STH RP < AVIV Mean? {'✓ YA' if rp_ok else '✗ TIDAK'}")
    else:
        print("  TIDAK DITEMUKAN entry Z3 early setelah Z2 end")

    # ── 2. TRANSITION Z3 EARLY → Z3 LATE ─────────────────────────────────────
    z3_late_start = None
    z3_late_start_idx = None
    print("\n── 2. TRANSITION Z3 EARLY → Z3 LATE ──────────────────────────────")
    if z3_early_start is not None:
        sub_from_early = sub.loc[z3_early_start_idx:]
        price_ge_aviv = sub_from_early['price'] >= sub_from_early['aviv_mean']
        prev_below    = ~price_ge_aviv.shift(1, fill_value=True)
        cross_mask    = price_ge_aviv & prev_below

        crosses = sub_from_early[cross_mask]
        if not crosses.empty:
            r = crosses.iloc[0]
            z3_late_start = r
            z3_late_start_idx = crosses.index[0]

            days_early = (r['date'] - z3_early_start['date']).days
            gain_early = (r['price'] / z3_early_start['price'] - 1) * 100
            sth_lt_aviv = r['sth_rp'] < r['aviv_mean']

            print(f"  Tanggal : {r['date'].date()}")
            print(f"  Price   : ${r['price']:,.0f}")
            print(f"  AVIV Mean: ${r['aviv_mean']:,.0f}")
            print(f"  STH RP  : ${r['sth_rp']:,.0f}")
            print(f"  Konfirmasi STH RP < AVIV Mean? {'✓ YA' if sth_lt_aviv else '✗ TIDAK'}")
            print(f"  Durasi Z3 early : {days_early} hari")
            print(f"  Price gain Z3 early: {gain_early:+.1f}%")
        else:
            print("  Tidak ada price cross AVIV Mean ditemukan")

    # ── 3. Z3 LATE & SEMUA CROSS AVIV UPPER ──────────────────────────────────
    print("\n── 3. Z3 LATE — SEMUA CROSS UP AVIV UPPER ─────────────────────────")
    all_crosses = []
    if z3_late_start is not None:
        sub_late = sub.loc[z3_late_start_idx:].reset_index(drop=True)

        price_ge_upper = sub_late['price'] >= sub_late['aviv_upper']
        prev_below_u   = ~price_ge_upper.shift(1, fill_value=True)
        cross_up_mask  = price_ge_upper & prev_below_u

        for pos_idx in sub_late[cross_up_mask].index:
            r  = sub_late.loc[pos_idx]
            n  = count_days_above_upper(sub_late, pos_idx)
            gap = (r['sth_rp'] / r['aviv_mean'] - 1) * 100
            all_crosses.append({
                'date':       r['date'],
                'price':      r['price'],
                'sth_rp':     r['sth_rp'],
                'aviv_mean':  r['aviv_mean'],
                'aviv_upper': r['aviv_upper'],
                'days_above': n,
                'gap_pct':    gap,
            })

        print(f"\n  Total cross up AVIV Upper ditemukan: {len(all_crosses)}\n")
        hdr = f"  {'Tanggal':<12} {'Price':>9} {'STH RP':>9} {'AVIV Mean':>10} {'AVIV Upper':>11} {'Days>':>6} {'Gap STH/AM':>11}"
        print(hdr)
        print("  " + "-"*74)
        for c in all_crosses:
            gap_s = f"{c['gap_pct']:+.1f}%"
            print(f"  {str(c['date'].date()):<12} ${c['price']:>8,.0f} "
                  f"${c['sth_rp']:>8,.0f} ${c['aviv_mean']:>9,.0f} "
                  f"${c['aviv_upper']:>10,.0f} {c['days_above']:>6} {gap_s:>11}")

        print()
        print("  Test definisi 'valid cross':")
        print(f"  {'Threshold':<14} {'Valid Date':<14} {'False before':>13} {'Days above':>11} "
              f"{'Gap STH/AM':>11}")
        print("  " + "-"*66)
        for thr in [3, 5, 7]:
            valid_list   = [c for c in all_crosses if c['days_above'] >= thr]
            if valid_list:
                fv          = valid_list[0]
                false_cnt   = len([c for c in all_crosses if c['days_above'] < thr and c['date'] < fv['date']])
                gap_s       = f"{fv['gap_pct']:+.1f}%"
                print(f"  ≥{thr} hari       {str(fv['date'].date()):<14} {false_cnt:>13} "
                      f"{fv['days_above']:>11} {gap_s:>11}")
            else:
                print(f"  ≥{thr} hari       {'—':<14} {'N/A':>13} {'N/A':>11} {'N/A':>11}")
    else:
        print("  (Z3 late tidak ditemukan)")

    # ── 4. KONDISI STH RP SAAT Z3 BERAKHIR ────────────────────────────────────
    print("\n── 4. STH RP vs AVIV MEAN SAAT Z3 BERAKHIR ────────────────────────")
    for thr in [3, 5, 7]:
        valid_list = [c for c in all_crosses if c['days_above'] >= thr]
        if valid_list:
            c   = valid_list[0]
            gap = c['gap_pct']
            ok  = abs(gap) < 5
            print(f"  Threshold ≥{thr}d: "
                  f"STH RP=${c['sth_rp']:,.0f}  "
                  f"AVIV Mean=${c['aviv_mean']:,.0f}  "
                  f"Gap={gap:+.1f}%  "
                  f"STH RP ≈ AVIV Mean (<5%)? {'✓ YA' if ok else '✗ TIDAK'}")
        else:
            print(f"  Threshold ≥{thr}d: tidak ada valid cross")

    # ── 5. RINGKASAN TABEL ────────────────────────────────────────────────────
    print("\n── 5. RINGKASAN TABEL ──────────────────────────────────────────────")
    if z3_early_start is not None and z3_late_start is not None and all_crosses:
        days_early_base = (z3_late_start['date'] - z3_early_start['date']).days
        gain_early_base = (z3_late_start['price'] / z3_early_start['price'] - 1) * 100

        for thr in [3, 5, 7]:
            valid_list = [c for c in all_crosses if c['days_above'] >= thr]
            if not valid_list:
                print(f"\n  [Threshold ≥{thr}d] — tidak ada valid cross")
                continue
            fv         = valid_list[0]
            false_cnt  = len([c for c in all_crosses if c['days_above'] < thr and c['date'] < fv['date']])

            d_early = days_early_base
            d_late  = (fv['date'] - z3_late_start['date']).days
            d_total = d_early + d_late

            g_early = gain_early_base
            g_late  = (fv['price'] / z3_late_start['price'] - 1) * 100
            g_total = (fv['price'] / z3_early_start['price'] - 1) * 100

            gap     = fv['gap_pct']
            gap_ok  = abs(gap) < 5

            print(f"\n  ┌─ Threshold ≥{thr} hari {'─'*43}┐")
            print(f"  │ Z3 early start    {str(z3_early_start['date'].date()):<12}  "
                  f"Price={z3_early_start['price']:>9,.0f}            │")
            print(f"  │ Z3 late start     {str(z3_late_start['date'].date()):<12}  "
                  f"Price={z3_late_start['price']:>9,.0f}            │")
            print(f"  │ Z3 end (valid)    {str(fv['date'].date()):<12}  "
                  f"Price={fv['price']:>9,.0f}            │")
            print(f"  │ {'─'*58}│")
            print(f"  │ Durasi Z3 early   {d_early:>4} hari    "
                  f"Gain Z3 early  {g_early:>+8.1f}%           │")
            print(f"  │ Durasi Z3 late    {d_late:>4} hari    "
                  f"Gain Z3 late   {g_late:>+8.1f}%           │")
            print(f"  │ Durasi Z3 total   {d_total:>4} hari    "
                  f"Gain Z3 total  {g_total:>+8.1f}%           │")
            print(f"  │ {'─'*58}│")
            print(f"  │ False cross AVIV Upper sebelum valid: {false_cnt:<3}               │")
            print(f"  │ STH RP vs AVIV Mean gap: {gap:>+6.1f}%                              │")
            print(f"  │ STH RP ≈ AVIV Mean (<5%)? {'YA ✓' if gap_ok else 'TIDAK ✗':<6}                        │")
            print(f"  └{'─'*60}┘")
    print()

print(SEP)
print("SELESAI")
print(SEP)
