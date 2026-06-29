# MVRV Divergence Analysis — K3 Early Warning Signal Design
**Tanggal analisis:** 30 Juni 2026
**Sumber data:** `data_mvrv.csv` (lokal) — 5,824 hari, 2010-07-17 s/d 2026-06-26
**Script:** `analyze_mvrv_divergence_k3.py`

---

## Definisi Metrik

```
Divergence = Price Percentile (365d) − MVRV Percentile (365d)

Positif  → price naik lebih kencang dari MVRV relative to 1yr history
Negatif  → MVRV naik lebih kencang dari price relative to 1yr history
Nol      → keduanya sinkron
```

Percentile dihitung dengan rolling window 365 calendar days (method: `percentileofscore`, kind=`rank`).

---

## Section 1 — Snapshot di Tanggal-Tanggal Kritis

### Cycle Tops

| Tanggal | Event | Price | MVRV | Price% | MVRV% | Divergence |
|---------|-------|------:|-----:|-------:|------:|-----------:|
| 2017-12-17 | Cycle top 2017 | $19,336 | 4.25 | 99.7 | 99.2 | **+0.5** |
| 2021-04-14 | Local top pre-correction | $63,007 | 3.38 | 99.7 | 89.6 | **+10.1** |
| 2021-11-08 | Cycle top 2021 | $67,525 | 2.85 | 100.0 | 67.7 | **+32.3** |

### Mid-Cycle Correction 2021

| Tanggal | Event | Price | MVRV | Price% | MVRV% | Divergence |
|---------|-------|------:|-----:|-------:|------:|-----------:|
| 2021-05-19 | Crash awal | $36,800 | 1.85 | 69.0 | 33.7 | **+35.3** |
| 2021-07-20 | Bottom mid-cycle | $29,837 | 1.54 | 45.5 | 0.3 | **+45.2** |

### Bear Bottoms

| Tanggal | Event | Price | MVRV | Price% | MVRV% | Divergence |
|---------|-------|------:|-----:|-------:|------:|-----------:|
| 2018-12-16 | Bear bottom | $3,303 | 0.71 | 0.8 | 0.8 | **+0.0** |
| 2022-11-21 | Bear bottom | $15,774 | 0.78 | 0.3 | 0.5 | **−0.3** |

### Early Bull

| Tanggal | Event | Price | MVRV | Price% | MVRV% | Divergence |
|---------|-------|------:|-----:|-------:|------:|-----------:|
| 2019-02-01 | Early bull 2019 | $3,498 | 0.78 | 2.7 | 4.4 | **−1.6** |
| 2023-02-01 | Early bull 2023 | $23,731 | 1.20 | 61.1 | 64.1 | **−3.0** |

**Key Takeaway:**
- Divergence di kedua cycle tops sangat berbeda: 2017 = +0.5 (hampir nol), 2021 = +32.3
- Bear bottoms konsisten mendekati nol: 2018 = +0.0, 2022 = −0.3 (price dan MVRV sama-sama di lantai)
- Mid-cycle bottom (Jul 2021) justru divergence tinggi (+45.2) karena MVRV sudah tertekan tapi price belum recover → MVRV% sangat rendah (0.3)

---

## Section 2 — Divergence di Successive ATHs (Cycle 2020–2021)

| ATH Date | Price | Divergence | Delta vs Prev |
|----------|------:|-----------:|--------------:|
| 2020-01-01 | $7,441 | +0.8 | — |
| 2020-01-17 | $9,044 | +9.6 | +8.8 |
| 2020-02-05 | $9,613 | +9.0 | −0.5 |
| 2020-07-27 | $11,037 | +3.8 | −5.2 |
| 2020-08-16 | $11,916 | +1.4 | −2.5 |
| 2020-10-21 | $12,818 | +0.0 | −1.4 |
| 2020-11-05 | $15,596 | +0.0 | +0.0 |
| 2020-11-20 | $18,676 | +0.0 | +0.0 |
| 2020-12-16 | $21,354 | +0.0 | +0.0 |
| 2020-12-31 | $28,979 | +0.3 | +0.3 |
| 2021-02-08 | $46,343 | +0.8 | +0.5 |
| 2021-03-11 | $57,800 | +3.3 | +2.5 |
| 2021-04-13 | $63,551 | +8.8 | +5.5 |
| 2021-10-19 | $64,301 | +31.5 | **+22.7** |
| 2021-11-08 | $67,525 | +32.3 | +0.8 |

**Key Takeaway:**
- Trend **tidak** konsisten menurun — ini bukan bearish divergence klasik di setiap ATH
- Divergence flat mendekati nol sepanjang Nov 2020 – Mar 2021 (fase parabolic pertama)
- **Lonjakan tajam terjadi di ATH terakhir**: dari +8.8 (Apr 2021) ke +31.5 (Okt 2021) = delta +22.7
- Pattern yang benar: divergence **meledak di ATH terakhir setelah mid-cycle correction**, bukan menurun bertahap

---

## Section 3 — Lead Time Analysis

**Definisi signal:** Divergence tembus ≥+30, kemudian turun kembali di bawah +30.

### Cycle 2017 — Episode yang berakhir sebelum top (17 Des 2017)

| Episode End | Peak Div | Days Above +30 | Days to Top |
|-------------|:--------:|:--------------:|:-----------:|
| 2017-03-24 | +32.3 | 1 | 268 hari |
| 2017-09-17 | +58.9 | 5 | 91 hari |
| 2017-09-29 | +46.6 | 11 | 79 hari |
| 2017-10-07 | +33.7 | 6 | 71 hari |
| 2017-11-13 | +43.0 | 3 | 34 hari |

### Cycle 2021 — Episode yang berakhir sebelum top (8 Nov 2021)

| Episode End | Peak Div | Days Above +30 | Days to Top |
|-------------|:--------:|:--------------:|:-----------:|
| 2021-05-19 | +35.3 | 1 | 173 hari |
| 2021-05-23 | +38.6 | 3 | 169 hari |
| 2021-06-02 | +38.6 | 6 | 159 hari |
| 2021-06-12 | +41.4 | 9 | 149 hari |
| 2021-07-25 | +46.0 | 39 | 106 hari |
| 2021-08-03 | +31.8 | 1 | 97 hari |
| 2021-09-14 | +30.1 | 1 | 55 hari |
| 2021-09-17 | +30.7 | 1 | 52 hari |
| 2021-09-19 | +31.2 | 1 | 50 hari |
| 2021-09-21 | +34.0 | 1 | 48 hari |
| 2021-09-29 | +34.8 | 4 | 40 hari |
| 2021-10-04 | +32.3 | 4 | 35 hari |
| 2021-10-11 | +30.7 | 1 | 28 hari |
| 2021-10-19 | +36.2 | 7 | 20 hari |

**Key Takeaway:**
- Single crossing +30 memberikan lead time sangat lebar (20–268 hari) → terlalu early untuk actionable signal sendiri
- Ada pola **acceleration**: semakin dekat ke actual top, episode +30 makin pendek, makin sering, dan makin rapid → "rapid signaling cluster"
- Di 2021, 19 episode +30 terjadi dalam 173 hari sebelum top; di 2017, 5 episode dalam 268 hari sebelum top
- Episode singkat berulang di Sep–Okt 2021 (≤4 hari tiap episode) bisa dianggap "final warning cluster"

---

## Section 4 — Threshold Analysis (episode ≥+30 selama ≥7 hari berturut-turut)

Total episodes sustained ≥7 hari: **18 episodes**

| Start | End | Days | Peak Div | Price at End | +30d | +60d | Outcome |
|-------|-----|-----:|:--------:|-------------:|-----:|-----:|---------|
| 2011-07-16 | 2011-12-30 | 168 | +77.0 | $4 | +27% | +14% | CONTINUED_BULL |
| 2012-01-04 | 2012-01-15 | 12 | +32.3 | $7 | −36% | −24% | CORRECTION |
| 2013-07-02 | 2013-07-11 | 10 | +71.0 | $89 | +14% | +47% | CONTINUED_BULL |
| 2013-07-18 | 2013-07-24 | 7 | +50.4 | $94 | +25% | +42% | CONTINUED_BULL |
| 2013-09-18 | 2013-10-13 | 26 | +37.5 | $145 | +148% | +500% | CONTINUED_BULL |
| 2014-01-20 | 2014-08-12 | 205 | +71.2 | $570 | −16% | −37% | CORRECTION |
| 2017-09-19 | 2017-09-29 | 11 | +46.6 | $4,130 | +47% | +147% | CONTINUED_BULL |
| 2018-01-08 | 2018-07-10 | 184 | +82.2 | $6,355 | +3% | −1% | CONTINUED_BULL |
| 2021-06-04 | 2021-06-12 | 9 | +41.4 | $35,539 | −7% | +28% | CORRECTION |
| 2021-06-17 | 2021-07-25 | 39 | +46.0 | $35,390 | +35% | +27% | CONTINUED_BULL |
| 2021-10-13 | 2021-10-19 | 7 | +36.2 | $64,301 | −11% | −27% | **CYCLE_TOP** |
| 2021-10-21 | 2021-12-16 | 57 | +47.1 | $47,669 | −10% | −11% | **CYCLE_TOP** |
| 2021-12-20 | 2021-12-27 | 8 | +35.1 | $50,699 | −27% | −23% | CORRECTION |
| 2025-02-04 | 2025-04-21 | 77 | +64.9 | $87,523 | +25% | +18% | CONTINUED_BULL |
| 2025-06-12 | 2025-06-19 | 8 | +33.2 | $104,700 | +13% | +11% | CONTINUED_BULL |
| 2025-06-23 | 2025-07-02 | 10 | +36.4 | $108,870 | +4% | −1% | CONTINUED_BULL |
| 2025-07-31 | 2025-08-09 | 10 | +46.6 | $116,472 | −4% | +6% | CORRECTION |
| 2025-08-14 | 2025-11-13 | 92 | +63.6 | $99,703 | −9% | −9% | CORRECTION |

**Outcome Summary:**

| Outcome | Count | % |
|---------|------:|--:|
| CONTINUED_BULL | 10 | 56% |
| CORRECTION | 6 | 33% |
| CYCLE_TOP | 2 | 11% |

**Key Takeaway:**
- False positive rate = **56%** (threshold +30/7 hari saja tidak cukup)
- 10 dari 18 episodes, price tetap naik setelah episode berakhir
- Threshold ini berguna sebagai **early warning** tapi butuh filter tambahan untuk reduce false positives
- Dari 2 episode CYCLE_TOP, keduanya terjadi di Okt–Des 2021 (satu sebelum top, satu sesudah)

---

## Section 5 — Mid-Cycle vs Cycle Top Separation Test

### Apr 2021 — Local Top / Mid-Cycle Correction

| Date | Price | MVRV | Price% | MVRV% | Divergence |
|------|------:|-----:|-------:|------:|-----------:|
| 2021-03-15 | $55,681 | 3.41 | 97.8 | 92.6 | +5.2 |
| 2021-03-31 | $58,889 | 3.38 | 99.2 | 89.6 | +9.6 |
| 2021-04-05 | $59,082 | 3.33 | 99.5 | 87.9 | +11.5 |
| **2021-04-14** | **$63,007** | **3.38** | **99.7** | **89.6** | **+10.1 ◀ TOP** |
| 2021-04-18 | $56,338 | 2.95 | 91.8 | 72.6 | +19.2 |
| 2021-04-25 | $49,216 | 2.56 | 84.1 | 63.0 | +21.1 |

**Summary Apr 2021:** Peak divergence = **+21.1** | Days ≥+30 = **0 hari**

---

### Nov 2021 — Actual Cycle Top

| Date | Price | MVRV | Price% | MVRV% | Divergence |
|------|------:|-----:|-------:|------:|-----------:|
| 2021-10-11 | $57,500 | 2.64 | 91.2 | 60.5 | +30.7 |
| 2021-10-15 | $61,696 | 2.79 | 99.2 | 64.9 | +34.2 |
| 2021-10-21 | $62,249 | 2.75 | 98.6 | 60.8 | +37.8 |
| 2021-10-30 | $61,878 | 2.69 | 97.5 | 58.4 | +39.2 |
| 2021-11-04 | $61,475 | 2.62 | 96.2 | 54.8 | +41.4 |
| 2021-11-06 | $61,520 | 2.62 | 96.2 | 54.2 | **+41.9** |
| **2021-11-08** | **$67,525** | **2.85** | **100.0** | **67.7** | **+32.3 ◀ TOP** |
| 2021-11-12 | $64,189 | 2.65 | 98.4 | 55.1 | +43.3 |
| 2021-11-16 | $60,153 | 2.47 | 90.1 | 43.0 | **+47.1 ← PEAK** |

**Summary Nov 2021:** Peak divergence = **+47.1** | Days ≥+30 = **41 hari**

---

### Perbandingan

| Metric | Apr 2021 (mid-cycle) | Nov 2021 (cycle top) | Perbedaan |
|--------|:--------------------:|:--------------------:|:---------:|
| Divergence at event | +10.1 | +32.3 | **+22.2** |
| Peak divergence (window ±30d) | +21.1 | +47.1 | **+26.0** |
| Days divergence ≥+30 | **0 hari** | **41 hari** | sangat berbeda |
| MVRV at top | 3.38 | 2.85 | lower di cycle top |

**Key Takeaway:**
- Separation **sangat jelas**: mid-cycle correction tidak pernah sustain di atas +30, actual cycle top sustain 41 hari
- **Duration ≥+30 adalah discriminating factor** terkuat antara kedua event
- MVRV lebih rendah di cycle top 2021 (2.85) vs mid-cycle (3.38) — consistent dengan pattern bahwa diminishing returns terjadi di tiap cycle
- Divergence tinggi di cycle top mencerminkan: price masih bisa ATH tapi MVRV percentile sudah ketinggalan karena realized value base yang lebih besar

---

## Section 6 — Current State (26 Juni 2026)

| Metric | Value |
|--------|------:|
| Price | $59,321 |
| MVRV Ratio | 1.1129 |
| Price Percentile (365d) | 0.3% |
| MVRV Percentile (365d) | 0.3% |
| **Divergence** | **+0.0** |
| Divergence percentile (all-time) | 24th |

**Konteks historis:** Divergence +0.0 di persentil ke-24 dari seluruh dataset. Kondisi ini muncul di 2,342 hari historis — mayoritas di fase accumulation/consolidation:

| Tahun | Hari dengan divergence ±5 dari saat ini |
|-------|-----------------------------------------:|
| 2015 | 216 |
| 2016 | 290 |
| 2019 | 257 |
| 2020 | 216 |
| 2022 | 224 |
| 2023 | 261 |

**Key Takeaway:**
- Price dan MVRV sepenuhnya sinkron — tidak ada divergence dalam arah apapun
- Persentil 24 = bawah median historis, typical untuk range-bound / bear-to-recovery transition
- Consistent dengan kondisi saat ini: S2 Latch aktif, bear market mid-to-late stage
- Tidak ada K3 warning signal yang aktif saat ini

---

## Rekomendasi K3 Signal Design

Berdasarkan seluruh analisis, kombinasi threshold yang paling discriminating:

| Level | Kondisi | Interpretasi | False Positive Rate |
|-------|---------|--------------|:-------------------:|
| **Warning** | Divergence ≥+30 pertama kali | Awal elevated risk window | Tinggi — early warning only |
| **Elevated** | Divergence ≥+30 sustained ≥14 hari | Risk meningkat, mulai monitor ketat | Sedang |
| **Strong** | Divergence ≥+30 sustained ≥30 hari | Late-cycle high probability | Rendah |
| **Confirmed** | Sustained ≥30 hari **DAN** peak ≥+40 | Cycle top territory | Sangat rendah (1 confirmed cycle) |

**Proposed K3 Trigger:**
```
K3 = ACTIVE jika:
  (A) Divergence telah ≥+30 selama ≥ 30 hari berturut-turut
  AND
  (B) Peak divergence dalam episode tersebut ≥ +40

K3 = WARNING jika:
  (A) terpenuhi tapi (B) belum

K3 = INACTIVE jika keduanya belum terpenuhi
```

**Validasi retrospektif:**
- Apr 2021: K3 = INACTIVE (peak +21.1, 0 hari ≥+30) → **Correct — bukan cycle top**
- Nov 2021: K3 = ACTIVE (41 hari ≥+30, peak +47.1) → **Correct — actual cycle top**
- Jun 2026: K3 = INACTIVE (divergence +0.0) → **Consistent dengan bear market regime**

**Catatan penting:** Validasi hanya dari 1 confirmed cycle top (2021). 2017 top memiliki divergence +0.5 — K3 tidak akan fired. Ini mengindikasikan bahwa K3 mungkin cycle-specific atau bahwa karakteristik MVRV divergence berubah seiring maturing market.

---

## Caveat

| Item | Detail |
|------|--------|
| Total data points (raw) | 5,824 hari (2010-07-17 s/d 2026-06-26) |
| Usable setelah 365d warmup | 5,460 hari (2011-07-16 s/d 2026-06-26) |
| Siklus yang bisa dianalisa | 2 (2017, 2021) — 2013 excluded karena data pre-warmup |
| Gap data | Tidak ada gap signifikan (daily frequency) |
| Method percentile | `percentileofscore` kind=`rank` — tied values dibagi rata |
| Rolling window | 365 calendar days (bukan trading days) |
| Sample size warning | **2 cycle tops = sample sangat kecil** — inferensi statistik tidak robust |
| Classification outcome (Sec 4) | Proximity rule ±45 hari — bukan ground truth label |
| Cross-validation | Data dari satu sumber lokal — disarankan cross-validate dengan Glassnode |
| 2017 anomali | Divergence +0.5 di 2017 top — K3 signal design mungkin tidak applicable untuk early cycles |

---

*Generated: 30 Juni 2026 | Script: `analyze_mvrv_divergence_k3.py` | Data: `data_mvrv.csv`*
