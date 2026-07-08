# F&G Cadence Session
*Tanggal: 29 Juni 2026*

---

## Latar Belakang

Mengeksplorasi **F&G Cadence (90D)** sebagai indikator potensial untuk framework on-chain. Referensi awal dari video YouTube "The Bitcoin Strategy That Beat DCA 10x Since 2019" oleh On-Chain Mind.

---

## Definisi Indikator

```
Cadence = Fear & Greed[today] - Fear & Greed[90 days ago]
```

Bukan level absolut F&G, tapi **rate of change (momentum) sentiment** dalam 90 hari terakhir.

- Cadence > 0 → sentiment sedang membaik vs 90 hari lalu
- Cadence < 0 → sentiment sedang memburuk vs 90 hari lalu
- Zero cross NEG→POS = momentum balik positif (BUY signal)
- Zero cross POS→NEG = momentum balik negatif (SELL signal)

**Composite strategy dari video:**
- BUY: smoothed cadence > 0 + BTC > 200D MA + F&G > 20
- SELL: immediate cadence cross below 0

---

## Eksperimen yang Dilakukan

### 1. Lower High Detection (Baseline)

**Hipotesis:** Cadence POS→NEG zero cross bisa mendeteksi Lower High confirmation.

**Script:** `analyze_fg_cadence_lower_high.py`

**Hasil:**
- Raw zero cross menghasilkan **157 sinyal bearish**
- Hanya **3% precision** untuk Lower High detection (97% false positive)
- False negative: 0% (semua LH events tertangkap, tapi dibanjiri noise)

**Kesimpulan:** Cadence tidak bisa dipakai untuk LH detection.

---

### 2. Smoothed Cadence vs SMA (Cadence crossing SMA60/SMA90)

**Script:** `analyze_fg_cadence_sma_cross.py`

**Hasil perbandingan:**

| Method | Total Signals | Precision LH |
|--------|--------------|--------------|
| Raw zero cross | 157 | 3% |
| Cadence cross below SMA60 | 171 | 3% |
| Cadence cross below SMA90 | 129 | 3% |

Tidak ada improvement. Double-confirmation (kedua SMA di hari yang sama) lebih bersih tapi tetap presisi rendah.

---

### 3. SMA60 vs SMA90 Cross (Dua SMA saling silang)

**Script:** `analyze_fg_cadence_sma_cross2.py`  
**Chart:** `fg_cadence_sma_crossover.png`

**Hasil:**
- 19 sinyal total
- 0% precision, 100% false negative
- Worst method — SMA terlalu smooth, terlalu lambat

---

### 4. State Condition (cadence < -15 AND cadence < SMA60)

**Script:** `chart_fg_cadence_state.py`  
**Chart:** `fg_cadence_state_condition.png`

**Hasil:**
- Bear State aktif hampir sepanjang semua periode bear/sideways
- Terlalu sering ON — tidak diskriminatif untuk LH spesifik

---

### 5. Exit Timing Chart (Cycle Peaks & Local Tops)

**Pivot utama sesi ini.** Cadence ternyata berguna untuk **exit timing**, bukan LH detection.

**Script:** `chart_cadence_tops.py`  
**Chart:** `fg_cadence_exit_timing.png`

**Temuan:**
- SMA60/SMA90 cadence membentuk bukit jelas di setiap Cycle Peak
- POS→NEG zero cross muncul ~2-4 minggu setelah peak (lag wajar)
- Sell signals (▼) cluster di area Local Tops dan Cycle Peaks
- Contoh konkret: cadence sell signal di Sep 2025 → sell di $111K sebelum 40% drawdown

---

### 6. Full Signal Map (Buy + Sell)

**Script:** `chart_cadence_full_signals.py`  
**Chart:** `fg_cadence_full_signals.png`

Signal dipisah oleh filter 200D MA:

| Signal | Trigger | Kondisi |
|--------|---------|---------|
| SELL | POS→NEG zero cross | — |
| BD1 buy | NEG→POS zero cross | Price > 200D MA |
| PD1/SB1 buy | NEG→POS zero cross | Price < 200D MA |

Filter 200D MA secara otomatis memisahkan BD1 dari PD1/SB1 — konsisten dengan framework yang sudah ada.

---

### 7. Clean Buy Signal Chart

**Script:** `chart_cadence_buy_signals.py`  
**Chart:** `fg_cadence_buy_signals.png`

Chart 2-panel dengan hanya ▲ BD1 (green) dan ▲ PD1/SB1 (cyan). Event lines tanpa label teks.

**Pola yang terkonfirmasi secara visual:**
- Bear market 2018-2019: cyan ▲ cluster di bottom sebelum bull run 2019
- Bull market 2019-2021: green ▲ rapi di setiap bull dip
- Bear market 2022-2023: cyan ▲ di area FTX collapse dan Pre Detection 2023
- Bull market 2024-2025: green ▲ di bull dips
- Sekarang 2025-2026: cyan ▲ mulai muncul (price masih below 200D MA)

---

### 8. Grid Search — Best SMA Pair untuk Lower High Detection

**Script:** `grid_search_cadence_sma.py`

55 kombinasi SMA (range 5–150) ditest. Metric: SMA_fast crosses below SMA_slow.

**Best pair overall (F1): SMA15 vs SMA60**

```
F1 = 0.136  |  Precision = 7.3%  |  Recall = 100%
Total signals = 41  |  TP = 3  |  FP = 38
```

**Top pairs dengan Recall 100%:**

| Rank | Fast | Slow | Total | TP | FP | Precision |
|------|------|------|-------|----|----|-----------|
| 1 | 15 | 60 | 41 | 3 | 38 | 7.3% |
| 2 | 10 | 45 | 56 | 4 | 52 | 7.1% |
| 3 | 30 | 60 | 38 | 2 | 36 | 5.3% |
| 4 | 20 | 60 | 40 | 2 | 38 | 5.0% |

**Verdict:** Tidak ada SMA pair yang bisa mendorong precision di atas ~8% untuk LH detection. Ini bukan masalah parameter — ini limitasi fundamental: cadence mengukur arah sentiment, bukan price structure.

---

## Kesimpulan Sesi

### Yang TIDAK bisa dilakukan cadence:
- Deteksi Lower High confirmation (precision max 7-8% dengan recall 100%)
- Discriminate antara general bear market dan LH-specific formation

### Yang BISA dilakukan cadence:

**Exit timing (S1/S2):**
- SMA60/SMA90 membentuk bukit visibel di cycle peaks dan local tops
- POS→NEG zero cross → confirming indicator untuk S1/S2
- Timing sinyal: lag 2-4 minggu setelah actual peak (acceptable)

**Entry signals:**
- NEG→POS zero cross + price > 200D MA → BD1 buy confirmation
- NEG→POS zero cross + price < 200D MA → PD1/SB1 buy confirmation

---

## Rekomendasi Integrasi ke Framework

| Signal | Role Cadence |
|--------|-------------|
| S1/S2 (Sell at tops) | Confirming indicator — POS→NEG cross saat cadence elevated (SMA > 0) |
| BD1 (Bull dip buy) | Trigger — NEG→POS cross AND price above 200D MA |
| PD1/SB1 (Bottom buy) | Trigger — NEG→POS cross AND price below 200D MA |
| Lower High (LH) | **Tidak dipakai** — cadence tidak cocok untuk ini |

Cadence paling kuat sebagai **satu trigger tambahan** yang konsisten di ketiga signal entry/exit, bukan sebagai standalone detector. Untuk Lower High detection, butuh metric berbasis price structure (MVRV divergence, realized price breakdown, dll).

---

## Files yang Dibuat

| File | Keterangan |
|------|-----------|
| `analyze_fg_cadence_lower_high.py` | Baseline LH detection analysis |
| `analyze_fg_cadence_sma_cross.py` | Cadence vs SMA60/SMA90 cross |
| `analyze_fg_cadence_sma_cross2.py` | SMA60 vs SMA90 crossover |
| `chart_fg_cadence_state.py` | State condition chart (4 panel) |
| `chart_cadence_tops.py` | Exit timing chart |
| `chart_cadence_full_signals.py` | Full signal map (buy + sell) |
| `chart_cadence_buy_signals.py` | Clean buy signal chart |
| `grid_search_cadence_sma.py` | Grid search 55 SMA combinations |
| `fg_cadence_sma_crossover.png` | Chart SMA cross |
| `fg_cadence_state_condition.png` | Chart state condition |
| `fg_cadence_exit_timing.png` | Chart exit timing |
| `fg_cadence_full_signals.png` | Chart full signal map |
| `fg_cadence_buy_signals.png` | Chart clean buy signals |

---

## Data Sources

- `data_fg.csv` — Fear & Greed Index harian mulai 2018-02-01
- `data_momentum_events.csv` — Event labels (LH, BB, CP, LT, PD/SB, BD)
- `data_master_all_metrics.csv` — BTC price + all metrics (untuk 200D MA)
