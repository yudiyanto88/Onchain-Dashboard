# K5 — Fear & Greed Index sebagai Dip-Entry Signal (Z2/Z3)

Script: `analyze_k5_fear_greed_trigger.py`. Dikerjakan 2026-07-05.

**Kondisi diuji:** Fear & Greed turun ke bawah 50 (alternatif: di bawah 45) sebagai
sinyal dip-entry di zona Z2/Z3 (early bull recovery), dibandingkan terhadap kondisi
yang sudah divalidasi sebelumnya: STH Supply in Loss ≥50% + min(aSOPR,STH-SOPR) ≤0.98.

**Window Z2/Z3 (given):**
- Episode 1 (2019): 2019-05-07 → 2019-07-08 (63 hari)
- Episode 2 (2023-2024): 2023-03-01 → 2024-02-27 (364 hari)

## Data check
`data_fg.csv` — kolom `Fear & Greed`, tersedia harian sejak 2018-02-01. Data lengkap,
tidak ada gap di kedua window.

## Descriptive stats

| Episode | Mean | Min | Max | Hari <50 | Hari <45 |
|---|---|---|---|---|---|
| 2019 (63 hari) | 69.3 | 27 | 95 | 5 (7.9%) | 4 (6.3%) |
| 2023-2024 (364 hari) | 57.6 | 30 | 79 | 85 (23.4%) | 35 (9.6%) |

2019 recovery jauh lebih "greedy" sepanjang waktu — F&G jarang oversold karena
recovery-nya V-shape cepat. 2023-2024 recovery choppy lebih lama di bawah 50.

## Pullback identification (≥5% drop dari local high)

19 pullback total (6 di 2019, 13 di 2023-2024). Dari 19, hanya **5 pullback** yang
F&G-nya sempat turun ke bawah 50 saat trough: 1x di 2019, 4x di 2023-2024.

**Temuan kunci — pola bersih:** Kelima pullback dengan F&G<50 di trough SEMUANYA
positif di 30 hari (+41.2%, +43.8%, +18.5%, +3.6%, +26.6%). Sebaliknya, dari 14
pullback dengan F&G tetap ≥50 sepanjang pullback, hasilnya campur — banyak yang
negatif di 30d (-1.9%, -6.5%, -6.2%, -10.8%, -12.3%, -0.3%, -14.0%, -4.2%) dan
beberapa positif. F&G<50 tampak jadi filter yang cukup jelas membedakan pullback
yang genuinely oversold vs pullback dangkal — meski n=5 sangat kecil.

**Threshold <45 (lebih ketat):** 4 pullback dengan F&G<45 di trough (2019-06-09,
2023-03-10, 2023-06-14, 2023-09-11) — 4/4 positif di 30d.

## Alignment dengan STH+SOPR (kondisi tervalidasi sebelumnya)

Dari 5 pullback dengan F&G<50, hanya **2 yang align same-day** dengan
STH in Loss≥50% + SOPR≤0.98 (keduanya di 2023-2024: Mar 2023 trough $20,620,
Sep 2023 trough $25,850 — sama persis dengan 2 sinyal yang sudah confirm di
[[project_k5_dip_entry_trigger]]).

**3 pullback F&G<50 TIDAK align dengan STH+SOPR:**
- 2019-06-09 (F&G=27): STH in Loss cuma sampai 40.5% (tidak pernah tembus 50% —
  konsisten dengan finding sebelumnya bahwa 2019 recovery terlalu cepat untuk STH
  cohort mayoritas underwater).
- 2023-04-21 (F&G=50, borderline): STH loss 37.6%, tidak align.
- 2023-06-14 (F&G=41): STH loss max 76.3% tapi SOPR min 0.984 (di atas threshold
  0.98) pada hari yang sama dengan F&G rendah — kedua kondisi terpenuhi di
  pullback ini tapi TIDAK pada hari yang persis sama.
- 2024-01-22 (F&G=48): STH loss 60.6%, SOPR min 0.976 — kedua kondisi terpenuhi
  di pullback yang sama tapi tidak same-day.

**Implikasi:** F&G<45-50 menangkap 2019-06-09 dan 2023-06-14 — dua momen dip
genuine (both positif 30d) yang **terlewat** oleh kondisi STH+SOPR standalone
(karena threshold STH≥50% tidak pernah tercapai di 2019, dan same-day
co-occurrence gagal di Jun 2023 meski kedua kondisi individually terpenuhi).
F&G bisa jadi **komplemen**, bukan sekadar redundan seperti Funding Rate
([[project_k5_dip_entry_trigger]]).

## False signal check

**2019:** 2 run F&G<50 terdeteksi (4-7 Jun, 10 Jun). 0 tanpa bounce, 0 saat uptrend.
Bersih.

**2023-2024:** 16 run F&G<50 terdeteksi (granular, termasuk yang bukan trough
pullback). Dari 16:
- 1 run tanpa bounce >10% lanjutan (Aug 6-7 2023, F&G=49 → harga masih turun
  -11.7% lebih lanjut sebelum benar-benar bottom di Sep 11) — false signal jika
  dipakai standalone di titik itu.
- 2 run terjadi saat harga sedang uptrend, bukan konteks pullback (Oct 4-7 2023).

Overall false rate raw daily crossing ~19% (3/16) — cukup rendah, tapi
menunjukkan F&G<50 mentah (tanpa syarat "sedang pullback ≥5%") bisa fire di
tengah decline yang belum selesai.

## Ringkasan tabel (semua 19 pullback)

| Episode | Trough | Price@FGmin | F&G min | STH Loss max | SOPR min | Gain 14d | Gain 30d | Align STH+SOPR? |
|---|---|---|---|---|---|---|---|---|
| 2019 | 2019-05-18 | $7,347 | 65 | 22.7% | 0.996 | +16.6% | +22.4% | TIDAK |
| 2019 | 2019-05-22 | $7,633 | 69 | 23.8% | 1.004 | +2.0% | +32.4% | TIDAK |
| 2019 | 2019-05-30 | $8,255 | 73 | 17.1% | 1.009 | -0.2% | +44.3% | TIDAK |
| 2019 | 2019-06-09 | $7,789 | **27** | 40.5% | 0.932 | +19.0% | +41.2% | TIDAK |
| 2019 | 2019-06-27 | $11,187 | 92 | 7.5% | 1.019 | +1.7% | -14.0% | TIDAK |
| 2019 | 2019-07-01 | $10,837 | 63 | 22.6% | 0.998 | -12.0% | -4.2% | TIDAK |
| 2023 | 2023-03-10 | $20,620 | **33** | 51.4% | 0.866 | +33.5% | +43.8% | **YA** |
| 2023 | 2023-04-21 | $27,284 | 50 | 37.6% | 0.994 | +8.4% | -1.9% | TIDAK |
| 2023 | 2023-05-01 | $28,697 | 55 | 31.5% | 0.990 | -5.8% | -6.5% | TIDAK |
| 2023 | 2023-05-04 | $28,879 | 64 | 22.5% | 1.000 | -7.1% | -6.2% | TIDAK |
| 2023 | 2023-06-14 | $25,592 | **41** | 76.3% | 0.984 | +18.9% | +18.5% | TIDAK |
| 2023 | 2023-07-18 | $29,884 | 56 | 39.3% | 1.002 | -0.6% | -10.8% | TIDAK |
| 2023 | 2023-07-22 | $29,892 | 50 | 40.6% | 0.989 | -2.7% | -12.3% | TIDAK |
| 2023 | 2023-09-11 | $25,850 | **30** | 97.8% | 0.909 | +1.6% | +3.6% | **YA** |
| 2023 | 2023-11-21 | $35,806 | 71 | 16.6% | 0.993 | +23.2% | +22.6% | TIDAK |
| 2023 | 2023-12-11 | $41,483 | 67 | 21.0% | 0.995 | +2.5% | +11.9% | TIDAK |
| 2023 | 2023-12-15 | $41,947 | 70 | 20.9% | 1.005 | +0.3% | -0.3% | TIDAK |
| 2023 | 2023-12-17 | $41,356 | 73 | 25.9% | 0.998 | +2.3% | +4.3% | TIDAK |
| 2024 | 2024-01-22 | $40,118 | 48 | 60.6% | 0.976 | +10.5% | +26.6% | TIDAK |

(F&G min dalam **bold** = turun di bawah 45)

## Kesimpulan & rekomendasi

1. F&G<50 di trough pullback adalah filter yang berguna secara empiris di sample
   ini (5/5 positif 30d) — tapi n=5 sangat tipis (2 cycle saja), jangan overclaim.
2. F&G<45 lebih ketat, tetap 4/4 positif — dan menangkap 2 kasus yang terlewat
   STH+SOPR (2019-06-09, 2023-06-14). Kandidat trigger tambahan yang **melengkapi**
   BB1/PD1 di [[project_onchain_dashboard]], bukan pengganti.
3. Raw daily F&G<50 crossing (tanpa syarat sedang dalam pullback ≥5%) punya
   false-rate ~19% di 2023 — pakai sebagai trigger HANYA dalam konteks pullback
   yang sudah terkonfirmasi, bukan level absolut harian.
4. Sample kecil (n=19 pullback, 2 cycle) — sesuai Hard Constraint #3, F&G tidak
   boleh jadi gate standalone. Perlakukan sebagai N-of-M trigger kandidat.
