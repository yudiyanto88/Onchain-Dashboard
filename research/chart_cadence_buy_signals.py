"""
F&G Cadence — Clean buy signal chart
PD/SB1 (cyan) dan BD1 (green) only, no event labels
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

master = pd.read_csv("data_master_all_metrics.csv", parse_dates=["date"])
master = master[["date","btc_price"]].dropna().sort_values("date").drop_duplicates("date")
master["ma200"] = master["btc_price"].rolling(200).mean()

events = pd.read_csv("data_momentum_events.csv", parse_dates=["date"])

# ── Cadence ────────────────────────────────────────────────────────────────
fg["cadence"] = fg["fg"] - fg["fg"].shift(90)
fg["sma60"]   = fg["cadence"].rolling(60).mean()
fg["sma90"]   = fg["cadence"].rolling(90).mean()
valid = fg.dropna(subset=["sma60","sma90"]).copy()
valid = valid.merge(master[["date","btc_price","ma200"]], on="date", how="left")
valid[["btc_price","ma200"]] = valid[["btc_price","ma200"]].ffill()

date_min = valid["date"].min()
date_max = valid["date"].max()

# ── Zero crosses ───────────────────────────────────────────────────────────
valid["c_pos"]      = (valid["cadence"] > 0).astype(bool)
prev_pos            = valid["c_pos"].shift(1).fillna(False).astype(bool)
valid["cross_buy"]  = ~prev_pos & valid["c_pos"]                          # NEG→POS
valid["above_ma200"] = valid["btc_price"] > valid["ma200"]
valid["cross_bd"]   = valid["cross_buy"] & valid["above_ma200"]           # BD1
valid["cross_pd"]   = valid["cross_buy"] & ~valid["above_ma200"]          # PD1/SB1

# ── Event lines (no labels) ────────────────────────────────────────────────
def ev(pattern):
    return events[events["event"].str.contains(pattern, na=False, regex=True)].drop_duplicates("event").sort_values("date")

dips    = ev("Bull Dip")
pre_sb  = ev("Pre Detection|Start of Bull")
bottoms = ev("Bear Bottom")
cyc     = ev("Cycle Peak")
tops    = ev("Local Top")
lh      = ev("Lower High")

# ── Figure ─────────────────────────────────────────────────────────────────
DARK = "#0d1117"
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(22, 11), sharex=True,
                                gridspec_kw={"height_ratios":[1.6, 1.4], "hspace":0.04},
                                facecolor=DARK)
fig.suptitle("F&G Cadence (90D) — Buy Signal Map\n▲ BD1  (above 200D MA)     ▲ PD1 / SB1  (below 200D MA)",
             color="white", fontsize=13, fontweight="bold", y=0.995)

for ax in (ax1, ax2):
    ax.set_facecolor(DARK)
    ax.tick_params(colors="#8b949e", labelsize=9)
    for sp in ax.spines.values(): sp.set_color("#21262d")
    ax.grid(axis="y", color="#1c2128", linewidth=0.6, linestyle="--", alpha=0.8)
    ax.grid(axis="x", color="#1c2128", linewidth=0.3, linestyle=":", alpha=0.4)

# ── Panel 1: BTC Price ─────────────────────────────────────────────────────
btc_v = master[master["date"] >= date_min]
ax1.plot(btc_v["date"], btc_v["btc_price"],
         color="#58a6ff", linewidth=1.2, alpha=0.90, zorder=4)
ax1.plot(btc_v["date"], btc_v["ma200"],
         color="#8b949e", linewidth=1.3, alpha=0.65, zorder=4, linestyle="--")
ax1.set_yscale("log")
ax1.set_ylabel("BTC Price (log)", color="#8b949e", fontsize=9)

# 200D MA zone shading
ax1.fill_between(btc_v["date"], btc_v["btc_price"], btc_v["ma200"],
                  where=btc_v["btc_price"] >= btc_v["ma200"],
                  alpha=0.06, color="#3fb950", interpolate=True)
ax1.fill_between(btc_v["date"], btc_v["btc_price"], btc_v["ma200"],
                  where=btc_v["btc_price"] < btc_v["ma200"],
                  alpha=0.06, color="#f85149", interpolate=True)

# Event lines — thin, no labels
def vlines(ax, df, color, lw=0.9, ls="-", alpha=0.55, zorder=3):
    for _, r in df.iterrows():
        if r["date"] < date_min: continue
        ax.axvline(r["date"], color=color, linewidth=lw, linestyle=ls, alpha=alpha, zorder=zorder)

vlines(ax1, dips,    "#3fb950", lw=0.8, ls=":",  alpha=0.50)
vlines(ax1, pre_sb,  "#79c0ff", lw=1.0, ls="-.", alpha=0.65)
vlines(ax1, bottoms, "#bc8cff", lw=1.0, ls="--", alpha=0.65)
vlines(ax1, cyc,     "#e3b341", lw=1.8, ls="-",  alpha=0.85)
vlines(ax1, tops,    "#f0883e", lw=0.9, ls="-",  alpha=0.50)
vlines(ax1, lh,      "#f85149", lw=0.9, ls="--", alpha=0.50)

ax1.set_title("BTC Price + 200D MA  |  no labels — see legend for line colors",
              color="#8b949e", fontsize=8.5, pad=5)

leg1 = [
    Line2D([0],[0], color="#58a6ff", lw=1.5, label="BTC Price"),
    Line2D([0],[0], color="#8b949e", lw=1.3, ls="--", label="200D MA"),
    Line2D([0],[0], color="#e3b341", lw=2.0, label="Cycle Peak"),
    Line2D([0],[0], color="#f0883e", lw=1.0, label="Local Top"),
    Line2D([0],[0], color="#bc8cff", lw=1.0, ls="--", label="Bear Bottom"),
    Line2D([0],[0], color="#79c0ff", lw=1.0, ls="-.", label="PD / Start of Bull"),
    Line2D([0],[0], color="#3fb950", lw=1.0, ls=":", label="Bull Dip"),
    Line2D([0],[0], color="#f85149", lw=1.0, ls="--", label="Lower High"),
]
ax1.legend(handles=leg1, loc="upper left", fontsize=7.5,
           framealpha=0.20, labelcolor="white", ncol=4)

# ── Panel 2: Cadence ──────────────────────────────────────────────────────
ax2.axhline(0, color="#30363d", linewidth=1.0, linestyle="--", zorder=3)

ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] >= 0, alpha=0.10, color="#3fb950", interpolate=True)
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] < 0,  alpha=0.10, color="#f85149", interpolate=True)

ax2.plot(valid["date"], valid["cadence"],
         color="#30363d", linewidth=0.7, alpha=0.60, zorder=3)
ax2.plot(valid["date"], valid["sma60"],
         color="#e3b341", linewidth=2.3, alpha=0.95, zorder=5, label="SMA60")
ax2.plot(valid["date"], valid["sma90"],
         color="#3fb950", linewidth=2.3, alpha=0.95, zorder=5, label="SMA90")

# SMA zone fill
ax2.fill_between(valid["date"], valid["sma60"], valid["sma90"],
                  where=valid["sma60"] >= valid["sma90"],
                  alpha=0.12, color="#3fb950", interpolate=True)
ax2.fill_between(valid["date"], valid["sma60"], valid["sma90"],
                  where=valid["sma60"] < valid["sma90"],
                  alpha=0.12, color="#f85149", interpolate=True)

# Mirror event lines
vlines(ax2, dips,    "#3fb950", lw=0.8, ls=":",  alpha=0.40)
vlines(ax2, pre_sb,  "#79c0ff", lw=1.0, ls="-.", alpha=0.60)
vlines(ax2, bottoms, "#bc8cff", lw=1.0, ls="--", alpha=0.60)
vlines(ax2, cyc,     "#e3b341", lw=1.8, ls="-",  alpha=0.75)
vlines(ax2, tops,    "#f0883e", lw=0.9, ls="-",  alpha=0.45)
vlines(ax2, lh,      "#f85149", lw=0.9, ls="--", alpha=0.45)

# BD1 signals ▲ green
bd = valid[valid["cross_bd"]]
ax2.scatter(bd["date"], bd["sma60"],
            color="#3fb950", s=80, zorder=9, marker="^",
            edgecolors="#0d1117", linewidths=0.5)

# PD1/SB1 signals ▲ cyan
pd_sig = valid[valid["cross_pd"]]
ax2.scatter(pd_sig["date"], pd_sig["sma60"],
            color="#79c0ff", s=90, zorder=9, marker="^",
            edgecolors="#0d1117", linewidths=0.5)

ax2.set_ylabel("Cadence value", color="#8b949e", fontsize=9)
ax2.set_title("Cadence + SMA60 (yellow) + SMA90 (green)  |  ▲ green = BD1   ▲ cyan = PD1/SB1",
              color="#8b949e", fontsize=9, pad=5)

leg2 = [
    Line2D([0],[0], color="#30363d", lw=1,  label="Cadence raw"),
    Line2D([0],[0], color="#e3b341", lw=2.3, label="SMA60"),
    Line2D([0],[0], color="#3fb950", lw=2.3, label="SMA90"),
    Line2D([0],[0], color="#3fb950", lw=0, marker="^", ms=9,
           markeredgecolor="#0d1117", label="BD1 buy  (price > 200D MA)"),
    Line2D([0],[0], color="#79c0ff", lw=0, marker="^", ms=9,
           markeredgecolor="#0d1117", label="PD1/SB1 buy  (price < 200D MA)"),
]
ax2.legend(handles=leg2, loc="lower right", fontsize=8,
           framealpha=0.22, labelcolor="white", ncol=2)

# ── X axis ────────────────────────────────────────────────────────────────
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0, ha="center",
         color="#8b949e", fontsize=9)
plt.setp(ax1.xaxis.get_majorticklabels(), visible=False)

# Today line
for ax in (ax1, ax2):
    ax.axvline(date_max, color="#484f58", linewidth=0.8, linestyle="--", alpha=0.5)

plt.tight_layout(rect=[0, 0, 1, 0.975])
out = "fg_cadence_buy_signals.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=DARK, edgecolor="none")
plt.close()
print(f"Saved: {out}")
