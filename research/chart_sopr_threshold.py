"""
Reproduce Alphactal SOPR Trend Signal chart
EMA90 / SMA80 with threshold filters:
  Bearish (red)  : DOWN crossover AND EMA90 was >= 1.015 before crossing
  Bullish (green): UP crossover   AND EMA90 was <= 0.99  before crossing
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

# ── Style ──────────────────────────────────────────────────────────────────
matplotlib.rcParams.update({
    "figure.facecolor" : "#0d1117",
    "axes.facecolor"   : "#131920",
    "text.color"       : "#c9d1d9",
    "axes.labelcolor"  : "#c9d1d9",
    "xtick.color"      : "#8b949e",
    "ytick.color"      : "#8b949e",
    "axes.edgecolor"   : "#30363d",
    "grid.color"       : "#21262d",
    "font.family"      : "monospace",
    "font.size"        : 9,
})

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"], usecols=["date","btc_price","asopr"]
)
df = (df.dropna(subset=["btc_price","asopr"])
       .query("btc_price > 0 and date >= '2012-01-01'")
       .sort_values("date").reset_index(drop=True))

df["EMA90"] = df["asopr"].ewm(span=90, adjust=False).mean()
df["SMA80"] = df["asopr"].rolling(80, min_periods=80).mean()

# ── Signal Detection ───────────────────────────────────────────────────────
BEAR_THRESH = 1.015
BULL_THRESH = 0.99
MIN_GAP     = 90   # min days between same-type signals

diff      = df["EMA90"] - df["SMA80"]
prev_diff = diff.shift(1)
prev_ema  = df["EMA90"].shift(1)   # EMA level just before crossover

raw_down = (diff < 0) & (prev_diff >= 0)   # EMA crosses below SMA
raw_up   = (diff > 0) & (prev_diff <= 0)   # EMA crosses above SMA

# Threshold filter: the EMA level on the day before crossover
bear_mask = raw_down & (prev_ema >= BEAR_THRESH)
bull_mask = raw_up   & (prev_ema <= BULL_THRESH)

# Apply min-gap cooldown
def apply_gap(mask, gap=MIN_GAP):
    dates = df.loc[mask, "date"].tolist()
    filtered, last = [], pd.Timestamp("2000-01-01")
    for d in dates:
        if (d - last).days >= gap:
            filtered.append(d)
            last = d
    return filtered

bear_dates = apply_gap(bear_mask)
bull_dates = apply_gap(bull_mask)

print(f"Bearish signals: {len(bear_dates)}")
for d in bear_dates:
    row = df[df["date"]==d].iloc[0]
    print(f"  {d.strftime('%Y-%m-%d')}  BTC=${row.btc_price:,.0f}  EMA90={row.EMA90:.4f}  SMA80={row.SMA80:.4f}")

print(f"\nBullish signals: {len(bull_dates)}")
for d in bull_dates:
    row = df[df["date"]==d].iloc[0]
    print(f"  {d.strftime('%Y-%m-%d')}  BTC=${row.btc_price:,.0f}  EMA90={row.EMA90:.4f}  SMA80={row.SMA80:.4f}")

# ── Chart ──────────────────────────────────────────────────────────────────
fig, ax1 = plt.subplots(figsize=(20, 9))
ax2 = ax1.twinx()

# BTC Price — right axis, log scale
ax2.semilogy(df["date"], df["btc_price"],
             color="#c9d1d9", lw=1.0, alpha=0.75, zorder=2)
ax2.set_ylabel("BTC Price (USD)", color="#8b949e", fontsize=9, labelpad=8)
ax2.tick_params(axis="y", colors="#8b949e")
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x, _: f"${x:,.0f}" if x >= 1000 else f"${x:.0f}"))
ax2.set_ylim(0.05, df["btc_price"].max() * 5)

# aSOPR — left axis (raw, faded)
ax1.plot(df["date"], df["asopr"],
         color="#8b949e", lw=0.5, alpha=0.30, zorder=3, label="aSOPR (raw)")

# SMA80 — green
ax1.plot(df["date"], df["SMA80"],
         color="#3fb950", lw=1.6, alpha=0.90, zorder=4, label="SMA 80")

# EMA90 — orange
ax1.plot(df["date"], df["EMA90"],
         color="#f0883e", lw=1.6, alpha=0.90, zorder=4, label="EMA 90")

# Threshold lines
ax1.axhline(BEAR_THRESH, color="#f85149", lw=1.0, ls="--",
            alpha=0.70, zorder=3, label=f"Threshold {BEAR_THRESH}")
ax1.axhline(BULL_THRESH, color="#58a6ff", lw=1.0, ls="--",
            alpha=0.70, zorder=3, label=f"Threshold {BULL_THRESH}")

# Fill zone between thresholds (neutral zone)
ax1.axhspan(BULL_THRESH, BEAR_THRESH, alpha=0.04, color="#e6edf3", zorder=1)

# Signal vertical lines
for d in bear_dates:
    ax1.axvline(d, color="#f85149", lw=1.2, alpha=0.80, zorder=5)
for d in bull_dates:
    ax1.axvline(d, color="#3fb950", lw=1.2, alpha=0.80, zorder=5)

# Signal labels on top
ymax_label = ax1.get_ylim()[1] if ax1.get_ylim()[1] else 1.27
for d in bear_dates:
    ax1.text(d, 1.255, "▼", ha="center", va="top",
             color="#f85149", fontsize=7.5, fontweight="bold", zorder=6)
for d in bull_dates:
    ax1.text(d, 0.955, "▲", ha="center", va="bottom",
             color="#3fb950", fontsize=7.5, fontweight="bold", zorder=6)

# aSOPR y-axis
ax1.set_ylabel("aSOPR", color="#c9d1d9", fontsize=9, labelpad=8)
ax1.set_ylim(0.945, 1.265)
ax1.tick_params(axis="y", colors="#c9d1d9")
ax1.set_zorder(ax2.get_zorder() + 1)
ax1.patch.set_visible(False)

# X-axis
ax1.xaxis.set_major_locator(mdates.YearLocator())
ax1.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
plt.setp(ax1.xaxis.get_majorticklabels(), ha="center", fontsize=8)
ax1.set_xlim(df["date"].min(), df["date"].max())

# Grid
ax1.grid(True, axis="both", alpha=0.20, zorder=0)

# Legend
from matplotlib.lines import Line2D
from matplotlib.patches import Patch
legend_els = [
    Line2D([0],[0], color="#c9d1d9", lw=1.2, label="BTC Price"),
    Line2D([0],[0], color="#8b949e", lw=0.8, alpha=0.5, label="aSOPR (raw)"),
    Line2D([0],[0], color="#3fb950", lw=1.8, label="SMA 80"),
    Line2D([0],[0], color="#f0883e", lw=1.8, label="EMA 90"),
    Line2D([0],[0], color="#f85149", lw=1.2, ls="--", label=f"Threshold {BEAR_THRESH}"),
    Line2D([0],[0], color="#58a6ff", lw=1.2, ls="--", label=f"Threshold {BULL_THRESH}"),
    Patch(facecolor="#f85149", alpha=0.7, label="Bearish Signal"),
    Patch(facecolor="#3fb950", alpha=0.7, label="Bullish Signal"),
]
ax1.legend(handles=legend_els, loc="upper left", fontsize=8,
           framealpha=0.35, facecolor="#161b22", edgecolor="#30363d",
           ncol=2, columnspacing=1.0)

# Title & subtitle
fig.suptitle("Bitcoin: aSOPR Trend Signal  —  EMA90 / SMA80",
             fontsize=14, fontweight="bold", color="#e6edf3", y=0.98)
ax1.set_title(f"Bearish threshold ≥ {BEAR_THRESH}  |  Bullish threshold ≤ {BULL_THRESH}  |  Min gap {MIN_GAP}d",
              fontsize=8.5, color="#8b949e", pad=4)

out = r"D:\Claude Code\Projects\Onchain-Dashboard\chart_sopr_threshold.png"
plt.savefig(out, dpi=160, bbox_inches="tight", facecolor="#0d1117")
print(f"\nSaved: {out}")
plt.show()
