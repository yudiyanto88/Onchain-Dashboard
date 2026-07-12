"""
Kandidat B — F&G peak index terjadi sebelum price top (potensi sinyal ke-6 K1)

Klaim generik (didefinisikan SEBELUM lihat hasil, supaya tidak post-hoc fitting ke
angka spesifik video 2021 $30k/92% & 70-80%):
  "F&G value di ATH price baru dalam siklus yang sama < F&G value di ATH sebelumnya
   dalam siklus yang sama" — analog PERSIS dengan cara K1 signal #1 (MVRV turun di
   tiap ATH baru) diuji.

Event definition (dipakai APA ADANYA dari precedent script yang sudah ada:
`research/analyze_mvrv_zscore_independence_check.py`, findings:
`mvrv_zscore_rolling_divergence_k1_findings.md` / `mvrv_zscore_independence_check.md`):
  - find_local_tops(): local top = harga hari itu lebih tinggi dari max harga 5 hari
    sebelum DAN 5 hari sesudah (margin=5, sama seperti definisi K6).
  - Cycle boundaries (bear-market bottom terkonfirmasi) SAMA PERSIS dengan script itu.
  - Ditambah di sini: filter is_ath = local top tsb juga ATH GLOBAL (harga >= running
    all-time-high price dari seluruh histori sejak 2010-07-17), bukan cuma local top
    dalam cycle. Ini yang membedakan dari filter di script precedent (yang ambil SEMUA
    local top, bukan cuma yang genuinely all-time-high).

Data F&G cuma mulai 2018-02-01 -> HANYA cycle 2021 dan cycle 2023-2025(current) yang
bisa dicek. Cycle 2011/2013/2017 NEEDS-DATA-WE-DONT-HAVE untuk F&G.

Redundancy check (jebakan skeptic #1): apakah arah F&G turun di ATH SELALU align
same-pair dengan arah MVRV turun / aSOPR turun di ATH yang sama (K1 signal #1 & #2
existing) -> kalau selalu align dan tidak pernah menambah informasi baru, ini REDUNDAN.
"""

import pandas as pd
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 200)

# ── Load & merge ─────────────────────────────────────────────────────────────
price = pd.read_csv('data_price_level.csv', parse_dates=['date'])[['date', 'btc_price']]
mvrv = pd.read_csv('data_mvrv.csv', parse_dates=['date'])[['date', 'mvrv_ratio']]
mo = pd.read_csv('data_momentum.csv', parse_dates=['date'])[['date', 'asopr']]
fg = pd.read_csv('data_fg.csv', parse_dates=['date']).rename(columns={'Fear & Greed': 'fg'})

df_full = price.merge(mvrv, on='date', how='left').merge(mo, on='date', how='left').sort_values('date').reset_index(drop=True)

# running all-time-high price computed from FULL history (2010-07-17+), tidak dipotong cycle
df_full['ath_running'] = df_full['btc_price'].cummax()
df_full['is_ath'] = df_full['btc_price'] >= df_full['ath_running'] - 1e-6  # exact new high day

print("=" * 90)
print("LANGKAH 0 — CEK DATA")
print("=" * 90)
print(f"Price data: {price['date'].min().date()} s/d {price['date'].max().date()}")
print(f"F&G data  : {fg['date'].min().date()} s/d {fg['date'].max().date()} <- pembatas utama")
print(f"ATH price sepanjang histori (utk cek cycle 2023-2025 sudah topping?): "
      f"${df_full['btc_price'].max():,.0f} pada {df_full.loc[df_full['btc_price'].idxmax(),'date'].date()}")
current_price = df_full.iloc[-1]
print(f"Harga terakhir di data ({current_price['date'].date()}): ${current_price['btc_price']:,.0f} "
      f"({(current_price['btc_price']/df_full['btc_price'].max()-1)*100:+.1f}% dari ATH tsb)")
print("-> per tanggal data terakhir, cycle 2023-2025 SUDAH topping (harga turun >48% dari ATH Okt 2025),")
print("   beda dari framing awal task ('siklus 2025 partial, belum tahu top'). Tetap dilaporkan terpisah")
print("   dari cycle 2021 karena bear-phase-nya jauh lebih muda (~9 bulan vs >3 tahun utk 2021).")

# ── Cycle boundaries (IDENTIK dgn analyze_mvrv_zscore_independence_check.py) ─
cycles = [
    ('2021', '2020-03-12', '2022-11-21'),
    ('2023-2025 (current)', '2022-11-21', None),
]
MARGIN = 5  # sama dengan definisi K6 / precedent script


def find_local_tops(seg_df, margin=MARGIN):
    d = seg_df.reset_index(drop=True)
    n = len(d)
    idxs = []
    for i in range(margin, n - margin):
        left = d['btc_price'].iloc[i - margin:i]
        right = d['btc_price'].iloc[i + 1:i + 1 + margin]
        if d.loc[i, 'btc_price'] > left.max() and d.loc[i, 'btc_price'] > right.max():
            idxs.append(i)
    return d.loc[idxs].reset_index(drop=True)


def direction(val_prev, val_curr, thresh_pct=0.02):
    chg = (val_curr - val_prev) / val_prev
    if chg > thresh_pct:
        return 'NAIK'
    elif chg < -thresh_pct:
        return 'TURUN'
    else:
        return 'FLAT'


print("\n" + "=" * 90)
print("1. IDENTIFIKASI ATH EVENTS PER CYCLE (local top DAN genuine all-time-high)")
print("=" * 90)

all_ath_rows = []
for name, d0, d1 in cycles:
    seg = df_full.copy()
    if d0 is not None:
        seg = seg[seg['date'] > d0]
    if d1 is not None:
        seg = seg[seg['date'] <= d1]
    seg = seg.reset_index(drop=True)

    tops = find_local_tops(seg)
    # filter to genuine global ATH days only
    ath_tops = tops[tops['is_ath']].copy()
    # merge F&G (only where available -> otomatis exclude cycle sebelum 2018)
    ath_tops = ath_tops.merge(fg, on='date', how='left')
    ath_tops['cycle'] = name
    print(f"\n{name}: {len(tops)} local top total, {len(ath_tops)} di antaranya genuine ATH (harga baru tertinggi sepanjang histori)")
    for _, r in ath_tops.iterrows():
        fg_str = f"{r['fg']:.0f}" if pd.notna(r['fg']) else "NO F&G DATA"
        print(f"  {r['date'].date()}  price=${r['btc_price']:,.0f}  MVRV={r['mvrv_ratio']:.3f}  "
              f"aSOPR={r['asopr']:.4f}  F&G={fg_str}")
    all_ath_rows.append(ath_tops)

all_ath = pd.concat(all_ath_rows, ignore_index=True)
# restrict to rows with F&G data available (data mulai 2018-02-01)
ath_fg = all_ath.dropna(subset=['fg']).reset_index(drop=True)

print("\n" + "=" * 90)
print("2. ATH EVENTS DENGAN F&G DATA TERSEDIA (subset yang bisa diuji)")
print("=" * 90)
print(ath_fg[['cycle', 'date', 'btc_price', 'mvrv_ratio', 'asopr', 'fg']].to_string(index=False))

# ── Pairwise consecutive-ATH comparison per cycle ───────────────────────────
print("\n" + "=" * 90)
print("3. PASANGAN ATH BERURUTAN — ARAH F&G vs MVRV vs aSOPR (analog signal #1/#2 K1)")
print("=" * 90)

pair_rows = []
for name in ath_fg['cycle'].unique():
    sub = ath_fg[ath_fg['cycle'] == name].sort_values('date').reset_index(drop=True)
    if len(sub) < 2:
        print(f"\n{name}: cuma {len(sub)} ATH event dengan F&G data -> tidak ada pasangan untuk dibandingkan.")
        continue
    print(f"\n{name}: {len(sub)} ATH event -> {len(sub)-1} pasangan berurutan")
    for i in range(1, len(sub)):
        prev = sub.iloc[i - 1]
        curr = sub.iloc[i]
        dir_fg = direction(prev['fg'], curr['fg'])
        dir_mvrv = direction(prev['mvrv_ratio'], curr['mvrv_ratio'])
        dir_asopr = direction(prev['asopr'], curr['asopr'])

        fg_matches_mvrv = dir_fg == dir_mvrv
        fg_matches_asopr = dir_fg == dir_asopr

        print(f"  {prev['date'].date()} (${prev['btc_price']:,.0f}) -> {curr['date'].date()} (${curr['btc_price']:,.0f})")
        print(f"    F&G   : {prev['fg']:.0f} -> {curr['fg']:.0f}  ({dir_fg})")
        print(f"    MVRV  : {prev['mvrv_ratio']:.3f} -> {curr['mvrv_ratio']:.3f}  ({dir_mvrv})  "
              f"{'[SAMA arah dgn F&G]' if fg_matches_mvrv else '[BEDA arah dgn F&G]'}")
        print(f"    aSOPR : {prev['asopr']:.4f} -> {curr['asopr']:.4f}  ({dir_asopr})  "
              f"{'[SAMA arah dgn F&G]' if fg_matches_asopr else '[BEDA arah dgn F&G]'}")

        pair_rows.append({
            'cycle': name,
            'date_prev': prev['date'].date(), 'date_curr': curr['date'].date(),
            'price_prev': prev['btc_price'], 'price_curr': curr['btc_price'],
            'fg_prev': prev['fg'], 'fg_curr': curr['fg'], 'dir_fg': dir_fg,
            'mvrv_prev': prev['mvrv_ratio'], 'mvrv_curr': curr['mvrv_ratio'], 'dir_mvrv': dir_mvrv,
            'asopr_prev': prev['asopr'], 'asopr_curr': curr['asopr'], 'dir_asopr': dir_asopr,
            'fg_matches_mvrv': fg_matches_mvrv, 'fg_matches_asopr': fg_matches_asopr,
        })

pairs = pd.DataFrame(pair_rows)

print("\n" + "=" * 90)
print("4. RINGKASAN — BERAPA PASANGAN F&G TURUN DI ATH BARU (analog signal #1)")
print("=" * 90)
if len(pairs) > 0:
    n_total = len(pairs)
    n_turun = (pairs['dir_fg'] == 'TURUN').sum()
    n_naik = (pairs['dir_fg'] == 'NAIK').sum()
    n_flat = (pairs['dir_fg'] == 'FLAT').sum()
    print(f"Total pasangan ATH berurutan (dgn F&G data): {n_total}")
    print(f"  F&G TURUN di ATH baru : {n_turun}/{n_total}")
    print(f"  F&G NAIK  di ATH baru : {n_naik}/{n_total}")
    print(f"  F&G FLAT             : {n_flat}/{n_total}")
    print(f"\nPer cycle:")
    print(pairs.groupby('cycle')['dir_fg'].value_counts())

    n_match_mvrv = pairs['fg_matches_mvrv'].sum()
    n_match_asopr = pairs['fg_matches_asopr'].sum()
    print(f"\nRedundancy check:")
    print(f"  Arah F&G sama dengan arah MVRV : {n_match_mvrv}/{n_total} pasangan")
    print(f"  Arah F&G sama dengan arah aSOPR: {n_match_asopr}/{n_total} pasangan")
else:
    print("Tidak ada pasangan yang bisa dibandingkan (kurang dari 2 ATH event dengan F&G data per cycle).")

pairs.to_csv('research/findings/_fg_ath_decline_k1_pairs.csv', index=False)
ath_fg.to_csv('research/findings/_fg_ath_decline_k1_events.csv', index=False)
print("\nSaved: research/findings/_fg_ath_decline_k1_pairs.csv")
print("Saved: research/findings/_fg_ath_decline_k1_events.csv")

print("\n" + "=" * 90)
print("SELESAI")
print("=" * 90)
