"""
Analisis F&G Cadence (90-day) untuk deteksi Lower High Confirmation
Cek false positive dan false negative vs event Lower High di data_momentum_events.csv
"""
import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────
fg = pd.read_csv("data_fg.csv", parse_dates=["date"])
fg = fg.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)

events = pd.read_csv("data_momentum_events.csv", parse_dates=["date"])
lower_high_rows = events[events["event"].str.contains("Lower High", na=False)].copy()

# ── Hitung F&G Cadence 90-day ───────────────────────────────────────────────
fg["cadence_90"] = fg["fg"] - fg["fg"].shift(90)

# Detect zero cross
fg["cadence_positive"] = (fg["cadence_90"] > 0).astype(bool)
prev_pos = fg["cadence_positive"].shift(1).fillna(False).astype(bool)
fg["zero_cross_down"] = prev_pos & ~fg["cadence_positive"]   # pos→neg (SELL)
fg["zero_cross_up"]   = ~prev_pos & fg["cadence_positive"]   # neg→pos (BUY)

print("=" * 70)
print("F&G CADENCE (90-DAY) — LOWER HIGH CONFIRMATION ANALYSIS")
print("=" * 70)

# ── Data availability check ─────────────────────────────────────────────────
fg_start = fg["date"].min()
cadence_valid_start = fg["date"].iloc[90]  # first date with valid 90-day lookback
print(f"\nF&G data mulai  : {fg_start.date()}")
print(f"Cadence valid   : {cadence_valid_start.date()} (setelah 90 hari lookback)")
print(f"F&G data sampai : {fg['date'].max().date()}")

# ── Summary Lower High events ───────────────────────────────────────────────
print("\n" + "─" * 70)
print("LOWER HIGH EVENTS DI DATA")
print("─" * 70)
for event_name, grp in lower_high_rows.groupby("event", sort=False):
    start = grp["date"].min()
    end   = grp["date"].max()
    price_peak = grp["btc_price"].max()
    coverable  = start >= cadence_valid_start
    print(f"  {event_name}")
    print(f"    Window   : {start.date()} → {end.date()}")
    print(f"    BTC Peak : ${price_peak:,.0f}")
    print(f"    Cadence  : {'AVAILABLE' if coverable else 'TIDAK ADA DATA (sebelum F&G start)'}")

# ── Per-event analisis mendalam ─────────────────────────────────────────────
analyzable_events = []
for event_name, grp in lower_high_rows.groupby("event", sort=False):
    start = grp["date"].min()
    end   = grp["date"].max()
    if start < cadence_valid_start:
        continue
    analyzable_events.append((event_name, start, end, grp["btc_price"].max()))

print("\n" + "─" * 70)
print("ANALISIS CADENCE SAAT LOWER HIGH TERJADI")
print("─" * 70)

WINDOW_BEFORE = 60   # hari sebelum event untuk cek lead time
WINDOW_AFTER  = 60   # hari sesudah event untuk cek lagging confirmation

for event_name, ev_start, ev_end, ev_price in analyzable_events:
    print(f"\n{'='*60}")
    print(f"EVENT: {event_name}  ({ev_start.date()} → {ev_end.date()})")
    print(f"BTC Peak: ${ev_price:,.0f}")

    # Ambil window data
    window_start = ev_start - pd.Timedelta(days=WINDOW_BEFORE)
    window_end   = ev_end   + pd.Timedelta(days=WINDOW_AFTER)
    w = fg[(fg["date"] >= window_start) & (fg["date"] <= window_end)].copy()

    # Cadence saat event
    ev_rows = w[(w["date"] >= ev_start) & (w["date"] <= ev_end)]
    cadence_at_event = ev_rows["cadence_90"].mean()
    cadence_min_event = ev_rows["cadence_90"].min()
    cadence_max_event = ev_rows["cadence_90"].max()
    cadence_trend = "NEGATIF" if cadence_at_event < 0 else "POSITIF"

    print(f"\nCadence saat event window:")
    print(f"  Mean  = {cadence_at_event:.1f}  |  Min = {cadence_min_event:.1f}  |  Max = {cadence_max_event:.1f}")
    print(f"  Status: {cadence_trend}")

    # Zero cross events dalam window
    crosses_in_window = w[w["zero_cross_down"] | w["zero_cross_up"]]
    if len(crosses_in_window) > 0:
        print(f"\nZero crosses dalam window ({window_start.date()} → {window_end.date()}):")
        for _, row in crosses_in_window.iterrows():
            cross_type = "POS→NEG (bearish)" if row["zero_cross_down"] else "NEG→POS (bullish)"
            days_from_event = (row["date"] - ev_start).days
            rel = f"{abs(days_from_event)}d {'SEBELUM' if days_from_event < 0 else 'SETELAH'} event start"
            print(f"  {row['date'].date()}  [{cross_type}]  cadence={row['cadence_90']:.1f}  ({rel})")
    else:
        print(f"\n  Tidak ada zero cross dalam window ±{WINDOW_BEFORE}/{WINDOW_AFTER} hari")

    # Lead time: berapa hari sebelum event cadence sudah negatif
    pre_window = w[w["date"] < ev_start]
    if len(pre_window) > 0:
        neg_before = pre_window[pre_window["cadence_90"] < 0]
        if len(neg_before) > 0:
            earliest_neg = neg_before["date"].min()
            lead = (ev_start - earliest_neg).days
            print(f"\nCadence negatif pertama kali: {earliest_neg.date()} ({lead} hari sebelum event)")
        else:
            print(f"\nCadence POSITIF sepanjang pre-window — tidak ada lead warning")

    # Print tabel cadence harian sekitar event
    print(f"\nTabel harian {WINDOW_BEFORE}d sebelum → event → {WINDOW_AFTER}d sesudah:")
    print(f"  {'Date':<12} {'F&G':>5} {'Cadence':>9} {'ZeroCross':<20} {'Note'}")
    print(f"  {'─'*65}")
    for _, row in w.iterrows():
        note = ""
        if ev_start <= row["date"] <= ev_end:
            note = "◄ EVENT WINDOW"
        cross = ""
        if row["zero_cross_down"]:
            cross = "▼ POS→NEG"
        elif row["zero_cross_up"]:
            cross = "▲ NEG→POS"
        cadence_str = f"{row['cadence_90']:+.1f}" if not pd.isna(row["cadence_90"]) else "N/A"
        print(f"  {str(row['date'].date()):<12} {row['fg']:>5.0f} {cadence_str:>9} {cross:<20} {note}")

# ── False Positive analysis ─────────────────────────────────────────────────
# False Positive = Cadence cross neg tapi bukan Lower High event
print("\n" + "=" * 70)
print("FALSE POSITIVE ANALYSIS")
print("Cadence zero cross POS→NEG yang TIDAK BERTEPATAN dengan Lower High")
print("=" * 70)

# Define Lower High windows (expanded ±30 days)
lh_windows = []
for event_name, grp in lower_high_rows.groupby("event", sort=False):
    start = grp["date"].min() - pd.Timedelta(days=30)
    end   = grp["date"].max() + pd.Timedelta(days=30)
    lh_windows.append((start, end, event_name))

def is_near_lower_high(date):
    for s, e, name in lh_windows:
        if s <= date <= e:
            return name
    return None

bearish_crosses = fg[fg["zero_cross_down"] & (fg["date"] >= cadence_valid_start)].copy()
print(f"\nTotal bearish zero cross (POS→NEG) sejak {cadence_valid_start.date()}: {len(bearish_crosses)}")
print()

fp_count = 0
tp_count = 0
for _, row in bearish_crosses.iterrows():
    near_lh = is_near_lower_high(row["date"])
    label = "TRUE POSITIVE (near LH)" if near_lh else "FALSE POSITIVE"
    if near_lh:
        tp_count += 1
    else:
        fp_count += 1
    lh_note = f"  → {near_lh}" if near_lh else ""
    print(f"  {row['date'].date()}  cadence={row['cadence_90']:+.1f}  fg={row['fg']:.0f}  [{label}]{lh_note}")

print(f"\nTrue Positive  : {tp_count}")
print(f"False Positive : {fp_count}")
if len(bearish_crosses) > 0:
    print(f"Precision      : {tp_count/len(bearish_crosses)*100:.0f}% (bearish cross yang memang Lower High)")

# ── False Negative analysis ─────────────────────────────────────────────────
print("\n" + "=" * 70)
print("FALSE NEGATIVE ANALYSIS")
print("Lower High events yang TIDAK DIKONFIRMASI oleh bearish zero cross (±30d)")
print("=" * 70)

for event_name, ev_start, ev_end, ev_price in analyzable_events:
    # Cek ada bearish cross dalam ±30 hari dari event
    check_start = ev_start - pd.Timedelta(days=30)
    check_end   = ev_end   + pd.Timedelta(days=30)
    nearby_cross = fg[fg["zero_cross_down"] & (fg["date"] >= check_start) & (fg["date"] <= check_end)]
    if len(nearby_cross) > 0:
        dates = [str(r["date"].date()) for _, r in nearby_cross.iterrows()]
        print(f"  ✓ CONFIRMED  | {event_name}  → cross pada: {', '.join(dates)}")
    else:
        # Check cadence state saat event
        ev_cadence = fg[(fg["date"] >= ev_start) & (fg["date"] <= ev_end)]["cadence_90"].mean()
        print(f"  ✗ MISSED     | {event_name}  (cadence avg saat event = {ev_cadence:+.1f})")

# ── Composite filter check (seperti di video) ───────────────────────────────
print("\n" + "=" * 70)
print("COMPOSITE FILTER CHECK (seperti Composite Strategy di video)")
print("Bearish cross VALID jika: cadence neg + F&G < 50 (opsional filter)")
print("=" * 70)
for _, row in bearish_crosses.iterrows():
    fg_val = row["fg"]
    cadence_val = row["cadence_90"]
    filter_pass = fg_val < 50  # sentimen sudah elevated sebelumnya = more meaningful
    near_lh = is_near_lower_high(row["date"])
    print(f"  {row['date'].date()}  fg={fg_val:.0f}  cadence={cadence_val:+.1f}  filter={'PASS' if filter_pass else 'FAIL'}  lh={'YES' if near_lh else 'NO'}")

print("\n✓ Analisis selesai.")
