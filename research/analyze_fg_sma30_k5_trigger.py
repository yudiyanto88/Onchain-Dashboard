"""
Kandidat A — F&G SMA30 sebagai refinement trigger K5 (dibanding raw F&G harian)

Definisi event: SAMA PERSIS dengan `analyze_k5_fear_greed_trigger.py` (findings:
`research/findings/k5_fear_greed_trigger_findings.md`) — 19 pullback (>=5% drop dari
running local high) di dua episode Z2/Z3:
  Episode 1 (2019): 2019-05-07 -> 2019-07-08
  Episode 2 (2023-2024): 2023-03-01 -> 2024-02-27

Tambahan di sini: hitung SMA30 harian dari kolom Fear & Greed (rolling dihitung dari
FULL series data_fg.csv, bukan dipotong per episode dulu, supaya rolling window
benar-benar punya histori 30 hari ke belakang — konsisten dengan cara SMA dipakai
di tempat lain di repo ini, tidak ada lookahead karena rolling pakai window backward).

Uji:
  1. Apakah SMA30(F&G)<50 pernah tersentuh di tiap 19 pullback yang sama?
  2. Forward return 14d/30d dari titik SMA30<50 first-crossing dalam window pullback,
     dibanding raw F&G<50 first-crossing di window yang sama.
  3. False-positive rate SMA30<50 (run-level, whole-episode) vs raw F&G<50 (dari findings lama).
  4. Lag: berapa hari SMA30<50 crossing pertama muncul SETELAH raw F&G<50 crossing
     pertama di pullback yang sama (cek redundansi — "cuma versi telat").
"""

import pandas as pd
import numpy as np
import sys
sys.stdout.reconfigure(encoding='utf-8')
pd.set_option('display.width', 160)

# ── Load & prep (sama seperti analyze_k5_fear_greed_trigger.py) ────────────
fg_raw = pd.read_csv('data_fg.csv', parse_dates=['date']).rename(columns={'Fear & Greed': 'fg'})
fg_raw = fg_raw.sort_values('date').reset_index(drop=True)
# SMA30 dihitung dari full series SEBELUM merge/filter, backward rolling, no lookahead
fg_raw['fg_sma30'] = fg_raw['fg'].rolling(30, min_periods=30).mean()

sp = pd.read_csv('data_supply.csv', parse_dates=['date'])
mo = pd.read_csv('data_momentum.csv', parse_dates=['date'])
pl = pd.read_csv('data_price_level.csv', parse_dates=['date'])

df = pl[['date', 'btc_price', 'lth_cost_basis']].merge(
    fg_raw[['date', 'fg', 'fg_sma30']], on='date', how='inner'
).merge(
    sp[['date', 'pct_sth_in_profit', 'pct_sth_in_loss']], on='date', how='inner'
).merge(
    mo[['date', 'asopr', 'sth_sopr']], on='date', how='inner'
)
df = df.rename(columns={'btc_price': 'price', 'lth_cost_basis': 'lth_rp'})
df = df.dropna(subset=['price', 'fg', 'fg_sma30']).sort_values('date').reset_index(drop=True)

print("=" * 78)
print("LANGKAH 0 — CEK DATA & SMA30")
print("=" * 78)
print(f"F&G tersedia: {fg_raw['date'].min().date()} s/d {fg_raw['date'].max().date()}")
print(f"SMA30 pertama kali valid (min_periods=30): {fg_raw.dropna(subset=['fg_sma30'])['date'].min().date()}")
print("-> lookback SMA30 cukup untuk kedua episode (2019 & 2023-2024), tidak ada NaN gap.")

episodes_def = [
    ('EPISODE 1 (2019)', '2019-05-07', '2019-07-08'),
    ('EPISODE 2 (2023-2024)', '2023-03-01', '2024-02-27'),
]

episodes = []
for name, ws, we in episodes_def:
    ep_df = df[(df['date'] >= ws) & (df['date'] <= we)].reset_index(drop=True)
    episodes.append({'name': name, 'start': ws, 'end': we, 'df': ep_df})

# ── Pullback detection (IDENTIK dengan analyze_k5_fear_greed_trigger.py) ───
def find_pullbacks(ep_df, min_drop_pct=5.0):
    d = ep_df.copy().reset_index(drop=True)
    d['run_peak'] = d['price'].cummax()
    d['run_peak_idx'] = d['price'].expanding().apply(lambda x: x.values.argmax()).astype(int)
    d['dd_pct'] = (d['price'] / d['run_peak'] - 1) * 100
    in_pb = d['dd_pct'] <= -min_drop_pct

    pullbacks = []
    i, n = 0, len(d)
    while i < n:
        if in_pb.iloc[i]:
            peak_idx = int(d.loc[i, 'run_peak_idx'])
            j = i
            while j < n and in_pb.iloc[j] and d.loc[j, 'run_peak_idx'] == peak_idx:
                j += 1
            trough_slice = d.iloc[i:j]
            trough_pos = trough_slice['price'].idxmin()
            pullbacks.append({
                'peak_date': d.loc[peak_idx, 'date'], 'peak_price': d.loc[peak_idx, 'price'],
                'start_idx': i, 'end_idx': j - 1,
                'trough_idx': trough_pos, 'trough_date': d.loc[trough_pos, 'date'],
                'trough_price': d.loc[trough_pos, 'price'], 'drop_pct': d.loc[trough_pos, 'dd_pct'],
            })
            i = j
        else:
            i += 1
    return d, pullbacks


def gain_after(d, ref_idx, ref_price, days, global_df):
    ref_date = d.loc[ref_idx, 'date']
    target_date = ref_date + pd.Timedelta(days=days)
    fut = global_df[global_df['date'] >= target_date]
    if fut.empty:
        return None
    return (fut.iloc[0]['price'] / ref_price - 1) * 100


print("\n" + "=" * 78)
print("1-2. PULLBACK: RAW F&G<50 vs SMA30(F&G)<50 — TOUCH & LAG & FORWARD RETURN")
print("=" * 78)

all_rows = []
for ep in episodes:
    d, pullbacks = find_pullbacks(ep['df'])
    print(f"\n{ep['name']}: {len(pullbacks)} pullback (>=5% drop) terdeteksi")

    for k, pb in enumerate(pullbacks, 1):
        seg = d.iloc[pb['start_idx']:pb['end_idx'] + 1]

        raw_below50 = bool((seg['fg'] < 50).any())
        sma_below50 = bool((seg['fg_sma30'] < 50).any())

        # first-crossing index within window
        raw_cross_idx = seg.index[seg['fg'] < 50][0] if raw_below50 else None
        sma_cross_idx = seg.index[seg['fg_sma30'] < 50][0] if sma_below50 else None

        raw_cross_date = d.loc[raw_cross_idx, 'date'] if raw_cross_idx is not None else None
        sma_cross_date = d.loc[sma_cross_idx, 'date'] if sma_cross_idx is not None else None
        lag_days = (sma_cross_date - raw_cross_date).days if (raw_cross_date is not None and sma_cross_date is not None) else None

        g14_raw = g30_raw = g14_sma = g30_sma = None
        if raw_cross_idx is not None:
            ref_price_raw = d.loc[raw_cross_idx, 'price']
            g14_raw = gain_after(d, raw_cross_idx, ref_price_raw, 14, df)
            g30_raw = gain_after(d, raw_cross_idx, ref_price_raw, 30, df)
        if sma_cross_idx is not None:
            ref_price_sma = d.loc[sma_cross_idx, 'price']
            g14_sma = gain_after(d, sma_cross_idx, ref_price_sma, 14, df)
            g30_sma = gain_after(d, sma_cross_idx, ref_price_sma, 30, df)

        fg_min = seg['fg'].min()
        sma_min = seg['fg_sma30'].min()
        sma_min_date = d.loc[seg['fg_sma30'].idxmin(), 'date']

        print(f"\n  Pullback #{k}: peak {pb['peak_date'].date()} (${pb['peak_price']:,.0f}) -> "
              f"trough {pb['trough_date'].date()} (${pb['trough_price']:,.0f}), drop {pb['drop_pct']:.1f}%, "
              f"{len(seg)} hari window")
        print(f"    Raw F&G  : min={fg_min:.0f}  <50 tersentuh? {'YA' if raw_below50 else 'TIDAK'}"
              f"{'  cross @ ' + str(raw_cross_date.date()) if raw_cross_date is not None else ''}")
        print(f"    SMA30 F&G: min={sma_min:.1f} @ {sma_min_date.date()}  <50 tersentuh? {'YA' if sma_below50 else 'TIDAK'}"
              f"{'  cross @ ' + str(sma_cross_date.date()) if sma_cross_date is not None else ''}")
        if lag_days is not None:
            print(f"    Lag SMA30 vs raw crossing pertama: {lag_days} hari")
        elif raw_below50 and not sma_below50:
            print(f"    SMA30 TIDAK PERNAH turun <50 di window ini meski raw sempat <50 -> SINYAL HILANG")
        g14r = f"{g14_raw:+.1f}%" if g14_raw is not None else "N/A"
        g30r = f"{g30_raw:+.1f}%" if g30_raw is not None else "N/A"
        g14s = f"{g14_sma:+.1f}%" if g14_sma is not None else "N/A"
        g30s = f"{g30_sma:+.1f}%" if g30_sma is not None else "N/A"
        print(f"    Forward return dari raw-cross : 14d={g14r}  30d={g30r}")
        print(f"    Forward return dari SMA30-cross: 14d={g14s}  30d={g30s}")

        all_rows.append({
            'episode': ep['name'], 'pullback': k,
            'trough_date': pb['trough_date'].date(), 'drop_pct': pb['drop_pct'],
            'window_days': len(seg),
            'raw_below50': raw_below50, 'sma_below50': sma_below50,
            'raw_cross_date': raw_cross_date.date() if raw_cross_date is not None else None,
            'sma_cross_date': sma_cross_date.date() if sma_cross_date is not None else None,
            'lag_days': lag_days,
            'fg_min': fg_min, 'sma_min': sma_min,
            'gain14_raw': g14_raw, 'gain30_raw': g30_raw,
            'gain14_sma': g14_sma, 'gain30_sma': g30_sma,
        })

res = pd.DataFrame(all_rows)

# ── 2019 khusus — cek klaim "SMA30 tidak pernah <50 karena lag" ────────────
print("\n" + "=" * 78)
print("CEK KHUSUS 2019 (episode 63 hari, raw F&G<50 cuma 5 hari)")
print("=" * 78)
ep2019 = episodes[0]['df']
print(f"Total hari episode 2019: {len(ep2019)}")
print(f"Hari raw F&G<50: {(ep2019['fg'] < 50).sum()}")
print(f"Hari SMA30<50  : {(ep2019['fg_sma30'] < 50).sum()}")
print(f"SMA30 min sepanjang episode 2019: {ep2019['fg_sma30'].min():.1f} pada "
      f"{ep2019.loc[ep2019['fg_sma30'].idxmin(),'date'].date()}")

# ── 3. Summary: berapa dari 19 pullback masing-masing metode "menyala" ─────
print("\n" + "=" * 78)
print("3. RINGKASAN TOUCH-RATE: RAW vs SMA30 (dari 19 pullback)")
print("=" * 78)
n_total = len(res)
n_raw = res['raw_below50'].sum()
n_sma = res['sma_below50'].sum()
n_both = ((res['raw_below50']) & (res['sma_below50'])).sum()
n_raw_only = ((res['raw_below50']) & (~res['sma_below50'])).sum()
n_sma_only = ((~res['raw_below50']) & (res['sma_below50'])).sum()
print(f"Total pullback: {n_total}")
print(f"Raw F&G<50 tersentuh   : {n_raw}/{n_total}")
print(f"SMA30<50 tersentuh     : {n_sma}/{n_total}")
print(f"Kedua-duanya tersentuh : {n_both}")
print(f"Raw saja (SMA30 gagal) : {n_raw_only}  <- SINYAL HILANG kalau pakai SMA30")
print(f"SMA30 saja (raw gagal) : {n_sma_only}  <- SMA30 nangkep yang raw lewatkan")

per_ep = res.groupby('episode').agg(
    n=('pullback', 'count'), raw=('raw_below50', 'sum'), sma=('sma_below50', 'sum')
)
print("\nPer episode:")
print(per_ep)

lag_valid = res.dropna(subset=['lag_days'])
if len(lag_valid) > 0:
    print(f"\nLag rata-rata (SMA30 cross - raw cross) di {len(lag_valid)} pullback yang dua-duanya nyala: "
          f"{lag_valid['lag_days'].mean():.1f} hari (median {lag_valid['lag_days'].median():.0f}, "
          f"min {lag_valid['lag_days'].min():.0f}, max {lag_valid['lag_days'].max():.0f})")
else:
    print("\nTidak ada pullback di mana raw DAN SMA30 dua-duanya cross -> tidak bisa hitung lag.")

# ── 4. False-positive check: run-level, whole episode, SMA30<50 ────────────
print("\n" + "=" * 78)
print("4. FALSE-SIGNAL CHECK — SMA30<50 run-level (whole episode, bukan cuma window pullback)")
print("=" * 78)

for ep in episodes:
    d = ep['df']
    print(f"\n{ep['name']}:")
    below50_mask = d['fg_sma30'] < 50
    if not below50_mask.any():
        print("  SMA30(F&G) tidak pernah < 50 di seluruh window episode ini.")
        continue

    idxs = d.index[below50_mask].to_list()
    runs = []
    run_start = idxs[0]
    prev = idxs[0]
    for ix in idxs[1:]:
        if ix == prev + 1:
            prev = ix
            continue
        runs.append((run_start, prev))
        run_start = ix
        prev = ix
    runs.append((run_start, prev))

    n_no_bounce = 0
    n_during_uptrend = 0
    for a, b in runs:
        lookahead_end = min(b + 30, len(d) - 1)
        lookahead = d.iloc[b:lookahead_end + 1]
        min_price_after = lookahead['price'].min()
        further_drop = (min_price_after / d.loc[b, 'price'] - 1) * 100
        no_bounce = further_drop <= -10
        if no_bounce:
            n_no_bounce += 1

        pre_idx = max(a - 5, 0)
        trending_up = d.loc[a, 'price'] > d.loc[pre_idx, 'price'] if a > 0 else False
        recent_peak = d['price'].iloc[max(0, a - 30):a + 1].max() if a > 0 else d.loc[a, 'price']
        in_drawdown = (d.loc[a, 'price'] / recent_peak - 1) * 100 <= -3
        if trending_up and not in_drawdown:
            n_during_uptrend += 1

        print(f"  Run: {d.loc[a,'date'].date()} -> {d.loc[b,'date'].date()}  "
              f"SMA30 low={d.loc[a:b,'fg_sma30'].min():.1f}  price ${d.loc[a,'price']:,.0f}->${d.loc[b,'price']:,.0f}  "
              f"further drop within 30d after={further_drop:+.1f}%  "
              f"{'[NO BOUNCE >10%]' if no_bounce else ''} {'[DURING UPTREND, bukan pullback]' if (trending_up and not in_drawdown) else ''}")

    print(f"  Total run SMA30<50: {len(runs)}  |  Tanpa bounce (>10% further drop): {n_no_bounce}  |  "
          f"Terjadi saat uptrend (bukan pullback): {n_during_uptrend}")

print("\n" + "=" * 78)
print("PEMBANDING (dari findings lama, raw F&G<50 run-level, untuk referensi):")
print("  2019: 2 run, 0 no-bounce, 0 during-uptrend")
print("  2023-2024: 16 run, 1 no-bounce (6.3%), 2 during-uptrend (12.5%)")
print("=" * 78)

# ── 5. Save & final summary table ───────────────────────────────────────────
res.to_csv('research/findings/_fg_sma30_k5_trigger_pullbacks.csv', index=False)
print("\nSaved: research/findings/_fg_sma30_k5_trigger_pullbacks.csv")

print("\n" + "=" * 78)
print("5. TABEL RINGKAS 19 PULLBACK")
print("=" * 78)
print(f"{'Episode':<24}{'Trough':<12}{'RawMin':>8}{'SMAmin':>8}{'Raw<50':>8}{'SMA<50':>8}{'Lag(d)':>8}{'G30_raw':>10}{'G30_sma':>10}")
for _, r in res.iterrows():
    lag = f"{r['lag_days']:.0f}" if pd.notna(r['lag_days']) else "-"
    g30r = f"{r['gain30_raw']:+.1f}%" if pd.notna(r['gain30_raw']) else "N/A"
    g30s = f"{r['gain30_sma']:+.1f}%" if pd.notna(r['gain30_sma']) else "N/A"
    print(f"{r['episode']:<24}{str(r['trough_date']):<12}{r['fg_min']:>8.0f}{r['sma_min']:>8.1f}"
          f"{'YA' if r['raw_below50'] else 'TIDAK':>8}{'YA' if r['sma_below50'] else 'TIDAK':>8}"
          f"{lag:>8}{g30r:>10}{g30s:>10}")

print("\n" + "=" * 78)
print("SELESAI")
print("=" * 78)
