"""
aSOPR Crossover — Visual Chart
Best combos:
  UP   (bottom): EMA30/SMA15 + EMA50/SMA30  — dual confirmation
  DOWN (peak)  : EMA30/SMA15 + EMA55/SMA35  — dual confirmation
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.lines import Line2D
from matplotlib.patches import Patch

matplotlib.rcParams["figure.facecolor"] = "#0d1117"
matplotlib.rcParams["axes.facecolor"]   = "#0d1117"
matplotlib.rcParams["text.color"]       = "#e6edf3"
matplotlib.rcParams["axes.labelcolor"]  = "#e6edf3"
matplotlib.rcParams["xtick.color"]      = "#8b949e"
matplotlib.rcParams["ytick.color"]      = "#8b949e"
matplotlib.rcParams["axes.edgecolor"]   = "#30363d"
matplotlib.rcParams["grid.color"]       = "#21262d"
matplotlib.rcParams["font.family"]      = "monospace"

# ── Load ───────────────────────────────────────────────────────────────────
df = pd.read_csv(
    r"D:\Claude Code\Projects\Onchain-Dashboard\data_momentum_events.csv",
    parse_dates=["date"], usecols=["date","btc_price","asopr"]
)
df = (df.dropna(subset=["btc_price","asopr"])
       .query("btc_price > 0 and date >= '2013-01-01'")
       .sort_values("date").reset_index(drop=True))

# ── MAs ───────────────────────────────────────────────────────────────────
df["EMA30"] = df["asopr"].ewm(span=30, adjust=False).mean()
df["EMA50"] = df["asopr"].ewm(span=50, adjust=False).mean()
df["EMA55"] = df["asopr"].ewm(span=55, adjust=False).mean()
df["SMA15"] = df["asopr"].rolling(15, min_periods=15).mean()
df["SMA30"] = df["asopr"].rolling(30, min_periods=30).mean()
df["SMA35"] = df["asopr"].rolling(35, min_periods=35).mean()

MIN_GAP = 30

def detect_crossovers(df, fast, slow):
    diff = df[fast] - df[slow]
    prev = diff.shift(1)
    up   = (diff > 0) & (prev <= 0)
    down = (diff < 0) & (prev >= 0)
    events, last_up, last_dn = [], pd.Timestamp("2000-01-01"), pd.Timestamp("2000-01-01")
    for i in df.index:
        if pd.isna(df.at[i,fast]) or pd.isna(df.at[i,slow]): continue
        d = df.at[i,"date"]
        if up[i] and (d-last_up).days >= MIN_GAP:
            events.append({"date":d,"direction":"UP","price":df.at[i,"btc_price"],"asopr":df.at[i,"asopr"]})
            last_up = d
        elif down[i] and (d-last_dn).days >= MIN_GAP:
            events.append({"date":d,"direction":"DOWN","price":df.at[i,"btc_price"],"asopr":df.at[i,"asopr"]})
            last_dn = d
    return pd.DataFrame(events) if events else pd.DataFrame()

cross_30_15 = detect_crossovers(df, "EMA30", "SMA15")
cross_50_30 = detect_crossovers(df, "EMA50", "SMA30")
cross_55_35 = detect_crossovers(df, "EMA55", "SMA35")

AGREE_WIN = 14

def dual_signals(ca, cb, direction):
    a = ca[ca["direction"]==direction].reset_index(drop=True)
    b = cb[cb["direction"]==direction].reset_index(drop=True)
    if a.empty or b.empty: return pd.DataFrame()
    signals, used_b = [], set()
    for _, ra in a.iterrows():
        da = ra["date"]
        matches = b[(b["date"] >= da - pd.Timedelta(days=AGREE_WIN)) &
                    (b["date"] <= da + pd.Timedelta(days=AGREE_WIN))]
        for idx_b, rb in matches.iterrows():
            if idx_b in used_b: continue
            sig_date = max(da, rb["date"])
            if signals and (sig_date - signals[-1]["date"]).days < AGREE_WIN:
                break
            row = df[df["date"]==sig_date]
            price  = row["btc_price"].values[0] if not row.empty else np.nan
            asoprv = row["asopr"].values[0]     if not row.empty else np.nan
            signals.append({"date":sig_date,"price":price,"asopr":asoprv})
            used_b.add(idx_b)
            break
    return pd.DataFrame(signals) if signals else pd.DataFrame()

# Best combos
dual_up   = dual_signals(cross_30_15, cross_50_30, "UP")    # bottom
dual_down = dual_signals(cross_30_15, cross_55_35, "DOWN")  # peak

# Major events
def find_major_events(df, window=90, min_dd=0.28, min_ru=0.65, merge=60):
    prices, dates, n = df["btc_price"].values, df["date"].values, len(df)
    bottoms, peaks = [], []
    for i in range(window, n-window):
        p, prev, nxt = prices[i], prices[i-window:i], prices[i+1:i+window+1]
        if p <= prev.min() and p <= nxt.min() and (prev.max()-p)/prev.max() >= min_dd:
            bottoms.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
        if p >= prev.max() and p >= nxt.max() and (p-prev.min())/prev.min() >= min_ru:
            peaks.append({"date":pd.Timestamp(dates[i]),"price":float(p)})
    def mg(evts, keep):
        if not evts: return []
        evts = sorted(evts, key=lambda x: x["date"])
        merged, grp = [], [evts[0]]
        for e in evts[1:]:
            if (e["date"]-grp[-1]["date"]).days <= merge: grp.append(e)
            else:
                merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                              else max(grp,key=lambda x:x["price"]))
                grp = [e]
        merged.append(min(grp,key=lambda x:x["price"]) if keep=="min"
                      else max(grp,key=lambda x:x["price"]))
        return merged
    return pd.DataFrame(mg(bottoms,"min")), pd.DataFrame(mg(peaks,"max"))

bottoms_df, peaks_df = find_major_events(df)

# ══════════════════════════════════════════════════════════════════════════
# CHART 1 — Overview: BTC Price + Dual Signals
# ══════════════════════════════════════════════════════════════════════════
fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(18, 10), sharex=True,
                                 gridspec_kw={"height_ratios":[2.5,1], "hspace":0.04})
fig1.suptitle("aSOPR Dual-Pair Crossover Signals — BTC Price Overview",
              fontsize=14, fontweight="bold", color="#e6edf3", y=0.98)

# ── Panel 1: BTC Price ────────────────────────────────────────────────────
ax1.semilogy(df["date"], df["btc_price"], color="#58a6ff", lw=0.8, alpha=0.9, label="BTC Price")
ax1.fill_between(df["date"], df["btc_price"], 1, alpha=0.06, color="#58a6ff")

# Major bottoms
for _, r in bottoms_df.iterrows():
    ax1.axvline(r["date"], color="#3fb950", lw=0.6, alpha=0.25, ls="--")
    ax1.scatter(r["date"], r["price"], color="#3fb950", s=120, zorder=5,
                marker="^", edgecolors="#0d1117", linewidths=0.8)

# Major peaks
for _, r in peaks_df.iterrows():
    ax1.axvline(r["date"], color="#f85149", lw=0.6, alpha=0.25, ls="--")
    ax1.scatter(r["date"], r["price"], color="#f85149", s=120, zorder=5,
                marker="v", edgecolors="#0d1117", linewidths=0.8)

# Dual UP signals (bottom signal)
if not dual_up.empty:
    ax1.scatter(dual_up["date"], dual_up["price"],
                color="#3fb950", s=220, zorder=6, marker="*",
                edgecolors="#ffffff", linewidths=0.5, alpha=0.95, label="Dual UP (bottom)")

# Dual DOWN signals (peak signal)
if not dual_down.empty:
    ax1.scatter(dual_down["date"], dual_down["price"],
                color="#f85149", s=220, zorder=6, marker="*",
                edgecolors="#ffffff", linewidths=0.5, alpha=0.95, label="Dual DOWN (peak)")

ax1.set_ylabel("BTC Price (USD, log)", fontsize=10)
ax1.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(
    lambda x, _: f"${x:,.0f}"))
ax1.grid(True, axis="both", alpha=0.3)
ax1.set_ylim(bottom=50)

legend_elements = [
    Line2D([0],[0], color="#58a6ff", lw=1.5, label="BTC Price"),
    Line2D([0],[0], marker="^", color="w", markerfacecolor="#3fb950",
           markersize=9, label="Major Bottom", linestyle="None"),
    Line2D([0],[0], marker="v", color="w", markerfacecolor="#f85149",
           markersize=9, label="Major Peak", linestyle="None"),
    Line2D([0],[0], marker="*", color="w", markerfacecolor="#3fb950",
           markersize=11, label="Dual UP signal (EMA30/15 + EMA50/30)", linestyle="None"),
    Line2D([0],[0], marker="*", color="w", markerfacecolor="#f85149",
           markersize=11, label="Dual DOWN signal (EMA30/15 + EMA55/35)", linestyle="None"),
]
ax1.legend(handles=legend_elements, loc="upper left", fontsize=8,
           framealpha=0.3, facecolor="#161b22")

# ── Panel 2: aSOPR raw ────────────────────────────────────────────────────
ax2.plot(df["date"], df["asopr"], color="#8b949e", lw=0.5, alpha=0.5)
ax2.axhline(1.0, color="#e6edf3", lw=0.6, ls="--", alpha=0.4)
ax2.set_ylabel("aSOPR", fontsize=9)
ax2.set_ylim(0.85, 1.15)
ax2.grid(True, alpha=0.25)
ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax2.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax2.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=8)

plt.savefig(r"D:\Claude Code\Projects\Onchain-Dashboard\chart1_overview.png",
            dpi=150, bbox_inches="tight", facecolor="#0d1117")
print("Saved: chart1_overview.png")

# ══════════════════════════════════════════════════════════════════════════
# CHART 2 — aSOPR + MA lines + Crossover signals (UP combo)
# ══════════════════════════════════════════════════════════════════════════
fig2, (ax3, ax4) = plt.subplots(2, 1, figsize=(18, 10), sharex=True,
                                 gridspec_kw={"height_ratios":[1.8,1], "hspace":0.04})
fig2.suptitle("UP Crossover: EMA30/SMA15 + EMA50/SMA30 — Bottom Detection",
              fontsize=13, fontweight="bold", color="#e6edf3", y=0.98)

# ── Panel top: BTC price with UP signals ─────────────────────────────────
ax3.semilogy(df["date"], df["btc_price"], color="#8b949e", lw=0.7, alpha=0.6)
for _, r in bottoms_df.iterrows():
    ax3.axvline(r["date"], color="#3fb950", lw=0.8, alpha=0.3, ls=":")

# Individual pair UP signals
up30 = cross_30_15[cross_30_15["direction"]=="UP"]
up50 = cross_50_30[cross_50_30["direction"]=="UP"]
ax3.scatter(up30["date"], up30["price"], color="#79c0ff", s=60, zorder=4,
            marker="^", alpha=0.5, label="EMA30/SMA15 UP", edgecolors="none")
ax3.scatter(up50["date"], up50["price"], color="#d2a8ff", s=60, zorder=4,
            marker="^", alpha=0.5, label="EMA50/SMA30 UP", edgecolors="none")
# Dual confirmed
if not dual_up.empty:
    ax3.scatter(dual_up["date"], dual_up["price"], color="#3fb950", s=250, zorder=6,
                marker="*", edgecolors="#ffffff", linewidths=0.6,
                label="DUAL confirmed UP")

ax3.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax3.set_ylabel("BTC Price (log)", fontsize=9)
ax3.grid(True, alpha=0.25)
ax3.set_ylim(bottom=50)
ax3.legend(loc="upper left", fontsize=8, framealpha=0.3, facecolor="#161b22")

# ── Panel bottom: aSOPR + MA lines ───────────────────────────────────────
ax4.plot(df["date"], df["asopr"], color="#8b949e", lw=0.5, alpha=0.45, label="aSOPR")
ax4.plot(df["date"], df["EMA30"], color="#79c0ff", lw=1.2, alpha=0.85, label="EMA30")
ax4.plot(df["date"], df["SMA15"], color="#ffa657", lw=1.2, alpha=0.85, label="SMA15")
ax4.plot(df["date"], df["EMA50"], color="#d2a8ff", lw=1.2, alpha=0.85, label="EMA50")
ax4.plot(df["date"], df["SMA30"], color="#ff7b72", lw=1.2, alpha=0.85, label="SMA30")
ax4.axhline(1.0, color="#e6edf3", lw=0.6, ls="--", alpha=0.4)

# Mark crossover points on aSOPR panel
if not dual_up.empty:
    ax4.scatter(dual_up["date"], dual_up["asopr"], color="#3fb950", s=120, zorder=6,
                marker="*", edgecolors="white", linewidths=0.5)

ax4.set_ylabel("aSOPR", fontsize=9)
ax4.set_ylim(0.87, 1.13)
ax4.grid(True, alpha=0.25)
ax4.legend(loc="upper left", fontsize=8, ncol=5, framealpha=0.3, facecolor="#161b22")
ax4.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax4.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax4.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=8)

plt.savefig(r"D:\Claude Code\Projects\Onchain-Dashboard\chart2_up_signal.png",
            dpi=150, bbox_inches="tight", facecolor="#0d1117")
print("Saved: chart2_up_signal.png")

# ══════════════════════════════════════════════════════════════════════════
# CHART 3 — aSOPR + MA lines + Crossover signals (DOWN combo)
# ══════════════════════════════════════════════════════════════════════════
fig3, (ax5, ax6) = plt.subplots(2, 1, figsize=(18, 10), sharex=True,
                                 gridspec_kw={"height_ratios":[1.8,1], "hspace":0.04})
fig3.suptitle("DOWN Crossover: EMA30/SMA15 + EMA55/SMA35 — Peak Detection",
              fontsize=13, fontweight="bold", color="#e6edf3", y=0.98)

# ── Panel top: BTC price with DOWN signals ────────────────────────────────
ax5.semilogy(df["date"], df["btc_price"], color="#8b949e", lw=0.7, alpha=0.6)
for _, r in peaks_df.iterrows():
    ax5.axvline(r["date"], color="#f85149", lw=0.8, alpha=0.3, ls=":")

dn30 = cross_30_15[cross_30_15["direction"]=="DOWN"]
dn55 = cross_55_35[cross_55_35["direction"]=="DOWN"]
ax5.scatter(dn30["date"], dn30["price"], color="#79c0ff", s=60, zorder=4,
            marker="v", alpha=0.5, label="EMA30/SMA15 DOWN", edgecolors="none")
ax5.scatter(dn55["date"], dn55["price"], color="#ffa657", s=60, zorder=4,
            marker="v", alpha=0.5, label="EMA55/SMA35 DOWN", edgecolors="none")
if not dual_down.empty:
    ax5.scatter(dual_down["date"], dual_down["price"], color="#f85149", s=250, zorder=6,
                marker="*", edgecolors="#ffffff", linewidths=0.6,
                label="DUAL confirmed DOWN")

ax5.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f"${x:,.0f}"))
ax5.set_ylabel("BTC Price (log)", fontsize=9)
ax5.grid(True, alpha=0.25)
ax5.set_ylim(bottom=50)
ax5.legend(loc="upper left", fontsize=8, framealpha=0.3, facecolor="#161b22")

# ── Panel bottom: aSOPR + MA lines ───────────────────────────────────────
ax6.plot(df["date"], df["asopr"], color="#8b949e", lw=0.5, alpha=0.45, label="aSOPR")
ax6.plot(df["date"], df["EMA30"], color="#79c0ff", lw=1.2, alpha=0.85, label="EMA30")
ax6.plot(df["date"], df["SMA15"], color="#58a6ff", lw=1.2, alpha=0.85, label="SMA15")
ax6.plot(df["date"], df["EMA55"], color="#ffa657", lw=1.2, alpha=0.85, label="EMA55")
ax6.plot(df["date"], df["SMA35"], color="#f85149", lw=1.2, alpha=0.85, label="SMA35")
ax6.axhline(1.0, color="#e6edf3", lw=0.6, ls="--", alpha=0.4)

if not dual_down.empty:
    ax6.scatter(dual_down["date"], dual_down["asopr"], color="#f85149", s=120, zorder=6,
                marker="*", edgecolors="white", linewidths=0.5)

ax6.set_ylabel("aSOPR", fontsize=9)
ax6.set_ylim(0.87, 1.13)
ax6.grid(True, alpha=0.25)
ax6.legend(loc="upper left", fontsize=8, ncol=5, framealpha=0.3, facecolor="#161b22")
ax6.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
ax6.xaxis.set_major_locator(mdates.YearLocator())
plt.setp(ax6.xaxis.get_majorticklabels(), rotation=0, ha="center", fontsize=8)

plt.savefig(r"D:\Claude Code\Projects\Onchain-Dashboard\chart3_down_signal.png",
            dpi=150, bbox_inches="tight", facecolor="#0d1117")
print("Saved: chart3_down_signal.png")

# ══════════════════════════════════════════════════════════════════════════
# CHART 4 — Precision & Lead Time comparison bar chart
# ══════════════════════════════════════════════════════════════════════════
fig4, (ax7, ax8) = plt.subplots(1, 2, figsize=(14, 6))
fig4.suptitle("Precision & Avg Lead Time — Single vs Dual Pair",
              fontsize=13, fontweight="bold", color="#e6edf3", y=1.01)
fig4.patch.set_facecolor("#0d1117")

labels_up = ["EMA30/15\n(single)", "EMA60/30\n(single)", "EMA50/30\n(single)",
             "EMA90/80\n(single)", "EMA30/15\n+EMA50/30\n(dual)", "EMA35/20\n+EMA55/35\n(dual)"]
prec_up   = [28.3, 31.7, 29.6, 29.8, 40.9, 40.0]
lead_up   = [21,   62,   58,   59,   62,   74]

labels_dn = ["EMA30/15\n(single)", "EMA60/30\n(single)", "EMA55/35\n(single)",
             "EMA90/80\n(single)", "EMA30/15\n+EMA55/35\n(dual)"]
prec_dn   = [22.3, 25.9, 23.8, 22.4, 31.6]
lead_dn   = [28,   56,   58,   52,   66]

def bar_chart(ax, labels, precision, lead, title):
    ax.set_facecolor("#0d1117")
    x = np.arange(len(labels))
    w = 0.38
    b1 = ax.bar(x - w/2, precision, w, color="#3fb950", alpha=0.85, label="Precision (%)", zorder=3)
    ax2b = ax.twinx()
    ax2b.set_facecolor("#0d1117")
    b2 = ax2b.bar(x + w/2, lead, w, color="#58a6ff", alpha=0.85, label="Avg Lead (days)", zorder=3)
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8, color="#e6edf3")
    ax.set_ylabel("Precision (%)", color="#3fb950", fontsize=9)
    ax2b.set_ylabel("Avg Lead (days)", color="#58a6ff", fontsize=9)
    ax.tick_params(axis="y", colors="#3fb950")
    ax2b.tick_params(axis="y", colors="#58a6ff")
    ax.set_title(title, fontsize=10, color="#e6edf3", pad=10)
    ax.grid(True, axis="y", alpha=0.2, zorder=0)
    ax.set_ylim(0, 55)
    ax2b.set_ylim(0, 100)
    # value labels
    for bar in b1:
        ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                f"{bar.get_height():.1f}%", ha="center", va="bottom",
                fontsize=7, color="#3fb950")
    for bar in b2:
        ax2b.text(bar.get_x()+bar.get_width()/2, bar.get_height()+1,
                  f"{int(bar.get_height())}d", ha="center", va="bottom",
                  fontsize=7, color="#58a6ff")
    lines = [Patch(facecolor="#3fb950", label="Precision (%)"),
             Patch(facecolor="#58a6ff", label="Avg Lead (days)")]
    ax.legend(handles=lines, loc="upper left", fontsize=8,
              framealpha=0.3, facecolor="#161b22")
    # highlight dual bars
    for i in range(len(labels)):
        if "dual" in labels[i]:
            ax.axvspan(i-0.5, i+0.5, alpha=0.07, color="#f0e020", zorder=1)

bar_chart(ax7, labels_up, prec_up, lead_up, "UP Signal (Bottom Detection)")
bar_chart(ax8, labels_dn, prec_dn, lead_dn, "DOWN Signal (Peak Detection)")

plt.tight_layout()
plt.savefig(r"D:\Claude Code\Projects\Onchain-Dashboard\chart4_comparison.png",
            dpi=150, bbox_inches="tight", facecolor="#0d1117")
print("Saved: chart4_comparison.png")

plt.show()
print("\nDone. 4 charts saved.")
