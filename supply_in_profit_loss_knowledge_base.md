# SUPPLY IN PROFIT & LOSS — KNOWLEDGE BASE DOCUMENT

**Version:** 1.0 | **Created:** 2026-05-31
**Data source:** ChartInspect.com (Glassnode-sourced)
**Data range:** 2017-03-01 to 2026-05-20
**Total data points:** 2,592 | **Transition events analyzed:** 55 events across 10 regime categories

---

## WHAT THESE METRICS MEASURE & WHY THEY MATTER

Supply in Profit/Loss mengukur berapa persen dari total Bitcoin supply yang saat ini dalam posisi untung atau rugi, berdasarkan harga saat coin terakhir berpindah on-chain vs harga sekarang.

Metrik ini dibagi berdasarkan holder type:

- **% Total Supply in Profit/Loss** — seluruh supply. Barometer luas kondisi market.
- **% STH (Short-Term Holder) Supply in Profit/Loss** — coin yang terakhir berpindah <155 hari lalu. Ini adalah "recent buyers" — paling sensitif terhadap pergerakan harga. STH profit/loss bergerak cepat dan volatile, mencerminkan sentimen dan pain dari partisipan terbaru.
- **% LTH (Long-Term Holder) Supply in Profit/Loss** — coin yang terakhir berpindah ≥155 hari lalu. Ini "conviction holders." LTH profit bergerak lambat dan stabil, tapi kalau mulai turun signifikan, itu berarti harga sudah di bawah cost basis dari orang-orang yang "tahan" paling lama — structural damage.

**Kenapa penting untuk cycle positioning:** Profit/loss supply adalah proxy langsung dari dua kekuatan yang menggerakkan market: (1) insentif untuk jual (take profit), dan (2) tekanan untuk jual (cut loss/capitulation). Distribusi profit/loss antara STH dan LTH memberi informasi tentang siapa yang masih hold, siapa yang sudah surrender, dan di mana tekanan jual selanjutnya bisa muncul.

**Limitasi fundamental:** Metric ini menghitung berdasarkan kapan coin terakhir berpindah on-chain. Coin yang berpindah antar wallet sendiri ter-reset. Exchange flows bisa distort. Dan yang paling penting: "in profit" tidak berarti "will sell" — banyak LTH tetap hold meskipun deep in profit.

---

## SECTION 1: HISTORICAL BEHAVIOR PER REGIME

### 1.1 CYCLE PEAK
**3 events: 2017, 2021, 2025**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Cycle Peak 2017 | $16,349 | 96.0 | 91.5 | 100.0 | 8.5 | 0.0 |
| Cycle Peak 2021 (Nov 8) | $66,027 | 96.3 | 85.2 | 99.4 | 14.8 | 0.6 |
| Cycle Peak 2025 | $123,537 | 98.6 | 93.9 | 100.0 | 6.1 | 0.0 |

**Signal fingerprint:** Total profit 96–99%, STH profit 85–94%, LTH profit ≥99%

**Leading/lagging behavior:** STH profit adalah leading indicator di semua 3 cycle peak — bergerak naik di periode 90 hari sebelumnya (3/3 leading). LTH profit tetap stabil di 99–100% (3/3 stable). Total profit mostly stable (2/3 stable) karena LTH dominan dan LTH sudah maxed out.

**Post-transition:** 90 hari setelah cycle peak, total profit turun rata-rata 14pp dan STH profit turun rata-rata 20pp. Ini konfirmasi bahwa setelah peak, recent buyers yang paling cepat terkena dampak.

**Cross-cycle observation:** Total supply in profit di cycle peak TIDAK mengalami diminishing returns — konsisten di 96–99% di semua 3 cycle. Yang berubah: STH profit di 2021 (85.2%) sedikit lebih rendah dari 2017 (91.5%) dan 2025 (93.9%), tapi ini kemungkinan lebih soal kecepatan rally ke peak daripada structural change.

**⚠️ Confidence note:** 3 data points saja. Range yang terlihat tight bisa jadi artifact dari sample size kecil.

---

### 1.2 LOCAL TOP
**6 events: Mar 2021, Apr 2021 (ATH), Mar 2024 (ATH), Des 2024 (ATH), Jan 2025 (ATH), Jul-Aug 2025 (ATH)**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Local Top Mar 2021 | $61,186 | 99.2 | 97.7 | 100.0 | 2.3 |
| Local Top Apr 2021 (ATH) | $63,551 | 99.2 | 97.6 | 100.0 | 2.4 |
| Local Top Mar 2024 (ATH) | $71,472 | 97.4 | 88.7 | 100.0 | 11.3 |
| Local Top Des 2024 (ATH) | $98,402 | 96.8 | 86.7 | 100.0 | 13.3 |
| Local Top Jan 2025 (ATH) | $99,994 | 97.2 | 89.7 | 100.0 | 10.3 |
| Local Top Jul-Aug 2025 (ATH) | $119,057 | 95.9 | 81.1 | 100.0 | 18.9 |

**Signal fingerprint:** Total profit 96–99%, STH profit 81–98%, LTH profit 100.0% (all events)

**Masalah kritis: Local Top dan Cycle Peak TIDAK bisa dibedakan dari metrik ini saja.** Range-nya overlap hampir sempurna — total profit 96–99% di keduanya, LTH profit 100% di keduanya. Supply in profit/loss TIDAK bisa menjawab "ini local top yang akan recover, atau ini the top?"

**Apa yang berbeda:** Post-transition behavior. Setelah local top, STH profit turun rata-rata 34pp dalam 90 hari (range -1.6 sampai -66.8pp). Range yang sangat lebar ini menunjukkan beberapa local top diikuti koreksi ringan (Mar 2021: hanya -1.6pp STH profit drop) sementara yang lain diikuti koreksi berat (Jul-Aug 2025 ATH: -66.8pp drop). Tapi ini baru diketahui SETELAH fakta.

**Structural shift yang terlihat:** STH profit di local top MENURUN setiap cycle peak berikutnya di cycle 2024-2025. Mar 2021: 97.7% → Des 2024: 86.7% → Jul 2025: 81.1%. Ini menunjukkan setiap ATH baru dicapai dengan porsi STH yang lebih kecil dalam profit — tanda market makin "stretched."

---

### 1.3 LOWER HIGH CONFIRM TOP CYCLE
**5 events: 2018, 2019, 2021, 2025, 2025 Confirmation**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Lower High 2018 | $13,783 | 90.1 | 78.6 | 100.0 | 21.4 |
| Lower High 2019 | $11,487 | 91.2 | 86.2 | 93.3 | 13.8 |
| Lower High 2021 | $56,995 | 85.0 | 51.1 | 95.1 | 48.9 |
| Lower High 2025 | $114,584 | 90.5 | 60.4 | 100.0 | 39.6 |
| Lower High 2025 Conf | $112,964 | 88.1 | 51.0 | 100.0 | 49.0 |

**Signal fingerprint:** Total profit **85–91%** (median 90.1%), STH profit 51–86%, LTH profit 93–100%

**Ini regime yang paling actionable untuk sell signal dari total profit.** Range total profit (85–91%) lebih rendah dari Cycle Peak (96–99%) dan Local Top (96–99%), tapi masih relatif tinggi. Gap antara total profit yang masih tinggi (85-91%) dengan STH profit yang sudah collapse (51-86%) adalah sinyal khas lower high.

**Leading/lagging:** STH profit sudah bergerak turun sebelum lower high di 3/5 events (leading). Total profit tetap stabil di 4/5 events — ini paradox penting: total profit bisa "terlihat baik-baik saja" sementara STH sudah bleeding.

**Post-transition:** Total profit turun rata-rata 8.7pp dalam 90 hari. Tapi yang krusial: ini adalah point of no return — setelah lower high terkonfirmasi, bear market decline dimulai.

**Cross-cycle shift:** Lower High 2021 dan 2025 menunjukkan STH profit yang jauh lebih rendah (51%) dibanding 2018 (78.6%) dan 2019 (86.2%). Ini mungkin karena cycle yang lebih mature memiliki lebih banyak recent buyers yang sudah underwater.

---

### 1.4 BULL DIP
**15 events across 2017–2025 — sample terbesar**

| Event | Year | Price | Total Profit | STH Profit | LTH Profit |
|-------|------|-------|:---:|:---:|:---:|
| Bull Dip Mar 2017 | 2017 | $967 | 85.2 | 51.7 | 99.2 |
| Bull Dip Jul 2017 | 2017 | $1,989 | 81.5 | 44.6 | 100.0 |
| Bull Dip Sep 2017 | 2017 | $4,423 | 91.7 | 80.2 | 100.0 |
| Bull Dip Jun 2020 | 2020 | $9,291 | 73.7 | 50.3 | 81.8 |
| Bull Dip Sep 2020 | 2020 | $10,173 | 81.3 | 54.3 | 89.7 |
| Bull Dip Jan 2021 | 2021 | $35,551 | 91.6 | 74.3 | 100.0 |
| Bull Dip Mar 2023 | 2023 | $22,429 | 61.7 | 60.8 | 61.9 |
| Bull Dip Jun 2023 | 2023 | $25,766 | 62.7 | 31.3 | 70.4 |
| Bull Dip Aug-Sep 2023 | 2023 | $26,069 | 59.9 | 10.8 | 71.7 |
| Bull Dip Jan 2024 | 2024 | $41,320 | 78.3 | 45.8 | 86.0 |
| Bull Dip Mei 2024 | 2024 | $58,341 | 81.8 | 35.0 | 97.5 |
| Bull Dip Jul 2024 | 2024 | $57,082 | 74.7 | 9.6 | 96.2 |
| Bull Dip Agt (Yen Carry) | 2024 | $58,174 | 73.0 | 5.2 | 93.7 |
| Bull Dip Sep 2024 | 2024 | $56,210 | 71.0 | 5.7 | 85.8 |
| Bull Dip Mar-Apr 2025 | 2025 | $86,294 | 77.3 | 14.7 | 100.0 |

**Signal fingerprint:** Total profit **60–92%** (median 77.3%), STH profit **5–80%** (median 44.6%), LTH profit 62–100%

**Ini adalah regime yang PALING sulit diidentifikasi dari supply metrics saja.** Range-nya sangat lebar di semua metrik — spread 32pp untuk total profit, 75pp untuk STH profit, 38pp untuk LTH profit. Artinya: supply in profit/loss TIDAK reliable sebagai standalone signal untuk mengidentifikasi bull dip.

**Structural shift lintas cycle yang jelas:** 
- **2017 bull dips:** Total profit tetap tinggi (82–92%), LTH profit 99–100%. Early bull market di mana hampir semua LTH masih deep profit.
- **2023 bull dips:** Total profit lebih rendah (60–63%), LTH profit 62–72%. Ini karena banyak LTH yang beli di 2021 masih underwater — structural hangover dari cycle sebelumnya.
- **2024 bull dips:** STH profit collapse ke single digits (5–10%) sementara LTH profit tetap tinggi (86–96%). Gap STH-LTH yang sangat besar ini adalah feature baru cycle 2024-2025.

**Pattern baru 2024-2025:** Gap antara LTH profit (tinggi, 85–100%) dan STH profit (sangat rendah, 5–15%) di bull dip adalah ciri khas cycle ini. Ini terjadi karena harga bergerak dalam range yang cukup lebar, membuat recent buyers cepat underwater sementara LTH yang beli jauh lebih rendah tetap aman.

---

### 1.5 MID-CYCLE CORRECTION
**2 events: May 2021 (start), Jun-Jul 2021 (bottom)**

| Event | Price | Total Profit | STH Profit | LTH Profit |
|-------|-------|:---:|:---:|:---:|
| Mid-Cycle Start (May 2021) | $59,074 | 96.7 | 90.6 | 100.0 |
| Mid-Cycle Bottom (Jun-Jul 2021) | $32,517 | 70.1 | 11.3 | 94.6 |

**Signal behavior:** Dari start ke bottom, total profit turun 27pp, STH profit collapse 79pp (dari 91% ke 11%), LTH profit hanya turun 5pp (100% ke 95%). Ini adalah pola "STH wipeout with LTH intact" — signature mid-cycle correction.

**⚠️ Masalah besar: Hanya 1 event (2021). Tidak ada basis untuk generalize.** Mid-cycle correction sendiri jarang terjadi — ini membuatnya sangat sulit untuk dibedakan dari start of bear market secara real-time. Di titik nadir mid-cycle 2021, metriks terlihat MIRIP dengan early bear market decline.

**Yang membedakan dari bear start:** LTH profit tetap >94% saat mid-cycle bottom — di bear decline yang sebenarnya, LTH profit mulai erode di bawah 90%. Tapi dengan hanya 1 sample, threshold ini tidak reliable.

---

### 1.6 BEAR MARKET DECLINE
**7 events across 2018, 2019, 2022, 2025, 2026**

| Event | Price | Total Profit | STH Profit | LTH Profit | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Bear Decline Start 2018 | $10,849 | 76.7 | 46.7 | 100.0 | 0.0 |
| Bear Decline Mid 2018 | $7,689 | 63.8 | 21.5 | 86.7 | 13.3 |
| Bear Decline Low 2018 | $6,604 | 59.1 | 16.6 | 77.6 | 22.4 |
| Bear Decline Mid 2019 | $10,342 | 79.4 | 52.5 | 90.7 | 9.3 |
| Bear Market Decline Mid 2022 | $46,829 | 79.1 | 64.1 | 83.6 | 16.4 |
| Bear Decline Start 2025 | $110,108 | 83.1 | 31.2 | 99.8 | 0.2 |
| Bear Market Decline Mid 2026 | $96,918 | 75.8 | 55.8 | 84.1 | 15.9 |

**Signal fingerprint:** Total profit 59–83% (median 76.7%), LTH profit 78–100%, LTH loss 0–22%

**Feature kritis: LTH profit TETAP TINGGI di awal bear market, lalu erode secara gradual.** 

Sequence khas (terlihat di 2018 dan 2025-2026):
1. Bear decline start: LTH profit masih 100% (2018) atau 99.8% (2025) → FALSE COMFORT
2. Bear decline mid: LTH profit turun ke 84–87%
3. Bear decline low: LTH profit turun ke 78%
4. Eventually → bear bottom: LTH profit 55–56%

**Ini berarti LTH profit bukan early warning untuk bear market — ia adalah lagging confirmation.** STH profit jauh lebih informatif: sudah collapse ke 31–47% di bear decline start, vs LTH yang masih 100%.

**Leading indicator pattern:** STH profit dan total profit adalah LEADING indicators di bear decline (5/7 dan 5/7 leading respectively). Mereka mulai turun 30-90 hari sebelum transition event.

---

### 1.7 BEAR BOTTOM NEAR
**7 events across 2018, 2019, 2020, 2022**

| Event | Price | Total Profit | STH Profit | LTH Profit | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Bear Bottom 2018 (Tier 1) | $3,441 | 41.5 | 5.8 | 55.8 | 44.2 |
| Bear Bottom Window End 2019 | $3,510 | 41.9 | 10.9 | 54.5 | 45.5 |
| Bear Bottom 2019 (Tier 2) | $7,187 | 58.6 | 12.0 | 75.9 | 24.1 |
| COVID Flash Crash 2020 | $5,632 | 46.6 | 11.2 | 59.0 | 41.0 |
| Bear Bottom FTX 2022 | $18,550 | 46.2 | 0.5 | 57.7 | 42.3 |
| Bear Bottom Actual Low 2022 | $15,774 | 44.5 | 0.0 | 56.2 | 43.8 |
| Bear Bottom Final Low 2022 | $16,442 | 47.9 | 18.2 | 55.8 | 44.2 |

**Signal fingerprint:** Total profit **42–59%** (median 46.2%), STH profit **0–18%** (median 10.9%), LTH profit **55–76%** (median 56.2%), LTH loss **24–46%** (median 43.8%)

**Ini adalah regime dengan signal paling konsisten dari LTH metrics.** LTH profit di 55–56% dan LTH loss di 43–45% muncul berulang di true cycle bottoms (2018, 2020, 2022). LTH pre-transition behavior: STABLE (7/7) — tidak bergerak sebelum bottom, artinya LTH profit BUKAN leading indicator untuk bottom. Ia hanya memberitahu bahwa level pain sudah cukup dalam.

**Outlier: Bear Bottom 2019 (Tier 2)** dengan LTH profit 75.9% — jauh lebih tinggi dari bottom lain. Ini karena "Tier 2" bottom di Nov 2019 sebenarnya bukan deep capitulation — harga ($7,187) masih jauh di atas 2018 low ($3,441). Ini menunjukkan tidak semua event yang dilabeli "bottom" memiliki signature yang sama.

**Post-transition recovery:** 90 hari setelah bear bottom, total profit naik rata-rata 12pp dan STH profit naik rata-rata 37pp. Recovery STH profit yang cepat ini adalah konfirmasi bahwa bottom telah berlalu — tapi hanya bisa digunakan SETELAH fakta.

**STH profit di 0%:** Terjadi 2 kali (Nov 2022: 0.5% dan 0.0%). Ini absolute capitulation — SETIAP short-term holder underwater. Secara historis, ini adalah sinyal akumulasi yang sangat kuat, tapi bisa bertahan beberapa minggu sampai bulan.

---

### 1.8 PRE DETECTION START OF BULL MARKET
**3 events: 2019 (ref), 2019, 2023**

| Event | Price | Total Profit | STH Profit | LTH Profit | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Pre Detection 2019 Ref | $3,943 | 55.9 | 58.7 | 54.8 | 45.2 |
| Pre Detection 2019 | $4,039 | 58.3 | 68.0 | 54.2 | 45.8 |
| Pre Detection 2023 | $17,444 | 59.2 | 69.6 | 56.4 | 43.6 |

**Signal fingerprint:** Total profit **56–59%**, STH profit **59–70%**, LTH profit **54–56%**, LTH loss **44–46%**

**Pattern yang sangat konsisten:** LTH profit pada 54–56% dan LTH loss pada 44–46% di semua 3 events, dengan spread hanya 2.2pp — metrik paling tight di seluruh dataset. Ini masuk akal: pre-detection terjadi saat market sudah cukup recover dari bottom sehingga STH mulai profit (59–70%), tapi LTH belum recover (masih 54–56% profit).

**Key signature: STH profit SUDAH LEBIH TINGGI dari LTH profit.** Ini counter-intuitive — biasanya LTH lebih profitable karena beli lebih rendah. Tapi di pre-detection phase, banyak LTH yang beli di cycle sebelumnya masih underwater, sementara STH yang beli di bottom sudah profit karena harga naik dari low.

**Post-transition:** Total profit naik rata-rata 14pp dalam 90 hari — transisi menuju bull confirmed.

---

### 1.9 START OF BULL MARKET CONFIRMATION
**2 events: 2019, 2023**

| Event | Price | Total Profit | STH Profit | LTH Profit | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Start of Bull 2019 | $5,249 | 64.3 | 81.4 | 57.2 | 42.8 |
| Start of Bull 2023 | $21,632 | 64.6 | 75.0 | 61.7 | 38.3 |

**Signal fingerprint:** Total profit **~64%**, STH profit **75–81%**, LTH profit **57–62%**, LTH loss **38–43%**

**Konsistensi luar biasa:** Total profit pada 64.3% dan 64.6% — spread hanya 0.3pp. Dua data points saja, tapi kemiripannya striking.

**Key transition dari Pre Detection:** STH profit naik dari 59–70% ke 75–81%, dan total profit naik dari 56–59% ke ~64%. LTH profit mulai naik (dari 54–56% ke 57–62%) tapi masih jauh dari recovery — masih 38–43% LTH supply underwater.

**Post-transition anomaly:** STH profit TURUN rata-rata 12pp setelah bull start confirmation. Ini kemungkinan karena harga rally cepat, menarik buyers baru yang kemudian mengalami pullback — awal dari pola bull dip.

**⚠️ 2 data points. Gunakan sebagai reference, bukan rule.**

---

### 1.10 UPPER RANGE RECOVERY
**3 events: 2019 (Failed), Mar 2023, Jun-Jul 2023**

| Event | Price | Total Profit | STH Profit | LTH Profit | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|
| Upper Range 2019 (Failed) | $12,830 | 95.4 | 100.0 | 93.6 | 6.4 |
| Upper Range Mar 2023 | $30,496 | 75.6 | 91.4 | 71.2 | 28.8 |
| Upper Range Jun-Jul 2023 | $30,547 | 76.0 | 85.5 | 73.6 | 26.4 |

**Outlier jelas: Upper Range 2019 (Failed)** memiliki profil yang sangat berbeda dari 2023 events — total profit 95% vs 76%, LTH profit 94% vs 71-74%. Ini karena 2019 "upper range" sebenarnya sudah near-ATH relative to the previous cycle, sementara 2023 upper range masih ~50% di bawah ATH.

**Pola 2023 lebih representatif:** STH profit tinggi (85–91%) tapi LTH profit masih suppressed (71–74%) karena banyak LTH dari cycle sebelumnya masih underwater.

---

## SECTION 2: RULE RANGES — SIGNAL THRESHOLDS

### 2A. SELL SIGNALS

**Sell events analyzed:** Cycle Peak (3) + Local Top (6) + Lower High (5) = 14 events

#### Total Supply in Profit

| Threshold | Triggered | Hit Rate | Key False Signals | Notes |
|-----------|:---------:|:--------:|-------------------|-------|
| ≥97% | 5/14 (36%) | Semua benar top events | — | Terlalu ketat — miss 9/14 sell events |
| ≥95% | 9/14 (64%) | Semua benar top events | — | Better coverage tapi masih miss lower highs |
| ≥92% | 9/14 (64%) | Semua benar | — | Same coverage sebagai 95% |
| ≥90% | 12/14 (86%) | 10 benar, 2 juga triggered di bull dip (Sep 2017: 91.7%, Jan 2021: 91.6%) | Bull dip Sep 2017 triggered → price +323% setelahnya; Bull dip Jan 2021 triggered → price +48% setelahnya | Cost of false positive: keluar terlalu cepat, miss massive upside |

**Rekomendasi:** ≥95% total profit sebagai alert, bukan automatic sell. Pada level ini, SEMUA triggered events di data adalah genuine top/local top events. Tapi hanya menangkap 64% sell events — lower highs sering di 85-91% yang tidak tertangkap.

#### STH Supply in Profit

| Threshold | Triggered | False Signal Risk |
|-----------|:---------:|-------------------|
| ≥95% | 2/14 (14%) | Sangat tight — hanya Local Top Mar & Apr 2021 |
| ≥90% | 4/14 (29%) | Low false signal, tapi miss 70% sell events |
| ≥85% | 9/14 (64%) | No false signals dari bull dips |
| ≥80% | 10/14 (71%) | 1 edge case (Bull Dip Sep 2017 at 80.2%) |

**Rekomendasi:** STH profit ≥85% sebagai sell alert lebih reliable dari total profit karena TIDAK ada bull dip yang triggered di level ini (tightest bull dip STH profit = 80.2% di Sep 2017, tapi itu border case). Avg drawdown setelah ≥85% STH profit triggered: -34.6%.

#### Combined Sell Signal (RECOMMENDED)

**Total profit ≥95% AND STH profit ≥85%:**
- Triggered di: Cycle Peak 2017, Local Top Mar 2021, Local Top Apr 2021, Local Top Mar 2024, Local Top Jan 2025, Cycle Peak 2025
- 6/14 sell events (43% coverage)
- **0 false signals dari bull dips**
- Avg drawdown after: -38%
- Trade-off: miss lower highs dan beberapa local tops, tapi setiap sinyal yang muncul historically reliable

**Total profit ≥90% AND STH profit ≥80%:**
- Higher coverage (mencakup lebih banyak sell events)
- Tapi 2 bull dip false signals (Sep 2017, Jan 2021)
- Cost of false positive: massive missed upside (323% dan 48%)

---

### 2B. BUY SIGNALS

**Buy events analyzed:** Bear Bottom (7) + Bull Dip (15) + Pre Detection (3) + Start of Bull (2) = 27 events

#### Total Supply in Profit — Buy Thresholds

| Threshold | Triggered | Avg 90d Recovery | Notes |
|-----------|:---------:|:----------------:|-------|
| ≤50% | 6/27 (22%) | +52% | Hanya bear bottom events — deep capitulation |
| ≤55% | 6/27 (22%) | +52% | Same events — no additional coverage |
| ≤60% | 11/27 (41%) | +76% | Adds pre-detection dan beberapa bull dips |
| ≤65% | 15/27 (56%) | +72% | Broader — includes start of bull events |

**⚠️ Critical caveat:** Total profit ≤50% HANYA triggered di bear bottom events di data ini — TIDAK ada false signal. Tapi timing uncertainty sangat besar: total profit bisa stay di bawah 50% selama berminggu-minggu sampai berbulan-bulan. Ini bukan "buy now" signal, ini "accumulation window open" signal.

#### STH Supply in Loss — Capitulation Buy Threshold

| Threshold | Triggered | Avg 90d Recovery | False signal risk |
|-----------|:---------:|:----------------:|-------------------|
| ≥95% | 2/27 (7%) | +42% | Ultra-tight: hanya FTX dan Actual Low 2022 |
| ≥90% | 6/27 (22%) | +45% | All bear bottoms + Yen Carry Trade dip |
| ≥85% | 11/27 (41%) | +51% | Adds several bull dips — some recovered quickly, some took months |
| ≥80% | 12/27 (44%) | +52% | Adds Bear Bottom Final Low |

**Rekomendasi:** STH loss ≥90% sebagai strong buy signal — 6 triggers, semua followed by recovery, tapi timing varies dari days to months.

#### Combined Buy Signal (RECOMMENDED)

**Total profit ≤50% AND STH loss ≥90%:**
- Triggered di: Bear Bottom 2018 Tier 1, FTX Collapse, Actual Price Low 2022
- 3 events — semua absolute cycle bottoms
- **Perfect historical hit rate, tapi 3 data points**
- Signals yang muncul adalah extreme capitulation — timing window masih uncertain tapi quality sangat tinggi

**Total profit ≤60% AND STH profit ≤15%:**
- Broader coverage
- Adds: Bear Bottom events, beberapa extreme bull dips (Jul 2024, Agt 2024, Sep 2024)
- Bull dip additions recovered +7 to +85% dalam 90d

---

## SECTION 3: METRIC INTERACTIONS

### 3A. STH vs LTH Divergence — Pattern Utama

**Pattern 1: LTH profit tinggi, STH profit collapse (Gap >50pp)**

Ini adalah divergence pattern paling sering muncul — 14 instances di data. Interpretasinya BUKAN satu-arah:

| Outcome | Count | Events |
|---------|:-----:|--------|
| Followed by recovery (bull dip/mid-cycle) | 9/14 | Jul 2017 (+112%), Mid-Cycle Bottom 2021 (+88%), Sep 2024 (+85%), Aug 2024 (+53%), etc |
| Followed by continued decline (bear) | 3/14 | Bear Decline Start 2018 (-38%), Bear Bottom 2019 Tier 2 (-7%), Bear Decline Start 2025 (-34%) |
| Sideways | 2/14 | Halving 2024 (-0.1%), Mei 2024 (+16%) |

**Takeaway:** LTH high + STH low divergence sendiri BUKAN bearish atau bullish signal. Harus dikombinasikan dengan arah pergerakan LTH profit: jika LTH profit STABIL (tetap >95%), kemungkinan besar bull dip. Jika LTH profit MULAI TURUN, lebih mungkin bear transition.

**Pattern 2: Both STH dan LTH profit rendah (capitulation)**

| Event | LTH Profit | STH Profit | Total Profit | 90d After |
|-------|:---:|:---:|:---:|:---:|
| Bear Bottom 2018 | 55.8 | 5.8 | 41.5 | +15% |
| Bear Bottom Window End | 54.5 | 10.9 | 41.9 | +52% |
| COVID Flash Crash | 59.0 | 11.2 | 46.6 | +67% |
| FTX Collapse | 57.7 | 0.5 | 46.2 | +25% |
| Actual Price Low | 56.2 | 0.0 | 44.5 | +54% |
| Final Low 2022 | 55.8 | 18.2 | 47.9 | +61% |

**Semua 6 events followed by recovery.** LTH profit <60% + STH profit <20% = true capitulation territory. Hit rate 6/6 tapi durasi di bottom bervariasi — 2018 bottom berlangsung beberapa bulan, 2022 bottoming process juga ~6 minggu.

### 3B. Pre Detection Divergence — Signal Unik

Di fase Pre Detection, terjadi crossover di mana **STH profit > LTH profit:**

| Event | STH Profit | LTH Profit | Gap |
|-------|:---:|:---:|:---:|
| Pre Detection 2019 Ref | 58.7 | 54.8 | STH +3.9 |
| Pre Detection 2019 | 68.0 | 54.2 | STH +13.8 |
| Pre Detection 2023 | 69.6 | 56.4 | STH +13.2 |

**Ini terjadi karena STH (recent buyers di bottom) sudah profit sementara LTH (buyers dari cycle sebelumnya) masih underwater.** Pattern ini HANYA muncul di pre-detection phase — ini potential leading indicator yang unik.

### 3C. Concordance vs Divergence Summary

| Regime | STH-LTH Concordant | STH-LTH Divergent | Interpretation |
|--------|:------------------:|:------------------:|----------------|
| Start of Bull | 2/2 (100%) | 0/2 | Semua bergerak sejalan — broad-based recovery |
| Bull Dip | 9/15 (60%) | 6/15 | Mixed — divergence sering karena LTH stable sementara STH collapse |
| Bear Market Decline | 4/7 (57%) | 3/7 | Divergence terjadi di early bear (LTH stable, STH falling) |
| Bear Bottom Near | 2/7 (29%) | 5/7 | Dominan divergent — STH mulai recover sementara LTH masih turun |
| Pre Detection | 0/3 (0%) | 3/3 | Selalu divergent — STH naik, LTH masih turun/stable |
| Cycle Peak | 1/3 (33%) | 2/3 | LTH maxed out (stable), STH volatile |

**Takeaway:** Divergence pola STH naik + LTH turun/stable muncul di Bear Bottom → Pre Detection → Start of Bull sequence. Ini adalah recovery signature. Divergence pola STH turun + LTH stable muncul di Cycle Peak → Lower High → Bear Decline sequence. Ini adalah topping signature.

---

## SECTION 4: FAILURE MODES

### 4A. Total Supply in Profit — Kapan Gagal

**False sell signals (total profit tinggi tapi bukan top):**

| Event | Total Profit | Actual Regime | Price 90d After | Cost of Error |
|-------|:---:|-------------|:---:|---------------|
| Bull Dip Sep 2017 | 91.7 | Bull Dip | +323% | Massive missed upside |
| Bull Dip Jan 2021 | 91.6 | Bull Dip | +48% | Significant missed upside |

**Kenapa gagal:** Di early/mid bull market, total profit bisa tetap tinggi (>90%) karena hampir semua supply masih in profit dari accumulation di bear. Koreksi 10-15% muncul sebagai bull dip, bukan distribusi, tapi total profit sudah di level yang "seharusnya" concerning.

**Kapan unreliable:** Total supply in profit PALING unreliable saat membedakan antara bull dip dan cycle peak — keduanya bisa show 90%+ total profit. Metrik ini juga tidak berguna untuk membedakan local top dari cycle peak — range overlap total.

**False buy signals (total profit rendah tapi belum bottom):**
Dari data yang tersedia, TIDAK ada false buy signal di bawah 50% — setiap kali total profit turun di bawah 50%, itu adalah genuine bear bottom zone. Tapi caveat: data hanya mencakup 3-4 cycle.

---

### 4B. STH Supply in Profit — Kapan Gagal

**STH adalah metrik paling volatile — dan karena itu paling sering memberikan sinyal ambiguous.**

**False bottom: STH profit near 0% tapi bukan actual bottom:**

| Event | STH Profit | Regime | What Happened |
|-------|:---:|--------|---------------|
| FTX Collapse (Nov 8, 2022) | 0.5% | Bear Bottom | Price dropped FURTHER to $15,774 (actual low Nov 21) → FALSE bottom |
| Bull Dip Agt 2024 | 5.2% | Bull Dip | Price dropped further -7% before recovering → temporary false bottom |

**Kenapa gagal:** STH profit bisa hit 0% di cascade liquidation event (FTX) sementara harga belum selesai turun. STH profit 0% menunjukkan semua recent buyers underwater, tapi BUKAN berarti semua selling pressure sudah habis — bisa ada forced liquidation dan panic selling lanjutan.

**STH noise level:** STH profit bisa bergerak 50+pp dalam seminggu. Di Jul 2017, STH profit bergerak dari 59% ke 39% dalam 5 hari, lalu kembali ke 91% dalam 3 hari setelahnya. Ini membuat daily readings unreliable — smoothing (7-day average) lebih berguna.

---

### 4C. LTH Supply in Profit — Kapan Gagal

**LTH profit memberikan FALSE COMFORT di early bear market:**

| Phase | LTH Profit | Price | Apa Yang Terjadi |
|-------|:---:|-------|------------------|
| Bear Start 2018 | 100.0% | $10,849 | LTH semua masih profit → "everything is fine" |
| Bear Mid 2018 | 86.7% | $7,689 | Baru mulai turun — sudah -30% dari peak |
| Bear Low 2018 | 77.6% | $6,604 | -40% dari peak, LTH masih 78% profit |
| Bear Start 2025 | 99.8% | $110,108 | Hampir identik — LTH all profit saat bear dimulai |
| Bear Mid 2026 | 84.1% | $96,918 | LTH masih 84% profit, tapi sudah -22% dari peak |

**Ini adalah failure mode terpenting dari LTH profit:** Karena LTH membeli di harga jauh lebih rendah (seringkali 1-2 cycle sebelumnya), LTH profit tetap tinggi JAUH ke dalam bear market. Investor yang hanya melihat LTH profit >90% bisa merasa "aman" sementara harga sudah turun 30%+.

**LTH profit baru mulai memberikan sinyal meaningful (turun ke <60%) saat bear market sudah advanced — ini terlalu lambat untuk protective action.**

**Structural shift potensial untuk cycle berikutnya:** Cycle 2025-2026 menunjukkan LTH profit turun lebih cepat (dari 100% ke 65% dalam ~7 bulan, per data terbaru Mei 2026) dibanding 2018 (dari 100% ke 56% dalam ~12 bulan). Ini bisa karena lebih banyak coin yang dibeli di high prices sudah mature menjadi LTH status — structural change yang bisa membuat historical thresholds kurang reliable.

---

### 4D. Metric Reliability Ranking

Berdasarkan konsistensi range di dalam regime yang sama (lower = tighter range = more reliable):

| Rank | Metric | Avg Spread Within Regime | Verdict |
|:----:|--------|:------------------------:|---------|
| 1 | LTH Profit | 12.4pp | **Most reliable** — consistent ranges per regime |
| 2 | LTH Loss | 12.4pp | Mirror of LTH profit — same reliability |
| 3 | Total Profit | 13.5pp | Moderate — useful but overlapping ranges across regimes |
| 4 | Total Loss | 13.5pp | Mirror of total profit |
| 5 | STH Profit | 31.2pp | **High variance** — ranges too wide for standalone use |
| 6 | STH Loss | 31.2pp | Mirror of STH profit — same high variance |

**Implikasi untuk signal framework:** LTH metrics sebagai anchor/context (di mana kita dalam big picture), total metrics sebagai primary signal, STH metrics sebagai confirming/divergence indicator. Jangan pernah trade STH signals alone.

---

## SECTION 5: REGIME MAPPING — QUICK REFERENCE

### Decision Matrix

| Regime | Total Profit | STH Profit | LTH Profit | Confidence |
|--------|:---:|:---:|:---:|:---:|
| **Cycle Peak** | 96–99% | 85–94% | ≥99% | ⚠️ Can't distinguish from Local Top |
| **Local Top** | 96–99% | 81–98% | 100% | ⚠️ Same as Cycle Peak |
| **Lower High** | 85–91% | 51–86% | 93–100% | ✅ Total profit gap vs peak visible |
| **Bull Dip** | 60–92% | 5–80% | 62–100% | ❌ Too wide — need other indicators |
| **Mid-Cycle Correction** | 70–97% | 11–91% | 95–100% | ❌ Only 1 event |
| **Bear Market Decline** | 59–83% | 17–64% | 78–100% | ⚠️ LTH misleading early |
| **Bear Bottom Near** | 42–59% | 0–18% | 55–76% | ✅ LTH <60% strong signal |
| **Pre Detection** | 56–59% | 59–70% | 54–56% | ✅ Very tight range, STH > LTH |
| **Start of Bull** | ~64% | 75–81% | 57–62% | ✅ Very tight (2 events) |

### When to Give These Metrics HIGH Weight

- **Bear Bottom identification:** Total profit <50% + LTH profit <60% + STH profit <10% → strong accumulation signal
- **Pre Detection / Start of Bull:** STH profit > LTH profit → unique signal, very tight ranges
- **Lower High identification:** Total profit drop dari >95% ke 85-91% sementara harga di dekat previous highs

### When to Give These Metrics LOW Weight

- **Distinguishing Local Top vs Cycle Peak:** Overlapping ranges → useless alone
- **Bull Dip identification:** Ranges terlalu lebar → need valuation metrics (MVRV, NUPL) as primary
- **Early bear market warning:** LTH profit stays high → misleading comfort
- **Timing:** Semua metrik ini bisa stay di extreme levels for weeks/months

### RED FLAGS — Immediate Attention Triggers

1. **LTH profit declining from 100% dengan kecepatan >5pp/bulan** → structural bear indicator, bukan noise
2. **Total profit drop >10pp dalam 2 minggu** → rapid regime change, reassess everything
3. **STH profit ≤5% untuk >2 minggu** → deep capitulation, tapi bisa lebih dalam lagi (FTX false bottom)
4. **STH profit > LTH profit** saat total profit <65% → pre-detection signature, potential bull start
5. **Total profit >95% tapi STH profit trending down** → distribution happening, smart money exiting to retail

---

## SECTION 6: CURRENT STATE ANALYSIS (Per 20 Mei 2026)

| Metric | Current Value | Nearest Regime Match |
|--------|:---:|----------------------|
| Total Profit | 61.9% | Between Pre Detection (56-59%) and Start of Bull (64%) |
| STH Profit | 47.4% | Moderate — between bear decline and bull dip ranges |
| LTH Profit | 65.3% | Below Start of Bull (57-62%) BUT declining trend from 100% |
| LTH Loss | 34.7% | Approaching Start of Bull range (38-43%) from above |

**Interpretive note (requires confidence caveat):** Berdasarkan mapping murni ke historical ranges, current metrics paling dekat dengan zona antara Bear Market Decline dan Start of Bull territory. Tapi ini interpretasi yang HARUS dikombinasikan dengan:
1. Arah pergerakan (trending): LTH profit MASIH TURUN → belum bottoming
2. Speed of decline: LTH profit turun dari 100% ke 65% dalam ~7 bulan — faster than 2018
3. Valuation metrics (MVRV, NUPL) untuk context
4. Total profit 62% belum mencapai historical Pre Detection level (56-59%)

**⚠️ Ini BUKAN call bahwa bottom dekat atau jauh. Ini positioning information.** Total profit masih 3-4pp di atas Pre Detection range, dan LTH profit masih 9pp di atas Pre Detection range. Jika trajectory saat ini berlanjut, Pre Detection zone bisa tercapai dalam beberapa bulan — tapi trajectory bisa berubah.

---

## SECTION 7: WHAT COULD MAKE HISTORICAL THRESHOLDS INVALID

1. **ETF structural change:** Bitcoin ETFs mengubah ownership structure. Coin yang di-hold via ETF mungkin tidak berpindah on-chain saat dijual, membuat supply-in-profit calculation less representative. Jika significant portion of supply ada di ETFs, metric bisa overstate "in profit" karena coin-coin ini jarang bergerak on-chain.

2. **Higher base of institutional holders:** Jika cycle ini memiliki proporsi institutional buyers yang lebih besar, LTH profit threshold di bear bottom (55-56%) mungkin tidak tercapai — institutions mungkin hold longer, membuat LTH profit tetap lebih tinggi di bottom.

3. **Faster LTH maturation:** Coin yang dibeli di $90K-$125K akan mature menjadi LTH status setelah 155 hari. Ini berarti LTH loss bisa meningkat lebih cepat dari historical precedent jika harga tetap di bawah level tersebut — bisa membuat LTH loss lebih "noisy" di cycle ini.

4. **Cycle length uncertainty:** Jika cycle ini lebih pendek atau lebih panjang dari precedent, semua timing-based interpretations dari pre/post transition dynamics bisa off.

5. **Multi-peak vs single-peak structure:** 2021 menunjukkan double-top. 2025 menunjukkan multi-local-top structure. Jika future cycles juga multi-peak, "Cycle Peak" signal ranges bisa shift karena distribution happens more gradually.

---

## APPENDIX: CONFIDENCE LEVELS

| Section | Confidence | Reason |
|---------|:----------:|--------|
| Bear Bottom signals (LTH <60%, Total <50%) | **HIGH** | 6/6 confirmed across 3 cycles |
| Pre Detection / Start of Bull signals | **MEDIUM-HIGH** | Very tight ranges tapi hanya 2-3 events |
| Cycle Peak signals | **MEDIUM** | 3 events, consistent tapi small sample |
| Lower High signals | **MEDIUM** | 5 events, good consistency pada total profit |
| Bull Dip signals | **LOW** | 15 events tapi ranges terlalu lebar — unreliable standalone |
| STH-based signals overall | **LOW-MEDIUM** | High variance, best used as confirming indicator |
| Future cycle applicability | **UNCERTAIN** | ETF structural change, faster LTH maturation |
