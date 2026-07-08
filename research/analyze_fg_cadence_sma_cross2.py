"""
F&G Cadence (90D) — SMA60 vs SMA90 crossover analysis + chart
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D

# ── Load data ──────────────────────────────────────────────────────────────
fg = pd.read_csv("data_fg.csv", parse_dates=["date"])
fg = fg.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)

events = pd.read_csv("data_momentum_events.csv", parse_dates=["date"])
lh_rows = events[events["event"].str.contains("Lower High", na=False)].copy()

# ── Compute Cadence + SMAs ─────────────────────────────────────────────────
fg["cadence"]   = fg["fg"] - fg["fg"].shift(90)
fg["sma60"]     = fg["cadence"].rolling(60).mean()
fg["sma90"]     = fg["cadence"].rolling(90).mean()

# Valid start (need 90+90 = 180 days minimum for sma90 to be valid)
valid = fg.dropna(subset=["sma60", "sma90"]).copy()

# ── Detect SMA60 vs SMA90 crossovers ──────────────────────────────────────
valid["sma60_above"] = valid["sma60"] > valid["sma90"]
prev_above = valid["sma60_above"].shift(1).fillna(False)

valid["cross_bear"] = prev_above & ~valid["sma60_above"]   # SMA60 crosses BELOW SMA90 → bearish
valid["cross_bull"] = ~prev_above & valid["sma60_above"]   # SMA60 crosses ABOVE SMA90 → bullish

bear_crosses = valid[valid["cross_bear"]].copy()
bull_crosses = valid[valid["cross_bull"]].copy()

# ── Lower High windows ─────────────────────────────────────────────────────
lh_windows = []
for name, grp in lh_rows.groupby("event", sort=False):
    s = grp["date"].min()
    e = grp["date"].max()
    lh_windows.append((s, e, name))

def near_lh(date, margin=30):
    for s, e, name in lh_windows:
        if (s - pd.Timedelta(days=margin)) <= date <= (e + pd.Timedelta(days=margin)):
            return name
    return None

# ── Stats ──────────────────────────────────────────────────────────────────
print("=" * 65)
print("SMA60 vs SMA90 CROSSOVER — STATS")
print("=" * 65)
print(f"\nData range : {valid['date'].min().date()} -> {valid['date'].max().date()}")
print(f"Bear cross (SMA60 < SMA90): {len(bear_crosses)}")
print(f"Bull cross (SMA60 > SMA90): {len(bull_crosses)}")

tp, fp = 0, 0
print("\nBear crosses detail:")
print(f"  {'Date':<12} {'Cadence':>8} {'SMA60':>7} {'SMA90':>7}  Near LH?")
print(f"  {'─'*55}")
for _, row in bear_crosses.iterrows():
    lh = near_lh(row["date"])
    tag = f"<< {lh}" if lh else ""
    if lh: tp += 1
    else:   fp += 1
    print(f"  {str(row['date'].date()):<12} {row['cadence']:>+8.1f} {row['sma60']:>7.1f} {row['sma90']:>7.1f}  {tag}")

print(f"\nTrue Positive  : {tp}")
print(f"False Positive : {fp}")
if len(bear_crosses) > 0:
    print(f"Precision      : {tp/len(bear_crosses)*100:.0f}%")

# False negatives
print("\nFalse Negative check (±30d):")
analyzable = [(n, s, e) for s, e, n in lh_windows if s >= valid["date"].min()]
for name, ev_s, ev_e in analyzable:
    ws = ev_s - pd.Timedelta(days=30)
    we = ev_e + pd.Timedelta(days=30)
    hits = bear_crosses[(bear_crosses["date"] >= ws) & (bear_crosses["date"] <= we)]
    if len(hits) > 0:
        dates = [str(r["date"].date()) for _, r in hits.iterrows()]
        lead  = [(ev_s - r["date"]).days for _, r in hits.iterrows()]
        info  = ", ".join(f"{d} ({l}d before)" if l > 0 else f"{d} ({-l}d after)" for d, l in zip(dates, lead))
        print(f"  CONFIRMED | {name} -> {info}")
    else:
        print(f"  MISSED    | {name}")

print(f"\nState sekarang ({valid.iloc[-1]['date'].date()}):")
last = valid.iloc[-1]
print(f"  Cadence={last['cadence']:+.1f}  SMA60={last['sma60']:.1f}  SMA90={last['sma90']:.1f}")
pos = "SMA60 ABOVE SMA90 (bullish)" if last["sma60"] > last["sma90"] else "SMA60 BELOW SMA90 (bearish)"
print(f"  Posisi: {pos}")

# ── CHART ─────────────────────────────────────────────────────────────────
# Plot full history (from valid start)
fig, axes = plt.subplots(3, 1, figsize=(18, 13),
                          gridspec_kw={"height_ratios": [2.5, 2.5, 1]},
                          facecolor="#0d1117")
fig.suptitle("F&G Cadence (90D) — SMA60 vs SMA90 Crossover\nLower High Confirmation Signal",
             color="white", fontsize=14, fontweight="bold", y=0.98)

for ax in axes:
    ax.set_facecolor("#0d1117")
    ax.tick_params(colors="gray", labelsize=8)
    ax.spines[["top","right","left","bottom"]].set_color("#30363d")
    ax.grid(axis="y", color="#21262d", linewidth=0.5, linestyle="--")
    ax.grid(axis="x", color="#21262d", linewidth=0.3, linestyle=":")

ax1, ax2, ax3 = axes

# ── Panel 1: BTC price (from momentum events) ─────────────────────────────
btc = events[["date","btc_price"]].dropna().sort_values("date")
btc = btc[btc["date"] >= valid["date"].min()]

ax1.plot(btc["date"], btc["btc_price"], color="#58a6ff", linewidth=1.0, alpha=0.85, label="BTC Price")
ax1.set_yscale("log")
ax1.set_ylabel("BTC Price (log)", color="gray", fontsize=8)
ax1.yaxis.label.set_color("gray")

# Mark Lower High events on price
for s, e, name in lh_windows:
    if s < valid["date"].min():
        continue
    ax1.axvspan(s, e, alpha=0.25, color="#f85149", zorder=2)
    mid = s + (e - s) / 2
    price_row = btc[btc["date"] <= e]
    if len(price_row):
        p = price_row.iloc[-1]["btc_price"]
        ax1.annotate(name.replace(" Conformation", "\nConf."),
                     xy=(mid, p), xytext=(0, 18), textcoords="offset points",
                     color="#f85149", fontsize=6.5, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color="#f85149", lw=0.5))

ax1.set_title("BTC Price", color="#8b949e", fontsize=9, pad=4)
ax1.legend(loc="upper left", fontsize=7, framealpha=0.2, labelcolor="white")

# ── Panel 2: Cadence + SMA60 + SMA90 ─────────────────────────────────────
ax2.axhline(0, color="#484f58", linewidth=0.8, linestyle="--")

# Shade cadence positive/negative regions
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] >= 0, alpha=0.12, color="#3fb950", interpolate=True)
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] < 0,  alpha=0.12, color="#f85149", interpolate=True)

ax2.plot(valid["date"], valid["cadence"], color="#484f58", linewidth=0.6, alpha=0.6, label="Cadence (raw)")
ax2.plot(valid["date"], valid["sma60"],   color="#e3b341", linewidth=1.5, alpha=0.9, label="SMA60")
ax2.plot(valid["date"], valid["sma90"],   color="#3fb950", linewidth=1.5, alpha=0.9, label="SMA90")

# Shade between SMA60 and SMA90
ax2.fill_between(valid["date"], valid["sma60"], valid["sma90"],
                  where=valid["sma60"] >= valid["sma90"],
                  alpha=0.18, color="#3fb950", interpolate=True, label="SMA60 > SMA90 (bull zone)")
ax2.fill_between(valid["date"], valid["sma60"], valid["sma90"],
                  where=valid["sma60"] < valid["sma90"],
                  alpha=0.18, color="#f85149", interpolate=True, label="SMA60 < SMA90 (bear zone)")

# Mark bear crosses (SMA60 crosses below SMA90)
for _, row in bear_crosses.iterrows():
    lh = near_lh(row["date"])
    color = "#f85149" if lh else "#ff7b72"
    alpha = 1.0 if lh else 0.5
    ax2.axvline(row["date"], color=color, linewidth=1.5 if lh else 0.8,
                alpha=alpha, linestyle="-", zorder=5)
    ax2.scatter(row["date"], row["sma60"], color=color, s=60 if lh else 25,
                zorder=6, marker="v")

# Mark bull crosses (SMA60 crosses above SMA90)
for _, row in bull_crosses.iterrows():
    ax2.axvline(row["date"], color="#3fb950", linewidth=0.8, alpha=0.4, linestyle="-", zorder=4)
    ax2.scatter(row["date"], row["sma60"], color="#3fb950", s=25, zorder=5, marker="^")

# Mark Lower High windows
for s, e, name in lh_windows:
    if s < valid["date"].min():
        continue
    ax2.axvspan(s, e, alpha=0.2, color="#f85149", zorder=2)

ax2.set_ylabel("Cadence value", color="gray", fontsize=8)
ax2.set_title("F&G Cadence (90D) + SMA60 + SMA90  |  ▼ Bear Cross  ▲ Bull Cross  |  Red vertical = near Lower High",
              color="#8b949e", fontsize=8.5, pad=4)

legend_elems = [
    Line2D([0],[0], color="#484f58", lw=1, label="Cadence raw"),
    Line2D([0],[0], color="#e3b341", lw=2, label="SMA60"),
    Line2D([0],[0], color="#3fb950", lw=2, label="SMA90"),
    Line2D([0],[0], color="#f85149", lw=1.5, label="Bear cross (SMA60<SMA90) near LH"),
    Line2D([0],[0], color="#ff7b72", lw=0.8, alpha=0.5, label="Bear cross (false positive)"),
    mpatches.Patch(color="#f85149", alpha=0.2, label="Lower High event window"),
]
ax2.legend(handles=legend_elems, loc="upper left", fontsize=6.5, framealpha=0.25,
           labelcolor="white", ncol=2)

# ── Panel 3: SMA60 - SMA90 spread (histogram-style) ──────────────────────
spread = valid["sma60"] - valid["sma90"]
ax3.axhline(0, color="#484f58", linewidth=0.8, linestyle="--")
ax3.bar(valid["date"], spread,
        color=np.where(spread >= 0, "#3fb950", "#f85149"),
        alpha=0.7, width=1.2)

# Mark bear crosses on spread panel
for _, row in bear_crosses.iterrows():
    lh = near_lh(row["date"])
    ax3.axvline(row["date"], color="#f85149" if lh else "#ff7b72",
                linewidth=1.5 if lh else 0.6, alpha=1.0 if lh else 0.4)

# Mark Lower High windows
for s, e, name in lh_windows:
    if s < valid["date"].min():
        continue
    ax3.axvspan(s, e, alpha=0.2, color="#f85149")

ax3.set_ylabel("SMA60 − SMA90", color="gray", fontsize=8)
ax3.set_title("Spread: SMA60 − SMA90  (positive = bull zone, negative = bear zone)",
              color="#8b949e", fontsize=8.5, pad=4)

# ── X-axis sync ───────────────────────────────────────────────────────────
date_min = valid["date"].min()
date_max = valid["date"].max()
for ax in axes:
    ax.set_xlim(date_min, date_max)

# Hide x tick labels on top panels
for ax in [ax1, ax2]:
    ax.tick_params(labelbottom=False)

plt.tight_layout(rect=[0, 0, 1, 0.97])
outpath = "fg_cadence_sma_crossover.png"
plt.savefig(outpath, dpi=150, bbox_inches="tight",
            facecolor="#0d1117", edgecolor="none")
plt.close()
print(f"\nChart saved: {outpath}")
