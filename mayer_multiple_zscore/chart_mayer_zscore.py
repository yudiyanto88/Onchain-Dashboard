"""
Mayer Multiple Z-Score - meniru chart checkonchain "The Mayer Multiple Z-score".

Rumus (dicocokkan ke angka di chart checkonchain, bukan dari dokumentasi resmi):
  Mayer Multiple (MM) = harga / 200DMA
  Z = (ln MM - rata2 ln MM) / SD ln MM
  rata2 & SD = expanding (semua data sejak 2012-01-01 s/d hari itu, tanpa
  melihat masa depan). Z mulai dihitung sesudah 365 hari data.
  Band harga di level Z = k:  200DMA * exp(rata2 + k * SD)

Titik penanda: puncak tiap episode Z > +1.5 (merah), dasar tiap episode
Z < -1.5 (hijau), dan nilai hari terakhir (abu).

Output: data_mayer_zscore.csv dan mayer_zscore.png di folder ini.
Jalankan dari root repo:  python mayer_multiple_zscore/chart_mayer_zscore.py
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = Path(__file__).resolve().parent

STATS_START = "2012-01-01"   # awal data untuk rata2 & SD
MIN_DAYS = 365               # Z baru muncul sesudah 1 tahun data
CHART_START = "2015-01-01"
BANDS = [1.5, 1.0, -1.0, -1.5]
EXTREME = 1.5
EPISODE_GAP = 90             # hari; pemisah antar episode ekstrem

SURFACE = "#1a1a19"
INK_PRIMARY = "#ffffff"
INK_SECONDARY = "#c3c2b7"
INK_MUTED = "#898781"
GRID = "#2c2c2a"
PRICE_COLOR = "#e8e6dc"
DMA_COLOR = "#3987e5"
Z_COLOR = "#F7931A"
BAND_COLORS = {1.5: "#e34948", 1.0: "#d9a441", -1.0: "#3987e5", -1.5: "#2fb89a"}
TOP_COLOR = "#e34948"
BOTTOM_COLOR = "#3fbf4a"
NOW_COLOR = "#9a9993"


def build():
    df = pd.read_csv(ROOT / "data_price_level.csv", parse_dates=["date"])
    df = df[["date", "btc_price"]].set_index("date")
    df["dma200"] = df["btc_price"].rolling(200).mean()
    df["mayer_multiple"] = df["btc_price"] / df["dma200"]

    ln_mm = np.log(df.loc[STATS_START:, "mayer_multiple"])
    mean = ln_mm.expanding(MIN_DAYS).mean()
    sd = ln_mm.expanding(MIN_DAYS).std()
    df["ln_mm_mean"] = mean
    df["ln_mm_sd"] = sd
    df["mayer_z"] = (ln_mm - mean) / sd
    for k in BANDS:
        df[f"price_{k:+.1f}sd"] = df["dma200"] * np.exp(mean + k * sd)
    return df


def episode_extremes(z, level):
    """Satu titik per episode: puncak saat z > level (level > 0) atau dasar saat z < level.
    Hari lewat batas yang berjarak < EPISODE_GAP hari dianggap satu episode."""
    hit = z[z > level] if level > 0 else z[z < level]
    episode = (hit.index.to_series().diff().dt.days > EPISODE_GAP).cumsum()
    return [seg.idxmax() if level > 0 else seg.idxmin() for _, seg in hit.groupby(episode)]


def style_axis(ax):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.6)
    ax.tick_params(colors=INK_SECONDARY, labelsize=9)
    for s in ax.spines.values():
        s.set_visible(False)


def chart(df):
    d = df[CHART_START:].dropna(subset=["mayer_z"])
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(18, 10), sharex=True, facecolor=SURFACE,
        gridspec_kw={"height_ratios": [3, 2], "hspace": 0.05},
    )
    style_axis(ax1)
    style_axis(ax2)

    # Panel atas: harga, 200DMA, band harga
    for k in BANDS:
        ax1.plot(d.index, d[f"price_{k:+.1f}sd"], color=BAND_COLORS[k],
                 linestyle="--", linewidth=1, alpha=0.6, label=f"Price {k:+.1f}sd")
    ax1.plot(d.index, d["dma200"], color=DMA_COLOR, linewidth=2, label="200DMA")
    ax1.plot(d.index, d["btc_price"], color=PRICE_COLOR, linewidth=1, label="Price")
    ax1.set_yscale("log")
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(
        lambda v, _: f"${v/1000:,.0f}k" if v >= 1000 else f"${v:,.0f}"))
    ax1.set_ylabel("Price (USD, log)", color=INK_SECONDARY)

    # Panel bawah: Z-score
    ax2.axhline(0, color=INK_MUTED, linewidth=1)
    for k in BANDS:
        ax2.axhline(k, color=BAND_COLORS[k], linestyle="--", linewidth=1, alpha=0.8)
        ax2.text(1.002, k, f"{k:+.1f}sd", transform=ax2.get_yaxis_transform(),
                 color=INK_SECONDARY, fontsize=8, va="center")
    ax2.plot(d.index, d["mayer_z"], color=Z_COLOR, linewidth=1.2, label="Mayer Multiple Z")
    ax2.set_ylabel("Mayer Multiple Z-Score", color=INK_SECONDARY)

    # Penanda episode ekstrem + hari terakhir
    marks = [(t, TOP_COLOR) for t in episode_extremes(d["mayer_z"], EXTREME)]
    marks += [(t, BOTTOM_COLOR) for t in episode_extremes(d["mayer_z"], -EXTREME)]
    for t, c in marks:
        ax1.scatter(t, d.at[t, "btc_price"], s=90, color=c, edgecolor=SURFACE,
                    linewidth=2, zorder=5)
        ax2.scatter(t, d.at[t, "mayer_z"], s=60, color=c, edgecolor=SURFACE,
                    linewidth=2, zorder=5)
    last = d.index[-1]
    ax1.scatter(last, d.at[last, "btc_price"], s=110, color=NOW_COLOR,
                edgecolor=SURFACE, linewidth=2, zorder=6)
    ax2.scatter(last, d.at[last, "mayer_z"], s=70, color=NOW_COLOR,
                edgecolor=SURFACE, linewidth=2, zorder=6)
    ax2.annotate(
        f"{last:%d %b %Y}\nZ {d.at[last, 'mayer_z']:+.2f} | MM {d.at[last, 'mayer_multiple']:.2f}",
        (last, d.at[last, "mayer_z"]), xytext=(-12, 22), textcoords="offset points",
        ha="right", color=INK_PRIMARY, fontsize=9)

    ax2.xaxis.set_major_locator(mdates.YearLocator())
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    leg = ax1.legend(loc="upper left", ncol=6, fontsize=9, frameon=False)
    for t in leg.get_texts():
        t.set_color(INK_SECONDARY)

    fig.suptitle("The Mayer Multiple Z-Score", color=INK_PRIMARY, fontsize=16, y=0.95)
    fig.text(0.5, 0.915,
             "MM = Price / 200DMA  ·  Z = (ln MM − expanding mean) / expanding SD, "
             f"since {STATS_START[:4]}  ·  red/green = extreme of each episode beyond ±{EXTREME}sd",
             ha="center", color=INK_MUTED, fontsize=9)
    out = OUT_DIR / "mayer_zscore.png"
    fig.savefig(out, dpi=110, facecolor=SURFACE, bbox_inches="tight")
    return out


if __name__ == "__main__":
    df = build()
    cols = ["btc_price", "dma200", "mayer_multiple", "mayer_z"] + [f"price_{k:+.1f}sd" for k in BANDS]
    df[cols].dropna(subset=["dma200"]).round(6).to_csv(OUT_DIR / "data_mayer_zscore.csv")
    print("chart:", chart(df))
    last = df.dropna(subset=["mayer_z"]).iloc[-1]
    print(f"terakhir {df.index[-1]:%Y-%m-%d}: price {last.btc_price:,.0f}  200DMA {last.dma200:,.0f}  "
          f"MM {last.mayer_multiple:.3f}  Z {last.mayer_z:+.2f}")
    for k in BANDS:
        print(f"  Price {k:+.1f}sd = {last[f'price_{k:+.1f}sd']:,.0f}")
