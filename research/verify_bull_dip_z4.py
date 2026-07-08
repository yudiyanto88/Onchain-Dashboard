"""
Verify bull dip characteristics in Z4 territory.

AVIV Mean  = active_realized_price
AVIV Upper = active_realized_price * 1.25  (Z4 boundary)
Z4         = price >= AVIV Upper
Dip zone   = STH RP <= price < AVIV Mean

Episode:
  - Price was in Z4 within last 60 days before the dip
  - Price drops below AVIV Mean (episode start)
  - Ends: (a) recovers above AVIV Mean -> BULL DIP
           (b) drops below STH RP      -> DEEPER
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')

# ── Load ───────────────────────────────────────────────────────────────────────
ev = pd.read_csv(r'D:\Claude Code\Projects\Onchain-Dashboard\data_price_level_events.csv',
                 parse_dates=['date'])
ev = ev.rename(columns={'btc_price': 'price', 'sth_cost_basis': 'sth_rp',
                         'active_realized_price': 'aviv_mean'})
ev['aviv_upper'] = ev['aviv_mean'] * 1.25
keep = ['date','price','sth_rp','aviv_mean','aviv_upper','event']
ev   = ev[keep].dropna(subset=['price','sth_rp','aviv_mean'])
ev   = ev[ev['date'] >= '2016-01-01'].sort_values('date').reset_index(drop=True)

# ── Numpy arrays for speed ────────────────────────────────────────────────────
price    = ev['price'].to_numpy()
sth_rp   = ev['sth_rp'].to_numpy()
aviv_m   = ev['aviv_mean'].to_numpy()
aviv_u   = ev['aviv_upper'].to_numpy()
dates    = ev['date'].to_numpy()
events   = ev['event'].to_numpy(dtype=object)
n        = len(ev)

in_z4       = price >= aviv_u
below_mean  = price <  aviv_m
below_sth   = price <  sth_rp

# Rolling "was in Z4 within last 60 days" using max in window
was_z4_60d = pd.Series(in_z4).rolling(60, min_periods=1).max().astype(bool).to_numpy()

print("="*72)
print("BULL DIP VERIFICATION - Z4 Territory (2016-2026)")
print("="*72)
print(f"Data: {pd.Timestamp(dates[0]).date()} -> {pd.Timestamp(dates[-1]).date()}, {n} hari\n")
print(f"AVIV Mean  = active_realized_price")
print(f"AVIV Upper = active_realized_price x 1.25\n")

# ── Episode detection (numpy loop) ────────────────────────────────────────────
episodes = []
i = 1  # start at 1 to check prev day

while i < n:
    # Episode start: price drops below AVIV Mean AND was above yesterday
    if below_mean[i] and not below_mean[i-1]:
        # Must have been in Z4 within last 60 days (window ends BEFORE today)
        lookback = max(0, i - 60)
        was_z4 = in_z4[lookback:i].any()

        if was_z4:
            ep_start_idx  = i
            ep_start_date = pd.Timestamp(dates[i])
            ep_start_px   = price[i]
            ep_low        = price[i]
            ep_low_idx    = i
            outcome       = 'OPEN'
            ep_end_idx    = n - 1

            j = i
            while j < n:
                px = price[j]
                if px >= aviv_m[j]:
                    outcome    = 'BULL DIP'
                    ep_end_idx = j
                    break
                elif px < sth_rp[j]:
                    outcome    = 'DEEPER'
                    ep_end_idx = j
                    break
                if px < ep_low:
                    ep_low     = px
                    ep_low_idx = j
                j += 1

            ep_end_date = pd.Timestamp(dates[ep_end_idx])
            duration    = (ep_end_date - ep_start_date).days

            # Check ground truth labels in this window
            ep_ev_labels = [str(e) for e in events[ep_start_idx:ep_end_idx+1] if e is not None and str(e) != 'nan']
            gt_bull_dip  = any('Bull Dip' in lb or 'bull dip' in lb.lower() for lb in ep_ev_labels)
            uniq_labels  = list(dict.fromkeys(ep_ev_labels))  # unique, order-preserving

            # Days to re-enter Z4 after episode ends (only BULL DIP)
            days_to_z4 = None
            if outcome == 'BULL DIP':
                for k in range(ep_end_idx + 1, n):
                    if in_z4[k]:
                        days_to_z4 = (pd.Timestamp(dates[k]) - ep_end_date).days
                        break

            episodes.append({
                'start_date':    ep_start_date,
                'end_date':      ep_end_date,
                'duration':      duration,
                'low_price':     ep_low,
                'low_date':      pd.Timestamp(dates[ep_low_idx]),
                'start_price':   ep_start_px,
                'end_price':     price[ep_end_idx],
                'outcome':       outcome,
                'days_to_z4':   days_to_z4,
                'gt_labels':    uniq_labels[:3],
                'gt_bull_dip':  gt_bull_dip,
            })

            i = ep_end_idx + 1
        else:
            i += 1
    else:
        i += 1

# ── Cycle assignment ──────────────────────────────────────────────────────────
def assign_cycle(d):
    if   d < pd.Timestamp('2018-01-01'): return '2017'
    elif d < pd.Timestamp('2020-01-01'): return '2019_mini'
    elif d < pd.Timestamp('2022-07-01'): return '2020-2021'
    elif d < pd.Timestamp('2024-01-01'): return '2022-2023'
    else:                                 return '2024-2025'

for ep in episodes: ep['cycle'] = assign_cycle(ep['start_date'])

# ── Per-cycle output ──────────────────────────────────────────────────────────
cycle_order = ['2017','2019_mini','2020-2021','2022-2023','2024-2025']

for cycle in cycle_order:
    eps = [e for e in episodes if e['cycle'] == cycle]
    if not eps: continue

    bull_dips = [e for e in eps if e['outcome'] == 'BULL DIP']
    deeperr   = [e for e in eps if e['outcome'] == 'DEEPER']
    openep    = [e for e in eps if e['outcome'] == 'OPEN']

    print(f"\n{'='*72}")
    print(f"CYCLE: {cycle}  |  Episodes: {len(eps)}  (BD={len(bull_dips)}, DEEPER={len(deeperr)}, OPEN={len(openep)})")
    print(f"{'='*72}")
    print(f"  {'Start':<12} {'End':<12} {'Days':>5} {'Low $':>10} {'Outcome':<10} {'GT':>4} {'->Z4':>6}")
    print(f"  {'-'*60}")
    for ep in eps:
        gt  = 'BD' if ep['gt_bull_dip'] else ('GT' if ep['gt_labels'] else '--')
        z4s = f"{ep['days_to_z4']}d" if ep['days_to_z4'] is not None else '--'
        print(f"  {str(ep['start_date'].date()):<12} "
              f"{str(ep['end_date'].date()):<12} "
              f"{ep['duration']:>5} "
              f"${ep['low_price']:>9,.0f} "
              f"{ep['outcome']:<10} "
              f"{gt:>4} "
              f"{z4s:>6}")
        if ep['gt_labels']:
            lbl = ', '.join(ep['gt_labels'])
            print(f"    {'':12} {'GT labels: ' + lbl}")

# ── Global stats ──────────────────────────────────────────────────────────────
all_bd = [e for e in episodes if e['outcome'] == 'BULL DIP']
all_dp = [e for e in episodes if e['outcome'] == 'DEEPER']
all_op = [e for e in episodes if e['outcome'] == 'OPEN']

print(f"\n\n{'='*72}")
print(f"GLOBAL SUMMARY")
print(f"{'='*72}")
print(f"  BULL DIP : {len(all_bd)}")
print(f"  DEEPER   : {len(all_dp)}")
print(f"  OPEN     : {len(all_op)}")

if all_bd:
    bd_dur = sorted([e['duration'] for e in all_bd])
    print(f"\n  BULL DIP duration (days): {bd_dur}")
    print(f"  Min={bd_dur[0]}  Max={bd_dur[-1]}  Median={bd_dur[len(bd_dur)//2]}")

if all_dp:
    dp_dur = sorted([e['duration'] for e in all_dp])
    print(f"\n  DEEPER duration (days): {dp_dur}")
    print(f"  Min={dp_dur[0]}  Max={dp_dur[-1]}  Median={dp_dur[len(dp_dur)//2]}")

# ── Threshold test ─────────────────────────────────────────────────────────────
print(f"\n\n{'='*72}")
print("THRESHOLD ANALYSIS")
print(f"{'='*72}")
print(f"  Rule: duration <= T hari -> BULL DIP, > T hari -> DEEPER\n")
print(f"  {'Thresh':>7}  {'BD corr':>8}  {'BD wrong':>9}  "
      f"{'DP corr':>8}  {'DP wrong':>9}  {'Total err':>10}")
print(f"  {'-'*60}")

best_thr = None
best_err = 9999

for thr in [5, 7, 9, 14, 21, 30]:
    bd_ok   = sum(1 for e in all_bd if e['duration'] <= thr)
    bd_bad  = sum(1 for e in all_bd if e['duration'] > thr)
    dp_ok   = sum(1 for e in all_dp if e['duration'] > thr)
    dp_bad  = sum(1 for e in all_dp if e['duration'] <= thr)
    tot_err = bd_bad + dp_bad
    mark    = ' <-- BEST' if tot_err < best_err else ''
    if tot_err < best_err:
        best_err = tot_err
        best_thr = thr
    print(f"  {'<= '+str(thr)+'d':>7}  {bd_ok}/{len(all_bd):>5}    {bd_bad:>6}    "
          f"{dp_ok}/{len(all_dp):>5}    {dp_bad:>6}    {tot_err:>8}{mark}")

# ── Misclassification detail ───────────────────────────────────────────────────
print(f"\n\n{'='*72}")
print(f"DETAIL MISCLASSIFICATION (threshold = 9 hari)")
print(f"{'='*72}")

thr = 9
fn = [e for e in all_bd if e['duration'] > thr]
fp = [e for e in all_dp if e['duration'] <= thr]

print(f"\n  BULL DIP tapi > 9 hari (false negative -- harus DEEPER?): {len(fn)}")
for e in fn:
    print(f"    {e['start_date'].date()} -> {e['end_date'].date()}  "
          f"{e['duration']}d  low=${e['low_price']:,.0f}  "
          f"cycle={e['cycle']}  labels={e['gt_labels']}")

print(f"\n  DEEPER tapi <= 9 hari (false positive -- harus BULL DIP?): {len(fp)}")
for e in fp:
    print(f"    {e['start_date'].date()} -> {e['end_date'].date()}  "
          f"{e['duration']}d  low=${e['low_price']:,.0f}  "
          f"cycle={e['cycle']}  labels={e['gt_labels']}")

print(f"\n{'='*72}")
print("SELESAI")
print(f"{'='*72}")
