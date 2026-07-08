# BITCOIN ON-CHAIN SIGNAL FRAMEWORK V1.0

**Version:** 1.0
**Created:** 5 Juni 2026
**Foundation:** 5 Knowledge Base documents (MVRV, NUPL, SOPR, Realized Prices, Supply in Profit/Loss)
**Data coverage:** Maret 2017 – Mei 2026 (3 complete cycles)
**Architecture:** Signal-based N-of-M confirmation + Decision Tree routing + Scoring dashboard

---

## FRAMEWORK ARCHITECTURE

Tiga layer yang bekerja bersamaan:

**Layer 1 — ROUTING (Decision Tree)**
Quick-check untuk menentukan kamu di zona mana. Ini menentukan SET OF SIGNALS mana yang aktif. Routing pakai 2 metrik yang paling stabil lintas cycle: Price vs STH Realized Price, dan Total Supply in Profit.

**Layer 2 — SIGNALS (N-of-M Confirmation)**
Per zona, ada specific trigger conditions. Setiap trigger butuh konfirmasi dari N indikator sebelum actionable. N bervariasi per signal — semakin ambigu zona-nya, semakin banyak konfirmasi yang dibutuhkan.

**Layer 3 — DASHBOARD (Weekly Scoring)**
Summary mingguan: setiap indikator dikasih status per regime. Untuk tracking trajectory, bukan decision-making.

---

## LAYER 1: ROUTING — DI ZONA MANA KAMU SEKARANG?

### Step 1: Cek Price vs STH Realized Price

```
Price > STH RP secara sustained (>80% hari dalam 30 hari terakhir)?
├── YA → ZONA ATAS (bull territory)
│   └── Lanjut Step 2A
└── TIDAK → ZONA BAWAH (stress/bear territory)
    └── Lanjut Step 2B
```

### Step 2A (Zona Atas): Cek Total Supply in Profit

```
Total Supply in Profit?
├── > 95% → ZONA MERAH: Sell signals aktif (S1, S2, S3)
├── 80–95% → ZONA KUNING ATAS: Monitor signals, late-cycle checks aktif
└── 65–80% → ZONA HIJAU: Bull market normal, bull dip buy signals aktif (BD1)
```

### Step 2B (Zona Bawah): Cek Total Supply in Profit

```
Total Supply in Profit?
├── > 65% → ZONA KUNING BAWAH: Ambiguous zone — full N-of-M confirmation required (BD1, BT1)
├── 50–65% → ZONA BIRU: Pre-detection / early bull signals aktif (PD1, SB1)
└── < 50% → ZONA HIJAU TUA: Accumulation signals aktif (BB1)
```

### Routing Summary

| Zona | Kondisi | Signals Aktif | Mindset |
|------|---------|---------------|---------|
| MERAH | Price > STH RP + Total Profit > 95% | S1, S2, S3 | Reduce exposure, monitor divergence |
| KUNING ATAS | Price > STH RP + Total Profit 80–95% | Late-cycle checks, BD1 | Alert, position sizing conservative |
| HIJAU | Price > STH RP + Total Profit 65–80% | BD1 | Normal bull, buy dips |
| KUNING BAWAH | Price < STH RP + Total Profit > 65% | BD1 + BT1 (full confirmation) | AMBIGUOUS — paling butuh konfirmasi |
| BIRU | Price < STH RP + Total Profit 50–65% | PD1, SB1 | Transitioning, scale in cautiously |
| HIJAU TUA | Price < STH RP + Total Profit < 50% | BB1 | Deep accumulation zone |

**⚠️ OVERRIDE RULE:** Kalau ada posisi leverage/loan aktif, LTV buffer di-cek SEBELUM routing. Kalau LTV mendekati danger zone, semua analisis on-chain secondary — risk management first.

---

## LAYER 2: SIGNAL DEFINITIONS

Setiap signal punya: trigger conditions dari 5 indikator, minimum confirmation requirement (N-of-M), historical hit rate, dan prescribed action.

---

### SELL SIGNALS

---

#### S1: CYCLE PEAK WARNING

**Kapan aktif:** Zona MERAH

**Trigger conditions (6 indikator):**

| # | Indikator | Kondisi | Basis KB | Hit Rate |
|---|-----------|---------|----------|----------|
| 1 | MVRV | MVRV > 2.2 + bearish divergence (ATH baru, MVRV lebih rendah dari ATH sebelumnya) | MVRV S1 | 2/2 (2021, 2025) |
| 2 | NUPL | NUPL > 0.55 + STH-NUPL < 0.10 + LTH-STH gap > 0.60 | NUPL S2 + S3 | 4/4 (2021-2025) |
| 3 | SOPR | aSOPR 7d avg declining dari > 1.03 saat harga di ATH (Divergence #3: elevated aSOPR + STH declining) | SOPR S1 + Div #3 | 2/2 (2021, 2025 LH) |
| 4 | Realized Prices | Price/STH < 1.15 saat ATH + degrading across successive ATHs | RP Rule 3.1 | 3/3 |
| 5 | Supply | Total profit > 95% TAPI STH profit trending down across successive ATHs | Supply Sell | Consistent pattern |
| 6 | SOPR MA Gap | STH-SOPR MA90 vs MA90-MA60 gap peaked dan declining. Semakin jauh gap sudah turun dari peak, semakin kuat signal. | SOPR Bagian 11, Signal A | 6/6 (semua local tops + cycle peaks) |

**Minimum confirmation:** 3 of 6

**Prescribed action:**
- 3 of 6: Mulai reduce exposure 20-30%. Tighten stops. Review LTV buffer. Kalau ada posisi loan: mulai reduce loan saat gap pertama kali declining — jangan tunggu trigger penuh.
- 4 of 6: Reduce exposure 40-50%. No new leveraged positions. Loan exposure harus sudah turun signifikan.
- 5+ of 6: Significant de-risk. Prepare untuk transisi ke S2.

**Post-S1 confirmation — Signal B (Bearish Cross setelah Local Top):**

Setelah S1 trigger, monitor apakah MA90 crosses di bawah MA90-MA60. Cross ini mengkonfirmasi koreksi sedang berlangsung.

| Bearish Cross Date | Setelah Event | Outcome | Basis KB |
|---|---|---|---|
| 28 Mar 2021 | Local Top Mar 2021 (+15d) | Mid-Cycle Correction -50% | SOPR 11.4 |
| 28 Apr 2024 | Local Top Mar 2024 (+45d) | Bull dips berturut-turut | SOPR 11.4 |
| 3 Feb 2025 | Local Top Jan 2025 (+14d) | Bull Dip -25% | SOPR 11.4 |

Hit rate: 3/3 — bearish cross setelah local top selalu diikuti koreksi signifikan.

**Fungsi praktis — Post-Signal-B Workflow:**

```
Signal B fire (bearish cross MA90/MA60)
    ↓
Koreksi confirmed. JANGAN re-enter atau tambah posisi.
    ↓
Monitor BTC price vs MVRV 0σ dan Cum PL Price
(gunakan whichever is HIGHER dari keduanya sebagai reference)
    ↓
Price TIDAK cross di bawah kedua level
    → Bull dip tanpa sentuh level → check BD1 triggers → re-entry bila confirmed
    ↓
Price cross di bawah salah satu atau kedua level:
    ├── Recovery ≤ 4 hari → BULL DIP (data: semua bull dips ≤ 4 hari, 11/11)
    │   → Check BD1 triggers untuk re-entry
    │
    ├── 5-6 hari → GREY ZONE (n=1, borderline)
    │   → Jangan assume bull dip. Check S2 triggers + BT1 triggers.
    │   → Kalau Signal C juga aktif: treat lebih dekat ke bear.
    │
    └── ≥ 7 hari → BEAR CONFIRMED (data: 5/6 bear, 1/6 MCC acceptable)
        → LATCH: bear stays confirmed sampai PD1/SB1 triggers
        → Brief bounces di atas level setelah ini = dead cat, bukan reset
        → Full de-risk, exit leverage, transisi ke S2
```

**Backtest sequence (Signal B/C selalu fire sebelum price breakdown, 6/6):**

| Signal | Signal Date | Price Breakdown | Lead Time |
|---|---|---|---|
| Signal C 2018 | 19 Jan | 30 Jan | +11 hari |
| Signal B 2021 | 28 Mar | 28 Mei | +61 hari |
| Signal C 2021 | 30 Nov | 1 Mar 2022 | +91 hari |
| Signal B 2024 | 28 Apr | 5 Agt | +99 hari |
| Signal B 2025 | 3 Feb | 6 Apr | +62 hari |
| Signal C 2025 | ~27 Oct | 4 Nov | +8 hari |

**⚠️ MCC false positive (n=1):** Jun 2021, 11 hari di bawah level setelah Signal B → framework classify BEAR, actual = MCC. Tapi de-leverage saat -50% drawdown adalah behavior yang correct. Re-entry via BD1/PD1 setelah recovery.

**⚠️ Signal B tidak bisa bedakan severity.** Mar 2021 → -50% (MCC). Feb 2025 → -25% (bull dip). Cross hanya bilang "koreksi real." Price level duration adalah severity filter.

**⚠️ DANGER ZONE — ATH dengan gap MA90-MA60 sudah negatif:**
Kalau harga membuat ATH baru tapi SOPR MA90-MA60 gap sudah negatif (MA90 < MA90-MA60), ini potential cycle peak tanpa dukungan profitability momentum. Di data, Oct 2025 ATH ($123K) terjadi dengan gap -0.00152 — satu-satunya ATH di dataset dimana gap sudah negatif. Semua cycle peak sebelumnya (2017, 2021) dan Jul 2025 ATH masih punya gap positif saat ATH.

Kalau kondisi ini terjadi: treat sebagai potential cycle peak. Fokus pada S1 trigger count dan siapkan transisi ke S2. Pattern ini baru n=1 — monitor apakah repeat di cycle berikutnya.

**Catatan terminologi — MVRV 0σ:** Sepanjang framework ini, MVRV 0σ merujuk ke `mvrv_avg_price` — yaitu price level dimana MVRV Ratio = long-term historical average-nya. Bukan MVRV Z-Score. Semua trigger conditions yang menyebut angka MVRV (> 2.2, ≈ 1.0, < 1.0, dll) mengacu ke MVRV Ratio, bukan Z-Score.

**Confidence:** MEDIUM — n=2 untuk cycle peaks yang applicable (2021, 2025). Trigger #6 menambah coverage (6/6 hit rate) tapi juga menambah lead time yang bisa terlalu early. Threshold MVRV > 2.2 mungkin terlalu tinggi di cycle berikutnya (diminishing returns). Recalibrate setiap cycle.

**Cost of being wrong:** Sell di local top bukan cycle peak → miss 10-30% upside yang masih bisa re-enter setelah koreksi. Asymmetry favors partial selling.

**Cost of missing signal:** Hold through cycle peak → drawdown 50-80%.

---

#### S2: LOWER HIGH CONFIRMATION (Bear Confirmed)

**Kapan aktif:** Zona MERAH dan KUNING ATAS, setelah S1 pernah trigger atau setelah price membentuk potential lower high

**Trigger conditions:**

| # | Indikator | Kondisi | Basis KB | Hit Rate |
|---|-----------|---------|----------|----------|
| 1 | MVRV | STH-MVRV ≈ 1.0 (range 1.00-1.07) + MVRV < cycle peak MVRV + MVRV declining | MVRV S3 | 2/2 |
| 2 | NUPL | STH-NUPL < 0.07 + NUPL > 0.50 + gap > 0.60 + ratio > 11 atau sign flip | NUPL S2 + S3 + Ratio Zona 4 | 4/4 (2021-2025) |
| 3 | SOPR | aSOPR declining saat harga naik + STH-SOPR declining | SOPR 1.5 | 4/4 |
| 4 | Realized Prices | Price/STH ≤ 1.05 saat lower high + Price above STH RP < 50% dalam 30d sebelumnya | RP Rule 3.4 | 2/2 (recent) |
| 5 | Supply | Total profit 85-91% + STH profit collapsing (< 60%) sementara LTH masih > 93% | Supply 1.3 | 5/5 |
| 6 | SOPR MA Cross | STH-SOPR MA90 crosses di bawah MA90-MA60 setelah cycle peak. Timing cross historically hampir persis di tanggal lower high (Jan 2018: cross 19 Jan = LH period Jan 1-8. Nov 2021: cross 30 Nov = LH date 30 Nov-2 Des). | SOPR Bagian 11.5, Signal C | 2/2 |

**Minimum confirmation:** 3 of 6

**Prescribed action:**
- 3 of 6: Bear confirmed. Exit leveraged positions. Reduce spot exposure ke defensive level.
- 4+ of 6: High-conviction bear. Dari data, 7 hari pertama setelah lower high adalah window drop tercepat (MVRV KB Finding 4: front-loaded decline di 3/4 cases). Act within days, bukan weeks.
- Trigger #6 (Signal C) terpenuhi: ini memberikan mechanical timestamp yang presisi. Kalau MA90 bearish cross terjadi dalam konteks post-cycle-peak, treat sebagai strong independent confirmation bahwa lower high sudah terbentuk, bahkan kalau trigger lain masih borderline.

**Confidence:** HIGH — setiap KB secara independen menunjukkan lower high sebagai salah satu signal paling reliable.

**Pre-requisite:** Harus ada price structure yang menunjukkan lower high (harga di bawah ATH setelah cycle peak candidate). Ini bukan murni on-chain — butuh price context.

**⚠️ LATCH MECHANISM:** Begitu S2 triggers (3/6 confirmed), bear STAYS confirmed. Brief bounces di atas MVRV 0σ / Cum PL tidak reset signal. Data: 2018 dan 2022 sama-sama punya 1-4 hari reclaim attempts setelah breakdown — semua ditolak. Bear hanya "un-confirmed" kalau PD1 triggers.

**⚠️ FAILED RECLAIM = ADDITIONAL CONFIRMATION:** Kalau harga breakdown lalu bounce kembali ke level MVRV 0σ / Cum PL tapi gagal sustained di atas (< 7 hari lalu turun lagi), ini memperkuat S2. Pattern 3/3 di bear transitions: setiap failed reclaim attempt semakin lemah (7d → 4d → 1d di 2025), sebelum final breakdown.

---

### BUY SIGNALS

---

#### BB1: DEEP BEAR BOTTOM (Accumulation Zone)

**Kapan aktif:** Zona HIJAU TUA

**Trigger conditions:**

| # | Indikator | Kondisi | Basis KB | Hit Rate |
|---|-----------|---------|----------|----------|
| 1 | MVRV | All three < 1.0 (MVRV, STH-MVRV, LTH-MVRV) | MVRV B1 | 6/6 |
| 2 | NUPL | All three negative (NUPL, STH-NUPL, LTH-NUPL) + gap near zero | NUPL B4 + Gap 9.1 | 5/5 |
| 3 | SOPR | aSOPR < 0.93 + LTH-SOPR < 0.50 (deep LTH capitulation) | SOPR B2 | 3/3 |
| 4 | Realized Prices | STH/LTH RP < 1.0 + Price/RP < 1.0 | RP Rules 4.1, 4.2 | 2/2 dan 3/3 |
| 5 | Supply | Total profit < 50% + STH profit < 10% | Supply Combined Buy | 6/6 (< 50%) |

**Minimum confirmation:** 4 of 5

**Prescribed action:**
- 4 of 5: Begin DCA accumulation. BUKAN lump sum. Dari data: FTX trigger Nov 8 ($18.5K) → harga turun lagi ke $15.7K (15% drawdown tambahan). "Bottom zone" ≠ "exact bottom."
- 5 of 5: Increase DCA pace. Dari data, 5/5 confluence belum pernah gagal, tapi expect masih bisa turun 10-20%.
- Scale: DCA 20-30% dari planned allocation per bulan selama signals aktif.

**Confidence:** VERY HIGH — ini signal dengan convergence terbaik di seluruh library. Lima indikator independen, semua menunjuk ke zona yang sama.

**⚠️ TIMING CAVEAT:** Bottom zone bisa berlangsung minggu sampai bulan. Bear Bottom 2018 ke Start of Bull 2019 = ~4 bulan. FTX Nov 2022 ke Start of Bull Feb 2023 = ~3 bulan. Sabar. DCA. Jangan all-in.

**⚠️ LEVERAGE CAVEAT:** JANGAN leverage di zona ini. Meskipun historically high-conviction accumulation zone, additional drawdown 10-20% + volatility bisa trigger liquidation. Cash/spot only.

---

#### PD1: PRE-DETECTION / START OF BULL

**Kapan aktif:** Zona BIRU

**Trigger conditions — Pre-Detection:**

| # | Indikator | Kondisi | Basis KB | Hit Rate |
|---|-----------|---------|----------|----------|
| 1 | MVRV | STH-MVRV crossing above LTH-MVRV, keduanya mendekati 1.0 | MVRV B3 | 2/2 |
| 2 | NUPL | Gap negatif (STH > LTH), keduanya positif dan rendah (< 0.20), ratio < 1.0 | NUPL Gap 9.1 + Ratio Zona 1 | 2/2 |
| 3 | SOPR | STH-SOPR > 1.0 sustained + aSOPR masih < 1.0 + State D↔E oscillation 2-4 minggu | SOPR B3 + State D | 2/2 |
| 4 | Realized Prices | Price approaching STH RP dari bawah + STH/LTH < 1.0 | RP 2.8 | 2/2 |
| 5 | Supply | STH profit > LTH profit + Total profit 56-59% | Supply 1.8 | 3/3 |

**Minimum confirmation:** 3 of 5 untuk Pre-Detection, 4 of 5 untuk Start of Bull

**Trigger conditions — Start of Bull (upgrade dari Pre-Detection):**

| # | Indikator | Kondisi | Basis KB |
|---|-----------|---------|----------|
| 1 | MVRV | All three > 1.0 | MVRV 2.6 |
| 2 | NUPL | All three positive, STH > LTH | NUPL 2.9 |
| 3 | SOPR | aSOPR sustained > 1.0 (7+ hari) | SOPR 1.7 |
| 4 | Realized Prices | Price > STH RP sustained + STH/LTH < 1.0 + Price/RP > 1.0 | RP 2.9 |
| 5 | Supply | Total profit ~64%, STH profit 75-81% | Supply 1.9 |

**Prescribed action:**
- Pre-Detection (3 of 5): Increase DCA allocation. Masih spot only.
- Start of Bull (4 of 5): Full allocation. Conservative leverage mulai masuk akal per strategy table. Tapi multi-indicator confirmation dulu, bukan single signal.

**Confidence:** HIGH untuk identification, tapi n=2 untuk setiap individual trigger. Fingerprint-nya sangat tight di semua 5 KB — ini yang memberi confidence meskipun sample kecil.

---

#### BD1: BULL DIP BUY

**Kapan aktif:** Zona HIJAU, KUNING ATAS, dan KUNING BAWAH

**⚠️ INI SIGNAL YANG PALING BUTUH KONFIRMASI karena bull dip vs bear onset overlap.**

**Pre-requisite:**

S2 belum trigger. Kalau S2 sudah fire (bear confirmed oleh 3/6 multi-indicator check), BD1 tidak applicable — kamu bukan di bull dip, kamu di bear market. Ini regime check, bukan probabilistic signal.

**Trigger conditions:**

| # | Indikator | Kondisi | Basis KB | Hit Rate |
|---|-----------|---------|----------|----------|
| 1 | MVRV | STH-MVRV < 0.95 + LTH/STH ratio RISING (14d pre-dip) | MVRV B2 + Ratio Finding 3 | Ratio rising: 100% (10/10) |
| 2 | NUPL | STH-NUPL < -0.05 + LTH-NUPL > 0.50 + NUPL > 0.30 | NUPL B3 | 6/8 (75%) |
| 3 | SOPR | STH-SOPR < 0.97 sustained < 14 hari + aSOPR > 0.95 | SOPR B1 + durasi | 5/5 triggered, 100% recovery |
| 4 | Realized Prices | Price/STH > 0.85 (not extreme capitulation) + STH/LTH > 2.0 | RP 2.4 + 4.4 | Type 1 dips (>1.0): 8/8. Type 2 (< 1.0): mixed |
| 5 | Supply | STH profit declining + Total profit masih > 60% | Supply 3A Pattern 1 | Consistent di bull dips |
| 6 | Supply | LTH profit stable (±2pp dari 30d average) — LTH tidak ikut turun | Supply 3A + 4C | 9/14 recover when LTH stable |
| 7 | Price Level | Price briefly di bawah MVRV 0σ / Cum PL lalu recover ≤ 4 hari — "level held as support" | Price level backtest | 11/11 bull dip ketika ≤ 4 hari |

**Minimum confirmation — depends on zona dan LC1 score:**

| Zona | LC1 Score | Minimum N | Alasan |
|------|-----------|-----------|--------|
| HIJAU (Total Profit 65-80%) | 0-1 of 7 | 3 of 7 | Early-mid bull, lower risk |
| HIJAU | 2-3 of 7 | 4 of 7 | Late cycle awareness, tighter bar |
| KUNING ATAS (Total Profit 80-95%) | any | 4 of 7 | Late cycle by definition |
| KUNING BAWAH (Price < STH RP, Profit > 65%) | any | 5 of 7 | AMBIGUOUS ZONE — highest bar |

**Prescribed action:**
- N met: Add to position. Size = 50% of normal dip-buy allocation (conservative karena BD1 punya 32.5% standalone precision per MVRV KB).
- N met + SOPR recovery velocity > +0.015/day (MVRV KB Finding 3): Full dip-buy allocation.
- N NOT met: Wait. Jangan beli hanya karena "terasa murah."

**Confidence:** MEDIUM — ini signal terlemah di framework. Improve path: tambah Exchange Net Flows di V1.1.

**Cost of being wrong:** Buy di bull dip yang ternyata awal bear → drawdown 15-30% sebelum stop-loss area. Manageable kalau sizing conservative (50% allocation).

---

### CAUTION / TRANSITION SIGNALS

---

#### BT1: BEAR TRANSITION WARNING

**Kapan aktif:** Zona KUNING BAWAH — berjalan paralel dengan BD1. Di zona ini, kedua signal aktif bersamaan. BD1 mencari konfirmasi bullish, BT1 mencari konfirmasi bearish. Yang lebih banyak trigger-nya yang menentukan arah.

**Ini bukan "sell everything" signal. Ini "regime sedang berubah, reduce risk" signal.**

**Trigger conditions (minimal 2 dari 5 harus TRUE):**

| # | Kondisi | Basis KB |
|---|---------|----------|
| 1 | Price < STH RP sustained > 14 hari + STH/LTH RP compressing (turun > 0.3 dalam 2 bulan) | RP Rule 3.2 + Red Flag 2 |
| 2 | STH-SOPR < 0.97 sustained > 14 hari (bukan bull dip lagi, escalating) | SOPR: Mid-Cycle vs Bull Dip distinguisher |
| 3 | NUPL gap widening (> 0.60) dengan NUPL > 0.45 dan STH negatif | NUPL Divergence Type 2 (bearish) |
| 4 | LTH profit declining > 5pp/bulan dari 100% atau near-100% | Supply KB 4C |
| 5 | Price breakdown di bawah MVRV 0σ / Cum PL 5-6 hari (grey zone) + Signal B/C aktif, ATAU failed reclaim: harga bounce kembali ke level tapi ditolak dalam < 7 hari | Price level analysis + backtest 3/3 |

**Prescribed action:**
- 2 of 5: Reduce leverage. Tighten LTV buffer ke conservative level. Jangan tambah posisi baru.
- 3 of 5: Actively de-risk. Ini historically precedes bear market confirmation.
- 4-5 of 5: Treat as pre-bear. Protect capital. Siapkan transisi ke S2.

**Confidence:** MEDIUM-HIGH — pattern ini konsisten tapi window antara BT1 dan full bear confirmation (S2) bisa 2-8 minggu.

---

#### LC1: LATE CYCLE ALERT

**Kapan aktif:** Zona KUNING ATAS — background monitoring selama bull market

**Tujuan:** Mendeteksi bahwa cycle sudah mature SEBELUM signals jelas. Ini bukan trigger untuk action besar, tapi untuk mindset shift dari "aggressive" ke "cautious."

**Checklist (score 0-7, berapa yang TRUE):**

| # | Kondisi | Basis KB |
|---|---------|----------|
| 1 | Price/STH degrading across 2+ successive ATHs (current ATH Price/STH < previous ATH Price/STH) | RP Rule 3.1 |
| 2 | Bull dips sudah konsisten Type 2 (Price/STH < 1.0 di dip) | RP 2.4 |
| 3 | MVRV bearish divergence di 2+ ATH berturut-turut (ATH baru, MVRV lebih rendah) | MVRV 5.1, Div 1 |
| 4 | STH-NUPL peak values declining di successive local tops | NUPL 2.2 |
| 5 | aSOPR 7d average peak semakin rendah di successive rallies | SOPR diminishing |
| 6 | STH-SOPR MA90-MA60 gap peak values semakin rendah di successive rallies (gap magnitude diminishing) | SOPR Bagian 11.7 |
| 7 | MVRV 0σ / Cum PL ratio < 1.03 di ATH (compressing menuju inversion). Ratio < 1.0 = unprecedented warning. Di 2021 cycle ratio stabil ~1.12; di 2024-2025 cycle compressed dari 1.07 ke 0.998 di cycle peak. | Price level analysis |

**Interpretation:**
- 0-1 of 7: Cycle masih sehat.
- 2-3 of 7: Late cycle. Kurangi sizing pada dip buys. Mulai plan exit strategy.
- 4-7 of 7: Very late cycle. Dip buys harus sangat selective (BD1 minimum N naik, lihat BD1 table). Persiapan untuk S1 trigger.

---

## LAYER 3: WEEKLY DASHBOARD

### Template Mingguan

```
DATE: [tanggal]
BTC PRICE: $[harga]

=== ROUTING ===
Price vs STH RP: [ABOVE / BELOW] (sustained [X]% of last 30d)
Total Supply in Profit: [XX]%
ZONA: [MERAH / KUNING ATAS / HIJAU / KUNING BAWAH / BIRU / HIJAU TUA]

=== ACTIVE SIGNALS ===
[List signals yang aktif berdasarkan zona]

=== PER-INDICATOR STATUS ===

MVRV Family:
- MVRV Ratio: [value] | Trajectory: [rising/falling/flat]
- STH-MVRV: [value] | vs 1.0: [above/below]
- LTH-MVRV: [value] | vs 1.0: [above/below]
- LTH/STH Ratio: [value] | Direction: [rising/falling]
- Bearish divergence across ATHs: [YES/NO]

NUPL Family:
- NUPL: [value] | Trajectory: [rising/falling/flat]
- STH-NUPL: [value] | vs 0: [positive/negative]
- LTH-NUPL: [value] | vs 0: [positive/negative]
- LTH-STH Gap: [value]
- LTH/STH Ratio: [value] | Zona: [1-5]

SOPR Family:
- aSOPR: [value] | 7d avg: [value] | vs 1.0: [above/below]
- STH-SOPR: [value] | vs 1.0: [above/below] | Duration below: [X days]
- LTH-SOPR: [value] | vs 1.0: [above/below]
- EMA55/SMA35 status: [bullish cross / bearish cross / no cross]
- Divergence State: [A/B/C/D/E]
- STH-SOPR MA90 vs MA90-MA60 gap: [value] | Direction: [rising/peaked/declining] | Cross status: [above/below]

Price Level Analysis (MVRV 0σ / Cum PL):
- MVRV 0σ Price: $[value]
- Cum PL Price: $[value]
- Higher of two: $[value] ([which one])
- Price vs Higher Level: [ABOVE / BELOW] | Days in current state: [X]
- MVRV 0σ / Cum PL Ratio: [value] | vs 1.0: [above/below] | Trend: [compressing/stable/inverting]
- Signal B/C active?: [YES (date fired) / NO]
- If Signal B/C active: Duration below higher level: [X days] → [BULL DIP / GREY ZONE / BEAR CONFIRMED / Not triggered yet]
- Last failed reclaim attempt: [date, X days sustained above]

- Price/RP: [value]
- Price/STH RP: [value]
- STH/LTH RP: [value] | Trajectory: [compressing/expanding]
- Price above STH RP: [X]% of last 30d

Supply in Profit:
- Total Profit: [value]%
- STH Profit: [value]%
- LTH Profit: [value]% | Trajectory: [stable/declining/rising]
- STH > LTH?: [YES/NO]

=== SIGNAL CHECK ===
[Per signal yang aktif, list berapa trigger yang terpenuhi]
[Contoh: "BD1: 2/5 triggers met (SOPR ✅, MVRV ✅, NUPL ❌, RP ❌, Supply ❌) → NOT ACTIONABLE"]

=== REGIME ASSESSMENT ===
Primary: [regime terbaik fit]
Secondary: [alternative regime kalau data ambigu]
Confidence: [HIGH / MEDIUM / LOW]

=== ACTION ITEMS ===
[Apa yang dilakukan minggu ini berdasarkan assessment]
[LTV check kalau ada posisi aktif]

=== CONTENT IDEAS ===
[2-3 ide dari insight minggu ini]
```

---

## RISK MANAGEMENT OVERLAY

Rules ini OVERRIDE semua signal di atas.

### Rule 1: LTV Buffer First

Kalau ada posisi loan/leverage aktif:
- Cek LTV buffer SEBELUM analisis on-chain apapun
- Kalau LTV > 50%: de-risk immediately, analisis bisa nanti
- Kalau LTV 40-50%: monitor daily, prepare collateral top-up
- Kalau LTV < 40%: proceed dengan analisis normal

### Rule 2: Simultaneous Worst-Case (Oktober 2025 Rule)

Setiap kali sizing atau leverage dibahas, tanya:
"Kalau BTC turun 30% DAN [worst case kedua] terjadi bersamaan, apa yang terjadi dengan posisi ini?"

Worst case kedua bisa: altcoin portfolio crash, fiat income disruption, exchange freeze, atau regulatory shock. Kalau jawaban worst-case = liquidation → sizing terlalu besar.

### Rule 3: Signal Conflict = Reduce, Bukan Add

Kalau sell signal dan buy signal aktif bersamaan (bisa terjadi di zona KUNING), DEFAULT = reduce exposure. Jangan tambah posisi saat signals konflik. Tunggu clarity.

### Rule 4: Diminishing Returns Recalibration

Setiap kali ATH baru tercapai di cycle baru, recalibrate:
- S1 MVRV threshold: expect ~30% lower dari cycle sebelumnya
- NUPL peak: expect ~15% lower
- aSOPR peak: expect ~20% lower
- Price/STH at peak: expect ~15% lower

Ini bukan exact science, tapi directional guidance untuk mencegah "threshold lama tidak pernah trigger."

### Rule 5: No Leverage Before Start of Bull Confirmed

Per strategy table: leverage hanya setelah Start of Bull Confirmation (PD1 → SB1 upgrade, 4+ of 5 confirming). Sebelum itu, spot only. Ini non-negotiable.

---

## CURRENT STATE ASSESSMENT (Data terakhir: 20 Mei 2026)

### Routing

- Price: ~$77,563
- STH RP: ~$78,000 → Price ≈ STH RP (borderline)
- Price < STH RP sustained? Yes (majority of recent weeks)
- Total Supply in Profit: 61.9%
- **ZONA: BIRU (Price < STH RP + Total Profit 50-65%)**
- **Signals aktif: PD1 (Pre-Detection) dan BB1 (Bear Bottom)**

### Per-Signal Check

**BB1 (Deep Bear Bottom):**

| # | Trigger | Status | Met? |
|---|---------|--------|------|
| 1 | MVRV all three < 1.0 | MVRV 1.43, STH 0.99, LTH 1.59 → LTH masih > 1.0 | ❌ |
| 2 | NUPL all three negative | Estimated NUPL ~0.30 (masih positif) | ❌ |
| 3 | aSOPR < 0.93 + LTH < 0.50 | aSOPR 0.887 ✅, LTH 0.822 (> 0.50) | ❌ (partial) |
| 4 | STH/LTH RP < 1.0 + Price/RP < 1.0 | STH/LTH 1.6 (> 1.0), Price/RP 1.4 (> 1.0) | ❌ |
| 5 | Total profit < 50% + STH profit < 10% | Total 61.9% (> 50%), STH 47.4% (> 10%) | ❌ |

**BB1 result: 0 of 5 → NOT in bear bottom zone.** aSOPR satu-satunya yang menunjukkan deep capitulation levels. Semua metrik lain belum sampai.

**PD1 (Pre-Detection):**

| # | Trigger | Status | Met? |
|---|---------|--------|------|
| 1 | STH-MVRV crossing above LTH-MVRV | STH 0.99, LTH 1.59 → STH masih < LTH | ❌ |
| 2 | NUPL gap negatif, keduanya positif rendah, ratio < 1.0 | Gap masih positif (LTH > STH) | ❌ |
| 3 | STH-SOPR > 1.0 + aSOPR < 1.0 + State D sustained | STH-SOPR 0.889 (< 1.0), sporadis State D tapi belum sustained | ❌ |
| 4 | Price approaching STH RP dari bawah + STH/LTH < 1.0 | Price ≈ STH RP (approaching) ✅, tapi STH/LTH 1.6 (> 1.0) | ❌ (partial) |
| 5 | STH profit > LTH profit | STH 47.4% < LTH 65.3% | ❌ |

**PD1 result: 0 of 5 → NOT in pre-detection zone.**

### Assessment

**Primary regime: Bear Market Decline (late stage)**

Berdasarkan:
- Semua metrik masih di atas bear bottom thresholds
- Tapi aSOPR 0.887 sudah di deep capitulation territory (historically hanya di bear bottoms)
- STH/LTH RP 1.6 masih compressing (target < 1.0 untuk bottom)
- LTH profit 65% masih turun (target 54-56% untuk pre-detection)

**Divergence yang worth monitoring:** SOPR sudah di levels yang historically hanya terjadi near bottom. Tapi 4 indikator lain belum confirm. Dua kemungkinan:
1. SOPR leading — bottom lebih dekat dari yang 4 indikator lain suggest. Monitoring apakah SOPR State D mulai sustained.
2. Current cycle punya SOPR behavior yang berbeda karena ETF/institutional flows — SOPR readings lebih extreme tanpa harga se-extreme historical bottoms.

Tanpa data tambahan, default ke conservative interpretation: bear market masih berlanjut, belum accumulation zone. Monitor weekly.

**Confidence: MEDIUM** — trajectory konsisten dengan bear decline, tapi SOPR divergence menambah uncertainty.

**Action items:**
- Spot only. No leverage.
- Kalau ada posisi loan: cek LTV, pastikan buffer cukup untuk additional 20-30% downside.
- Monitor STH/LTH RP compression weekly. Target: < 1.2 untuk early signal, < 1.0 untuk confirmation.
- Monitor SOPR State D frequency. Kalau sustained 2+ minggu: upgrade assessment.

---

## KNOWN LIMITATIONS & IMPROVEMENT PATH

### Apa yang framework ini TIDAK bisa lakukan

1. **Predict exogenous shocks.** COVID, FTX, regulatory events — zero lead time dari on-chain. Risk management (sizing, LTV) adalah satu-satunya proteksi.

2. **Distinguish local top vs cycle peak secara real-time.** Range overlap terlalu besar di semua 5 indikator. Yang bisa dilakukan: bearish divergence sebagai probabilistic warning, bukan definitive call.

3. **Pinpoint exact bottom atau top.** Framework identify ZONES, bukan POINTS. "Bear bottom zone" bisa berlangsung minggu-bulan. Selalu DCA, jangan lump sum.

4. **Guarantee next cycle behaves like previous ones.** n=2 sampai n=6 per rule. Structural changes (ETF, institutional) bisa mengubah behavior.

### V1.1 Planned Improvements

1. **Exchange Net Flows integration.** Terutama untuk BD1 (bull dip buy) — outflow saat dip = accumulation = bullish confirmation. Inflow saat dip = distribution = bearish.

2. **Funding Rates + Open Interest.** Derivatives sentiment sebagai additional layer, terutama di zona KUNING BAWAH yang paling ambigu.

3. **Puell Multiple.** Miner revenue cycle sebagai independent dimension yang belum covered.

4. **Backtesting framework secara simultan.** Saat ini hit rates per trigger dihitung per-KB. V1.1 harus backtest seluruh N-of-M logic secara combined terhadap historical data.

### Recalibration Protocol

Setiap kali cycle baru dimulai (Start of Bull confirmed):
1. Recalculate diminishing returns factor dari cycle peak terakhir
2. Adjust S1 thresholds (MVRV, NUPL, aSOPR) berdasarkan ~30% compression expectation
3. Document pre-detection fingerprint dari cycle ini untuk comparison
4. Update hit rates dengan data dari cycle yang baru selesai

### Patterns yang Perlu Dimonitor di Cycle Berikutnya

**1. ATH dengan SOPR MA90-MA60 gap negatif (n=1)**

Oct 2025 adalah satu-satunya ATH di dataset dimana STH-SOPR MA90 sudah di bawah MA90-MA60 saat harga membuat ATH baru. Semua ATH sebelumnya (2017, 2021, Jul 2025) masih punya gap positif. Cross-validation terhadap 4 KB lain menunjukkan Oct 2025 juga punya MVRV, NUPL, dan SOPR readings yang lebih lemah dari Jul 2025 ATH meskipun harga lebih tinggi.

Kalau pattern ini repeat di cycle berikutnya (ATH baru terjadi setelah profitability momentum sudah breakdown), ini memperkuat interpretasi bahwa ATH tersebut adalah potential cycle peak tanpa fondasi. Satu repetisi akan upgrade confidence dari "n=1 observation" ke "emerging pattern."

Monitoring: saat approaching cycle peak territory di cycle berikutnya, cek apakah MA90-MA60 gap masih positif saat ATH. Kalau negatif → treat sebagai S1 danger zone, bukan "ATH = bull still healthy."

**2. Warning time compression (30d → 22d → 6d)**

Gap peak-to-bearish-cross window menyusut setiap cycle. Di cycle berikutnya, window bisa < 5 hari. Implikasi: reduce exposure saat gap PERTAMA KALI mulai declining, jangan tunggu cross. Cross adalah confirmation yang mungkin datang terlalu lambat.

---

## CHANGELOG

- V1.0 (5 Juni 2026): Initial framework build. 6 signals defined (S1, S2, BB1, PD1, BD1, BT1) + 1 monitoring alert (LC1). Routing layer, dashboard template, risk management overlay, dan current state assessment.
- V1.0.1 (7 Juni 2026): S1 updated — trigger #6 ditambahkan (SOPR MA90-MA60 gap peak + decline, hit rate 6/6). Minimum confirmation diubah dari 3/5 ke 3/6. Danger zone note untuk ATH dengan gap negatif (n=1, Oct 2025). Signal B (bearish cross setelah local top, 3/3) ditambahkan sebagai post-S1 confirmation flow — confirm koreksi sedang berlangsung, jangan re-enter selama cross aktif. S2 updated — trigger #6 ditambahkan (Signal C: MA90 bearish cross setelah cycle peak, 2/2, timing presisi di tanggal lower high). Minimum confirmation S2 diubah dari 3/5 ke 3/6. Pattern monitoring section ditambahkan.
- V1.0.3 (8 Juni 2026): MVRV 0σ / Cum PL Price Level Framework integrated. S1 post-Signal-B flow di-replace dengan full workflow: price level crossing → duration filter (≤4d bull dip, 5-6d grey zone, 7+d bear) → latch mechanism. Backtest validated: Signal B/C selalu fire sebelum price breakdown (6/6), lead time 8-99 hari. S2 ditambah latch mechanism (bear stays confirmed post-breakdown) dan failed reclaim pattern (3/3 bear transitions). BT1 trigger #5 ditambah (grey zone breakdown + failed reclaim). LC1 item #7 ditambah (MVRV 0σ/Cum PL ratio). BD1 trigger #7 ditambah (≤4d recovery = level held as support, 11/11). Dashboard template ditambah price level tracking section.
