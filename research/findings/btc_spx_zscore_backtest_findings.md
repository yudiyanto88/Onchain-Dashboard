# BTC/SPX Ratio Z-Score — backtest jendela 1, 2, 4 tahun (21 Sep 2026)

Script: `research/analyze_btc_spx_zscore.py`
Output: `_btc_spx_zscore_summary.csv`, `_btc_spx_zscore_signals.csv`, data S&P `_spx_yahoo.csv`

## Setelan
- Z = (log(BTC/SPX) − SMA_w) ÷ SD_w, rata-rata dan SD dari jendela yang sama
- S&P di akhir pekan = harga penutupan terakhir. BTC dari ChartInspect, S&P dari Yahoo (^GSPC)
- Sinyal = episode: hari pertama Z menembus ambang. Sinyal berikutnya baru dihitung setelah Z kembali melewati 0
- Periode uji sama untuk semua jendela: 2 Jan 2014 – 18 Sep 2026
- Baseline (semua hari): return 180 hari median +22%, naik 60%; penurunan terdalam 180 hari median −18%

## Hasil sisi beli (Z di bawah ambang)

| Jendela | Ambang | Sinyal | Return 180h median | Naik 180h | Penurunan terdalam 180h (median / terburuk) |
|---|---|---|---|---|---|
| 1 tahun | −2.0 | 4 | −22% | 25% | −39% / −45% |
| 1 tahun | −2.5 | 3 | −16% | 33% | −30% / −34% |
| 2 tahun | −1.5 | 2 | +20% | 50% | −17% / −20% |
| 2 tahun | −2.0 | 2 | +38% | 100% | −4% / −7% |
| 4 tahun | semua | 0 | — | — | Z tidak pernah turun di bawah −0.52 |

Sinyal 2 tahun, Z ≤ −2.0: 9 Nov 2022 ($15.9k, dekat dasar siklus) dan 5 Feb 2026 ($62.8k, return 365 hari belum tersedia).

Cek per hari (bukan per episode), 180 hari ke depan:
- 1 tahun, Z ≤ −2: 214 hari, median −6%, naik 46%. Lebih buruk dari baseline.
- 2 tahun, Z ≤ −2: 69 hari, median +61%, naik 91%, penurunan terdalam median −4%. Tapi semua hari ini berasal dari hanya 2 episode.

## Hasil sisi jual (Z di atas ambang)
Tidak ada jendela yang layak dipakai sebagai sinyal jual. Sesudah Z tinggi, harga BTC umumnya malah terus naik. Contoh: 1 tahun, +2.0 → naik dalam 180 hari pada 80% sinyal. 2 tahun, +2.5 (Mei 2017, Des 2020, Feb 2024) → semuanya muncul di tengah bull market. Z tinggi = BTC sedang kuat, bukan tanda puncak.

## Kesimpulan
1. **Jendela 1 tahun: tolak sebagai sinyal beli.** Sinyalnya muncul di awal bear (Okt 2014, Nov 2018, Jan/Mei 2022, Nov 2025), lalu harga masih turun median −39%. Dengan leverage, ini persis skenario Oktober 2025.
2. **Jendela 2 tahun: kandidat, belum terbukti.** Hasilnya bagus, tapi hanya 2 episode dan satu belum selesai. Jendela ini juga melewatkan dasar 2018 sepenuhnya (Z minimum −0.6).
3. **Jendela 4 tahun: tidak berguna.** Tidak pernah memberi sinyal beli.
4. **Sisi jual: jangan dipakai.**

Status: 2 tahun Z ≤ −2 sebaiknya diperlakukan sebagai hipotesis, bukan aturan. Sampel terlalu kecil untuk masuk framework. Kalau mau dilanjutkan, uji berikutnya: apakah sinyal ini menambah informasi di atas zona ZC/ZD yang sudah ada, atau hanya mengulang sinyal yang sama.

---

# BTC/XAU (emas) — setelan dan periode uji sama (21 Sep 2026)

Emas dari Yahoo GC=F (futures bulan terdekat, pendekatan harga spot). Jalankan: `python research/analyze_btc_spx_zscore.py xau`
Output: `_btc_xau_zscore_summary.csv`, `_btc_xau_zscore_signals.csv`, `_xau_yahoo.csv`, chart `research/btc_xau_zscore_3_jendela.png`

| Jendela | Ambang | Sinyal | Return 180h median | Naik 180h | Penurunan terdalam 180h (median / terburuk) |
|---|---|---|---|---|---|
| 1 tahun | −2.0 | 5 | −9% | 40% | −36% / −38% |
| 1 tahun | −2.5 | 5 | +36% | 60% | −22% / −34% |
| 2 tahun | −2.0 | 2 | +23% | 50% | −13% / −30% |
| 2 tahun | −2.5 | 1 | −26% | 0% | −35% |
| 4 tahun | −2.0 | 0 | — | — | — |

Sinyal 2 tahun, Z ≤ −2.0: 21 Nov 2022 ($15.8k, bagus) dan 15 Des 2025 ($86.5k, 180 hari kemudian −26%, penurunan terdalam −30%).

Kesimpulan: BTC/XAU lebih buruk dari BTC/SPX sebagai sinyal beli. Jendela 2 tahun, yang terbaik di BTC/SPX, di sini memberi sinyal terlalu awal di bear 2025–2026. Jendela 1 tahun tetap bermasalah (penurunan terdalam median −36% di Z ≤ −2). Sisi jual sama seperti SPX: Z tinggi diikuti kenaikan, bukan puncak.

---

# Tambahan syarat: bullish divergence (21 Sep 2026)

Definisi (fungsi `divergences()` di script):
- Pivot low Z = titik terendah dalam ±n hari. Pivot baru diketahui n hari kemudian, jadi tanggal sinyal = pivot kedua + n hari (tanpa melihat masa depan)
- Low pertama Z ≤ ambang. Low berikutnya dalam episode yang sama (Z belum kembali ke atas 0): Z lebih tinggi, tapi harga BTC lebih rendah → sinyal
- Satu sinyal per episode. Diuji n = 14, 30, 60 hari dan ambang low pertama −1.5, −2, −2.5
Output: `_btc_{spx,xau}_zscore_divergence_summary.csv`, `_btc_{spx,xau}_zscore_divergence_signals.csv`, chart `research/btc_zscore_divergence_1y.png`

Hasil utama: jendela 1 tahun, pivot 30 hari, low pertama ≤ −2

| Pembanding | Tanggal sinyal | Harga | Return 180h | Penurunan terdalam 180h |
|---|---|---|---|---|
| SPX | 2 Mar 2019 | $3.9k | +149% | −3% |
| SPX | 21 Des 2022 | $16.8k | +60% | −2% |
| SPX | 5 Jul 2026 | $63.7k | belum lengkap | −2% sejauh ini |
| XAU | 9 Des 2022 | $17.1k | +55% | −4% |
| XAU | 6 Jul 2026 | $64.0k | belum lengkap | −3% sejauh ini |

Bandingkan dengan Z ≤ −2 tanpa divergence (jendela 1 tahun, SPX): penurunan terdalam median −39%. Divergence membuang semua sinyal yang terlalu awal (Okt 2014, Nov 2018, Mei 2022, Nov 2025).

Sensitivitas:
- Pivot 14 hari: menambah sinyal Jan 2015 (SPX, −43% sesudahnya) dan Jun 2022 (XAU, −46%). Terlalu pendek.
- Pivot 60 hari: sinyal lebih telat. SPX 2019 hilang, 2022 masuk di $22.7k.
- Jendela 2 dan 4 tahun: hampir tidak pernah membentuk divergence (SPX 0 sinyal, XAU hanya Jul 2026).
- Ambang low pertama (−1.5 / −2 / −2.5) hampir tidak mengubah hasil.

Batasan:
- Hanya 2 sinyal SPX dan 1 sinyal XAU yang sudah selesai. Terlalu sedikit untuk jadi bukti.
- Pivot 30 hari dipilih setelah melihat hasilnya, jadi ada risiko overfit.
- Divergence tidak menangkap dasar 2015 (SPX, pivot 30) dan terlambat 1–3 bulan dari dasar harga (2019: dasar $3.2k, sinyal $3.9k).

Jendela 2 tahun + divergence (chart `research/btc_zscore_divergence_2y.png`): SPX 0 sinyal, XAU 1 sinyal (6 Jul 2026, belum selesai). Penyebabnya: di jendela 2 tahun, low Z biasanya jatuh bersamaan dengan low harga. Contoh SPX: Jun 2022 Z −0.83 (harga $19.0k) lalu Nov 2022 Z −2.21 (harga $15.8k), jadi Z juga membuat low lebih rendah. SPX 2026: Feb Z −2.28 ($62.8k) lalu Jun Z −2.37 ($61.0k), sama-sama turun. Jendela 2 tahun bergerak lambat, sehingga jarang membentuk higher low. Divergence tidak cocok untuk jendela ini.

---

# BTC/NDX (Nasdaq 100, ^NDX) — setelan dan periode uji sama (21 Sep 2026)

Jalankan: `python research/analyze_btc_spx_zscore.py ndx`. Chart: `research/btc_ndx_zscore_3_jendela.png`, `research/btc_ndx_zscore_divergence.png`

Sinyal Z ≤ −2 tanpa divergence:
| Jendela | Sinyal | Return 180h median | Naik 180h | Penurunan terdalam 180h (median / terburuk) |
|---|---|---|---|---|
| 1 tahun | 4 (Nov 2014, Nov 2018, Jun 2022, Nov 2025) | −23% | 25% | −34% / −45% |
| 2 tahun | 2 (13 Nov 2022 $16.3k, 5 Feb 2026 $62.8k) | +33% | 100% | −5% / −7% |
| 4 tahun | 0 | — | — | — |

Dengan divergence (pivot 30 hari, low pertama ≤ −2):
- 1 tahun: 13 Des 2022 ($17.8k, +46% dalam 180 hari, turun terdalam −8%) dan 7 Mar 2026 ($67.3k, +15% dalam 180 hari, turun terdalam −13%). Divergence 2026 sangat tipis: Z −3.96 lalu −3.86.
- 2 tahun: 0 sinyal.
- Berbeda dari SPX, tidak ada sinyal Mar 2019.

Kesimpulan: pola BTC/NDX hampir sama dengan BTC/SPX. Jendela 1 tahun tanpa divergence berbahaya. Jendela 2 tahun tanpa divergence memberi dua sinyal yang sama dengan SPX. Z-Score sekarang: 1 tahun −0.52, 2 tahun −1.16, 4 tahun −0.27.
