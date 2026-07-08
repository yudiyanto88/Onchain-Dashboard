"""
K3 Stage 1 Trigger Verification — Bitcoin On-Chain Framework
Analyzes 3 triggers for early warning of bear market across 3 cycles:
  2017 (Cycle Peak Dec 2017 → Lower High Jan 2018)
  2021 (Cycle Peak Nov 2021 → Lower High Nov-Dec 2021)
  2025 (Cycle Peak Oct 2025 → Lower High Oct 2025)
"""

import pandas as pd
import numpy as np
from datetime import timedelta

# ─── Load Data ───────────────────────────────────────────────────────────────

pl = pd.read_csv("data_price_level.csv", parse_dates=["date"])
mv = pd.read_csv("data_mvrv.csv", parse_dates=["date"])
mo = pd.read_csv("data_momentum.csv", parse_dates=["date"])
ev = pd.read_csv("data_mvrv_events.csv", parse_dates=["date"])

df = pl[["date","btc_price","active_realized_price"]].copy()
df = df.merge(mv[["date","mvrv_ratio","sth_mvrv","lth_mvrv"]], on="date", how="left")
df = df.merge(mo[["date","sth_sopr"]], on="date", how="left")
df = df[df["date"] >= "2016-01-01"].reset_index(drop=True)

# ─── Derived Metrics ─────────────────────────────────────────────────────────

df["aviv_upper"] = df["active_realized_price"] * 1.25
df["price_aviv_upper_ratio"] = df["btc_price"] / df["aviv_upper"]
df["above_aviv_upper"] = df["btc_price"] > df["aviv_upper"]

df["sth_sopr_ma90"] = df["sth_sopr"].rolling(90).mean()
df["ma90_ma60"] = df["sth_sopr_ma90"].rolling(60).mean()
df["sopr_gap"] = df["sth_sopr_ma90"] - df["ma90_ma60"]

# ─── Cycle Definitions ───────────────────────────────────────────────────────
# Dates determined from event labels — using peak day within labeled window

CYCLES = {
    "2017": {
        "cycle_peak_date": pd.Timestamp("2017-12-16"),   # ATH $19,538
        "lower_high_date": pd.Timestamp("2018-01-06"),   # $17,578 peak
        "analysis_start":  pd.Timestamp("2017-01-01"),
        "local_tops": [
            ("Cycle Peak Dec 2017", pd.Timestamp("2017-12-16")),
        ],
    },
    "2021": {
        "cycle_peak_date": pd.Timestamp("2021-11-08"),   # ATH $67,524
        "lower_high_date": pd.Timestamp("2021-12-01"),   # $57,273 peak
        "analysis_start":  pd.Timestamp("2021-01-01"),
        "local_tops": [
            ("Local Top Mar 2021",    pd.Timestamp("2021-03-13")),
            ("Local Top Apr 2021",    pd.Timestamp("2021-04-13")),
            ("Cycle Peak Nov 2021",   pd.Timestamp("2021-11-08")),
        ],
    },
    "2025": {
        "cycle_peak_date": pd.Timestamp("2025-10-06"),   # ATH $124,714
        "lower_high_date": pd.Timestamp("2025-10-27"),   # $114,143 peak
        "analysis_start":  pd.Timestamp("2024-01-01"),
        "local_tops": [
            ("Local Top Mar 2024",    pd.Timestamp("2024-03-13")),
            ("Local Top Des 2024",    pd.Timestamp("2024-12-16")),
            ("Local Top Jan 2025",    pd.Timestamp("2025-01-22")),
            ("Local Top Jul-Aug 2025",pd.Timestamp("2025-08-13")),
            ("Cycle Peak Oct 2025",   pd.Timestamp("2025-10-06")),
        ],
    },
}

# ─── TRIGGER 1: AVIV Upper Streak Ends ────────────────────────────────────────

print("=" * 70)
print("TRIGGER 1 — AVIV Upper Streak Ends")
print("=" * 70)

t1_results = []

for cycle, cfg in CYCLES.items():
    lh_date = cfg["lower_high_date"]
    start   = cfg["analysis_start"]
    cp_date = cfg["cycle_peak_date"]

    # Work on data from analysis_start up to lower high + 30d buffer
    mask = (df["date"] >= start) & (df["date"] <= lh_date + timedelta(days=30))
    sub  = df[mask].copy().reset_index(drop=True)

    above = sub["above_aviv_upper"].values
    dates = sub["date"].values
    prices = sub["btc_price"].values
    aviv_uppers = sub["aviv_upper"].values

    # Find all streaks of consecutive days above AVIV Upper
    streaks = []
    i = 0
    while i < len(above):
        if above[i]:
            j = i
            while j < len(above) and above[j]:
                j += 1
            streak_len = j - i
            streaks.append({
                "start_idx": i,
                "end_idx":   j - 1,  # last day still above
                "break_idx": j,      # first day below (or end of data)
                "length":    streak_len,
                "start_date": pd.Timestamp(dates[i]),
                "last_above": pd.Timestamp(dates[j-1]),
                "break_date": pd.Timestamp(dates[j]) if j < len(dates) else None,
            })
            i = j
        else:
            i += 1

    # Filter streaks of >= 14 days that start before lower high
    valid = [s for s in streaks if s["length"] >= 14 and s["start_date"] <= lh_date]

    if not valid:
        print(f"\n[{cycle}] No sustained streak ≥14 days found before Lower High")
        t1_results.append({
            "cycle": cycle,
            "streak_start": None,
            "streak_end_signal": None,
            "days_to_lower_high": None,
            "streak_length": None,
        })
        continue

    # Use the LAST valid streak (closest to cycle peak / lower high)
    last_streak = valid[-1]

    streak_start = last_streak["start_date"]
    last_above   = last_streak["last_above"]
    break_date   = last_streak["break_date"]  # signal = first day below AVIV Upper
    streak_len   = last_streak["length"]

    if break_date is None:
        print(f"\n[{cycle}] Streak never broke before lower high — streak still active at LH")
        t1_results.append({
            "cycle": cycle,
            "streak_start": streak_start,
            "streak_end_signal": None,
            "days_to_lower_high": None,
            "streak_length": streak_len,
        })
        continue

    days_to_lh = (lh_date - break_date).days

    print(f"\n[{cycle}]")
    print(f"  Streak start       : {streak_start.date()}  ({streak_len} days above AVIV Upper)")
    print(f"  Last day above     : {last_above.date()}")
    print(f"  Streak break (signal): {break_date.date()}  (price first drops below AVIV Upper)")
    print(f"  Lower High actual  : {lh_date.date()}")
    print(f"  Days to Lower High : {days_to_lh:+d}  ({'before' if days_to_lh>0 else 'after'})")

    # Show price context around break
    bk_idx = last_streak["break_idx"]
    if bk_idx < len(sub):
        print(f"  Price at break     : ${sub.iloc[bk_idx]['btc_price']:,.0f}  |  AVIV Upper: ${sub.iloc[bk_idx]['aviv_upper']:,.0f}")

    t1_results.append({
        "cycle": cycle,
        "streak_start": streak_start,
        "streak_end_signal": break_date,
        "days_to_lower_high": days_to_lh,
        "streak_length": streak_len,
    })

    # Also list all ≥14d streaks for context
    if len(valid) > 1:
        print(f"\n  [All valid streaks >=14d before LH:]")
        for s in valid:
            bd = s["break_date"].date() if s["break_date"] else "no break"
            lead = (lh_date - s["break_date"]).days if s["break_date"] else "N/A"
            print(f"    {s['start_date'].date()} to {s['last_above'].date()} "
                  f"({s['length']}d)  break: {bd}  -> {lead}d to LH")


# ─── TRIGGER 2: MVRV Bearish Divergence Across ATHs ──────────────────────────

print("\n\n" + "=" * 70)
print("TRIGGER 2 — MVRV Bearish Divergence Across ATHs")
print("=" * 70)

t2_results = []

for cycle, cfg in CYCLES.items():
    lh_date  = cfg["lower_high_date"]
    cp_date  = cfg["cycle_peak_date"]
    lt_list  = cfg["local_tops"]

    print(f"\n[{cycle}]  Local tops + cycle peak:")

    rows = []
    for name, lt_date in lt_list:
        row = df[df["date"] == lt_date]
        if row.empty:
            # Try day before/after
            for delta in [-1, 1, -2, 2]:
                row = df[df["date"] == lt_date + timedelta(days=delta)]
                if not row.empty:
                    break
        if row.empty:
            print(f"  !! Date {lt_date.date()} not found in data for {name}")
            continue
        r = row.iloc[0]
        rows.append({
            "name": name,
            "date": r["date"],
            "price": r["btc_price"],
            "mvrv": r["mvrv_ratio"],
            "sth_mvrv": r["sth_mvrv"],
        })

    # Print table
    print(f"  {'ATH / Top':<30} {'Date':<12} {'Price':>12}  {'MVRV':>6}  {'STH-MVRV':>9}  {'Divg?'}")
    prev = None
    first_sth_below_110 = None
    first_sth_below_105 = None

    for r in rows:
        if prev is None:
            divg_str = "—"
        else:
            price_higher = r["price"] > prev["price"]
            mvrv_lower   = r["mvrv"]  < prev["mvrv"]
            if price_higher and mvrv_lower:
                divg_str = "YES (Bearish Divg)"
            elif price_higher:
                divg_str = "price↑ MVRV↑ (no divg)"
            elif not price_higher:
                divg_str = "price↓ (not ATH)"
            else:
                divg_str = "—"

        print(f"  {r['name']:<30} {str(r['date'].date()):<12} "
              f"${r['price']:>11,.0f}  {r['mvrv']:>6.3f}  {r['sth_mvrv']:>9.4f}  {divg_str}")
        prev = r

    # Find first STH-MVRV < 1.10 and < 1.05 — in full daily data before LH
    mask = (df["date"] >= cfg["analysis_start"]) & (df["date"] <= lh_date)
    sub  = df[mask].copy()

    lt_dates = [x[1] for x in lt_list]
    first_lt = min(lt_dates)

    sub_post_first_lt = sub[sub["date"] >= first_lt]

    sub_110 = sub_post_first_lt[sub_post_first_lt["sth_mvrv"] < 1.10]
    sub_105 = sub_post_first_lt[sub_post_first_lt["sth_mvrv"] < 1.05]

    if not sub_110.empty:
        first_sth_below_110 = sub_110.iloc[0]["date"]
        days_110_to_lh = (lh_date - first_sth_below_110).days
        print(f"\n  STH-MVRV first < 1.10 : {first_sth_below_110.date()}  "
              f"(price ${sub_110.iloc[0]['btc_price']:,.0f})  → {days_110_to_lh}d to Lower High")
    else:
        days_110_to_lh = None
        print(f"\n  STH-MVRV never < 1.10 in this window")

    if not sub_105.empty:
        first_sth_below_105 = sub_105.iloc[0]["date"]
        days_105_to_lh = (lh_date - first_sth_below_105).days
        print(f"  STH-MVRV first < 1.05 : {first_sth_below_105.date()}  "
              f"(price ${sub_105.iloc[0]['btc_price']:,.0f})  → {days_105_to_lh}d to Lower High")
    else:
        days_105_to_lh = None
        print(f"  STH-MVRV never < 1.05 in this window")

    t2_results.append({
        "cycle": cycle,
        "first_sth_below_110": first_sth_below_110,
        "days_110_to_lh": days_110_to_lh,
        "first_sth_below_105": first_sth_below_105,
        "days_105_to_lh": days_105_to_lh,
    })


# ─── TRIGGER 3: SOPR Gap Peaked and Declining ────────────────────────────────

print("\n\n" + "=" * 70)
print("TRIGGER 3 — SOPR Gap Peaked and Declining (MA90 - MA90-MA60)")
print("=" * 70)

t3_results = []

for cycle, cfg in CYCLES.items():
    lh_date = cfg["lower_high_date"]
    start   = cfg["analysis_start"]
    cp_date = cfg["cycle_peak_date"]

    # Look at a wider window: analysis_start to lower_high + 60 for gap 20% calc
    mask = (df["date"] >= start) & (df["date"] <= lh_date + timedelta(days=60))
    sub  = df[mask].copy().reset_index(drop=True)

    # Drop NaN gap rows (need 90+60=150 days of sth_sopr history)
    sub_valid = sub[sub["sopr_gap"].notna()].copy()

    # Find local peak of gap BEFORE lower high
    sub_before_lh = sub_valid[sub_valid["date"] <= lh_date]

    if sub_before_lh.empty:
        print(f"\n[{cycle}] No valid gap data before Lower High")
        t3_results.append({"cycle": cycle})
        continue

    # Gap peak = maximum gap before lower high
    peak_idx  = sub_before_lh["sopr_gap"].idxmax()
    gap_peak_date = sub_before_lh.loc[peak_idx, "date"]
    gap_peak_val  = sub_before_lh.loc[peak_idx, "sopr_gap"]

    # Find when gap drops 20% from peak (sustained = stays below for 3 consecutive days)
    threshold = gap_peak_val * 0.80  # gap must drop to 80% of peak = 20% decline
    sub_after_peak = sub_valid[sub_valid["date"] > gap_peak_date].copy()

    signal_date_20 = None
    for i in range(len(sub_after_peak) - 2):
        chunk = sub_after_peak.iloc[i:i+3]
        if all(chunk["sopr_gap"] <= threshold):
            signal_date_20 = chunk.iloc[0]["date"]
            break

    print(f"\n[{cycle}]")
    print(f"  Gap peak date      : {gap_peak_date.date()}")
    print(f"  Gap peak value     : {gap_peak_val:.5f}")
    print(f"  20% decline thresh : {threshold:.5f}")

    if signal_date_20 is not None and signal_date_20 <= lh_date:
        days_to_lh = (lh_date - signal_date_20).days
        print(f"  Gap -20% signal    : {signal_date_20.date()}  → {days_to_lh}d to Lower High")
        t3_results.append({
            "cycle": cycle,
            "gap_peak_date": gap_peak_date,
            "gap_peak_val": gap_peak_val,
            "signal_20pct": signal_date_20,
            "days_to_lh": days_to_lh,
        })
    elif signal_date_20 is not None:
        print(f"  Gap -20% signal    : {signal_date_20.date()}  "
              f"(AFTER Lower High by {(signal_date_20 - lh_date).days}d — late signal)")
        t3_results.append({
            "cycle": cycle,
            "gap_peak_date": gap_peak_date,
            "gap_peak_val": gap_peak_val,
            "signal_20pct": signal_date_20,
            "days_to_lh": (lh_date - signal_date_20).days,  # negative
        })
    else:
        print(f"  Gap -20% sustained: NOT reached before lower high")
        t3_results.append({
            "cycle": cycle,
            "gap_peak_date": gap_peak_date,
            "gap_peak_val": gap_peak_val,
            "signal_20pct": None,
            "days_to_lh": None,
        })

    print(f"  Lower High actual  : {lh_date.date()}")

    # Show gap evolution around peak
    window_rows = sub_valid[
        (sub_valid["date"] >= gap_peak_date - timedelta(days=30)) &
        (sub_valid["date"] <= (signal_date_20 + timedelta(days=10) if signal_date_20 else lh_date))
    ]
    print(f"\n  Gap evolution (peak ±30d → signal):")
    print(f"  {'Date':<12}  {'STH-SOPR MA90':>14}  {'MA90-MA60':>10}  {'Gap':>8}  {'%Peak':>6}")
    for _, r in window_rows.iterrows():
        pct = (r["sopr_gap"] / gap_peak_val * 100) if gap_peak_val else 0
        marker = " ← PEAK" if r["date"] == gap_peak_date else \
                 " ← SIGNAL(-20%)" if (signal_date_20 and r["date"] == signal_date_20) else ""
        print(f"  {str(r['date'].date()):<12}  {r['sth_sopr_ma90']:>14.5f}  "
              f"{r['ma90_ma60']:>10.5f}  {r['sopr_gap']:>8.5f}  {pct:>5.1f}%{marker}")


# ─── SUMMARY TABLE ────────────────────────────────────────────────────────────

print("\n\n" + "=" * 70)
print("SUMMARY TABLE — K3 Stage 1 Trigger Signals")
print("=" * 70)
print(f"\n{'Cycle':<8} {'Trigger':<15} {'Signal Date':<14} {'Days to LH':>12}  Keterangan")
print("-" * 70)

all_rows = []

for r in t1_results:
    if r["streak_end_signal"]:
        row = (r["cycle"], "T1 AVIV Break", str(r["streak_end_signal"].date()),
               r["days_to_lower_high"],
               f"Streak {r['streak_length']}d, break = signal")
    else:
        row = (r["cycle"], "T1 AVIV Break", "N/A", None, "No clean streak/break found")
    all_rows.append(row)
    print(f"{row[0]:<8} {row[1]:<15} {row[2]:<14} {str(row[3]) if row[3] else 'N/A':>12}  {row[4]}")

print()

for r in t2_results:
    sig_date = str(r.get("first_sth_below_110").date()) if r.get("first_sth_below_110") else "N/A"
    days     = r.get("days_110_to_lh")
    row = (r["cycle"], "T2 STH-MVRV<1.10", sig_date, days, "First sustained cross below 1.10")
    all_rows.append(row)
    print(f"{row[0]:<8} {row[1]:<15} {row[2]:<14} {str(row[3]) if row[3] else 'N/A':>12}  {row[4]}")

print()

for r in t3_results:
    sig_date = str(r.get("signal_20pct").date()) if r.get("signal_20pct") else "N/A"
    days     = r.get("days_to_lh")
    row = (r["cycle"], "T3 Gap -20%",
           sig_date, days,
           f"Peak: {r['gap_peak_date'].date() if r.get('gap_peak_date') else 'N/A'}")
    all_rows.append(row)
    print(f"{row[0]:<8} {row[1]:<15} {row[2]:<14} {str(row[3]) if row[3] else 'N/A':>12}  {row[4]}")

# ─── LEAD TIME STATS ─────────────────────────────────────────────────────────

print("\n\n" + "=" * 70)
print("LEAD TIME STATS per Trigger")
print("=" * 70)

def stats_for(rows, trigger_keyword):
    relevant = [r for r in rows if trigger_keyword in r[1] and r[3] is not None]
    leads = [r[3] for r in relevant]
    if not leads:
        return None
    return {
        "n": len(leads),
        "avg": np.mean(leads),
        "min": min(leads),
        "max": max(leads),
        "std": np.std(leads),
        "values": leads,
    }

for t_name, keyword in [
    ("T1 — AVIV Upper Break", "T1"),
    ("T2 — STH-MVRV < 1.10", "T2 STH"),
    ("T3 — SOPR Gap -20%",   "T3"),
]:
    st = stats_for(all_rows, keyword)
    if st:
        print(f"\n{t_name}")
        print(f"  N = {st['n']}  |  Avg lead = {st['avg']:.0f}d  "
              f"|  Range = [{st['min']}d, {st['max']}d]  |  StdDev = {st['std']:.1f}d")
        print(f"  Per-cycle leads: {st['values']}")
    else:
        print(f"\n{t_name}: insufficient data")

print("\n\n[Catatan definitif:]")
print("  - '+Xd' = X hari SEBELUM lower high (early signal = bagus)")
print("  - '-Xd' = X hari SETELAH lower high (late signal = miss)")
print("  - 'Early' = lead time besar  |  'Reliable' = konsistensi (std dev kecil)")
