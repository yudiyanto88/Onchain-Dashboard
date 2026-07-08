# Local High Harga vs STH-MVRV — Divergence Test, Z2+Z3 Cycle 2019 & 2023

Script: `analyze_local_high_sth_mvrv_divergence.py`. Dikerjakan 2026-07-05.

**Definisi:** Local high = price[t] > 5 hari sebelum DAN sesudahnya (strict).
Untuk tiap pasangan local high berurutan (H_k → H_k+1): price higher high?
STH-MVRV higher high juga? Window Z2+Z3 identik dengan analisis sebelumnya
([[project_k5_dip_entry_trigger]], [[project_sth_mvrv_k6_trigger]]).

## Window & local high

- 2019: 4 local high dalam window (2019-05-15, 05-27, 06-02, 06-26) → 3 pasangan
- 2023: 27 local high dalam window → 26 pasangan
- Total: 29 pasangan local high berurutan

## Koreksi asumsi awal

**Asumsi "price selalu higher high di uptrend" TERBUKTI SALAH.** Dari 29
pasangan, hanya 20 yang price-nya benar-benar higher high (12 confirmed + 8
divergence); **9 pasangan (31%) price-nya justru LOWER high** — wajar karena
Z2+Z3 bukan uptrend murni tanpa jeda, ada banyak local high minor di tengah
konsolidasi/koreksi (terutama di window panjang 2023 yang mencakup periode
choppy Mei-Oktober 2023).

## Breakdown pola (a)/(b)/(c) per cycle — untuk kandidat K6 trigger

| Cycle | Total pasangan | (a) Price HH saja | (b) Price HH + MVRV HH | (c) Price HH, MVRV tidak HH | Price tidak HH |
|---|---|---|---|---|---|
| 2019 | 3 | 2 | 1 | 1 | 1 |
| 2023 | 26 | 18 | 11 | 7 | 8 |
| **Gabungan** | **29** | **20** | **12** | **8** | **9** |

Hit rate koreksi ≥5%/14 hari per pola (gabungan): (a) 60% (12/20), (b) 58%
(7/12), (c) 62% (5/8). (b) vs (a) hampir identik — syarat MVRV HH tidak
menaikkan presisi dibanding price HH saja. (b) vs (c) juga hampir identik,
arah bahkan terbalik dari intuisi klasik "divergence lebih bearish".

## Hasil utama: Confirmed vs Divergence

| Grup | n | Koreksi ≥5% | Hit Rate |
|---|---|---|---|
| **Confirmed** (price HH + STH-MVRV HH) | 12 | 7 | **58%** |
| **Divergence** (price HH TANPA STH-MVRV HH) | 8 | 5 | **62%** |
| Price TIDAK HH (sanity check) | 9 | 2 | 22% |

**Per cycle:**
- 2019: Confirmed 1/1 (100%), Divergence 1/1 (100%) — n terlalu kecil untuk
  disimpulkan apa-apa.
- 2023: Confirmed 6/11 (55%), Divergence 4/7 (57%) — hampir identik.

## Jawaban ke pertanyaan inti: apakah STH-MVRV divergence menambah informasi?

**TIDAK — di data ini, tidak ada perbedaan berarti antara grup confirmed dan
grup divergence** (58% vs 62%, selisih 4 poin, arahnya bahkan berlawanan dari
intuisi klasik "bearish divergence lebih berbahaya"). Dengan n=12 vs n=8,
selisih ini sepenuhnya dalam rentang noise — bukan sinyal yang bisa dipakai.

**Artinya:** syarat tambahan "STH-MVRV juga harus higher high" TIDAK
menyaring apa pun secara berguna — baik price HH dikonfirmasi STH-MVRV HH
maupun tidak, probabilitas koreksi ≥5% dalam 14 hari sama-sama sekitar
55-60%. Price higher high sendiri (regardless STH-MVRV) sudah cukup
informatif (58-62% gabungan, n=20), jauh lebih tinggi dari base rate "price
tidak HH" (22%, n=9).

## Observasi tambahan

1. **Temuan paling kuat justru bukan yang ditanya**: pasangan local high di
   mana price GAGAL membuat higher high (lower high, n=9) punya hit rate jauh
   lebih rendah (22%) dibanding kedua grup higher-high (58-62%). Artinya
   "harga berhasil membuat local high baru yang lebih tinggi" sendiri sudah
   jadi sinyal risiko koreksi yang lebih kuat daripada status STH-MVRV-nya.
2. Sample per grup kecil (n=8-12 untuk perbandingan utama), dan didominasi
   data 2023 (2019 cuma n=1 tiap grup) — kesimpulan "tidak ada beda" perlu
   divalidasi lagi kalau ada data cycle tambahan di masa depan.
3. Ini konsisten dengan pola yang berulang di analisis-analisis sebelumnya
   ([[project_asopr_bb_z3]], [[project_sth_mvrv_k6_trigger]]) — indikator
   berbasis SOPR/MVRV relatif di Z2/Z3 cenderung noisy dan sering TIDAK
   menambah presisi dibanding sinyal harga murni.

## Kesimpulan

STH-MVRV higher-high sebagai syarat konfirmasi tambahan pada local high harga
**tidak terbukti menambah informasi** untuk memprediksi koreksi ≥5% dalam 14
hari di sample 2019+2023 (n=20 pasangan HH). Kalau butuh sinyal early-warning
di Z2/Z3, price-based higher-high pattern sendiri sudah menangkap sebagian
besar informasi yang relevan; menambahkan syarat STH-MVRV HH tidak
memperbaiki precision di data ini. Jangan pakai STH-MVRV divergence sebagai
gate tambahan untuk K6/K-series trigger berdasarkan temuan ini, kecuali ada
data cycle tambahan yang mengubah kesimpulan.
