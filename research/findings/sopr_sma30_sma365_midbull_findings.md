# aSOPR SMA30 / SMA365 Crossover — Mid-Bull Dip Recovery Findings

**Disiapkan:** Juni 2026  
**Konteks:** Analisis sinyal aSOPR mid-bull menggunakan crossover SMA30 vs SMA365 untuk integrasi ke Signal Framework v1.0.3 sebagai BD1 trigger kandidat

---

## Definisi Sinyal

**Mid-Bull Cross UP:** SMA30 melintasi naik SMA365 dengan kondisi **SMA30 > 1.0** saat crossover terjadi.

Artinya: market sedang dalam konteks bullish (rata-rata transaksi 30 hari masih profit), dan aSOPR yang sempat tertekan selama mid-cycle correction kini recovery. Ini bukan regime change dari bear ke bull — ini **dip recovery di dalam ongoing bull market**.

---

## Filter untuk "Clean" Signal

Dari 24 total mid-bull cross UP events, hanya yang memenuhi kriteria berikut yang dianggap valid:

> **SMA30 > 1.0 saat crossover AND SMA30 bertahan di atas SMA365 selama > 30 hari sebelum cross DOWN**

- Filter ini mengeliminasi crossover noisy (oscillation 1–12 hari) yang tidak reliable sebagai entry signal
- Menghasilkan **12 clean events** dari 2012 hingga 2025

---

## Clean Events — Data Lengkap

| Date | Price | SMA30 | Days Held | Supply% | Zone | MVRV | STH-MVRV | LTH-MVRV |
|------|-------|-------|-----------|---------|------|------|----------|----------|
| 2012-11-25 | $13 | 1.0101 | 180d | 88.9% | KUNING ATAS | 1.778 | 1.122 | 2.920 |
| 2013-10-21 | $189 | 1.0412 | 70d | 99.1% | MERAH | 2.873 | 1.454 | 5.577 |
| 2016-10-26 | $680 | 1.0126 | 158d | 92.2% | KUNING ATAS | 1.774 | 1.083 | 2.307 |
| 2017-04-17 | $1,218 | 1.0199 | 89d | 94.9% | KUNING ATAS | 2.216 | 1.145 | 3.706 |
| 2017-07-27 | $2,665 | 1.0271 | 59d | 91.6% | KUNING ATAS | 2.679 | 1.207 | 7.267 |
| 2017-10-12 | $5,475 | 1.0405 | 96d | 98.3% | MERAH | 3.011 | 1.479 | 14.148 |
| 2020-01-29 | $9,300 | 1.0134 | 37d | 79.8% | HIJAU | 1.628 | 1.092 | 1.938 |
| 2020-05-07 | $9,971 | 1.0149 | 147d | 85.4% | KUNING ATAS | 1.747 | 1.227 | 2.039 |
| 2020-10-05 | $10,795 | 1.0069 | 213d | 84.2% | KUNING ATAS | 1.713 | 1.026 | 2.167 |
| 2024-10-21 | $67,349 | 1.0303 | 93d | 90.6% | KUNING ATAS | 2.053 | 1.062 | 2.694 |
| 2025-05-11 | $104,139 | 1.0270 | 46d | 98.4% | MERAH | 2.306 | 1.109 | 3.400 |
| 2025-06-30 | $107,199 | 1.0288 | 44d | 96.4% | MERAH | 2.225 | 1.083 | 3.028 |

---

## Forward Returns — Summary Stats (12 events)

| Window | Avg Return | Median Return | Win Rate |
|--------|-----------|---------------|----------|
| +30d | +37.7% | +12.9% | 10/12 (83%) |
| +60d | +62.0% | +39.5% | 10/12 (83%) |
| +90d | +95.7% | +54.4% | 11/12 (92%) |
| +180d | +202.5% | +64.2% | 10/12 (83%) |
| **Exit saat cross DOWN** | **+169.0% avg** | **+58.6%** | **11/12 (92%)** |

**Max drawdown selama hold:** avg -2.5%, worst -13.3%  
**Avg hold duration:** 103 hari (min 37d, max 213d)

---

## Exit Strategy: SMA30 Cross DOWN sebagai Exit Signal

Keunggulan signal ini bukan hanya di entry — **cross DOWN sebagai exit signal juga terbukti efektif:**

- 11 dari 12 events: exit di atas entry price (92% win rate)
- Median exit return: +58.6% — lebih consistent dari hold fixed window
- Max DD selama hold rendah (avg -2.5%) → entry timing tidak langsung underwater jauh

**Ilustrasi hold-then-exit:**

```
SMA30 ─────────────────────────────────────╮ exit sini
                    ╱ cross UP (entry)       ╰─────────
SMA365 ────────────╱──────────────────────────────────
                   ^                        ^
                entry                     exit
                                    (cross DOWN = jual)
```

---

## Catatan Khusus: Outlier 2020-01-29

Entry $9,300 → exit $9,202 (-1.1%) setelah 37 hari. Terlihat buruk, tapi konteksnya:
- COVID crash terjadi setelah exit — harga turun ke $3,800
- **Cross DOWN pada Mar 6 justru berfungsi sebagai stop-loss yang efektif**, memotong posisi -1.1% sebelum crash -60%
- Ini bukan kegagalan signal, ini black swan yang di-manage dengan baik oleh exit rule

---

## Konteks Market saat Clean Events Terjadi

**Zone dominan:** KUNING ATAS (7 dari 12 events) — semua di zona bull market, bukan bear recovery

**Range MVRV:** 1.63 – 3.01 (rata-rata 2.2) — semua events terjadi saat market genuinely dalam bull regime (MVRV > 1.5)

**STH-MVRV:** 1.03 – 1.48 (rata-rata 1.2) — short-term holders selalu profit saat crossover, tapi belum overstretched

**LTH-MVRV:** 1.94 – 14.1 — range luas, dari awal bull (2.0) hingga late-cycle (14x). Signal ini bekerja di berbagai titik dalam siklus.

---

## Implikasi untuk Signal Framework

### Integrasi ke BD1 (Bull Dip Confirmation)

Trigger kandidat tambahan untuk BD1 (zona HIJAU/KUNING ATAS):

> **aSOPR SMA30 cross UP SMA365, dengan SMA30 > 1.00 saat crossover, dan sustained > 30 hari**

- Bobot: 1 dari 7 trigger BD1
- Karakteristik: mid-cycle dip recovery signal, bukan regime change
- Valid hanya ketika S2 Latch TIDAK aktif (harus dalam confirmed bull market context)
- Exit companion: SMA30 cross DOWN = pertimbangkan reduce / exit partial

### Perbedaan dengan Tipe 1 (Pre-Detection)

| Aspek | Pre-Detection (Tipe 1) | Mid-Bull Recovery (Tipe 2) |
|-------|----------------------|--------------------------|
| SMA30 saat crossover | < 1.0 (masih tertekan) | > 1.0 (sudah bullish) |
| Zone framework | BIRU / HIJAU TUA | KUNING ATAS / MERAH |
| MVRV konteks | < 1.0 – 1.2 (distressed) | > 1.5 (bull confirmed) |
| Role di framework | PD1 trigger ke-4/5 | BD1 trigger |
| Exit signal | Cross DOWN atau PD1 confirmed | Cross DOWN = pertimbangkan jual |

### Syarat tambahan yang disarankan sebelum act

Karena ini masuk BD1 (bukan standalone signal), harus dikonfirmasi dengan:
1. S2 Latch belum aktif / sudah di-reset oleh PD1
2. Price masih di atas STH Realized Price (zona atas)
3. Minimal 2 trigger BD1 lain sudah fired (dari 7 total)
