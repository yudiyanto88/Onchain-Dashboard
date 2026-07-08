"""
F&G Cadence (90D) vs Cycle Peaks & Local Tops — exit timing chart
2 panels only: BTC Price + Cadence
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
import matplotlib.dates as mdates

# ── Load ───────────────────────────────────────────────────────────────────
fg = pd.read_csv("data_fg.csv", parse_dates=["date"])
fg = fg.rename(columns={"Fear & Greed": "fg"}).sort_values("date").reset_index(drop=True)

events = pd.read_csv("data_momentum_events.csv", parse_dates=["date"])
btc_all = events[["date","btc_price"]].dropna().sort_values("date").drop_duplicates("date")

# Filter events
cyc_rows = events[events["event"].str.contains("Cycle Peak", na=False)].copy()
top_rows = events[events["event"].str.contains("Local Top", na=False)].copy()
lh_rows  = events[events["event"].str.contains("Lower High", na=False)].copy()

# ── Compute ────────────────────────────────────────────────────────────────
fg["cadence"] = fg["fg"] - fg["fg"].shift(90)
fg["sma60"]   = fg["cadence"].rolling(60).mean()
fg["sma90"]   = fg["cadence"].rolling(90).mean()

valid = fg.dropna(subset=["sma60","sma90"]).copy()
date_min = valid["date"].min()
date_max = valid["date"].max()

# Zero cross detection (raw cadence)
valid["c_pos"]          = (valid["cadence"] > 0).astype(bool)
prev_pos                = valid["c_pos"].shift(1).fillna(False).astype(bool)
valid["zero_cross_dn"]  = prev_pos & ~valid["c_pos"]   # pos→neg SELL

# ── Figure: 2 panels ──────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(20, 11), sharex=True,
                                gridspec_kw={"height_ratios": [1.6, 1.4], "hspace": 0.06},
                                facecolor="#0d1117")
fig.suptitle("F&G Cadence (90D) — Exit Timing at Local Tops & Cycle Peaks",
             color="white", fontsize=14, fontweight="bold", y=0.99)

DARK   = "#0d1117"
GRID   = "#21262d"
SPINE  = "#30363d"

for ax in (ax1, ax2):
    ax.set_facecolor(DARK)
    ax.tick_params(colors="#8b949e", labelsize=8)
    for sp in ax.spines.values(): sp.set_color(SPINE)
    ax.grid(axis="y", color=GRID, linewidth=0.5, linestyle="--", alpha=0.8)
    ax.grid(axis="x", color=GRID, linewidth=0.3, linestyle=":", alpha=0.5)

btc_v = btc_all[btc_all["date"] >= date_min].copy()

# ── Event label helpers ────────────────────────────────────────────────────
def short_label(name):
    return (name
            .replace("Cycle Peak ", "CP ")
            .replace("Local Top ", "LT ")
            .replace(" (ATH)", "\n(ATH)")
            .replace("Lower High ", "LH "))

# ── Panel 1: BTC Price ────────────────────────────────────────────────────
ax1.plot(btc_v["date"], btc_v["btc_price"],
         color="#58a6ff", linewidth=1.1, alpha=0.90, zorder=3)
ax1.set_yscale("log")
ax1.set_ylabel("BTC Price (log)", color="#8b949e", fontsize=9)

# Cycle Peaks — yellow vertical + label
cp_done = {}
for _, row in cyc_rows.iterrows():
    if row["date"] < date_min: continue
    ax1.axvline(row["date"], color="#e3b341", linewidth=1.6, alpha=0.85, zorder=5, linestyle="-")
    label = short_label(row["event"])
    if label not in cp_done:
        ax1.annotate(label, xy=(row["date"], row["btc_price"]),
                     xytext=(5, 6), textcoords="offset points",
                     color="#e3b341", fontsize=7.5, fontweight="bold", zorder=6)
        cp_done[label] = True

# Local Tops — orange vertical + label
lt_done = {}
alt = 1
for _, row in top_rows.drop_duplicates("event").iterrows():
    if row["date"] < date_min: continue
    ax1.axvline(row["date"], color="#f0883e", linewidth=1.2, alpha=0.75, zorder=5, linestyle="-")
    label = short_label(row["event"])
    offset = 28 * alt
    if label not in lt_done:
        ax1.annotate(label, xy=(row["date"], row["btc_price"]),
                     xytext=(4, offset), textcoords="offset points",
                     color="#f0883e", fontsize=6.5, zorder=6,
                     arrowprops=dict(arrowstyle="-", color="#f0883e", lw=0.5))
        lt_done[label] = True
        alt = alt * -1 if abs(offset) > 20 else alt + 1

# Lower High — red vertical
for _, row in lh_rows.drop_duplicates("event").iterrows():
    if row["date"] < date_min: continue
    ax1.axvline(row["date"], color="#f85149", linewidth=1.2, alpha=0.70, zorder=4, linestyle="--")
    ax1.annotate(short_label(row["event"]),
                 xy=(row["date"], row["btc_price"]),
                 xytext=(-40, -22), textcoords="offset points",
                 color="#f85149", fontsize=6.5, zorder=6,
                 arrowprops=dict(arrowstyle="-", color="#f85149", lw=0.5))

ax1.set_title("BTC Price  |  Yellow = Cycle Peak  |  Orange = Local Top  |  Red dashed = Lower High",
              color="#8b949e", fontsize=9, pad=5)

legend1 = [
    Line2D([0],[0], color="#e3b341", lw=2.0, label="Cycle Peak"),
    Line2D([0],[0], color="#f0883e", lw=1.5, label="Local Top"),
    Line2D([0],[0], color="#f85149", lw=1.2, linestyle="--", label="Lower High"),
]
ax1.legend(handles=legend1, loc="upper left", fontsize=8,
           framealpha=0.25, labelcolor="white")

# ── Panel 2: Cadence + SMA60 + SMA90 ─────────────────────────────────────
ax2.axhline(0, color="#484f58", linewidth=1.0, linestyle="--", zorder=3)

# Cadence fill
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] >= 0, alpha=0.15, color="#3fb950", interpolate=True)
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] < 0,  alpha=0.15, color="#f85149", interpolate=True)

ax2.plot(valid["date"], valid["cadence"],
         color="#484f58", linewidth=0.7, alpha=0.55, label="Cadence raw", zorder=3)
ax2.plot(valid["date"], valid["sma60"],
         color="#e3b341", linewidth=2.2, alpha=0.95, label="SMA60", zorder=5)
ax2.plot(valid["date"], valid["sma90"],
         color="#3fb950", linewidth=2.2, alpha=0.95, label="SMA90", zorder=5)

# Zero cross pos→neg (sell signal) — red dot on SMA60
sells = valid[valid["zero_cross_dn"]]
ax2.scatter(sells["date"], sells["sma60"],
            color="#f85149", s=55, zorder=7, marker="v", label="Zero cross ↓ (sell)")

# Mirror event lines on cadence panel
for _, row in cyc_rows.iterrows():
    if row["date"] < date_min: continue
    ax2.axvline(row["date"], color="#e3b341", linewidth=1.6, alpha=0.75, zorder=5)

for _, row in top_rows.drop_duplicates("event").iterrows():
    if row["date"] < date_min: continue
    ax2.axvline(row["date"], color="#f0883e", linewidth=1.2, alpha=0.65, zorder=4)

for _, row in lh_rows.drop_duplicates("event").iterrows():
    if row["date"] < date_min: continue
    ax2.axvline(row["date"], color="#f85149", linewidth=1.2, alpha=0.60, zorder=4, linestyle="--")

ax2.set_ylabel("Cadence value", color="#8b949e", fontsize=9)
ax2.set_title("F&G Cadence (90D) + SMA60 (yellow) + SMA90 (green)  |  ▼ = zero cross sell signal",
              color="#8b949e", fontsize=9, pad=5)

legend2 = [
    Line2D([0],[0], color="#484f58", lw=1, label="Cadence raw"),
    Line2D([0],[0], color="#e3b341", lw=2, label="SMA60"),
    Line2D([0],[0], color="#3fb950", lw=2, label="SMA90"),
    Line2D([0],[0], color="#f85149", lw=0, marker="v", markersize=7, label="Zero cross sell ↓"),
]
ax2.legend(handles=legend2, loc="upper left", fontsize=8,
           framealpha=0.25, labelcolor="white", ncol=2)

# ── X axis ────────────────────────────────────────────────────────────────
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0, ha="center", color="#8b949e", fontsize=9)

ax2.axvline(date_max, color="#8b949e", linewidth=0.8, linestyle="--", alpha=0.4)
ax2.text(date_max, ax2.get_ylim()[0] * 0.85 if ax2.get_ylim()[0] < 0 else 2,
         " Today", color="#8b949e", fontsize=7, alpha=0.6)

plt.tight_layout(rect=[0, 0, 1, 0.98])
outpath = "fg_cadence_exit_timing.png"
plt.savefig(outpath, dpi=150, bbox_inches="tight",
            facecolor=DARK, edgecolor="none")
plt.close()
print(f"Saved: {outpath}")
