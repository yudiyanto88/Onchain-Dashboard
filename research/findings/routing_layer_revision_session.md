# Routing Layer Revision — Research Session
**Tanggal:** Juni 2026  
**Konteks:** Signal Framework v1.0.3 — revisi Layer 1 routing dari zone-based (Supply%) ke price-level-based  
**Data:** 2016–2026, ~3830 hari, sumber ChartInspect / Glassnode

---

## Latar Belakang

Framework saat ini (v1.0.3) menggunakan dua variabel routing:
1. Price vs STH Realized Price (above/below)
2. Total Supply in Profit (%)

Revisi yang diusulkan: ganti routing ke **price relative to key price levels** yang lebih intuitif dan bisa di-visualisasi langsung di chart:
- CVDD (Coindays Destroyed Value)
- LTH RP = LTH Realized Price (`lth_cost_basis`)
- RP = Aggregate Realized Price (`realized_price`)
- STH RP = STH Realized Price (`sth_cost_basis`)
- AVIV Mean = harga BTC saat AVIV ratio = mean
- AVIV Upper = harga BTC saat AVIV ratio = +0.5 SD

---

## Usulan Awal Routing (bottom to top)

User mengusulkan zona dari bawah ke atas:

1. **Price < STH RP dan LTH RP** → Bear Capitulation / Bear Bottom Near  
2. **Price menembus STH RP dari bawah, masih di bawah LTH RP** → Pre-Detection / transisi  
   *(user awalnya tidak yakin: apakah pakai LTH RP atau RP sebagai batas atas?)*  
3. **Price > STH RP dan LTH RP, tapi masih < AVIV Mean** → Upper Range Discovery (early bull)  
4. **Price cross up AVIV Mean** → Mid Bull  
   *(user menduga STH RP akan menyusul naik di atas AVIV Mean)*  
5. Dan seterusnya (belum defined)

**CVDD:** User menyebut sebagai titik bottom yang "sudah perfect" — tidak perlu diperdebatkan.

---

## Analisis yang Dilakukan

### A. Matrix urutan antar level (berapa % hari A < B)

Dataset 2015–2026, 4190 hari dengan data AVIV lengkap.

| | CVDD | LTH RP | RP | STH RP | AVIV Mean | AVIV Upper |
|---|---|---|---|---|---|---|
| **CVDD** | — | 60.8% | 100% | 100% | 100% | 100% |
| **LTH RP** | 39.2% | — | 88.3% | 88.3% | 100% | 100% |
| **RP** | 0% | 11.7% | — | 88.3% | 100% | 100% |
| **STH RP** | 0% | 11.7% | 11.7% | — | 52.8% | 84.1% |
| **AVIV Mean** | 0% | 0% | 0% | 47.2% | — | 100% |
| **AVIV Upper** | 0% | 0% | 0% | 15.9% | 0% | — |

**Urutan permanen (selalu berlaku):**
```
CVDD < RP  (100%)
CVDD < STH RP  (100%)
RP < AVIV Mean  (100%)
AVIV Mean < AVIV Upper  (100%)
LTH RP < AVIV Mean  (100%)
```

**Yang tidak permanen:**
- CVDD vs LTH RP: bertukar 39% hari — CVDD bisa di atas LTH RP
- STH RP vs AVIV Mean: hampir 50/50 (STH RP < AVIV Mean hanya 52.8% hari)

---

### B. Temuan Kritis: LTH RP ≈ RP di Recovery

STH RP < LTH RP hanya terjadi **11.7% dari seluruh hari**, dan selalu bersamaan dengan STH RP < RP (0% overlap antara "STH < LTH" dan "LTH < STH < RP").

Di setiap recovery crossover historis, ketiga level berkonvergensi sangat dekat:

| Tanggal | STH RP | RP | LTH RP | Spread max |
|---------|--------|-----|---------|-----------|
| 2019-05-07 | $4,451 | $4,429 | $4,420 | 0.7% |
| 2023-03-01 | $19,888 | $19,880 | $19,878 | 0.05% |

**Implikasi:** "STH RP cross up LTH RP" dan "STH RP cross up RP" adalah kejadian yang **identik** — selalu terjadi hari yang sama (0 hari gap). Tidak perlu memilih.

---

### C. Urutan Crossover di Bear Recovery

Di deep bear, STH RP **lebih rendah** dari LTH RP (new buyers accumulate di harga rendah):

| Cycle | Sequence | Gap |
|-------|----------|-----|
| 2019 | Price cross STH RP (Mar 28) → Price cross LTH RP (Apr 2) | 5 hari |
| 2022-23 | Price cross STH RP (Nov 4, 2022) → Price cross LTH RP (Jan 14, 2023) | ~70 hari |

Zona "Price antara STH RP dan LTH RP" adalah nyata tapi sangat singkat (3–70 hari).

---

### D. AVIV Mean — STH RP Tidak Selalu Menyusul

Asumsi user "STH RP akan selalu menyusul naik di atas AVIV Mean" tidak terbukti di data.

- Price cross AVIV Mean dari bawah: terjadi **19x** sejak 2015
- STH RP cross AVIV Mean: hanya **3x** dalam seluruh sejarah (2016, 2020, 2024)

Pattern yang lebih reliabel — **posisi STH RP relatif ke AVIV Mean saat Price cross AVIV Mean**:

| Kondisi saat Price cross AVIV Mean | Artinya | Contoh |
|------------------------------------|---------|--------|
| Price > STH RP (STH < AVIV) | Early bull, buyers relatif murah | 2019, 2020-09, 2023-11 |
| Price < STH RP (STH > AVIV) + bull context | Mid-late bull, recent buyers mahal | 2024-07, 2025-04 |
| Price < STH RP (STH > AVIV) + bear context | Bear bounce / false signal | 2021-05, 2022-02 |

---

## Routing Accuracy Test

### Setup

Setiap hari 2016–2026 diberi label zona berdasarkan posisi harga:

| Zona | Definisi |
|------|---------|
| Z0_BELOW_CVDD | Price < CVDD |
| Z1_BELOW_LTH_RP | Price < LTH RP |
| Z2_BELOW_RP | LTH RP ≤ Price < RP |
| Z3_BELOW_STH_RP | RP ≤ Price < STH RP |
| Z4_BELOW_AVIV_MEAN | STH RP ≤ Price < AVIV Mean |
| Z5_BELOW_AVIV_UPPER | AVIV Mean ≤ Price < AVIV Upper |
| Z6_ABOVE_AVIV_UPPER | Price ≥ AVIV Upper |

Ground truth events dari `data_price_level_events.csv` — 405 hari dengan label:  
Bear Bottom, Pre Detection, Start of Bull, Bull Dip, Cycle Peak, Lower High, Upper Range, MCC

### Distribusi Zona (3830 hari, 2016–2026)

| Zona | Hari | % |
|------|------|---|
| Z0_BELOW_CVDD | 2 | 0.1% |
| Z1_BELOW_LTH_RP | 273 | 7.1% |
| Z2_BELOW_RP | 47 | 1.2% |
| Z3_BELOW_STH_RP | 1234 | 32.2% |
| Z4_BELOW_AVIV_MEAN | 592 | 15.5% |
| Z5_BELOW_AVIV_UPPER | 469 | 12.2% |
| Z6_ABOVE_AVIV_UPPER | 1213 | 31.7% |

### Hasil Accuracy

| Regime | Correct | Total | Accuracy |
|--------|---------|-------|----------|
| BEAR_BOTTOM | 23 | 23 | **100%** |
| **PRE_DETECT** | **0** | **10** | **0%** ← masalah utama |
| START_BULL | 4 | 4 | **100%** |
| BULL_DIP | 143 | 174 | **82%** |
| CYCLE_PEAK | 118 | 118 | **100%** |
| LOWER_HIGH | 13 | 14 | 93% |
| UPPER_RANGE | 28 | 29 | 97% |
| MCC | 30 | 31 | 97% |

### Insight dari Mismatches

**PRE_DETECT — 0% accuracy:**  
Semua 10 hari "Pre Detection 2019" jatuh di **Z1_BELOW_LTH_RP** (bukan Z2/Z3).

```
2019-02-22  Pre Detection 2019 Ref  Price=$3,943  LTH RP=$4,498  → Price < LTH RP
2019-03-21  Pre Detection 2019      Price=$4,039  LTH RP=$4,507  → Price < LTH RP
```

**Kesimpulan:** Pre-detection terjadi SAAT price masih di bawah LTH RP. Zone Z1 berisi dua kondisi berbeda yang tidak bisa dibedakan dari price level saja: deep bear bottom dan pre-detection approaching. Sub-classifier yang tepat untuk membedakan keduanya adalah trajectory on-chain indicators (MVRV, SOPR) — bukan price level tambahan.

**BULL_DIP — 18% salah (31 hari di Z6):**  
Bull Dip March 2017 terjadi di atas AVIV Upper. Di 2017, baseline AVIV sangat rendah, sehingga bull dip terjadi di Z6. Implikasi: BD1 signal seharusnya applicable di Z6 juga.

### Distribusi Zona per Tahun

| Tahun | Z1 | Z2 | Z3 | Z4 | Z5 | Z6 | Regime Dominan |
|-------|-----|-----|------|-----|-----|-----|----------------|
| 2016 | 0 | 0 | 13 | 133 | 126 | 94 | Early recovery |
| 2017 | 0 | 0 | 8 | 0 | 4 | 353 | Bull run |
| 2018 | 40 | 3 | 282 | 7 | 6 | 27 | Bear market |
| 2019 | 91 | 0 | 99 | 48 | 93 | 34 | Recovery cycle |
| 2020 | 1 | 6 | 66 | 157 | 71 | 65 | COVID + bull |
| 2021 | 0 | 0 | 118 | 0 | 18 | 229 | Bull + MCC |
| 2022 | 128 | 38 | 190 | 1 | 6 | 0 | Bear market |
| 2023 | 13 | 0 | 68 | 233 | 49 | 2 | Recovery |
| 2024 | 0 | 0 | 84 | 1 | 96 | 185 | Strong bull |
| 2025 | 0 | 0 | 141 | 0 | 0 | 224 | Bull peak → bear |
| 2026 | 0 | 0 | 165 | 12 | 0 | 0 | Bear/recovery |

**Z3 (Below STH RP) adalah zona paling heterogen** — muncul dominan di bear market (2018, 2022), di recovery (2019, 2023), DAN di bull transition (2021, 2025). Ini zona yang butuh internal sub-classifier via on-chain indicators.

---

## False Signal Analysis — 3 Kandidat Transition Signal

**Tujuan:** Menentukan signal terbaik untuk routing "kapan bear berakhir / bull dimulai"

**Tiga kandidat:**
- **Signal A:** `Price > RP` (price melintasi aggregate realized price dari bawah)
- **Signal B:** `STH RP > RP` (STH cost basis naik di atas RP)
- **Signal C:** `STH/LTH ratio > 1.0` (STH RP / LTH RP melewati 1.0 ke atas)

**Definisi outcome:**
- GENUINE_BULL: Price bertahan di atas STH RP selama ≥90 hari setelah signal
- PARTIAL: 30–89 hari
- FALSE_SIGNAL: Price jatuh kembali di bawah STH RP dalam <30 hari

### Signal A: Price > RP (7 events)

| Tanggal | Price | STH/LTH | Days Above STH RP | MaxGain | Outcome |
|---------|-------|---------|------------------|---------|---------|
| 2016-01-01 | $434 | 1.280 | 14 hari | +23% | **FALSE** |
| **2019-04-02** | **$4,896** | **0.905** | **151 hari** | **+162%** | **GENUINE** |
| 2020-03-19 | $6,386 | 1.627 | 0 hari | +87% | **FALSE** |
| 2022-07-18 | $22,497 | 1.435 | 0 hari | +9% | **FALSE** |
| 2022-09-10 | $21,656 | 1.163 | 0 hari | +10% | **FALSE** |
| 2022-11-05 | $21,300 | 0.991 | 1 hari | +34% | **FALSE** |
| **2023-01-13** | **$19,929** | **0.889** | **143 hari** | **+53%** | **GENUINE** |

**Hasil: 2/7 genuine (29%) — 5/7 false (71%)**

### Signal B: STH RP > RP (3 events)

| Tanggal | Price | STH/LTH | Days Above STH RP | MaxGain | Outcome |
|---------|-------|---------|------------------|---------|---------|
| 2016-01-01 | $434 | 1.280 | 14 hari | +23% | **FALSE** |
| **2019-05-07** | **$5,778** | **1.007** | **140 hari** | **+122%** | **GENUINE** |
| **2023-03-01** | **$23,649** | **1.001** | **96 hari** | **+33%** | **GENUINE** |

**Hasil: 2/3 genuine (67%) — 1/3 false (33%)**

### Signal C: STH/LTH ratio > 1.0 (3 events)

Identik dengan Signal B — fire di hari yang sama persis untuk semua 3 events.

**Hasil: 2/3 genuine (67%) — 1/3 false (33%)**

### Perbandingan Ringkas

| Signal | Events | Genuine | False | Lead vs B/C |
|--------|--------|---------|-------|-------------|
| A: Price > RP | 7 | 29% | **71%** | 35 hari lebih awal (2019) |
| B: STH RP > RP | 3 | **67%** | 33% | baseline |
| C: STH/LTH > 1.0 | 3 | **67%** | 33% | identik dengan B |

### Lead Time Analysis

| Cycle | Signal A | Signal B/C | Gap |
|-------|----------|-----------|-----|
| 2016 | Jan 1 | Jan 1 | 0 hari |
| 2019 | **Apr 2** | May 7 | A lebih awal **35 hari** |
| 2020 | Mar 19 | *(tidak fire — filtered)* | A false signal, B/C skip |
| 2022 Jul | Jul 18 | *(tidak fire)* | A false signal, B/C skip |
| 2022 Sep | Sep 10 | *(tidak fire)* | A false signal, B/C skip |
| 2022 Nov | Nov 5 | *(tidak fire)* | A false signal, B/C skip |
| 2023 Jan | Jan 13 | Mar 1 | A lebih awal **47 hari** |

**Signal A lebih awal masuk 35–47 hari tapi membawa 3 false entries di 2022 yang tidak perlu.**

---

## Hidden Filter di Signal A

Dua genuine bull dari Signal A keduanya punya **STH/LTH ratio < 1.0** saat signal fire (0.905 dan 0.889). Semua 5 false signals punya STH/LTH > 0.99 saat fire.

Jika ditambah filter: `Price > RP AND STH/LTH ratio < 1.0`:
- 2019-04-02: ratio 0.905 → ✅ (GENUINE)
- 2023-01-13: ratio 0.889 → ✅ (GENUINE)  
- Semua 5 false signals: ratio 0.991–1.627 → ❌ (filtered out)

Signal A dengan filter ini = precision 100% di 2 events tersedia, dan fire **35–47 hari lebih awal** dari B/C.

---

## Temuan Keseluruhan dan Implikasi

### 1. Untuk Revisi Routing Zones

Zona yang disarankan dari bawah ke atas:

```
Z0 — BELOW CVDD         → Rare extreme (2 hari dari 3830)
Z1 — BELOW LTH RP       → Bear Bottom + Pre-Detection eligible
                           (tidak bisa dibedakan dari price level saja)
Z2 — LTH RP to RP       → Transisi sangat singkat (47 hari total, 1.2%)
Z3 — RP to STH RP       → Ambigu: bear mid, recovery, atau bull-under-STH
Z4 — STH RP to AVIV Mean → Early bull — price above STH, below fair value
Z5 — AVIV Mean to AVIV Upper → Mid bull
Z6 — ABOVE AVIV Upper   → Late bull / distribution (dan early 2017 bull dip)
```

**Masalah utama di Z3:** Heterogen, muncul di bear (2018, 2022), recovery (2019, 2023), dan bull (2021, 2025). Sub-classifier diperlukan via on-chain indicators — tidak bisa selesai dari price level saja.

### 2. Pre-Detection tidak punya price-level boundary sendiri

Pre-detection (2019, 2023) terjadi di Z1 (below LTH RP) — sama dengan bear bottom. Membedakannya membutuhkan: trajectory MVRV (mulai naik dari < 1), SOPR (State D persistent), dan STH/LTH ratio approaching 1.0 dari bawah.

### 3. Signal untuk routing transition (bear→bull)

Rekomendasi berdasarkan data:
- **Signal B (STH RP > RP)** atau **Signal C (STH/LTH > 1.0)** sebagai confirmation signal (67% genuine, 3 events)
- **Signal A dengan filter STH/LTH < 1.0** sebagai alert/early warning (35–47 hari lebih awal, 100% precision di subset tersedia)
- B dan C selalu fire hari yang sama → pilih satu; C (STH/LTH ratio) lebih intuitif secara visual

### 4. BD1 perlu applicable di Z6

Data historis: Bull Dip March 2017 terjadi di Z6 (price di atas AVIV Upper). BD1 tidak boleh dibatasi hanya di Z3/Z4/Z5.

---

## Open Questions untuk Diskusi Lanjut

1. **Z3 sub-classification:** Apa indikator terbaik untuk membedakan "bear dalam Z3" vs "recovery dalam Z3" vs "bull dip dalam Z3"? Kandidat: S2 Latch status, SOPR regime, STH/LTH ratio trend.

2. **Z1 split:** Apakah perlu split Z1 menjadi Z1a (far below LTH RP, > 20%) dan Z1b (approaching LTH RP, < 20%)? Z1b bisa jadi "pre-detection eligible" zona.

3. **Di atas AVIV Upper:** Apa level berikutnya yang meaningful? AVIV Upper 1.0 SD? MVRV 0σ? Data AVIV Upper 1.0 SD belum tersedia di CSV saat ini.

4. **Signal A + filter STH/LTH < 1.0:** Perlu backtest lebih lanjut dengan data 2015 (hanya 2 events tersedia 2016–2026). Apakah berlaku konsisten?

5. **CVDD sebagai hard floor:** Hanya 2 hari dalam 3830 hari di bawah CVDD. Apakah perlu jadi zone tersendiri atau cukup jadi "flag" dalam Z1?
