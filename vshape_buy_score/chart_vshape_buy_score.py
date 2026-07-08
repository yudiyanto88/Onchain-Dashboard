"""
Chart V-Shape Buy Score final - 2 panel: harga BTC (log scale) di atas,
confirm_count (0-3, dari 3 metrik boolean) di bawah, dengan shading zona
BUY (>=2-dari-3) dan penanda 6 tanggal V-shape correction referensi.
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
COUNT_COLOR = "#0ca30c"
BUY_ZONE_COLOR = "#0ca30c"
EVENT_COLOR = "#e34948"

CONFIRM_THRESHOLD = 2
START_DATE = "2016-01-01"

EVENTS = [
    ("6-9 Mar 2023", "2023-03-06", "2023-03-09"),
    ("21 Jan 2024", "2024-01-21", "2024-01-21"),
    ("5 Sep 2020", "2020-09-05", "2020-09-05"),
    ("14-16 Jul 2017", "2017-07-14", "2017-07-16"),
    ("13-15 Sep 2017", "2017-09-13", "2017-09-15"),
    ("21 Sep 2021", "2021-09-21", "2021-09-21"),
]

df = pd.read_csv("data_vshape_buy_score.csv", parse_dates=["date"])
df = df[df["date"] >= START_DATE].reset_index(drop=True)

fig, (ax_price, ax_score) = plt.subplots(
    2, 1, figsize=(18, 8), sharex=True,
    gridspec_kw={"height_ratios": [2, 1.3]}, facecolor=SURFACE,
)
for ax in (ax_price, ax_score):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color(BASELINE)
    ax.tick_params(colors=INK_MUTED, labelsize=9)

# Shade BUY zone across both panels
buy_mask = df["zone"] == "BUY_ZONE"
dates = df["date"].values
m = buy_mask.values
in_span, start = False, None
for i in range(len(m)):
    if m[i] and not in_span:
        start, in_span = dates[i], True
    elif not m[i] and in_span:
        for ax in (ax_price, ax_score):
            ax.axvspan(start, dates[i], color=BUY_ZONE_COLOR, alpha=0.15, linewidth=0)
        in_span = False
if in_span:
    for ax in (ax_price, ax_score):
        ax.axvspan(start, dates[-1], color=BUY_ZONE_COLOR, alpha=0.15, linewidth=0)

# Top panel: price
ax_price.plot(df["date"], df["btc_price"], color=PRICE_COLOR, linewidth=1.3)
ax_price.set_yscale("log")
ax_price.set_ylabel("BTC Price (log)", color=INK_SECONDARY, fontsize=10)
ax_price.set_title(
    "V-Shape Buy Score — N-of-3 (MIN aSOPR/STH-SOPR<=0.98, STH%loss>=40%+ROC, RSI14+BB breach)",
    color=INK_PRIMARY, fontsize=12.5, fontweight="bold", loc="left", pad=12,
)

# Bottom panel: confirm count (step)
ax_score.step(df["date"], df["confirm_count"], color=COUNT_COLOR, linewidth=1.4, where="post")
ax_score.axhline(CONFIRM_THRESHOLD, color=BUY_ZONE_COLOR, linewidth=0.8, linestyle="--", alpha=0.8)
ax_score.text(df["date"].iloc[-1], CONFIRM_THRESHOLD, f" {CONFIRM_THRESHOLD}-dari-3 threshold",
              color=BUY_ZONE_COLOR, fontsize=8, va="bottom", ha="left")
ax_score.set_ylim(0, 3.2)
ax_score.set_yticks([0, 1, 2, 3])
ax_score.set_ylabel("Confirm Count (0-3)", color=INK_SECONDARY, fontsize=10)

# Event markers
for label, d0, d1 in EVENTS:
    mid = pd.Timestamp(d0) + (pd.Timestamp(d1) - pd.Timestamp(d0)) / 2
    if mid < pd.Timestamp(START_DATE):
        continue
    for ax, ytop in ((ax_price, ax_price.get_ylim()[1]), (ax_score, 3.2)):
        ax.axvline(mid, color=EVENT_COLOR, linewidth=0.9, linestyle=":", alpha=0.85)
        ax.text(mid, ytop, f" {label}", color=EVENT_COLOR, fontsize=7,
                rotation=90, va="top", ha="center")

ax_score.xaxis.set_major_locator(mdates.YearLocator())
ax_score.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
ax_score.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

latest = df.iloc[-1]
fig.text(
    0.01, 0.01,
    f"Latest ({latest['date'].date()}): confirm count {int(latest['confirm_count'])}/3, "
    f"zone {latest['zone']} — N-of-3 boolean, bukan komposit kontinu (persistence filter & "
    f"percentile rank terbukti gagal untuk deteksi V-shape yang tajam & singkat).",
    color=INK_MUTED, fontsize=7.5,
)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("vshape_buy_score.png", dpi=150, facecolor=SURFACE)
print("Saved vshape_buy_score.png")
