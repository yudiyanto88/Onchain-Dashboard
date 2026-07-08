# STH-MVRV (Price/STH_RP) sebagai Proxy K6 Trigger — Z2+Z3, Cycle 2019 & 2023

Script: `analyze_sth_mvrv_k6_trigger.py`. Dikerjakan 2026-07-05.

**Definisi:** STH-MVRV = Price / STH_RP. Window Z2+Z3 identik dengan
[[project_k5_dip_entry_trigger]] dan [[project_price_stretch_sth_rp]]
(Z2 start = STH RP cross atas RP, Z3 end = price cross atas AVIV Upper 0.5σ
sustained ≥3 hari). Signal = STH-MVRV menyentuh/melewati threshold, hari
konsekutif digabung jadi 1 signal (beda metodologi dari analisis stretch
sebelumnya yang pakai raw daily count).

## Window

- 2019 CYCLE: 2019-05-07 → 2019-07-08 (63 hari)
- 2023 CYCLE: 2023-03-01 → 2024-02-27 (364 hari)

## 1. Distribusi STH-MVRV harian

| Cycle | Min | P25 | Median | Mean | P75 | P90 | Max |
|---|---|---|---|---|---|---|---|
| 2019 (63 hari) | 1.234 | 1.372 | 1.422 | 1.430 | 1.509 | 1.562 | 1.739 |
| 2023 (364 hari) | 0.898 | 1.026 | 1.109 | 1.113 | 1.201 | 1.267 | 1.359 |
| **Gabungan (427 hari)** | 0.898 | 1.035 | 1.157 | 1.160 | 1.249 | 1.379 | 1.739 |

Sama seperti temuan stretch sebelumnya — STH-MVRV 2019 jauh lebih tinggi di
semua persentil. 2023 bahkan sempat di bawah 1.0 (price < STH RP, 0.898) di
awal window sebelum Z2 benar-benar established.

## 2. Threshold test — signal (konsekutif digabung) vs koreksi ≥5% dalam 14 hari

| Threshold | #Signal (2019) | Hit Rate (2019) | #Signal (2023) | Hit Rate (2023) | #Signal (Gabungan) | Hit Rate (Gabungan) |
|---|---|---|---|---|---|---|
| ≥1.10 | 1 | 0% | 9 | 33% | 10 | 30% |
| ≥1.15 | 1 | 0% | 5 | 20% | 6 | 17% |
| ≥1.20 | 1 | 0% | 13 | 31% | 14 | 29% |
| ≥1.25 | 2 | 0% | 4 | 0% | 6 | 0% |
| ≥1.30 | 2 | 0% | 6 | 50% | 8 | 38% |
| ≥1.40 | 8 | 50% | 0 | N/A | 8 | 50% |
| ≥1.50 | 7 | 71% | 5 | (n=5 dari 2019) | 7 | **71%** |

**Observasi kunci:**
1. **Tidak monotonik bersih** di rentang 1.10-1.30 (naik-turun: 30%→17%→29%→
   **0%**→38%) — sample per threshold kecil (n=6-14 signal) sehingga rentan
   noise. Threshold 1.25 kebetulan 0/6 di data ini, jangan overinterpretasi
   sebagai "level aman".
2. **Di atas 1.30, hit rate naik tajam dan konsisten**: 38%→50%→71%. Tapi
   perhatikan komposisi sample: threshold ≥1.40 dan ≥1.50 **didominasi/hanya
   dari 2019** (2023 tidak pernah tembus 1.40 — max STH-MVRV 2023 cuma 1.359).
   Jadi "hit rate tinggi di threshold tinggi" sebagian besar cerita 2019, bukan
   pola universal yang terverifikasi di 2 cycle independen.
3. **Level 1.50 = hit rate tertinggi (71%, n=7)** tapi n kecil dan sample
   effectively dari 1 cycle saja untuk rentang ini.

## 3. STH-MVRV di local peak sebelum tiap koreksi ≥5%

**2019 (6 koreksi):** rata-rata = **1.621** (semua peak antara 1.545-1.739)

**2023 (13 koreksi):** rata-rata = **1.248** (range 1.121-1.320)

**Gabungan (n=19):** rata-rata = **1.366**, median = **1.320**

**Observasi:** Sama seperti temuan stretch sebelumnya — "level natural"
sebelum koreksi jauh berbeda antar cycle. 2019 butuh STH-MVRV >1.5 dulu
sebelum koreksi genuine terjadi, sementara 2023 koreksi ≥5% sudah muncul
dari STH-MVRV serendah ~1.12. **Tidak ada satu angka absolut yang berlaku
universal** sebagai "level bahaya" K6.

## Kesimpulan

1. STH-MVRV sebagai proxy trigger K6 punya pola yang mirip temuan stretch
   ([[project_price_stretch_sth_rp]]) — hit rate cenderung naik di threshold
   lebih tinggi, tapi TIDAK bersih-monotonik di rentang menengah (1.10-1.30)
   karena sample kecil per bucket.
2. **Threshold tinggi (≥1.40, ≥1.50) secara statistik didominasi data 2019** —
   generalisasi ke cycle lain (termasuk 2023, yang tidak pernah mencapai level
   ini) belum terverifikasi. Perlu skeptis terhadap threshold absolut tetap.
3. STH-MVRV di peak sebelum koreksi (rata-rata 1.62 di 2019 vs 1.25 di 2023)
   menegaskan level "bahaya" relatif terhadap cycle berjalan, bukan angka
   tetap — konsisten dengan kesimpulan analisis stretch sebelumnya (memang
   STH-MVRV = 1 + stretch/100, jadi ini variabel yang sama diekspresikan
   beda unit).
4. Sesuai Hard Constraint #3 — jangan pakai threshold STH-MVRV absolut
   sebagai gate standalone untuk K6. Kalau perlu proxy, pertimbangkan
   threshold relatif per-cycle (mis. percentile historis cycle berjalan)
   dan tetap kombinasikan dengan indikator lain (STH Supply in Loss/Profit,
   SOPR) sebelum dipakai untuk sizing/deploy keputusan.
