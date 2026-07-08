"""
K3 Stage Analysis: AVIV Upper Cross vs MA60-MA90 Gap
Uses REAL AVIV data from ChartInspect (data_aviv.csv).

CORRECT AVIV band formula (verified against ChartInspect chart crosshair):
  - Base price = btc_price / aviv_ratio  (= true investor/market mean price)
  - Bands computed using FULL HISTORY mean & std of aviv_ratio
  - Price at +Nsig = (hist_mean + N * hist_std) * (btc_price / aviv_ratio)
  - Verified: +0.5sig = $111,743 vs chart $112,500 (0.7% diff); +1sig = $129,179 vs chart $129,900 (0.6% diff)

  NOTE: API columns price_at_aviv_plus_1_sigma and price_at_aviv_mean use 'active_realized_price'
  as base (not true investor price) — those columns give WRONG values for this analysis.

Indicators:
1. Price cross DOWN from AVIV Upper 0.5sig (sustained streak ending)
   - "Streak": price above AVIV +0.5sig for >= MIN_STREAK_DAYS consecutive days
   - Signal: first day price closes below AVIV +0.5sig after sustained streak

2. MA Gap peaked AND declining
   - MA60 = 60-day SMA of MVRV ratio
   - MA90 = 90-day SMA of MVRV ratio
   - Gap = MA60 - MA90 (positive = uptrend)
   - "Gap peaked" = gap has been declining for >= PEAK_CONFIRM_DAYS days after local max
   - Signal date = the day gap was at local max (confirmed after PEAK_CONFIRM_DAYS)
"""

import pandas as pd
import numpy as np

MIN_STREAK_DAYS   = 7   # min days price above AVIV +0.5sig for "sustained streak"
PEAK_CONFIRM_DAYS = 14  # days of decline to confirm MA gap peak

# --- Load data ---
df_aviv = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_aviv.csv", parse_dates=["date"])
df_mvrv = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_mvrv.csv",  parse_dates=["date"])

df = df_aviv[["date","btc_price","aviv_ratio"]].merge(
    df_mvrv[["date","mvrv_ratio"]], on="date", how="inner"
)
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["aviv_ratio","mvrv_ratio","btc_price"])
df = df[df["btc_price"] > 1].reset_index(drop=True)

# --- Compute AVIV bands using CORRECT formula ---
# Full history mean & std of AVIV ratio (verified against ChartInspect chart)
HIST_MEAN = df["aviv_ratio"].mean()
HIST_STD  = df["aviv_ratio"].std()
df["true_mkt_mean"] = df["btc_price"] / df["aviv_ratio"]
df["aviv_05sig"] = (HIST_MEAN + 0.5 * HIST_STD) * df["true_mkt_mean"]
df["aviv_1sig"]  = (HIST_MEAN + 1.0 * HIST_STD) * df["true_mkt_mean"]

# =====================================================================
# INDICATOR 1: AVIV +0.5sig sustained streak cross-down
# =====================================================================
df = df.reset_index(drop=True)
df["above_05sig"] = df["btc_price"] > df["aviv_05sig"]

streak = []
cur = 0
for v in df["above_05sig"]:
    cur = cur + 1 if v else 0
    streak.append(cur)
df["streak_above"] = streak

df["aviv_cross_down"] = False
above = df["above_05sig"].values
strk  = df["streak_above"].values
for i in range(1, len(df)):
    if not above[i] and strk[i-1] >= MIN_STREAK_DAYS:
        df.at[i, "aviv_cross_down"] = True

# =====================================================================
# INDICATOR 2: MA60-MA90 MVRV Gap peaked AND declining
# =====================================================================
df["ma60"] = df["mvrv_ratio"].rolling(60, min_periods=60).mean()
df["ma90"] = df["mvrv_ratio"].rolling(90, min_periods=90).mean()
df["ma_gap"] = df["ma60"] - df["ma90"]

df["gap_peaked_signal"]          = False
df["gap_peak_retroactive_date"]  = pd.NaT

gap_vals = df["ma_gap"].values
dates    = df["date"].values

for i in range(1, len(df) - PEAK_CONFIRM_DAYS):
    if pd.isna(gap_vals[i]) or gap_vals[i] <= 0:
        continue
    if gap_vals[i] <= gap_vals[i-1]:
        continue
    future = gap_vals[i+1 : i+1+PEAK_CONFIRM_DAYS]
    if len(future) < PEAK_CONFIRM_DAYS:
        continue
    if all(future[j] < gap_vals[i] for j in range(len(future))):
        sig_idx = i + PEAK_CONFIRM_DAYS
        if sig_idx < len(df):
            df.at[sig_idx, "gap_peaked_signal"]         = True
            df.at[sig_idx, "gap_peak_retroactive_date"] = dates[i]

# =====================================================================
# Key events
# =====================================================================
events = [
    ("Cycle Top 2017",     "2017-12-17"),
    ("Local Top Apr 2021", "2021-04-14"),
    ("Cycle Top 2021",     "2021-11-08"),
    ("Cycle Top 2025",     "2025-10-05"),
    ("Lower High 2025",    "2025-10-28"),
]
LOOKBACK = 300

print(f"HIST_MEAN={HIST_MEAN:.4f}, HIST_STD={HIST_STD:.4f} -- verified vs ChartInspect crosshair")
print("=" * 95)
print("K3 STAGE ANALYSIS  |  AVIV corrected formula  |  AVIV +0.5sig cross vs MA60-90 Gap")
print(f"Params: min streak={MIN_STREAK_DAYS}d, gap confirm={PEAK_CONFIRM_DAYS}d")
print("=" * 95)

summary_rows = []

for ev_name, ev_date_str in events:
    ev_date  = pd.Timestamp(ev_date_str)
    ev_row   = df[df["date"] <= ev_date].iloc[-1]
    ev_price = ev_row["btc_price"]
    ev_05sig = ev_row["aviv_05sig"]
    ev_1sig  = ev_row["aviv_1sig"]

    window = df[(df["date"] >= ev_date - pd.Timedelta(days=LOOKBACK)) & (df["date"] <= ev_date)]

    # AVIV cross-down
    av_sigs = window[window["aviv_cross_down"]]
    if not av_sigs.empty:
        last_av   = av_sigs.iloc[-1]
        av_date   = last_av["date"]
        av_lead   = (ev_date - av_date).days
        idx       = df.index[df["date"] == av_date][0]
        streak_len = int(df.at[idx-1, "streak_above"])
        streak_start = df.at[idx - streak_len, "date"]
        av_str    = av_date.strftime("%Y-%m-%d")
        av_streak = f"{streak_len}d (from {streak_start.strftime('%Y-%m-%d')})"
    else:
        av_date, av_lead, av_str, av_streak = None, None, "NO SIGNAL (streak past event)", ""

    # MA gap signal
    gp_sigs = window[window["gap_peaked_signal"]]
    if not gp_sigs.empty:
        last_gp       = gp_sigs.iloc[-1]
        gp_sig_date   = last_gp["date"]
        gp_peak_date  = last_gp["gap_peak_retroactive_date"]
        gp_lead_sig   = (ev_date - gp_sig_date).days
        gp_lead_peak  = (ev_date - gp_peak_date).days if pd.notna(gp_peak_date) else None
        pk_gap        = df.loc[df["date"] == gp_peak_date, "ma_gap"].values[0] if pd.notna(gp_peak_date) else None
        gp_str        = gp_sig_date.strftime("%Y-%m-%d")
        gp_peak_str   = gp_peak_date.strftime("%Y-%m-%d") if pd.notna(gp_peak_date) else "?"
    else:
        gp_lead_sig = gp_lead_peak = pk_gap = None
        gp_str = "NO SIGNAL"
        gp_peak_str = ""

    # Winner
    if av_lead is not None and gp_lead_sig is not None:
        diff = av_lead - gp_lead_sig
        who  = f"AVIV +{diff}d earlier" if diff > 0 else (f"MA GAP +{-diff}d earlier" if diff < 0 else "TIE")
    else:
        who = "INCOMPLETE"

    print(f"\n{'─'*95}")
    print(f"EVENT : {ev_name}  |  {ev_date_str}  |  Price=${ev_price:,.0f}")
    print(f"        AVIV +0.5sig={ev_05sig:,.0f}  |  AVIV +1sig={ev_1sig:,.0f}  |  AVIV ratio={ev_row['aviv_ratio']:.4f}")
    print(f"  [1] AVIV +0.5sig cross-down : {av_str}  (lead {av_lead}d)")
    print(f"      Streak info             : {av_streak}")
    print(f"  [2] MA Gap peak signal      : {gp_str}  (lead {gp_lead_sig}d)")
    print(f"      Gap actual peak         : {gp_peak_str}  (lead {gp_lead_peak}d from event)  gap={pk_gap:.4f}" if pk_gap else f"      Gap actual peak: {gp_peak_str}")
    print(f"  >>> {who}")

    summary_rows.append((ev_name, ev_date_str, av_str, av_lead, gp_str, gp_lead_sig, gp_peak_str, gp_lead_peak, who))

# Summary table
print(f"\n{'='*95}")
print("SUMMARY TABLE")
print(f"{'='*95}")
hdr = f"{'Event':<24} {'Date':>12}  {'AVIV Cross':>14} {'Lead':>7}  {'MA Gap Sig':>14} {'Lead':>7}  {'Peak Date':>12} {'Lead':>7}  {'Winner'}"
print(hdr)
print("-"*95)
for ev_name, ev_date_str, av_str, av_lead, gp_str, gp_lead_sig, gp_peak_str, gp_lead_peak, who in summary_rows:
    av_l  = f"{av_lead}d"  if av_lead  is not None else "—"
    gp_l  = f"{gp_lead_sig}d" if gp_lead_sig is not None else "—"
    gp_pl = f"{gp_lead_peak}d" if gp_lead_peak is not None else "—"
    print(f"{ev_name:<24} {ev_date_str:>12}  {av_str:>14} {av_l:>7}  {gp_str:>14} {gp_l:>7}  {gp_peak_str:>12} {gp_pl:>7}  {who}")

# All AVIV cross-down events
print(f"\n{'='*95}")
print("ALL AVIV +0.5sig CROSS-DOWN EVENTS (sustained streaks)")
print(f"{'Cross Date':>12} {'Price':>12} {'AVIV 0.5sig':>12} {'AVIV 1sig':>12} {'Streak':>8}")
print("-"*60)
for _, row in df[df["aviv_cross_down"]].iterrows():
    idx2 = df.index[df["date"] == row["date"]][0]
    sl   = int(df.at[idx2-1, "streak_above"])
    print(f"{row['date'].strftime('%Y-%m-%d'):>12} {row['btc_price']:>12,.0f} {row['aviv_05sig']:>12,.0f} {row['aviv_1sig']:>12,.0f} {sl:>8}d")
