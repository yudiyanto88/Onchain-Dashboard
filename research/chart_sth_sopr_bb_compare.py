"""
STH-SOPR Bollinger Band — Visual Comparison Chart (v2)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

# ── Data ─────────────────────────────────────────────────────────────────────
df = pd.read_csv("data_momentum.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[["date", "btc_price", "sth_sopr"]].dropna()

START = pd.Timestamp("2023-01-01")
df    = df[df["date"] >= START].copy().reset_index(drop=True)

BULL_END   = pd.Timestamp("2025-10-31")
BEAR_START = pd.Timestamp("2025-11-01")

# ── Bull dip bottoms ──────────────────────────────────────────────────────────
BULL_DIPS = [
    ("2023-03-10", 20214),  ("2023-04-21", 27284),
    ("2023-05-24", 26347),  ("2023-06-14", 25173),
    ("2023-08-26", 26033),  ("2023-09-11", 25179),
    ("2024-01-22", 39564),  ("2024-03-19", 61942),
    ("2024-04-17", 61290),  ("2024-05-01", 58341),
    ("2024-07-07", 55919),  ("2024-08-05", 54026),
    ("2024-09-06", 53998),  ("2025-01-09", 92581),
    ("2025-03-10", 78626),  ("2025-04-08", 76270),
    ("2025-08-31", 108303), ("2025-10-17", 106499),
]
dip_df = pd.DataFrame(BULL_DIPS, columns=["date", "price"])
dip_df["date"] = pd.to_datetime(dip_df["date"])

# ── BB helpers ────────────────────────────────────────────────────────────────
def compute_bb(sth_series, period, std_dev):
    sma   = sth_series.rolling(period, min_periods=period).mean()
    sigma = sth_series.rolling(period, min_periods=period).std()
    return sma, sma + std_dev * sigma, sma - std_dev * sigma

def get_bull_signals(df_in, period, std_dev, dedup_days=7):
    sma, upper, lower = compute_bb(df_in["sth_sopr"], period, std_dev)
    below    = df_in["sth_sopr"] < lower
    first_ep = below & ~below.shift(1, fill_value=False)
    bull_mask = first_ep & (df_in["date"] <= BULL_END)
    bear_mask = first_ep & (df_in["date"] > BULL_END)

    def dedup(dates):
        out = []
        for d in dates:
            if not out or (d - out[-1]).days > dedup_days:
                out.append(d)
        return out

    return (sma, upper, lower,
            dedup(df_in[bull_mask]["date"].tolist()),
            dedup(df_in[bear_mask]["date"].tolist()))

def fwd_gain(df_in, sig_date, days=30):
    entry = df_in[df_in["date"] == sig_date]["btc_price"]
    if entry.empty:
        return None
    entry_px = entry.iloc[0]
    future   = df_in[(df_in["date"] > sig_date) &
                     (df_in["date"] <= sig_date + pd.Timedelta(days=days))]
    if future.empty:
        return None
    return (future["btc_price"].max() / entry_px - 1) * 100

# ── Settings ──────────────────────────────────────────────────────────────────
SETTINGS = [
    dict(period=28, std=1.5,  label="BB(28, 1.5)   High Recall",
         color="#27ae60", stats="Recall 88.9%  |  Precision 67.7%  |  Avg G30d +11.4%  |  Avg G60d +21.2%  |  Score 62.6"),
    dict(period=28, std=2.0,  label="BB(28, 2.0)   Image Baseline",
         color="#e67e22", stats="Recall 55.6%  |  Precision 76.5%  |  Avg G30d +13.0%  |  Avg G60d +22.1%  |  Score 56.4"),
    dict(period=28, std=2.5,  label="BB(28, 2.5)   Best Score ★",
         color="#e74c3c", stats="Recall 50.0%  |  Precision 90.9%  |  Avg G30d +15.5%  |  Avg G60d +23.4%  |  Score 64.6"),
    dict(period=60, std=2.25, label="BB(60, 2.25)  Best 60d Gain",
         color="#8e44ad", stats="Recall 44.4%  |  Precision 91.7%  |  Avg G30d +16.0%  |  Avg G60d +29.3%  |  Score 62.3"),
]

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 28), facecolor="#0d1117")
gs  = GridSpec(5, 1, figure=fig, hspace=0.06,
               height_ratios=[2.0, 1.3, 1.3, 1.3, 1.3],
               top=0.97, bottom=0.05, left=0.07, right=0.98)

axs = [fig.add_subplot(gs[i]) for i in range(5)]
date_vals = df["date"].values

def style_ax(ax, show_xlabels=False):
    ax.set_facecolor("#111827")
    ax.tick_params(colors="#9ca3af", labelsize=8)
    for spine in ax.spines.values():
        spine.set_color("#374151")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
    if not show_xlabels:
        ax.tick_params(labelbottom=False)
    else:
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=25, ha="right", fontsize=8)
    ax.set_xlim(df["date"].min(), df["date"].max())
    # Bear shade
    ax.axvspan(BEAR_START, df["date"].max(), color="#7f1d1d33", zorder=0)
    ax.axvline(BEAR_START, color="#dc2626", lw=0.9, linestyle="--", alpha=0.7, zorder=4)
    # Vertical month gridlines (subtle)
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    ax.grid(which="major", axis="x", color="#1f2937", lw=0.5, zorder=0)
    ax.grid(which="major", axis="y", color="#1f2937", lw=0.5, zorder=0)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 0: BTC Price
# ─────────────────────────────────────────────────────────────────────────────
ax0 = axs[0]
style_ax(ax0)

# Price fill gradient effect
ax0.fill_between(df["date"], df["btc_price"], df["btc_price"].min() * 0.5,
                 alpha=0.08, color="#3b82f6")
ax0.semilogy(df["date"], df["btc_price"],
             color="#93c5fd", lw=1.1, alpha=0.95, zorder=3)

# Mark dip bottoms
ax0.scatter(dip_df["date"], dip_df["price"],
            color="#10b981", s=80, zorder=5, marker="o",
            edgecolors="#ffffff", linewidths=0.6)

ax0.set_ylabel("BTC / USD (log)", fontsize=9, color="#9ca3af")
ax0.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda x, _: f"${x/1000:.0f}K" if x >= 1000 else f"${x:.0f}"))

# Title
ax0.set_title(
    "STH-SOPR Bollinger Band Grid Search  —  Bull Dip Signal Comparison\n"
    "● = Identified bull dip bottom (18 events, 2023–Oct 2025)   |   Red zone = Bear market (S2 latch active Nov 2025)",
    color="#f9fafb", fontsize=11.5, pad=10, loc="left", fontweight="bold")

bear_label = ax0.text(
    BEAR_START + pd.Timedelta(days=4), ax0.get_ylim()[0] if ax0.get_ylim()[0] > 0 else 10000,
    "BEAR\nS2 LATCH", color="#ef4444", fontsize=8, va="bottom",
    fontweight="bold", zorder=6)

# ─────────────────────────────────────────────────────────────────────────────
# Panels 1-4: STH-SOPR + BB
# ─────────────────────────────────────────────────────────────────────────────
for idx, cfg in enumerate(SETTINGS):
    ax   = axs[idx + 1]
    show = (idx == 3)
    style_ax(ax, show_xlabels=show)

    sma, upper, lower, bull_sigs, bear_sigs = get_bull_signals(
        df, cfg["period"], cfg["std"])

    # Bands fill
    ax.fill_between(df["date"], lower, upper,
                    alpha=0.10, color=cfg["color"], zorder=1)
    ax.fill_between(df["date"], df["sth_sopr"], lower,
                    where=df["sth_sopr"] < lower,
                    alpha=0.30, color=cfg["color"], zorder=2, label="_")

    # Band lines
    ax.plot(df["date"], upper, color=cfg["color"], lw=0.7, alpha=0.55, linestyle="--")
    ax.plot(df["date"], sma,   color=cfg["color"], lw=0.5, alpha=0.35, linestyle=":")
    ax.plot(df["date"], lower, color=cfg["color"], lw=1.0, alpha=0.80, linestyle="--")

    # STH-SOPR
    ax.plot(df["date"], df["sth_sopr"],
            color="#e2e8f0", lw=0.85, alpha=0.90, zorder=3)

    # 1.0 line
    ax.axhline(1.0, color="#4b5563", lw=0.8, zorder=2)
    ax.text(df["date"].min() + pd.Timedelta(days=3), 1.001,
            "1.0", color="#6b7280", fontsize=7)

    # ── Bull signals ──────────────────────────────────────────────────────────
    if bull_sigs:
        sig_rows = df[df["date"].isin(bull_sigs)].copy()
        ax.scatter(sig_rows["date"], sig_rows["sth_sopr"],
                   color="#10b981", s=90, zorder=7, marker="^",
                   edgecolors="#ffffff", linewidths=0.6)

        # Annotate G30d for EACH signal
        for _, row in sig_rows.iterrows():
            g = fwd_gain(df, row["date"], days=30)
            if g is not None:
                label = f"+{g:.0f}%" if g >= 0 else f"{g:.0f}%"
                col   = "#10b981" if g >= 0 else "#ef4444"
                ax.annotate(
                    label,
                    xy=(row["date"], row["sth_sopr"]),
                    xytext=(0, -16), textcoords="offset points",
                    color=col, fontsize=7, ha="center", va="top",
                    fontweight="bold", zorder=8)

        # Count label
        ax.text(0.003, 0.94, f"▲ {len(bull_sigs)} bull signals",
                transform=ax.transAxes, color="#10b981",
                fontsize=8, va="top", fontweight="bold")

    # ── Bear FPs ──────────────────────────────────────────────────────────────
    if bear_sigs:
        bear_rows = df[df["date"].isin(bear_sigs)].copy()
        ax.scatter(bear_rows["date"], bear_rows["sth_sopr"],
                   color="#ef4444", s=90, zorder=7, marker="v",
                   edgecolors="#ffffff", linewidths=0.6)
        ax.text(0.003, 0.06, f"▼ {len(bear_sigs)} bear FP",
                transform=ax.transAxes, color="#ef4444",
                fontsize=8, va="bottom", fontweight="bold")

    # Stats box
    ax.text(0.998, 0.97, cfg["stats"],
            transform=ax.transAxes, color="#cbd5e1", fontsize=7.8,
            ha="right", va="top",
            bbox=dict(facecolor="#1e293b", edgecolor="#334155",
                      boxstyle="round,pad=0.35", alpha=0.9))

    # Panel label (left)
    ax.set_ylabel(cfg["label"], fontsize=9, color=cfg["color"], fontweight="bold")

    # Y limits — fixed range to match reference chart style
    ax.set_ylim(0.895, 1.115)

# ── Shared legend ─────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color="#10b981", label="▲ Bull entry signal (lower band touch, bull period)"),
    mpatches.Patch(color="#ef4444", label="▼ Bear FP — ignore (S2 latch active)"),
    mpatches.Patch(color="#e2e8f0", alpha=0.7, label="STH-SOPR daily"),
    mpatches.Patch(color="#7f1d1d", alpha=0.5, label="Bear market (Nov 2025 →)"),
    mpatches.Patch(color="#6b7280", alpha=0.4, label="Bands: Upper / SMA / Lower"),
]
axs[4].legend(handles=legend_items, loc="lower right",
              facecolor="#1e293b", edgecolor="#334155",
              labelcolor="#cbd5e1", fontsize=8.5, ncol=3,
              handlelength=1.2, borderpad=0.8)

plt.savefig("sth_sopr_bb_compare.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
print("Saved: sth_sopr_bb_compare.png")
