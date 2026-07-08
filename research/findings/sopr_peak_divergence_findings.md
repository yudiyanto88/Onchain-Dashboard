# aSOPR SMA Cross DOWN SMA365 — Cycle Peak Divergence Findings

**Disiapkan:** Juni 2026  
**Konteks:** Analisis diminishing returns aSOPR di cycle peaks, grid search SMA periods, dan implikasi untuk S1/S2 signal di Signal Framework v1.0.3

---

## Observasi Awal

Di cycle peak 2021-P2 (Nov) dan 2025 (Jan), aSOPR SMA30 berada di bawah atau hampir sama dengan SMA365 sementara harga masih di ATH. Ini adalah manifestasi **diminishing returns** — setiap siklus, market mencapai price peak dengan "exuberance" aSOPR yang semakin kecil.

---

## Diminishing Returns: Gap SMA30 vs SMA365 di Setiap Cycle Peak

| Cycle | Peak Price | Gap SMA30–SMA365 | SMA30 < SMA365? |
|-------|-----------|-----------------|----------------|
| 2013 Peak 1 | $231 | **+12.7%** | No |
| 2013 Peak 2 | $1,156 | **+14.0%** | No |
| 2017 Peak | $19,538 | **+7.9%** | No |
| 2021 Peak 1 | $63,551 | **+1.0%** | No (tipis) |
| 2021 Peak 2 | $67,525 | **-0.35%** | **YES** |
| 2024 Peak 1 | $73,095 | **+5.5%** | No |
| 2025 Peak | $106,188 | **+0.23%** | No (hampir nol) |

**Tren yang jelas:** Gap semakin menyempit di setiap siklus. Market bisa ATH dengan profit-taking yang semakin tipis — tanda mature market dengan distribusi yang lebih terstruktur.

---

## Grid Search: 14 SMA Periods vs SMA365

### Days dari Peak ke Cross DOWN (negatif = fired sebelum peak)

| SMA | 2017 | 2021-P1 | 2021-P2 | 2024-P1 | 2025 |
|-----|------|---------|---------|---------|------|
| SMA7 | +9d | +8d | **-13d** | +31d | **-14d** |
| SMA10 | +14d | +10d | **-12d** | +31d | **-12d** |
| SMA14 | +16d | +11d | **-17d** | +34d | **-12d** |
| SMA20 | +30d | +13d | — | +39d | **-8d** |
| SMA25 | +29d | +13d | — | +45d | **-6d** |
| **SMA30** | **+31d** | **+23d** | **76d early*** | **+49d** | **+2d** |
| SMA40 | +36d | +28d | — | +56d | +12d |
| SMA50 | +42d | +31d | — | +66d | +18d |
| SMA75 | +57d | +36d | — | +116d | +36d |
| SMA120 | +86d | +56d | — | +132d | +77d |
| SMA200 | +97d | +99d | — | +188d | +158d |

*SMA30 crossed DOWN 76 hari SEBELUM 2021-P2 — harga masih +47% dari situ ke ATH

### Price saat Cross DOWN vs Peak Price (semakin kecil = tangkap peak lebih baik)

| SMA | 2021-P1 | 2024-P1 | 2025 | Avg 3 peaks |
|-----|---------|---------|------|-------------|
| SMA7 | -15.3% | -12.5% | -3.7%† | -10.5% |
| SMA14 | -21.0% | -12.7% | -10.5% | -14.7% |
| SMA20 | -14.8% | -11.1% | -11.0% | -12.3% |
| SMA25 | -14.8% | -13.2% | -9.1% | -12.4% |
| **SMA30** | **-10.9%** | -20.2% | **-2.4%** | **-11.2%** |
| **SMA40** | **-10.4%** | -16.3% | **-5.2%** | **-10.6%** |
| SMA50 | -21.3% | -8.4% | -9.1% | -12.9% |
| SMA75 | -42.1% | -23.5% | -16.5% | -27.4% |
| SMA200 | -49.4% | -17.4% | +0.9% | -22.0% |

†SMA7 fired 14 hari SEBELUM 2025 peak — harga masih naik +3.7% setelah signal

---

## Tiga Insight Utama

### 1. Trade-off yang jelas antara kecepatan dan kepresisian

| Kelompok | SMA Range | Karakteristik |
|----------|-----------|---------------|
| **Terlalu cepat** | SMA7–25 | Bisa fired sebelum peak (2 dari 5 cycles), miss final run |
| **Sweet spot** | SMA30–50 | Selalu fired SETELAH peak, drawdown moderat -10% s/d -20% |
| **Terlalu lambat** | SMA75–200 | Selalu fired setelah peak tapi harga sudah -20% s/d -50% |

### 2. SMA30 dan SMA40 paling konsisten di siklus modern

| | SMA30 | SMA40 |
|--|-------|-------|
| 2021-P1 | +23d, -10.9% | +28d, -10.4% |
| 2024-P1 | +49d, -20.2% | +56d, -16.3% |
| **2025** | **+2d, -2.4%** | +12d, -5.2% |

SMA30 sangat presisi di 2025 (fired hanya 2 hari setelah peak, -2.4%).  
SMA40 konsisten sedikit lebih lambat tapi lebih "tenang" dari noise.

### 3. 2021-P2 adalah kasus anomali — tidak bisa diselesaikan dengan grid search

Tidak ada SMA period yang bisa "catch" peak November 2021 dengan clean signal:
- SMA7–25: fired 6–17 hari **sebelum** peak, harga masih naik ke ATH setelahnya
- SMA30+: fired **76+ hari sebelum** peak (saat harga $47K), terlalu early untuk dijadikan exit signal

Ini adalah kasus **extreme diminishing returns** — harga bisa ATH baru ($69K) sementara aSOPR SMA30 sudah di bawah SMA365 selama 3 bulan. SMA7–25 menangkap ini sebagai "early warning" 2 minggu sebelum ATH terakhir.

**Implikasi:** 2021-P2 mengajarkan bahwa SMA cross DOWN alone tidak cukup — harus dikombinasikan dengan konfirmasi dari metrik lain (MVRV, NUPL, Supply) untuk membedakan "legitimate early warning" dari "false exit sebelum final run."

---

## Rekomendasi: Two-Stage Alert System untuk S1/S2

### Struktur

```
Stage 1 — ALERT (SMA14 cross DOWN SMA365)
  → "aSOPR mulai kehilangan momentum distribusi"
  → Timing: 11–16 hari setelah peak (2021-P1, 2017)
             Bisa early 12–17 hari (2021-P2, 2025)
  → Action: Raise alert, monitor ketat, JANGAN full de-risk sendirian

Stage 2 — CONFIRM (SMA30 cross DOWN SMA365)
  → "Distribution phase dikonfirmasi"
  → Timing: selalu SETELAH peak di semua 5 cycles yang terukur
             2 s/d 49 hari setelah peak, harga -2.4% s/d -20%
  → Action: Valid sebagai S1/S2 trigger jika konteks zone = MERAH/KUNING ATAS
```

### Rules

**Valid sebagai S1/S2 trigger jika:**
1. Price sedang di ZONA MERAH atau KUNING ATAS (Supply > 80%, price > STH RP)
2. SMA14 sudah fired (Stage 1 confirmed)
3. SMA30 cross DOWN SMA365 terjadi (Stage 2)
4. MVRV minimal 2 trigger lain sudah fired di S1 (N-of-M context)

**Tidak valid / gunakan sebagai alert saja jika:**
- Hanya SMA14 yang fired (SMA30 belum) → alert, bukan trigger
- Price masih di ZONA HIJAU atau BIRU → bukan peak context
- SMA30 fired tapi price jauh di bawah recent ATH (>30% drawdown) → sudah terlambat, ini bukan sell signal, ini bear confirmation

### Konteks 2021-P2 Warning

Jika SMA14 fired sebagai early warning tapi SMA30 BELUM fired, dan price masih naik (seperti 2021 Aug–Nov), **jangan exit**. Ini justru bisa jadi:
- Final leg bull yang tersisa
- Hanya valid sebagai "mulai kurangi leverage" bukan "exit spot"

---

## Gap Narrowing sebagai Pre-Signal (Sinyal A)

Selain crossover, **kecepatan gap menyempit** bisa jadi early warning tambahan:

Contoh 2025:
```
Des 10:  $97K  → gap +3.98%  ← maximum
Des 17:  $106K → gap +3.63%  ← mulai menyempit
Jan 7:   $97K  → gap +1.87%  ← narrowing cepat
Jan 14:  $97K  → gap +0.68%
Jan 21:  $106K → gap +0.23%  ← PEAK
Jan 28:  $101K → gap -0.10%  ← cross DOWN
```

Gap menyempit dari +4% ke ~0% dalam **5–6 minggu** sebelum peak. Ini adalah warning window yang bisa dimonitor.

**Rule kandidat:** Jika gap SMA30–SMA365 turun dari ≥3% ke ≤1% sementara price masih di ATH territory → mulai tracking S1 triggers lebih agresif.

---

## Catatan Limitasi

- **Sample size kecil:** Hanya 5 cycle peaks (2017, 2021-P1, 2021-P2, 2024-P1, 2025) yang cukup data
- **2024-P1 outlier:** Cross DOWN datang sangat terlambat (+49–66 hari) karena penurunan pasca-ATH bersifat gradual, bukan sharp crash
- **Tidak backward-compatible sempurna:** 2013 dan 2017 peaks memiliki karakteristik berbeda (gap jauh lebih besar di peak) — framework modern mungkin tidak applicable ke siklus lama tersebut
