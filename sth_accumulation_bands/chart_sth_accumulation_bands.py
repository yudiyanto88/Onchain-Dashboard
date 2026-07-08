"""
Chart OCM STH Accumulation Bands - satu panel, price (log) dengan STH Cost
Basis sebagai garis atas (putih), dan 2 band di BAWAHNYA saja (olive/orange,
lalu maroon/red) - meniru struktur visual asli di video (bukan cloud
simetris ke atas & bawah).
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
CENTER_COLOR = "#f2f2ea"        # putih - STH cost basis
BAND1_LINE = "#d9a441"          # kuning/emas - lower_1sd
BAND2_LINE = "#c8425a"          # merah/pink - lower_2sd
MILD_FILL = "#8a6d2f"           # olive - antara cost basis & lower_1sd
DEEP_FILL = "#7a2636"           # maroon - antara lower_1sd & lower_2sd
EVENT_COLOR = "#e34948"

START_DATE = "2016-01-01"

EVENTS = [
    ("Cycle Peak 2017", "2017-12-08", "2017-12-19"),
    ("Bear Bottom 2018", "2018-12-11", "2018-12-17"),
    ("COVID Crash 2020", "2020-03-13", "2020-03-17"),
    ("Cycle Peak 2021", "2021-10-20", "2021-11-09"),
    ("Bear Bottom 2022", "2022-11-08", "2022-12-19"),
    ("Cycle Peak 2025", "2025-10-05", "2025-10-07"),
]

df = pd.read_csv("data_sth_accumulation_bands.csv", parse_dates=["date"])
df = df[df["date"] >= START_DATE].reset_index(drop=True)

fig, ax = plt.subplots(figsize=(18, 8), facecolor=SURFACE)
ax.set_facecolor(SURFACE)
ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
for spine in ax.spines.values():
    spine.set_color(BASELINE)
ax.tick_params(colors=INK_MUTED, labelsize=9)

# Fills (downside-only bands)
ax.fill_between(df["date"], df["lower_1sd"], df["sth_cost_basis"], color=MILD_FILL, alpha=0.35, linewidth=0)
ax.fill_between(df["date"], df["lower_2sd"], df["lower_1sd"], color=DEEP_FILL, alpha=0.45, linewidth=0)

ax.plot(df["date"], df["sth_cost_basis"], color=CENTER_COLOR, linewidth=1.2, label="STH Cost Basis")
ax.plot(df["date"], df["lower_1sd"], color=BAND1_LINE, linewidth=1.0, alpha=0.9, label="-1sd (mild accumulation)")
ax.plot(df["date"], df["lower_2sd"], color=BAND2_LINE, linewidth=1.0, alpha=0.9, label="-2sd (deep accumulation)")
ax.plot(df["date"], df["btc_price"], color=PRICE_COLOR, linewidth=1.3, label="BTC Price")

# Highlight vertical background where price is inside/below the bands (mirrors video's red highlight bars)
dates = df["date"].values
in_zone = (df["zone"] != "NEUTRAL").values
in_span, start = False, None
for i in range(len(in_zone)):
    if in_zone[i] and not in_span:
        start, in_span = dates[i], True
    elif not in_zone[i] and in_span:
        ax.axvspan(start, dates[i], color=EVENT_COLOR, alpha=0.08, linewidth=0)
        in_span = False
if in_span:
    ax.axvspan(start, dates[-1], color=EVENT_COLOR, alpha=0.08, linewidth=0)

ax.set_yscale("log")
ax.set_ylabel("BTC Price (log)", color=INK_SECONDARY, fontsize=10)
ax.set_title(
    "OCM STH Accumulation Bands — STH Cost Basis + 2 band ke bawah saja (rolling log-ratio std, 730d)",
    color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12,
)
ax.legend(loc="upper left", frameon=False, fontsize=9, labelcolor=INK_SECONDARY)

y_top = ax.get_ylim()[1]
for label, d0, d1 in EVENTS:
    mid = pd.Timestamp(d0) + (pd.Timestamp(d1) - pd.Timestamp(d0)) / 2
    if mid < pd.Timestamp(START_DATE):
        continue
    ax.axvline(mid, color=EVENT_COLOR, linewidth=0.9, linestyle=":", alpha=0.85)
    ax.text(mid, y_top, f" {label}", color=EVENT_COLOR, fontsize=7,
            rotation=90, va="top", ha="center")

ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

latest = df.iloc[-1]
fig.text(
    0.01, 0.01,
    f"Latest ({latest['date'].date()}): price ${latest['btc_price']:,.0f}, "
    f"STH Cost Basis ${latest['sth_cost_basis']:,.0f}, zone {latest['zone']} — "
    f"band HANYA ke bawah (buy-zone detector), tidak ada band distribusi di atas "
    f"cost basis, meniru struktur asli video On-Chain Mind.",
    color=INK_MUTED, fontsize=7.5,
)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("sth_accumulation_bands.png", dpi=150, facecolor=SURFACE)
print("Saved sth_accumulation_bands.png")
