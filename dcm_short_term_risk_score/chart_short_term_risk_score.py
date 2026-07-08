"""
Chart DCM Short-Term Risk Score (replikasi) - 2 panel: harga BTC (log scale)
di atas, risk score composite di bawah dengan shading zona high/low risk.
Meniru gaya visual video On-Chain Mind "This Bitcoin Signal Has Nailed EVERY Dip".
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ─── PALETTE (dataviz skill - dark surface) ─────────────────────────────────
SURFACE = "#1a1a19"
INK_PRIMARY = "#ffffff"
INK_SECONDARY = "#c3c2b7"
INK_MUTED = "#898781"
GRID = "#2c2c2a"
BASELINE = "#383835"
PRICE_COLOR = "#3987e5"       # blue
SCORE_COLOR = "#3987e5"       # blue (smoothed score, main line)
RAW_COLOR = "#898781"         # muted (raw pre-smooth line)
GOOD = "#0ca30c"              # low-risk zone
CRITICAL = "#d03b3b"          # high-risk zone

HIGH_RISK = 0.70
LOW_RISK = 0.30

START_DATE = "2011-07-01"  # earliest full 7-factor coverage (SSR joins as 8th factor from 2018-11-28)
SSR_START = "2018-11-28"   # when SSR component (8th factor) becomes valid

# ─── LOAD ────────────────────────────────────────────────────────────────────

df = pd.read_csv("data_short_term_risk_score.csv", parse_dates=["date"])
df = df[df["date"] >= START_DATE].reset_index(drop=True)

# ─── FIGURE ──────────────────────────────────────────────────────────────────

fig, (ax_price, ax_score) = plt.subplots(
    2, 1, figsize=(18, 8), sharex=True,
    gridspec_kw={"height_ratios": [2, 1.3]},
    facecolor=SURFACE,
)

for ax in (ax_price, ax_score):
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.6, alpha=0.7)
    for spine in ax.spines.values():
        spine.set_color(BASELINE)
    ax.tick_params(colors=INK_MUTED, labelsize=9)

# Zone shading across both panels
high_mask = df["zone"] == "HIGH_RISK"
low_mask = df["zone"] == "LOW_RISK"

def shade_spans(ax, mask, color):
    in_span = False
    start = None
    dates = df["date"].values
    m = mask.values
    for i in range(len(m)):
        if m[i] and not in_span:
            start = dates[i]
            in_span = True
        elif not m[i] and in_span:
            ax.axvspan(start, dates[i], color=color, alpha=0.15, linewidth=0)
            in_span = False
    if in_span:
        ax.axvspan(start, dates[-1], color=color, alpha=0.15, linewidth=0)

for ax in (ax_price, ax_score):
    shade_spans(ax, high_mask, CRITICAL)
    shade_spans(ax, low_mask, GOOD)

# ─── TOP PANEL: price ───────────────────────────────────────────────────────

ax_price.plot(df["date"], df["btc_price"], color=PRICE_COLOR, linewidth=1.4)
ax_price.set_yscale("log")
ax_price.set_ylabel("BTC Price (log)", color=INK_SECONDARY, fontsize=10)
ax_price.set_title(
    "DCM Short-Term Risk Score (replikasi) — komposit 8 faktor",
    color=INK_PRIMARY, fontsize=13, fontweight="bold", loc="left", pad=12,
)

# ─── BOTTOM PANEL: risk score ───────────────────────────────────────────────

ax_score.plot(df["date"], df["risk_raw"], color=RAW_COLOR, linewidth=0.9,
              alpha=0.6, label="Raw")
ax_score.plot(df["date"], df["risk_score"], color=SCORE_COLOR, linewidth=1.6,
              label="Smoothed (EMA-7)")

ax_score.axhline(HIGH_RISK, color=CRITICAL, linewidth=0.8, linestyle="--", alpha=0.8)
ax_score.axhline(0.50, color=INK_MUTED, linewidth=0.8, linestyle="--", alpha=0.6)
ax_score.axhline(LOW_RISK, color=GOOD, linewidth=0.8, linestyle="--", alpha=0.8)

ax_score.text(df["date"].iloc[-1], HIGH_RISK, " 70% high risk", color=CRITICAL,
              fontsize=8, va="bottom", ha="left")
ax_score.text(df["date"].iloc[-1], LOW_RISK, " 30% low risk", color=GOOD,
              fontsize=8, va="top", ha="left")

ax_score.set_ylim(0, 1)
ax_score.set_ylabel("Risk Score", color=INK_SECONDARY, fontsize=10)
ax_score.legend(
    loc="upper left", frameon=False, fontsize=9,
    labelcolor=INK_SECONDARY,
)

ax_score.xaxis.set_major_locator(mdates.YearLocator())
ax_score.xaxis.set_minor_locator(mdates.MonthLocator(interval=3))
ax_score.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# Marker: SSR (8th factor) joins the blend from this date onward
ssr_start_ts = pd.Timestamp(SSR_START)
for ax in (ax_price, ax_score):
    ax.axvline(ssr_start_ts, color=INK_MUTED, linewidth=0.8, linestyle=":", alpha=0.7)
ax_price.text(ssr_start_ts, ax_price.get_ylim()[1], " 8-faktor mulai (SSR join)",
              color=INK_MUTED, fontsize=7.5, va="top", ha="left", rotation=90)

# ─── FOOTER ──────────────────────────────────────────────────────────────────

latest = df.iloc[-1]
fig.text(
    0.01, 0.01,
    f"Latest ({latest['date'].date()}): score {latest['risk_score']:.0%}, zone {latest['zone']} — "
    f"rekonstruksi berbasis definisi standar, bobot equal-weight (bukan formula asli video). "
    f"Sebelum {SSR_START}: 7 faktor (tanpa SSR, data stablecoin belum ada).",
    color=INK_MUTED, fontsize=7.5,
)

plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig("short_term_risk_score.png", dpi=150, facecolor=SURFACE)
print("Saved short_term_risk_score.png")
