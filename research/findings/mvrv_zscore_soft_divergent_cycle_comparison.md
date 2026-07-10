# Perbandingan Pola Soft-Divergent "MVRV Flat, Z Turun" Antar Cycle

**Tanggal:** 2026-07-10
**Sumber prompt:** `prompt_soft_divergent_cycle_comparison.md` (dari sesi Claude.ai)
**Tujuan:** Cek apakah pola "MVRV flat, Z-score turun" yang muncul 5x di cycle 2023-2025 (current) tepat di titik-titik topping itu spesifik ke cycle sekarang (hipotesis: volatility compression karena market makin matang), atau sudah ada juga di cycle-cycle besar sebelumnya (2017, 2021) dengan frekuensi/positioning yang mirip.

Data sumber: `research/findings/mvrv_zscore_independence_pairs.csv` (329 baris, dari sesi independence check sebelumnya). Filter: `Class == 'DIVERGEN (MVRV naik/flat, Z turun)'` DAN `Dir_MVRV == 'FLAT'` (subset soft, bukan hard-reversal).

---

## 1. Frekuensi per cycle

| Cycle | Kejadian (n) | Total pasangan | % dari total pasangan |
|---|---|---|---|
| 2011 | 1 | 20 | 5.0% |
| 2013 | 1 | 56 | 1.8% |
| **2017** | **6** | 84 | **7.1%** |
| 2019 (mini-cycle) | 0 | 28 | 0.0% |
| **2021** | **1** | 59 | **1.7%** |
| **2023-2025 (current)** | **5** | 82 | **6.1%** |

**Catatan penting:** 2017 (n=6, 7.1%) justru punya frekuensi RELATIF sedikit lebih tinggi dibanding 2023-2025 (n=5, 6.1%) — bukan lebih rendah. 2021 cuma punya **1 kejadian (1.7%)** — sample terlalu kecil untuk kesimpulan solid, dinyatakan eksplisit sebagai keterbatasan sesuai instruksi task.

---

## 2. Tabel data mentah — 2017 (n=6)

| Tanggal (curr) | Price prev → curr | MVRV (arah) | Z-Score (arah) | RollStd (curr) |
|---|---|---|---|---|
| 29-Feb-16 | $440.69 → $438.68 | 1.436 → 1.421 (FLAT) | 1.864 → 1.703 (**TURUN**) | 0.235 |
| 05-Apr-16 | $427.51 → $424.63 | 1.370 → 1.356 (FLAT) | 1.289 → 1.174 (**TURUN**) | 0.248 |
| 09-May-16 | $468.16 → $462.13 | 1.470 → 1.442 (FLAT) | 1.494 → 1.291 (**TURUN**) | 0.248 |
| 22-Aug-16 | $595.92 → $588.55 | 1.621 → 1.598 (FLAT) | 0.918 → 0.783 (**TURUN**) | 0.306 |
| 11-Jun-17 | $2,491.18 → $2,976.89 | 3.560 → 3.612 (FLAT) | 4.420 → 3.407 (**TURUN**) | 0.455 |
| 21-Oct-17 | $5,824.80 → $6,033.14 | 3.134 → 3.091 (FLAT) | 1.572 → 1.436 (**TURUN**) | 0.459 |

## 3. Tabel data mentah — 2021 (n=1)

| Tanggal (curr) | Price prev → curr | MVRV (arah) | Z-Score (arah) | RollStd (curr) |
|---|---|---|---|---|
| 30-Nov-20 | $19,118.12 → $19,667.50 | 2.604 → 2.628 (FLAT) | 3.274 → 3.130 (**TURUN**) | 0.316 |

## 4. Tabel data mentah — 2023-2025 (current, n=5, recap dari laporan sebelumnya)

| Tanggal (curr) | Price prev → curr | MVRV (arah) | Z-Score (arah) | RollStd (curr) |
|---|---|---|---|---|
| 01-Aug-23 | $30,101.26 → $29,703.81 | 1.471 → 1.457 (FLAT) | 1.437 → 1.317 (**TURUN**) | 0.240 |
| 22-Dec-23 | $44,191.40 → $44,028.19 | 2.061 → 2.023 (FLAT) | 2.928 → 2.507 (**TURUN**) | 0.254 |
| 08-Apr-24 | $71,321.70 → $71,636.46 | 2.551 → 2.522 (FLAT) | 2.254 → 2.053 (**TURUN**) | 0.401 |
| 17-Dec-24 | $98,943.50 → $106,168.86 | 2.726 → 2.683 (FLAT) | 2.548 → 1.989 (**TURUN**) | 0.262 |
| 22-Jul-25 | $119,831.20 → $119,963.30 | 2.411 → 2.365 (FLAT) | 1.031 → 0.809 (**TURUN**) | 0.237 |

---

## 5. Positioning — apakah kejadian terjadi mendekati fase topping?

Diukur sebagai persentase jarak hari dari cycle-start (bottom) menuju tanggal puncak harga cycle tersebut:

| Cycle | Cycle start | Puncak cycle | Hari cycle-start → puncak | Posisi kejadian (% menuju puncak) |
|---|---|---|---|---|
| 2017 | 14-Jan-15 | 16-Dec-17 | 1,067 hari | 39%, 42%, 45%, 55%, 82%, 95% |
| 2021 | 12-Mar-20 | 08-Nov-21 | 606 hari | 43% (n=1, tidak cukup untuk pola) |
| 2023-2025 | 21-Nov-22 | 06-Oct-25 | 1,050 hari | 24%, 38%, 48%, 72%, 93% |

**Pengamatan:** Di 2017 maupun 2023-2025, tidak ada kejadian yang muncul di 20% pertama cycle (fase awal akumulasi/awal bull) — semua terjadi mulai pertengahan cycle (≥24%) sampai sangat dekat puncak (93-95%). Ini pola yang **konsisten antar dua cycle**, bukan spesifik ke cycle sekarang. 2023-2025 mulai sedikit lebih awal (24% vs 39% di 2017) tapi keduanya sama-sama tersebar dari pertengahan sampai injak puncak cycle, bukan random di seluruh cycle. 2021 cuma 1 titik (43%) — konsisten dengan rentang yang sama, tapi n=1 tidak bisa jadi bukti pola.

---

## 6. RollStd — test hipotesis volatility compression

| Cycle | RollStd rata-rata SAAT kejadian (n) | RollStd rata-rata SEMUA pasangan di cycle (baseline) | Kejadian vs baseline |
|---|---|---|---|
| 2017 | 0.325 (n=6, range 0.235–0.459) | 0.411 (n=84) | -21% (kejadian di volatility lebih rendah dari rata-rata cycle) |
| 2021 | 0.316 (n=1) | 0.472 (n=59) | -33% (n=1, tidak bisa disimpulkan) |
| 2023-2025 | 0.279 (n=5, range 0.237–0.401) | 0.281 (n=82) | -1% (kejadian ≈ rata-rata cycle, TIDAK lebih rendah dari baseline-nya sendiri) |

**Dua temuan terpisah yang penting dibedakan:**

1. **Antar cycle:** RollStd baseline 2023-2025 (0.281) memang jauh lebih rendah dari 2017 (0.411) dan 2021 (0.472) — market memang secara keseluruhan lebih tidak volatile di cycle sekarang. Ini konsisten dengan fenomena market maturation yang sudah established sebelumnya (diminishing MVRV peaks, dll).

2. **Dalam masing-masing cycle:** Di 2017, kejadian pola ini justru terjadi di titik-titik dengan RollStd **di bawah rata-rata cycle-nya sendiri** (-21%) — artinya pola ini historically SUDAH cenderung muncul saat volatility sedang relatif rendah, bukan fenomena baru. Sementara di 2023-2025, kejadian terjadi tepat di rata-rata cycle (-1%, tidak istimewa rendah). Jadi **kejadian di 2023-2025 bukan terjadi di titik yang "lebih compressed" dibanding rata-rata cycle-nya sendiri** — beda dengan yang diharapkan hipotesis.

---

## 7. Jawaban eksplisit atas hipotesis (item 5)

**Hipotesis "pola ini spesifik ke cycle sekarang karena volatility compression" TIDAK TERBUKTI.**

Alasan:
- **Frekuensi:** 2017 (7.1%) justru punya frekuensi relatif SEDIKIT LEBIH TINGGI dari 2023-2025 (6.1%), bukan lebih rendah — kalau hipotesis benar, cycle lama harusnya jarang menunjukkan pola ini.
- **Positioning:** Pola konsentrasi di pertengahan-sampai-akhir cycle (39-95% di 2017, 24-93% di 2023-2025) hampir identik bentuknya antar dua cycle — bukan sesuatu yang baru muncul di cycle sekarang.
- **RollStd relatif:** Walau benar bahwa cycle 2023-2025 secara keseluruhan lebih rendah volatilitasnya (market maturation, sudah established), kejadian pola ini di 2023-2025 terjadi PERSIS di rata-rata cycle-nya sendiri, bukan di titik yang secara khusus lebih rendah dari baseline. Sementara di 2017, kejadian pola ini malah terjadi di titik-titik yang SECARA RELATIF lebih rendah dari baseline cycle-nya. Jadi arah efeknya kalau ada malah terbalik dari yang diharapkan hipotesis.

**Kesimpulan:** Pola "MVRV flat, Z-score turun" berulang di titik-titik topping bukan fenomena baru yang muncul karena cycle sekarang lebih matang/compressed — pola ini **sudah ada di cycle 2017 dengan frekuensi dan positioning yang sebanding** (bahkan sedikit lebih sering secara relatif). Ini artinya pola tersebut kemungkinan besar cuma **mekanisme generik dari cara kerja rolling-window normalization** (RollMean mengejar level harga baru) yang terjadi setiap kali struktur harga membentuk plateau menjelang local top — berlaku lintas cycle, bukan spesifik ke kondisi pasar 2023-2025.

2021 tidak bisa dipakai untuk menguatkan atau melemahkan kesimpulan ini karena cuma 1 kejadian (n=1) — kemungkinan besar karena 2021 double-top strukturnya jauh lebih sederhana (cuma 2 local top besar, bukan rally bertahap dengan banyak plateau kecil seperti 2017/2023-2025), bukan berarti pola tidak berlaku di 2021.

---

## 8. Catatan

Tidak ada rekomendasi revisi Decision Framework di laporan ini — sesuai instruksi, itu dibahas terpisah setelah hasil ini dievaluasi oleh Claude.ai.
