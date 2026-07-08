"""
STH-SOPR MA90 / MA90-MA60 Gap-and-Cross Framework — Backtest
Signal A: Gap peaked + declining  → Local Top Warning
Signal B: Bearish cross (MA90 < MA90-MA60) after local top
Signal C: Bearish cross after cycle peak  → Lower High Confirmation
"""
import sys
sys.stdout.reconfigure(encoding="utf-8")
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.gridspec import GridSpec
from matplotlib.patches import Patch
from matplotlib.lines import Line2D

# ── Load data ─────────────────────────────────────────────────────────────────
df = pd.read_csv("data_momentum.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)
df = df[["date","btc_price","sth_sopr"]].dropna()
df = df[df["date"] >= "2017-01-01"].reset_index(drop=True)

# ── Construct indicators ──────────────────────────────────────────────────────
df["ma90"]    = df["sth_sopr"].rolling(90, min_periods=90).mean()
df["ma90_60"] = df["ma90"].rolling(60, min_periods=60).mean()
df["gap"]     = df["ma90"] - df["ma90_60"]

# ── Known events ──────────────────────────────────────────────────────────────
EVENTS = {
    "cycle_peaks": [
        ("2017-12-17", "Cycle Peak 2017",     "C"),
        ("2021-11-10", "Cycle Peak 2021",     "C"),
        ("2025-10-05", "Cycle Peak 2025 (BT)","C"),
    ],
    "local_tops": [
        ("2021-03-13", "LT Mar 2021",    "B"),
        ("2021-04-14", "LT Apr 2021 ATH","B"),
        ("2024-03-14", "LT Mar 2024 ATH","B"),
        ("2024-12-17", "LT Dec 2024 ATH","B"),
        ("2025-01-20", "LT Jan 2025 ATH","B"),
        ("2025-07-01", "LT Jul 2025 ATH","B"),
    ],
}
ALL_EVENTS = [(pd.Timestamp(d), label, stype)
              for cat in EVENTS.values() for d, label, stype in cat]
ALL_EVENTS.sort(key=lambda x: x[0])

# Bear market zones
BEAR_ZONES = [
    ("2017-12-18","2019-01-31"),
    ("2021-11-11","2022-12-31"),
    ("2025-11-01","2026-06-17"),
]
def in_bear(d):
    return any(pd.Timestamp(s) <= d <= pd.Timestamp(e) for s,e in BEAR_ZONES)

def in_bull(d):
    return not in_bear(d)

# ── Signal A: Gap peaks that are MEANINGFUL ───────────────────────────────────
# Criteria: (1) local max in gap, (2) gap > 0.006, (3) in bull market,
#           (4) NOT in bear zone, (5) deduplicated 90 days
def find_signal_a(df_in, min_gap=0.006, lookback=40, dedup=90):
    g = df_in["gap"].rolling(7, center=True, min_periods=1).mean()
    peaks = []
    n = len(g)
    for i in range(lookback, n - lookback):
        d = df_in["date"].iloc[i]
        if in_bear(d): continue
        window = g.iloc[max(0,i-lookback):i+lookback+1]
        if g.iloc[i] == window.max() and g.iloc[i] > min_gap:
            left  = g.iloc[max(0,i-20):i].mean()
            right = g.iloc[i+1:min(n,i+21)].mean()
            if left < g.iloc[i] and right < g.iloc[i]:
                peaks.append(df_in["date"].iloc[i])
    merged = []
    for p in peaks:
        if not merged or (p-merged[-1]).days > dedup:
            merged.append(p)
    return merged

sig_a = find_signal_a(df)

# ── Signal B/C: FIRST bearish cross after each event (within 120d) ─────────────
# Also track all crosses for the chart
def find_all_crosses(df_in):
    bear_crosses, bull_crosses = [], []
    prev_pos, prev_neg = None, None
    for _, row in df_in.dropna(subset=["gap"]).iterrows():
        pos = row["gap"] > 0
        if prev_pos is True and not pos:
            bear_crosses.append(row["date"])
        if prev_neg is True and pos:
            bull_crosses.append(row["date"])
        prev_pos = pos
        prev_neg = not pos
    return bear_crosses, bull_crosses

all_bear_cross, all_bull_cross = find_all_crosses(df)

# Match each event to its first bearish cross within 120 days
event_crosses = []
for ev_date, ev_label, ev_type in ALL_EVENTS:
    # Find first bear cross AFTER the event (within 120 days)
    candidates = [c for c in all_bear_cross
                  if 0 <= (c - ev_date).days <= 120]
    if candidates:
        cross = min(candidates)
        lag   = (cross - ev_date).days
        r = df[df["date"]==cross]
        price = r["btc_price"].iloc[0] if not r.empty else None
        event_crosses.append((ev_date, ev_label, ev_type, cross, lag, price))
    else:
        event_crosses.append((ev_date, ev_label, ev_type, None, None, None))

# ── Text output ───────────────────────────────────────────────────────────────
print(f"{'='*90}")
print("  STH-SOPR MA90 / MA90-MA60 GAP-AND-CROSS FRAMEWORK — Backtest")
print("  MA90 = SMA(STH-SOPR, 90)  |  MA90-MA60 = SMA(MA90, 60)  |  Gap = MA90 − MA90-MA60")
print(f"{'='*90}")

print(f"\n  {'─'*80}")
print(f"  SIGNAL A — Gap Peak → Local Top Warning   (Bull-market peaks only, gap > 0.006)")
print(f"  {'─'*80}")
print(f"  {'Signal A Date':14} {'Gap Value':>10} {'BTC Price':>12} {'Nearest Upcoming Event':>35}")
print(f"  {'-'*14} {'-'*10} {'-'*12} {'-'*35}")
for p in sig_a:
    r = df[df["date"]==p]
    if r.empty: continue
    gap_val = r["gap"].iloc[0]
    price   = r["btc_price"].iloc[0]
    # Find next event after this peak
    future = [(d, lbl, st) for d, lbl, st in ALL_EVENTS if d > p]
    if future:
        nxt_d, nxt_l, _ = future[0]
        lag = (nxt_d - p).days
        evt_str = f"{nxt_l} (+{lag}d)"
    else:
        evt_str = "—"
    print(f"  {str(p.date()):14} {gap_val:>10.5f} ${price:>10,.0f}  → {evt_str}")

print(f"\n  {'─'*80}")
print(f"  SIGNAL B/C — First Bearish Cross After Each Local Top / Cycle Peak")
print(f"  {'─'*80}")
print(f"  {'Event':28} {'Event Date':12} {'Cross Date':12} {'Lag':>6} {'BTC at Cross':>13} {'Type'}")
print(f"  {'-'*28} {'-'*12} {'-'*12} {'-'*6} {'-'*13} {'-'*4}")
for row in event_crosses:
    ev_d, ev_lbl, ev_type, cross, lag, price = row
    if cross:
        print(f"  {ev_lbl:<28} {str(ev_d.date()):12} {str(cross.date()):12} +{lag:>4}d "
              f"${price:>11,.0f} {ev_type}")
    else:
        print(f"  {ev_lbl:<28} {str(ev_d.date()):12} {'—':12} {'—':>6} {'—':>13} {ev_type}")

print(f"\n  {'─'*80}")
print(f"  ALL BEARISH CROSSES TIMELINE")
print(f"  {'─'*80}")
print(f"  {'Date':14} {'BTC Price':>12} {'Context':>35} {'Valid?':>7}")
print(f"  {'-'*14} {'-'*12} {'-'*35} {'-'*7}")
for c in all_bear_cross:
    r = df[df["date"]==c]
    if r.empty: continue
    price = r["btc_price"].iloc[0]
    context = "BEAR MKT NOISE" if in_bear(c) else ""
    # Check if this is a 'first cross after event'
    is_valid = any(row[3]==c for row in event_crosses)
    ctx2 = "✓ First after event" if is_valid else ("— Bear noise" if in_bear(c) else "— late/extra cross")
    print(f"  {str(c.date()):14} ${price:>10,.0f}  {ctx2}")

print(f"\n  {'─'*80}")
print(f"  SIGNAL B/C LEAD TIME SUMMARY (valid signals only)")
print(f"  {'─'*80}")
valid = [(row[1], row[4]) for row in event_crosses if row[3] is not None]
if valid:
    lags = [v[1] for v in valid]
    print(f"  Count: {len(valid)} | Min: {min(lags)}d | Max: {max(lags)}d | Avg: {np.mean(lags):.0f}d | Median: {np.median(lags):.0f}d")
    for lbl, lag in valid:
        print(f"  {lbl:<30} lag = +{lag}d")

print(f"\n  {'─'*80}")
print(f"  CURRENT STATE  ({df.iloc[-1]['date'].date()})")
print(f"  {'─'*80}")
last = df.dropna(subset=["gap"]).iloc[-1]
g30  = df.dropna(subset=["gap"]).tail(30)["gap"].values
trend= "RISING" if g30[-1] > g30[0] else "DECLINING"
print(f"  BTC Price  : ${last['btc_price']:,.0f}")
print(f"  MA90       : {last['ma90']:.5f}")
print(f"  MA90-MA60  : {last['ma90_60']:.5f}")
print(f"  Gap        : {last['gap']:+.5f}  [{trend} vs 30d ago]")
status = "POSITIVE  → MA90 above baseline" if last['gap']>0 else "NEGATIVE  → MA90 below baseline"
print(f"  Status     : {status}")

g_series = df.dropna(subset=["gap"])
peak_idx  = g_series.tail(120)["gap"].idxmax()
peak_date = g_series.loc[peak_idx, "date"]
peak_val  = g_series.loc[peak_idx, "gap"]
days_since= (last["date"] - peak_date).days
print(f"  Recent peak: {peak_val:+.5f} on {peak_date.date()} ({days_since}d ago)")

# Last cross
last_bear_c = max([c for c in all_bear_cross if c<=last["date"]], default=None)
last_bull_c = max([c for c in all_bull_cross  if c<=last["date"]], default=None)
if last_bear_c:
    print(f"  Last bear cross  : {last_bear_c.date()} (BTC ${df[df['date']==last_bear_c]['btc_price'].iloc[0]:,.0f})")
if last_bull_c:
    print(f"  Last bull cross  : {last_bull_c.date()} (BTC ${df[df['date']==last_bull_c]['btc_price'].iloc[0]:,.0f})")

# ── CHART ─────────────────────────────────────────────────────────────────────
C = dict(
    bg="#0d1117", panel="#111827", text="#e6edf3", muted="#8b949e",
    grid="#1f2937", edge="#374151",
    price="#93c5fd", ma90="#f0883e", ma90_60="#f85149",
    gap_pos="#3fb950", gap_neg="#f85149",
    sig_a="#e3b341", bc="#f85149", bc_bull="#3fb950",
    lt="#58a6ff", cp="#d2a8ff",
)
matplotlib.rcParams.update({
    "figure.facecolor":C["bg"],"axes.facecolor":C["panel"],
    "text.color":C["text"],"axes.labelcolor":C["muted"],
    "xtick.color":C["muted"],"ytick.color":C["muted"],
    "axes.edgecolor":C["edge"],"grid.color":C["grid"],
    "font.family":"monospace","font.size":9,
})

lt_dates = [pd.Timestamp(d) for d,_,_ in EVENTS["local_tops"]]
cp_dates = [pd.Timestamp(d) for d,_,_ in EVENTS["cycle_peaks"]]

fig = plt.figure(figsize=(24, 19), facecolor=C["bg"])
gs  = GridSpec(3,1, figure=fig, hspace=0.05,
               height_ratios=[2.2,1.8,1.8],
               top=0.96, bottom=0.05, left=0.065, right=0.97)
axs = [fig.add_subplot(gs[i]) for i in range(3)]

def style_ax(ax, show_x=False):
    ax.set_facecolor(C["panel"])
    ax.tick_params(colors=C["muted"], labelsize=8)
    for sp in ax.spines.values(): sp.set_color(C["edge"])
    ax.xaxis.set_major_locator(mdates.MonthLocator(interval=6))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    if not show_x: ax.tick_params(labelbottom=False)
    else: plt.setp(ax.xaxis.get_majorticklabels(), rotation=30, ha="right", fontsize=8)
    ax.set_xlim(df["date"].min(), df["date"].max())
    ax.grid(axis="x",color=C["grid"],lw=0.4,zorder=0)
    ax.grid(axis="y",color=C["grid"],lw=0.4,zorder=0)

def shade_bears(ax):
    for s,e in BEAR_ZONES:
        ax.axvspan(pd.Timestamp(s),pd.Timestamp(e),color="#7f1d1d22",zorder=0)

ax0, ax1, ax2 = axs

# ─── Panel 1: BTC Price ───────────────────────────────────────────────────────
style_ax(ax0)
shade_bears(ax0)
ax0.semilogy(df["date"], df["btc_price"], color=C["price"], lw=1.0, zorder=3)
ax0.fill_between(df["date"],df["btc_price"],df["btc_price"].min()*0.5,alpha=0.07,color=C["price"])

for d in lt_dates:
    ax0.axvline(d, color=C["lt"], lw=0.9, alpha=0.7, zorder=4)
for d in cp_dates:
    ax0.axvline(d, color=C["cp"], lw=1.1, alpha=0.9, zorder=4)

# Signal B/C vertical lines on price (first cross after event)
valid_crosses = [row[3] for row in event_crosses if row[3] is not None]
for c in valid_crosses:
    ax0.axvline(c, color="#ff7b72", lw=1.0, alpha=0.6, ls=":", zorder=3)

ax0.set_ylabel("BTC / USD (log)", color=C["muted"], fontsize=9)
ax0.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x,_: f"${x/1000:.0f}K" if x>=1000 else f"${x:.0f}"))
ax0.set_title(
    "STH-SOPR  MA90 / MA90-MA60  Gap-and-Cross Framework\n"
    "Blue = Local Tops  |  Purple = Cycle Peaks  |  Dotted red = Bearish Cross  |  Red zones = Bear Markets",
    color=C["text"],fontsize=11,pad=10,loc="left",fontweight="bold")

# ─── Panel 2: MA90 + MA90-MA60 ────────────────────────────────────────────────
style_ax(ax1)
shade_bears(ax1)

for c in valid_crosses:
    ax1.axvline(c, color=C["bc"], lw=1.2, alpha=0.8, ls=":", zorder=3)
for c in all_bull_cross:
    ax1.axvline(c, color=C["bc_bull"], lw=0.8, alpha=0.5, ls=":", zorder=3)
for d in sig_a:
    ax1.axvline(d, color=C["sig_a"], lw=0.9, alpha=0.6, ls="--", zorder=3)
    ax1.text(d, 1.064, "A", color=C["sig_a"], fontsize=8,
             ha="center", va="top", fontweight="bold")

ax1.plot(df["date"],df["sth_sopr"],color="#e2e8f0",lw=0.5,alpha=0.40,zorder=2)
ax1.plot(df["date"],df["ma90"],    color=C["ma90"],lw=2.0,alpha=0.90,zorder=4,label="MA90")
ax1.plot(df["date"],df["ma90_60"],color=C["ma90_60"],lw=2.0,alpha=0.90,zorder=4,label="MA90-MA60")
ax1.fill_between(df["date"],df["ma90"],df["ma90_60"],
                 where=df["ma90"]>=df["ma90_60"],alpha=0.22,color=C["gap_pos"],zorder=1)
ax1.fill_between(df["date"],df["ma90"],df["ma90_60"],
                 where=df["ma90"]<df["ma90_60"],alpha=0.22,color=C["gap_neg"],zorder=1)
ax1.axhline(1.0,color=C["muted"],lw=0.8,alpha=0.5)
ax1.text(df["date"].iloc[2],1.0007,"1.0",color=C["muted"],fontsize=7)
ax1.set_ylabel("STH-SOPR + MA90 + MA90-MA60", color=C["muted"], fontsize=9)
ax1.set_ylim(0.940, 1.068)
ax1.legend(loc="upper left",fontsize=8,framealpha=0.4,
           facecolor="#161b22",edgecolor=C["edge"],ncol=2)

# ─── Panel 3: Gap ─────────────────────────────────────────────────────────────
style_ax(ax2, show_x=True)
shade_bears(ax2)
ax2.axhline(0,color=C["muted"],lw=1.0,alpha=0.7,zorder=3)

gp = df.dropna(subset=["gap"])
bar_colors = [C["gap_pos"] if v>=0 else C["gap_neg"] for v in gp["gap"]]
ax2.bar(gp["date"],gp["gap"],color=bar_colors,alpha=0.55,width=1.0,zorder=2)
ax2.plot(gp["date"],gp["gap"].rolling(14,center=True,min_periods=1).mean(),
         color="#e6edf3",lw=1.3,alpha=0.85,zorder=4,label="14d smooth")

# Signal A markers on gap panel
for d in sig_a:
    r = df[df["date"]==d]
    if r.empty: continue
    gval = r["gap"].iloc[0]
    ax2.scatter([d],[gval],color=C["sig_a"],s=140,zorder=7,marker="v",edgecolors="#fff",lw=0.5)
    ax2.text(d,gval+0.0004,"A",color=C["sig_a"],fontsize=8.5,
             ha="center",va="bottom",fontweight="bold")

# Valid bear crosses on gap panel
for c in valid_crosses:
    ax2.axvline(c,color=C["bc"],lw=1.5,alpha=0.9,zorder=5)
for c in all_bull_cross:
    ax2.axvline(c,color=C["bc_bull"],lw=0.8,alpha=0.5,zorder=4)

# Label cross types for confirmed events
for row in event_crosses:
    ev_d, ev_lbl, ev_type, cross, lag, price = row
    if cross is None: continue
    ax2.text(cross, ax2.get_ylim()[0] if ax2.get_ylim()[0]!=0 else -0.0060,
             f"{ev_type}", color=C["bc"], fontsize=7.5,
             ha="center", va="bottom", fontweight="bold")

ax2.set_ylabel("Gap  (MA90 − MA90-MA60)", color=C["muted"], fontsize=9)
ax2.yaxis.set_major_formatter(mticker.FuncFormatter(
    lambda x,_: f"{x*10000:+.1f}×10⁻⁴"))

# Fix ylim for gap panel
g_vals = gp["gap"].dropna()
ymax = max(abs(g_vals.max()), abs(g_vals.min())) * 1.35
ax2.set_ylim(-ymax, ymax)

# Re-add labels now that ylim is set
ybot = ax2.get_ylim()[0]*0.88
for row in event_crosses:
    _, _, ev_type, cross, _, _ = row
    if cross is None: continue
    ax2.text(cross, ybot, ev_type, color=C["bc"],
             fontsize=7.5, ha="center", va="bottom", fontweight="bold")

legend_els = [
    Patch(facecolor=C["gap_pos"],alpha=0.7,label="Gap > 0  (MA90 above baseline)"),
    Patch(facecolor=C["gap_neg"],alpha=0.7,label="Gap < 0  (MA90 below baseline)"),
    Line2D([0],[0],color=C["sig_a"],lw=2,ls="--",label="Signal A — Gap Peak"),
    Line2D([0],[0],color=C["bc"],  lw=2,label="Signal B/C — Bearish Cross (confirmed)"),
    Line2D([0],[0],color=C["bc_bull"],lw=1.5,label="Bullish Cross (regime recovery)"),
    Patch(facecolor="#7f1d1d",alpha=0.5,label="Bear Market"),
    Line2D([0],[0],color=C["lt"],lw=1.5,ls="--",label="Local Tops"),
    Line2D([0],[0],color=C["cp"],lw=1.5,ls="--",label="Cycle Peaks"),
]
ax2.legend(handles=legend_els,loc="lower right",fontsize=7.5,
           framealpha=0.45,facecolor="#161b22",edgecolor=C["edge"],
           ncol=4,columnspacing=0.8)

for ax in axs:
    ax.set_xlim(df["date"].min(), df["date"].max())

out = "sth_sopr_ma90_gap_cross.png"
plt.savefig(out,dpi=150,bbox_inches="tight",facecolor=C["bg"])
print(f"\nSaved: {out}")
