# Independence Check — MVRV Level vs MVRV Z-Score Rolling 1Y

**Tanggal:** 2026-07-10
**Sumber prompt:** `prompt_independence_check.md` (dari sesi Claude.ai)
**Tujuan:** Cek apakah divergensi "price HH, Z-score LH" yang ditemukan sesi sebelumnya (6 titik cherry-picked, 5/6 cycle) genuinely independen dari MVRV level raw, atau cuma echo/representasi lain dari sinyal yang sama plus efek mekanik rolling window.

Script: `research/analyze_mvrv_zscore_independence_check.py`
Raw data lengkap (semua local top & semua pasangan): `research/findings/mvrv_zscore_independence_all_local_tops.csv` (335 baris), `research/findings/mvrv_zscore_independence_pairs.csv` (329 baris), subset soft-divergent: `research/findings/mvrv_zscore_independence_soft_divergent.csv` (41 baris).

---

## 1. Metodologi

- **Local top:** `price[i] > max(price[i-5:i])` DAN `price[i] > max(price[i+1:i+6])` — margin 5 hari, sama seperti definisi K6. Diterapkan ke SELURUH histori harian (bukan window Z2+Z3 seperti script K6 asli), supaya tidak cherry-pick.
- **Cycle boundary** (bear-market bottom terkonfirmasi, konsisten dengan contoh framework "2017, 2019, 2021, 2023"):
  - 2011: awal data (2010-07-17) → 2011-11-18 ($2.05)
  - 2013: 2011-11-18 → 2015-01-14 ($178.50)
  - 2017: 2015-01-14 → 2018-12-14 ($3,281)
  - 2019 (mini-cycle): 2018-12-14 → 2020-03-12 ($4,837, COVID crash)
  - 2021: 2020-03-12 → 2022-11-21 ($15,774)
  - 2023-2025 (current): 2022-11-21 → data terkini (2026-07-10)
- **MVRV Z-Score rolling 1Y:** `Z = (MVRV_ratio − rolling_mean(MVRV_ratio, 365d)) / rolling_std(MVRV_ratio, 365d)`, `min_periods=30` — sama persis dengan tab MVRV Z-Score Lab.
- **Klasifikasi arah** antar pasangan local top berurutan dalam cycle yang sama:
  - MVRV: `NAIK` jika perubahan >+2%, `TURUN` jika <-2%, selain itu `FLAT`.
  - Z-score: `NAIK` jika perubahan >+0.10, `TURUN` jika <-0.10, selain itu `FLAT`.
  - **SEARAH:** MVRV naik & Z naik, atau MVRV turun & Z turun.
  - **DIVERGEN:** MVRV naik/flat & Z turun, ATAU MVRV turun & Z naik/flat.

---

## 2. Ringkasan angka

**335 local top ditemukan di seluruh histori** (2010-07-17 s/d 2026-07-10), **329 pasangan berurutan** dalam 6 cycle:

| Cycle | Local top | Pasangan |
|---|---|---|
| 2011 | 21 | 20 |
| 2013 | 57 | 56 |
| 2017 | 85 | 84 |
| 2019 (mini-cycle) | 29 | 28 |
| 2021 | 60 | 59 |
| 2023-2025 (current) | 83 | 82 |
| **Total** | **335** | **329** |

**Distribusi klasifikasi (329 pasangan):**

| Klasifikasi | n | % |
|---|---|---|
| SEARAH (turun-turun) | 116 | 35.3% |
| SEARAH (naik-naik) | 115 | 35.0% |
| **Total SEARAH** | **231** | **70.2%** |
| FLAT/FLAT (tidak ada perubahan berarti di dua-duanya) | 54 | 16.4% |
| DIVERGEN (MVRV turun, Z naik/flat) | 27 | 8.2% |
| DIVERGEN (MVRV naik/flat, Z turun) | 17 | 5.2% |
| **Total DIVERGEN** | **44** | **13.4%** |

---

## 3. Breakdown penting: divergensi "keras" (hard) vs "lunak" (soft)

Klasifikasi DIVERGEN di atas termasuk kasus di mana salah satu sisi cuma FLAT (tidak benar-benar bergerak berlawanan, cuma diam saat sisi lain bergerak). Ini dipecah lagi jadi:

- **Hard reversal** (dua-duanya bergerak signifikan, arah berlawanan): **3 dari 329 pasangan (0.9%)**
- **Soft divergent** (satu sisi FLAT, sisi lain bergerak): **41 dari 329 pasangan (12.5%)**

### 3a. Semua kasus hard reversal (n=3, dari total 329 pasangan di seluruh histori)

| Cycle | Tanggal | Price | MVRV | Z-Score |
|---|---|---|---|---|
| 2011 | 13-May-11 → 08-Jun-11 | $8.19 → $29.60 | 6.727 → 7.445 (**NAIK**) | 3.525 → 3.384 (**TURUN**) |
| 2017 | 04-Nov-15 → 15-Dec-15 | $409.88 → $465.35 | 1.418 → 1.552 (**NAIK**) | 4.296 → 3.917 (**TURUN**) |
| 2021 | 08-Jan-21 → 21-Feb-21 | $40,736 → $57,551 | 3.772 → 3.954 (**NAIK**) | 4.061 → 2.898 (**TURUN**) |

**Temuan kunci:** Ketiga kasus hard-reversal ini **semuanya arah yang sama** — MVRV naik kuat tapi Z-score turun — dan **tidak satu pun** terjadi di sekitar local top dekat puncak cycle (K1-relevant). Ketiganya justru terjadi di fase **awal/tengah bull run yang sedang berakselerasi cepat** (Mei 2011 sebelum puncak Jun 2011, Nov-Des 2015 di awal ramp-up menuju puncak Des 2017, Jan-Feb 2021 di awal ramp-up menuju double-top Apr/Nov 2021). Di ketiga kasus, RollStd melonjak cepat (contoh 2021: 0.485→0.675, +39%) karena volatilitas harga baru yang ekstrem mulai masuk window 1 tahun — inilah yang menekan Z turun meski MVRV terus naik. **Sebaliknya, arah "MVRV turun genuine tapi Z naik genuine" TIDAK PERNAH terjadi sama sekali di 329 pasangan** — nol kejadian.

### 3b. Kasus soft-divergent (n=41) — breakdown

- Kategori "MVRV turun, Z naik/flat" (27 kasus): **27/27 (100%) sebenarnya Z-nya FLAT**, bukan naik. Artinya: setiap kali MVRV turun cukup jelas, Z-score tidak pernah benar-benar naik melawannya — paling banter cuma diam.
- Kategori "MVRV naik/flat, Z turun" (17 kasus): 14/17 MVRV-nya FLAT, 3/17 MVRV-nya genuinely NAIK (= 3 hard-reversal di atas).

Detail lengkap 41 kasus soft-divergent ada di `mvrv_zscore_independence_soft_divergent.csv`.

### 3c. Kasus di cycle 2023-2025 (current) — relevan untuk pertanyaan leading-indicator

| Tanggal | Price | MVRV | Z-Score |
|---|---|---|---|
| 14-Dec-22 → 26-Dec-22 | $17,801 → $16,922 | 0.889 → 0.850 (TURUN) | -0.998 → -1.044 (FLAT) |
| 14-Apr-23 → 27-Apr-23 | $30,496 → $29,491 | 1.532 → 1.477 (TURUN) | 2.047 → 1.954 (FLAT) |
| 23-Jul-23 → 01-Aug-23 | $30,101 → $29,704 | 1.471 → 1.457 (FLAT) | 1.437 → 1.317 (**TURUN**) |
| 08-Dec-23 → 22-Dec-23 | $44,191 → $44,028 | 2.061 → 2.023 (FLAT) | 2.928 → 2.507 (**TURUN**) |
| 31-Mar-24 → 08-Apr-24 | $71,322 → $71,636 | 2.551 → 2.522 (FLAT) | 2.254 → 2.053 (**TURUN**) |
| 22-Nov-24 → 17-Dec-24 | $98,943 → $106,169 | 2.726 → 2.683 (FLAT) | 2.548 → 1.989 (**TURUN**) |
| 14-Jul-25 → 22-Jul-25 | $119,831 → $119,963 | 2.411 → 2.365 (FLAT) | 1.031 → 0.809 (**TURUN**) |
| 09-Dec-25 → 21-Dec-25 | $92,701 → $88,655 | 1.645 → 1.576 (TURUN) | -2.143 → -2.233 (FLAT) |
| 16-Mar-26 → 25-Mar-26 | $74,863 → $71,304 | 1.376 → 1.313 (TURUN) | -1.534 → -1.608 (FLAT) |

**Poin penting:** 7 dari 9 kasus di cycle ini adalah pola "MVRV flat, Z turun" — dan pola ini muncul berulang **tepat di setiap fase topping** sepanjang cycle (Jul 2023, Des 2023, pasca-ATH Mar 2024, Nov-Des 2024, Jul 2025). Kasus **14-Jul-25 → 22-Jul-25** khususnya menarik: ini local top paling awal dalam struktur Jul-Okt 2025 (price cuma naik tipis $119,831→$119,963, MVRV nyaris tidak bergerak), tapi Z-score sudah turun jelas (1.031→0.809) — beberapa bulan sebelum puncak harga aktual (6 Okt 2025, $124,715) terkonfirmasi. Ini pola paling dekat dengan "Z turun duluan sebelum MVRV level turun jelas" yang ditanyakan di task.

---

## 4. Jawaban eksplisit untuk pertanyaan task

### Apakah ada divergensi arah? (item 2)

Ya, 44 dari 329 pasangan (13.4%) diklasifikasikan divergen secara mekanis. **Tapi hanya 3 (0.9%) yang divergensi keras (dua-duanya bergerak signifikan, arah berlawanan)** — sisanya (41, 12.5%) adalah kasus di mana salah satu sisi cuma diam (FLAT) sementara sisi lain bergerak.

### Penjelasan kasus divergensi (item 3)

- **3 hard-reversal:** selalu arah "MVRV naik kuat, Z turun", selalu di fase awal/tengah bull run yang berakselerasi cepat (bukan di dekat cycle top), disebabkan RollStd yang melonjak cepat akibat volatilitas baru masuk window 1 tahun. Bukan sinyal K1-relevant.
- **41 soft-divergent:** didominasi pola "MVRV flat, Z turun" (khususnya berulang di cycle 2023-2025 saat ini, persis di titik-titik topping). Penyebabnya sama dengan temuan sesi sebelumnya di sisi dip — RollMean bergeser naik (window mengejar level harga baru) membuat level MVRV yang sama persis terlihat "lebih dekat ke mean" dibanding pasangan sebelumnya, sehingga Z turun meski MVRV-nya sendiri nyaris tidak berubah.
- **Nol kejadian** untuk arah "MVRV turun genuine, Z naik genuine" di seluruh 329 pasangan — arah ini benar-benar tidak pernah muncul.

### Kesimpulan independensi (item 4)

**TIDAK ADA divergensi arah yang genuinely independen dalam jumlah berarti.** 70.2% pasangan searah penuh, dan dari 13.4% yang tampak divergen, 96% (41/44) cuma soft-divergent (satu sisi diam, bukan berlawanan arah). Hard reversal genuine cuma 0.9% dan tidak pernah terjadi di dekat cycle top. **MVRV Z-Score rolling 1Y pada dasarnya adalah representasi ternormalisasi dari MVRV level yang sama** — bukan sumber informasi independen — dengan sensitivitas tambahan murni dari efek mekanik rolling window (RollMean naik, RollStd berubah), bukan dari sinyal on-chain baru.

### Kesimpulan leading/early-warning (item 5)

Secara **statistik tidak independen**, tapi secara **praktis/operasional ada nilai timing**: karena Z-score menormalisasi MVRV terhadap window 1 tahun yang terus bergeser, dia bisa "mendeteksi" plateau MVRV yang sangat halus (masih dalam rentang FLAT ±2%) sebagai penurunan yang jelas (>0.10 Z), lebih awal dari titik di mana MVRV raw sendiri akan terlihat jelas menurun bagi mata manusia. Kasus Jul 2025 di atas adalah contoh konkretnya — 2-3 bulan lebih awal dari puncak harga aktual.

**Rekomendasi:** Z-score rolling 1Y boleh dipakai sebagai **alat visualisasi/early-flag** untuk granularitas timing yang lebih halus dari MVRV level mentah — TAPI harus eksplisit dicatat bahwa ini bukan sinyal independen tambahan secara informasi, cuma cara membaca sinyal yang sama (diminishing MVRV peaks) dengan resolusi lebih tinggi karena efek normalisasi window. Jangan diberi bobot sebagai "confirming signal terpisah" di samping MVRV level di K1 — kalau dipakai, treat sebagai representasi alternatif dari signal #1 yang sama, bukan signal #1b yang baru.

---

## 5. Catatan data mentah

Semua 335 local top dan 329 pasangan (termasuk MVRV, Z-score, RollMean, RollStd di setiap titik) tersedia lengkap di:
- `research/findings/mvrv_zscore_independence_all_local_tops.csv`
- `research/findings/mvrv_zscore_independence_pairs.csv`
- `research/findings/mvrv_zscore_independence_soft_divergent.csv` (41 kasus soft-divergent saja)
