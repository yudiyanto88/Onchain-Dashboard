"""
Chart price vs SSR (proxy) dan price vs MVRV Monthly Delta, dengan penanda
di tanggal-tanggal V-shape correction yang mau dicek sebagai kandidat sinyal buy:
6-9 Mar 2023, 21 Jan 2024, 5 Sep 2020, 14-16 Jul 2017, 13-15 Sep 2017, 21 Sep 2021.

Catatan: SSR baru punya data dari 29 Nov 2017 (data stablecoin supply belum ada
sebelum itu) - jadi 2 event Jul & Sep 2017 tidak akan tampil di chart SSR.
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
METRIC_COLOR = "#eda100"   # yellow, beda dari price supaya jelas 2 series-nya
EVENT_COLOR = "#e34948"    # red marker utk tanggal V-shape

START_DATE = "2016-06-01"

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
                rotation=90, va="top" if y_label_pos > 0 else "bottom", ha="center")


def build_chart(metric_col, metric_label, out_path, hline_zero=False, metric_log=False, pct_style=False):
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
        f"BTC Price vs {metric_label} — cek kandidat sinyal V-shape correction",
        color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12,
    )

    ax_metric.plot(df["date"], df[metric_col], color=METRIC_COLOR, linewidth=1.1)
    if metric_log:
        ax_metric.set_yscale("log")
    if hline_zero:
        ax_metric.axhline(0, color=INK_MUTED, linewidth=0.8, linestyle="--", alpha=0.6)
    if pct_style:
        ax_metric.axhline(0.30, color="#0ca30c", linewidth=0.8, linestyle="--", alpha=0.8)
        ax_metric.axhline(0.70, color="#d03b3b", linewidth=0.8, linestyle="--", alpha=0.8)
        ax_metric.set_ylim(0, 1)
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
        "Garis merah putus-putus = tanggal V-shape correction yang dicek. "
        "SSR baru ada data dari 29 Nov 2017 (2 event Jul/Sep 2017 tidak tampil di chart SSR).",
        color=INK_MUTED, fontsize=7.5,
    )

    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(out_path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {out_path}")


build_chart("pct_ssr", "SSR percentile rank (rolling 2yr, 0=low/dry-powder, 1=high)", "price_vs_ssr.png", pct_style=True)
build_chart("raw_mvrv_delta", "MVRV Monthly Delta", "price_vs_mvrv_delta.png", hline_zero=True)
