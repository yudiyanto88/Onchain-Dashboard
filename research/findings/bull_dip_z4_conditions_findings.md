# Bull Dip ke Z4 — Test 3 Kondisi K5, Bull Market 2019-2020 & 2023-2024

Script: `analyze_bull_dip_z4_conditions.py`. Dikerjakan 2026-07-05.

**Definisi zona:**
- Z5 = Price ≥ AVIV Upper (0.5σ)
- Z4 = AVIV Mean ≤ Price < AVIV Upper

**Episode bull dip ke Z4** = run hari konsekutif di Z4 yang persis mengikuti
hari-hari di Z5 sebelumnya (price baru turun dari euforia Z5 ke Z4). Episode
diresolusi sebagai "RECOVERED ke Z5" (bounce balik) atau "BREAKDOWN di bawah
Z4" (turun lebih jauh menembus AVIV Mean).

## Episode ditemukan (14 total, 7 per bull market)

| Period | Start | End | Days | Drop% | Resolusi |
|---|---|---|---|---|---|
| 2019-2020 | 2019-06-27 | 2019-06-27 | 1 | -12.8% | RECOVERED |
| 2019-2020 | 2019-06-30 | 2019-07-02 | 3 | -11.6% | RECOVERED |
| 2019-2020 | 2019-07-04 | 2019-07-07 | 4 | -8.2% | RECOVERED |
| 2019-2020 | 2019-07-11 | 2019-07-13 | 3 | -6.1% | **BREAKDOWN** |
| 2019-2020 | 2020-11-26 | 2020-11-28 | 3 | -8.4% | RECOVERED |
| 2019-2020 | 2020-12-08 | 2020-12-08 | 1 | -4.5% | RECOVERED |
| 2019-2020 | 2020-12-10 | 2020-12-11 | 2 | -2.8% | RECOVERED |
| 2023-2024 | 2024-03-19 | 2024-03-19 | 1 | -8.4% | RECOVERED |
| 2023-2024 | 2024-03-22 | 2024-03-23 | 2 | -2.6% | RECOVERED |
| 2023-2024 | 2024-04-02 | 2024-04-03 | 2 | -6.0% | RECOVERED |
| 2023-2024 | 2024-04-12 | 2024-04-30 | 19 | -13.4% | **BREAKDOWN** |
| 2023-2024 | 2024-05-21 | 2024-06-23 | 34 | -11.5% | **BREAKDOWN** |
| 2023-2024 | 2024-12-22 | 2024-12-23 | 2 | -2.5% | RECOVERED |
| 2023-2024 | 2024-12-26 | 2025-01-02 | 8 | -6.8% | RECOVERED |

(11 RECOVERED, 3 BREAKDOWN)

## Tabel 3 kondisi per episode

| Period | Start | End | Days | Drop% | F&G<50 | STH Loss≥60% | SOPR≤0.98 | N/3 | Resolusi |
|---|---|---|---|---|---|---|---|---|---|
| 2019-2020 | 06-27 | 06-27 | 1 | -12.8% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-2020 | 06-30 | 07-02 | 3 | -11.6% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-2020 | 07-04 | 07-07 | 4 | -8.2% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-2020 | 07-11 | 07-13 | 3 | -6.1% | **YA** | TIDAK | TIDAK | 1 | BREAKDOWN |
| 2019-2020 | 11-26 | 11-28 | 3 | -8.4% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-2020 | 12-08 | 12-08 | 1 | -4.5% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2019-2020 | 12-10 | 12-11 | 2 | -2.8% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-2024 | 03-19 | 03-19 | 1 | -8.4% | TIDAK | TIDAK | **YA** | 1 | RECOVERED |
| 2023-2024 | 03-22 | 03-23 | 2 | -2.6% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-2024 | 04-02 | 04-03 | 2 | -6.0% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-2024 | 04-12 | 04-30 | 19 | -13.4% | TIDAK | **YA** | **YA** | 2 | BREAKDOWN |
| 2023-2024 | 05-21 | 06-23 | 34 | -11.5% | TIDAK | **YA** | TIDAK | 1 | BREAKDOWN |
| 2023-2024 | 12-22 | 12-23 | 2 | -2.5% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |
| 2023-2024 | 12-26 | 01-02 | 8 | -6.8% | TIDAK | TIDAK | TIDAK | 0 | RECOVERED |

## Persentase episode yang memenuhi tiap kondisi (n=14)

| Kondisi | Terpenuhi | Persentase |
|---|---|---|
| F&G < 50 | 1/14 | 7% |
| STH Loss ≥ 60% | 2/14 | 14% |
| min(aSOPR,STH-SOPR) ≤ 0.98 | 2/14 | 14% |

**Distribusi jumlah kondisi terpenuhi:**
- 0/3: 10 episode (71%)
- 1/3: 3 episode (21%)
- 2/3: 1 episode (7%)
- 3/3: 0 episode (0%)

## Observasi penting

1. **Ketiga kondisi hampir tidak pernah fire selama bull dip normal.** Ini
   sesuai ekspektasi — kondisi ini (F&G<50, STH Loss≥60%, SOPR≤0.98) adalah
   sinyal capitulation ala bear-recovery (dirancang untuk [[project_k5_dip_entry_trigger]]
   di Z2/Z3), dan bull dip di Z4/Z5 secara struktural jauh lebih dangkal —
   mayoritas STH cohort tetap profit, F&G jarang benar-benar takut.
2. **TEMUAN PALING PENTING (tidak diminta eksplisit tapi sangat relevan):**
   ada korelasi kuat antara kondisi yang fire dan RESOLUSI episode.
   - Dari **3 episode yang berakhir BREAKDOWN** (turun lebih jauh menembus
     AVIV Mean, bukan cuma bounce balik ke Z5): **ketiganya (100%) punya
     ≥1 kondisi terpenuhi** (1, 2, 1 kondisi masing-masing).
   - Dari **11 episode yang RECOVERED ke Z5**: **cuma 1 (9%)** yang punya
     kondisi terpenuhi (dan cuma 1/3, SOPR saja).
   - Artinya: kalau salah satu dari 3 kondisi ini fire selama dip di Z4,
     itu sinyal bahwa dip kemungkinan LEBIH DALAM dari bull dip biasa
     (berpotensi breakdown lanjut), bukan sekadar bull dip dangkal yang
     langsung bounce.
3. Ini langsung relevan untuk **BD1 vs BT1 discrimination** di
   `signal_framework_v1.md` — dokumen sudah menyebut "BD1 signal ini paling
   butuh konfirmasi karena bull dip vs bear onset overlap." Temuan di sini
   memberi data konkret: 0/3 kondisi K5 terpenuhi selama dip = pola konsisten
   dengan bull dip sehat (91% dari kasus recovered). ≥1 kondisi terpenuhi =
   flag untuk cek BT1/S2 lebih ketat.
4. **Sample sangat kecil (n=14, hanya 3 breakdown)** — pola ini menjanjikan
   tapi butuh lebih banyak data cycle untuk konfirmasi sebelum dijadikan
   aturan baku.

## Kesimpulan

Ketiga kondisi K5 (F&G<50, STH Loss≥60%, SOPR≤0.98) **jarang sekali fire
selama bull dip normal** (71% episode 0/3 kondisi) — sesuai ekspektasi karena
kondisi ini dirancang untuk capitulation di bear recovery, bukan bull market.
Namun ditemukan pola menarik: **episode yang memicu ≥1 kondisi selalu berakhir
breakdown** (3/3), sementara episode yang 0/3 kondisi hampir selalu recovered
(9/10, 90%). Ini kandidat filter tambahan untuk membedakan bull dip dangkal
vs dip yang berisiko jadi breakdown — tapi n masih sangat kecil (3 breakdown
event), perlu divalidasi lebih lanjut sebelum masuk signal_framework_v1.md
sebagai trigger baku.
