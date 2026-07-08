"""
K3 Exit A Threshold Analysis
Tujuan: Cari optimal N (consecutive closes above AVIV Mean) untuk Exit A,
        berdasarkan historical K3 Stage 2 episodes.
"""

import sys
sys.stdout.reconfigure(encoding='utf-8')
import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────
df_aviv = pd.read_csv("data_aviv.csv", parse_dates=['date'])
df_mvrv = pd.read_csv("data_mvrv.csv", parse_dates=['date'])
df_mom  = pd.read_csv("data_momentum.csv", parse_dates=['date'])

df = df_aviv.merge(df_mvrv[['date','mvrv_ratio','sth_mvrv','lth_mvrv']], on='date', how='left')
df = df.merge(df_mom[['date','asopr','sth_sopr']], on='date', how='left')
df = df.sort_values('date').reset_index(drop=True)

# ── Derived columns ────────────────────────────────────────────────────────
# AVIV Upper 0.5σ (ratio level)
df['aviv_upper_0.5sd'] = df['aviv_mean'] + 0.5 * (df['aviv_upper_1sd'] - df['aviv_mean'])
# AVIV Upper 0.5σ (price level)
df['price_at_aviv_upper_0.5sd'] = (
    df['price_at_aviv_mean'] + 0.5 * (df['price_at_aviv_plus_1_sigma'] - df['price_at_aviv_mean'])
)
# Above AVIV Mean flag
df['above_aviv_mean'] = df['btc_price'] > df['price_at_aviv_mean']
# Above AVIV Upper 0.5σ flag
df['above_aviv_upper_0.5sd'] = df['aviv_ratio'] > df['aviv_upper_0.5sd']

# STH-SOPR MAs and gap
df['sth_sopr_ma60'] = df['sth_sopr'].rolling(60, min_periods=30).mean()
df['sth_sopr_ma90'] = df['sth_sopr'].rolling(90, min_periods=45).mean()
df['sth_sopr_ma_gap'] = df['sth_sopr_ma60'] - df['sth_sopr_ma90']

# MA gap rolling max (60-day lookback) to detect "peaked"
df['ma_gap_rolling_max'] = df['sth_sopr_ma_gap'].rolling(60, min_periods=20).max()
# Gap "declining from peak": gap < 95% of its 60-day rolling max
df['ma_gap_declining'] = df['sth_sopr_ma_gap'] < (df['ma_gap_rolling_max'] * 0.95)

# ── Episode definitions ────────────────────────────────────────────────────
# ATH pairs (within same cycle) where MVRV bearish divergence can occur.
# PREREQUISITE check is embedded in the verification below.
EPISODES = [
    {
        'name'       : '2021 Double Top',
        'ath1_date'  : '2021-04-14',
        'ath2_date'  : '2021-11-10',
        'stage_start': '2021-11-10',   # Stage 1/2 search begins at ATH2
        'stage_end'  : '2022-09-30',
        'bull_end'   : '2022-12-31',   # for post-exit price tracking
    },
    {
        'name'       : '2025 Cycle',
        'ath1_date'  : '2024-03-14',
        'ath2_date'  : '2025-01-20',
        'stage_start': '2025-01-20',
        'stage_end'  : '2026-06-29',
        'bull_end'   : '2026-06-29',
    },
]

def get_row(date_str):
    d = pd.Timestamp(date_str)
    rows = df[df['date'] == d]
    return rows.iloc[0] if len(rows) else None

def first_cross_down(window, col_flag):
    """Return index of first day where above_flag goes False after being True."""
    was_above = False
    for i, row in window.iterrows():
        if row[col_flag]:
            was_above = True
        elif was_above:
            return i
    return None

def ma_gap_peaked_date(window):
    """
    Return first date where MA gap is declining (< 95% of 60-day max)
    AND gap was positive before (confirming it was at elevated level).
    """
    prev_positive = False
    for i, row in window.iterrows():
        if row['sth_sopr_ma_gap'] > 0:
            prev_positive = True
        if prev_positive and row['ma_gap_declining'] and row['sth_sopr_ma_gap'] > 0:
            return i
    return None

def find_exit_a(post_k3, n):
    """
    Return (exit_date, exit_price) for N consecutive closes above AVIV Mean.
    Returns (None, None) if never triggered.
    """
    streak = 0
    streak_start = None
    for i, row in post_k3.iterrows():
        if row['above_aviv_mean']:
            if streak == 0:
                streak_start = i
            streak += 1
            if streak >= n:
                return post_k3.loc[i, 'date'], post_k3.loc[i, 'btc_price']
        else:
            streak = 0
            streak_start = None
    return None, None

def post_exit_outcome(df, exit_date, days=60):
    """
    After exit_date, did price continue up or reverse?
    Returns: (max_high_pct, drawdown_pct, still_above_mean_after_30d)
    """
    if exit_date is None:
        return None, None, None
    future = df[(df['date'] > exit_date) & (df['date'] <= exit_date + pd.Timedelta(days=days))]
    if future.empty:
        return None, None, None
    exit_price = df[df['date'] == exit_date]['btc_price'].iloc[0]
    max_high = future['btc_price'].max()
    min_low  = future['btc_price'].min()
    above_30 = future[future['date'] <= exit_date + pd.Timedelta(days=30)]['above_aviv_mean']
    pct_days_above = above_30.mean() if len(above_30) else None
    return (max_high - exit_price) / exit_price * 100, \
           (min_low - exit_price) / exit_price * 100, \
           pct_days_above

def count_whipsaws(post_k3, lookback_days=90):
    """
    Count: price crosses above AVIV Mean but returns below within 3 days.
    """
    window = post_k3.head(lookback_days).reset_index(drop=True)
    whipsaws = 0
    i = 0
    while i < len(window):
        row = window.iloc[i]
        if not row['above_aviv_mean']:
            # look for transition to above
            if i + 1 < len(window) and window.iloc[i+1]['above_aviv_mean']:
                # crossed above — check next 3 days
                fell_back = False
                for j in range(i+1, min(i+5, len(window))):
                    if not window.iloc[j]['above_aviv_mean']:
                        fell_back = True
                        break
                if fell_back:
                    whipsaws += 1
        i += 1
    return whipsaws

# ── Main analysis ──────────────────────────────────────────────────────────
print("=" * 70)
print("K3 EXIT A THRESHOLD ANALYSIS")
print("=" * 70)

N_VALUES = [1, 2, 3, 5, 7]

for ep in EPISODES:
    print(f"\n{'─'*70}")
    print(f"EPISODE: {ep['name']}")
    print(f"{'─'*70}")

    # ── PREREQUISITE check ─────────────────────────────────────────────
    r1 = get_row(ep['ath1_date'])
    r2 = get_row(ep['ath2_date'])
    if r1 is None or r2 is None:
        print("  [SKIP] ATH date not in data.")
        continue

    mvrv_div = r2['mvrv_ratio'] < r1['mvrv_ratio']
    asopr_div = r2['asopr'] < r1['asopr']

    print(f"\n  PREREQUISITE:")
    print(f"    ATH1 ({ep['ath1_date']}): Price={r1['btc_price']:,.0f}  MVRV={r1['mvrv_ratio']:.3f}  aSOPR={r1['asopr']:.4f}")
    print(f"    ATH2 ({ep['ath2_date']}): Price={r2['btc_price']:,.0f}  MVRV={r2['mvrv_ratio']:.3f}  aSOPR={r2['asopr']:.4f}")
    print(f"    MVRV bearish divergence: {'✓ YES' if mvrv_div else '✗ NO'} (ATH2 MVRV {'<' if mvrv_div else '>='} ATH1)")
    print(f"    aSOPR diminishing return: {'✓ YES' if asopr_div else '✗ NO'} (ATH2 aSOPR {'<' if asopr_div else '>='} ATH1)")
    prereq_met = mvrv_div and asopr_div
    print(f"    → PREREQUISITE: {'MET ✓' if prereq_met else 'NOT MET ✗'}")

    # ── Stage 1 & 2 detection ──────────────────────────────────────────
    stage_window = df[
        (df['date'] >= pd.Timestamp(ep['stage_start'])) &
        (df['date'] <= pd.Timestamp(ep['stage_end']))
    ].copy()

    # Stage 1A: AVIV Upper 0.5σ cross-down
    # Find first day where above_aviv_upper_0.5sd goes from True to False
    stage1a_idx = None
    was_above = stage_window['above_aviv_upper_0.5sd'].iloc[0] if len(stage_window) else False
    # Look back a bit to see if was above at ATH2
    lookback = df[df['date'] <= pd.Timestamp(ep['stage_start'])].tail(30)
    was_above_before = lookback['above_aviv_upper_0.5sd'].any()

    if was_above_before:
        for i, row in stage_window.iterrows():
            if not row['above_aviv_upper_0.5sd']:
                stage1a_idx = i
                break
    else:
        # Price wasn't above 0.5sd at ATH2 — find first time it goes above then crosses down
        went_above = False
        for i, row in stage_window.iterrows():
            if row['above_aviv_upper_0.5sd']:
                went_above = True
            elif went_above:
                stage1a_idx = i
                break

    stage1a_date = stage_window.loc[stage1a_idx, 'date'] if stage1a_idx is not None else None
    stage1a_price = stage_window.loc[stage1a_idx, 'btc_price'] if stage1a_idx is not None else None

    # Stage 1B: STH-SOPR MA gap peaked+declining
    stage1b_idx = ma_gap_peaked_date(stage_window)
    stage1b_date  = stage_window.loc[stage1b_idx, 'date'] if stage1b_idx is not None else None
    stage1b_price = stage_window.loc[stage1b_idx, 'btc_price'] if stage1b_idx is not None else None

    print(f"\n  STAGE 1 candidates (whichever fires first):")
    print(f"    1A — AVIV Upper 0.5σ cross-down:   {stage1a_date.date() if stage1a_date else 'NOT FIRED'}  price=${stage1a_price:,.0f}" if stage1a_price else f"    1A — AVIV Upper 0.5σ cross-down:   NOT FIRED")
    print(f"    1B — STH-SOPR MA gap peaked:        {stage1b_date.date() if stage1b_date else 'NOT FIRED'}  price=${stage1b_price:,.0f}" if stage1b_price else f"    1B — STH-SOPR MA gap peaked:        NOT FIRED")

    # Determine which fires first (Stage 1) and which is Stage 2
    if stage1a_date is None and stage1b_date is None:
        print("  → Neither Stage 1 trigger fired. EPISODE SKIPPED.")
        continue

    if stage1a_date is None:
        stage1_date, stage1_label = stage1b_date, "1B (MA gap)"
        stage2_date, stage2_label = None, "1A (AVIV cross) — NOT FIRED"
    elif stage1b_date is None:
        stage1_date, stage1_label = stage1a_date, "1A (AVIV cross)"
        stage2_date, stage2_label = None, "1B (MA gap) — NOT FIRED"
    elif stage1a_date <= stage1b_date:
        stage1_date, stage1_label = stage1a_date, "1A (AVIV cross)"
        # Stage 2 = 1B, must fire AFTER stage1
        stage2_win = stage_window[stage_window['date'] > stage1a_date]
        stage2_idx = ma_gap_peaked_date(stage2_win)
        stage2_date = stage2_win.loc[stage2_idx, 'date'] if stage2_idx is not None else None
        stage2_label = "1B (MA gap)"
    else:
        stage1_date, stage1_label = stage1b_date, "1B (MA gap)"
        # Stage 2 = 1A, must fire AFTER stage1b
        stage2_win = stage_window[stage_window['date'] > stage1b_date]
        was_above_s2 = stage2_win['above_aviv_upper_0.5sd'].any()
        s2_idx = None
        went_above_s2 = False
        for i, row in stage2_win.iterrows():
            if row['above_aviv_upper_0.5sd']:
                went_above_s2 = True
            elif went_above_s2 or was_above_before:
                s2_idx = i
                break
        stage2_date = stage2_win.loc[s2_idx, 'date'] if s2_idx is not None else None
        stage2_label = "1A (AVIV cross)"

    stage1_price = df[df['date'] == stage1_date]['btc_price'].iloc[0] if stage1_date is not None else None
    stage2_price = df[df['date'] == stage2_date]['btc_price'].iloc[0] if stage2_date is not None else None

    print(f"\n  → Stage 1 fired: {stage1_label} on {stage1_date.date() if stage1_date else 'N/A'}  price=${stage1_price:,.0f}" if stage1_price else f"\n  → Stage 1 fired: {stage1_label} — N/A")
    print(f"  → Stage 2 fired: {stage2_label} on {stage2_date.date() if stage2_date else 'NOT FIRED'}  price=${stage2_price:,.0f}" if stage2_price else f"  → Stage 2 fired: {stage2_label}")

    # K3 Stage 2 fire date
    k3_date  = stage2_date if stage2_date is not None else stage1_date
    k3_price = df[df['date'] == k3_date]['btc_price'].iloc[0]
    k3_label = "FULL (Stage 2)" if stage2_date is not None else "PARTIAL (Stage 1 only)"
    print(f"\n  ▶ K3 reference date: {k3_date.date()}  price=${k3_price:,.0f}  [{k3_label}]")

    # ── Post-K3 price vs AVIV Mean ─────────────────────────────────────
    post_k3 = df[df['date'] >= k3_date].copy().reset_index(drop=True)

    print(f"\n  POST-K3 PRICE vs AVIV MEAN (first 30 days):")
    print(f"  {'Date':<12} {'BTC Price':>10} {'AVIV Mean':>10} {'Diff%':>8} {'Above?':>7} {'Streak':>7}")
    print(f"  {'─'*56}")
    streak = 0
    for _, row in post_k3.head(30).iterrows():
        if row['above_aviv_mean']:
            streak += 1
        else:
            streak = 0
        diff_pct = (row['btc_price'] - row['price_at_aviv_mean']) / row['price_at_aviv_mean'] * 100
        flag = "YES" if row['above_aviv_mean'] else "no"
        print(f"  {str(row['date'].date()):<12} {row['btc_price']:>10,.0f} {row['price_at_aviv_mean']:>10,.0f} {diff_pct:>7.1f}% {flag:>7} {streak:>7}")

    # ── Exit A threshold analysis ──────────────────────────────────────
    print(f"\n  EXIT A THRESHOLD ANALYSIS (from K3 date: {k3_date.date()}, price=${k3_price:,.0f}):")
    print(f"  {'N':>3} {'Exit Date':<12} {'Exit Price':>11} {'Δ from K3':>10} {'Max+60d%':>10} {'Min+60d%':>10} {'%DaysAbove/30d':>15} {'Outcome':>12}")
    print(f"  {'─'*90}")

    for n in N_VALUES:
        exit_date, exit_price = find_exit_a(post_k3, n)
        if exit_date is None:
            print(f"  {n:>3} {'NOT TRIGGERED':<12}")
            continue
        delta_pct = (exit_price - k3_price) / k3_price * 100
        max_up, max_dn, pct_above_30 = post_exit_outcome(df, exit_date, days=60)
        # Outcome: if price went up >5% and stayed above mean >60% of next 30d → K3 was WRONG (good exit)
        if max_up is not None:
            if max_up > 5 and pct_above_30 is not None and pct_above_30 > 0.5:
                outcome = "K3 WRONG ✓"
            elif max_dn is not None and max_dn < -10:
                outcome = "EXIT EARLY ✗"
            else:
                outcome = "AMBIGUOUS"
        else:
            outcome = "NO DATA"
        print(f"  {n:>3} {str(exit_date.date()):<12} {exit_price:>11,.0f} {delta_pct:>+9.1f}% {max_up or 0:>+9.1f}% {max_dn or 0:>+9.1f}% {(pct_above_30 or 0)*100:>14.0f}% {outcome:>12}")

    # ── Whipsaw analysis ───────────────────────────────────────────────
    ws_count = count_whipsaws(post_k3, lookback_days=90)
    total_crosses = 0
    in_above = post_k3.iloc[0]['above_aviv_mean']
    for _, row in post_k3.head(90).iterrows():
        if not in_above and row['above_aviv_mean']:
            total_crosses += 1
        in_above = row['above_aviv_mean']
    print(f"\n  WHIPSAW ANALYSIS (first 90 days post-K3):")
    print(f"    Total upward crosses of AVIV Mean: {total_crosses}")
    print(f"    Of those, returned below within 3 days: {ws_count}")
    print(f"    Whipsaw rate: {ws_count/total_crosses*100:.0f}%" if total_crosses > 0 else "    Whipsaw rate: N/A")

    # ── AVIV Mean proximity at K3 fire ────────────────────────────────
    k3_row = df[df['date'] == k3_date].iloc[0]
    k3_to_mean_pct = (k3_price - k3_row['price_at_aviv_mean']) / k3_row['price_at_aviv_mean'] * 100
    print(f"\n  Context: At K3 fire, price was {k3_to_mean_pct:+.1f}% relative to AVIV Mean (${k3_row['price_at_aviv_mean']:,.0f})")

# ── Summary table ──────────────────────────────────────────────────────────
print(f"\n{'='*70}")
print("SUMMARY: ALL EPISODES × ALL N VALUES")
print(f"{'='*70}")
print(f"{'Episode':<22} {'N':>3} {'Triggered?':<12} {'Δ from K3':>10} {'Outcome':>12}")
print(f"{'─'*65}")

for ep in EPISODES:
    r1 = get_row(ep['ath1_date'])
    r2 = get_row(ep['ath2_date'])
    if r1 is None or r2 is None:
        continue
    mvrv_div = r2['mvrv_ratio'] < r1['mvrv_ratio']
    asopr_div = r2['asopr'] < r1['asopr']
    if not (mvrv_div and asopr_div):
        continue

    stage_window = df[
        (df['date'] >= pd.Timestamp(ep['stage_start'])) &
        (df['date'] <= pd.Timestamp(ep['stage_end']))
    ]

    # Re-derive K3 date (simplified)
    stage1a_idx = None
    was_above_before = df[df['date'] <= pd.Timestamp(ep['stage_start'])].tail(30)['above_aviv_upper_0.5sd'].any()
    if was_above_before:
        for i, row in stage_window.iterrows():
            if not row['above_aviv_upper_0.5sd']:
                stage1a_idx = i
                break
    else:
        went_above = False
        for i, row in stage_window.iterrows():
            if row['above_aviv_upper_0.5sd']:
                went_above = True
            elif went_above:
                stage1a_idx = i
                break
    stage1a_date = stage_window.loc[stage1a_idx, 'date'] if stage1a_idx is not None else None
    stage1b_idx = ma_gap_peaked_date(stage_window)
    stage1b_date = stage_window.loc[stage1b_idx, 'date'] if stage1b_idx is not None else None

    if stage1a_date is None and stage1b_date is None:
        continue
    if stage1a_date is None:
        k3_date = stage1b_date
    elif stage1b_date is None:
        k3_date = stage1a_date
    elif stage1a_date <= stage1b_date:
        stage2_win = stage_window[stage_window['date'] > stage1a_date]
        s2i = ma_gap_peaked_date(stage2_win)
        k3_date = stage2_win.loc[s2i, 'date'] if s2i is not None else stage1a_date
    else:
        stage2_win = stage_window[stage_window['date'] > stage1b_date]
        s2_idx = None
        went_up = False
        for i, row in stage2_win.iterrows():
            if row['above_aviv_upper_0.5sd']:
                went_up = True
            elif went_up or was_above_before:
                s2_idx = i
                break
        k3_date = stage2_win.loc[s2_idx, 'date'] if s2_idx is not None else stage1b_date

    k3_price = df[df['date'] == k3_date]['btc_price'].iloc[0]
    post_k3 = df[df['date'] >= k3_date].copy().reset_index(drop=True)

    for n in N_VALUES:
        exit_date, exit_price = find_exit_a(post_k3, n)
        if exit_date is None:
            print(f"  {ep['name']:<22} {n:>3} {'NO':<12} {'—':>10} {'—':>12}")
        else:
            delta_pct = (exit_price - k3_price) / k3_price * 100
            max_up, max_dn, pct_above_30 = post_exit_outcome(df, exit_date, days=60)
            if max_up is not None:
                if max_up > 5 and pct_above_30 is not None and pct_above_30 > 0.5:
                    outcome = "K3 WRONG ✓"
                elif max_dn is not None and max_dn < -10:
                    outcome = "EXIT EARLY ✗"
                else:
                    outcome = "AMBIGUOUS"
            else:
                outcome = "NO DATA"
            print(f"  {ep['name']:<22} {n:>3} {str(exit_date.date()):<12} {delta_pct:>+9.1f}% {outcome:>12}")

print(f"\n{'='*70}")
print("NOTES:")
print("  - Sample size: 2 episodes ONLY. Recommendations have very low statistical confidence.")
print("  - 'K3 WRONG ✓' = Exit A correct: price +5% within 60d AND >50% days above AVIV Mean/30d")
print("  - 'EXIT EARLY ✗' = Price dropped >10% within 60d after exit → K3 was right, exited too soon")
print("  - 'AMBIGUOUS' = Mixed signals, neither clearly right nor wrong")
print("  - Whipsaw = price crosses above AVIV Mean but returns below within 3 days")
print(f"{'='*70}")
