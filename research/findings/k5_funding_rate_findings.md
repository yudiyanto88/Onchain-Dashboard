# K5 Funding Rate as Additional Confirmation — Findings

Script: `analyze_k5_funding_rate_trigger.py`. Data per 2026-07-05 snapshot.

## Langkah 0 — Ketersediaan data
`data_derivatives.csv` punya kolom `funding_rate` (dan `total_oi`). Historical coverage: **2020-02-28 → sekarang** (non-null pertama 2020-03-31).

- **2018-2019 episode** (Z2/Z3: 2019-05-07 → 2019-07-08): **0 hari** data FR — window selesai sebelum funding rate mulai tercatat di source ini. Analisis FR untuk episode ini **tidak bisa dilakukan** (bukan soal magnitude kecil, datanya memang tidak exist).
- **2022-2023 episode** (Z2/Z3: 2023-03-01 → 2024-02-27): 364/364 hari ada data — analisis penuh.

## FR stats (2022-2023 window)
Mean 0.089, min -0.213 (2023-03-12), max 0.531. FR negatif 10/364 hari (2.7%). FR ≤ -0.01: 7/364 hari (1.9%) — threshold ini natural (jarang tersentuh, bukan noise harian).

## Pullback × FR (13 pullback total)
Hanya 2/13 pullback yang FR-nya pernah ≤-0.01, dan keduanya **sama persis** dengan 2 pullback yang sudah confirm via STH≥50%+SOPR≤0.98 (lihat `k5_dip_entry_trigger_findings.md`):

| Pullback | FR min | Tanggal | Price di FR min | Gain 7d | Gain 14d | Gain 30d |
|---|---|---|---|---|---|---|
| Mar 2023 | -0.213 | 2023-03-12 | $22,146 | +26.6% | +26.5% | +36.5% |
| Aug 2023 | -0.028 | 2023-08-17 | $26,668 | -1.8% | -2.7% | -0.3% |

Catatan timing: Mar 2023, FR min terjadi 2 hari setelah trough harga aktual ($20,214 pada 03-10) dan di harga lebih tinggi ($22,146) — pakai FR sebagai trigger utama akan entry lebih mahal dibanding STH+SOPR asli ($20,376). Aug 2023: FR min persis sama tanggal/harga dengan konfirmasi SOPR.

## Skenario A vs B
- A (STH+SOPR saja): 2 sinyal fire.
- B (A + FR≤-0.01 dalam ±5 hari): 2 sinyal tetap fire — **tidak mengurangi**, tapi juga tidak menambah sinyal baru.

## False signal
0 kejadian FR sharp-drop tanpa bounce. 0 kejadian FR sharp-drop di luar konteks pullback. (n terlalu kecil untuk klaim statistik kuat — hanya 2 event total.)

## Kesimpulan
FR ≤-0.01 align persis dengan 2 entry yang sudah tervalidasi di 2023, tanpa false signal — tapi terlihat sebagai **konfirmasi redundan** dengan STH+SOPR (metrik-metrik ini bergerak bersamaan saat capitulation nyata), bukan penambah presisi independen. Sample size n=2, tidak cukup untuk klaim kuat. Tidak bisa divalidasi sama sekali untuk cycle 2019 karena data FR belum exist saat itu.

**How to apply:** FR bisa dipakai sebagai supporting/tie-breaker signal dalam N-of-M framework, bukan gate independen atau pengganti STH+SOPR. Perlu lebih banyak episode/cycle sebelum dianggap sinyal yang robust.
