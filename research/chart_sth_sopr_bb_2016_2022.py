"""
STH-SOPR Bollinger Band — 2016-2022 Historical Comparison
Same 4 settings: BB(28,1.5) vs BB(28,2.0) vs BB(28,2.5) vs BB(60,2.25)
Two bull cycles: 2016-2017 and 2020-2021
Two bear markets: 2018 and 2022
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

START = pd.Timestamp("2016-01-01")
END   = pd.Timestamp("2022-12-31")
df    = df[(df["date"] >= START) & (df["date"] <= END)].copy().reset_index(drop=True)

# ── Market regime definitions ─────────────────────────────────────────────────
# Bull periods: price in bull market (for signal evaluation)
BULL_PERIODS = [
    (pd.Timestamp("2016-01-01"), pd.Timestamp("2017-12-17")),   # Cycle 1 peak
    (pd.Timestamp("2019-01-01"), pd.Timestamp("2019-06-26")),   # 2019 mini bull
    (pd.Timestamp("2020-03-13"), pd.Timestamp("2021-11-10")),   # Cycle 2 peak (excl. COVID crash)
]

# Bear periods: for shading + FP counting
BEAR_PERIODS = [
    (pd.Timestamp("2017-12-18"), pd.Timestamp("2019-01-31")),
    (pd.Timestamp("2021-11-11"), pd.Timestamp("2022-12-31")),
]

def in_bull(d):
    return any(s <= d <= e for s, e in BULL_PERIODS)

def in_bear(d):
    return any(s <= d <= e for s, e in BEAR_PERIODS)

df["is_bull"] = df["date"].apply(in_bull)
df["is_bear"] = df["date"].apply(in_bear)

# ── Find bull dip bottoms ─────────────────────────────────────────────────────
def find_dip_bottoms(df_in, lookback=30, min_drop_pct=10, merge_days=14):
    prices = df_in["btc_price"].reset_index(drop=True)
    dates  = df_in["date"].reset_index(drop=True)
    rolling_max = prices.rolling(lookback, min_periods=1).max()
    pct_from_peak = (prices / rolling_max - 1) * 100

    bottoms, in_dip, best_px, best_dt = [], False, np.inf, None
    for i in range(len(prices)):
        if pct_from_peak.iloc[i] <= -min_drop_pct:
            if not in_dip:
                in_dip = True
            if prices.iloc[i] < best_px:
                best_px, best_dt = prices.iloc[i], dates.iloc[i]
        else:
            if in_dip:
                bottoms.append({"date": best_dt, "price": best_px})
                in_dip, best_px, best_dt = False, np.inf, None
    if in_dip and best_dt:
        bottoms.append({"date": best_dt, "price": best_px})

    # merge nearby
    merged = []
    for b in bottoms:
        if merged and (b["date"] - merged[-1]["date"]).days < merge_days:
            if b["price"] < merged[-1]["price"]:
                merged[-1] = b
        else:
            merged.append(b)
    return pd.DataFrame(merged) if merged else pd.DataFrame(columns=["date", "price"])


df_bull_only = df[df["is_bull"]].copy()
bull_dips = find_dip_bottoms(df_bull_only, lookback=30, min_drop_pct=10)
dip_dates = pd.to_datetime(bull_dips["date"].tolist())

print(f"Bull dip bottoms identified ({len(bull_dips)} events):")
for _, r in bull_dips.iterrows():
    print(f"  {r['date'].date()} | ${r['price']:>9,.0f}")

# ── BB helpers ────────────────────────────────────────────────────────────────
def compute_bb(sth_series, period, std_dev):
    sma   = sth_series.rolling(period, min_periods=period).mean()
    sigma = sth_series.rolling(period, min_periods=period).std()
    return sma, sma + std_dev * sigma, sma - std_dev * sigma

def get_signals(df_in, period, std_dev, dedup_days=7):
    sma, upper, lower = compute_bb(df_in["sth_sopr"], period, std_dev)
    below    = df_in["sth_sopr"] < lower
    first_ep = below & ~below.shift(1, fill_value=False)

    bull_mask = first_ep & df_in["is_bull"]
    bear_mask = first_ep & df_in["is_bear"]

    def dedup(dates):
        out = []
        for d in dates:
            if not out or (d - out[-1]).days > dedup_days:
                out.append(d)
        return out

    return sma, upper, lower, dedup(df_in[bull_mask]["date"].tolist()), \
                               dedup(df_in[bear_mask]["date"].tolist())

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

# ── Evaluate each setting ─────────────────────────────────────────────────────
def evaluate(df_in, period, std_dev, dip_dates_ts,
             pre_window=21, post_window=7, dedup_days=7):
    _, _, _, bull_sigs, bear_sigs = get_signals(df_in, period, std_dev, dedup_days)
    n_dips = len(dip_dates_ts)

    dips_covered = set()
    true_sigs = 0
    for s in bull_sigs:
        for i, dip_dt in enumerate(dip_dates_ts):
            delta = (dip_dt - s).days
            if -post_window <= delta <= pre_window:
                dips_covered.add(i)
                true_sigs += 1
                break

    recall    = len(dips_covered) / n_dips * 100 if n_dips else 0
    precision = true_sigs / len(bull_sigs)   * 100 if bull_sigs else 0

    gains_30 = []
    for s in bull_sigs:
        g = fwd_gain(df_in, s, 30)
        if g is not None:
            gains_30.append(g)

    return dict(recall=round(recall, 1), precision=round(precision, 1),
                n_bull=len(bull_sigs), n_bear_fp=len(bear_sigs),
                avg_g30=round(np.mean(gains_30), 1) if gains_30 else None)

SETTINGS = [
    dict(period=28, std=1.5,  label="BB(28, 1.5)   High Recall",      color="#27ae60"),
    dict(period=28, std=2.0,  label="BB(28, 2.0)   Image Baseline",    color="#e67e22"),
    dict(period=28, std=2.5,  label="BB(28, 2.5)   Best Score ★",      color="#e74c3c"),
    dict(period=60, std=2.25, label="BB(60, 2.25)  Best 60d Gain",     color="#8e44ad"),
]

print("\nEvaluation (2016-2022):")
for cfg in SETTINGS:
    r = evaluate(df, cfg["period"], cfg["std"], dip_dates)
    cfg["stats_hist"] = (f"Recall {r['recall']}%  |  Precision {r['precision']}%  |  "
                         f"Avg G30d +{r['avg_g30']}%  |  "
                         f"Bull sigs {r['n_bull']}  |  Bear FP {r['n_bear_fp']}")
    print(f"  BB({cfg['period']},{cfg['std']}): {cfg['stats_hist']}")

# ── Figure ────────────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(22, 28), facecolor="#0d1117")
gs  = GridSpec(5, 1, figure=fig, hspace=0.06,
               height_ratios=[2.0, 1.3, 1.3, 1.3, 1.3],
               top=0.97, bottom=0.05, left=0.07, right=0.98)
axs = [fig.add_subplot(gs[i]) for i in range(5)]

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
    ax.grid(which="major", axis="x", color="#1f2937", lw=0.5, zorder=0)
    ax.grid(which="major", axis="y", color="#1f2937", lw=0.5, zorder=0)

def shade_bears(ax, alpha_price=False):
    for s, e in BEAR_PERIODS:
        s = max(s, df["date"].min())
        e = min(e, df["date"].max())
        ax.axvspan(s, e, color="#7f1d1d33", zorder=0)
        ax.axvline(s, color="#dc2626", lw=0.8, linestyle="--", alpha=0.6, zorder=4)

# ─────────────────────────────────────────────────────────────────────────────
# Panel 0: BTC Price
# ─────────────────────────────────────────────────────────────────────────────
ax0 = axs[0]
style_ax(ax0)
shade_bears(ax0)

ax0.fill_between(df["date"], df["btc_price"], df["btc_price"].min() * 0.5,
                 alpha=0.08, color="#3b82f6")
ax0.semilogy(df["date"], df["btc_price"],
             color="#93c5fd", lw=1.0, alpha=0.95, zorder=3)

ax0.scatter(bull_dips["date"], bull_dips["price"],
            color="#10b981", s=80, zorder=5, marker="o",
            edgecolors="#ffffff", linewidths=0.6)

ax0.set_ylabel("BTC / USD (log)", fontsize=9, color="#9ca3af")
ax0.yaxis.set_major_formatter(ticker.FuncFormatter(
    lambda x, _: f"${x/1000:.0f}K" if x >= 1000 else f"${x:.0f}"))

ax0.set_title(
    "STH-SOPR Bollinger Band — 2016–2022 Historical Validation\n"
    "● = Identified bull dip bottoms   |   Red zones = Bear markets (2018, 2022)",
    color="#f9fafb", fontsize=11.5, pad=10, loc="left", fontweight="bold")

# Label bear zones on price panel
for s, e in BEAR_PERIODS:
    mid = s + (e - s) / 2
    ax0.text(mid, df["btc_price"].max() * 0.6, "BEAR",
             color="#ef4444", fontsize=9, ha="center", fontweight="bold",
             alpha=0.7, zorder=6)

# ─────────────────────────────────────────────────────────────────────────────
# Panels 1-4: STH-SOPR + BB
# ─────────────────────────────────────────────────────────────────────────────
for idx, cfg in enumerate(SETTINGS):
    ax   = axs[idx + 1]
    show = (idx == 3)
    style_ax(ax, show_xlabels=show)
    shade_bears(ax)

    sma, upper, lower, bull_sigs, bear_sigs = get_signals(
        df, cfg["period"], cfg["std"])

    # Fill between bands
    ax.fill_between(df["date"], lower, upper,
                    alpha=0.10, color=cfg["color"], zorder=1)
    ax.fill_between(df["date"], df["sth_sopr"], lower,
                    where=df["sth_sopr"] < lower,
                    alpha=0.30, color=cfg["color"], zorder=2)

    ax.plot(df["date"], upper, color=cfg["color"], lw=0.7, alpha=0.55, linestyle="--")
    ax.plot(df["date"], sma,   color=cfg["color"], lw=0.5, alpha=0.35, linestyle=":")
    ax.plot(df["date"], lower, color=cfg["color"], lw=1.0, alpha=0.80, linestyle="--")
    ax.plot(df["date"], df["sth_sopr"],
            color="#e2e8f0", lw=0.85, alpha=0.90, zorder=3)
    ax.axhline(1.0, color="#4b5563", lw=0.8, zorder=2)
    ax.text(df["date"].min() + pd.Timedelta(days=3), 1.001,
            "1.0", color="#6b7280", fontsize=7)

    # Bull signals
    if bull_sigs:
        sig_rows = df[df["date"].isin(bull_sigs)].copy()
        ax.scatter(sig_rows["date"], sig_rows["sth_sopr"],
                   color="#10b981", s=90, zorder=7, marker="^",
                   edgecolors="#ffffff", linewidths=0.6)
        for _, row in sig_rows.iterrows():
            g = fwd_gain(df, row["date"], days=30)
            if g is not None:
                label = f"+{g:.0f}%" if g >= 0 else f"{g:.0f}%"
                col   = "#10b981" if g >= 0 else "#ef4444"
                ax.annotate(label,
                    xy=(row["date"], row["sth_sopr"]),
                    xytext=(0, -16), textcoords="offset points",
                    color=col, fontsize=7, ha="center", va="top",
                    fontweight="bold", zorder=8)
        ax.text(0.003, 0.94, f"▲ {len(bull_sigs)} bull signals",
                transform=ax.transAxes, color="#10b981",
                fontsize=8, va="top", fontweight="bold")

    # Bear FPs
    if bear_sigs:
        bear_rows = df[df["date"].isin(bear_sigs)].copy()
        ax.scatter(bear_rows["date"], bear_rows["sth_sopr"],
                   color="#ef4444", s=90, zorder=7, marker="v",
                   edgecolors="#ffffff", linewidths=0.6)
        ax.text(0.003, 0.06, f"▼ {len(bear_sigs)} bear FP",
                transform=ax.transAxes, color="#ef4444",
                fontsize=8, va="bottom", fontweight="bold")

    # Stats box
    ax.text(0.998, 0.97, cfg["stats_hist"],
            transform=ax.transAxes, color="#cbd5e1", fontsize=7.8,
            ha="right", va="top",
            bbox=dict(facecolor="#1e293b", edgecolor="#334155",
                      boxstyle="round,pad=0.35", alpha=0.9))

    ax.set_ylabel(cfg["label"], fontsize=9, color=cfg["color"], fontweight="bold")
    ax.set_ylim(0.895, 1.115)

# ── Legend ────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color="#10b981", label="▲ Bull entry signal (lower band touch)"),
    mpatches.Patch(color="#ef4444", label="▼ Bear FP (fired during bear market)"),
    mpatches.Patch(color="#e2e8f0", alpha=0.7, label="STH-SOPR daily"),
    mpatches.Patch(color="#7f1d1d", alpha=0.5, label="Bear market zones (2018, 2022)"),
    mpatches.Patch(color="#6b7280", alpha=0.4, label="Bands: Upper / SMA / Lower"),
]
axs[4].legend(handles=legend_items, loc="lower right",
              facecolor="#1e293b", edgecolor="#334155",
              labelcolor="#cbd5e1", fontsize=8.5, ncol=3,
              handlelength=1.2, borderpad=0.8)

for ax in axs:
    ax.set_xlim(df["date"].min(), df["date"].max())

plt.savefig("sth_sopr_bb_2016_2022.png", dpi=150, bbox_inches="tight",
            facecolor="#0d1117")
print("Saved: sth_sopr_bb_2016_2022.png")
