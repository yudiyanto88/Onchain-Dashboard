# MVRV FAMILY KNOWLEDGE BASE
## MVRV Z-Score, LTH-MVRV, STH-MVRV — Historical Behavior, Rule Ranges & Failure Modes

**Version:** 1.0  
**Data Source:** ChartInspect.com (Glassnode-sourced)  
**Data Coverage:** Maret 2017 – Mei 2026  
**Last Updated:** 30 Mei 2026

---

## 1. MEKANIK DASAR — APA YANG DIUKUR DAN KENAPA PENTING

### MVRV Z-Score
Membandingkan Market Value (market cap berdasarkan harga spot) dengan Realized Value (market cap berdasarkan harga terakhir setiap coin bergerak on-chain). Z-Score menstandarisasi deviasi ini.

- **Di atas 1.0:** Market secara agregat dalam profit — setiap koin rata-rata bernilai lebih dari harga terakhir pemindahannya.
- **Di bawah 1.0:** Market secara agregat dalam kerugian unrealized.
- **Kenapa penting:** Ini proxy paling langsung untuk "seberapa overvalued atau undervalued market relatif terhadap cost basis agregat semua holder."

### LTH-MVRV (Long-Term Holder MVRV)
Sama seperti MVRV, tapi hanya mengukur coin yang dipegang >155 hari. Mewakili "smart money" atau holder yang sudah melewati satu siklus volatilitas.

- **Kenapa penting:** LTH biasanya mulai distribusi di cycle top dan akumulasi di cycle bottom. LTH-MVRV yang tinggi = profit unrealized LTH besar = tekanan jual potensial tinggi.

### STH-MVRV (Short-Term Holder MVRV)
Hanya mengukur coin yang dipegang <155 hari. Mewakili new money, spekulan, dan late-cycle entrants.

- **Kenapa penting:** STH paling rentan terhadap panic selling karena cost basis mereka dekat dengan harga spot. STH-MVRV < 1.0 berarti short-term buyer rata-rata rugi — ini kondisi yang historically trigger capitulation ATAU buying opportunity, tergantung konteks cycle.

### Hubungan Ketiganya
MVRV Z-Score = weighted average dari keduanya. Ketika STH-MVRV dan LTH-MVRV diverge (satu naik, satu turun), MVRV Z-Score bisa terlihat "normal" padahal ada tekanan besar di bawah permukaan.

---

## 2. HISTORICAL BEHAVIOR PER REGIME — DATA DARI CSV

### 2.1 CYCLE PEAKS

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Cycle Peak 2017 (Des 8-19) | $15,242–$19,538 | 3.79–4.39 | 1.90–2.19 | 28.0–35.6 |
| Cycle Peak 2021 (Okt 20 – Nov 9) | $58,544–$67,525 | 2.56–2.92 | 1.22–1.43 | 3.70–4.24 |
| Cycle Peak 2025 (Okt 5-7) | $121,430–$124,715 | 2.22–2.28 | 1.07–1.10 | 3.30–3.39 |

**Pola konsisten:** MVRV Z-Score selalu di atas 2.0 di semua cycle peak. STH-MVRV selalu di atas 1.0. LTH-MVRV selalu di atas 3.0.

**Perubahan antar cycle (CRITICAL — DIMINISHING RETURNS):**
- MVRV peak: 4.39 → 2.92 → 2.28. Setiap cycle, peak MVRV turun ~35%.
- STH-MVRV peak: 2.19 → 1.43 → 1.10. Turun drastis — di 2025, STH barely profitable di peak.
- LTH-MVRV: 35.6 → 4.24 → 3.39. Anomali 2017 (LTH-MVRV >30) karena pool LTH masih sangat kecil di era awal Bitcoin. 2021 vs 2025 menunjukkan compression yang lebih moderat.

**Leading/lagging behavior sebelum cycle peak:**
- 2017: 30 hari sebelum peak, price +278% tapi MVRV hanya +63%. Divergence masif — harga naik jauh lebih cepat dari MVRV, menandakan overshoot.
- 2021: 30 hari sebelum, price +48% vs MVRV +33%. Price masih outpace MVRV tapi gap lebih kecil.
- 2025: 30 hari sebelum, price +12% vs MVRV +8%. Gap minimal — diminishing euphoria.

**Post-transition behavior:**
- 2017: +30 hari setelah peak, price -36%. MVRV turun dari 3.79 ke 2.08.
- 2021: +30 hari setelah peak, price -29%. MVRV turun dari 2.82 ke 1.95.
- 2025: +30 hari setelah peak, price -17%. MVRV turun dari 2.22 ke 1.81.

### 2.2 LOCAL TOPS (bukan cycle peak — masih ada upside setelahnya)

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Local Top Mar 2021 | $59,107–$61,186 | 3.63–3.78 | 1.57–1.64 | 12.07–12.47 |
| Local Top Apr 2021 (ATH) | $63,007–$63,551 | 3.37–3.43 | 1.43–1.45 | 12.23–12.36 |
| Local Top Mar 2024 (ATH) | $69,504–$73,095 | 2.59–2.75 | 1.27–1.37 | 3.76–3.96 |
| Local Top Des 2024 (ATH) | $91,940–$106,079 | 2.50–2.73 | 1.18–1.33 | 3.71–4.35 |
| Local Top Jan 2025 (ATH) | $99,994–$106,188 | 2.38–2.52 | 1.12–1.18 | 4.07–4.33 |
| Local Top Jul-Aug 2025 (ATH) | $112,571–$123,314 | 2.19–2.41 | 1.06–1.18 | 3.09–3.37 |

**Pola konsisten:** MVRV selalu di atas 2.0. STH-MVRV selalu di atas 1.0. LTH-MVRV selalu di atas 3.0 (kecuali 2021 yang anomali tinggi karena basis LTH kecil).

**Trend diminishing di local tops:**
- 2021 cycle: MVRV peak 3.78 di local top → final cycle peak hanya 2.92 (local top LEBIH TINGGI dari cycle peak di MVRV terms — ini karena bearish divergence)
- 2024-2025 cycle: MVRV local tops turun berurutan: 2.75 → 2.73 → 2.52 → 2.41. Setiap ATH baru punya MVRV lebih rendah.

**CRITICAL OBSERVATION — Bearish Divergence sebagai warning:**
Di 2021, Local Top Apr (ATH $63.5K, MVRV 3.43) punya MVRV lebih rendah dari Local Top Mar ($61K, MVRV 3.78) meskipun harga lebih tinggi. Pola yang sama terulang: Local Top Jul-Aug 2025 (ATH $123K, MVRV 2.41) punya MVRV lebih rendah dari Cycle Peak 2025 yang datang setelahnya ($124K, MVRV 2.28). Ini mungkin membingungkan — saya akan jelaskan di Section 5 (Failure Modes).

**Post-local-top behavior:**
- Sebagian besar local tops diikuti koreksi 5-18% dalam 14 hari, lalu recovery.
- Local Top Apr 2021 → -18% dalam 7 hari, kemudian mid-cycle crash -53%.
- Local Top Jan 2025 → -19% dalam 30 hari.

### 2.3 LOWER HIGH CONFIRM (konfirmasi bahwa top cycle sudah terjadi)

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Lower High 2018 (Jan 1-8) | $13,783–$17,579 | 2.74–3.31 | 1.37–1.62 | 22.0–25.9 |
| Lower High 2019 (Agt 6-8) | $11,487–$11,994 | 2.08–2.16 | 1.27–1.32 | 2.82–2.95 |
| Lower High 2021 (Nov 30 – Des 2) | $56,560–$57,274 | 2.30–2.33 | 1.06–1.07 | 3.52–3.57 |
| Lower High 2025 (Okt 26-28) | $112,964–$114,584 | 2.03–2.06 | 1.00–1.01 | 3.02–3.06 |

**Pola konsisten — STH-MVRV mendekati 1.0 di lower high:** Ini sinyal paling reliable. Di setiap lower high, STH-MVRV berada di range 1.00–1.62 (tapi trend turun tajam dari cycle ke cycle). Di 2025, STH-MVRV = 1.00-1.01 — STH literally di breakeven point.

**Pola konsisten — MVRV selalu lebih rendah dari cycle peak sebelumnya:** Ini definitional, tapi yang penting adalah SEBERAPA JAUH lebih rendah. 2018: peak 4.39 vs lower high 3.31 (gap 1.08). 2025: peak 2.28 vs lower high 2.06 (gap hanya 0.22). Gap yang menyusut membuat deteksi lower high lebih sulit.

**Post-lower-high behavior (ini yang penting — ini konfirmasi bear market):**
- Lower High 2018 → -46% dalam 30 hari.
- Lower High 2019 → -12% dalam 30 hari.
- Lower High 2021 → -16% dalam 7 hari, terus turun.
- Lower High 2025 → -22% dalam 30 hari.

### 2.4 BEAR MARKET DECLINE

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Bear Decline Start 2018 (Mar 6) | $10,849 | 1.97 | 0.97 | 10.31 |
| Bear Decline Mid 2018 (Jun 3) | $7,689 | 1.43 | 0.79 | 2.53 |
| Bear Decline Low 2018 (Jul 2) | $6,604 | 1.27 | 0.81 | 1.70 |
| Bear Decline Mid 2019 (Sep 14-16) | $10,305–$10,419 | 1.79–1.81 | 1.05–1.06 | 2.54–2.57 |
| Bear Market Decline Mid 2022 (Mar 27 – Apr 3) | $45,539–$47,444 | 1.85–1.93 | 0.98–1.02 | 2.52–2.64 |
| Bear Decline Start 2025 (Okt 29) | $110,108 | 1.97 | 0.97 | 2.94 |
| Bear Market Decline Mid 2026 (Jan 14-18) | $93,650–$96,918 | 1.66–1.72 | 0.96–0.99 | 2.40–2.51 |

**Pola konsisten:**
- STH-MVRV selalu < 1.0 atau sangat dekat 1.0 selama bear decline. Ini bukan hanya "STH rugi" — ini indikasi structural: new money yang masuk di dekat top sudah underwater.
- MVRV range 1.27–1.97 selama berbagai fase decline. Belum "murah" (< 1.0), tapi sudah compressed.
- LTH-MVRV tetap > 1.0 sampai sangat dekat bear bottom — LTH masih profit selama sebagian besar bear market.

**Eerie similarity: Bear Decline Start 2018 vs 2025:** MVRV 1.97 dan STH 0.97 — identik di kedua titik transisi. Ini mungkin coincidence, tapi patut dicatat sebagai reference.

### 2.5 BEAR BOTTOMS

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Bear Bottom 2018 Tier 1 (Des 11-17) | $3,281–$3,580 | 0.70–0.77 | 0.64–0.70 | 0.73–0.80 |
| Bear Bottom Window End (Jan 30 – Feb 6, 2019) | $3,439–$3,528 | 0.77–0.79 | 0.79–0.80 | 0.77–0.79 |
| Bear Bottom 2019 Tier 2 (Nov 25 – Des 18) | $6,854–$7,787 | 1.21–1.37 | 0.76–0.86 | 1.51–1.81 |
| COVID Flash Crash (Mar 13-17, 2020) | $5,108–$5,632 | 0.91–0.99 | 0.65–0.70 | 1.06–1.17 |
| Bear Bottom FTX (Nov 8, 2022) | $18,550 | 0.88 | 0.90 | 0.88 |
| Bear Bottom Actual Low (Nov 21, 2022) | $15,774 | 0.78 | 0.83 | 0.76 |
| Bear Bottom Final Low (Des 19, 2022) | $16,442 | 0.82 | 0.90 | 0.81 |

**Pola paling konsisten di seluruh dataset — "Both Below 1.0" Rule:**
Ketika MVRV Z-Score < 1.0 DAN STH-MVRV < 1.0 DAN LTH-MVRV < 1.0 secara bersamaan, ini adalah sinyal bear bottom paling kuat. Ini terjadi di:
- Bear Bottom 2018: ✅ (MVRV 0.70, STH 0.64, LTH 0.73)
- Bear Bottom Window End 2019: ✅ (MVRV 0.77, STH 0.79, LTH 0.77)
- Pre Detection 2019: ✅ (MVRV 0.90, STH 0.97, LTH 0.88)
- Bear Bottom FTX 2022: ✅ (MVRV 0.88, STH 0.90, LTH 0.88)
- Bear Bottom Actual Low 2022: ✅ (MVRV 0.78, STH 0.83, LTH 0.76)
- Bear Bottom Final Low 2022: ✅ (MVRV 0.82, STH 0.90, LTH 0.81)

**Hit rate: 6/6 — setiap kali ketiga metrik di bawah 1.0 bersamaan, itu adalah bottom zone.** Tidak ada single instance di data ini di mana "all three below 1.0" BUKAN bear bottom.

**Peringatan:** Bear Bottom 2019 Tier 2 dan COVID Flash Crash TIDAK memenuhi "all three below 1.0" (LTH masih > 1.0). Ini menunjukkan bahwa bear bottom bisa terjadi tanpa semua tiga di bawah 1.0, tapi ketika ketiga di bawah 1.0, itu SELALU bottom.

**STH-MVRV sebagai capitulation marker:** Di deep bottoms, STH-MVRV turun ke 0.64-0.70 (2018, COVID). Di moderate bottoms, STH-MVRV di 0.76-0.90. Semakin rendah STH-MVRV, semakin dalam capitulation.

### 2.6 PRE DETECTION & START OF BULL

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Pre Detection 2019 (Mar 21-26) | $3,926–$4,044 | 0.90–0.92 | 0.97–0.99 | 0.87–0.90 |
| Pre Detection 2023 (Jan 10-12) | $17,444–$18,853 | 0.88–0.96 | 0.98–1.06 | 0.86–0.93 |
| Start of Bull 2019 (Apr 25) | $5,249 | 1.19 | 1.23 | 1.17 |
| Start of Bull 2023 (Feb 10-12) | $21,632–$21,863 | 1.09–1.10 | 1.12–1.13 | 1.08–1.09 |

**Pola kunci — STH-MVRV leads:**
Di kedua pre-detection events, STH-MVRV mendekati atau menembus 1.0 SEBELUM MVRV Z-Score dan LTH-MVRV. Ini karena short-term buyers yang masuk di dekat bottom menjadi profitable duluan ketika harga mulai naik — cost basis mereka rendah dan fresh.

- Pre Detection 2019: STH 0.97-0.99, sudah hampir 1.0, sementara LTH masih 0.87-0.90.
- Pre Detection 2023: STH 0.98-1.06, sudah menembus 1.0 duluan, LTH masih 0.86-0.93.

**Start of Bull confirmation = semua tiga di atas 1.0:**
- Start of Bull 2019: MVRV 1.19, STH 1.23, LTH 1.17 — semua di atas 1.0.
- Start of Bull 2023: MVRV 1.09, STH 1.12, LTH 1.08 — semua di atas 1.0 tapi tipis.

**Post-start-of-bull performance:**
- 2019: +120% dalam 60 hari (Start of Bull Apr → Upper Range Jun $12.8K).
- 2023: +14% dalam 30 hari (Start of Bull Feb → bull dip Mar lalu rebound).

### 2.7 BULL DIPS

Ini kategori dengan sample terbanyak (15 events). Saya kelompokkan berdasarkan cycle phase.

**Early Cycle Bull Dips (sebelum ATH tertembus):**

| Event | MVRV | STH-MVRV | LTH-MVRV |
|-------|------|----------|----------|
| Bull Dip Jun 2020 | 1.54–1.61 | 1.04–1.08 | 1.85–1.92 |
| Bull Dip Sep 2020 | 1.62–1.77 | 0.98–1.07 | 2.04–2.24 |
| Bull Dip Mar 2023 | 1.02–1.13 | 1.02–1.13 | 1.02–1.13 |
| Bull Dip Jun 2023 | 1.25–1.35 | 0.95–1.03 | 1.35–1.46 |
| Bull Dip Aug-Sep 2023 | 1.24–1.37 | 0.90–0.98 | 1.36–1.51 |
| Bull Dip Jan 2024 | 1.75–1.84 | 1.02–1.08 | 2.09–2.20 |

**Mature Cycle Bull Dips (setelah ATH tertembus):**

| Event | MVRV | STH-MVRV | LTH-MVRV |
|-------|------|----------|----------|
| Bull Dip Mar 2017 | 1.79–2.15 | 0.94–1.12 | 2.90–3.47 |
| Bull Dip Jul 2017 | 2.07–2.47 | 0.93–1.11 | 5.31–6.41 |
| Bull Dip Sep 2017 | 2.57–2.84 | 1.23–1.37 | 11.48–12.54 |
| Bull Dip Jan 2021 | 2.59–3.44 | 1.18–1.57 | 6.28–8.13 |
| Bull Dip Mei 2024 | 2.02 | 0.98 | 3.15 |
| Bull Dip Jul 2024 | 1.81–1.89 | 0.87–0.91 | 2.83–2.95 |
| Bull Dip Agt 2024 (Yen Carry) | 1.72–1.85 | 0.83–0.89 | 2.58–2.78 |
| Bull Dip Sep 2024 | 1.72–1.78 | 0.87–0.90 | 2.20–2.29 |
| Bull Dip Mar-Apr 2025 | 1.74–2.01 | 0.82–0.94 | 2.91–3.46 |

**Pola PALING RELIABLE di bull dips — STH-MVRV < 1.0:**
Di 12 dari 15 bull dips, STH-MVRV turun di bawah 1.0 selama dip. Tiga pengecualian: Bull Dip Sep 2017 (STH 1.23-1.37, masih sangat early/parabolic phase), Bull Dip Mar 2023 (STH 1.02-1.13, barely above), dan Bull Dip Jan 2024 (STH 1.02-1.08, barely above).

**Interpretasi:** STH-MVRV < 1.0 berarti short-term buyer rata-rata underwater — mereka yang beli dalam beberapa bulan terakhir rata-rata rugi. Historically, ini trigger beli yang baik DI DALAM BULL MARKET. Tapi ini juga terjadi di mid-cycle correction bottom 2021 (STH 0.67-0.78) dan bahkan di bear market, jadi konteksnya penting.

**Post-bull-dip performance (selection):**
- Bull Dip Mar 2017 → +163% dalam 30 hari (ke $2,572)
- Bull Dip Sep 2020 → +27% dalam 30 hari (ke $12,935)
- Bull Dip Mar 2023 → +40% dalam 30 hari (ke $28,352)
- Bull Dip Jan 2024 → +29% dalam 30 hari (ke $51,577)
- Bull Dip Sep 2024 → +27% dalam 30 hari (ke $69,893)
- Bull Dip Mar-Apr 2025 → +27% dalam 30 hari (ke $105,756)

### 2.8 MID-CYCLE CORRECTION (2021 — unique event)

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Mid-Cycle Start (May 8) | $59,074 | 2.95 | 1.25 | 10.94 |
| Mid-Cycle Bottom (Jun 22 – Jul 21) | $29,837–$35,888 | 1.54–1.84 | 0.67–0.78 | 3.19–4.45 |

**Ini menunjukkan limitasi bull dip rules:** Di bottom mid-cycle correction, MVRV turun ke 1.54 dan STH-MVRV ke 0.67 — lebih rendah dari beberapa bear market checkpoints. Harga turun -53% dari ATH. Kalau hanya lihat MVRV dan STH-MVRV tanpa konteks, ini bisa disalahartikan sebagai bear market.

**Pembeda mid-cycle correction vs bear market:** LTH-MVRV masih 3.19-4.45 — sangat tinggi. Di bear market aktual, LTH-MVRV turun jauh lebih rendah (< 2.0 typically, < 1.0 di bottom). LTH yang masih sangat profitable di tengah crash = mereka belum mulai distribusi massal = bull market belum selesai.

### 2.9 UPPER RANGE RECOVERY

| Event | Harga | MVRV | STH-MVRV | LTH-MVRV |
|-------|-------|------|----------|----------|
| Upper Range 2019 (Failed) | $12,830 | 2.55 | 1.74 | 3.08 |
| Upper Range Mar 2023 | $29,454–$30,496 | 1.48–1.53 | 1.26–1.32 | 1.55–1.61 |
| Upper Range Jun-Jul 2023 | $29,930–$31,481 | 1.47–1.54 | 1.07–1.13 | 1.61–1.70 |

**Upper Range 2019 failed — kenapa penting:**
MVRV 2.55 dan STH 1.74 di Upper Range 2019 terlihat sangat overheated untuk fase recovery. Bandingkan dengan Upper Range 2023 yang MVRV hanya 1.47-1.54. Harga 2019 naik terlalu cepat (3x dalam 2 bulan) tanpa konsolidasi yang cukup, membuat metrics overshoot. Setelah Upper Range 2019, harga turun -23% dalam 30 hari dan berlanjut ke mini bear market.

**Lesson:** Upper range recovery yang sehat punya MVRV 1.4-1.6 dan STH 1.0-1.3. Kalau metrics sudah mendekati level local top (MVRV > 2.0, STH > 1.5), waspada — ini bisa jadi "too far too fast."

---

## 3. RULE RANGES — SELL SIGNALS

### Rule S1: "Cycle Peak Warning" — MVRV Z-Score > 2.2 + STH-MVRV > 1.05 + bearish divergence (harga ATH tapi MVRV lebih rendah dari ATH sebelumnya)

**Trigger history:**
- 2017: MVRV peaked di 4.39, STH 2.19 — triggered, tapi threshold 2.2 sudah jauh terlampaui. Sell di 2.2 = sell di ~$6,600 (awal Nov 2017), missed 196% upside ke $19.5K. Threshold terlalu dini di 2017.
- 2021: MVRV peaked di 2.92 (Nov 8). Threshold 2.2 sudah triggered sejak Okt 20 ($66K). Kalau sell di trigger, keluar di $66K. Cycle peak $67.5K — missed ~2% upside. Timing bagus.
- 2025: MVRV peaked di 2.28 (Okt 5). Threshold 2.2 triggered di Okt 5 ($123.5K). Cycle peak $124.7K — missed ~1% upside. Timing sangat baik.

**Bearish divergence confirmation:**
- 2021: Local Top Apr MVRV 3.43 > Cycle Peak MVRV 2.92. ATH baru, MVRV lebih rendah. Divergence confirmed.
- 2025: Local Top Jul-Aug MVRV 2.41 > Cycle Peak MVRV 2.28. ATH baru ($124K vs $123K), MVRV lebih rendah. Divergence confirmed.

**Hit rate:** 2/2 di cycle yang bisa diuji (2021, 2025). Threshold 2.2 terlalu rendah untuk 2017.

**False signals:** MVRV > 2.2 juga terjadi di:
- Local Top Mar 2024 (MVRV 2.73): Kalau sell di sini, missed seluruh rally ke $124K. FALSE SIGNAL sebagai cycle peak indicator, tapi VALID sebagai local top indicator.
- Local Top Des 2024 (MVRV 2.70): Sama — koreksi 20% lalu rally ke $124K. FALSE sebagai cycle peak.
- Bull Dip Jan 2021 (MVRV 3.44 di recovery): Ini tricky — MVRV tinggi tapi itu recovery bounce dari dip, bukan top.

**Perbaikan: MVRV > 2.2 PLUS bearish divergence** mengurangi false signals secara signifikan. Tanpa divergence check, MVRV > 2.2 sering trigger di local tops yang bukan cycle peak. DENGAN divergence check, hit rate 2/2 untuk cycle peaks.

**Cost of being wrong:**
- Sell terlalu early (di local top, bukan cycle peak): opportunity cost 20-80% upside tergantung timing.
- Not selling (miss the signal): drawdown 50-80% kalau itu memang cycle peak.
- **Risk asymmetry favors selling partially:** kalau salah (sell di local top), re-entry masih mungkin karena harga biasanya turun 10-20% dari local top sebelum rally lagi. Kalau benar, avoid 50%+ drawdown.

### Rule S2: "Local Top Warning" — MVRV > 2.5 + STH-MVRV > 1.15

**Trigger history:**

| Trigger | MVRV | STH | Setelahnya |
|---------|------|-----|-----------|
| Local Top Mar 2021 | 3.78 | 1.64 | -3% 7d, +8% 30d ke ATH baru |
| Local Top Apr 2021 | 3.43 | 1.45 | -18% 7d, -26% 30d → mid-cycle crash |
| Local Top Mar 2024 | 2.73 | 1.37 | -8% 7d, -5% 30d, lalu recovery |
| Local Top Des 2024 | 2.73 | 1.33 | -11% 7d, -13% 14d, lalu recovery |
| Local Top Jan 2025 | 2.52 | 1.18 | -7% 7d, -19% 30d |
| Cycle Peak 2021 | 2.92 | 1.43 | -10% 7d, -29% 30d |
| Cycle Peak 2025 | 2.28 | 1.10 | STH hanya 1.10 — TIDAK trigger S2 |

**Hit rate sebagai "koreksi minimal 5% dalam 14 hari":** 5/6 triggered events melihat koreksi >5% dalam 14 hari. Local Top Mar 2021 hanya turun 3% dalam 7 hari lalu rebound — ini false signal untuk take-profit.

**CRITICAL PROBLEM:** Cycle Peak 2025 TIDAK trigger S2 karena STH-MVRV hanya 1.10, di bawah threshold 1.15. Ini menunjukkan diminishing returns membuat fixed thresholds tidak reliable di cycle baru.

**Cost of being wrong:** Sell di local top → 10-20% koreksi terjadi, bisa re-buy lower. Upside risk kalau ternyata bukan local top = miss 5-15% rally sementara.

### Rule S3: "Lower High Sell" — STH-MVRV turun ke 1.00-1.01 + MVRV > 2.0 + harga di bawah ATH

**Trigger history:**
- Lower High 2021 (STH 1.06, MVRV 2.30, harga $57K vs ATH $67K): Triggered. Setelahnya: -16% 7 hari, terus turun ke bear market. CORRECT.
- Lower High 2025 (STH 1.01, MVRV 2.06, harga $114K vs ATH $124K): Triggered. Setelahnya: -22% 30 hari, terus turun ke bear market. CORRECT.
- Lower High 2018 (STH 1.37-1.62, MVRV 2.74-3.31): STH terlalu tinggi, rule ini TIDAK triggered di 2018. Perlu adjustable threshold.

**Hit rate:** 2/2 di 2021 dan 2025. Tidak applicable di 2018 karena STH terlalu tinggi.

**False signals:** None dalam dataset. Tapi sample size kecil (n=2).

**Cost of being wrong:** Kalau sell di suspected lower high dan ternyata harga rally ke ATH baru, opportunity cost bisa 10-20%. Tapi historically, ketika harga membuat lower high setelah cycle peak candidates, recovery ke ATH baru belum pernah terjadi (0/2 di data).

---

## 4. RULE RANGES — BUY SIGNALS

### Rule B1: "Deep Bear Bottom" — MVRV < 0.85 + STH-MVRV < 0.90 + LTH-MVRV < 1.0

**Trigger history:**

| Trigger | MVRV | STH | LTH | Setelahnya |
|---------|------|-----|-----|-----------|
| Bear Bottom 2018 (Des 14) | 0.70 | 0.64 | 0.73 | +15% 7d, +6% 14d, sideways |
| Bear Bottom Window 2019 (Feb 2) | 0.79 | 0.80 | 0.79 | +6% 7d, +17% 14d |
| Bear Bottom FTX (Nov 8, 2022) | 0.88 | 0.90 | 0.88 | -9% 7d (masih turun!), -13% 14d |
| Bear Bottom Actual Low (Nov 21, 2022) | 0.78 | 0.83 | 0.76 | +3% 7d, +8% 14d |
| Bear Bottom Final (Des 19, 2022) | 0.82 | 0.90 | 0.81 | +3% 7d, +26% 30d |

**Hit rate sebagai "dalam 3 bulan harga sudah jauh lebih tinggi":** 5/5. Setiap kali semua tiga metrik di bawah threshold ini, itu bottom zone — meskipun timing exact bottom bisa off beberapa minggu.

**CRITICAL FALSE SIGNAL — FTX Collapse:** Rule triggered di Nov 8 ($18.5K) tapi harga turun lagi ke $15.7K — 15% drawdown lebih lanjut. **Ini bukan berarti rule salah (memang bottom zone), tapi menunjukkan bahwa "bottom zone" ≠ "exact bottom."** Harus expect drawdown tambahan 10-20% setelah trigger.

**Cost of being wrong:** Kalau buy di trigger dan harga turun lagi 15-20%, posisi temporarily underwater tapi historically recover within 2-3 bulan. Opportunity cost of NOT buying: miss 50-100%+ rally dari bottom.

### Rule B2: "Bull Dip Buy" — STH-MVRV < 0.95 + MVRV > 1.4 + LTH-MVRV > 2.0

**⚠ UPDATED 31 Mei 2026 — Rule ini jauh lebih lemah dari yang awalnya diklaim. Full backtesting menunjukkan masalah serius.**

Kriteria ini trigger 40 kali di dataset. Dari 40 trigger, hanya 13 menghasilkan return positif >5% dalam 30 hari. **27 trigger menghasilkan return negatif atau flat.** Precision mentah: 32.5%. Ini TIDAK cukup baik untuk dijadikan standalone buy signal.

**Kenapa awalnya terlihat bagus:** Versi pertama knowledge base hanya mengecek trigger terhadap events yang sudah di-label sebagai "Bull Dip" — cherry-picking yang sudah diketahui hasilnya. Ketika di-scan comprehensively (setiap hari di dataset yang memenuhi kriteria), false signals muncul di mana-mana.

**False signal categories:**

*1. Early bear market (MVRV masih > 1.4 tapi sudah post-peak):*
- Des 2021 – Apr 2022: 8 trigger ranges, semua menghasilkan -10% sampai -53% dalam 30 hari. Ini terjadi karena setelah cycle peak Nov 2021, MVRV turun dari 2.9 ke ~2.0 TAPI masih di atas 1.4 selama berbulan-bulan. Rule terus trigger "buy the dip" padahal ini bear market.
- Okt 2025 – Jan 2026: 3 trigger ranges, -14% sampai -27%. Pattern identik — post-cycle-peak, MVRV declining tapi masih > 1.4.

*2. Mini-bear / failed rally 2019:*
- Okt-Nov 2019: 4 trigger ranges setelah Lower High 2019, menghasilkan -15% sampai -21%.

**Proposed fixes dan hasilnya:**

*Fix 1: "MVRV < 1.4 dalam 90 hari terakhir → reject"*
Accuracy: 60%. Precision: 44.8%. Ini catch 2018 false signals (MVRV sudah turun ke < 1.4) tapi MISS 2021-2022 dan 2025-2026 (MVRV belum turun ke < 1.4 saat bear market dimulai). **Fix ini tidak cukup.**

*Fix 2: "MVRV pernah > 2.2 dalam 120 hari terakhir DAN sekarang < 2.2 → reject"*
Zero false positives (tidak pernah membeli di bear market), TAPI zero true positives (filter out SEMUA bull dip juga). Ini karena di 2024-2025 cycle, bull dips juga terjadi setelah MVRV pernah > 2.2. Filter terlalu agresif.

*Combined Fix 1+2:*
Sama dengan Fix 2 — masih zero true positives. Overfit.

**Fundamental problem yang terungkap:**

Ketiga metrik (MVRV, STH-MVRV, LTH-MVRV) alone TIDAK BISA membedakan "bull dip" dari "awal bear market" ketika MVRV masih di range 1.5-2.0. Profilnya identik:

| Metric | Bull Dip Jul 2024 | Bear Decline Des 2021 |
|--------|-------------------|----------------------|
| MVRV | 1.81-1.89 | 1.91-2.02 |
| STH | 0.87-0.91 | 0.89-0.93 |
| LTH | 2.83-2.95 | 2.90-3.07 |
| 30d return | -0.4% to +22% | -15% to -21% |

Angkanya hampir identik, outcome-nya berlawanan total. Ini bukan soal "threshold yang salah" — ini batas fundamental dari apa yang bisa dijawab oleh MVRV family tanpa konteks tambahan.

**Apa yang BISA membantu (tapi butuh data di luar CSV ini):**
- Exchange Net Flows: bull dip biasanya disertai outflow (accumulation), bear rally disertai inflow (distribution)
- Funding rates: bull dip biasanya punya funding negatif (shorts overleveraged), bear rally punya funding positif
- Apakah harga sudah membuat lower high setelah ATH (regime S3/Lower High confirm) — ini bisa dites dari data yang ada dan historically sangat reliable sebagai "ini bukan dip, ini bear"

**Revised recommendation untuk B2 — UPDATED 1 Jun 2026:**

Dari comprehensive scan 14 STH-MVRV < 1.0 dip points, satu hal yang perfectly membedakan 9 works dari 5 exceptions adalah regime: semua exceptions terjadi post cycle peak atau post lower high — artinya market sudah bukan bull market. Semua works terjadi dalam bull market yang masih intact.

Ini bukan "filter" — ini definisi. B2 adalah bull dip rule. Kalau regime sudah bukan bull, B2 not applicable. Masalahnya adalah **MVRV, STH-MVRV, dan LTH-MVRV sendiri tidak bisa mengkonfirmasi apakah regime masih bull atau sudah bear** ketika MVRV berada di range 1.5–2.0. Profilnya identik:

| Metric | Bull Dip Jul 2024 | Bear Decline Des 2021 |
|--------|-------------------|----------------------|
| MVRV | 1.81–1.89 | 1.91–2.02 |
| STH | 0.87–0.91 | 0.89–0.93 |
| LTH | 2.83–2.95 | 2.90–3.07 |
| 30d return | +22% | -21% |

**Kesimpulan yang jujur: B2 tidak bisa membedakan bull dip dari bear onset menggunakan MVRV family saja.** Untuk menggunakan B2 dengan confidence, kamu perlu konfirmasi regime dari indikator lain — Exchange Net Flows, SOPR, atau price structure (apakah harga sudah membuat lower high setelah ATH). Tanpa konfirmasi itu, B2 adalah ambiguous signal, bukan buy signal.

Tier system tetap valid sebagai framework gradasi risk, tapi tier apapun hanya applicable kalau regime sudah dikonfirmasi bull oleh indikator di luar MVRV family.

### Rule B3: "Pre-Bull Accumulation" — STH-MVRV crossing above LTH-MVRV dari bawah + keduanya mendekati 1.0

**Trigger history:**
- Bear Bottom Window 2019: STH 0.79-0.80 vs LTH 0.77-0.79. STH > LTH — keduanya near 1.0. Crossover confirmed.
- Pre Detection 2023: STH 0.98-1.06 vs LTH 0.86-0.93. STH sudah crossing above LTH. Crossover confirmed.

**Kenapa ini penting:** Normalnya LTH-MVRV > STH-MVRV (LTH punya cost basis lebih rendah karena beli lebih lama). Ketika STH overtakes LTH, ini berarti: (a) LTH sudah distribusi cukup banyak di bear sehingga realized price mereka naik, atau (b) STH baru masuk di dekat bottom dengan cost basis yang rendah. Keduanya bullish signals.

**LTH/STH Ratio di transisi:**
- Bear bottoms: LTH/STH ratio ≈ 0.90–1.15 (convergence, almost equal)
- Pre detection: LTH/STH ratio ≈ 0.88–0.94 (STH starting to lead)
- Start of bull: LTH/STH ratio ≈ 0.95–0.97 (still near parity)
- Bull market: ratio diverges → LTH/STH typically 1.5–10+ (LTH much more profitable)

**Hit rate:** 2/2. Sample kecil tapi logikanya sound.

### Rule B5: "STH-MVRV crosses above MVRV SMA30" — Pre-Detection / Bear Bottom Exit signal

**Added 1 Jun 2026. Grid search result: SMA30 dengan filter STH < 1.10.**

**Mekanik:** Hitung SMA 30 hari dari MVRV Z-Score. Signal trigger ketika STH-MVRV cross dari bawah ke atas SMA30 tersebut, DAN nilai STH-MVRV saat crossing < 1.10.

**Logika:** STH-MVRV lebih responsif dari MVRV karena pool-nya lebih kecil dan turnover lebih cepat. Di bear market dalam, STH jatuh lebih cepat dari MVRV. Ketika STH mulai recover dan cross di atas SMA MVRV, ini menandakan STH — cohort yang paling tertekan — mulai outperform rata-rata 30 hari. Filter STH < 1.10 memastikan cross ini terjadi di zona bear/recovery, bukan di bull market yang sudah berjalan.

**Grid search results — semua windows yang ditest:**

| SMA | Crossings | True | False | Precision | Lead PD | Lead SoB |
|-----|----------|------|-------|-----------|---------|---------|
| SMA14 | 7 | 5 | 2 | 71% | 20d / 53d | 82d / 84d |
| SMA21 | 6 | 4 | 2 | 67% | 17d / 48d | 79d / 79d |
| **SMA30** | **4*** | **4** | **0** | **100%** | **14d / 45d** | **76d / 76d** |
| SMA60 | 3* | 2 | 1 | 67% | 14d / 41d | 76d / 72d |
| SMA90 | 2* | 2 | 0 | 100% | 7d / 17d | 69d / 48d |
| SMA120 | 2* | 2 | 0 | 100% | MISS / MISS | 61d / 30d |

*dengan filter STH < 1.10 applied

SMA30 dipilih karena: precision 100%, catch semua 4 target events, lead time paling awal (14–76d), dan tidak melewatkan Pre Detection seperti SMA120.

**Historical crossings SMA30 (filtered, STH < 1.10):**

| # | Date | Price | STH | 90d Return | Context |
|---|------|-------|-----|-----------|---------|
| 1 | 20 Des 2018 | $4,156 | 0.822 | -1.2% | ALERT — fired before actual bottom ($3,281) |
| 2 | 8 Feb 2019 | $3,673 | 0.847 | +108.3% | CONFIRM — 50d after #1, 14d before Pre Detection 2019 |
| 3 | 28 Okt 2022 | $20,596 | 0.971 | +11.8% | ALERT — pre-FTX collapse, harga lanjut turun |
| 4 | 26 Nov 2022 | $16,453 | 0.874 | +41.0% | CONFIRM — 29d after #3, 45d before Pre Detection 2023 |

**Two-cross pattern yang konsisten:**

Crossing pertama sering fired sebelum actual price bottom — 90d return bisa negatif atau tipis positif. Crossing kedua (setelah harga sempat lebih rendah lagi, lalu recover dan cross ulang) adalah yang lebih reliable. Gap antar crossing: 29–50 hari.

Praktisnya: crossing pertama = kurangi short exposure / mulai watchlist. Crossing kedua = mulai accumulation.

**Perbedaan lead time per target:**
- Pre Detection 2019: crossing ke-2 terjadi 14 hari sebelumnya
- Pre Detection 2023: crossing ke-2 terjadi 45 hari sebelumnya
- Start of Bull 2019: crossing ke-2 terjadi 76 hari sebelumnya
- Start of Bull 2023: crossing ke-2 terjadi 76 hari sebelumnya

Signal ini adalah **leading indicator** — muncul sebelum Pre Detection dan jauh sebelum Start of Bull Confirmation.

**Current state (20 Mei 2026):**
STH-MVRV: 0.991. MVRV SMA30: 1.452. Gap: -0.461 (-31.8%). Belum ada crossing. Gap melebar dari -0.36 (21 Apr) ke -0.46 (20 Mei) — SMA30 masih tinggi karena loaded nilai-nilai dari bull run 2024–2025. Untuk crossing terjadi, butuh STH naik DAN SMA30 terus compressing. Tidak ada crossing imminent di data saat ini.

**Limitations:**
- Dataset hanya 2 complete bear market cycles (2018–2019 dan 2022–2023). n=2 per pattern.
- False crossings setelah Start of Bull (SMA tanpa filter) menunjukkan rule ini harus dimatikan setelah bull market confirmed — hanya relevan di zona bear/recovery.
- SMA30 terus-menerus bergeser — level SMA yang dibutuhkan akan berbeda setiap hari.

### Rule B4: "STH-MVRV Bullish Divergence" — Dip baru punya STH-MVRV ≤ dip sebelumnya, harga lebih tinggi

**Added 1 Jun 2026.**

Kalau harga membuat higher low tapi STH-MVRV membuat equal/lower low, short-term holders di harga lebih tinggi punya unrealized loss yang sama atau lebih besar dari dip sebelumnya. Market de-foamed relatif terhadap harga — demand menyerap supply lebih efisien di harga yang lebih tinggi.

**Rule berlaku di dalam bull market yang sudah confirmed (setelah Start of Bull Confirmation, sebelum lower high terkonfirmasi).** Di luar kondisi itu, B4 tidak applicable — bukan karena butuh filter tambahan, tapi karena pertanyaan "bull dip atau bear onset" memang tidak bisa dijawab oleh STH-MVRV divergence sendirian.

**Evidence — 5 confirmed divergences dalam bull market:**

| Pair | STH₁ → STH₂ | Price₁ → Price₂ | 90d return |
|------|-------------|----------------|-----------|
| Apr 2018 → Mar 2020 | 0.635 → 0.591 | $6,964 → $4,837 | +89% |
| Sep 2020 → Jul 2021 | 0.985 → 0.666 | $10,127 → $29,837 | +100% |
| Mar 2023 → Aug-Sep 2023 | 1.023 → 0.898 | $20,214 → $25,179 | +74% |
| Aug-Sep 2023 → Sep 2024 | 0.898 → 0.870 | $25,179 → $53,998 | +84% |
| Sep 2024 → Apr 2025 | 0.870 → 0.823 | $53,998 → $76,270 | +53% |

5/5 positive. N kecil, tapi pattern konsisten dan logikanya sound.

**Cara pakai:**
1. Regime sudah confirmed bull (prerequisite — bukan bagian dari rule ini)
2. Dip sedang terjadi, STH-MVRV compressed
3. Bandingkan STH sekarang dengan dip terakhir dalam cycle yang sama
4. Kalau STH₂ ≤ STH₁ dengan harga lebih tinggi → divergence confirmed, tambah confidence untuk entry
5. Kalau STH₂ > STH₁ → bukan divergence, rule tidak trigger, tidak perlu dianalisis lebih lanjut

**Catatan:** Reference dip harus dari cycle yang sama (setelah Start of Bull Confirmation terakhir). Cross-cycle comparison tidak apple-to-apple.

---

## 5. FAILURE MODES — KAPAN METRIK INI GAGAL ATAU MISLEADING

### 5.1 MVRV Z-Score Failures

**Failure Mode 1: Diminishing cycle peaks membuat fixed thresholds obsolete.**
MVRV peak: 4.39 → 2.92 → 2.28. Threshold yang benar di satu cycle terlalu tinggi atau rendah di cycle berikutnya. "MVRV > 3.0 = overheated" benar di 2017 dan 2021, tapi kalau diterapkan ke 2025, sinyal TIDAK PERNAH trigger dan kamu miss seluruh cycle peak.

*Implikasi: Setiap cycle perlu threshold yang di-recalibrate. Rule-of-thumb: expect MVRV cycle peak ~30-35% lebih rendah dari cycle sebelumnya.*

**Failure Mode 2: MVRV bisa stay elevated untuk waktu lama.**
Bull Dip Sep 2017: MVRV di 2.57-2.84. Ini terlihat "overheated" — tapi harga naik 261% dalam 30 hari setelahnya (ke cycle peak). MVRV tinggi ≠ immediate sell signal dalam parabolic phase.

**Failure Mode 3: MVRV identik di fase yang sangat berbeda.**
Bear Decline Start 2018: MVRV 1.97. Bear Decline Start 2025: MVRV 1.97. Bull Dip Mei 2024: MVRV 2.02. Tiga konteks yang sangat berbeda, MVRV hampir identik. **MVRV alone cannot distinguish between bear decline start vs bull dip** — butuh STH-MVRV dan LTH-MVRV sebagai context.

### 5.2 STH-MVRV Failures

**Failure Mode 1: STH < 1.0 bisa berarti "buy the dip" ATAU "ini baru awal bear."**
STH < 1.0 di Bull Dip Jul 2024 (0.87) → harga naik 22% dalam 14 hari. BENAR.
STH < 1.0 di Bear Market Decline Mid 2022 (0.98) → harga turun 58%. SALAH kalau dipakai sebagai buy signal.

**Pembedanya:** Cek apakah MVRV trend-nya naik atau turun. Di bull dip, MVRV baru saja turun tajam dari level tinggi (mean reversion). Di bear market, MVRV sudah dalam downtrend sustained.

**Failure Mode 2: STH-MVRV threshold terus turun di cycle peaks.**
STH di Cycle Peak 2017: 2.19. Di 2021: 1.43. Di 2025: 1.10. Kalau pakai threshold "STH > 1.5 = overheated," threshold ini benar di 2017 dan 2021 tapi NEVER triggered di 2025. Rule S2 (STH > 1.15 untuk local top) juga gagal catch Cycle Peak 2025 karena STH hanya 1.10.

*Ini failure mode paling berbahaya karena membuat kamu think "metrics belum overheated" padahal cycle peak sudah terjadi.*

**Failure Mode 3: STH-MVRV bisa sangat volatile short-term.**
STH-MVRV bergerak lebih cepat dari MVRV karena pool-nya lebih kecil dan turnover lebih cepat. Ini berarti noise lebih tinggi — satu hari bisa swing 5-10% di STH-MVRV tanpa implikasi structural.

### 5.3 LTH-MVRV Failures

**Failure Mode 1: LTH-MVRV di 2017 secara structural berbeda dari cycle lain.**
LTH-MVRV mencapai 35.6 di 2017 vs 4.24 di 2021 vs 3.39 di 2025. Ini bukan diminishing returns normal — pool LTH di 2017 sangat kecil dan dominated oleh early adopter yang beli di < $100. Metrics dari 2017 LTH-MVRV tidak bisa langsung dibandingkan dengan cycle lain.

**Failure Mode 2: LTH-MVRV slow-moving → terlalu lagging untuk tactical decisions.**
Contoh: Di awal mid-cycle correction 2021, LTH-MVRV masih 10.94 padahal harga sudah turun dari $63K ke $59K. LTH-MVRV baru turun ke 3.19 setelah crash ke $30K — saat itu sudah terlambat sebagai sell signal. LTH-MVRV leading ability: LOW. Mostly useful sebagai confirmation dan context, bukan timing.

**Failure Mode 3: LTH-MVRV bisa create false sense of security.**
Di Bear Market Decline Mid 2022 (Mar-Apr), LTH-MVRV masih 2.52-2.64. Ini terlihat "LTH masih profit, berarti bull market" — tapi itu mid-bear rally. LTH-MVRV tetap > 1.0 untuk sebagian besar bear market dan baru turun di bawah 1.0 sangat dekat bottom. **Jadi LTH-MVRV > 1.0 ≠ bull market confirmed.**

### 5.4 Ranking: Mana yang paling sering gagal?

**STH-MVRV paling sering memberikan ambiguous signals** (12 instances di data di mana STH < 1.0 tapi outcome sangat berbeda — kadang buy, kadang bear). Ini bukan karena metric-nya buruk — justru karena STH-MVRV responsive, dia react ke semua dips termasuk yang tidak meaningful.

**MVRV Z-Score paling terpengaruh diminishing returns** — fixed thresholds dari cycle lalu hampir pasti salah di cycle baru. Ini membuatnya unreliable JIKA dipakai dengan fixed numbers tanpa adjustment.

**LTH-MVRV paling lagging** — rarely wrong tapi sering terlambat. Useful sebagai confirmer dan context-setter, kurang useful sebagai primary signal.

### 5.5 Apa yang bisa membuat threshold historis tidak berlaku di cycle berikutnya?

1. **Continued compression of MVRV peaks.** Kalau trend 4.39 → 2.92 → 2.28 berlanjut, cycle berikutnya bisa peak di ~1.5-1.8. Di level itu, sangat sulit membedakan cycle peak dari bull dip.

2. **ETF inflows mengubah holder composition.** ETF holders technically LTH setelah 155 hari, tapi perilaku mereka berbeda dari on-chain LTH tradisional. ETF share terus bertambah, potensially mengubah mekanik LTH-MVRV.

3. **Structural de-leverage.** Kalau bear market 2025-2026 cukup severe, realized price bisa naik significantly (karena banyak coin terliquidasi dan berpindah tangan di harga tinggi). Ini bisa membuat MVRV di cycle berikutnya dimulai dari baseline yang berbeda.

4. **Inflation of STH cost basis.** DCA culture dan ETF auto-buy membuat STH cost basis lebih stabil dan lebih tinggi. STH-MVRV mungkin tidak turun se-rendah di cycle sebelumnya bahkan di bear market.

---

## 6. INTERAKSI ANTAR KETIGA METRIK

### 6.1 Kapan ketiganya sejalan — dan artinya

**Semua naik bersamaan:** Healthy bull trend. Terjadi di awal-mid bull market (Q4 2020, Feb-Mar 2024, Mei-Jun 2025). Artinya semua cohort profiting dan belum ada structural stress.

**Semua turun bersamaan:** Bear market atau deep correction. Terjadi di bear markets (2018, 2022, late 2025-2026). Artinya semua cohort losing value — no support.

**Semua di bawah 1.0:** Bear bottom (lihat Section 2.5). 6/6 hit rate sebagai bottom signal.

### 6.2 Divergences — yang paling penting

**Divergence 1 (MOST DANGEROUS): Harga naik ke ATH baru tapi MVRV lebih rendah dari ATH sebelumnya.**

Ini "bearish divergence" paling reliable di dataset:
- 2021: Local Top Mar MVRV 3.78 → Local Top Apr (higher price) MVRV 3.43. Gap: -0.35.
- 2024-2025: MVRV di successive ATHs: 2.73 → 2.73 → 2.52 → 2.41 → 2.28. Declining trend.

*Interpretasi: Setiap ATH baru membutuhkan lebih banyak modal relatif terhadap cost basis. Market makin "expensive" relatif ke realized value, meskipun harga masih naik nominally.*

**Divergence 2: STH-MVRV turun sementara LTH-MVRV masih tinggi.**

Ini terjadi di:
- Awal mid-cycle correction 2021: STH 1.25 → 0.67, LTH 10.94 → 3.19. STH collapsed sementara LTH masih very profitable.
- Bull dips 2024: STH turun ke 0.83-0.90, LTH masih 2.2-3.1.
- Bear Decline Start 2025: STH 0.97, LTH 2.94. STH underwater tapi LTH masih very comfortable.

*Interpretasi: STH capitulation tanpa LTH distribution = likely bull dip, bukan bear market. TAPI kalau STH stays < 1.0 untuk prolonged period DAN LTH mulai turun juga, itu transisi ke bear.*

**Divergence 3: LTH-MVRV turun tajam sementara STH-MVRV stabil.**

Ini terjadi di:
- Bear Decline Mid 2018: LTH crashed dari 10.3 ke 2.5 (dalam ~3 bulan), STH hanya turun dari 0.97 ke 0.79.
- Bear Market 2022: LTH turun dari 2.64 ke 0.76 over 7 bulan, STH range-bound 0.83-1.02.

*Interpretasi: LTH distribusi masif (selling at loss eventually). STH yang stabil berarti new money masih masuk tapi LTH offloading ke mereka. Ini bearish — late bear sign.*

**Divergence 4 (Pre-bull signal): STH-MVRV crossing ABOVE LTH-MVRV.**

Dibahas di Rule B3. Signal transition dari bear ke bull.

### 6.3 Kombinasi paling reliable per regime transition

| Transition | Primary Signal | Confirmation | Weight |
|-----------|---------------|--------------|--------|
| Bear Bottom → Pre-Bull | All three < 1.0, STH crossing above LTH | MVRV trending up from < 0.85 | Sangat tinggi |
| Start of Bull | All three > 1.0 | STH > LTH (baru cross) | Tinggi |
| Bull Dip (buy) | STH < 0.95, MVRV > 1.4, LTH > 2.0 | MVRV rapid drop dari level tinggi | Medium-High (ada false signal di early bear) |
| Local Top (reduce) | MVRV > 2.5, STH > 1.15 | Bearish divergence vs prev local top | Medium (threshold terus turun) |
| Cycle Peak (sell) | MVRV > 2.2 + bearish divergence | STH starting to decline dari peak | Medium (n=2) |
| Lower High (sell aggressif) | STH ~1.0, harga < ATH, MVRV < cycle peak MVRV | MVRV declining trend | Tinggi (2/2, tapi n=2) |
| Bear Market Confirm | STH sustained < 1.0, MVRV declining | LTH starting to decline | Tinggi |

---

## 6A. VELOCITY ANALYSIS — KECEPATAN PERUBAHAN SEBAGAI SINYAL TAMBAHAN

**Added: 31 Mei 2026. Analisis rate of change per hari untuk ketiga metrik, mengungkap empat pola yang tidak terlihat dari analisis level saja.**

### Finding 1: ASYMMETRY INVERSION DI CYCLE PEAKS — pola paling striking

Rasio kecepatan decline vs kecepatan rise (14 hari sebelum dan sesudah cycle peak):

| Cycle | MVRV rise/day | MVRV fall/day | Asym Ratio | Interpretasi |
|-------|--------------|---------------|------------|-------------|
| 2017 | +0.142 | -0.060 | 0.43x | Naik JAUH lebih cepat dari turun |
| 2021 | +0.025 | -0.032 | 1.27x | Turun sedikit lebih cepat dari naik |
| 2025 | +0.008 | -0.019 | 2.23x | Turun 2x lebih cepat dari naik |

**Trend: 0.43x → 1.27x → 2.23x.** Ini inversioning structural. Di 2017, MVRV naik parabolic dan turun gradual — tipikal blow-off top. Di 2025, MVRV naik gradual dan turun cepat — tipikal "tired rally yang kehabisan fuel."

STH-MVRV menunjukkan pattern yang sama (0.43x → 1.49x → 1.97x), tapi sedikit lebih damped dibanding MVRV.

**Implikasi practical:** Di cycle mendatang, kalau pattern ini berlanjut, cycle peak kemungkinan besar BUKAN blow-off top klasik (parabolic rise lalu crash). Lebih mungkin gradual grind up, plateau, lalu decline yang lebih cepat dari kenaikannya. Ini mengubah bagaimana kamu harus mendeteksi peak — bukan cari parabolic euphoria, tapi cari stagnasi momentum di level elevated.

**Implikasi untuk risk management:** Kalau decline dua kali lebih cepat dari kenaikan, window untuk react setelah peak semakin sempit. Sell rules harus proactive (sebelum peak), bukan reactive (setelah peak terlihat).

### Finding 2: LTH-MVRV leads hampir di SEMUA regime transition (kecuali satu)

Siapa yang bergerak paling cepat (% perubahan terbesar per hari) menuju transisi:

| Regime | Leader masuk transisi | Leader keluar transisi |
|--------|----------------------|----------------------|
| Cycle Peak | LTH (2/3) | Mixed |
| Local Top | LTH (5/6) | MVRV (4/6) |
| Lower High | LTH (4/5) | LTH (4/5) |
| Bear Decline | LTH (3/5) | LTH (5/5) |
| Bear Bottom | LTH (6/6) | **STH (5/6)** |
| Pre Detection / Start Bull | **STH (3/4)** | LTH (4/4) |
| Bull Dip | Mixed (STH 6, LTH 5, MVRV 3) | Mixed |

**Dua exceptions yang sangat meaningful:**

Pertama — **Bear Bottom: LTH leads masuk, STH leads keluar.** LTH bergerak paling cepat MENUJU bottom (distribusi/capitulation LTH accelerates ke bottom), tapi STH bergerak paling cepat KELUAR dari bottom (new buyers yang beli murah langsung masuk profit). Ini konsisten dengan mekanik market: LTH capitulation marks the bottom, STH accumulation marks the recovery.

Kedua — **Pre Detection: STH leads masuk transisi.** Ini satu-satunya regime dimana STH consistently leads. Ini karena pre-detection terjadi ketika new buyers mulai masuk dan STH cost basis bergerak duluan (fresh purchases di dekat bottom = STH realized price naik cepat). LTH masih duduk di cost basis lama, belum bergerak.

**Implikasi practical:** Kalau kamu melihat LTH-MVRV mulai turun paling cepat di antara ketiganya, itu LTH sedang distribusi. Di local top dan lower high, ini consistently terjadi. Sebaliknya, kalau STH-MVRV mulai naik paling cepat dari zona rendah, itu early accumulation signal.

### Finding 3: RECOVERY VELOCITY SEBAGAI BOTTOM QUALITY INDICATOR

7-hari post-bottom MVRV velocity vs 30-hari price return:

| Event | 7d MVRV vel | 7d STH vel | 30d return | Real bottom? |
|-------|------------|-----------|-----------|-------------|
| COVID Flash Crash | +0.032 | +0.023 | +63% | ✅ |
| Bull Dip Mar 2017 | +0.126 | +0.035 | +163% | ✅ |
| Bull Dip Mar 2023 | +0.051 | +0.045 | +40% | ✅ |
| Bull Dip Jun 2023 | +0.034 | +0.024 | +21% | ✅ |
| Bull Dip Jan 2024 | +0.018 | +0.008 | +29% | ✅ |
| Bull Dip Sep 2024 | +0.019 | +0.010 | +27% | ✅ |
| Bear Bottom FTX | **-0.010** | **-0.005** | -7% | ❌ delayed |
| Bull Dip Aug-Sep 2023 | +0.009 | +0.007 | +4% | ❌ weak |

**Pattern: Ketika MVRV 7d velocity positif > +0.015 setelah dip/bottom, 30d return selalu positif > 20%.** Ini 6/6 di data.

Ketika velocity negatif (FTX: -0.010) atau sangat lemah (Aug-Sep 2023: +0.009), recovery either gagal atau sangat lambat.

**Threshold potensial: MVRV 7d velocity > +0.015/hari** sebagai "recovery confirmation." Ini bisa menjadi filter tambahan untuk Rule B2 — alih-alih buy di dip, wait for recovery velocity confirmation.

**Caveat penting:** Ini mengorbankan entry timing. Kalau tunggu 7 hari untuk velocity confirmation, kamu sudah miss 5-15% dari rally. Trade-off: miss awal rally tapi avoid false bottoms seperti FTX (-7% lanjutan) dan Aug-Sep 2023 (flat months).

### Finding 4: LOWER HIGH DECLINE PATTERN — FRONT-LOADED DROP

Setelah lower high confirmed, decline velocity per hari:

| Event | 7d rate | 14d rate | 30d rate | Pattern |
|-------|---------|---------|---------|---------|
| 2018 | -0.043 | -0.058 | -0.043 | Accelerates lalu stabil |
| 2019 | -0.041 | -0.023 | -0.010 | Decelerates (front-loaded) |
| 2021 | -0.050 | -0.025 | -0.015 | Decelerates (front-loaded) |
| 2025 | -0.021 | -0.012 | -0.016 | Decelerates (front-loaded) |

**3 dari 4 lower high menunjukkan front-loaded decline** — 7 hari pertama setelah lower high adalah drop terbesar per hari, lalu melambat.

**Implikasi:** Kalau kamu mendeteksi lower high (Rule S3), 7 hari pertama adalah window paling kritikal untuk action. Setelah itu, decline biasanya melambat (tapi tetap turun). Ini relevan untuk LTV management — kalau ada posisi loan saat lower high terdeteksi, 7 hari pertama adalah danger zone terbesar.

**Exception: 2018 lower high.** Decline accelerated dari 7d ke 14d. Ini mungkin karena 2018 lower high masih di MVRV 3.31 (sangat tinggi), sehingga ada lebih banyak "room to fall." Lower highs di MVRV yang lebih rendah (2021: 2.33, 2025: 2.06) cenderung front-loaded.

---

## 6B. LTH/STH RATIO DEEP DIVE

**Added: 31 Mei 2026. LTH-MVRV dibagi STH-MVRV — mengukur seberapa besar keuntungan relatif long-term holders vs short-term holders.**

Ratio > 1.0 = LTH lebih profitable dari STH (normal di bull market).
Ratio < 1.0 = STH lebih profitable dari LTH (hanya terjadi di sekitar bear bottom dan awal bull).
Ratio naik = spread antara LTH dan STH melebar (LTH makin untung relatif ke STH).
Ratio turun = spread menyempit (convergence — bisa bearish atau transitional).

### Finding 1: RATIO LIFECYCLE — Peta jalan satu cycle penuh

Dari bear bottom ke cycle peak ke bear bottom berikutnya, ratio selalu mengikuti trajectory yang sama:

**2022-2025+ Cycle (trajectory lengkap):**

| Phase | Ratio | Zone |
|-------|-------|------|
| Bear Decline Mid 2022 | 2.57 | Moderate spread — masih dari cycle sebelumnya |
| Bear Bottom FTX | 0.98 | ◆ Convergence — LTH dan STH hampir sama |
| Bear Bottom Actual Low | 0.92 | ◆ Convergence — STH mulai lebih profitable |
| Bear Bottom Final | 0.90 | ◆ Convergence — titik terendah ratio |
| Pre Detection 2023 | 0.88 | ◆ Convergence — STH leads, LTH belum recover |
| Start of Bull 2023 | 0.97 | ◆ Convergence — mulai converge kembali ke 1.0 |
| Bull Dip Mar 2023 | 1.01 | ○ Near parity — baru cross 1.0 |
| Bull market develops | 1.2 → 1.5 → 2.0 → 3.0 | Expanding — LTH makin outperform |
| Local Top Mar 2024 | 2.95 | △ Moderate spread |
| Bull Dips 2024 | 3.0 → 3.2 → 2.5 | ▲ High spread, mulai oscillate |
| Local Top Des 2024 | 3.14 | ▲ High spread |
| Local Top Jan 2025 | 3.67 | ▲ High spread, peak ratio cycle ini |
| Local Top Jul-Aug 2025 | 2.92 | Ratio sudah turun dari peak ← DIVERGENCE |
| Cycle Peak 2025 | 3.09 | ▲ High spread tapi sudah declining trend |
| Lower High 2025 | 3.02 | ▲ Declining |
| Bear Decline 2025-2026 | 3.0 → 2.5 → 1.6 | Compressing kembali menuju convergence |

**Pola yang terulang di kedua cycle:**
Ratio turun ke < 1.0 di bear bottom, naik selama bull market, peak di pertengahan/akhir bull, lalu turun kembali menuju convergence. Ini "breathing pattern" — inhale (spread widens) selama bull, exhale (spread compresses) selama bear.

### Finding 2: RATIO < 1.0 — Marker transisi paling clean

Ratio di bawah 1.0 (STH lebih profitable dari LTH) HANYA terjadi di:
- Bear Bottom 2018/2019: ratio 0.90–0.98
- Bear Bottom 2022: ratio 0.88–0.98
- Pre Detection / Start of Bull: ratio 0.88–0.97

**Zero occurrences di bull market, mid-cycle correction, atau bear decline.** Ini membuat "ratio < 1.0" menjadi salah satu marker paling definitive bahwa kamu di deep bear territory atau sangat awal bull.

**Kenapa ini terjadi:** Di bear bottom, LTH yang masih hold dari cycle sebelumnya punya cost basis yang relatif tinggi (mereka beli di bull market lalu). STH yang baru masuk di dekat bottom punya cost basis rendah. Ketika harga mulai recover dari bottom, STH-MVRV naik duluan karena cost basis mereka dekat harga saat ini. LTH-MVRV naik lebih lambat karena cost basis mereka masih jauh di atas.

**Pre Detection 2023 special case:** Ratio 0.88 dengan STH 1.006 (di atas 1.0) tapi LTH 0.887 (di bawah 1.0). Ini berarti STH sudah profit tapi LTH masih rugi — "new money outperforming old money." Ini historically sangat bullish karena artinya wealth transfer dari seller lama ke buyer baru sudah terjadi.

### Finding 3: RATIO DIRECTION DI BULL DIP — Sinyal paling kuat yang ditemukan

Apakah ratio NAIK atau TURUN saat memasuki bull dip? Ini ternyata sangat predictive:

| Ratio direction 14d pre-dip | Positive 30d return | Hit rate |
|-----------------------------|---------------------|----------|
| RISING ↑ | 10/10 | **100%** |
| FALLING ↓ | 2/5 | 40% |

**100% hit rate ketika ratio rising into dip.** Ketika LTH/STH ratio naik sementara harga turun (dip), artinya LTH-MVRV turun lebih sedikit dari STH-MVRV. Secara mekanis ini berarti LTH tidak panik sell (mereka hold, cost basis stabil), sementara STH yang capitulate. Ini structural signature dari "healthy dip in bull market."

Ketika ratio falling into dip, artinya LTH-MVRV juga turun cepat — LTH juga distributing. Ini ambiguous: kadang temporary (40% masih recover) tapi kadang tanda transisi ke bear (60% tidak recover dalam 30 hari).

**TAPI — caveat penting dari comprehensive B2 scan:**

Ketika saya test ratio direction sebagai filter untuk B2 rule di SELURUH dataset (bukan hanya labeled bull dips), hasilnya:
- Ratio rising + B2 triggered: 2 true positives, 0 false positives. **100% precision tapi hanya catch 2 dari 13 true dips** (15% recall).
- Ratio falling + B2 triggered: 11 true dips + 27 false signals = **29% precision**.

**Interpretasi:** Ratio rising saat B2 trigger = sangat aman untuk buy (100% precision), tapi jarang terjadi. Ratio falling saat B2 trigger = kamu tidak bisa tahu tanpa konfirmasi tambahan. Ini masih meningkatkan framework — sekarang kamu punya satu scenario (ratio rising) di mana bisa act with high confidence, dan satu scenario (ratio falling) yang explicitly membutuhkan konfirmasi dari indikator lain.

### Finding 4: CYCLE PEAK vs LOCAL TOP — Ratio tidak bisa membedakan

| Event | Ratio | Ratio 14d trend |
|-------|-------|----------------|
| Local Top Mar 2021 | 7.67 | +0.59 ↑ |
| Local Top Apr 2021 | 8.56 | +0.42 ↑ |
| Cycle Peak 2021 | 3.05 | +0.19 ↑ |
| Local Top Mar 2024 | 2.95 | +0.61 ↑ |
| Local Top Des 2024 | 3.14 | +0.50 ↑ |
| Local Top Jan 2025 | 3.67 | +0.10 ↑ |
| Local Top Jul-Aug 2025 | 2.92 | +0.13 ↑ |
| Cycle Peak 2025 | 3.09 | +0.04 ↑ |

Semua menunjukkan ratio rising. Tidak ada level ratio atau trend speed yang consistently membedakan cycle peak dari local top.

**Satu observation yang worth monitoring tapi belum bisa jadi rule (n terlalu kecil):** Ratio 14d trend di cycle peaks (+0.19 dan +0.04) LEBIH KECIL dari local tops (+0.10 sampai +0.61). Cycle peaks punya momentum ratio yang lebih lemah — ratio barely rising. Ini mungkin karena di cycle peak, STH-MVRV sudah turun hampir sebanyak LTH-MVRV, jadi ratio stagnant. Tapi n=2 untuk cycle peaks, jadi ini observation bukan rule.

### Finding 5: CURRENT STATE (20 Mei 2026) — Ratio 1.61, declining

Ratio 1.61 dengan trajectory turun (dari ~3.0 di Okt 2025).

Historical matches untuk ratio ~1.6:
- COVID Bottom Flash Crash (ratio 1.65): tapi STH jauh lebih rendah (0.68 vs current 0.99). Konteks berbeda.
- Halving 2020 (ratio 1.67): STH 1.06, LTH 1.77 — mirip current state. Ini adalah mid-recovery period.
- Bull Dip Aug-Sep 2023 (ratio 1.54): STH 0.92, LTH 1.42 — juga mirip.

Yang paling mirip overall: antara Halving 2020 context dan late-2023 bull dip territory. Ratio declining dari high spread menuju moderate spread — ini konsisten dengan bear market compression tapi belum di convergence zone (< 1.0) yang menandakan bear bottom.

---

## 7. MAPPING KE REGIME CATEGORIES

| Regime | MVRV Z-Score | STH-MVRV | LTH-MVRV | Confidence |
|--------|-------------|----------|----------|------------|
| 1. Cycle Peak | > 2.2 + divergence | > 1.05 (tapi turun) | > 3.0 (tapi turun) | Medium — thresholds terus turun |
| 2. Local Top | > 2.4 | > 1.15 | > 3.0 | Medium — 2025 peak terlalu rendah untuk trigger |
| 3. Upper Range Recovery | 1.4–2.0 | 1.0–1.3 | 1.5–2.5 | Medium |
| 4. Bull Dip | Drop dari elevated, masih > 1.4 | < 0.95 (temporarily) | > 2.0 (masih tinggi) | Medium-High — need context |
| 5. Mid-Cycle Correction | 1.5–1.9 (sharp drop) | 0.65–0.80 (severe) | > 3.0 (masih tinggi) | Low — hanya 1 sample (2021) |
| 6. Lower High Confirm | < cycle peak MVRV, masih > 2.0 | ~1.0 (breakeven) | > 3.0 tapi declining | High (2/2 tapi n=2) |
| 7. Bear Market Decline | 1.2–2.0 declining | < 1.0 sustained | 2.0–3.0 declining | High |
| 8. Bear Bottom Near | < 0.85 | < 0.90 | < 1.0 | Very High (6/6) |
| 9. Pre Detection Start of Bull | 0.85–0.95, rising | ~1.0, crossing above LTH | < 0.95, below STH | High |
| 10. Start of Bull Confirmation | > 1.0, all three | > 1.0 | > 1.0 | High |

### Red Flags yang harus trigger immediate attention:

1. **STH-MVRV turun di bawah 0.95 saat ada posisi leverage aktif** — ini bisa mean bull dip (buy) ATAU bear start (cut loss). LTV buffer harus dicek SEGERA sebelum analisis lain.

2. **Bearish divergence di successive ATHs** — harga ATH baru tapi MVRV lebih rendah. Ini historically precedes cycle peak atau major correction 100% of the time di data ini.

3. **All three below 1.0** — ini bear bottom territory. Jangan panic sell, ini accumulation zone. Tapi juga jangan all-in karena masih bisa turun 15-20% (contoh: FTX Nov 2022).

4. **LTH-MVRV mulai declining dari > 3.0 secara sustained** — LTH distribution. Ini late cycle warning, bukan immediate sell tapi alert level harus naik.

---

## 8. KONDISI SAAT INI — STATUS CHECK (Data terakhir: 20 Mei 2026)

**Readings terkini:**
- BTC: $77,563
- MVRV: 1.428
- STH-MVRV: 0.991
- LTH-MVRV: 1.592

**Assessment berdasarkan framework:**

MVRV 1.43 berada di range yang historically match dengan: Bear Decline Mid 2018 (1.43), early recovery zones, atau compressed bull dip levels. Tanpa konteks, angka ini ambiguous.

STH-MVRV 0.99 — sangat dekat 1.0. STH barely profitable. Ini bisa berarti:
- Baru masuk accumulation setelah bear decline (bullish interpretation)
- Masih dalam downtrend dan belum bottomed (bearish interpretation)

LTH-MVRV 1.59 — LTH masih profitable tapi sudah compressed signifikan dari 3.4 (Okt 2025). Ini menunjukkan distribusi sudah terjadi atau realized price naik.

**Konteks dari trajectory:** Setelah Cycle Peak Okt 2025, harga turun dari $124K ke $62.8K (Feb 5 2026, MVRV 1.14 — terendah di dataset current cycle). Recovery ke $77K (+23% dari low).

**Best match regime:** Bear Market Decline to early recovery zone. Belum confident ini bear bottom karena "all three below 1.0" belum tercapai (LTH masih 1.59). Tapi MVRV sudah turun ke 1.14 (Feb 5) yang mendekati bear market zones dari cycle sebelumnya.

**⚠ CONFIDENCE NOTE:** Current positioning assessment punya high uncertainty karena:
- Diminishing returns trend membuat historical thresholds mungkin tidak applicable
- Data hanya sampai Mei 2026 — masih dalam bear decline trajectory
- LTH-MVRV belum menunjukkan capitulation pattern (< 1.0) yang historically mark definitive bottoms

---

## 9. LIMITATIONS DOCUMENT INI

1. **Sample size fundamental:** Hanya 3 complete cycles (2013-2017, 2017-2021, 2021-2025+). Statistical significance terbatas. Setiap "rule" berdasarkan n=2 sampai n=6. Jangan treat sebagai definitive.

2. **Data gaps:** CSV tidak continuous — ada gaps antar event periods. Analisis before/after bisa miss intermediate price action yang penting.

3. **Survivorship bias:** Kita hanya lihat cycles yang selesai. Structural break (hyper-bitcoinization, government ban, new asset class displacement) tidak ada di dataset.

4. **Diminishing returns mungkin nonlinear:** Saya assume ~30-35% compression per cycle di MVRV peak. Ini bisa accelerate atau decelerate unpredictably.

5. **ETF structural change belum fully reflected:** 2024-2025 cycle pertama dengan significant ETF presence. Holder composition berubah — metrics bisa behave differently going forward.

6. **LTH-MVRV 2017 anomaly:** Semua rule ranges yang melibatkan LTH-MVRV sebaiknya exclude 2017 data atau treat sebagai outlier karena pool size yang berbeda secara fundamental.

---

## CHANGELOG

- v1.0 (30 Mei 2026): Initial version dari CSV data analysis. 51 transition points analyzed. Rule ranges proposed dengan hit rates dan failure modes. Framework siap untuk iterasi berdasarkan weekly analysis.
- v1.1 (31 Mei 2026): B2 rule dikoreksi setelah comprehensive backtesting — precision turun dari claimed "6/7" ke actual 32.5% ketika di-scan terhadap seluruh dataset. "Butuh data tambahan" claim removed karena salah. Tiga-tier confidence system diperkenalkan menggunakan LTH/STH ratio direction sebagai filter.
- v1.1 (31 Mei 2026): Section 6A (Velocity Analysis) ditambahkan — cycle peak asymmetry inversion, LTH leadership pattern, recovery velocity threshold, lower high front-loaded decline.
- v1.1 (31 Mei 2026): Section 6B (LTH/STH Ratio Deep Dive) ditambahkan — ratio lifecycle mapping, ratio < 1.0 sebagai bear bottom marker, ratio direction sebagai bull dip quality filter (100% precision saat rising, 29% saat falling).
- v1.3 (1 Jun 2026): Rule B5 ditambahkan — grid search STH-MVRV cross above MVRV SMA(N). SMA30 dengan filter STH < 1.10 optimal: 100% precision, 0 false signals, lead 14–76d sebelum Pre Detection / Start of Bull. Two-cross pattern documented (cross 1 = alert, cross 2 = confirm). Current state: STH 0.991 vs SMA30 1.452, gap -31.8%, no crossing imminent.
- v1.3 (1 Jun 2026): B4 exceptions table dihapus — bukan bullish divergence dari awal, tidak relevan dibahas sebagai failure case. "No peak in 120d" di B2 dikoreksi: bukan filter teknikal, itu definisi regime. Kesimpulan yang lebih jujur: B2 dan B4 tidak bisa membedakan bull dip dari bear onset menggunakan MVRV family saja — butuh regime confirmation dari indikator lain.
