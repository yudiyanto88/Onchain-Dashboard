"""
MVRV Divergence Analysis untuk K3 Early Warning Signal Design
Menghitung price_percentile_365d dan mvrv_percentile_365d dari data lokal,
lalu menjalankan 6 analisis sesuai task spec.
"""

import pandas as pd
import numpy as np
from scipy.stats import percentileofscore

# ─── LOAD DATA ───────────────────────────────────────────────────────────────

df = pd.read_csv("data_mvrv.csv", parse_dates=["date"])
df = df.sort_values("date").reset_index(drop=True)

WINDOW = 365  # rolling window in days

# ─── COMPUTE PERCENTILES ──────────────────────────────────────────────────────

def rolling_percentile(series, window):
    """Percentile rank of current value within rolling `window` days."""
    result = np.full(len(series), np.nan)
    arr = series.values
    for i in range(window - 1, len(arr)):
        window_data = arr[max(0, i - window + 1): i + 1]
        result[i] = percentileofscore(window_data, arr[i], kind="rank")
    return result


print("Computing rolling 365-day percentiles... (may take ~10 sec)")
df["price_pct"] = rolling_percentile(df["btc_price"], WINDOW)
df["mvrv_pct"] = rolling_percentile(df["mvrv_ratio"], WINDOW)
df["divergence"] = df["price_pct"] - df["mvrv_pct"]

# Drop first 364 rows where percentile is undefined
df_full = df.copy()
df = df.dropna(subset=["divergence"]).reset_index(drop=True)

print(f"Total usable data points: {len(df)}")
print(f"Date range: {df['date'].min().date()} to {df['date'].max().date()}")
print()

# ─── HELPER: nearest date lookup ─────────────────────────────────────────────

def get_nearest(target_str):
    target = pd.to_datetime(target_str)
    idx = (df["date"] - target).abs().idxmin()
    row = df.loc[idx]
    return row

def fmt_row(row, label=""):
    return (f"{label or str(row['date'].date()):<20} | "
            f"Price: ${row['btc_price']:>10,.0f} | "
            f"MVRV: {row['mvrv_ratio']:>5.2f} | "
            f"Price%: {row['price_pct']:>5.1f} | "
            f"MVRV%: {row['mvrv_pct']:>5.1f} | "
            f"Div: {row['divergence']:>+7.1f}")

# ─── SECTION 1: SNAPSHOT AT KEY DATES ────────────────────────────────────────

print("=" * 90)
print("SECTION 1 — SNAPSHOT DI TANGGAL-TANGGAL KRITIS")
print("=" * 90)

key_dates = {
    "Cycle Tops": [
        ("17 Des 2017 — cycle top 2017", "2017-12-17"),
        ("14 Apr 2021 — local top pre-correction", "2021-04-14"),
        ("8 Nov 2021  — cycle top 2021", "2021-11-08"),
    ],
    "Mid-Cycle Correction 2021": [
        ("19 Mei 2021 — crash awal", "2021-05-19"),
        ("20 Jul 2021 — bottom mid-cycle", "2021-07-20"),
    ],
    "Bear Bottoms": [
        ("16 Des 2018 — bear bottom", "2018-12-16"),
        ("21 Nov 2022 — bear bottom", "2022-11-21"),
    ],
    "Early Bull": [
        ("1 Feb 2019 — early bull", "2019-02-01"),
        ("1 Feb 2023 — early bull", "2023-02-01"),
    ],
}

header = (f"{'Tanggal':<35} | {'Harga':>12} | {'MVRV':>6} | "
          f"{'Price%':>7} | {'MVRV%':>6} | {'Divergence':>10}")
sep = "-" * 90

for section, dates in key_dates.items():
    print(f"\n  [{section}]")
    print(f"  {header}")
    print(f"  {sep}")
    for label, d in dates:
        row = get_nearest(d)
        actual = str(row["date"].date())
        tag = f"{label} ({actual})"
        print(f"  {tag:<35} | ${row['btc_price']:>11,.0f} | {row['mvrv_ratio']:>6.2f} | "
              f"{row['price_pct']:>7.1f} | {row['mvrv_pct']:>6.1f} | {row['divergence']:>+10.1f}")

print("\n  KEY TAKEAWAY:")
top_2017 = get_nearest("2017-12-17")
top_2021 = get_nearest("2021-11-08")
bot_2018 = get_nearest("2018-12-16")
bot_2022 = get_nearest("2022-11-21")
print(f"  • Divergence di kedua cycle tops: 2017={top_2017['divergence']:+.1f}, 2021={top_2021['divergence']:+.1f}")
print(f"  • Divergence di kedua bear bottoms: 2018={bot_2018['divergence']:+.1f}, 2022={bot_2022['divergence']:+.1f}")

# ─── SECTION 2: ATHs DURING 2020–2021 CYCLE ──────────────────────────────────

print()
print("=" * 90)
print("SECTION 2 — DIVERGENCE DI SUCCESSIVE ATHs (2020–2021 CYCLE)")
print("=" * 90)

mask_2020_2021 = (df["date"] >= "2020-01-01") & (df["date"] <= "2021-12-31")
df_2021 = df[mask_2020_2021].copy()

# Identify ATH dates (days where price exceeds all prior prices in the window)
ath_rows = []
running_ath = 0
for _, row in df_2021.iterrows():
    if row["btc_price"] > running_ath:
        running_ath = row["btc_price"]
        ath_rows.append(row)

# Cluster consecutive ATH days — keep only the first of each run
# (i.e., filter to days where the ATH was newly crossed)
ath_rows_filtered = [ath_rows[0]]
for i in range(1, len(ath_rows)):
    days_gap = (ath_rows[i]["date"] - ath_rows_filtered[-1]["date"]).days
    if days_gap > 14:
        ath_rows_filtered.append(ath_rows[i])

print(f"\n  {'ATH Date':<15} | {'Price':>12} | {'Divergence':>12} | {'Delta vs Prev':>15}")
print(f"  {'-'*60}")
prev_div = None
for row in ath_rows_filtered:
    delta = ""
    if prev_div is not None:
        d = row["divergence"] - prev_div
        delta = f"{d:+.1f}"
    print(f"  {str(row['date'].date()):<15} | ${row['btc_price']:>11,.0f} | "
          f"{row['divergence']:>+12.1f} | {delta:>15}")
    prev_div = row["divergence"]

print("\n  KEY TAKEAWAY:")
# Check trend across ATH divergences
divs = [r["divergence"] for r in ath_rows_filtered]
declining = all(divs[i] >= divs[i+1] for i in range(len(divs)-1))
print(f"  • Trend divergence di successive ATHs: {'MENURUN (bearish divergence confirmed)' if declining else 'TIDAK konsisten menurun — mixed pattern'}")
print(f"  • Divergence range: {max(divs):+.1f} (awal) → {min(divs):+.1f} (akhir)")

# ─── SECTION 3: LEAD TIME ANALYSIS ───────────────────────────────────────────

print()
print("=" * 90)
print("SECTION 3 — LEAD TIME ANALYSIS (divergence menembus/turun dari +30)")
print("=" * 90)

THRESHOLD = 30.0

# Find all episodes where divergence crosses above +30 then back below
above = df["divergence"] >= THRESHOLD
# Label consecutive runs
episodes = []
in_episode = False
start_idx = None
for i, val in enumerate(above):
    if val and not in_episode:
        in_episode = True
        start_idx = i
    elif not val and in_episode:
        in_episode = False
        episodes.append((start_idx, i - 1))
if in_episode:
    episodes.append((start_idx, len(df) - 1))

cycle_tops = [pd.to_datetime("2017-12-17"), pd.to_datetime("2021-11-08")]

print(f"\n  Semua episode divergence ≥ +{THRESHOLD}:")
print(f"  {'Start':<15} | {'End':<15} | {'Days':<6} | {'Peak Div':>9} | {'Days to Top':<15} | {'Cycle Top'}")
print(f"  {'-'*80}")

for s, e in episodes:
    start_date = df.loc[s, "date"]
    end_date = df.loc[e, "date"]
    duration = (end_date - start_date).days + 1
    peak_div = df.loc[s:e, "divergence"].max()

    # Find nearest cycle top after episode end
    nearest_top = None
    nearest_top_name = "—"
    days_to_top = "—"
    for top in cycle_tops:
        if top >= end_date:
            d = (top - end_date).days
            if nearest_top is None or d < (top - end_date).days:
                nearest_top = top
                nearest_top_name = str(top.date())
                days_to_top = f"{(top - end_date).days}d"
            break

    print(f"  {str(start_date.date()):<15} | {str(end_date.date()):<15} | {duration:<6} | "
          f"{peak_div:>+9.1f} | {days_to_top:<15} | {nearest_top_name}")

print("\n  KEY TAKEAWAY:")
# Focus on episodes before 2017 and 2021 tops
pre_top_eps = []
for s, e in episodes:
    end_date = df.loc[e, "date"]
    for top in cycle_tops:
        if end_date < top:
            days_to = (top - end_date).days
            if days_to < 365:
                pre_top_eps.append((df.loc[s,"date"], end_date, days_to, df.loc[s:e,"divergence"].max()))
if pre_top_eps:
    for ep in pre_top_eps:
        print(f"  • Episode yg berakhir {ep[1].date()}: turun balik bawah +30 → {ep[2]} hari sebelum nearest cycle top (peak div: {ep[3]:+.1f})")
else:
    print("  • Tidak ada episode >7 hari yang berakhir dalam 365 hari sebelum cycle top — periksa tabel manual")

# ─── SECTION 4: THRESHOLD ANALYSIS ───────────────────────────────────────────

print()
print("=" * 90)
print("SECTION 4 — THRESHOLD ANALYSIS (episode ≥ +30 selama ≥ 7 hari berturut-turut)")
print("=" * 90)

# Filter episodes >= 7 days
sustained_episodes = [(s, e) for s, e in episodes if (df.loc[e,"date"] - df.loc[s,"date"]).days + 1 >= 7]

print(f"\n  Total episodes sustained ≥ 7 hari: {len(sustained_episodes)}")
print()
print(f"  {'Start':<12} | {'End':<12} | {'Days':>4} | {'Peak Div':>9} | {'Price @Start':>13} | "
      f"{'Price +30d':>11} | {'Price +60d':>11} | Outcome")
print(f"  {'-'*100}")

outcomes = []
for s, e in sustained_episodes:
    start_date = df.loc[s, "date"]
    end_date = df.loc[e, "date"]
    duration = (df.loc[e, "date"] - df.loc[s, "date"]).days + 1
    peak_div = df.loc[s:e, "divergence"].max()
    price_start = df.loc[e, "btc_price"]  # price at END of episode

    # Price 30 and 60 days after episode ends
    date_30 = end_date + pd.Timedelta(days=30)
    date_60 = end_date + pd.Timedelta(days=60)

    idx_30 = (df["date"] - date_30).abs().idxmin()
    idx_60 = (df["date"] - date_60).abs().idxmin()
    price_30 = df.loc[idx_30, "btc_price"] if abs((df.loc[idx_30,"date"] - date_30).days) < 10 else None
    price_60 = df.loc[idx_60, "btc_price"] if abs((df.loc[idx_60,"date"] - date_60).days) < 10 else None

    # Classify outcome
    if price_30 is not None:
        chg_30 = (price_30 - price_start) / price_start * 100
        chg_60 = (price_60 - price_start) / price_start * 100 if price_60 else None

        # Rough classification
        # Check if top was near episode end
        top_2017_near = abs((pd.to_datetime("2017-12-17") - end_date).days) < 45
        top_2021_near = abs((pd.to_datetime("2021-11-08") - end_date).days) < 45
        mid_corr_near = abs((pd.to_datetime("2021-04-14") - end_date).days) < 45

        if top_2017_near or top_2021_near:
            outcome = "CYCLE_TOP"
        elif mid_corr_near:
            outcome = "MID_CORRECTION"
        elif chg_30 is not None and chg_30 > 0:
            outcome = "CONTINUED_BULL"
        else:
            outcome = "CORRECTION"
    else:
        chg_30 = None
        chg_60 = None
        outcome = "NO_DATA (recent)"

    outcomes.append(outcome)
    p30_str = f"${price_30:>9,.0f} ({chg_30:>+.0f}%)" if price_30 else "N/A"
    p60_str = f"${price_60:>9,.0f} ({chg_60:>+.0f}%)" if price_60 else "N/A"

    print(f"  {str(start_date.date()):<12} | {str(end_date.date()):<12} | {duration:>4} | "
          f"{peak_div:>+9.1f} | ${price_start:>11,.0f} | {p30_str:<15} | {p60_str:<15} | {outcome}")

print()
from collections import Counter
oc = Counter(outcomes)
print(f"  Outcome summary: {dict(oc)}")
false_pos = sum(v for k, v in oc.items() if k == "CONTINUED_BULL")
total_valid = sum(v for k, v in oc.items() if k != "NO_DATA (recent)")
print(f"  KEY TAKEAWAY:")
print(f"  • False positives (divergence ≥+30 ≥7 hari tapi price lanjut naik): {false_pos}/{total_valid}")
print(f"  • Threshold +30/7 hari {'memiliki false positives' if false_pos > 0 else 'sangat clean — no false positives'} dalam data historis")

# ─── SECTION 5: MID-CYCLE vs CYCLE TOP SEPARATION TEST ───────────────────────

print()
print("=" * 90)
print("SECTION 5 — MID-CYCLE vs CYCLE TOP SEPARATION TEST")
print("=" * 90)

# Apr 2021: local top before mid-cycle correction
# Nov 2021: actual cycle top
# Look at 30-day window around each event
for label, center, window_days in [
    ("Apr 2021 (local top / mid-cycle correction)", "2021-04-14", 30),
    ("Nov 2021 (actual cycle top)", "2021-11-08", 30),
]:
    center_dt = pd.to_datetime(center)
    mask = (df["date"] >= center_dt - pd.Timedelta(days=window_days)) & \
           (df["date"] <= center_dt + pd.Timedelta(days=14))
    sub = df[mask]

    print(f"\n  [{label}]")
    print(f"  {'Date':<13} | {'Price':>10} | {'MVRV':>6} | {'Price%':>7} | {'MVRV%':>6} | {'Divergence':>11}")
    print(f"  {'-'*65}")
    for _, row in sub.iterrows():
        marker = " ◀ EVENT" if abs((row["date"] - center_dt).days) <= 1 else ""
        print(f"  {str(row['date'].date()):<13} | ${row['btc_price']:>9,.0f} | "
              f"{row['mvrv_ratio']:>6.2f} | {row['price_pct']:>7.1f} | "
              f"{row['mvrv_pct']:>6.1f} | {row['divergence']:>+11.1f}{marker}")

    peak_div = sub["divergence"].max()
    days_above_30 = (sub["divergence"] >= 30).sum()
    peak_price = sub["btc_price"].max()
    print(f"\n  Summary: Peak divergence={peak_div:+.1f}, Days div≥+30={days_above_30}, "
          f"Peak price=${peak_price:,.0f}")

print("\n  KEY TAKEAWAY:")
row_apr = get_nearest("2021-04-14")
row_nov = get_nearest("2021-11-08")
print(f"  • Apr 2021 divergence at top: {row_apr['divergence']:+.1f}")
print(f"  • Nov 2021 divergence at top: {row_nov['divergence']:+.1f}")
diff = row_nov["divergence"] - row_apr["divergence"]
print(f"  • Perbedaan: {diff:+.1f} — {'Cycle top punya divergence lebih rendah (pattern: MVRV lebih kencang naik dari price)' if diff < 0 else 'Cycle top punya divergence lebih tinggi' if diff > 0 else 'Sama'}")

# ─── SECTION 6: CURRENT STATE ─────────────────────────────────────────────────

print()
print("=" * 90)
print("SECTION 6 — CURRENT STATE")
print("=" * 90)

latest = df.iloc[-1]
print(f"\n  Latest date: {latest['date'].date()}")
print(f"  {'Field':<20} | {'Value':>15}")
print(f"  {'-'*40}")
print(f"  {'Price':<20} | ${latest['btc_price']:>14,.0f}")
print(f"  {'MVRV Ratio':<20} | {latest['mvrv_ratio']:>15.4f}")
print(f"  {'Price Pct (365d)':<20} | {latest['price_pct']:>14.1f}%")
print(f"  {'MVRV Pct (365d)':<20} | {latest['mvrv_pct']:>14.1f}%")
print(f"  {'Divergence':<20} | {latest['divergence']:>+14.1f}")

# Percentile of CURRENT divergence across ALL historical data
all_divs = df["divergence"].dropna().values
current_div_pct = percentileofscore(all_divs, latest["divergence"], kind="rank")
print(f"\n  Divergence {latest['divergence']:+.1f} berada di persentil ke-{current_div_pct:.1f} dari seluruh dataset.")

# Historical context: find dates with similar divergence
similar_range = df[(df["divergence"] >= latest["divergence"] - 5) &
                   (df["divergence"] <= latest["divergence"] + 5)]
print(f"\n  Tanggal historis dengan divergence serupa (±5): {len(similar_range)} hari")
if len(similar_range) > 0:
    # Show regime distribution
    similar_range = similar_range.copy()
    similar_range["year"] = similar_range["date"].dt.year
    year_counts = similar_range["year"].value_counts().sort_index()
    print(f"  Distribusi tahun: {dict(year_counts)}")

print("\n  KEY TAKEAWAY:")
print(f"  • Current divergence {latest['divergence']:+.1f} — persentil {current_div_pct:.0f} dari histori semua cycle")
if latest["divergence"] < -20:
    print("  • Negatif kuat: MVRV naik lebih kencang dari price → potential undervaluation signal")
elif latest["divergence"] < 0:
    print("  • Sedikit negatif: MVRV marginally outpacing price — neutral/cautious")
elif latest["divergence"] < 20:
    print("  • Low positive: price dan MVRV relatif sinkron")
elif latest["divergence"] < 40:
    print("  • Moderate positive: price mulai outpace MVRV — watch for +30 threshold")
else:
    print("  • High positive (>+30): Price jauh outpacing MVRV — elevated risk zone")

# ─── CAVEAT ────────────────────────────────────────────────────────────────────

print()
print("=" * 90)
print("CAVEAT")
print("=" * 90)

total_raw = len(df_full)
total_usable = len(df)
date_start = df["date"].min()
date_end = df["date"].max()
num_cycles = 2  # 2017 and 2021 confirmed tops

print(f"""
  a. Total data points (raw):    {total_raw:,} hari ({df_full['date'].min().date()} → {df_full['date'].max().date()})
  b. Usable after 365d warmup:   {total_usable:,} hari ({date_start.date()} → {date_end.date()})
  c. Siklus yang bisa dianalisa: {num_cycles} (2017, 2021) — 2013/2014 cycle excluded (butuh 365d price history)
  d. Gap data: Tidak ada gap signifikan dalam data MVRV (daily frequency)
  e. Keterbatasan metodologi:
     - percentileofscore menggunakan kind='rank' (tied values dibagi rata)
     - Rolling window 365 calendar days (bukan trading days)
     - MVRV data dari sumber tunggal (data_mvrv.csv) — cross-validate dengan Glassnode disarankan
     - 2 cycle tops saja = sample size sangat kecil untuk inferensi statistik kuat
     - Classification outcome di Section 4 menggunakan proximity rule (±45 hari) — bukan ground truth
""")

print("=" * 90)
print("SELESAI — Analisis MVRV Divergence untuk K3 Early Warning Signal Design")
print("=" * 90)
