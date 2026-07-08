import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker
from matplotlib.gridspec import GridSpec

df = pd.read_csv("data_momentum.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[["date","btc_price","sth_sopr"]].dropna()

PERIOD_DEFS = {
    "2023-2025": dict(
        start="2023-01-01", end="2026-06-17",
        bull=[("2023-01-01","2025-10-31")],
        bear=[("2025-11-01","2026-06-17")],
        bear_label="BEAR\nS2 LATCH",
    ),
    "2016-2022": dict(
        start="2016-01-01", end="2022-12-31",
        bull=[("2016-01-01","2017-12-17"),("2019-01-01","2019-06-26"),("2020-03-13","2021-11-10")],
        bear=[("2017-12-18","2019-01-31"),("2021-11-11","2022-12-31")],
        bear_label="BEAR",
    ),
}

SETTINGS = [
    dict(period=50, std=1.5,  label="BB(50, 1.5)   High Recall",   color="#27ae60"),
    dict(period=50, std=2.0,  label="BB(50, 2.0)   Mid Balance",   color="#e67e22"),
    dict(period=50, std=2.5,  label="BB(50, 2.5)   High Precision",color="#e74c3c"),
]

def find_dips(df_in, lookback=30, min_drop=10, merge=14):
    p = df_in["btc_price"].reset_index(drop=True)
    d = df_in["date"].reset_index(drop=True)
    rm = p.rolling(lookback, min_periods=1).max()
    pct = (p/rm - 1)*100
    bots, in_dip, bpx, bdt = [], False, np.inf, None
    for i in range(len(p)):
        if pct.iloc[i] <= -min_drop:
            if not in_dip: in_dip = True
            if p.iloc[i] < bpx: bpx, bdt = p.iloc[i], d.iloc[i]
        else:
            if in_dip:
                bots.append({"date": bdt, "price": bpx})
                in_dip, bpx, bdt = False, np.inf, None
    if in_dip and bdt: bots.append({"date": bdt, "price": bpx})
    merged = []
    for b in bots:
        if merged and (b["date"]-merged[-1]["date"]).days < merge:
            if b["price"] < merged[-1]["price"]: merged[-1] = b
        else: merged.append(b)
    return pd.DataFrame(merged) if merged else pd.DataFrame(columns=["date","price"])

def in_ranges(d, ranges):
    return any(pd.Timestamp(s) <= d <= pd.Timestamp(e) for s,e in ranges)

def compute_bb(series, period, std):
    sma = series.rolling(period, min_periods=period).mean()
    sig = series.rolling(period, min_periods=period).std()
    return sma, sma+std*sig, sma-std*sig

def get_signals(df_in, period, std, bull_ranges, bear_ranges, dedup=7):
    sma, upper, lower = compute_bb(df_in["sth_sopr"], period, std)
    below = df_in["sth_sopr"] < lower
    first = below & ~below.shift(1, fill_value=False)
    bull_mask = first & df_in["date"].apply(lambda d: in_ranges(d, bull_ranges))
    bear_mask = first & df_in["date"].apply(lambda d: in_ranges(d, bear_ranges))
    def dedup_list(dates):
        out = []
        for d in dates:
            if not out or (d-out[-1]).days > dedup: out.append(d)
        return out
    return sma, upper, lower, dedup_list(df_in[bull_mask]["date"].tolist()), \
                               dedup_list(df_in[bear_mask]["date"].tolist())

def fwd_gain(df_in, sig_date, days=30):
    entry = df_in[df_in["date"]==sig_date]["btc_price"]
    if entry.empty: return None
    fut = df_in[(df_in["date"]>sig_date)&(df_in["date"]<=sig_date+pd.Timedelta(days=days))]
    if fut.empty: return None
    return (fut["btc_price"].max()/entry.iloc[0]-1)*100

def evaluate(df_in, period, std, bull_ranges, bear_ranges, dip_dates):
    sma, upper, lower, bull_sigs, bear_sigs = get_signals(df_in, period, std, bull_ranges, bear_ranges)
    dips_covered, true_sigs, gains = set(), 0, []
    for s in bull_sigs:
        for i, dip_dt in enumerate(dip_dates):
            delta = (dip_dt - s).days
            if -7 <= delta <= 21:
                dips_covered.add(i); true_sigs += 1; break
        g = fwd_gain(df_in, s, 30)
        if g is not None: gains.append(g)
    recall = len(dips_covered)/len(dip_dates)*100 if len(dip_dates)>0 else 0
    prec   = true_sigs/len(bull_sigs)*100 if bull_sigs else 0
    return dict(recall=round(recall,1), precision=round(prec,1),
                n_bull=len(bull_sigs), n_bear_fp=len(bear_sigs),
                avg_g30=round(np.mean(gains),1) if gains else None)

# ── Print summary ─────────────────────────────────────────────────────────────
for pname, pdef in PERIOD_DEFS.items():
    df_p = df[(df["date"]>=pdef["start"])&(df["date"]<=pdef["end"])].copy().reset_index(drop=True)
    bull_only = df_p[df_p["date"].apply(lambda d: in_ranges(d, pdef["bull"]))]
    dips = find_dips(bull_only)
    dip_dates = pd.to_datetime(dips["date"].tolist())
    print(f"\n=== {pname} — {len(dips)} bull dips ===")
    for _, r in dips.iterrows():
        print(f"  {r['date'].date()} | ${r['price']:>9,.0f}")
    print()
    for cfg in SETTINGS:
        r = evaluate(df_p, cfg["period"], cfg["std"], pdef["bull"], pdef["bear"], dip_dates)
        print(f"  BB({cfg['period']},{cfg['std']}): Recall {r['recall']}% | Prec {r['precision']}% | G30d +{r['avg_g30']}% | BullSig {r['n_bull']} | BearFP {r['n_bear_fp']}")

# ── Charts ────────────────────────────────────────────────────────────────────
def make_chart(pname, pdef, filename):
    df_p = df[(df["date"]>=pdef["start"])&(df["date"]<=pdef["end"])].copy().reset_index(drop=True)
    bull_only = df_p[df_p["date"].apply(lambda d: in_ranges(d, pdef["bull"]))]
    dips = find_dips(bull_only)
    dip_dates = pd.to_datetime(dips["date"].tolist())

    # Pre-compute stats for labels
    for cfg in SETTINGS:
        r = evaluate(df_p, cfg["period"], cfg["std"], pdef["bull"], pdef["bear"], dip_dates)
        cfg["stats"] = (f"Recall {r['recall']}%  |  Precision {r['precision']}%  |  "
                        f"Avg G30d +{r['avg_g30']}%  |  "
                        f"Bull sigs {r['n_bull']}  |  Bear FP {r['n_bear_fp']}")

    fig = plt.figure(figsize=(22, 24), facecolor="#0d1117")
    gs  = GridSpec(4, 1, figure=fig, hspace=0.06,
                   height_ratios=[2.0, 1.3, 1.3, 1.3],
                   top=0.97, bottom=0.05, left=0.07, right=0.98)
    axs = [fig.add_subplot(gs[i]) for i in range(4)]

    def style_ax(ax, show_x=False):
        ax.set_facecolor("#111827")
        ax.tick_params(colors="#9ca3af", labelsize=8)
        for sp in ax.spines.values(): sp.set_color("#374151")
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b '%y"))
        ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
        if not show_x: ax.tick_params(labelbottom=False)
        else: plt.setp(ax.xaxis.get_majorticklabels(), rotation=25, ha="right", fontsize=8)
        ax.set_xlim(df_p["date"].min(), df_p["date"].max())
        ax.grid(axis="x", color="#1f2937", lw=0.5)
        ax.grid(axis="y", color="#1f2937", lw=0.5)

    def shade_bears(ax):
        for s, e in pdef["bear"]:
            s2 = max(pd.Timestamp(s), df_p["date"].min())
            e2 = min(pd.Timestamp(e), df_p["date"].max())
            ax.axvspan(s2, e2, color="#7f1d1d33", zorder=0)
            ax.axvline(s2, color="#dc2626", lw=0.8, ls="--", alpha=0.6, zorder=4)

    # ── Price panel ───────────────────────────────────────────────────────────
    ax0 = axs[0]
    style_ax(ax0)
    shade_bears(ax0)
    ax0.fill_between(df_p["date"], df_p["btc_price"], df_p["btc_price"].min()*0.5,
                     alpha=0.08, color="#3b82f6")
    ax0.semilogy(df_p["date"], df_p["btc_price"], color="#93c5fd", lw=1.0, zorder=3)
    ax0.scatter(dips["date"], dips["price"], color="#10b981", s=80, zorder=5,
                marker="o", edgecolors="#ffffff", linewidths=0.6)
    ax0.set_ylabel("BTC / USD (log)", fontsize=9, color="#9ca3af")
    ax0.yaxis.set_major_formatter(ticker.FuncFormatter(
        lambda x, _: f"${x/1000:.0f}K" if x>=1000 else f"${x:.0f}"))
    ax0.set_title(
        f"STH-SOPR  BB(50, 1.5 / 2.0 / 2.5)  —  {pname} Historical Validation\n"
        f"● = Bull dip bottoms ({len(dips)} events)   |   Red zones = Bear markets",
        color="#f9fafb", fontsize=11.5, pad=10, loc="left", fontweight="bold")
    for s, e in pdef["bear"]:
        mid = pd.Timestamp(s) + (pd.Timestamp(e)-pd.Timestamp(s))/2
        if df_p["date"].min() <= mid <= df_p["date"].max():
            ax0.text(mid, df_p["btc_price"].max()*0.55, pdef["bear_label"],
                     color="#ef4444", fontsize=8, ha="center", fontweight="bold", alpha=0.7)

    # ── STH-SOPR panels ───────────────────────────────────────────────────────
    for idx, cfg in enumerate(SETTINGS):
        ax  = axs[idx+1]
        show = (idx == 2)
        style_ax(ax, show_x=show)
        shade_bears(ax)

        sma, upper, lower, bull_sigs, bear_sigs = get_signals(
            df_p, cfg["period"], cfg["std"], pdef["bull"], pdef["bear"])

        ax.fill_between(df_p["date"], lower, upper, alpha=0.10, color=cfg["color"], zorder=1)
        ax.fill_between(df_p["date"], df_p["sth_sopr"], lower,
                        where=df_p["sth_sopr"]<lower, alpha=0.30, color=cfg["color"], zorder=2)
        ax.plot(df_p["date"], upper, color=cfg["color"], lw=0.7, alpha=0.55, ls="--")
        ax.plot(df_p["date"], sma,   color=cfg["color"], lw=0.5, alpha=0.35, ls=":")
        ax.plot(df_p["date"], lower, color=cfg["color"], lw=1.0, alpha=0.80, ls="--")
        ax.plot(df_p["date"], df_p["sth_sopr"], color="#e2e8f0", lw=0.85, alpha=0.90, zorder=3)
        ax.axhline(1.0, color="#4b5563", lw=0.8, zorder=2)
        ax.text(df_p["date"].min()+pd.Timedelta(days=3), 1.001, "1.0",
                color="#6b7280", fontsize=7)

        if bull_sigs:
            sig_rows = df_p[df_p["date"].isin(bull_sigs)]
            ax.scatter(sig_rows["date"], sig_rows["sth_sopr"], color="#10b981",
                       s=90, zorder=7, marker="^", edgecolors="#ffffff", lw=0.6)
            for _, row in sig_rows.iterrows():
                g = fwd_gain(df_p, row["date"], 30)
                if g is not None:
                    lbl = f"+{g:.0f}%" if g>=0 else f"{g:.0f}%"
                    ax.annotate(lbl, xy=(row["date"], row["sth_sopr"]),
                                xytext=(0,-16), textcoords="offset points",
                                color="#10b981" if g>=0 else "#ef4444",
                                fontsize=7, ha="center", va="top", fontweight="bold", zorder=8)
            ax.text(0.003, 0.94, f"▲ {len(bull_sigs)} bull signals",
                    transform=ax.transAxes, color="#10b981", fontsize=8,
                    va="top", fontweight="bold")

        if bear_sigs:
            bear_rows = df_p[df_p["date"].isin(bear_sigs)]
            ax.scatter(bear_rows["date"], bear_rows["sth_sopr"], color="#ef4444",
                       s=90, zorder=7, marker="v", edgecolors="#ffffff", lw=0.6)
            ax.text(0.003, 0.06, f"▼ {len(bear_sigs)} bear FP",
                    transform=ax.transAxes, color="#ef4444", fontsize=8,
                    va="bottom", fontweight="bold")

        ax.text(0.998, 0.97, cfg["stats"], transform=ax.transAxes,
                color="#cbd5e1", fontsize=7.8, ha="right", va="top",
                bbox=dict(facecolor="#1e293b", edgecolor="#334155",
                          boxstyle="round,pad=0.35", alpha=0.9))
        ax.set_ylabel(cfg["label"], fontsize=9, color=cfg["color"], fontweight="bold")
        ax.set_ylim(0.895, 1.115)

    legend_items = [
        mpatches.Patch(color="#10b981", label="▲ Bull entry signal"),
        mpatches.Patch(color="#ef4444", label="▼ Bear FP (ignore)"),
        mpatches.Patch(color="#e2e8f0", alpha=0.7, label="STH-SOPR"),
        mpatches.Patch(color="#7f1d1d", alpha=0.5, label="Bear market"),
    ]
    axs[3].legend(handles=legend_items, loc="lower right",
                  facecolor="#1e293b", edgecolor="#334155",
                  labelcolor="#cbd5e1", fontsize=8.5, ncol=4)

    for ax in axs:
        ax.set_xlim(df_p["date"].min(), df_p["date"].max())

    plt.savefig(filename, dpi=150, bbox_inches="tight", facecolor="#0d1117")
    print(f"Saved: {filename}")

make_chart("2023-2025", PERIOD_DEFS["2023-2025"], "sth_sopr_bb50_2023_2025.png")
make_chart("2016-2022", PERIOD_DEFS["2016-2022"], "sth_sopr_bb50_2016_2022.png")
