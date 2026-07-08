"""
K3 Stage 2 Trigger Verification — Confirmed Lower High
Tests Triggers A, B, C against:
  - 4 Lower High events (signal = TRUE)
  - 15 Bull Dip events (signal = FALSE POSITIVE if triggered)
"""

import pandas as pd
import numpy as np
from datetime import timedelta

# ─── Load & Merge Data ────────────────────────────────────────────────────────

pl  = pd.read_csv("data_price_level.csv",   parse_dates=["date"])
mv  = pd.read_csv("data_mvrv.csv",          parse_dates=["date"])
mo  = pd.read_csv("data_momentum.csv",      parse_dates=["date"])
ev  = pd.read_csv("data_mvrv_events.csv",   parse_dates=["date"])
av  = pd.read_csv("data_aviv.csv",          parse_dates=["date"])

df = pl[["date","btc_price","active_realized_price"]].copy()
df = df.merge(mv[["date","mvrv_ratio","sth_mvrv","lth_mvrv"]], on="date", how="left")
df = df.merge(mo[["date","sth_sopr"]], on="date", how="left")
df = df[df["date"] >= "2016-01-01"].reset_index(drop=True)

# ─── Derived Metrics ─────────────────────────────────────────────────────────

df["aviv_upper"]         = df["active_realized_price"] * 1.25
df["price_aviv_ratio"]   = df["btc_price"] / df["aviv_upper"]
df["sth_sopr_ma90"]      = df["sth_sopr"].rolling(90).mean()
df["ma90_ma60"]          = df["sth_sopr_ma90"].rolling(60).mean()
df["sopr_gap"]           = df["sth_sopr_ma90"] - df["ma90_ma60"]
df["above_gap"]          = df["sopr_gap"] > 0   # MA90 above MA90-MA60

# ─── Find Bearish Cross dates ─────────────────────────────────────────────────
# A bearish cross = first day MA90 < MA90-MA60 after being above for >=14 days

bearish_crosses = []   # list of dates
above_streak = 0

for i, row in df.iterrows():
    if pd.isna(row["sopr_gap"]):
        above_streak = 0
        continue
    if row["sopr_gap"] > 0:
        above_streak += 1
    else:
        if above_streak >= 14:
            bearish_crosses.append(row["date"])
        above_streak = 0

df["is_bearish_cross"] = df["date"].isin(bearish_crosses)

print(f"Total bearish crosses found (sustained >=14d): {len(bearish_crosses)}")
for bc in bearish_crosses:
    price_at_bc = df.loc[df["date"] == bc, "btc_price"].values[0]
    gap_at_bc   = df.loc[df["date"] == bc, "sopr_gap"].values[0]
    print(f"  {bc.date()}  price=${price_at_bc:,.0f}  gap={gap_at_bc:.5f}")

# ─── Extract Event Windows ────────────────────────────────────────────────────

events = ev[ev["event"].notna() & (ev["event"] != "")].copy()

LOWER_HIGH_LABELS = ["Lower High 2018", "Lower High 2021",
                     "Lower High 2025", "Lower High 2025 Conformation"]
BULL_DIP_LABELS = [
    "Bull Dip Mar 2017", "Bull Dip Jul 2017", "Bull Dip Sep 2017",
    "Bull Dip Jun 2020", "Bull Dip Sep 2020",
    "Bull Dip Jan 2021",
    "Mid-Cycle Correction Start",
    "Bull Dip Mar 2023", "Bull Dip Jun 2023", "Bull Dip Aug-Sep 2023",
    "Bull Dip Jan 2024", "Bull Dip Mei 2024", "Bull Dip Jul 2024",
    "Bull Dip Agt (Yen Carry Trade)", "Bull Dip Sep 2024",
    "Bull Dip MAr - Apr 2025",
]

def get_event_windows(labels):
    result = []
    for lbl in labels:
        grp = events[events["event"] == lbl]
        if grp.empty:
            print(f"  !! Event not found: {lbl}")
            continue
        result.append({
            "label": lbl,
            "start": grp["date"].min(),
            "end":   grp["date"].max(),
            "peak_date":  grp.loc[grp["btc_price"].idxmax(), "date"],
            "peak_price": grp["btc_price"].max(),
            "trough_date":  grp.loc[grp["btc_price"].idxmin(), "date"],
            "trough_price": grp["btc_price"].min(),
        })
    return result

print("\n=== EVENT WINDOWS ===")
lh_events  = get_event_windows(LOWER_HIGH_LABELS)
bd_events  = get_event_windows(BULL_DIP_LABELS)
print(f"\nLower High events: {len(lh_events)}")
print(f"Bull Dip events:   {len(bd_events)}")

# ─── Helper: get row for a date ───────────────────────────────────────────────

def get_row(date):
    r = df[df["date"] == date]
    if r.empty:
        for d in [-1, 1, -2, 2]:
            r = df[df["date"] == date + timedelta(days=d)]
            if not r.empty:
                break
    return r.iloc[0] if not r.empty else None

def rolling_max_before(date, days=30):
    """Max price in the `days` days before `date` (exclusive of date)."""
    sub = df[(df["date"] >= date - timedelta(days=days)) & (df["date"] < date)]
    if sub.empty:
        return None
    return sub["btc_price"].max()

def cycle_ath_before(date, lookback_days=365*2):
    """Max price in the `lookback_days` before `date`."""
    sub = df[(df["date"] >= date - timedelta(days=lookback_days)) & (df["date"] < date)]
    if sub.empty:
        return None
    return sub["btc_price"].max()

def nearest_bearish_cross(date, window_before=45, window_after=15):
    """Find bearish crosses within window_before .. window_after of date."""
    in_window = [bc for bc in bearish_crosses
                 if (date - timedelta(days=window_before)) <= bc <= (date + timedelta(days=window_after))]
    return in_window

# ─── Trigger A: Price/AVIV Upper in 0.95–1.10 ────────────────────────────────

TA_LO = 0.95
TA_HI = 1.10

print("\n\n" + "=" * 72)
print("TRIGGER A — Price/AVIV Upper ratio 0.95–1.10")
print(f"  Definition: ratio between {TA_LO}–{TA_HI} at event date")
print("=" * 72)

ta_lh_hits = 0
ta_bd_fps  = 0

print("\n--- LOWER HIGH EVENTS ---")
print(f"  {'Event':<35} {'Date':<12} {'Price':>10}  {'AVIV Uppr':>10}  {'Ratio':>6}  {'In Range?'}")
for ev_w in lh_events:
    date = ev_w["peak_date"]
    row  = get_row(date)
    if row is None:
        print(f"  {ev_w['label']:<35} DATA MISSING")
        continue
    ratio = row["price_aviv_ratio"]
    in_range = TA_LO <= ratio <= TA_HI
    ath = cycle_ath_before(date, lookback_days=730)
    below_ath = row["btc_price"] < ath if ath else None
    hit = in_range and (below_ath if below_ath is not None else True)
    if hit:
        ta_lh_hits += 1
    marker = "SIGNAL" if hit else "miss"
    print(f"  {ev_w['label']:<35} {str(date.date()):<12} ${row['btc_price']:>9,.0f}  "
          f"${row['aviv_upper']:>9,.0f}  {ratio:>6.3f}  {marker} ({'below ATH' if below_ath else 'AT ATH'})")

print(f"\n  Lower High Hit Rate: {ta_lh_hits}/{len(lh_events)}")

print("\n--- BULL DIP EVENTS ---")
print(f"  {'Event':<35} {'Date':<12} {'Price':>10}  {'Ratio':>6}  {'Label'}")
for ev_w in bd_events:
    # For bull dips, check BOTH the trough (lowest price) AND the peak (recovery)
    # The question asks for the trough date
    date = ev_w["trough_date"]
    row  = get_row(date)
    if row is None:
        print(f"  {ev_w['label']:<35} DATA MISSING")
        continue
    ratio = row["price_aviv_ratio"]
    in_range = TA_LO <= ratio <= TA_HI
    ath = cycle_ath_before(date, lookback_days=730)
    below_ath = row["btc_price"] < ath if ath else None
    fp = in_range and (below_ath if below_ath is not None else True)
    if fp:
        ta_bd_fps += 1
    label = "FALSE POSITIVE" if fp else "ok (not triggered)"
    print(f"  {ev_w['label']:<35} {str(date.date()):<12} ${row['btc_price']:>9,.0f}  {ratio:>6.3f}  {label}")

print(f"\n  Bull Dip False Positive Rate: {ta_bd_fps}/{len(bd_events)}")

# ─── Trigger B: STH-MVRV 1.00–1.07 + prior ≥15% selloff ─────────────────────

TB_LO = 1.00
TB_HI = 1.07
SELLOFF_PCT = 0.15
SELLOFF_WINDOW = 30

print("\n\n" + "=" * 72)
print("TRIGGER B — STH-MVRV 1.00–1.07 + prior selloff >=15%")
print(f"  Definition: STH-MVRV in {TB_LO}–{TB_HI} AND price dropped >=15% from high "
      f"in last {SELLOFF_WINDOW}d")
print("=" * 72)

tb_lh_hits = 0
tb_bd_fps  = 0

print("\n--- LOWER HIGH EVENTS ---")
print(f"  {'Event':<35} {'Date':<12} {'STH-MVRV':>9}  {'Selloff':>8}  {'Result'}")
for ev_w in lh_events:
    date = ev_w["peak_date"]
    row  = get_row(date)
    if row is None:
        continue
    sth_mv = row["sth_mvrv"]
    in_range = TB_LO <= sth_mv <= TB_HI
    # Selloff: max price in 30d before date vs current
    prior_max = rolling_max_before(date, days=SELLOFF_WINDOW)
    selloff = (prior_max - row["btc_price"]) / prior_max if prior_max else 0
    has_selloff = selloff >= SELLOFF_PCT
    hit = in_range and has_selloff
    if hit:
        tb_lh_hits += 1
    marker = "SIGNAL" if hit else f"miss ({'no selloff' if not has_selloff else 'MVRV out of range'})"
    print(f"  {ev_w['label']:<35} {str(date.date()):<12} {sth_mv:>9.4f}  "
          f"{selloff:>7.1%}  {marker}")

print(f"\n  Lower High Hit Rate: {tb_lh_hits}/{len(lh_events)}")

print("\n--- BULL DIP EVENTS ---")
print(f"  {'Event':<35} {'Date':<12} {'STH-MVRV':>9}  {'Selloff':>8}  {'Label'}")
for ev_w in bd_events:
    date = ev_w["trough_date"]
    row  = get_row(date)
    if row is None:
        continue
    sth_mv = row["sth_mvrv"]
    in_range = TB_LO <= sth_mv <= TB_HI
    prior_max = rolling_max_before(date, days=SELLOFF_WINDOW)
    selloff = (prior_max - row["btc_price"]) / prior_max if prior_max else 0
    has_selloff = selloff >= SELLOFF_PCT
    fp = in_range and has_selloff
    if fp:
        tb_bd_fps += 1
    label = "FALSE POSITIVE" if fp else "ok"
    print(f"  {ev_w['label']:<35} {str(date.date()):<12} {sth_mv:>9.4f}  "
          f"{selloff:>7.1%}  {label}")

print(f"\n  Bull Dip False Positive Rate: {tb_bd_fps}/{len(bd_events)}")

# ─── Trigger C: SOPR Bearish Cross MA90 ──────────────────────────────────────

print("\n\n" + "=" * 72)
print("TRIGGER C — SOPR MA90 Bearish Cross (MA90 crosses below MA90-MA60)")
print("  Filter: sustained above >=14 days before cross")
print("=" * 72)

tc_lh_hits = 0
tc_bd_fps  = 0

# For lower highs: find bearish cross in window 60d before to 15d after LH peak
print("\n--- LOWER HIGH EVENTS ---")
print(f"  {'Event':<35} {'LH Peak Date':<14} {'Cross Date':<12} {'Days Lead':>10}  {'Result'}")

lh_tc_details = []
for ev_w in lh_events:
    date = ev_w["peak_date"]
    crosses = nearest_bearish_cross(date, window_before=60, window_after=15)
    if crosses:
        # Use the cross CLOSEST to (but ideally before) the lower high
        # Prefer crosses before the LH
        before = [c for c in crosses if c <= date]
        after  = [c for c in crosses if c > date]
        if before:
            chosen = max(before)  # most recent before LH
        else:
            chosen = min(after)   # earliest after LH
        lead = (date - chosen).days
        tc_lh_hits += 1
        marker = "SIGNAL"
        price_at_cross = df.loc[df["date"] == chosen, "btc_price"].values[0]
    else:
        chosen = None
        lead   = None
        marker = "miss (no cross nearby)"
        price_at_cross = None

    lh_tc_details.append({
        "label": ev_w["label"],
        "peak_date": date,
        "cross_date": chosen,
        "lead_days": lead,
        "price_at_cross": price_at_cross,
    })
    cross_str = str(chosen.date()) if chosen else "N/A"
    lead_str  = f"{lead:+d}d" if lead is not None else "N/A"
    price_str = f"${price_at_cross:,.0f}" if price_at_cross else "N/A"
    print(f"  {ev_w['label']:<35} {str(date.date()):<14} {cross_str:<12} {lead_str:>10}  {marker}  ({price_str})")

print(f"\n  Lower High Hit Rate: {tc_lh_hits}/{len(lh_events)}")

# For bull dips: check if there's a bearish cross within 30d before or during the dip
BULL_DIP_WINDOW = 30
print(f"\n--- BULL DIP EVENTS (cross within {BULL_DIP_WINDOW}d before trough) ---")
print(f"  {'Event':<35} {'Trough Date':<14} {'Cross Date':<12} {'Label'}")

for ev_w in bd_events:
    date = ev_w["trough_date"]
    # Check for bearish cross within 30 days BEFORE the trough (and during the dip window)
    crosses = nearest_bearish_cross(date, window_before=BULL_DIP_WINDOW, window_after=5)
    if crosses:
        chosen = crosses[0]  # earliest cross in window
        tc_bd_fps += 1
        label = f"FALSE POSITIVE (cross {chosen.date()})"
    else:
        chosen = None
        label = "ok (no cross)"
    print(f"  {ev_w['label']:<35} {str(date.date()):<14} "
          f"{str(chosen.date()) if chosen else 'N/A':<12} {label}")

print(f"\n  Bull Dip False Positive Rate: {tc_bd_fps}/{len(bd_events)}")

# ─── Combined Analysis ────────────────────────────────────────────────────────

print("\n\n" + "=" * 72)
print("COMBINATION ANALYSIS: 2-of-3 Triggers")
print("=" * 72)

# For lower highs: count how many triggers each event satisfies
print("\n--- LOWER HIGH — Per-Event Trigger Count ---")
print(f"  {'Event':<35} {'TA':>4}  {'TB':>4}  {'TC':>4}  {'Count':>6}  {'>=2?'}")

lh_combo_hits = 0
lh_trigger_matrix = []

for i, ev_w in enumerate(lh_events):
    date = ev_w["peak_date"]
    row  = get_row(date)
    if row is None:
        continue

    # TA
    ratio = row["price_aviv_ratio"]
    ath = cycle_ath_before(date, lookback_days=730)
    below_ath = row["btc_price"] < ath if ath else True
    ta = (TA_LO <= ratio <= TA_HI) and below_ath

    # TB
    sth_mv = row["sth_mvrv"]
    prior_max = rolling_max_before(date, days=SELLOFF_WINDOW)
    selloff = (prior_max - row["btc_price"]) / prior_max if prior_max else 0
    tb = (TB_LO <= sth_mv <= TB_HI) and (selloff >= SELLOFF_PCT)

    # TC
    crosses = nearest_bearish_cross(date, window_before=60, window_after=15)
    tc = len(crosses) > 0

    count = sum([ta, tb, tc])
    combo = count >= 2
    if combo:
        lh_combo_hits += 1

    lh_trigger_matrix.append({"label": ev_w["label"], "ta": ta, "tb": tb, "tc": tc, "count": count})
    print(f"  {ev_w['label']:<35} {'Y' if ta else 'n':>4}  {'Y' if tb else 'n':>4}  "
          f"{'Y' if tc else 'n':>4}  {count:>6}  {'YES' if combo else 'no'}")

print(f"\n  2-of-3 Hit Rate: {lh_combo_hits}/{len(lh_events)}")

print("\n--- BULL DIP — Per-Event Trigger Count ---")
print(f"  {'Event':<35} {'TA':>4}  {'TB':>4}  {'TC':>4}  {'Count':>6}  {'>=2? (FP)'}")

bd_combo_fps = 0
bd_trigger_matrix = []

for ev_w in bd_events:
    date = ev_w["trough_date"]
    row  = get_row(date)
    if row is None:
        continue

    # TA
    ratio = row["price_aviv_ratio"]
    ath = cycle_ath_before(date, lookback_days=730)
    below_ath = row["btc_price"] < ath if ath else True
    ta = (TA_LO <= ratio <= TA_HI) and below_ath

    # TB
    sth_mv = row["sth_mvrv"]
    prior_max = rolling_max_before(date, days=SELLOFF_WINDOW)
    selloff = (prior_max - row["btc_price"]) / prior_max if prior_max else 0
    tb = (TB_LO <= sth_mv <= TB_HI) and (selloff >= SELLOFF_PCT)

    # TC — check within 30d before trough
    crosses = nearest_bearish_cross(date, window_before=BULL_DIP_WINDOW, window_after=5)
    tc = len(crosses) > 0

    count = sum([ta, tb, tc])
    combo = count >= 2
    if combo:
        bd_combo_fps += 1

    bd_trigger_matrix.append({"label": ev_w["label"], "ta": ta, "tb": tb, "tc": tc, "count": count})
    fp_label = "FALSE POSITIVE" if combo else "ok"
    print(f"  {ev_w['label']:<35} {'Y' if ta else 'n':>4}  {'Y' if tb else 'n':>4}  "
          f"{'Y' if tc else 'n':>4}  {count:>6}  {fp_label}")

print(f"\n  2-of-3 False Positive Rate: {bd_combo_fps}/{len(bd_events)}")

# ─── Summary Table ────────────────────────────────────────────────────────────

print("\n\n" + "=" * 72)
print("SUMMARY TABLE")
print("=" * 72)
print(f"\n  {'Trigger':<35} {'Hit LH':>10}  {'FP Bull Dip':>12}  {'Precision'}")
print(f"  {'-'*65}")

n_lh = len(lh_events)
n_bd = len(bd_events)

for t_name, hits, fps in [
    ("A — Price/AVIV Upper 0.95–1.10",  ta_lh_hits, ta_bd_fps),
    ("B — STH-MVRV 1.00–1.07 + selloff", tb_lh_hits, tb_bd_fps),
    ("C — SOPR MA90 Bearish Cross",     tc_lh_hits, tc_bd_fps),
    ("COMBO: 2-of-3",                   lh_combo_hits, bd_combo_fps),
]:
    # Precision = hits / (hits + fps) in a balanced set
    total_signals = hits + fps
    precision = hits / total_signals if total_signals > 0 else 0
    hit_rate = hits / n_lh
    fp_rate  = fps / n_bd
    print(f"  {t_name:<35} {hits}/{n_lh} ({hit_rate:.0%}){'':<3}  "
          f"{fps}/{n_bd} ({fp_rate:.0%}){'':<6}  P={precision:.0%}")

# ─── Recommendation ───────────────────────────────────────────────────────────

print("\n\n" + "=" * 72)
print("ASSESSMENT & REKOMENDASI")
print("=" * 72)
print("""
[Lihat output di atas untuk data kuantitatif]

Interpretasi:
- Hit Rate LH = seberapa sering trigger aktif di real lower high (higher = better)
- FP Rate BD  = seberapa sering trigger keliru aktif di bull dip (lower = better)
- Precision   = TP / (TP + FP) dalam dataset ini

Target untuk K3 Stage 2 trigger eksekusi:
- Ideal: Hit LH >= 3/4 (75%), FP Bull Dip <= 3/15 (20%), Precision >= 70%
- Combo 2-of-3: lebih restrictive — idealnya FP <= 2/15 (13%)
""")
