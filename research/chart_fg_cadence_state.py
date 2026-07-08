"""
F&G Cadence — State Condition Chart
Visualisasi: cadence < -15 AND cadence < SMA60 sebagai kondisi bearish
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

# BTC price daily (fill forward)
btc_all = events[["date","btc_price"]].dropna().sort_values("date").drop_duplicates("date")

lh_rows  = events[events["event"].str.contains("Lower High", na=False)].copy()
cyc_rows = events[events["event"].str.contains("Cycle Peak", na=False)].copy()

# ── Compute ────────────────────────────────────────────────────────────────
fg["cadence"] = fg["fg"] - fg["fg"].shift(90)
fg["sma60"]   = fg["cadence"].rolling(60).mean()
fg["sma90"]   = fg["cadence"].rolling(90).mean()

valid = fg.dropna(subset=["sma60","sma90"]).copy()

# State condition: cadence < -15 AND cadence < SMA60
THRESHOLD = -15
valid["bear_state"] = (valid["cadence"] < THRESHOLD) & (valid["cadence"] < valid["sma60"])

# SMA60 vs SMA90 cross (previous approach, for comparison)
valid["sma60_above"] = valid["sma60"] > valid["sma90"]
prev = valid["sma60_above"].shift(1).fillna(False)
valid["sma_bear_cross"] = prev & ~valid["sma60_above"]

# Lower High windows
lh_windows = []
for name, grp in lh_rows.groupby("event", sort=False):
    lh_windows.append((grp["date"].min(), grp["date"].max(), name))

# ── Layout ─────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(20, 15), facecolor="#0d1117")
gs  = fig.add_gridspec(4, 1, height_ratios=[2.2, 2.2, 1.2, 1.2],
                        hspace=0.08, left=0.06, right=0.97, top=0.94, bottom=0.04)

ax1 = fig.add_subplot(gs[0])
ax2 = fig.add_subplot(gs[1], sharex=ax1)
ax3 = fig.add_subplot(gs[2], sharex=ax1)
ax4 = fig.add_subplot(gs[3], sharex=ax1)

DARK_BG   = "#0d1117"
GRID_COL  = "#21262d"
SPINE_COL = "#30363d"

for ax in [ax1, ax2, ax3, ax4]:
    ax.set_facecolor(DARK_BG)
    ax.tick_params(colors="#8b949e", labelsize=8)
    for sp in ax.spines.values():
        sp.set_color(SPINE_COL)
    ax.grid(axis="y", color=GRID_COL, linewidth=0.5, linestyle="--", alpha=0.7)
    ax.grid(axis="x", color=GRID_COL, linewidth=0.3, linestyle=":", alpha=0.5)

fig.suptitle("F&G Cadence (90D) — State Condition Approach\n"
             "Bear State: Cadence < −15  AND  Cadence < SMA60",
             color="white", fontsize=13, fontweight="bold")

date_min = valid["date"].min()
date_max = valid["date"].max()

# ── LH window shading helper ───────────────────────────────────────────────
def shade_lh(ax, alpha=0.18, label=True):
    for i, (s, e, name) in enumerate(lh_windows):
        if s < date_min:
            continue
        ax.axvspan(s, e + pd.Timedelta(days=1), alpha=alpha, color="#f85149", zorder=2)

# ── Panel 1: BTC Price ─────────────────────────────────────────────────────
btc_v = btc_all[btc_all["date"] >= date_min]
ax1.plot(btc_v["date"], btc_v["btc_price"], color="#58a6ff", linewidth=1.1, alpha=0.9)
ax1.set_yscale("log")
ax1.set_ylabel("BTC Price (log)", color="#8b949e", fontsize=8)

# Bear state overlay on price (light red background when condition active)
bear_dates = valid[valid["bear_state"]]["date"]
for d in bear_dates:
    ax1.axvspan(d, d + pd.Timedelta(days=1), alpha=0.06, color="#f85149", zorder=1)

# Lower High events
for s, e, name in lh_windows:
    if s < date_min:
        continue
    ax1.axvspan(s, e + pd.Timedelta(days=1), alpha=0.30, color="#f85149", zorder=3)
    mid = s + (e - s)/2
    ax1.axvline(mid, color="#f85149", linewidth=1.2, alpha=0.8, zorder=4)
    row = btc_v[btc_v["date"] <= e + pd.Timedelta(days=3)]
    if len(row):
        p = row.iloc[-1]["btc_price"]
        short = name.replace(" Conformation","(Conf)").replace(" Confirmation","(Conf)")
        ax1.annotate(short, xy=(mid, p),
                     xytext=(0, 22), textcoords="offset points",
                     color="#f85149", fontsize=7, ha="center", fontweight="bold",
                     arrowprops=dict(arrowstyle="-", color="#f85149", lw=0.6))

# Cycle peaks
for _, row in cyc_rows.iterrows():
    if row["date"] < date_min:
        continue
    ax1.axvline(row["date"], color="#e3b341", linewidth=0.8, alpha=0.5, linestyle=":")
    ax1.annotate("Cycle\nPeak", xy=(row["date"], row["btc_price"]),
                 xytext=(4, -30), textcoords="offset points",
                 color="#e3b341", fontsize=6, ha="left")

ax1.set_title("BTC Price  |  Red shaded = Bear State active  |  Bright red = Lower High event",
              color="#8b949e", fontsize=8.5, pad=5)

# ── Panel 2: Cadence + SMA60 + SMA90 ─────────────────────────────────────
ax2.axhline(0, color="#484f58", linewidth=0.8, linestyle="--", zorder=3)
ax2.axhline(THRESHOLD, color="#f85149", linewidth=0.7, linestyle=":", alpha=0.7,
            zorder=3, label=f"Threshold = {THRESHOLD}")

# Raw cadence (dim)
ax2.plot(valid["date"], valid["cadence"], color="#484f58", linewidth=0.7, alpha=0.5, label="Cadence raw")

# SMA lines
ax2.plot(valid["date"], valid["sma60"], color="#e3b341", linewidth=2.0, alpha=0.95, label="SMA60", zorder=5)
ax2.plot(valid["date"], valid["sma90"], color="#3fb950", linewidth=2.0, alpha=0.95, label="SMA90", zorder=5)

# Shade between SMA60 and SMA90
ax2.fill_between(valid["date"], valid["sma60"], valid["sma90"],
                  where=valid["sma60"] >= valid["sma90"],
                  alpha=0.15, color="#3fb950", interpolate=True)
ax2.fill_between(valid["date"], valid["sma60"], valid["sma90"],
                  where=valid["sma60"] < valid["sma90"],
                  alpha=0.15, color="#f85149", interpolate=True)

# Bear state: fill cadence area strongly
ax2.fill_between(valid["date"], valid["cadence"], THRESHOLD,
                  where=valid["bear_state"],
                  alpha=0.40, color="#f85149", interpolate=True,
                  label="Bear State active", zorder=4)
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["bear_state"],
                  alpha=0.10, color="#f85149", interpolate=True, zorder=3)

# Lower High windows
shade_lh(ax2, alpha=0.20)

ax2.set_ylabel("Cadence value", color="#8b949e", fontsize=8)
ax2.set_title("F&G Cadence + SMA60 (yellow) + SMA90 (green)  |  Red fill = Bear State (cadence < −15 AND < SMA60)",
              color="#8b949e", fontsize=8.5, pad=5)

legend_elems = [
    Line2D([0],[0], color="#484f58", lw=1, label="Cadence raw"),
    Line2D([0],[0], color="#e3b341", lw=2, label="SMA60"),
    Line2D([0],[0], color="#3fb950", lw=2, label="SMA90"),
    Line2D([0],[0], color="#f85149", lw=1, linestyle=":", label=f"Threshold {THRESHOLD}"),
    mpatches.Patch(color="#f85149", alpha=0.40, label="Bear State active"),
    mpatches.Patch(color="#f85149", alpha=0.20, label="Lower High window"),
]
ax2.legend(handles=legend_elems, loc="lower left", fontsize=7,
           framealpha=0.25, labelcolor="white", ncol=3)

# ── Panel 3: Bear State binary bar ────────────────────────────────────────
ax3.fill_between(valid["date"], valid["bear_state"].astype(int), 0,
                  alpha=0.75, color="#f85149", step="post", label="Bear State ON")
ax3.set_yticks([0, 1])
ax3.set_yticklabels(["OFF", "ON"], color="#8b949e", fontsize=8)
ax3.set_ylim(-0.05, 1.3)
ax3.set_ylabel("Bear State", color="#8b949e", fontsize=8)
ax3.set_title("Bear State Signal  (cadence < −15 AND cadence < SMA60)",
              color="#8b949e", fontsize=8.5, pad=5)
shade_lh(ax3, alpha=0.30)

# Annotate Lower High events
for s, e, name in lh_windows:
    if s < date_min:
        continue
    mid = s + (e - s)/2
    ax3.axvline(mid, color="#f85149", linewidth=1.5, alpha=0.9, zorder=5)
    short = name.replace("Lower High ","LH ").replace(" Conformation","(C)")
    ax3.text(mid, 1.12, short, color="#f85149", fontsize=6.5, ha="center", fontweight="bold")

# ── Panel 4: Cadence level heatmap-style ───────────────────────────────────
spread = valid["sma60"] - valid["sma90"]
colors_bar = np.where(spread >= 0, "#3fb950", "#f85149")
ax4.bar(valid["date"], spread, color=colors_bar, alpha=0.7, width=1.5, zorder=3)
ax4.axhline(0, color="#484f58", linewidth=0.8, linestyle="--")
ax4.set_ylabel("SMA60 − SMA90", color="#8b949e", fontsize=8)
ax4.set_title("Spread: SMA60 − SMA90  (green = bull momentum, red = bear momentum)",
              color="#8b949e", fontsize=8.5, pad=5)
shade_lh(ax4, alpha=0.20)

# Mark SMA60 < SMA90 crosses on this panel
for _, row in valid[valid["sma_bear_cross"]].iterrows():
    ax4.axvline(row["date"], color="#ff7b72", linewidth=1.0, alpha=0.6, zorder=5)

# X-axis formatting on bottom panel only
ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax4.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=0, ha="center", color="#8b949e")
for ax in [ax1, ax2, ax3]:
    plt.setp(ax.xaxis.get_majorticklabels(), visible=False)

# Current date line
today = valid["date"].max()
for ax in [ax1, ax2, ax3, ax4]:
    ax.axvline(today, color="#8b949e", linewidth=0.8, linestyle="--", alpha=0.5)

ax4.text(today, ax4.get_ylim()[1]*0.85, "Today", color="#8b949e",
         fontsize=7, ha="right", alpha=0.7)

outpath = "fg_cadence_state_condition.png"
plt.savefig(outpath, dpi=150, bbox_inches="tight",
            facecolor=DARK_BG, edgecolor="none")
plt.close()
print(f"Saved: {outpath}")
