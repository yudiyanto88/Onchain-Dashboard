# STH-SOPR Bollinger Band Upper — Signal Validation di Z3 (2019 & 2023-2024)

Script: `analyze_sth_sopr_bb_z3.py`. Dikerjakan 2026-07-05. Replikasi persis dari
`analyze_asopr_bb_z3.py`, hanya metrik diganti aSOPR → STH-SOPR.

**Z3 def, window, & metodologi:** identik dengan analisis aSOPR
([[project_asopr_bb_z3]]) — RP<=Price<=AVIV Mean, 2019 difilter ke leg awal
recovery saja (2019-04-02→06-19), 2023-2024 pakai semua window Z3 (465 hari).

## Tabel hasil 6 kombinasi — STH-SOPR vs aSOPR

| MA | Std | #Signal (STH) | HitRate (STH) | #Signal (aSOPR) | HitRate (aSOPR) |
|---|---|---|---|---|---|
| 14 | 1.5 | 36 | **36%** | 41 | 29% |
| 14 | 2.0 | 25 | **32%** | 20 | 20% |
| 20 | 1.5 | 35 | 31% | 38 | 29% |
| 20 | 2.0 | 21 | 24% | 20 | 30% |
| 30 | 1.5 | 33 | 27% | 32 | 28% |
| 30 | 2.0 | 19 | 21% | 23 | 26% |

## Observasi

1. **STH-SOPR sedikit lebih baik di MA=14** (kedua std): 36% vs 29% (std 1.5),
   32% vs 20% (std 2.0) — perbedaan paling jelas di MA pendek. STH-SOPR lebih
   reaktif terhadap pergerakan cohort jangka pendek dibanding aSOPR (blend
   semua umur koin), jadi upper-band touch di MA14 menangkap capitulation
   short-term investor lebih presisi.
2. **Di MA=20/30, hasilnya campur** — STH-SOPR menang tipis di MA20/Std1.5
   (31% vs 29%) tapi kalah di MA20/Std2.0 (24% vs 30%) dan MA30 (kedua std,
   27%/21% vs 28%/26%). Tidak ada keunggulan sistematis di lookback lebih
   panjang.
3. **Kombinasi terbaik keseluruhan: STH-SOPR MA14/Std1.5 = 36% hit rate** —
   tertinggi dari 12 kombinasi (6 aSOPR + 6 STH-SOPR) yang sudah dites. Masih
   jauh dari "bersih" (64% tetap false), tapi konsisten sedikit lebih baik
   dari semua varian aSOPR.
4. **Overlap tanggal:** STH-SOPR memicu beberapa tanggal signal baru yang
   tidak muncul di aSOPR (mis. 2023-02-17, 2023-04-11, 2023-06-06, 2023-07-13,
   2023-08-08, 2023-08-29 — beberapa di antaranya JUSTRU koreksi ≥5%, seperti
   2023-04-11 -9.7%, 2023-08-08 -12.5%, 2023-08-29 -9.2%). Ini menangkap
   capitulation event yang terlewat aSOPR karena STH cohort lebih volatile
   dan overbought lebih sering secara relatif ke historinya sendiri.
5. Signal terbesar tetap sama: 2024-08-23 (-15.8%) dan 2019-05-29/05-15
   (~-11.7%/-11.1%) — capitulation event besar konsisten terdeteksi oleh
   kedua metrik.

## Kesimpulan

STH-SOPR BB upper-touch **sedikit lebih baik dari aSOPR** di lookback pendek
(MA14, hit rate 32-36% vs 20-29%), tapi masih jauh dari sinyal bersih —
mayoritas (~65-70%) signal tetap tidak diikuti koreksi ≥5%. Tetap **tidak
direkomendasikan sebagai trigger standalone**. Kalau harus pilih salah satu
untuk kandidat N-of-M trigger, STH-SOPR MA14/Std1.5 sedikit lebih unggul
secara empiris dari 12 kombinasi yang sudah divalidasi, tapi perbedaannya
tidak besar dan sample masih terbatas (2 cycle). Sesuai Hard Constraint #3,
kombinasikan dengan indikator lain sebelum dipakai untuk keputusan.
