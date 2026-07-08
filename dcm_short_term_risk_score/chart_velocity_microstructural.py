"""
Chart price vs Velocity RSI, dan price vs Microstructural Risk - 2 gambar
terpisah, dengan penanda tanggal V-shape correction yang sama seperti
chart_vshape_check.py, supaya bisa langsung dianalisa dan dibandingkan.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

SURFACE = "#1a1a19"
INK_PRIMARY = "#ffffff"
INK_SECONDARY = "#c3c2b7"
INK_MUTED = "#898781"
GRID = "#2c2c2a"
BASELINE = "#383835"
PRICE_COLOR = "#3987e5"
METRIC_COLOR = "#eda100"
EVENT_COLOR = "#e34948"

START_DATE = "2011-07-01"

EVENTS = [
    ("6-9 Mar 2023", "2023-03-06", "2023-03-09"),
    ("21 Jan 2024", "2024-01-21", "2024-01-21"),
    ("5 Sep 2020", "2020-09-05", "2020-09-05"),
    ("14-16 Jul 2017", "2017-07-14", "2017-07-16"),
    ("13-15 Sep 2017", "2017-09-13", "2017-09-15"),
    ("21 Sep 2021", "2021-09-21", "2021-09-21"),
]

df = pd.read_csv("data_short_term_risk_score.csv", parse_dates=["date"])
df = df[df["date"] >= START_DATE].reset_index(drop=True)


def mark_events(ax, y_label_pos):
    for label, d0, d1 in EVENTS:
        mid = pd.Timestamp(d0) + (pd.Timestamp(d1) - pd.Timestamp(d0)) / 2
        ax.axvline(mid, color=EVENT_COLOR, linewidth=0.9, linestyle=":", alpha=0.85)
        ax.text(mid, y_label_pos, f" {label}", color=EVENT_COLOR, fontsize=7,
                rotation=90, va="top", ha="center")


def build_chart(metric_col, metric_label, out_path, hlines=None, ylim=None):
    fig, (ax_price, ax_metric) = plt.subplots(
        2, 1, figsize=(18, 8), sharex=True,
        gridspec_kw={"height_ratios": [2, 1.3]}, facecolor=SURFACE,
    )
    for ax in (ax_price, ax_metric):
        ax.set_facecolor(SURFACE)
        ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
        for spine in ax.spines.values():
            spine.set_color(BASELINE)
        ax.tick_params(colors=INK_MUTED, labelsize=9)

    ax_price.plot(df["date"], df["btc_price"], color=PRICE_COLOR, linewidth=1.2)
    ax_price.set_yscale("log")
    ax_price.set_ylabel("BTC Price (log)", color=INK_SECONDARY, fontsize=10)
    ax_price.set_title(
        f"BTC Price vs {metric_label}",
        color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12,
    )

    ax_metric.plot(df["date"], df[metric_col], color=METRIC_COLOR, linewidth=1.0)
    if hlines:
        for y, color in hlines:
            ax_metric.axhline(y, color=color, linewidth=0.8, linestyle="--", alpha=0.8)
    if ylim:
        ax_metric.set_ylim(*ylim)
    ax_metric.set_ylabel(metric_label, color=INK_SECONDARY, fontsize=10)

    y_top = ax_price.get_ylim()[1]
    mark_events(ax_price, y_top)
    y_metric_top = ax_metric.get_ylim()[1]
    mark_events(ax_metric, y_metric_top)

    ax_metric.xaxis.set_major_locator(mdates.YearLocator())
    ax_metric.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
    ax_metric.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    fig.text(
        0.01, 0.01,
        "Garis merah putus-putus = tanggal V-shape correction referensi.",
        color=INK_MUTED, fontsize=7.5,
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(out_path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {out_path}")


build_chart(
    "raw_velocity_rsi", "Velocity RSI (RSI-14 of 14d ROC)", "price_vs_velocity_rsi.png",
    hlines=[(30, "#0ca30c"), (50, "#898781"), (70, "#d03b3b")], ylim=(0, 100),
)
build_chart(
    "raw_microstructural", "Microstructural Risk (vol14 + |dist 200DMA|, blended pct)",
    "price_vs_microstructural.png",
    hlines=[(0.30, "#0ca30c"), (0.70, "#d03b3b")], ylim=(0, 1),
)
