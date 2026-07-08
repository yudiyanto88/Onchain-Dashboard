"""
Grid search: best SMA_fast vs SMA_slow pair pada F&G Cadence (90D)
untuk deteksi Lower High confirmation
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
import numpy as np
from itertools import combinations

# ── Load ───────────────────────────────────────────────────────────────────
fg = pd.read_csv("data_fg.csv", parse_dates=["date"])
fg = fg.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)

events = pd.read_csv("data_momentum_events.csv", parse_dates=["date"])
lh_rows = events[events["event"].str.contains("Lower High", na=False)].copy()

fg["cadence"] = fg["fg"] - fg["fg"].shift(90)

# ── Lower High windows ─────────────────────────────────────────────────────
LH_MARGIN = 30   # hari tolerance

lh_windows = []
for name, grp in lh_rows.groupby("event", sort=False):
    s = grp["date"].min()
    e = grp["date"].max()
    lh_windows.append((s, e, name))

def near_lh(date):
    for s, e, _ in lh_windows:
        if (s - pd.Timedelta(days=LH_MARGIN)) <= date <= (e + pd.Timedelta(days=LH_MARGIN)):
            return True
    return False

def lh_confirmed_by(signal_dates, margin=LH_MARGIN):
    """Berapa LH events yang punya setidaknya satu signal dalam margin hari."""
    confirmed = 0
    for s, e, _ in lh_windows:
        ws = s - pd.Timedelta(days=margin)
        we = e + pd.Timedelta(days=margin)
        if any(ws <= d <= we for d in signal_dates):
            confirmed += 1
    return confirmed

# ── Grid ───────────────────────────────────────────────────────────────────
SMA_RANGE = [5, 10, 15, 20, 30, 45, 60, 75, 90, 120, 150]

results = []

for fast in SMA_RANGE:
    for slow in SMA_RANGE:
        if slow <= fast:
            continue

        # Compute SMAs
        fg[f"s{fast}"] = fg["cadence"].rolling(fast).mean()
        fg[f"s{slow}"] = fg["cadence"].rolling(slow).mean()

        valid = fg.dropna(subset=[f"s{fast}", f"s{slow}"]).copy()
        valid_start = valid["date"].min()

        # Only analyze LH events that fall within valid data range
        analyzable_lh = [(s, e, n) for s, e, n in lh_windows if s >= valid_start]
        n_lh = len(analyzable_lh)
        if n_lh == 0:
            continue

        # Detect bear cross: SMA_fast crosses BELOW SMA_slow
        above = (valid[f"s{fast}"] > valid[f"s{slow}"]).astype(bool)
        prev  = above.shift(1).fillna(False).astype(bool)
        cross_bear = valid[prev & ~above]["date"].tolist()

        if len(cross_bear) == 0:
            continue

        tp = sum(1 for d in cross_bear if near_lh(d))
        fp = len(cross_bear) - tp
        confirmed = lh_confirmed_by(cross_bear)
        fn = n_lh - confirmed

        precision = tp / len(cross_bear) if len(cross_bear) > 0 else 0
        recall    = confirmed / n_lh if n_lh > 0 else 0
        f1        = (2 * precision * recall / (precision + recall)
                     if (precision + recall) > 0 else 0)

        results.append({
            "fast":      fast,
            "slow":      slow,
            "total":     len(cross_bear),
            "tp":        tp,
            "fp":        fp,
            "confirmed": confirmed,
            "n_lh":      n_lh,
            "fn":        fn,
            "precision": round(precision, 4),
            "recall":    round(recall, 4),
            "f1":        round(f1, 4),
        })

        # Cleanup temp cols
        fg.drop(columns=[f"s{fast}", f"s{slow}"], errors="ignore", inplace=True)

df = pd.DataFrame(results).sort_values(["f1","precision","recall"],
                                        ascending=False).reset_index(drop=True)

# ── Print results ──────────────────────────────────────────────────────────
print("=" * 75)
print("GRID SEARCH: SMA_fast vs SMA_slow pada F&G Cadence (90D)")
print("Signal: SMA_fast crosses BELOW SMA_slow  →  Lower High detection")
print(f"LH margin: ±{LH_MARGIN} hari")
print("=" * 75)

print(f"\nTotal pairs tested: {len(df)}")
print(f"LH events analyzable: {df['n_lh'].max()} (excl. LH 2018 — no F&G data)\n")

print(f"{'Rank':<5} {'fast':>5} {'slow':>5} {'total':>7} {'TP':>4} "
      f"{'FP':>4} {'Conf':>5} {'Prec':>7} {'Recall':>7} {'F1':>7}")
print("-" * 65)
for i, row in df.head(30).iterrows():
    print(f"  {i+1:<4} {row['fast']:>5} {row['slow']:>5} {row['total']:>7} "
          f"{row['tp']:>4} {row['fp']:>4} {row['confirmed']:>5} "
          f"{row['precision']:>7.1%} {row['recall']:>7.1%} {row['f1']:>7.3f}")

# ── Filter: recall = 100% (tidak ada false negative) ──────────────────────
full_recall = df[df["recall"] == 1.0].sort_values(
    ["precision","f1"], ascending=False)

print(f"\n{'='*65}")
print("PAIRS DENGAN RECALL 100% (tidak ada LH yang terlewat)")
print(f"{'='*65}")
print(f"\n{'Rank':<5} {'fast':>5} {'slow':>5} {'total':>7} {'TP':>4} "
      f"{'FP':>4} {'Prec':>7} {'F1':>7}")
print("-" * 55)
for i, (_, row) in enumerate(full_recall.head(20).iterrows()):
    print(f"  {i+1:<4} {row['fast']:>5} {row['slow']:>5} {row['total']:>7} "
          f"{row['tp']:>4} {row['fp']:>4} {row['precision']:>7.1%} {row['f1']:>7.3f}")

# ── Best pair detail ───────────────────────────────────────────────────────
best = df.iloc[0]
print(f"\n{'='*65}")
print(f"BEST PAIR: SMA{int(best['fast'])} vs SMA{int(best['slow'])}")
print(f"{'='*65}")
print(f"  F1={best['f1']:.3f}  Precision={best['precision']:.1%}  "
      f"Recall={best['recall']:.1%}")
print(f"  Total signals={int(best['total'])}  TP={int(best['tp'])}  "
      f"FP={int(best['fp'])}  Confirmed LH={int(best['confirmed'])}/{int(best['n_lh'])}")

# Show signal dates for best pair
bfast, bslow = int(best["fast"]), int(best["slow"])
fg[f"sb{bfast}"] = fg["cadence"].rolling(bfast).mean()
fg[f"sb{bslow}"] = fg["cadence"].rolling(bslow).mean()
v2 = fg.dropna(subset=[f"sb{bfast}", f"sb{bslow}"]).copy()
above2 = (v2[f"sb{bfast}"] > v2[f"sb{bslow}"]).astype(bool)
prev2  = above2.shift(1).fillna(False).astype(bool)
bear2  = v2[prev2 & ~above2]

print(f"\n  Signal dates:")
for _, row in bear2.iterrows():
    lh = near_lh(row["date"])
    tag = "  << NEAR LOWER HIGH" if lh else ""
    print(f"    {str(row['date'].date())}  "
          f"sma{bfast}={row[f'sb{bfast}']:.1f}  "
          f"sma{bslow}={row[f'sb{bslow}']:.1f}{tag}")

# ── Best with full recall detail ──────────────────────────────────────────
if len(full_recall) > 0:
    best_fr = full_recall.iloc[0]
    bfr_fast, bfr_slow = int(best_fr["fast"]), int(best_fr["slow"])
    print(f"\n{'='*65}")
    print(f"BEST PAIR (RECALL 100%): SMA{bfr_fast} vs SMA{bfr_slow}")
    print(f"{'='*65}")
    print(f"  F1={best_fr['f1']:.3f}  Precision={best_fr['precision']:.1%}  "
          f"Recall=100%")
    print(f"  Total signals={int(best_fr['total'])}  TP={int(best_fr['tp'])}  "
          f"FP={int(best_fr['fp'])}")

    fg[f"sc{bfr_fast}"] = fg["cadence"].rolling(bfr_fast).mean()
    fg[f"sc{bfr_slow}"] = fg["cadence"].rolling(bfr_slow).mean()
    v3 = fg.dropna(subset=[f"sc{bfr_fast}", f"sc{bfr_slow}"]).copy()
    above3 = (v3[f"sc{bfr_fast}"] > v3[f"sc{bfr_slow}"]).astype(bool)
    prev3  = above3.shift(1).fillna(False).astype(bool)
    bear3  = v3[prev3 & ~above3]

    print(f"\n  Signal dates:")
    for _, row in bear3.iterrows():
        lh = near_lh(row["date"])
        tag = "  << NEAR LOWER HIGH" if lh else ""
        print(f"    {str(row['date'].date())}  "
              f"sma{bfr_fast}={row[f'sc{bfr_fast}']:.1f}  "
              f"sma{bfr_slow}={row[f'sc{bfr_slow}']:.1f}{tag}")

print("\nSelesai.")
