# SOPR Family Knowledge Base: aSOPR, LTH-SOPR, STH-SOPR

**Versi:** 1.3
**Tanggal terakhir update:** 7 Juni 2026
**Data source:** ChartInspect.com (Glassnode-sourced)
**Coverage:** Maret 2017 – Mei 2026 (3 cycle: 2017, 2021, 2025-current)
**Status:** DRAFT — perlu iterasi setelah cross-check dengan indikator lain

**Changelog:**
- v1.0 — Dokumen awal: historical behavior, rule ranges, failure modes, regime mapping
- v1.1 — Tambah Bagian 8: SMA15 divergence analysis (regular & hidden bull div)
- v1.2 — Tambah Bagian 9: aSOPR EMA/SMA optimal crossover (EMA55/SMA35). Tambah Bagian 10: LTH/STH ratio zones & five divergence states framework
- v1.3 — Tambah Bagian 11: STH-SOPR MA90 / MA90-MA60 gap-and-cross framework. Include bull trap thesis (Jul 2025 sebagai structural cycle peak vs Oct 2025 bull trap)

---

## BAGIAN 1: HISTORICAL BEHAVIOR PER REGIME TRANSITION

### 1.1 CYCLE PEAK

**Events dalam data:** Cycle Peak 2017 (Des 8–19), Cycle Peak 2021 Nov 8 (Okt 20 – Nov 9), Cycle Peak 2025 (Okt 5–7)

**Nilai di transition date:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|---|---|---|---|---|
| Peak 2017 (first day) | $16,349 | 1.177 | 16.48 | 1.135 |
| Peak 2021 (first day) | $66,027 | 1.073 | 1.90 | 1.051 |
| Peak 2025 (first day) | $123,537 | 1.025 | 2.24 | 1.008 |

**Aggregate across all peak dates:** aSOPR avg 1.068, median 1.060 | LTH-SOPR avg 7.68, median 2.52 | STH-SOPR avg 1.041, median 1.026

**Pre-transition behavior (30 hari sebelum):**

Cycle Peak 2017 — aSOPR avg 1.066, trend RISING. STH-SOPR avg 1.036, trend RISING. Pola yang jelas: sustained elevation above 1.05 di kedua metrik, dengan beberapa spike aSOPR di atas 1.15.

Cycle Peak 2021 — aSOPR avg 1.030, trend RISING. STH-SOPR avg 1.017, trend RISING. Jauh lebih subdued dibanding 2017 — diminishing euphoria signal.

Cycle Peak 2025 — aSOPR avg 1.024, trend RISING. STH-SOPR avg 1.004, trend RISING. Bahkan lebih compressed lagi. aSOPR hampir tidak pernah tembus 1.05 secara sustained.

**Post-transition behavior (30 hari setelah):**

2017: aSOPR drop tajam ke range 0.90–1.05 dalam 2 minggu, tapi bounce besar masih terjadi (Jan 2018 lower high saw aSOPR kembali ke 1.13). STH-SOPR collapse ke bawah 0.97 pada 22 Des ($13,833).

2021: aSOPR drop ke 1.02 range dalam 2 minggu, kemudian oscillate antara 0.98–1.07. STH-SOPR drop ke bawah 0.97 pada Nov 26 ($53,719) — lebih cepat dari 2017.

2025: aSOPR drop ke 0.987 pada Okt 10 (BTC turun dari $124K ke $113K), kemudian partial recovery ke 1.01–1.03 range sebelum lower high.

**Pola konsisten lintas cycle:**
- aSOPR dan STH-SOPR selalu RISING di 30 hari sebelum peak
- LTH-SOPR sangat volatile dan spike-driven — tidak reliable sebagai standalone signal
- Peak VALUES menurun setiap cycle (diminishing returns yang sangat jelas)

**Perubahan dari cycle ke cycle:**
- **CRITICAL — aSOPR peak values menurun drastis:** 2017 avg 1.124, 2021 avg 1.039, 2025 avg 1.043. Threshold yang bekerja di 2017 (misalnya "sell saat aSOPR > 1.10") akan miss 2021 dan 2025 peaks sepenuhnya.
- LTH-SOPR drop dari rata-rata 18.27 (2017) ke 2.40 (2021) ke 2.32 (2025). Ini structural — semakin banyak coins yang sudah terdistribusi, semakin kecil profit multiplier.
- STH-SOPR juga compressed: 2017 avg 1.089, 2021 avg 1.018, 2025 avg 1.007. Market semakin efficient.

---

### 1.2 LOCAL TOP

**Events dalam data:** Local Top Mar 2021 (2 hari), Local Top Apr 2021 ATH (3 hari), Local Top Mar 2024 ATH (4 hari), Local Top Des 2024 ATH (26 hari), Local Top Jan 2025 ATH (14 hari), Local Top Jul-Aug 2025 ATH (33 hari)

**Nilai aggregate:**
aSOPR: min 1.004, max 1.212, avg 1.051, median 1.041
LTH-SOPR: min 1.352, max 13.307, avg 2.838, median 2.349
STH-SOPR: min 0.992, max 1.196, avg 1.021, median 1.013

**Pre-transition behavior:**
Sebelum local tops, pola yang dominan: aSOPR trend RISING di 5 dari 6 events. STH-SOPR lebih mixed — RISING di 3, DECLINING di 3. Ini menunjukkan aSOPR lebih reliable sebagai leading indicator untuk local tops.

**Pola yang konsisten:**
- aSOPR sustained di atas 1.03–1.05 selama 1–2 minggu sebelum local top
- STH-SOPR di atas 1.01 selama beberapa hari berturut-turut
- LTH-SOPR spike besar (>3.0) sering muncul 1–3 hari sebelum puncak — ini tanda distribusi heavy oleh long-term holders

**Pola yang BERUBAH:**
- Local tops 2024–2025 punya aSOPR peaks yang lebih rendah dari 2021. Apr 2021 peak aSOPR = 1.087, Mar 2024 peak aSOPR = 1.212 (anomali — spike satu hari), tapi median values lebih rendah.
- Jul-Aug 2025 ATH menunjukkan local top yang "lama" — 33 hari dengan aSOPR rata-rata hanya 1.031. Ini membuat timing sangat sulit karena tidak ada spike tajam.

---

### 1.3 BULL DIP

**Events dalam data:** 14 bull dip events dari 2017 sampai 2025

**Nilai aggregate:**
aSOPR: min 0.942, max 1.105, avg 1.009, median 1.003
LTH-SOPR: min 0.759, max 8.175, avg 2.108, median 1.553
STH-SOPR: min 0.917, max 1.085, avg 0.995, median 0.995

**Pre-transition behavior:**
11 dari 14 bull dips menunjukkan aSOPR trend DECLINING sebelum dip. STH-SOPR trend DECLINING di 10 dari 14. Ini signal yang cukup reliable — profit-taking menurun menjelang dip karena holders mulai ragu.

**Pola di transition date:**
- STH-SOPR di bawah 1.0 adalah signature paling konsisten — terjadi di 12 dari 14 events (hit rate 86%)
- aSOPR bisa tetap di atas 1.0 bahkan di bull dip karena LTH profits masih masuk
- LTH-SOPR sangat volatile dan tidak bisa dijadikan standalone signal

**Post-transition recovery:**
- aSOPR bounce kembali ke atas 1.02 dalam 5–10 hari di bull dips yang genuine
- STH-SOPR reclaim 1.0 dalam 3–7 hari — ini konfirmasi recovery
- Bull dip yang GAGAL recover: Mid-Cycle Correction 2021 — STH-SOPR tetap di bawah 1.0 selama berminggu-minggu

**Variasi antar cycle:**
- 2017 bull dips: STH-SOPR bisa turun ke 0.93–0.95 (severe)
- 2020-2021 bull dips: STH-SOPR dip ke 0.96–0.98 (moderate)
- 2024-2025 bull dips: STH-SOPR dip ke 0.95–0.98, tapi Mar-Apr 2025 punya yang extended (35 hari, paling lama dalam dataset)

---

### 1.4 MID-CYCLE CORRECTION

**Events:** Mid-Cycle Correction Start (Mei 2021, 1 hari), Mid-Cycle Correction Bottom (Jun-Jul 2021, 30 hari)

**Start (Mei 8, 2021): BTC $59,074**
aSOPR: 1.045 | LTH-SOPR: 7.09 | STH-SOPR: 1.031

Pre-30d aSOPR trend: RISING (avg 1.043). Tidak ada warning yang jelas dari SOPR family — semua metrik masih "sehat". Ini adalah FAILURE MODE paling penting: mid-cycle correction tidak memberikan advance warning dari profitability metrics.

**Bottom (Jun 22 – Jul 21, 2021): BTC $29,837–$35,888**
aSOPR: min 0.867, avg 0.993 | STH-SOPR: min 0.859, avg 0.976

Bottom ditandai oleh:
- aSOPR multiple days di bawah 1.0 (sustained capitulation)
- STH-SOPR sustained di bawah 0.98 — short-term holders rugi secara persistent
- LTH-SOPR tetap di atas 2.0 kebanyakan waktu — long-term holders masih profit bahkan saat harga turun 50%

**Perbedaan dari bull dip biasa:**
- Durasi: 30+ hari vs 4–17 hari untuk bull dip
- Severity: STH-SOPR di bawah 0.96 secara sustained vs brief dip ke 0.96–0.98
- aSOPR: multiple days berturut-turut di bawah 1.0 vs biasanya 1–3 hari

---

### 1.5 LOWER HIGH CONFIRM

**Events:** Lower High 2018 (Jan 1–8), Lower High 2019 (Aug 6–8), Lower High 2021 (Nov 30 – Des 2), Lower High 2025 (Okt 26–28)

**Aggregate:**
aSOPR: avg 1.056, median 1.057
LTH-SOPR: avg 9.52, median 2.52 (skewed oleh outlier 54.82 dari Jan 7, 2018)
STH-SOPR: avg 1.027, median 1.029

**Pre-transition behavior:**
- aSOPR trend DECLINING di 4 dari 4 events — ini signal penting. Sebelum lower high, profitability sudah mulai turun meskipun harga naik. Divergence ini adalah red flag.
- STH-SOPR juga DECLINING di 3 dari 4 events
- Pattern: harga naik tapi profit yang direalisasikan menurun = distribusi tanpa conviction baru

**Nilai pada transition date vs cycle peak:**
- 2018: Lower high aSOPR avg 1.075 vs peak avg 1.124 — turun 4%
- 2021: Lower high aSOPR avg 1.006 vs peak avg 1.039 — turun 3%
- 2025: Lower high aSOPR avg 1.027 vs peak avg 1.043 — turun 2%

Patterns semakin compressed tapi ratio-nya konsisten: lower high SELALU punya aSOPR lebih rendah dari cycle peak meskipun harga bisa setara atau lebih tinggi.

---

### 1.6 BEAR BOTTOM NEAR

**Events:** Bear Bottom 2018 Tier 1 (Des 11–17), Bear Bottom Window End 2019 (Jan 30 – Feb 6), Bear Bottom 2019 Tier 2 (Nov 25 – Des 18), COVID Flash Crash (Mar 13–17 2020), FTX Collapse (Nov 8, 2022), Actual Price Low (Nov 21, 2022), Final Low (Des 19, 2022)

**Aggregate:**
aSOPR: min 0.821, max 1.006, avg 0.960, median 0.968
LTH-SOPR: min 0.343, max 1.964, avg 0.831, median 0.795
STH-SOPR: min 0.912, max 1.000, avg 0.971, median 0.974

**Signature yang paling reliable:**
- aSOPR di bawah 0.95 = strong capitulation signal (terjadi di semua bear bottom events)
- LTH-SOPR di bawah 0.50 = deep capitulation bahkan oleh long-term holders (terjadi di 2018 dan 2022 bottoms)
- STH-SOPR di bawah 0.96 secara sustained = market-wide loss realization

**Pre-transition behavior:**
aSOPR trend DECLINING di 4 dari 7 events. Tapi 3 events (Bear Bottom Window End, FTX Collapse, Final Low) menunjukkan aSOPR trend RISING sebelumnya — ini karena ada relief rally sebelum bottom final.

**Post-bottom recovery signature:**
- aSOPR reclaim 1.0 secara sustained (5+ hari berturut-turut) = bottom sudah terbentuk
- STH-SOPR reclaim 1.0 biasanya mendahului aSOPR — ini signal bahwa new buyers mulai in profit
- LTH-SOPR sangat lambat untuk recover — bisa butuh berbulan-bulan

---

### 1.7 PRE DETECTION START OF BULL & START OF BULL CONFIRMATION

**Pre Detection events:** Pre Detection 2019 Ref (Feb 22), Pre Detection 2019 (Mar 21–26), Pre Detection 2023 (Jan 10–12)

**Start of Bull events:** Start of Bull 2019 (Apr 25), Start of Bull 2023 (Feb 10–12)

**Pre Detection signature:**
aSOPR: avg 0.985, median 0.984 — masih di bawah 1.0
LTH-SOPR: avg 0.577, median 0.574 — LTH masih rugi
STH-SOPR: avg 1.005, median 1.004 — STH mulai balik profit DULUAN

Ini adalah divergence kunci: **STH-SOPR reclaim 1.0 sementara aSOPR dan LTH-SOPR masih di bawah.** STH buyers yang beli di near-bottom sudah profit — signal bahwa bottom sudah in dan momentum mulai bergeser.

**Start of Bull signature:**
aSOPR: avg 0.991, median 0.993 — mendekati 1.0 tapi belum sustained di atas
LTH-SOPR: avg 0.742, median 0.770 — masih rugi
STH-SOPR: avg 0.998, median 1.002 — oscillating di sekitar 1.0

**Pola transisi Pre Detection → Start of Bull:**
1. STH-SOPR reclaim 1.0 (Pre Detection)
2. aSOPR bergerak dari bawah 0.98 ke sekitar 1.0 (Start of Bull)
3. LTH-SOPR masih di bawah 1.0 tapi trending up (lagging)
4. Setelah Start of Bull confirmed, aSOPR sustained di atas 1.0 dalam 2–4 minggu

---

## BAGIAN 2: RULE RANGES — PROPOSED SIGNAL THRESHOLDS

### 2.1 SELL SIGNALS (Early Detection untuk Tops)

#### Rule S1: aSOPR 7-day average > 1.05

**Rationale:** Sustained high profitability menunjukkan euphoria dan distribusi.

**Backtesting:**
- 2017 Cycle Peak: TRIGGERED — 7d avg mencapai 1.10+ di awal Desember. ~7 hari sebelum ATH. ✅
- 2021 Cycle Peak: TRIGGERED — 7d avg mencapai 1.05+ di late Oktober. ~14 hari sebelum ATH. ✅
- 2025 Cycle Peak: NOT TRIGGERED — 7d avg hanya mencapai 1.04. ❌ FALSE NEGATIVE
- Local Top Apr 2021: TRIGGERED ✅
- Local Top Mar 2024: TRIGGERED ✅
- Local Top Des 2024: TRIGGERED ✅
- Local Top Jul-Aug 2025: NOT TRIGGERED — 7d avg hanya 1.031. ❌ FALSE NEGATIVE

**Hit rate:** 5/7 = 71%
**False negatives:** 2/7 = 29% — keduanya di cycle terbaru (2025), menunjukkan diminishing signal
**Cost of false negative:** Kalau tidak sell saat threshold tidak triggered, miss timing. Cycle Peak 2025 diikuti drop 15% dalam 2 minggu. Local Top Jul-Aug 2025 diikuti stagnasi tapi bukan crash besar.

**VERDICT:** Threshold ini terlalu tinggi untuk 2025 cycle. Perlu adjusted down ke 1.03–1.04 range, tapi ini akan meningkatkan false positives secara signifikan.

#### Rule S2: STH-SOPR 7-day average > 1.03

**Rationale:** Short-term holders taking profit secara konsisten = market mendekati local exhaustion.

**Backtesting:**
- 2017 Cycle Peak: TRIGGERED — STH avg 1.089 selama peak. ✅
- 2021 Cycle Peak: TRIGGERED — STH avg 1.018 (marginal). ✅ tapi barely
- 2025 Cycle Peak: NOT TRIGGERED — STH avg 1.007. ❌ FALSE NEGATIVE
- Local Top Des 2024: TRIGGERED — STH spike ke 1.098. ✅
- Local Top Jan 2025: TRIGGERED — STH avg 1.013 (marginal). ✅ tapi barely
- Local Top Jul-Aug 2025: NOT TRIGGERED — STH avg 1.009. ❌ FALSE NEGATIVE

**Hit rate:** 4/6 = 67%
**False negatives dari 2025 cycle:** Konfirmasi bahwa market semakin efficient dan thresholds historis tidak lagi berlaku tanpa adjustment.

**CRITICAL OBSERVATION:** Kalau threshold diturunkan ke STH > 1.01, hit rate naik ke 6/6 tapi false positive rate juga naik signifikan — setiap bounce kecil akan trigger.

#### Rule S3: LTH-SOPR spike > 5.0 (single day)

**Rationale:** Spike besar menunjukkan long-term holders melakukan distribusi besar.

**Backtesting:**
- 2017 Peak: 9 hari dengan LTH > 5.0 selama peak period. ✅ LEADING by 2-3 hari
- 2021 Peak: hanya 1 hari (Okt 31) dengan LTH > 5.14. ✅ tapi not sustained
- 2025 Peak: 0 hari dengan LTH > 5.0. ❌ FALSE NEGATIVE
- Local Top Apr 2021: LTH spike ke 13.3 (Apr 14). ✅ STRONG signal
- Local Top Jan 2025: LTH spike ke 4.92 dan 5.57. ✅ near threshold

**Hit rate:** 3/5 = 60%
**Problem besar:** LTH-SOPR sangat noisy. Spike > 5.0 juga terjadi selama bull dips yang bukan top (mis. Jan 2021 bull dip saw LTH = 5.35). False positives terlalu banyak.

**VERDICT:** Jangan pakai sebagai standalone signal. Hanya sebagai konfirmasi bersama aSOPR dan STH.

---

### 2.2 BUY SIGNALS (Early Detection untuk Bottoms & Dips)

#### Rule B1: STH-SOPR < 0.97 (sustained 3+ hari)

**Rationale:** Short-term holders rugi signifikan = panic selling, potensi oversold.

**Backtesting untuk Bull Dips:**
- Bull Dip Mar 2017: STH turun ke 0.944. TRIGGERED. Recovery dalam 9 hari. ✅
- Bull Dip Jul 2017: STH turun ke 0.931. TRIGGERED. Recovery dalam 5 hari. ✅
- Bull Dip Jan 2021: STH turun ke 0.960. TRIGGERED. Recovery dalam 18 hari. ✅
- Bull Dip Agt 2024 (Yen): STH turun ke 0.917. TRIGGERED. Recovery dalam 7 hari. ✅
- Bull Dip Mar-Apr 2025: STH turun ke 0.953. TRIGGERED. Tapi recovery lambat — 35 hari. ⚠️
- Bull Dip Jun 2023: STH dip ke 0.984. NOT TRIGGERED. ❌ FALSE NEGATIVE (dip terlalu shallow)
- Bull Dip Jan 2024: STH dip ke 0.980. NOT TRIGGERED. ❌ FALSE NEGATIVE

**Hit rate (untuk triggered signals):** 5/5 = 100% — setiap kali trigger, recovery terjadi
**False negatives:** 2 shallow dips yang tidak trigger threshold
**Timing issue:** Mar-Apr 2025 menunjukkan bahwa recovery bisa lambat — jangan assume cepat

**Backtesting untuk Bear Bottoms:**
- Bear Bottom 2018: STH turun ke 0.932. TRIGGERED. Tapi bottom belum final — turun lagi. ⚠️
- FTX Collapse: STH turun ke 0.954. TRIGGERED. Near bottom tapi harga turun 15% lagi. ⚠️
- COVID Crash: STH turun ke 0.912. TRIGGERED. Bottom tercapai dalam 5 hari. ✅

**IMPORTANT CAVEAT untuk bear markets:** STH < 0.97 di bear market BUKAN automatic buy signal. Market bisa stay irrational lebih lama. Ini hanya "watch zone" — perlu konfirmasi dari aSOPR reclaim 1.0.

#### Rule B2: aSOPR < 0.93 (capitulation extreme)

**Rationale:** Aggregate loss realization yang extreme menandakan capitulation.

**Backtesting:**
- Bear Bottom 2018: aSOPR = 0.821 pada Des 11. Near bottom. ✅
- FTX Collapse: aSOPR = 0.862 pada Nov 9. Near bottom. ✅
- COVID Crash: aSOPR = 0.693 pada Mar 12 (hari sebelum event window). Near bottom. ✅
- 2025 Bear: aSOPR turun ke 0.887 pada Mei 20, 2026 (latest data point). Status: TBD.

**Hit rate:** 3/3 completed events = 100%
**False signal risk:** Sangat rendah — aSOPR < 0.93 hanya terjadi di extreme events
**Cost of being wrong:** Kalau buy di aSOPR 0.93 dan market turun lagi, drawdown bisa 10–20% sebelum actual bottom. ALWAYS scale in, jangan all-in.

#### Rule B3: Divergence STH-SOPR > 1.0 while aSOPR < 1.0

**Rationale:** New buyers profit sementara aggregate masih rugi = bottom forming, momentum shifting.

**Backtesting:**
- Pre Detection 2019: STH = 1.004 while aSOPR = 0.993. ✅ Bull market started 2 bulan kemudian.
- Pre Detection 2023: STH = 1.009 while aSOPR = 0.973. ✅ Bull market started 1 bulan kemudian.
- Bear Bottom 2022 period: STH oscillating around 1.0 while aSOPR < 0.98 selama Nov-Des. ✅ Bottom terbentuk.

**Hit rate:** 3/3 = 100%
**CAVEAT:** Signal ini bisa bertahan berminggu-minggu sebelum actual breakout. Ini bukan timing signal — ini regime identification signal. Artinya "mulai accumulate secara bertahap" bukan "buy sekarang juga."

---

## BAGIAN 3: INTERAKSI ANTAR KETIGA METRIK

### 3.1 Kapan Ketiga Metrik Sejalan

**Semua di atas 1.0 (bullish alignment):**
Terjadi di bull market yang sehat. aSOPR > 1.0, STH > 1.0, LTH > 1.0. Ini menandakan semua cohort profit dan market dalam uptrend. Contoh: Okt-Nov 2021 menjelang cycle peak, atau Okt 2024 menjelang Nov 2024 ATH.

**Semua di bawah 1.0 (bearish alignment):**
Terjadi di deep bear market. Semua cohort rugi. Contoh: Nov-Des 2022 pasca FTX collapse. Ini biasanya near-bottom territory, tapi BISA bertahan lama (berminggu-minggu).

### 3.2 Kapan Diverge — dan Artinya

**Divergence #1: STH < 1.0, LTH > 1.0, aSOPR ≈ 1.0**
Artinya: Short-term buyers rugi tapi long-term holders masih profit. Ini adalah BULL DIP signature yang paling umum. LTH "menopang" aggregate karena profit mereka besar meskipun volume kecil.

Terjadi di: hampir semua bull dips dalam data — Mar 2017, Jul 2017, Jun 2020, Sep 2020, Jan 2021, setiap bull dip 2024-2025.

Implikasi: kalau ini terjadi dan LTH-SOPR tetap di atas 1.5, ini kemungkinan bull dip biasa. Kalau LTH-SOPR juga turun menuju 1.0, ini bisa escalate ke mid-cycle correction.

**Divergence #2: STH > 1.0, LTH < 1.0, aSOPR ≈ 1.0**
Artinya: New buyers profit tapi old holders masih rugi dari bear market. Ini adalah PRE DETECTION / START OF BULL signature. Market secara aggregate masih belum fully recovery, tapi momentum sudah bergeser ke pembeli baru.

Terjadi di: Feb-Mar 2019, Jan 2023. Kedua kali ini mendahului bull market baru.

Implikasi: STRONG accumulation signal. Tapi timing masih bisa berminggu-minggu sampai berbulan-bulan — bukan reason untuk leverage.

**Divergence #3: aSOPR elevated (> 1.05) tapi STH declining menuju 1.0**
Artinya: aSOPR tetap tinggi karena beberapa transaksi LTH besar, tapi broad market (STH) sudah kehilangan momentum. Ini adalah DISTRIBUTION + WEAKENING DEMAND pattern.

Terjadi di: Nov 2021 menjelang lower high, Jan 2025 menjelang lower high. Kedua kali ini mendahului bear market confirmation.

Implikasi: RED FLAG. Aggregate terlihat sehat tapi sebenarnya didriver oleh sedikit big players taking profit. Broad market sudah lemah. Ini harus trigger de-risking.

**Divergence #4: LTH-SOPR turun drastis ke bawah 1.0 sementara STH-SOPR masih di atas 0.95**
Artinya: Long-term holders panic selling at a loss — ini rare dan extreme. Di bear bottom 2018-2019, LTH-SOPR turun ke 0.34–0.50 (holders yang beli di peak 2017 finally capitulate setelah 12+ bulan rugi).

Terjadi di: Nov-Des 2018, Nov-Des 2022.

Implikasi: Ini HISTORICALLY bottom signal yang sangat strong — tapi sample size kecil (2 events). Di 2022, LTH-SOPR turun ke 0.36 pada Nov 18 — hanya 3 hari sebelum actual price low.

### 3.3 Kombinasi Sinyal Paling Reliable Per Regime

| Regime | Sinyal Paling Reliable | Confidence |
|---|---|---|
| Cycle Peak | aSOPR 7d avg > 1.04 + STH > 1.01 + trend RISING (keduanya) | MEDIUM — diminishing di 2025 |
| Local Top | aSOPR spike > 1.05 + LTH spike > 2.5 dalam 7 hari | MEDIUM |
| Bull Dip (buy) | STH < 0.97 sustained 3+ hari + aSOPR masih > 0.95 | HIGH |
| Mid-Cycle vs Bull Dip | STH < 0.96 sustained > 14 hari + aSOPR < 1.0 sustained > 14 hari | HIGH |
| Lower High | aSOPR declining saat harga naik + STH declining | HIGH |
| Bear Bottom | aSOPR < 0.93 + LTH < 0.50 + STH < 0.96 | HIGH (tapi sample=2) |
| Pre Detection Bull | STH > 1.0 sustained + aSOPR < 1.0 + LTH < 1.0 | HIGH |

### 3.4 Divergence Paling Berbahaya Kalau Diabaikan

**#1: Divergence #3 (aSOPR elevated + STH declining)**
Kenapa berbahaya: Terlihat sehat di surface tapi sebenarnya distribusi. Kalau kamu punya posisi leveraged dan lihat aSOPR masih di atas 1.0, kamu bisa over-confident. Tapi kalau STH sudah declining, market sedang weakening.

Consequences dari mengabaikan: Lower High 2021 → bear market -77%. Lower High 2025 → bear market (ongoing, sudah -50% dari peak ke data terakhir).

**#2: STH sustained di bawah 0.98 lebih dari 14 hari**
Kenapa berbahaya: Ini bisa signal transisi dari "bull dip" ke "mid-cycle correction" atau bahkan "bear market onset". Kalau kamu treat semua STH < 1.0 sebagai buying opportunity, kamu akan overleveraged saat yang terjadi sebenarnya adalah regime change.

---

## BAGIAN 4: FAILURE MODES

### 4.1 aSOPR Failure Modes

**Failure #1: Diminishing signal strength across cycles**
Data shows: Peak aSOPR values semakin rendah setiap cycle. Threshold yang works di 2017 misfire di 2021 dan especially 2025. Ini bukan anomali — ini structural. Market semakin mature, profit margins semakin compressed.

Implikasi: JANGAN pakai fixed thresholds. Selalu calibrate terhadap recent cycle behavior. aSOPR > 1.05 yang dulu "moderate" sekarang bisa jadi "extreme."

**Failure #2: Entity-adjusted masih terdistorsi oleh whale transactions**
Single large transaction dari long-term whale bisa spike aSOPR signifikan. Contoh: 7 Desember 2017, aSOPR = 1.467 — satu hari anomali yang distort averages. Juga 28 Mei 2024, aSOPR = 1.307 — almost certainly single large LTH transaction.

Implikasi: SELALU gunakan moving average (7d minimum), jangan daily readings untuk decision-making.

**Failure #3: aSOPR tidak bisa membedakan volume**
aSOPR = 1.05 bisa berarti: banyak orang realize 5% profit (healthy), atau sedikit orang realize 500% profit (whale distribusi). Tanpa volume context, signal ambigu.

Implikasi: Cross-reference dengan exchange flows dan volume data. aSOPR alone is insufficient.

**Failure #4: No advance warning untuk sudden crashes**
COVID crash (Mar 2020): aSOPR masih 0.95+ (normal) pada 11 Maret, crash ke 0.693 pada 12 Maret. Zero lead time. Yen carry trade unwind (Aug 2024): similar — aSOPR dari 0.99 ke 0.95 overnight.

Implikasi: aSOPR TIDAK BISA predict exogenous shocks. Risk management (position sizing, LTV buffer) harus account for ini regardless of on-chain signals.

### 4.2 LTH-SOPR Failure Modes

**Failure #1: Extremely noisy — most unreliable dari ketiga metrik**
LTH-SOPR swings wildly on any given day. Contoh: Jan 7, 2018 = 54.82 (outlier extreme), diikuti Jan 8 = 10.52. Single whale movement bisa move LTH-SOPR 5x dalam sehari.

Implikasi: JANGAN PERNAH pakai daily LTH-SOPR untuk keputusan. Minimum 14-day average, dan even then treat dengan skeptisisme.

**Failure #2: Structural decline across cycles**
2017 peak LTH-SOPR avg = 18.27. 2021 peak LTH-SOPR avg = 2.40. 2025 peak LTH-SOPR avg = 2.32. Ini bukan signal deterioration — ini refleksi bahwa Bitcoin distribution lebih merata dan ada lebih sedikit "ancient coins" yang menghasilkan extreme profit ratios.

Implikasi: LTH-SOPR thresholds dari 2017 (mis. "bearish di bawah 5.0") totally irrelevant untuk 2021 dan seterusnya.

**Failure #3: Can stay at extreme levels longer than expected**
Selama bull 2017, LTH-SOPR sustained di atas 5.0 selama berminggu-minggu. Selama bear 2018-2019, LTH-SOPR sustained di bawah 0.60 selama berminggu-minggu. Tidak ada mean-reversion yang reliable.

**Di antara ketiganya, LTH-SOPR paling sering gagal dan harus SELALU dipakai sebagai secondary/tertiary indicator, TIDAK PERNAH standalone.**

### 4.3 STH-SOPR Failure Modes

**Failure #1: Shallow dips di bull market 2023-2024 tidak trigger threshold**
Bull dips Jun 2023 dan Jan 2024 hanya melihat STH turun ke 0.98–0.99. Threshold 0.97 tidak triggered, menyebabkan false negative untuk buy signal. Market semakin efficient → dips semakin shallow → thresholds perlu diturunkan.

**Failure #2: STH-SOPR bisa stay di bawah 1.0 selama berminggu-minggu di bear market**
Di bear market 2022, STH-SOPR sustained di bawah 1.0 selama berbulan-bulan. Setiap "recovery" ke 1.0 ternyata temporary. Ini menjadikan STH reclaim 1.0 unreliable sebagai standalone bull signal di bear market — perlu sustained (14+ hari) untuk confidence.

**Failure #3: Sensitivity terhadap 155-day threshold definition**
STH vs LTH classification bergantung pada 155-day cutoff. Perubahan kecil dalam cutoff bisa shift banyak coins dari satu cohort ke cohort lain, mengubah readings. Ini bukan controllable tapi harus disadari.

### 4.4 Apa yang Bisa Membuat Threshold Historis Tidak Berlaku

1. **Institutional adoption continuing to compress volatility.** ETF flows, corporate treasury adoption, sovereign adoption semua membuat BTC less volatile per cycle. SOPR readings akan terus compressed.

2. **Change in holder composition.** Kalau ETFs hold significant portion of supply dan rarely transact on-chain, SOPR loses representativeness.

3. **L2 adoption.** Semakin banyak transaksi pindah ke Lightning atau L2 lain, on-chain SOPR hanya capture subset of activity — potentially biased toward large/institutional.

4. **Regulatory events.** Forced selling (tax events, sanctions) creates SOPR readings yang bukan refleksi market sentiment.

---

## BAGIAN 5: MAPPING KE REGIME CATEGORIES

### Regime Detection Decision Tree (menggunakan ketiga metrik):

```
STEP 1: Cek STH-SOPR 14-day average
├── > 1.02 → kemungkinan CYCLE PEAK / LOCAL TOP zone
│   ├── aSOPR 7d avg > 1.04 → HIGH confidence top zone
│   └── aSOPR 7d avg 1.00–1.04 → MODERATE confidence, bisa local top
├── 1.00–1.02 → BULL MARKET normal / UPPER RANGE RECOVERY
│   ├── Trending up → continuation
│   └── Trending down dari > 1.02 → WATCH for distribution (Lower High risk)
├── 0.97–1.00 → BULL DIP candidate
│   ├── Duration < 14 hari → likely bull dip, accumulate
│   └── Duration > 14 hari → escalating to MID-CYCLE CORRECTION
├── 0.95–0.97 → SEVERE DIP or BEAR MARKET transition
│   ├── aSOPR still > 0.98 → severe bull dip, cautious accumulate
│   └── aSOPR < 0.98 → possible BEAR MARKET DECLINE
└── < 0.95 → CAPITULATION / BEAR BOTTOM territory
    ├── LTH-SOPR < 0.50 → deep capitulation, historically near bottom
    └── LTH-SOPR > 0.50 → capitulation ongoing but may not be final
```

### Kapan Masing-Masing Metrik Harus Diberi Weight Tinggi vs Rendah

| Situasi | aSOPR Weight | STH-SOPR Weight | LTH-SOPR Weight |
|---|---|---|---|
| Detecting bull dip vs correction | MEDIUM | HIGH (durasi dan depth) | LOW |
| Detecting cycle peak | MEDIUM | HIGH (trend direction) | LOW-MEDIUM (spike konfirmasi) |
| Detecting bear bottom | HIGH (capitulation level) | MEDIUM | HIGH (LTH capitulation) |
| Detecting bull market start | MEDIUM | HIGH (divergence with aSOPR) | LOW |
| Lower high confirmation | HIGH (declining while price rises) | HIGH (declining trend) | LOW |

### Red Flags yang Harus Trigger Immediate Attention

1. **STH-SOPR declining while price making new highs** — distribution happening, potential top forming. This is the most actionable red flag.

2. **aSOPR spike > 1.10 (any single day)** — extreme profit-taking, check if this is isolated whale or broad-based. If broad-based (STH also > 1.05), consider taking profit.

3. **STH-SOPR < 0.95 for 3+ consecutive days** — severe stress on short-term holders. If you have leveraged positions, CHECK LTV IMMEDIATELY regardless of other signals.

4. **LTH-SOPR drop below 1.0 during what you thought was a bull market** — long-term holders are now selling at a loss. This has only happened at bear market bottoms historically. If this happens during supposed "bull dip," REASSESS YOUR REGIME ASSUMPTION.

5. **All three metrics simultaneously declining for 7+ days** — momentum deteriorating across all cohorts. Not necessarily bearish alone, but combined with price weakness = high alert.

---

## BAGIAN 6: CURRENT MARKET CONTEXT (per data terakhir)

**Latest data point: 20 Mei 2026**
BTC Price: $77,563
aSOPR: 0.887
LTH-SOPR: 0.822
STH-SOPR: 0.889

**Assessment:**

Ini adalah DEEP CAPITULATION territory. aSOPR di bawah 0.90 dan semua tiga metrik di bawah 1.0 — bahkan LTH-SOPR di bawah 1.0, yang artinya long-term holders selling at a loss.

Berdasarkan historical patterns:
- aSOPR < 0.90 telah terjadi di: Bear Bottom 2018 (0.82), FTX Collapse 2022 (0.86), COVID Crash 2020 (0.69). Setiap kali ini signaled near-bottom territory.
- LTH-SOPR < 1.0 secara sustained terjadi mulai dari bear decline 2018 ke bawah, dan Nov-Des 2022. Ini menandakan bear market yang sudah cukup mature.

**Regime indication:** BEAR MARKET DECLINE menuju BEAR BOTTOM NEAR territory.

**Confidence level:** MEDIUM-HIGH berdasarkan historical precedent, tapi dengan caveat bahwa:
1. Sample size kecil (3 previous cycles)
2. Current cycle memiliki structural differences (ETF flows, institutional adoption)
3. Data terakhir menunjukkan masih ada downward momentum (belum ada sustained recovery di STH-SOPR)

**Strategy table mapping:** Ini suggest fase "Bear Bottom Near" — accumulation window berdasarkan historical patterns. TAPI ini BUKAN timing call. Signal untuk "bottom confirmed" membutuhkan: aSOPR reclaim 1.0 sustained 7+ hari, STH-SOPR reclaim 1.0 mendahului aSOPR, dan LTH-SOPR trending up meskipun masih di bawah 1.0.

---

## BAGIAN 7: CONFIDENCE CAVEATS & LIMITATIONS

### Yang perlu diingat setiap kali menggunakan dokumen ini:

1. **Sample size = 3 completed cycles.** Statistical significance sangat terbatas. Patterns bisa berubah di cycle berikutnya.

2. **Diminishing returns sudah terbukti.** Setiap threshold yang bekerja di cycle N menjadi less reliable di cycle N+1. Thresholds HARUS di-recalibrate.

3. **SOPR family adalah PROFITABILITY metric, bukan PRICE metric.** Mereka memberi tahu kapan orang-orang realize profit/loss, bukan kemana harga akan pergi.

4. **Exogenous shocks tidak terdeteksi.** COVID, FTX, Yen carry trade — semua ini came without on-chain warning. SOPR TIDAK BISA melindungi dari black swans.

5. **Conflating aSOPR with STH/LTH is a common mistake.** aSOPR = weighted average, bisa misleading kalau distribusi antara STH dan LTH tidak proporsional.

6. **LTH-SOPR = most unreliable.** Gunakan hanya sebagai supporting evidence, never standalone.

7. **Current data (Mei 2026) menunjukkan readings yang extreme.** aSOPR 0.887 dan STH 0.889 di data terakhir menandakan stress level yang tinggi. Tapi ini juga bisa berarti market sudah dekat bottom — atau bisa turun lebih lagi. Historical parallels suggest near-bottom, tapi "near" bisa berarti hari atau bulan.

---

---

## BAGIAN 8: SMA15 DIVERGENCE ANALYSIS — REGULAR & HIDDEN BULL DIV

**Metodologi:** Cek SMA15 dari aSOPR, STH-SOPR, LTH-SOPR di dua window berbeda. Bandingkan low price vs low indicator value antar window.
- **Regular Bull Div:** Price lower low (LL), indicator higher low (HL) → capitulation tapi selling pressure berkurang
- **Hidden Bull Div:** Price higher low (HL), indicator lower low (LL) → uptrend intact, dip lebih tertekan tapi strukturally bullish

**Catatan metodologi:** SMA15 dihitung per row sequential, bukan per 15 hari kalender. Ada data gap 154 hari (Apr–Okt 2022) sehingga Jun 2022 tidak tersedia di dataset.

---

### 8.1 Bear Bottom: Oct 2019 vs Nov–Dec 2019

| Metrik | Window 1 (Oct 2019) | Window 2 (Nov–Dec 2019) | Divergence |
|---|---|---|---|
| Price low | $7,455 | $6,854 | Price LL (−8%) |
| aSOPR SMA15 low | 0.97890 | 0.97623 | ❌ LL — no div |
| STH SMA15 low | 0.96820 | 0.97141 | **✅ Regular Bull Div** |
| LTH SMA15 low | 1.374 | 1.060 | ❌ LL — no div |

**Interpretasi:** Divergence hanya di STH. Sinyal lemah tapi konsisten dengan karakteristik Bear Bottom 2019 — STH buyers di bottom kedua less stressed meskipun harga lebih rendah. STH adalah satu-satunya yang leading, LTH masih distributing. Ini "weak bull signal" — satu dari tiga konfirmasi, bukan enough untuk standalone action.

---

### 8.2 Bear Bottom: Oct 2022 vs Nov 2022

| Metrik | Window 1 (Oct 2022) | Window 2 (Nov 2022) | Divergence |
|---|---|---|---|
| Price low | $19,045 | $15,774 | Price LL (−17%) |
| aSOPR SMA15 low | — | — | ❌ Bearish cont. |
| STH SMA15 low | — | — | ❌ Bearish cont. |
| LTH SMA15 low | — | — | ❌ Bearish cont. |

**Catatan:** Jun 2022 actual low tidak ada di dataset (data gap). Oct 2022 adalah data pertama setelah gap — ini bukan "bear dip recovery" tapi masih dalam capitulation yang sama. FTX collapse period (Nov 2022) terlalu cepat dan brutal untuk divergence terbentuk. Zero divergence di semua tiga metrik = confirmed bear decline continuation.

**Lesson:** Tidak ada divergence bukan bearish signal tambahan, tapi absent of divergence mengkonfirmasi tidak ada structural improvement. Perlu source Jun 2022 data terpisah untuk analisis pair yang dimaksud.

---

### 8.3 Bull Dip: Jun 2023 vs Aug–Sep 2023

| Metrik | Window 1 (Jun 2023) | Window 2 (Aug–Sep 2023) | Divergence |
|---|---|---|---|
| Price low | $25,173 | $25,179 | Price HL (+0.03%) |
| aSOPR SMA15 low | 0.99780 | 0.98918 | **✅ Hidden Bull Div** (−0.86%) |
| STH SMA15 low | 0.99494 | 0.98785 | **✅ Hidden Bull Div** (−0.71%) |
| LTH SMA15 low | 1.11505 | 0.97593 | **✅ Hidden Bull Div** (−12.48%) |

**TRIPLE HIDDEN BULL DIVERGENCE.** Semua tiga metrik confirm. Harga virtually flat tapi semua indikator menunjukkan stress lebih dalam — artinya uptrend masih intact secara structural, dip semakin "tertekan" tapi bukan perubahan arah.

**Outcome:** Market rally besar ke $34–$44K di Oktober 2023 — divergence ini preceded major continuation.

LTH divergence paling besar (−12.48%) karena LTH profit per unit di Aug-Sep jauh lebih kecil — LTH holders realized less, consistent dengan bottom strengthening.

---

### 8.4 Bull Dip: Aug–Sep 2023 vs Aug 2024 (Yen Carry Trade)

| Metrik | Window 1 (Aug–Sep 2023) | Window 2 (Aug 2024) | Divergence |
|---|---|---|---|
| Price low | $25,179 | $54,026 | Price HL (+114%) |
| aSOPR SMA15 low | 0.98918 | 1.00335 | ↗ Clean uptrend (HL) |
| STH SMA15 low | 0.98785 | 0.98781 | **✅ Hidden Bull Div** (−0.00%) |
| LTH SMA15 low | 0.97593 | 1.91034 | ↗ Clean uptrend (HL) |

**Partial signal.** STH hidden div sangat subtle — hampir identik meskipun harga 2x lebih tinggi. Dalam konteks harga +114%, STH stress yang sama = relative strength bukan weakness. aSOPR dan LTH recovered signifikan (healthy), hanya STH yang menunjukkan persistent mild stress di dips.

---

### 8.5 Bull Dip: Aug 2024 (Yen) vs Mar–Apr 2025

| Metrik | Window 1 (Aug 2024) | Window 2 (Mar–Apr 2025) | Divergence |
|---|---|---|---|
| Price low | $54,026 | $76,270 | Price HL (+41%) |
| aSOPR SMA15 low | 1.00335 | 1.00246 | **✅ Hidden Bull Div** (−0.09%) |
| STH SMA15 low | 0.98781 | 0.98263 | **✅ Hidden Bull Div** (−0.52%) |
| LTH SMA15 low | 1.91034 | 1.89438 | **✅ Hidden Bull Div** (−0.84%) |

**TRIPLE HIDDEN BULL DIVERGENCE lagi.** Meskipun harga +41%, semua tiga SMA15 lows lebih rendah. Ini retroactively confirm Mar–Apr 2025 adalah genuine bull dip meskipun berlangsung 35 hari dan felt very extended. Structural integrity uptrend masih intact.

---

### 8.6 Summary Tabel — Divergence Pattern per Regime Type

| Pair | Regime | aSOPR | STH | LTH | Verdict |
|---|---|---|---|---|---|
| Oct vs Dec 2019 | Bear Bottom | ❌ | ✅ Regular | ❌ | Weak bull — STH only |
| Oct vs Nov 2022 | Bear Decline (FTX) | ❌ | ❌ | ❌ | Bearish continuation |
| Jun vs Aug-Sep 2023 | Bull Dip | ✅ Hidden | ✅ Hidden | ✅ Hidden | **Strong triple** |
| Aug-Sep 2023 vs Aug 2024 | Bull Dip | ↗ Uptrend | ✅ Hidden | ↗ Uptrend | Partial (STH only) |
| Aug 2024 vs Mar-Apr 2025 | Bull Dip | ✅ Hidden | ✅ Hidden | ✅ Hidden | **Strong triple** |
| Nov 2025 vs Jan-Feb 2026 | Bear Decline | ❌ | ❌ | ❌ | Bearish continuation |

**Key observations:**
1. Bull dips genuine dalam uptrend → hidden bull div (karena price HL)
2. Bear bottoms → regular bull div di STH saja (karena price LL, STH most sensitive)
3. Bear decline continuation → zero divergence di semua tiga metrik
4. Triple confirmation (semua tiga metrik) = highest confidence signal
5. Single metrik div (STH only) = watch zone, bukan action signal

---

## BAGIAN 9: aSOPR OPTIMAL EMA/SMA CROSSOVER

**Pertanyaan:** EMA dan SMA period berapa yang paling leading untuk aSOPR sebagai signal indicator?

**Metodologi:** Backtest 238 kombinasi EMA (20–95, step 5) × SMA (15–75, step 5) terhadap 25 regime transition events. Signal = crossover dalam 90-row lookback sebelum event. Lead time = rows antara crossover dan event date. Metrik evaluasi: hit rate dan avg lead time.

**Baseline pembanding:** EMA90/SMA80 (lagging approach)

---

### 9.1 Hasil Iterasi — Top Combinations

| Combo | Hits/25 | Hit Rate | Avg Lead | Catatan |
|---|---|---|---|---|
| **EMA55/SMA35** | **23/25** | **92%** | **40.9 rows** | **OPTIMAL — current best** |
| EMA55/SMA30 | 22/25 | 88% | 34.7 rows | Hit rate turun 1, lead lebih cepat |
| EMA60/SMA30 | 22/25 | 88% | 35.2 rows | Serupa |
| EMA60/SMA35 | 22/25 | 88% | 35.8 rows | 1 hit less dari 55/35 |
| EMA75/SMA30 | 21/25 | 84% | 39.6 rows | Lebih lambat, miss 4 |
| EMA65/SMA35 | 21/25 | 84% | 33.9 rows | Miss BD Jan 2021 tambahan |
| **EMA90/SMA80** | **20/25** | **80%** | **44.0 rows** | **Baseline lama — lagging** |
| EMA80/SMA30 | 18/25 | 72% | 39.1 rows | Terlalu lambat |

---

### 9.2 Per-Event Performance EMA55/SMA35

**Hits (23/25):**
| Event | Lead (rows) | Event | Lead (rows) |
|---|---|---|---|
| Peak 2017 | 43 | Peak 2021 | 13 |
| Peak 2025 | 87 | LH 2018 | 18 |
| LH 2021 | 35 | LH 2025 | 10 |
| Bottom 2018 | 68 | Bottom 2019 T2 | 15 |
| COVID bottom | 89 | FTX bottom | 52 |
| Bottom 2022 final | 27 | Pre-Det 2019 | 40 |
| Start Bull 2019 | 75 | Pre-Det 2023 | 3 |
| Start Bull 2023 | 25 | BD Jan 2021 | 63 |
| BD Jun 2023 | 44 | BD Aug 2023 | 14 |
| BD Aug 2024 Yen | 34 | BD Sep 2024 | 16 |
| BD Mar-Apr 2025 | 79 | Bear Start 2018 | 77 |
| Bear Start 2025 | 13 | | |

**Misses (2/25):**
- MCC Bottom 2021 — mid-cycle correction punya karakteristik berbeda, aSOPR masih di atas SMA35 ketika ini terjadi
- BD Jul 2017 — dip terlalu singkat (5 hari) untuk crossover terbentuk

---

### 9.3 Kenapa EMA55/SMA35 Beat EMA90/SMA80

Critical events yang EMA90/SMA80 miss tapi EMA55/SMA35 catch:

| Event | EMA90/SMA80 | EMA55/SMA35 |
|---|---|---|
| Peak 2017 | ❌ MISS | ✅ 43 rows early |
| COVID bottom | ❌ MISS | ✅ 89 rows early |
| FTX bottom | ❌ MISS | ✅ 52 rows early |
| Start Bull 2019 | ❌ MISS | ✅ 75 rows early |
| Peak 2025 | ✅ 65 rows | ✅ 87 rows (+22 earlier) |

Satu-satunya trade-off: Pre-Det 2023 di mana EMA90/SMA80 leading 26 rows lebih awal (lead 29 vs 3). Ini acceptable cost vs empat misses yang dihindari.

---

### 9.4 Kenapa Tidak Pakai Periode yang Lebih Pendek

EMA30/SMA15 memang 25/25 hit rate (100%), tapi avg lead hanya 19.4 rows. Ini karena crossover terjadi terlalu sering (noise/whipsaw) — secara teknis selalu ada cross dalam 90-row window. Bukan "leading", tapi "always triggering."

Prinsip: yang dibutuhkan bukan "paling sering trigger" tapi "trigger di momen yang benar, cukup awal." EMA55/SMA35 adalah sweet spot: cukup responsive untuk 92% hit rate, cukup smooth untuk avoid whipsaw.

---

### 9.5 Improvement Path

EMA55/SMA35 sudah optimal sebagai single crossover. Improvement harus datang dari multi-signal stacking:

1. **EMA55/SMA35** sebagai primary crossover signal (92% hit rate — gunakan as-is)
2. **SMA15 divergence analysis** (Bagian 8) sebagai confirmation layer
3. **aSOPR SMA35 crossing 1.0** sebagai additional heavy signal (crossing 1.0 = structural significance, bukan hanya moving average interaction)

---

## BAGIAN 10: LTH/STH RATIO & FIVE DIVERGENCE STATES FRAMEWORK

### 10.1 Definisi

**LTH/STH Ratio** = LTH-SOPR ÷ STH-SOPR. Mengukur relatif berapa besar profit yang direalisasikan long-term holders dibanding short-term holders pada waktu yang sama.

**Spread (L−S)** = LTH-SOPR minus STH-SOPR. Ukuran absolut perbedaan profitability antar cohort.

**STH-aSOPR** = STH-SOPR minus aSOPR. Positif artinya STH outperforms aggregate (unusual — biasanya LTH profits mengangkat aSOPR di atas STH).

---

### 10.2 LTH/STH Ratio Zones

| Zone | Range | Regime Indication |
|---|---|---|
| Extreme | > 15.0 | 2017 hanya (outlier whale events — tidak reliable untuk threshold) |
| Late-stage bull | 5.0–15.0 | 2017-style euphoria; hampir tidak relevan di cycle 2021+ |
| Approaching top | 2.5–5.0 | Elevated bull, upper range territory |
| Healthy bull | 1.2–2.5 | Normal bull market — LTH distributing, STH participating |
| Neutral / early recovery | 1.0–1.2 | Bull dip zone atau early upper range |
| Transition zone | 0.8–1.0 | Bear → Bull boundary, oscillation expected |
| Late bear / pre-detection | 0.5–0.8 | Historical Pre Detection range |
| Deep capitulation | < 0.5 | Bear bottom 2018 and 2022 territory |

**Per-regime ratio statistics dari data (outlier 2017 noted):**

| Regime | Min | Median | Max | n |
|---|---|---|---|---|
| Cycle Peak | 1.101 | 2.455 | 25.657 | 36 |
| Lower High | 1.591 | 2.534 | 53.252 | 17 |
| Local Top | 1.288 | 2.270 | 12.781 | 82 |
| MCC | 1.562 | 2.343 | 11.668 | 31 |
| Bull Dip | 0.523 | 1.543 | 7.820 | 174 |
| Bear Decline | 0.984 | 1.514 | 3.537 | 20 |
| Bear Bottom | 0.365 | 0.802 | 1.982 | 47 |
| Start of Bull | 0.632 | 0.723 | 0.899 | 4 |
| Pre Detection | 0.459 | 0.551 | 0.679 | 10 |

**Dua regime paling tightly bounded:** Pre Detection (0.459–0.679) dan Start of Bull (0.632–0.899). Ini menjelaskan kenapa dua regime ini paling reliably identifiable dari data on-chain.

---

### 10.3 Five Divergence States

Klasifikasi harian berdasarkan posisi relatif LTH-SOPR, STH-SOPR, dan threshold 1.0:

**State A — LTH > STH, keduanya > 1.0**
LTH distributing, STH following. Normal bull market. Regime: Bull Dip (saat STH baru recover), Local Top, Cycle Peak, Upper Range.

**State B — LTH > STH, STH < 1.0**
LTH masih profit, new buyers stressed. Bull dip territory atau early bear decline. Ini state paling umum di dataset — terjadi di hampir semua bull dips dan juga di awal bear decline.

**State C — STH > LTH, keduanya > 1.0**
New buyers outperforming LTH. Rare. Early bull momentum dimana coins baru lebih efficiently transacted. Terjadi beberapa kali di Upper Range 2023 dan transisi Bull Dip Mar 2023 → recovery.

**State D — STH > 1.0, LTH < 1.0**
STH buyers profit sementara LTH masih underwater. **PRE-BULL SIGNAL yang paling distinctive.** LTH belum recover dari bear, tapi new buyers yang beli near-bottom sudah in profit.

**State E — STH > LTH, keduanya < 1.0**
Keduanya rugi, tapi STH losing less. Deep capitulation — new buyers yang beli near-bottom more resilient dari long-term holders yang terjebak dari harga tinggi. Terjadi di semua major bear bottoms.

---

### 10.4 State D sebagai Pre-Bull Detector

State D adalah structural shift yang paling penting untuk dimonitor. Data historical:

| Period | State D Occurrences | Outcome |
|---|---|---|
| Feb–Apr 2019 | Frequent oscillation D↔E | Bull market dimulai Apr 2019 |
| Jul 2018 | Isolated 1-2 hari | False signal — harga turun lagi |
| Jan–Mar 2023 | Frequent oscillation D↔E | Bull market dimulai Feb 2023 |
| Feb–Mei 2026 | Sporadic, increasing | Status: monitoring |

**Rule:** Isolated State D = tidak reliable. Sustained oscillation D↔E selama 2–4 minggu = strong Pre Detection signal. Satu hari State D di tengah bear decline = noise.

**Distinction dari Jul 2018 false signal:** Di Jul 2018, State D hanya berlangsung 1–2 hari sebelum market dropped lagi. Di 2019 dan 2023, oscillation D↔E berlangsung 4–6 minggu dengan increasing frequency. Duration dan persistence adalah kunci.

---

### 10.5 State Patterns per Regime Type

| Regime | Dominant State(s) | Pattern |
|---|---|---|
| Cycle Peak | A (dengan LTH spikes) | State A persistent, LTH occasional B |
| Local Top | A, B oscillating | A→B saat STH drop, B→A saat STH recover |
| Bull Dip | B → A | Entry di B (STH stressed), resolution di A (STH recover) |
| MCC | A → B extended | B persists > 14 hari sebelum balik ke A |
| Lower High | A → B transition | A declining frequency, B increasing = warning |
| Bear Decline | B → E | Gradual deterioration dari B ke E |
| Bear Bottom | E dominant, D↔E oscillation | E = capitulation; D↔E oscillation = near-bottom |
| Pre Detection | D↔E frequent | STH breaking above 1.0 while LTH still < 1.0 |
| Start of Bull | D/E → gradual A | D→E oscillation reduces, A starts appearing |

---

### 10.6 STH-aSOPR Sign Flip sebagai Mechanical Confirm

STH-aSOPR adalah perbedaan STH-SOPR dikurangi aSOPR.

- **Di semua bull market regimes:** STH-aSOPR selalu NEGATIF (range −0.03 sampai −0.08). LTH profits yang besar selalu mengangkat aSOPR di atas STH.
- **Di Bear Bottom dan Pre Detection:** STH-aSOPR balik POSITIF (+0.01 sampai +0.06). STH outperforms aggregate.

Per-regime average:

| Regime | STH-aSOPR avg | LTH-aSOPR avg |
|---|---|---|
| Cycle Peak | −0.027 | +6.617 |
| Local Top | −0.030 | +1.787 |
| Bull Dip | −0.012 | +1.054 |
| Bear Decline | −0.008 | +0.681 |
| Bear Bottom | **+0.011** | −0.129 |
| Pre Detection | **+0.020** | −0.408 |
| Start of Bull | **+0.007** | −0.249 |

**Rule:** Ketika STH-aSOPR sign flip dari negatif ke positif secara sustained (3+ hari berturut-turut), ini adalah mechanical confirmation bahwa kita memasuki Bear Bottom / Pre Detection territory. Flip ini terjadi karena: (1) LTH sudah cukup kapitulasi sehingga tidak lagi mengangkat aSOPR, dan (2) STH buyers near-bottom mulai outperform aggregate.

---

### 10.7 Ratio Sebagai Regime Differentiator — Limitasi

**Bull Dip ratio range sangat lebar (0.523–7.820)** — terlalu lebar untuk jadi identifier standalone. Contoh:
- Jun 2020 bull dip: ratio 0.974 (LTH masih underwater post-COVID)
- Sep 2017 bull dip: ratio 6.689 (LTH extreme profit di akhir cycle)

Ratio alone tidak cukup — perlu price context (awal vs akhir cycle). Kombinasikan dengan:
- aSOPR absolute level (di atas atau bawah 1.0)
- Durasi State B (< 14 hari = bull dip, > 14 hari = escalation risk)
- EMA55/SMA35 crossover direction (Bagian 9)

---

### 10.8 Current Market Watchlist (Bear 2025–2026)

Berdasarkan pattern historical, tiga kondisi yang perlu terpenuhi untuk konfirmasi transisi ke Pre Detection / Start of Bull:

**Kondisi 1 — Ratio compress ke zona 0.5–0.8**
Data Jan 2026: ratio masih 1.0–1.5. Belum masuk zona Pre Detection historical (0.46–0.68). Artinya LTH belum cukup capitulate atau cycle ini akan berbeda structural.

**Kondisi 2 — State D sustained oscillation D↔E selama 2–4 minggu**
Per data Feb–Mei 2026: State D mulai muncul sporadis (6 Feb, 9 Mar, 15 Mar, 7 Apr, 9 Apr, 14 Apr). Mirip early-stage Pre Detection, tapi belum sustained. Monitor frekuensi meningkat atau menurun di minggu ke depan.

**Kondisi 3 — STH-aSOPR positif secara persistent (3+ hari berturut-turut)**
Belum terjadi secara sustained di data terbaru. Occasional positive days ada tapi belum continuous. Ini konfirmasi terakhir sebelum bisa label sebagai "Pre Detection confirmed."

**None of these adalah timing call.** Ketiga kondisi di atas adalah regime identification signals — artinya "mulai accumulate secara bertahap" bukan "buy sekarang." Selalu scale in. Selalu check LTV buffer sebelum sizing apapun.

---

---

## BAGIAN 11: STH-SOPR MA90 / MA90-MA60 GAP-AND-CROSS FRAMEWORK

### 11.1 Konstruksi Indikator

**MA90:** Simple Moving Average 90 hari dari STH-SOPR. Smooth enough untuk menghilangkan daily noise, tapi tetap responsive terhadap perubahan profitability regime.

**MA90-MA60:** Simple Moving Average 60 hari dari MA90 (double-smoothed). Ini baseline yang bergerak lebih lambat — menangkap "trend of the trend." Ketika MA90 di atas MA90-MA60, profitability STH sedang improving. Ketika di bawah, deteriorating.

**Gap:** MA90 minus MA90-MA60. Positif = momentum improving, negatif = momentum deteriorating. Magnitude gap menunjukkan seberapa cepat perubahan terjadi.

**Data source:** CSV terpisah dari ChartInspect.com (STH-SOPR dengan SMA90d pre-computed). MA60-of-MA90 dihitung sebagai derived metric.

---

### 11.2 Tiga Signal Types

**Signal A — Gap Peak + Decline → Local Top Warning (Reduce Loan)**

Ketika gap antara MA90 dan MA90-MA60 sudah peaked dan mulai menurun, ini menandakan profitability momentum STH sudah melemah meskipun harga mungkin masih naik. Signal ini bukan precision timing tool — ini early warning untuk mulai reduce loan exposure.

**Signal B — Bearish Cross Setelah Local Top → Regime Shift ke Bull Dip**

Ketika MA90 crosses di bawah MA90-MA60 setelah local top terjadi, ini mengkonfirmasi regime transition ke period koreksi. Bearish cross = profitability trend sudah secara definitif berubah arah.

**Signal C — Bearish Cross Setelah Cycle Peak → Lower High Confirmation**

Pattern yang sama tapi setelah cycle peak. Bearish cross di konteks ini mengkonfirmasi bahwa recovery selanjutnya akan membentuk lower high, bukan new ATH.

---

### 11.3 Signal A — Gap Peak + Decline: Historical Evidence

| Event | Gap Peak Value | Gap Peak Date | Gap at Event | Gap Declining From | Bearish Cross After Event |
|---|---|---|---|---|---|
| Local Top Mar 2021 | +0.02447 | 10 Jan | +0.00693 | −14d (declining) | 15 hari ($55,808) |
| Local Top Mar 2024 | +0.00680 | 14 Mar (= event) | +0.00680 | +7d (peak at event) | 45 hari ($63,130) |
| Local Top Des 2024 | +0.01088 | 12 Des (+7d) | +0.01036 | +14d (slight lag) | 60 hari ($101,436) |
| Local Top Jan 2025 | +0.00917 | 21 Des (−30d) | +0.00191 | −30d (well ahead) | 14 hari ($101,436) |
| Cycle Peak 2021 | +0.01313 | 21 Okt (−18d) | +0.00691 | −7d (declining) | 22 hari ($56,995) |
| Jul–Aug 2025 ATH | +0.00770 | 17 Jul (−26d) | +0.00096 | −14d (declining fast) | 6 hari ($116,295) |

**Hit rate:** 6/6 — setiap local top dan cycle peak dalam dataset ditandai oleh gap yang sudah peaked dan declining sebelum atau di sekitar event.

**Lead time bervariasi:** Gap mulai menurun antara 30 hari sebelum sampai 7 hari setelah event. Ini bukan precision timer. Fungsinya sebagai "alert zone" — saat gap mulai landai, risk/reward untuk maintain leveraged position sudah bergeser.

**Gap magnitude juga diminishing:** Mar 2021 peak gap = +0.024, Jan 2025 peak gap = +0.009. Signal semakin compressed setiap cycle — consistent dengan diminishing returns pattern yang terlihat di seluruh SOPR family.

---

### 11.4 Signal B — Bearish Cross Setelah Local Top: Historical Evidence

| Bearish Cross Date | Harga | Setelah Event | Yang Terjadi Setelahnya |
|---|---|---|---|
| 28 Mar 2021 | $55,808 | Local Top Mar 2021 (+15d) | Mid-Cycle Correction: drop ke $29K (−50%) |
| 28 Apr 2024 | $63,130 | Local Top Mar 2024 (+45d) | Bull dips berturut-turut (Mei, Jul, Agt 2024) |
| 3 Feb 2025 | $101,436 | Local Top Jan 2025 (+14d) | Bull Dip Mar–Apr 2025: drop ke $76K (−25%) |

**Hit rate:** 3/3 — bearish cross setelah local top selalu diikuti koreksi signifikan.

**Caveat severity:** Mar 2021 cross memunculkan mid-cycle correction (−50%), bukan bull dip biasa. Bearish cross sendiri tidak bisa bedakan severity koreksi yang akan terjadi. Perlu combine dengan indikator lain (durasi STH < 0.97 dari Bagian 2, aSOPR level, dll) untuk assess severity.

---

### 11.5 Signal C — Bearish Cross Setelah Cycle Peak: Historical Evidence

| Bearish Cross Date | Harga | Setelah Event | Yang Terjadi Setelahnya |
|---|---|---|---|
| 19 Jan 2018 | $12,037 | Cycle Peak 2017 (+33d) | Lower High Jan 2018, lalu bear market |
| 30 Nov 2021 | $56,995 | Cycle Peak 2021 (+22d) | Lower High Nov-Des 2021, lalu bear market |

**Hit rate:** 2/2 (sample kecil).

**Timing:** Bearish cross dates hampir persis di tanggal Lower High di regime taxonomy. 30 Nov 2021 = Lower High date di data original. Ini bukan coincidence — profitability momentum breakdown dan lower high formation terjadi secara simultan karena driven oleh mekanik yang sama: distribusi sudah selesai, demand baru tidak cukup.

---

### 11.6 Cycle 2025: Jul ATH vs Oct ATH — Bull Trap Thesis

**Observasi kunci dari data:**

Di setiap cycle peak sebelumnya, gap MA90−MA90-MA60 masih POSITIF saat ATH terjadi. Profitability momentum masih intact — harga dan on-chain metrics bergerak bersamaan.

| Event | Gap at ATH | Status | Cross Timing |
|---|---|---|---|
| Cycle Peak Des 2017 | POSITIF (peak +0.022, declining) | ✅ Classic peak | Cross 33d later |
| Cycle Peak Nov 2021 | +0.00691 (declining) | ✅ Classic peak | Cross 22d later |
| Jul–Aug 2025 ATH | +0.00096 (thin, declining) | ⚠️ Marginal | Cross 6d later |
| Oct 2025 ATH $123K | **−0.00152** (ALREADY NEGATIVE) | ❌ Anomalous | Already crossed |

**Oct 2025 ATH terjadi setelah profitability momentum sudah breakdown.** MA90 sudah di bawah MA90-MA60 sejak 18 Agustus. Harga membuat new ATH $123K pada 5–7 Oktober tanpa dukungan profitability structure. Ini definitionally a bull trap: price higher high, momentum lower low.

**Jul–Aug 2025 ATH** menunjukkan pattern yang lebih mirip cycle peak klasik: gap masih positif (+0.00096 meskipun thin), kemudian bearish cross 6d kemudian. Profitability momentum masih intact saat ATH, baru breakdown setelahnya. Ini mirip 2017 dan 2021, hanya jauh lebih compressed (6d vs 22–33d).

**Implikasi kalau thesis ini diadopsi:**

Kalau Jul–Aug 2025 = Structural Cycle Peak:
- Oct 2025 ATH $123K = Bull trap / failed rally (harga di atas Jul ATH tapi tanpa profitability backing)
- Oct 2025 lower high confirmation = regime transition ke bear (sudah terkonfirmasi oleh subsequent price action)
- Ini lebih clean secara on-chain karena menyelesaikan anomali "cycle peak yang terjadi setelah momentum breakdown"

Kalau Oct 2025 = Cycle Peak (current taxonomy):
- Anomali: satu-satunya cycle peak di dataset dimana profitability momentum sudah negative sebelum ATH
- Bisa jadi ini pattern baru yang muncul karena structural changes (ETF, institutional) yang compressed cycle dynamics
- Atau bisa jadi Oct 2025 memang bukan true cycle peak

**Status: OPEN QUESTION.** Kedua framing punya merit. Jul 2025 framing lebih consistent dengan on-chain mechanics tapi belum di-cross-validate dengan indikator lain (MVRV, NUPL, Supply in Profit). Oct 2025 framing mengikuti pure price action. Rekomendasi: validasi thesis ini saat membangun MVRV dan NUPL knowledge base — apakah pattern yang sama terlihat (momentum breakdown sebelum Oct ATH)?

---

### 11.7 Failure Modes & Limitasi

**Failure #1 — Severity tidak bisa dideteksi**
Bearish cross setelah local top tidak membedakan antara bull dip −15% dan mid-cycle correction −50%. Mar 2021 cross menghasilkan −50%, Feb 2025 cross menghasilkan −25%. Perlu combine dengan indikator lain untuk severity assessment.

**Failure #2 — Warning time semakin pendek**
| Cycle | Gap peak → bearish cross |
|---|---|
| 2017 | ~30 hari |
| 2021 | 22 hari |
| 2025 (Jul ATH) | 6 hari |

Market semakin efficient, window untuk act semakin sempit. Di cycle berikutnya, warning time bisa bahkan lebih pendek. Ini reinforces principle: reduce exposure saat gap MULAI declining, jangan tunggu bearish cross.

**Failure #3 — Gap magnitude diminishing**
Peak gap values menurun setiap cycle. Signal semakin subtle. Threshold absolut tidak bisa dipakai lintas cycle — harus selalu relatif terhadap recent readings.

**Failure #4 — Double-smoothing introduces lag**
MA60 dari MA90 sudah sangat lagged. Ini sengaja — fungsinya bukan precision timing tapi regime detection. Tapi artinya: kalau kamu tunggu bearish cross untuk act, kamu sudah kehilangan sebagian besar move. Cross adalah confirmation, bukan trigger. Trigger seharusnya gap declining.

**Failure #5 — Tidak bisa detect exogenous shocks**
COVID crash (15 Mar 2020) muncul sebagai bearish cross di data tapi bukan hasil organic profitability deterioration. Cross terjadi hanya 19 hari setelah gap peak — timeline yang compressed karena external shock, bukan gradual distribution. Signal framework ini assumes organic market mechanics.

---

### 11.8 Integration dengan Framework Lain

Signal ini paling efektif kalau dipakai sebagai salah satu layer dalam multi-signal framework:

| Step | Signal | Action |
|---|---|---|
| 1. Early warning | Gap MA90−MA90-MA60 peaked dan mulai declining | Mulai kurangi loan exposure (Scale down) |
| 2. Confirmation | Bearish cross MA90 di bawah MA90-MA60 | Loan harus sudah reduced signifikan |
| 3. Severity check | Combine dengan STH-SOPR duration < 0.97 (Bagian 2), aSOPR level, EMA55/SMA35 direction (Bagian 9) | Assess apakah ini bull dip, MCC, atau bear onset |
| 4. Regime ID | State D/E framework (Bagian 10), ratio zone | Confirm regime position setelah koreksi |

Cross-reference yang perlu dibangun:
- Apakah MVRV menunjukkan pattern serupa (momentum breakdown sebelum Oct 2025 ATH)?
- Apakah NUPL divergence alignment ada?
- Supply in Profit trajectory selama Jul → Oct 2025 window?

Ini semua masuk ke indicator library documents yang belum dibangun.

---

