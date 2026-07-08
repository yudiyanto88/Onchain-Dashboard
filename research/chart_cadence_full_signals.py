"""
F&G Cadence — Full signal map: sell at tops, buy at bottoms/dips
BD1 vs PD1/SB1 split by 200D MA filter
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

# Merge price + MA200
valid = valid.merge(master[["date","btc_price","ma200"]], on="date", how="left")
valid[["btc_price","ma200"]] = valid[["btc_price","ma200"]].ffill()

# ── Zero crosses ───────────────────────────────────────────────────────────
valid["c_pos"]         = (valid["cadence"] > 0).astype(bool)
prev_pos               = valid["c_pos"].shift(1).fillna(False).astype(bool)
valid["cross_sell"]    = prev_pos & ~valid["c_pos"]          # POS→NEG
valid["cross_buy"]     = ~prev_pos & valid["c_pos"]          # NEG→POS

# Split buy signal by 200D MA
valid["above_ma200"] = valid["btc_price"] > valid["ma200"]
valid["cross_bd"]    = valid["cross_buy"] & valid["above_ma200"]   # BD1
valid["cross_pd"]    = valid["cross_buy"] & ~valid["above_ma200"]  # PD1/SB1

date_min = valid["date"].min()
date_max = valid["date"].max()

# ── Event categories ───────────────────────────────────────────────────────
def get_events(pattern):
    rows = events[events["event"].str.contains(pattern, na=False, regex=True)]
    return rows.drop_duplicates("event").sort_values("date")

cyc   = get_events("Cycle Peak")
tops  = get_events("Local Top")
bottoms = get_events("Bear Bottom")
pre   = get_events("Pre Detection|Start of Bull")
dips  = get_events("Bull Dip")
lh    = get_events("Lower High")

def short(name):
    return (name
            .replace("Cycle Peak ","CP ")
            .replace("Local Top ","LT ")
            .replace("Bear Bottom ","BB ")
            .replace("Pre Detection ","PD ")
            .replace("Start of Bull ","SB ")
            .replace("Bull Dip ","BD ")
            .replace("Lower High ","LH ")
            .replace(" Conformation","(C)")
            .replace(" (ATH)","")
            .replace("(Tier 1)",""))

# ── Figure ─────────────────────────────────────────────────────────────────
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(22, 12), sharex=True,
                                gridspec_kw={"height_ratios":[1.6, 1.4], "hspace":0.05},
                                facecolor="#0d1117")
fig.suptitle("F&G Cadence (90D) — Full Signal Map\n"
             "Sell at Tops (▼)  |  Buy at Dips (▲ BD1)  |  Buy at Bottoms (▲ PD1/SB1)",
             color="white", fontsize=13, fontweight="bold", y=0.995)

DARK, GRID, SPINE = "#0d1117", "#21262d", "#30363d"
for ax in (ax1, ax2):
    ax.set_facecolor(DARK)
    ax.tick_params(colors="#8b949e", labelsize=8)
    for sp in ax.spines.values(): sp.set_color(SPINE)
    ax.grid(axis="y", color=GRID, linewidth=0.5, linestyle="--", alpha=0.8)
    ax.grid(axis="x", color=GRID, linewidth=0.3, linestyle=":", alpha=0.4)

# ── Event rendering helper ─────────────────────────────────────────────────
def vline_events(ax, df, color, lw=1.2, ls="-", alpha=0.75, zorder=4):
    for _, row in df.iterrows():
        if row["date"] < date_min: continue
        ax.axvline(row["date"], color=color, linewidth=lw, linestyle=ls,
                   alpha=alpha, zorder=zorder)

def label_events(ax, df, color, yref, offsets=None, fontsize=7):
    flip = 1
    for i, (_, row) in enumerate(df.iterrows()):
        if row["date"] < date_min: continue
        dy = (offsets[i % len(offsets)] if offsets else 22) * flip
        btc_at = master[master["date"] <= row["date"]]
        p = yref if yref else (btc_at.iloc[-1]["btc_price"] if len(btc_at) else 1e4)
        ax.annotate(short(row["event"]), xy=(row["date"], p),
                    xytext=(3, dy), textcoords="offset points",
                    color=color, fontsize=fontsize, fontweight="bold",
                    ha="left", zorder=7,
                    arrowprops=dict(arrowstyle="-", color=color, lw=0.4))
        flip *= -1

# ── Panel 1: BTC Price + 200D MA ──────────────────────────────────────────
btc_v = master[master["date"] >= date_min]
ax1.plot(btc_v["date"], btc_v["btc_price"],
         color="#58a6ff", linewidth=1.1, alpha=0.90, zorder=3, label="BTC Price")
ax1.plot(btc_v["date"], btc_v["ma200"],
         color="#8b949e", linewidth=1.1, alpha=0.60, zorder=3, linestyle="--", label="200D MA")
ax1.set_yscale("log")
ax1.set_ylabel("BTC Price (log)", color="#8b949e", fontsize=9)

# Above/below 200D MA shading
ax1.fill_between(btc_v["date"], btc_v["btc_price"], btc_v["ma200"],
                  where=btc_v["btc_price"] >= btc_v["ma200"],
                  alpha=0.07, color="#3fb950", interpolate=True)
ax1.fill_between(btc_v["date"], btc_v["btc_price"], btc_v["ma200"],
                  where=btc_v["btc_price"] < btc_v["ma200"],
                  alpha=0.07, color="#f85149", interpolate=True)

# Event verticals on price
vline_events(ax1, cyc,     "#e3b341", lw=2.0, alpha=0.90)
vline_events(ax1, tops,    "#f0883e", lw=1.0, alpha=0.65)
vline_events(ax1, bottoms, "#bc8cff", lw=1.2, alpha=0.75, ls="--")
vline_events(ax1, pre,     "#79c0ff", lw=1.2, alpha=0.75, ls="-.")
vline_events(ax1, dips,    "#3fb950", lw=0.8, alpha=0.50, ls=":")
vline_events(ax1, lh,      "#f85149", lw=1.0, alpha=0.60, ls="--")

# Labels (cycle peaks + bear bottoms only to avoid clutter)
for _, row in cyc.iterrows():
    if row["date"] < date_min: continue
    p = master[master["date"] <= row["date"]]
    p = p.iloc[-1]["btc_price"] if len(p) else 1e4
    ax1.annotate(short(row["event"]), xy=(row["date"], p),
                 xytext=(4, 8), textcoords="offset points",
                 color="#e3b341", fontsize=7.5, fontweight="bold", zorder=7)

for _, row in bottoms.iterrows():
    if row["date"] < date_min: continue
    p = master[master["date"] <= row["date"]]
    p = p.iloc[-1]["btc_price"] if len(p) else 1e4
    ax1.annotate(short(row["event"]), xy=(row["date"], p),
                 xytext=(4, -16), textcoords="offset points",
                 color="#bc8cff", fontsize=6.5, zorder=7,
                 arrowprops=dict(arrowstyle="-", color="#bc8cff", lw=0.4))

ax1.set_title(
    "BTC Price + 200D MA  |  Yellow=Cycle Peak  Orange=Local Top  Purple=Bear Bottom  "
    "Cyan=PD/SB  Green:=Bull Dip  Red--=Lower High",
    color="#8b949e", fontsize=8.5, pad=5)

legend1 = [
    Line2D([0],[0], color="#58a6ff", lw=1.5, label="BTC Price"),
    Line2D([0],[0], color="#8b949e", lw=1.1, ls="--", label="200D MA"),
    Line2D([0],[0], color="#e3b341", lw=2,   label="Cycle Peak"),
    Line2D([0],[0], color="#f0883e", lw=1.2, label="Local Top"),
    Line2D([0],[0], color="#bc8cff", lw=1.2, ls="--", label="Bear Bottom"),
    Line2D([0],[0], color="#79c0ff", lw=1.2, ls="-.", label="PD / Start of Bull"),
    Line2D([0],[0], color="#3fb950", lw=1.0, ls=":", label="Bull Dip"),
    Line2D([0],[0], color="#f85149", lw=1.0, ls="--", label="Lower High"),
]
ax1.legend(handles=legend1, loc="upper left", fontsize=7,
           framealpha=0.25, labelcolor="white", ncol=4)

# ── Panel 2: Cadence + SMA60 + SMA90 + signals ────────────────────────────
ax2.axhline(0, color="#484f58", linewidth=1.0, linestyle="--", zorder=3)

ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] >= 0, alpha=0.12, color="#3fb950", interpolate=True)
ax2.fill_between(valid["date"], valid["cadence"], 0,
                  where=valid["cadence"] < 0,  alpha=0.12, color="#f85149", interpolate=True)

ax2.plot(valid["date"], valid["cadence"],
         color="#484f58", linewidth=0.65, alpha=0.50, zorder=3)
ax2.plot(valid["date"], valid["sma60"],
         color="#e3b341", linewidth=2.2, alpha=0.95, label="SMA60", zorder=5)
ax2.plot(valid["date"], valid["sma90"],
         color="#3fb950", linewidth=2.2, alpha=0.95, label="SMA90", zorder=5)

# Mirror event verticals
vline_events(ax2, cyc,     "#e3b341", lw=1.8, alpha=0.70)
vline_events(ax2, tops,    "#f0883e", lw=0.9, alpha=0.55)
vline_events(ax2, bottoms, "#bc8cff", lw=1.1, alpha=0.65, ls="--")
vline_events(ax2, pre,     "#79c0ff", lw=1.1, alpha=0.65, ls="-.")
vline_events(ax2, dips,    "#3fb950", lw=0.7, alpha=0.40, ls=":")
vline_events(ax2, lh,      "#f85149", lw=0.9, alpha=0.55, ls="--")

# SELL signals ▼ (POS→NEG)
sells = valid[valid["cross_sell"]]
ax2.scatter(sells["date"], sells["sma60"],
            color="#f85149", s=70, zorder=8, marker="v", label="SELL: POS→NEG (▼)")

# BUY BD1 ▲ (NEG→POS above 200D MA)
bd = valid[valid["cross_bd"]]
ax2.scatter(bd["date"], bd["sma60"],
            color="#3fb950", s=70, zorder=8, marker="^", label="BUY BD1: above 200D MA (▲)")

# BUY PD1/SB1 ▲ (NEG→POS below 200D MA)
pd_sig = valid[valid["cross_pd"]]
ax2.scatter(pd_sig["date"], pd_sig["sma60"],
            color="#79c0ff", s=90, zorder=8, marker="^", label="BUY PD1/SB1: below 200D MA (▲)")

ax2.set_ylabel("Cadence value", color="#8b949e", fontsize=9)
ax2.set_title(
    "Cadence + SMA60 (yellow) + SMA90 (green)  |  "
    "▼ red=SELL  ▲ green=BD1 buy  ▲ cyan=PD1/SB1 buy",
    color="#8b949e", fontsize=9, pad=5)

legend2 = [
    Line2D([0],[0], color="#484f58", lw=1, label="Cadence raw"),
    Line2D([0],[0], color="#e3b341", lw=2, label="SMA60"),
    Line2D([0],[0], color="#3fb950", lw=2, label="SMA90"),
    Line2D([0],[0], color="#f85149", lw=0, marker="v", ms=8, label="SELL (POS→NEG)"),
    Line2D([0],[0], color="#3fb950", lw=0, marker="^", ms=8, label="BD1 buy (above MA200)"),
    Line2D([0],[0], color="#79c0ff", lw=0, marker="^", ms=8, label="PD1/SB1 buy (below MA200)"),
]
ax2.legend(handles=legend2, loc="lower right", fontsize=7.5,
           framealpha=0.25, labelcolor="white", ncol=3)

# ── X axis ────────────────────────────────────────────────────────────────
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0, ha="center",
         color="#8b949e", fontsize=9)
plt.setp(ax1.xaxis.get_majorticklabels(), visible=False)

ax2.axvline(date_max, color="#8b949e", linewidth=0.7, linestyle="--", alpha=0.4)
ax2.text(date_max, ax2.get_ylim()[0] * 0.9 if ax2.get_ylim()[0] < 0 else 1,
         " Today", color="#8b949e", fontsize=7, alpha=0.6)

plt.tight_layout(rect=[0, 0, 1, 0.975])
out = "fg_cadence_full_signals.png"
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor=DARK, edgecolor="none")
plt.close()
print(f"Saved: {out}")
