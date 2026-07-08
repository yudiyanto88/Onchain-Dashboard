"""
Chart per-metrik untuk 3 kandidat sinyal V-shape correction:
  1. Price vs MIN(aSOPR, STH-SOPR) - threshold 0.98
  2. Price vs STH % supply in loss - threshold 40% + filter rate-of-change (naik >=10pt/5hari)
  3. Price vs RSI14 + Bollinger Bands (30, 1.5) - breach lower band

Tiap chart shading area di mana kondisi sinyal aktif, plus penanda 6 tanggal
V-shape correction referensi.
"""

import numpy as np
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
BAND_COLOR = "#4a3aa7"
SIGNAL_COLOR = "#0ca30c"
EVENT_COLOR = "#e34948"

START_DATE = "2016-01-01"

EVENTS = [
    ("6-9 Mar 2023", "2023-03-06", "2023-03-09"),
    ("21 Jan 2024", "2024-01-21", "2024-01-21"),
    ("5 Sep 2020", "2020-09-05", "2020-09-05"),
    ("14-16 Jul 2017", "2017-07-14", "2017-07-16"),
    ("13-15 Sep 2017", "2017-09-13", "2017-09-15"),
    ("21 Sep 2021", "2021-09-21", "2021-09-21"),
]


def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1 / period, min_periods=period, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    return 100 - (100 / (1 + rs))


df = pd.read_csv("../data_master_all_metrics.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True).dropna(subset=["btc_price"]).reset_index(drop=True)

df["min_sopr"] = df[["asopr", "sth_sopr"]].min(axis=1)
df["sth_loss_chg5"] = df["pct_sth_in_loss"].diff(5)
df["rsi14"] = rsi(df["btc_price"])
bb_mid = df["rsi14"].rolling(30).mean()
bb_std = df["rsi14"].rolling(30).std()
df["bb_lower"] = bb_mid - 1.5 * bb_std
df["bb_upper"] = bb_mid + 1.5 * bb_std

df = df[df["date"] >= START_DATE].reset_index(drop=True)


def base_fig():
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
    return fig, ax_price, ax_metric


def shade_signal(ax_list, mask, color, alpha=0.18):
    dates = df["date"].values
    m = mask.values
    in_span, start = False, None
    for i in range(len(m)):
        if m[i] and not in_span:
            start, in_span = dates[i], True
        elif not m[i] and in_span:
            for ax in ax_list:
                ax.axvspan(start, dates[i], color=color, alpha=alpha, linewidth=0)
            in_span = False
    if in_span:
        for ax in ax_list:
            ax.axvspan(start, dates[-1], color=color, alpha=alpha, linewidth=0)


def mark_events(ax, y_top):
    for label, d0, d1 in EVENTS:
        mid = pd.Timestamp(d0) + (pd.Timestamp(d1) - pd.Timestamp(d0)) / 2
        ax.axvline(mid, color=EVENT_COLOR, linewidth=0.9, linestyle=":", alpha=0.85)
        ax.text(mid, y_top, f" {label}", color=EVENT_COLOR, fontsize=7,
                rotation=90, va="top", ha="center")


def finish(fig, ax_price, ax_metric, out_path, footer):
    y_top = ax_price.get_ylim()[1]
    mark_events(ax_price, y_top)
    mark_events(ax_metric, ax_metric.get_ylim()[1])
    ax_metric.xaxis.set_major_locator(mdates.YearLocator())
    ax_metric.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
    ax_metric.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    fig.text(0.01, 0.01, footer, color=INK_MUTED, fontsize=7.5)
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    plt.savefig(out_path, dpi=150, facecolor=SURFACE)
    plt.close(fig)
    print(f"Saved {out_path}")


# ─── CHART 1: MIN(aSOPR, STH-SOPR) ──────────────────────────────────────────

fig, ax_price, ax_metric = base_fig()
ax_price.set_title("BTC Price vs MIN(aSOPR, STH-SOPR) — threshold <=0.98",
                    color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12)
signal = df["min_sopr"] <= 0.98
shade_signal([ax_price, ax_metric], signal, SIGNAL_COLOR)
ax_metric.plot(df["date"], df["min_sopr"], color=METRIC_COLOR, linewidth=1.0)
ax_metric.axhline(0.98, color=SIGNAL_COLOR, linewidth=0.9, linestyle="--", alpha=0.85)
ax_metric.axhline(1.0, color=INK_MUTED, linewidth=0.7, linestyle=":", alpha=0.5)
ax_metric.set_ylabel("MIN(aSOPR, STH-SOPR)", color=INK_SECONDARY, fontsize=10)
finish(fig, ax_price, ax_metric, "price_vs_sopr_signal.png",
       "Area hijau = MIN(aSOPR,STH-SOPR) <= 0.98 (signal aktif). Garis merah putus-putus = tanggal V-shape referensi.")

# ─── CHART 2: STH % supply in loss (+ filter rate-of-change) ──────────────

fig, ax_price, ax_metric = base_fig()
ax_price.set_title("BTC Price vs STH % Supply in Loss — level >=40% & naik >=10pt/5hari",
                    color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12)
signal_raw = df["pct_sth_in_loss"] >= 40
signal_filtered = signal_raw & (df["sth_loss_chg5"] >= 10)
shade_signal([ax_price, ax_metric], signal_raw & ~signal_filtered, INK_MUTED, alpha=0.10)
shade_signal([ax_price, ax_metric], signal_filtered, SIGNAL_COLOR)
ax_metric.plot(df["date"], df["pct_sth_in_loss"], color=METRIC_COLOR, linewidth=1.0)
ax_metric.axhline(40, color=SIGNAL_COLOR, linewidth=0.9, linestyle="--", alpha=0.85)
ax_metric.set_ylabel("STH % Supply in Loss", color=INK_SECONDARY, fontsize=10)
finish(fig, ax_price, ax_metric, "price_vs_sthloss_signal.png",
       "Hijau = level>=40% DAN naik>=10pt/5hari (filtered signal). Abu-abu = level>=40% saja tanpa rate-of-change (noise yg difilter). Garis merah = tanggal referensi.")

# ─── CHART 3: RSI14 + BB(30, 1.5) ───────────────────────────────────────────

fig, ax_price, ax_metric = base_fig()
ax_price.set_title("BTC Price vs RSI14 + Bollinger Bands (30, 1.5) — breach lower band",
                    color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12)
signal = df["rsi14"] <= df["bb_lower"]
shade_signal([ax_price, ax_metric], signal, SIGNAL_COLOR)
ax_metric.fill_between(df["date"], df["bb_lower"], df["bb_upper"], color=BAND_COLOR, alpha=0.25, linewidth=0)
ax_metric.plot(df["date"], df["rsi14"], color=METRIC_COLOR, linewidth=1.0, label="RSI14")
ax_metric.plot(df["date"], df["bb_lower"], color=BAND_COLOR, linewidth=0.8, alpha=0.8, label="BB lower/upper (30, 1.5)")
ax_metric.plot(df["date"], df["bb_upper"], color=BAND_COLOR, linewidth=0.8, alpha=0.8)
ax_metric.set_ylabel("RSI14", color=INK_SECONDARY, fontsize=10)
ax_metric.legend(loc="upper left", frameon=False, fontsize=8, labelcolor=INK_SECONDARY)
finish(fig, ax_price, ax_metric, "price_vs_rsi_bb_signal.png",
       "Area hijau = RSI14 tembus di bawah BB lower band (signal aktif). Garis merah putus-putus = tanggal V-shape referensi.")
