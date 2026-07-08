"""
F&G Cadence (90D) crossing SMA60 dan SMA90
Cek apakah cross ini lebih presisi untuk exit timing di Lower High confirmation
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
import numpy as np

# ── Load data ──────────────────────────────────────────────────────────────
fg = pd.read_csv("data_fg.csv", parse_dates=["date"])
fg = fg.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)

events = pd.read_csv("data_momentum_events.csv", parse_dates=["date"])
lh_rows = events[events["event"].str.contains("Lower High", na=False)].copy()

# ── Hitung Cadence dan SMA ─────────────────────────────────────────────────
fg["cadence"]   = fg["fg"] - fg["fg"].shift(90)
fg["sma60"]     = fg["cadence"].rolling(60).mean()
fg["sma90"]     = fg["cadence"].rolling(90).mean()

# Cadence valid setelah 90 hari; SMA60 valid setelah 90+60=150 hari; SMA90 valid setelah 90+90=180 hari
cadence_start = fg.loc[fg["cadence"].notna(), "date"].min()
sma60_start   = fg.loc[fg["sma60"].notna(), "date"].min()
sma90_start   = fg.loc[fg["sma90"].notna(), "date"].min()

# ── Deteksi crosses (cadence crossing SMA) ─────────────────────────────────
def detect_cross_down(series, ref, label):
    """Deteksi saat series turun melewati ref (dari atas ke bawah)."""
    above = series > ref
    cross_down = above.shift(1).fillna(False) & ~above
    return cross_down

def detect_cross_up(series, ref, label):
    above = series > ref
    cross_up = ~above.shift(1).fillna(True) & above
    return cross_up

fg["cross_below_sma60"] = detect_cross_down(fg["cadence"], fg["sma60"], "sma60")
fg["cross_above_sma60"] = detect_cross_up(fg["cadence"], fg["sma60"], "sma60")
fg["cross_below_sma90"] = detect_cross_down(fg["cadence"], fg["sma90"], "sma90")
fg["cross_above_sma90"] = detect_cross_up(fg["cadence"], fg["sma90"], "sma90")

# ── Helper: cek apakah date dekat Lower High (±30 hari) ────────────────────
lh_windows = []
for name, grp in lh_rows.groupby("event", sort=False):
    s = grp["date"].min() - pd.Timedelta(days=30)
    e = grp["date"].max() + pd.Timedelta(days=30)
    lh_windows.append((s, e, name))

def near_lh(date):
    for s, e, name in lh_windows:
        if s <= date <= e:
            return name
    return None

# ── Summary function ────────────────────────────────────────────────────────
def analyze_cross(signal_col, label, valid_start):
    signals = fg[fg[signal_col] & (fg["date"] >= valid_start)].copy()
    tp, fp = 0, 0
    rows = []
    for _, row in signals.iterrows():
        lh = near_lh(row["date"])
        if lh:
            tp += 1
        else:
            fp += 1
        rows.append({
            "date": row["date"].date(),
            "fg": int(row["fg"]),
            "cadence": round(row["cadence"], 1),
            "sma_val": round(row[label] if label in row else 0, 1),
            "near_lh": lh or ""
        })
    precision = tp / len(signals) * 100 if signals.shape[0] > 0 else 0
    return signals, rows, tp, fp, precision

# ── Print ──────────────────────────────────────────────────────────────────
SEP = "=" * 70
sep = "-" * 70

print(SEP)
print("F&G CADENCE CROSSING SMA60 / SMA90 — EXIT TIMING ANALYSIS")
print(SEP)
print(f"\nCadence valid  : {cadence_start.date()}")
print(f"SMA60 valid    : {sma60_start.date()}")
print(f"SMA90 valid    : {sma90_start.date()}")
print(f"F&G data s/d   : {fg['date'].max().date()}")

# Lower High events yang bisa dianalisis
print(f"\n{sep}")
print("LOWER HIGH EVENTS (target detection)")
print(sep)
analyzable = []
for name, grp in lh_rows.groupby("event", sort=False):
    start = grp["date"].min()
    end   = grp["date"].max()
    price = grp["btc_price"].max()
    ok60  = start >= sma60_start
    ok90  = start >= sma90_start
    print(f"  {name}")
    print(f"    Window: {start.date()} -> {end.date()}  |  BTC ${price:,.0f}")
    print(f"    SMA60: {'OK' if ok60 else 'NO DATA'}  |  SMA90: {'OK' if ok90 else 'NO DATA'}")
    if ok60:
        analyzable.append((name, start, end, price))

# ── Per-event deep dive ────────────────────────────────────────────────────
print(f"\n{SEP}")
print("DETAIL PER LOWER HIGH EVENT")
print(SEP)

WINDOW = 60  # hari sebelum/sesudah

for name, ev_start, ev_end, ev_price in analyzable:
    ws = ev_start - pd.Timedelta(days=WINDOW)
    we = ev_end   + pd.Timedelta(days=WINDOW)
    w  = fg[(fg["date"] >= ws) & (fg["date"] <= we)].copy()

    print(f"\n{'='*60}")
    print(f"EVENT: {name}")
    print(f"Window: {ev_start.date()} -> {ev_end.date()}  |  BTC ${ev_price:,.0f}")

    # Cadence & SMA saat event
    ev = w[(w["date"] >= ev_start) & (w["date"] <= ev_end)]
    print(f"\nNilai saat event window:")
    print(f"  Cadence  : mean={ev['cadence'].mean():.1f}  min={ev['cadence'].min():.1f}  max={ev['cadence'].max():.1f}")
    print(f"  SMA60    : mean={ev['sma60'].mean():.1f}")
    print(f"  SMA90    : mean={ev['sma90'].mean():.1f}")
    c_vs_60 = "CADENCE < SMA60" if ev["cadence"].mean() < ev["sma60"].mean() else "CADENCE > SMA60"
    c_vs_90 = "CADENCE < SMA90" if ev["cadence"].mean() < ev["sma90"].mean() else "CADENCE > SMA90"
    print(f"  Posisi   : {c_vs_60}  |  {c_vs_90}")

    # Cross events dalam window
    crosses = w[
        w["cross_below_sma60"] | w["cross_above_sma60"] |
        w["cross_below_sma90"] | w["cross_above_sma90"]
    ]
    if len(crosses) > 0:
        print(f"\nCross events dalam window ({ws.date()} -> {we.date()}):")
        for _, row in crosses.iterrows():
            signals = []
            if row["cross_below_sma60"]: signals.append("CADENCE < SMA60 [BEARISH]")
            if row["cross_above_sma60"]: signals.append("CADENCE > SMA60 [BULLISH]")
            if row["cross_below_sma90"]: signals.append("CADENCE < SMA90 [BEARISH]")
            if row["cross_above_sma90"]: signals.append("CADENCE > SMA90 [BULLISH]")
            days_rel = (row["date"] - ev_start).days
            rel_str  = f"{abs(days_rel)}d {'SEBELUM' if days_rel < 0 else 'SETELAH'} event"
            print(f"  {row['date'].date()}  cadence={row['cadence']:+.1f}  sma60={row['sma60']:.1f}  sma90={row['sma90']:.1f}  ({rel_str})")
            for s in signals:
                print(f"           -> {s}")
    else:
        print(f"\n  Tidak ada cross events dalam window")

    # Tabel harian
    print(f"\nTabel harian (setiap 5 hari untuk ringkas):")
    print(f"  {'Date':<12} {'F&G':>4} {'Cadence':>8} {'SMA60':>7} {'SMA90':>7} {'Signal':<35} {'Note'}")
    print(f"  {'─'*85}")
    for _, row in w.iterrows():
        signals = []
        if row["cross_below_sma60"]: signals.append("< SMA60[BEAR]")
        if row["cross_above_sma60"]: signals.append("> SMA60[BULL]")
        if row["cross_below_sma90"]: signals.append("< SMA90[BEAR]")
        if row["cross_above_sma90"]: signals.append("> SMA90[BULL]")
        note = "EVENT" if ev_start <= row["date"] <= ev_end else ""
        sig_str = "  ".join(signals)
        if signals or note or (ev_start - pd.Timedelta(days=5) <= row["date"] <= ev_end + pd.Timedelta(days=5)):
            sma60_str = f"{row['sma60']:.1f}" if not pd.isna(row["sma60"]) else "N/A"
            sma90_str = f"{row['sma90']:.1f}" if not pd.isna(row["sma90"]) else "N/A"
            print(f"  {str(row['date'].date()):<12} {row['fg']:>4.0f} {row['cadence']:>+8.1f} {sma60_str:>7} {sma90_str:>7} {sig_str:<35} {note}")

# ── False Positive Comparison ──────────────────────────────────────────────
print(f"\n{SEP}")
print("FALSE POSITIVE COMPARISON: Raw ZeroCross vs SMA60 Cross vs SMA90 Cross")
print(SEP)

# Baseline: raw zero cross (dari analisis sebelumnya)
fg["cadence_pos"] = (fg["cadence"] > 0).astype(bool)
prev_pos = fg["cadence_pos"].shift(1).fillna(False).astype(bool)
fg["raw_zero_cross_down"] = prev_pos & ~fg["cadence_pos"]

raw_signals = fg[fg["raw_zero_cross_down"] & (fg["date"] >= cadence_start)]
raw_tp = sum(1 for _, r in raw_signals.iterrows() if near_lh(r["date"]))
raw_fp = len(raw_signals) - raw_tp

sma60_signals = fg[fg["cross_below_sma60"] & (fg["date"] >= sma60_start)]
s60_tp = sum(1 for _, r in sma60_signals.iterrows() if near_lh(r["date"]))
s60_fp = len(sma60_signals) - s60_tp

sma90_signals = fg[fg["cross_below_sma90"] & (fg["date"] >= sma90_start)]
s90_tp = sum(1 for _, r in sma90_signals.iterrows() if near_lh(r["date"]))
s90_fp = len(sma90_signals) - s90_tp

print(f"\n{'Method':<30} {'Total':>6} {'TP':>5} {'FP':>5} {'Precision':>10} {'FP Rate':>8}")
print(f"{'─'*65}")
for label, total, tp, fp in [
    ("Raw Zero Cross",         len(raw_signals),  raw_tp,  raw_fp),
    ("Cadence cross < SMA60",  len(sma60_signals), s60_tp, s60_fp),
    ("Cadence cross < SMA90",  len(sma90_signals), s90_tp, s90_fp),
]:
    prec = f"{tp/total*100:.0f}%" if total > 0 else "N/A"
    fpr  = f"{fp/total*100:.0f}%" if total > 0 else "N/A"
    print(f"  {label:<28} {total:>6} {tp:>5} {fp:>5} {prec:>10} {fpr:>8}")

# ── Detail semua SMA60 bearish crosses ───────────────────────────────────
print(f"\n{sep}")
print("SEMUA BEARISH CROSSES: Cadence < SMA60")
print(sep)
print(f"\n  {'Date':<12} {'F&G':>4} {'Cadence':>8} {'SMA60':>7} {'Near LH?'}")
print(f"  {'─'*55}")
for _, row in sma60_signals.iterrows():
    lh = near_lh(row["date"])
    mark = f"<< {lh}" if lh else ""
    print(f"  {str(row['date'].date()):<12} {row['fg']:>4.0f} {row['cadence']:>+8.1f} {row['sma60']:>7.1f}  {mark}")

print(f"\n{sep}")
print("SEMUA BEARISH CROSSES: Cadence < SMA90")
print(sep)
print(f"\n  {'Date':<12} {'F&G':>4} {'Cadence':>8} {'SMA90':>7} {'Near LH?'}")
print(f"  {'─'*55}")
for _, row in sma90_signals.iterrows():
    lh = near_lh(row["date"])
    mark = f"<< {lh}" if lh else ""
    print(f"  {str(row['date'].date()):<12} {row['fg']:>4.0f} {row['cadence']:>+8.1f} {row['sma90']:>7.1f}  {mark}")

# ── False Negative: Lower Highs yang missed ──────────────────────────────
print(f"\n{SEP}")
print("FALSE NEGATIVE: Lower High yang tidak dikonfirmasi cross (+-30d)")
print(SEP)
print("\nSMA60 Cross:")
for name, ev_start, ev_end, _ in analyzable:
    ws = ev_start - pd.Timedelta(days=30)
    we = ev_end   + pd.Timedelta(days=30)
    hits = sma60_signals[(sma60_signals["date"] >= ws) & (sma60_signals["date"] <= we)]
    if len(hits) > 0:
        dates = [str(r["date"].date()) for _, r in hits.iterrows()]
        print(f"  CONFIRMED  | {name} -> cross: {', '.join(dates)}")
    else:
        ev_cadence = fg[(fg["date"] >= ev_start) & (fg["date"] <= ev_end)]["cadence"].mean()
        ev_sma60   = fg[(fg["date"] >= ev_start) & (fg["date"] <= ev_end)]["sma60"].mean()
        print(f"  MISSED     | {name}  (cadence={ev_cadence:.1f}, sma60={ev_sma60:.1f})")

print("\nSMA90 Cross:")
for name, ev_start, ev_end, _ in analyzable:
    ws = ev_start - pd.Timedelta(days=30)
    we = ev_end   + pd.Timedelta(days=30)
    hits = sma90_signals[(sma90_signals["date"] >= ws) & (sma90_signals["date"] <= we)]
    if len(hits) > 0:
        dates = [str(r["date"].date()) for _, r in hits.iterrows()]
        print(f"  CONFIRMED  | {name} -> cross: {', '.join(dates)}")
    else:
        ev_cadence = fg[(fg["date"] >= ev_start) & (fg["date"] <= ev_end)]["cadence"].mean()
        ev_sma90   = fg[(fg["date"] >= ev_start) & (fg["date"] <= ev_end)]["sma90"].mean()
        print(f"  MISSED     | {name}  (cadence={ev_cadence:.1f}, sma90={ev_sma90:.1f})")

# ── State sekarang ──────────────────────────────────────────────────────────
today_row = fg.iloc[-1]
print(f"\n{SEP}")
print("STATE SEKARANG (data terbaru)")
print(SEP)
print(f"\nDate    : {today_row['date'].date()}")
print(f"F&G     : {today_row['fg']:.0f}")
print(f"Cadence : {today_row['cadence']:+.1f}")
print(f"SMA60   : {today_row['sma60']:.1f}")
print(f"SMA90   : {today_row['sma90']:.1f}")
c60 = "BELOW SMA60" if today_row["cadence"] < today_row["sma60"] else "ABOVE SMA60"
c90 = "BELOW SMA90" if today_row["cadence"] < today_row["sma90"] else "ABOVE SMA90"
print(f"Status  : Cadence {c60}  |  Cadence {c90}")

# Recent 30 days
print(f"\nTabel 30 hari terakhir:")
print(f"  {'Date':<12} {'F&G':>4} {'Cadence':>8} {'SMA60':>7} {'SMA90':>7} {'Signal'}")
print(f"  {'─'*65}")
last30 = fg.tail(30)
for _, row in last30.iterrows():
    sigs = []
    if row["cross_below_sma60"]: sigs.append("BEAR<SMA60")
    if row["cross_above_sma60"]: sigs.append("BULL>SMA60")
    if row["cross_below_sma90"]: sigs.append("BEAR<SMA90")
    if row["cross_above_sma90"]: sigs.append("BULL>SMA90")
    print(f"  {str(row['date'].date()):<12} {row['fg']:>4.0f} {row['cadence']:>+8.1f} {row['sma60']:>7.1f} {row['sma90']:>7.1f} {'  '.join(sigs)}")

print("\nSelesai.")
