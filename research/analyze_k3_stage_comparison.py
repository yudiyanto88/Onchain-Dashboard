"""
K3 Stage Analysis: AVIV Upper Cross vs STH-SOPR MA90/MA90-MA60 Gap
Sesuai SOPR Knowledge Base v1.4 Section 12.

INDICATOR 1: Price cross DOWN dari AVIV +0.5sig (sustained streak ending)
  - "Streak": price above AVIV +0.5sig >= MIN_STREAK_DAYS consecutive days
  - Signal date: first day price closes BELOW AVIV +0.5sig after sustained streak

INDICATOR 2: Gap STH-SOPR MA90 / MA90-MA60 peaked AND declining
  (Section 12.1 SOPR KB v1.4)
  - MA90      = SMA(STH-SOPR, 90)
  - MA90_MA60 = SMA(MA90, 60)  <-- double-smoothed baseline
  - Gap       = MA90 - MA90_MA60
  - "Peak + declining" = gap mulai turun dan PEAK_CONFIRM_DAYS hari berturut-turut
                         semua gap < gap di hari puncak
  - Signal date = hari ke-PEAK_CONFIRM_DAYS setelah puncak (retroactive peak date juga dicatat)
"""

import pandas as pd
import numpy as np
import sys

MIN_STREAK_DAYS   = 7    # min days price above AVIV +0.5sig for "sustained streak"
PEAK_CONFIRM_DAYS = 14   # days of decline to confirm MA90-MA90_MA60 gap peak

# ─── Load data ───────────────────────────────────────────────────────────────
df_aviv     = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_aviv.csv",     parse_dates=["date"])
df_momentum = pd.read_csv(r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum.csv", parse_dates=["date"])

df = (df_aviv[["date","btc_price","aviv_ratio"]]
      .merge(df_momentum[["date","sth_sopr"]], on="date", how="inner"))
df = df.sort_values("date").reset_index(drop=True)
df = df.dropna(subset=["aviv_ratio","sth_sopr","btc_price"])
df = df[df["btc_price"] > 1].reset_index(drop=True)

# ─── AVIV bands (verified formula) ──────────────────────────────────────────
HIST_MEAN = df["aviv_ratio"].mean()
HIST_STD  = df["aviv_ratio"].std()
df["true_mkt_mean"] = df["btc_price"] / df["aviv_ratio"]
df["aviv_05sig"]    = (HIST_MEAN + 0.5 * HIST_STD) * df["true_mkt_mean"]
df["aviv_1sig"]     = (HIST_MEAN + 1.0 * HIST_STD) * df["true_mkt_mean"]

# =============================================================================
# INDICATOR 1: AVIV +0.5sig sustained streak cross-down
# =============================================================================
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

# =============================================================================
# INDICATOR 2: STH-SOPR MA90/MA90-MA60 gap peaked AND declining
# (SOPR KB v1.4 Section 12)
# =============================================================================
df["ma90_sth"]        = df["sth_sopr"].rolling(90,  min_periods=90).mean()
df["ma90_ma60_sth"]   = df["ma90_sth"].rolling(60,  min_periods=60).mean()
df["sth_gap"]         = df["ma90_sth"] - df["ma90_ma60_sth"]

df["gap_peaked_signal"]         = False
df["gap_peak_retroactive_date"] = pd.NaT

gap_vals = df["sth_gap"].values
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

# =============================================================================
# Key events untuk comparison
# =============================================================================
events = [
    ("Cycle Top 2017",     "2017-12-17"),
    ("Local Top Apr 2021", "2021-04-14"),
    ("Cycle Top 2021",     "2021-11-08"),
    ("Jul-Aug ATH 2025",   "2025-08-01"),
    ("Lower High Oct 2025","2025-10-28"),
]
LOOKBACK = 365

print(f"HIST_MEAN={HIST_MEAN:.4f}, HIST_STD={HIST_STD:.4f}")
print("=" * 110)
print("K3 STAGE COMPARISON  |  AVIV +0.5sig Cross-Down  vs  STH-SOPR MA90/MA90-MA60 Gap Peak")
print(f"Params: min streak={MIN_STREAK_DAYS}d, gap confirm={PEAK_CONFIRM_DAYS}d")
print("=" * 110)

summary_rows = []

for ev_name, ev_date_str in events:
    ev_date  = pd.Timestamp(ev_date_str)
    ev_row   = df[df["date"] <= ev_date].iloc[-1]
    ev_price = ev_row["btc_price"]
    ev_05sig = ev_row["aviv_05sig"]
    ev_gap   = ev_row["sth_gap"]

    window = df[(df["date"] >= ev_date - pd.Timedelta(days=LOOKBACK)) & (df["date"] <= ev_date)]

    # --- INDICATOR 1: AVIV cross-down ---
    av_sigs = window[window["aviv_cross_down"]]
    if not av_sigs.empty:
        last_av    = av_sigs.iloc[-1]
        av_date    = last_av["date"]
        av_lead    = (ev_date - av_date).days
        idx        = df.index[df["date"] == av_date][0]
        streak_len = int(df.at[idx-1, "streak_above"])
        av_str     = av_date.strftime("%Y-%m-%d")
        av_streak  = f"{streak_len}d streak sebelumnya"
    else:
        av_date, av_lead, av_str, av_streak = None, None, "NO SIGNAL", ""

    # --- INDICATOR 2: STH-SOPR MA Gap peaked ---
    gp_sigs = window[window["gap_peaked_signal"]]
    if not gp_sigs.empty:
        last_gp      = gp_sigs.iloc[-1]
        gp_sig_date  = last_gp["date"]
        gp_peak_date = last_gp["gap_peak_retroactive_date"]
        gp_lead_sig  = (ev_date - gp_sig_date).days
        gp_lead_peak = (ev_date - gp_peak_date).days if pd.notna(gp_peak_date) else None
        pk_gap       = df.loc[df["date"] == gp_peak_date, "sth_gap"].values[0] if pd.notna(gp_peak_date) else None
        gp_str       = gp_sig_date.strftime("%Y-%m-%d")
        gp_peak_str  = gp_peak_date.strftime("%Y-%m-%d") if pd.notna(gp_peak_date) else "?"
        pk_gap_str   = f"{pk_gap:.5f}" if pk_gap is not None else ""
    else:
        gp_lead_sig = gp_lead_peak = pk_gap = None
        gp_str = gp_peak_str = pk_gap_str = "NO SIGNAL"

    # --- Siapa duluan? ---
    if av_lead is not None and gp_lead_sig is not None:
        diff = av_lead - gp_lead_sig
        if diff > 0:
            who = f"AVIV lebih dulu +{diff}d"
        elif diff < 0:
            who = f"STH GAP lebih dulu +{-diff}d"
        else:
            who = "TIE (hari yg sama)"
    else:
        who = "INCOMPLETE"

    print(f"\n{'─'*110}")
    print(f"EVENT : {ev_name}  ({ev_date_str})  |  Price=${ev_price:,.0f}  |  AVIV +0.5sig=${ev_05sig:,.0f}")
    print(f"  [1] AVIV +0.5sig cross-down : {av_str:<14}  (lead ke event: {av_lead}d)  |  {av_streak}")
    print(f"  [2] STH Gap signal date     : {gp_str:<14}  (lead ke event: {gp_lead_sig}d)")
    if gp_peak_str != "NO SIGNAL":
        print(f"      Gap actual peak date    : {gp_peak_str:<14}  (lead ke event: {gp_lead_peak}d)  |  gap max={pk_gap_str}")
    print(f"  >>> {who}")

    summary_rows.append({
        "Event":           ev_name,
        "Tgl Event":       ev_date_str,
        "AVIV Cross Date": av_str,
        "AVIV Lead":       f"{av_lead}d" if av_lead is not None else "-",
        "STH Gap Sig Date":gp_str,
        "STH Gap Lead":    f"{gp_lead_sig}d" if gp_lead_sig is not None else "-",
        "Gap Peak Date":   gp_peak_str if gp_peak_str != "NO SIGNAL" else "-",
        "Gap Peak Lead":   f"{gp_lead_peak}d" if gp_lead_peak is not None else "-",
        "Peak Gap Value":  pk_gap_str if pk_gap_str else "-",
        "Duluan":          who,
    })

# ─── Summary table ────────────────────────────────────────────────────────────
print(f"\n{'='*110}")
print("TABEL RINGKASAN")
print(f"{'='*110}")
print(f"{'Event':<22} {'Tgl Event':>12} | {'AVIV Cross':>12} {'Lead':>7} | {'STH Gap Sig':>12} {'Lead':>7} | {'Gap Peak':>12} {'Lead':>7} | Duluan")
print("-"*110)
for r in summary_rows:
    print(
        f"{r['Event']:<22} {r['Tgl Event']:>12} | "
        f"{r['AVIV Cross Date']:>12} {r['AVIV Lead']:>7} | "
        f"{r['STH Gap Sig Date']:>12} {r['STH Gap Lead']:>7} | "
        f"{r['Gap Peak Date']:>12} {r['Gap Peak Lead']:>7} | "
        f"{r['Duluan']}"
    )

# ─── Semua AVIV cross-down events ────────────────────────────────────────────
print(f"\n{'='*110}")
print("SEMUA AVIV +0.5sig CROSS-DOWN EVENTS (sustained streaks)")
print(f"{'Cross Date':>12} {'Price':>12} {'AVIV 0.5sig':>12} {'Streak sebelumnya':>20}")
print("-"*60)
for _, row in df[df["aviv_cross_down"]].iterrows():
    idx2 = df.index[df["date"] == row["date"]][0]
    sl   = int(df.at[idx2-1, "streak_above"])
    print(f"{row['date'].strftime('%Y-%m-%d'):>12} {row['btc_price']:>12,.0f} {row['aviv_05sig']:>12,.0f} {sl:>18}d")

# ─── STH-SOPR Gap: semua peak signals ─────────────────────────────────────────
print(f"\n{'='*110}")
print("SEMUA STH-SOPR MA90/MA90-MA60 GAP PEAK SIGNALS (confirmed setelah 14d decline)")
print(f"{'Signal Date':>12} {'Peak Date':>12} {'Price at Peak':>14} {'Gap at Peak':>13}")
print("-"*60)
peak_events = df[df["gap_peaked_signal"]].copy()
for _, row in peak_events.iterrows():
    pk_dt = row["gap_peak_retroactive_date"]
    if pd.notna(pk_dt):
        pk_price = df.loc[df["date"] == pk_dt, "btc_price"].values
        pk_g     = df.loc[df["date"] == pk_dt, "sth_gap"].values
        pk_price_str = f"${pk_price[0]:,.0f}" if len(pk_price) > 0 else "-"
        pk_g_str     = f"{pk_g[0]:.5f}"       if len(pk_g)     > 0 else "-"
    else:
        pk_price_str = pk_g_str = "-"
    print(f"{row['date'].strftime('%Y-%m-%d'):>12} {str(pk_dt)[:10]:>12} {pk_price_str:>14} {pk_g_str:>13}")
