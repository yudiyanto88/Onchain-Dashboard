"""
K3 Exit A Validation v2
Rule: X consecutive daily closes above AVIV Mean AND price still below STH RP
Additional: track STH RP whipsaw behaviour in post-trigger window
"""
import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

# ── Load & merge ───────────────────────────────────────────────────────────
df_aviv = pd.read_csv("data_aviv.csv", parse_dates=['date'])
df_pl   = pd.read_csv("data_price_level.csv", parse_dates=['date'])

df = df_aviv[['date','btc_price','price_at_aviv_mean']].merge(
    df_pl[['date','sth_cost_basis']], on='date', how='inner'
)
df = df.sort_values('date').reset_index(drop=True)
df = df.dropna(subset=['price_at_aviv_mean','sth_cost_basis'])

df['above_aviv'] = df['btc_price'] > df['price_at_aviv_mean']
df['below_sth']  = df['btc_price'] < df['sth_cost_basis']

# ── Periods ────────────────────────────────────────────────────────────────
PERIODS = {
    'Bear 2018-2019'  : ('2018-01-01', '2019-03-31'),
    'Mid-cycle 2021'  : ('2021-05-01', '2021-08-31'),
    'Bear 2022-2023'  : ('2021-11-10', '2023-01-31'),
}
N_VALUES = [2, 3, 4, 5]

# ── Helpers ────────────────────────────────────────────────────────────────
def find_instances(period_df, n):
    """
    Return list of df indices where streak of above_aviv reaches exactly N
    AND price is below STH RP on that trigger day.
    One instance per streak (fires on day-N of each new streak).
    """
    instances = []
    streak = 0
    p = period_df.reset_index()          # keep original df index in 'index' col
    for _, row in p.iterrows():
        if row['above_aviv']:
            streak += 1
            if streak == n and row['below_sth']:
                instances.append(row['index'])  # original df index
        else:
            streak = 0
    return instances

def check_outcome(trigger_idx, window=14):
    """
    Inspect next `window` rows after trigger_idx in the full df.
    Returns dict with outcome flags and price stats.
    """
    future = df.iloc[trigger_idx + 1 : trigger_idx + 1 + window]
    if future.empty:
        return None

    t_price = df.loc[trigger_idx, 'btc_price']

    # Primary outcome
    went_below_aviv = (future['btc_price'] < future['price_at_aviv_mean']).any()

    # STH RP dynamics in window
    crossed_sth_up  = False
    sth_whipsaw     = False
    for _, r in future.iterrows():
        if r['btc_price'] >= r['sth_cost_basis']:
            crossed_sth_up = True
        elif crossed_sth_up:          # was above, now below → whipsaw
            sth_whipsaw = True
            break

    days_above_aviv = future['above_aviv'].sum()
    pct_chg_14d     = (future['btc_price'].iloc[-1] - t_price) / t_price * 100 if len(future) == window else None
    max14            = (future['btc_price'].max() - t_price) / t_price * 100
    min14            = (future['btc_price'].min() - t_price) / t_price * 100

    return {
        'false_exit'    : went_below_aviv,
        'real_exit'     : not went_below_aviv,
        'sth_cross_up'  : crossed_sth_up,
        'sth_whipsaw'   : sth_whipsaw,
        'days_above'    : int(days_above_aviv),
        'pct_chg_14d'   : pct_chg_14d,
        'max14'         : max14,
        'min14'         : min14,
    }

# ── Per-period detail ──────────────────────────────────────────────────────
# Collect all results for summary table
summary = {n: {'instances': 0, 'false': 0, 'real': 0,
               'sth_cross': 0, 'sth_whip': 0} for n in N_VALUES}

print("=" * 72)
print("K3 EXIT A VALIDATION — N consecutive closes above AVIV Mean + below STH RP")
print("=" * 72)

for period_name, (start, end) in PERIODS.items():
    period_df = df[(df['date'] >= start) & (df['date'] <= end)].copy()

    print(f"\n{'─'*72}")
    print(f"PERIOD: {period_name}  ({start} → {end})")
    print(f"{'─'*72}")

    # STH RP whipsaw overview for the period
    sth_crosses = 0
    was_below = period_df['below_sth'].iloc[0]
    for _, r in period_df.iterrows():
        cur_below = r['btc_price'] < r['sth_cost_basis']
        if was_below and not cur_below:
            sth_crosses += 1
        was_below = cur_below
    print(f"  STH RP upward crosses in period: {sth_crosses} (proxy for STH RP whipsaw frequency)")

    for n in N_VALUES:
        instances_idx = find_instances(period_df, n)
        outcomes = [check_outcome(i) for i in instances_idx]
        outcomes = [o for o in outcomes if o is not None]

        n_total  = len(outcomes)
        n_false  = sum(o['false_exit']   for o in outcomes)
        n_real   = sum(o['real_exit']    for o in outcomes)
        n_scross = sum(o['sth_cross_up'] for o in outcomes)
        n_swhip  = sum(o['sth_whipsaw']  for o in outcomes)

        false_rate = f"{n_false/n_total*100:.0f}%" if n_total else "—"

        print(f"\n  N={n}  |  Instances: {n_total}  |  False exit: {n_false} ({false_rate})  |  Real exit: {n_real}")
        print(f"        STH RP cross-up in window: {n_scross}  |  STH RP whipsaw: {n_swhip}")

        if outcomes:
            avg_max = np.mean([o['max14'] for o in outcomes])
            avg_min = np.mean([o['min14'] for o in outcomes])
            print(f"        Avg max+14d: {avg_max:+.1f}%  |  Avg min+14d: {avg_min:+.1f}%")

        # Instance detail
        print(f"        {'Date':<12} {'BTC Price':>10} {'AVIV Mean':>10} {'STH RP':>10} {'Max14':>7} {'Min14':>7} {'FalseExit':>10} {'STH Whip':>9}")
        print(f"        {'─'*80}")
        for idx, o in zip(instances_idx, outcomes):
            row = df.loc[idx]
            fe  = "YES" if o['false_exit'] else "no"
            sw  = "YES" if o['sth_whipsaw'] else "no"
            print(f"        {str(row['date'].date()):<12} {row['btc_price']:>10,.0f} {row['price_at_aviv_mean']:>10,.0f} {row['sth_cost_basis']:>10,.0f} {o['max14']:>+6.1f}% {o['min14']:>+6.1f}% {fe:>10} {sw:>9}")

        # Accumulate summary
        summary[n]['instances'] += n_total
        summary[n]['false']     += n_false
        summary[n]['real']      += n_real
        summary[n]['sth_cross'] += n_scross
        summary[n]['sth_whip']  += n_swhip

# ── Summary table ──────────────────────────────────────────────────────────
print(f"\n{'='*72}")
print("SUMMARY — ALL PERIODS COMBINED")
print(f"{'='*72}")
print(f"  {'N':>3}  {'Instances':>10}  {'FalseExit':>10}  {'FalseRate':>10}  {'RealExit':>9}  {'STH Cross↑':>11}  {'STHWhipsaw':>11}")
print(f"  {'─'*70}")
for n in N_VALUES:
    s = summary[n]
    fr = f"{s['false']/s['instances']*100:.0f}%" if s['instances'] else "—"
    print(f"  {n:>3}  {s['instances']:>10}  {s['false']:>10}  {fr:>10}  {s['real']:>9}  {s['sth_cross']:>11}  {s['sth_whip']:>11}")

# ── Recommendation ─────────────────────────────────────────────────────────
print(f"\n{'='*72}")
print("RECOMMENDATION")
print(f"{'='*72}")
best_n = min(N_VALUES, key=lambda n: (
    summary[n]['false'] / summary[n]['instances'] if summary[n]['instances'] else 1
))
for n in N_VALUES:
    s = summary[n]
    fr = s['false'] / s['instances'] if s['instances'] else 1
    print(f"  N={n}: false exit rate {fr*100:.0f}%  ({s['false']}/{s['instances']})"
          f"  | STH whipsaw in window: {s['sth_whip']}/{s['instances']}")
print(f"\n  Lowest false exit rate: N={best_n}")
print(f"\n  NOTE: Sample covers 3 periods only. Treat as directional, not definitive.")
print(f"  NOTE: 'STH RP whipsaw' counts instances where price crossed above STH RP")
print(f"        in the 14-day window then fell back below — signals choppy STH RP zone.")
print(f"{'='*72}")
