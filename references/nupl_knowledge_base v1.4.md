# NUPL Family Knowledge Base — NUPL, LTH-NUPL, STH-NUPL

**Version:** 1.4
**Data source:** ChartInspect.com (Glassnode-sourced)
**Data Coverage:** 2016 – Jun 2026  
**Last Updated:** 20 Jun 2026

---

## 1. DEFINISI DAN MEKANIK

### 1.1 NUPL (Net Unrealized Profit/Loss)

Mengukur total unrealized profit atau loss seluruh market relatif terhadap market cap. Secara konseptual: "Kalau semua holder jual sekarang, apakah secara aggregate mereka profit atau loss?"

Komponen perhitungan: (Market Cap − Realized Cap) / Market Cap. Market Cap = harga sekarang × total supply. Realized Cap = setiap coin dinilai di harga terakhir kali berpindah on-chain (proxy untuk cost basis rata-rata market).

NUPL > 0 berarti secara aggregate market sedang dalam unrealized profit. NUPL < 0 berarti aggregate unrealized loss — ini historically terjadi hanya di deep bear markets.

### 1.2 LTH-NUPL (Long-Term Holder NUPL)

NUPL yang dihitung hanya untuk coins yang belum berpindah selama >155 hari. Cohort ini mewakili "conviction holders" — orang yang sudah melewati volatilitas dan belum menjual.

LTH-NUPL tinggi berarti long-term holders duduk di atas profit besar. LTH-NUPL rendah atau negatif berarti bahkan holder yang paling sabar pun sedang underwater — historically ini adalah zona capitulation terakhir.

### 1.3 STH-NUPL (Short-Term Holder NUPL)

NUPL untuk coins yang berpindah dalam <155 hari terakhir. Ini mewakili "recent buyers" — orang yang baru masuk atau baru menambah posisi. STH-NUPL jauh lebih volatile dan bereaksi lebih cepat terhadap price movement karena cost basis-nya dekat dengan harga saat ini.

Analogi: LTH-NUPL seperti mood investor senior yang sudah memegang saham bertahun-tahun. STH-NUPL seperti mood pembeli baru yang baru masuk beberapa bulan lalu. Ketika harga turun 20%, senior mungkin masih profit 100%, tapi pembeli baru sudah rugi 20%. Divergence antara keduanya memberi informasi krusial tentang siapa yang sedang stres.

### 1.4 Hubungan Antar Ketiganya

NUPL adalah weighted average dari LTH-NUPL dan STH-NUPL, tertimbang oleh proporsi supply masing-masing. Karena LTH biasanya menguasai mayoritas supply, NUPL cenderung tracking LTH-NUPL lebih dekat, tapi STH-NUPL memberikan early warning yang lebih responsif.

**Dua derived metrics yang penting (dibahas lengkap di Section 9):**

**Gap = LTH-NUPL − STH-NUPL.** Mengukur seberapa jauh jarak profit antara long-term holders dan recent buyers. Gap positif = LTH lebih profitable. Gap negatif = STH lebih profitable dari LTH (sinyal start of bull). Semakin lebar gap positif, semakin fragil market karena marginal buyer tidak punya cushion.

**Ratio = LTH-NUPL / STH-NUPL.** Mengamplifikasi sinyal gap, terutama saat STH mendekati nol. Ratio < 1 (both positive) = early bull fingerprint. Ratio extreme (>50 atau sign flip) = STH di zero-crossing zone, zona transisi kritis. Interpretasi ratio bergantung pada sign keduanya — lihat Section 9.2.

---

## 2. HISTORICAL BEHAVIOR PER REGIME TRANSITION

### 2.1 CYCLE PEAK

**Events dalam data:** Cycle Peak 2017 (Des 8–19), Cycle Peak 2021 (Okt 20 – Nov 9), Cycle Peak 2025 (Okt 5–7)

**Nilai di transition date:**

| Cycle | NUPL | STH-NUPL | LTH-NUPL | Harga |
|-------|------|----------|----------|-------|
| 2017 | 0.768 | 0.534 | 0.967 | $16,349 |
| 2021 | 0.649 | 0.250 | 0.764 | $67,525 |
| 2025 | 0.559 | 0.082 | 0.702 | $123,537 |

**Range selama window event:**

| Cycle | NUPL range | STH range | LTH range | Price range |
|-------|-----------|-----------|-----------|-------------|
| 2017 | 0.736–0.772 | 0.473–0.544 | 0.964–0.972 | $15,242–$19,538 |
| 2021 | 0.609–0.658 | 0.183–0.301 | 0.730–0.764 | $58,544–$67,525 |
| 2025 | 0.549–0.562 | 0.063–0.089 | 0.697–0.705 | $121,430–$124,715 |

**Pola yang konsisten:**
- NUPL dan STH-NUPL peak bersamaan atau sangat dekat dengan price peak. Di 2017 keduanya peak sehari sebelum transition (Des 7). Di 2021 keduanya masih naik hingga Nov 8 (hari pertama window). Di 2025 keduanya peak di hari kedua (Okt 6).
- LTH-NUPL lagging: peak setelah harga. Di 2017, LTH peak 8 hari setelah NUPL/STH peak (Des 16 vs Des 7). Di 2021, LTH masih naik beberapa hari setelah harga peak. Ini masuk akal karena LTH supply bergeser saat coin baru memasuki kategori 155+ hari.
- Setelah transition, STH-NUPL jatuh paling cepat dan paling dalam. 30 hari setelah cycle peak: STH turun dari 0.534 ke ~0.006 (2017), dari 0.250 ke -0.049 (2021), dari 0.082 ke -0.105 (2025). LTH-NUPL turun paling lambat — 30 hari setelah peak, LTH masih di 0.958 (2017), 0.681 (2021), 0.631 (2025).

**Pola yang BERUBAH (diminishing returns) — ini krusial:**

| Metrik | 2017 Peak | 2021 Peak | 2025 Peak | Drop 2017→2021 | Drop 2021→2025 |
|--------|-----------|-----------|-----------|----------------|----------------|
| NUPL | 0.772 | 0.658 | 0.562 | -0.114 | -0.096 |
| STH-NUPL | 0.544 | 0.250 | 0.082 | -0.294 | -0.168 |
| LTH-NUPL | 0.972 | 0.764 | 0.702 | -0.208 | -0.062 |

STH-NUPL mengalami diminishing paling ekstrem — turun 0.29 dari cycle ke cycle di awal, lalu 0.17. Ini reflect bahwa setiap cycle, buying power baru masuk di harga lebih tinggi relatif terhadap sisa upside yang tersedia. LTH diminishing melambat (0.21 → 0.06) — LTH lebih tahan terhadap structural shift karena populasinya lebih stabil.

Implikasi langsung: threshold cycle peak 2017 (NUPL > 0.75) tidak akan pernah tercapai lagi di 2021, dan threshold 2021 (NUPL > 0.65) tidak tercapai di 2025. Fixed threshold untuk sell signal tidak reliable lintas cycle.

STH-NUPL yang paling dramatic: di 2025, bahkan di cycle peak, STH-NUPL hanya 0.082 — artinya rata-rata pembeli baru hampir breakeven di puncak cycle. Ini suggest bahwa setiap cycle, buying power baru masuk di harga yang semakin tinggi relatif terhadap price appreciation yang tersisa.

### 2.2 LOCAL TOP

**Events dalam data:** Local Top Mar 2021, Apr 2021 (ATH), Mar 2024 (ATH), Des 2024 (ATH), Jan 2025 (ATH), Jul-Aug 2025 (ATH)

**Nilai di transition date:**

| Event | NUPL | STH-NUPL | LTH-NUPL | Harga |
|-------|------|----------|----------|-------|
| Mar 2021 | 0.735 | 0.389 | 0.920 | $61,186 |
| Apr 2021 (ATH) | 0.709 | 0.312 | 0.919 | $63,551 |
| Mar 2024 (ATH) | 0.634 | 0.269 | 0.741 | $71,472 |
| Des 2024 (ATH) | 0.634 | 0.249 | 0.748 | $98,402 |
| Jan 2025 (ATH) | 0.583 | 0.111 | 0.755 | $99,994 |
| Jul-Aug 2025 (ATH) | 0.584 | 0.151 | 0.695 | $119,057 |

**Pola konsisten:**
- NUPL di local top berkisar antara 0.58–0.74. Range ini overlap dengan cycle peak range (0.56–0.77), jadi NUPL sendiri tidak bisa membedakan local top dari cycle peak.
- STH-NUPL di 2021 cycle (0.31–0.39) jauh lebih tinggi dari 2024–2025 cycle (0.11–0.27). Diminishing returns pattern lagi.
- LTH-NUPL relatif stabil di 0.69–0.92 — menunjukkan long-term holders masih nyaman. Tapi di 2025 cycle, LTH juga mulai turun ke 0.695, terendah dari semua local tops.

**Yang membedakan local top dari cycle peak:** 30 hari setelah local top, harga biasanya recover atau sideways. Contoh: 30 hari setelah Local Top Mar 2021, harga naik dari $59,107 ke $63,551. 30 hari setelah Local Top Des 2024, harga naik dari $106,079 ke $100,509 (turun 5% — relatif mild). Bandingkan dengan cycle peak: 30 hari setelah Cycle Peak 2021, harga turun dari $66,963 ke $47,671 (-29%).

**Lead/lag:** Di local tops, STH-NUPL mulai menurun 1–2 minggu sebelum harga puncak. 14 hari sebelum Local Top Apr 2021 (ATH), STH sudah turun dari 0.365 ke 0.311. Pattern ini sebagai early warning yang cukup consistent.

**Yang membedakan local top dari cycle peak (retrospektif):** Setelah local top, harga recover dalam 30-60 hari. Setelah cycle peak, harga tidak recover ke high sebelumnya, diikuti lower high formation. **Ini hanya bisa dikonfirmasi retrospektif** — saat sedang terjadi, tidak ada cara membedakan local top dari cycle peak menggunakan NUPL family saja. Harus tunggu apakah harga membuat ATH baru atau membentuk lower high.

### 2.3 LOWER HIGH CONFIRM TOP CYCLE

**Events:** Lower High 2018 (Jan 1–8), 2021 (Nov 30 – Dec 2), 2025 (Okt 26–28, termasuk confirmation Okt 28)

**Nilai di transition date:**

| Event | NUPL | STH-NUPL | LTH-NUPL | LTH-STH Gap |
|-------|------|----------|----------|-------------|
| 2018 | 0.635 | 0.269 | 0.955 | 0.686 |
| 2021 | 0.569 | 0.062 | 0.719 | 0.657 |
| 2025 | 0.515 | 0.013 | 0.674 | 0.661 |
| 2025 (confirmation) | 0.507 | -0.001 | 0.669 | 0.670 |

**Pola konsisten yang sangat kuat:**
- STH-NUPL mendekati nol atau sedikit positif. Di 2021: 0.062, di 2025: 0.013, turun ke -0.001 saat confirmation. Ini artinya short-term buyers sudah hampir breakeven atau sudah loss — mereka tidak punya cushion untuk koreksi berikutnya. Exception: 2018 masih di 0.269, tapi ini karena lower high terjadi sangat cepat setelah cycle peak dan banyak buyer baru masih profit.
- LTH-STH gap sangat lebar (0.657–0.686). Long-term holders masih nyaman, short-term holders sudah borderline. Ini adalah hallmark lower high: disconnect antara veteran dan newbie.
- Setelah lower high, penurunan agresif. 30 hari setelah Lower High 2018: harga turun dari $15,434 ke $8,334 (-46%). 30 hari setelah Lower High 2021: harga turun dari $56,560 ke $44,434 (-21%). 30 hari setelah Lower High 2025: harga turun dari $114,584 ke $88,655 (-22%).

**Pola yang BERUBAH:** Lower high STH values turun per cycle (0.269 → 0.062 → 0.013 → -0.001). Di 2025, STH bahkan menyentuh negatif saat confirmation — short-term buyers sudah loss pada saat lower high terbentuk, bukan hanya borderline breakeven. Lower high NUPL values juga turun (0.635 → 0.569 → 0.515).

**Warning signal sebelum lower high:** 14 hari sebelum, STH-NUPL sudah declining sementara harga mencoba bounce. Di 2025: 14 hari sebelum, STH stagnan di near-zero (0.011 ke 0.013) saat harga masih di $114K–$118K — harga naik tapi STH tidak ikut. Bearish divergence.

**Pattern identifikasi lower high (bukan retrospektif):** Kombinasi yang muncul sebelum lower high dikonfirmasi: (1) STH-NUPL < 0.10 sementara harga masih di sekitar 85–95% dari ATH, (2) STH tidak naik mengikuti price bounce, (3) LTH masih kuat (>0.60) tapi tidak cukup untuk menopang STH yang sudah weak.

### 2.4 BULL DIP

**15 events dalam data, mencakup 3 cycle berbeda (2017, 2020-2021, 2023-2025)**

**Semua instance — nilai di hari pertama event:**

| Event | NUPL | STH-NUPL (entry) | STH min (selama dip) | LTH-NUPL | +30d Price |
|-------|------|-------------------|------------------------|----------|------------|
| Mar 2017 | 0.462 | -0.034 | -0.064 | 0.665 | ▲ (2017 bull lanjut) |
| Jul 2017 | 0.529 | -0.049 | -0.076 | 0.818 | ▲ (2017 bull lanjut) |
| Sep 2017 | 0.601 | 0.171 | -0.052 | 0.911 | ▲ (2017 bull lanjut) |
| Jun 2020 | 0.350 | 0.035 | +0.035 | 0.459 | ▲ moderate |
| Sep 2020 | 0.386 | -0.013 | -0.015 | 0.510 | ▲ moderate |
| Jan 2021 | 0.687 | 0.318 | 0.153 | 0.864 | ▲ strong |
| Mar 2023 | 0.115 | 0.114 | +0.023 | 0.115 | ▲ moderate |
| Jun 2023 | 0.215 | -0.020 | -0.051 | 0.273 | ▲ moderate |
| Agt-Sep 2023 | 0.219 | -0.096 | -0.113 | 0.298 | ▲ moderate |
| Jan 2024 | 0.453 | 0.066 | +0.022 | 0.542 | ▲ strong |
| Mei 2024 | 0.505 | -0.023 | -0.023 | 0.682 | ▲ moderate |
| Jul 2024 | 0.461 | -0.129 | -0.147 | 0.654 | ▲ flat (+0.3%) |
| Agt 2024 (Yen) | 0.460 | -0.128 | -0.203 | 0.640 | ▲ flat (-2.1%) |
| Sep 2024 | 0.439 | -0.109 | -0.150 | 0.564 | ▲ moderate |
| Mar-Apr 2025 | 0.472 | -0.125 | -0.215 | 0.691 | ▲ (lanjut ke local top) |

**Pola yang konsisten:**
- LTH-NUPL selalu positif di setiap bull dip, tanpa exception. Bahkan di bull dips terdalam (Agt 2024 Yen Carry, STH -0.203), LTH masih di 0.640. LTH positif + STH negatif = signature bull dip.
- STH-NUPL negatif di 10 dari 15 bull dips. Ini normal behavior, bukan bear signal. Yang penting LTH tetap positif dan STH recovery ke positif dalam hitungan minggu, bukan bulan.
- Setelah bull dip, harga selalu recover di dataset ini. Tidak ada satu pun instance di mana kondisi LTH > 0.50 dan STH < -0.10 kemudian berlanjut ke full bear market tanpa recovery terlebih dahulu.

**Pola yang BERUBAH:** STH dip depth makin dalam per cycle — 2017 (min -0.076) → 2020-2021 (min -0.015 sampai +0.153) → 2023-2025 (min -0.215). Semakin mature cycle, semakin dalam STH bisa dip karena cost basis pool dari STH semakin tinggi. NUPL range di bull dips juga melebar: 2017 (0.46–0.60) → 2020-2021 (0.35–0.69) → 2023-2025 (0.02–0.51) — range yang sangat lebar menunjukkan bahwa NUPL level absolut tidak berguna untuk mengidentifikasi bull dip, LTH/STH divergence jauh lebih reliable.

**Early cycle vs late cycle bull dips (penting untuk sizing):**

| Type | NUPL typical | STH typical | LTH typical | Recovery speed |
|------|-------------|-------------|-------------|----------------|
| Early cycle (2023) | 0.02–0.26 | -0.11 to +0.11 | 0.11–0.34 | Moderate |
| Mid cycle (2020, Jan 2024) | 0.35–0.46 | -0.02 to +0.07 | 0.46–0.55 | Strong |
| Late cycle (2024 dips, 2025) | 0.42–0.50 | -0.22 to -0.06 | 0.55–0.71 | Flat/moderate |

Late cycle dips (2024) dengan STH < -0.10 tidak selalu produce strong 30-day recovery — Jul dan Agt 2024 masing-masing +0.3% dan -2.1% dalam 30 hari. Context: cycle masih bull tapi harga sideways sebelum breakout.

### 2.5 MID-CYCLE CORRECTION

**Events:** Start (Mei 8, 2021), Bottom (Jun 22 – Jul 21, 2021)

**Nilai di transition dates:**

| Event | NUPL | STH-NUPL | LTH-NUPL | LTH-STH Gap | Harga |
|-------|------|----------|----------|-------------|-------|
| Start (Mei 8) | 0.661 | 0.203 | 0.909 | +0.706 | $59,074 |
| Bottom (Jun 22 – Jul 21) | 0.352–0.458 | -0.502 to -0.283 | 0.687–0.775 | +0.97 to +1.20 | $29,837–$35,888 |

STH-NUPL crash dari 0.203 ke serendah -0.502 adalah drop terbesar dalam dataset selain bear market genuine. LTH-NUPL tidak pernah masuk negatif selama seluruh correction — bahkan di price low $29,837, LTH masih di 0.697. LTH kuat = ini bukan bear market.

LTH-STH gap di bottom mencapai >1.0 (hingga 1.20) — paling lebar di seluruh dataset. Gap >1.0 belum pernah terjadi di regime lain. Ini adalah signature eksklusif mid-cycle correction: STH dalam extreme loss sementara LTH sangat profitable.

**7 hari setelah start:** NUPL turun ke 0.568, STH ke -0.010. STH mendekati nol dalam 7 hari — sangat cepat. 30 hari setelah start: NUPL 0.413, STH -0.397. Dip ini severe dan prolonged (berlangsung 2+ bulan).

**30 hari setelah bottom:** Harga recover dari $29,837–$35,888 ke ~$43,599 (+36% dari low). NUPL naik ke 0.518, STH recover ke 0.019. Bull market resumed.

**Distinguisher kritis vs bear market:**

| Signal | Mid-Cycle 2021 | Bear Market (2018, 2022) |
|--------|---------------|---------------------------|
| STH-NUPL | Sangat negatif (-0.50) | Negatif (-0.57 to -0.12) |
| LTH-NUPL | Tetap positif kuat (0.69–0.78) | NEGATIF (< 0) |
| NUPL | Tetap positif (0.35–0.46) | Negatif (< 0) |

**LTH negatif = bear market. LTH positif = bukan bear market.** Ini satu-satunya distinguisher yang reliable untuk membedakan mid-cycle correction dari genuine bear, terlepas seberapa dalam STH crash.

### 2.6 BEAR MARKET DECLINE

**Events:** Decline markers spanning 2018, 2019, 2022, 2025-2026

**Range nilai:**
- NUPL: 0.214–0.493. Bear decline dimulai saat NUPL masih di area 0.45–0.50, dan turun selama periode decline.
- STH-NUPL: -0.259 sampai 0.060. Kebanyakan negatif — recent buyers sudah loss.
- LTH-NUPL: 0.410–0.903. Masih positif tapi trending down. Di 2018 cycle, LTH masih di 0.903 di awal decline (Maret) tapi turun ke 0.410 di Juli — proses panjang ~4 bulan.

**Pattern kritis — bagaimana bear decline dimulai:**
- Bear Decline Start 2018 (Mar 6): NUPL 0.492, STH -0.036, LTH 0.903. STH sudah negatif sementara LTH masih sangat tinggi. Gap 0.939.
- Bear Decline Start 2022 (Apr): NUPL ~0.47, STH ~-0.10, LTH ~0.63.
- Bear Decline Crash 2022 (Jun, Luna): NUPL negatif, STH deeply negatif, LTH mulai turun ke negatif.
- Bear Decline Start 2025 (Okt 29): NUPL 0.493, STH -0.027, LTH 0.660. STH sedikit negatif, gap 0.686.
- Pattern: bear decline starts saat STH sudah negatif (below cost basis) dan LTH masih >0.60.

**30-day aftermath sangat brutal:**
- Bear Decline Start 2018 → 30d later: NUPL dari 0.492 ke 0.331, harga -25%
- Bear Decline Start 2025 → 30d later: NUPL dari 0.493 ke 0.357, harga -21%
- Bear Market Decline Mid 2022 → 30d later: NUPL dari 0.477 ke -0.084, harga -58% (Luna/USDT crash)
- Bear Market Decline Mid 2026 → 30d later: NUPL dari 0.420 ke 0.187, harga -30%

**Posisi terkini (Jun 2026):** NUPL ~0.355–0.420, masih negatif di STH, LTH ~0.56–0.58 — masih jauh di atas negatif, bear decline belum mencapai fase deep capitulation.

**Distinguisher bear decline dari bull dip:**

| Signal | Bull Dip | Bear Decline |
|--------|----------|---------------|
| LTH-NUPL | > 0.50, tidak trend turun signifikan | Turun progresif, menuju negatif |
| STH duration negatif | < 4 minggu | > 6–8 minggu dan makin dalam |
| Recovery setelah STH dip | STH kembali positif dalam weeks | STH tidak kembali kuat |
| NUPL trend | Sideways/bounce | Turun sustained |

### 2.7 BEAR BOTTOM

**Events:** Bear Bottom 2018 Tier 1, Bear Bottom 2018 Deepest, Window End 2019, FTX Collapse, Actual Price Low, Final Low 2022

**Nilai di transition:**

| Event | NUPL | STH-NUPL | LTH-NUPL | LTH-STH Gap | Harga |
|-------|------|----------|----------|-------------|-------|
| Bear Bottom 2018 Tier 1 (Des 11) | -0.364 | -0.517 | -0.303 | +0.214 | $3,441 |
| Bear Bottom 2018 Deepest (Des 14) | -0.424 | -0.569 | -0.366 | +0.203 | $3,281 |
| Window End (Jan 30, 2019) | -0.274 | -0.266 | -0.278 | +0.012 | $3,510 |
| FTX Collapse (Nov 8, 2022) | -0.135 | -0.115 | -0.140 | -0.025 | $18,550 |
| Actual Price Low (Nov 21, 2022) | -0.288 | -0.206 | -0.309 | -0.103 | $15,774 |
| Final Low (Des 19, 2022) | -0.214 | -0.117 | -0.240 | -0.123 | $16,442 |

**Pattern konsisten:**
- Semua tiga metrik negatif di semua bear bottoms terkonfirmasi (kecuali FTX yang merupakan panic event, bukan price bottom). Ini konfirmasi terkuat bahwa bottom territory sedang terbentuk.
- STH-NUPL selalu negatif di bear bottom, tanpa exception. STH selalu yang pertama masuk negatif dan terakhir keluar negatif.
- Lead/lag di bottoms: di 2018 dan 2022, ketiga metrik bottomed bersamaan atau dalam 1–2 hari. Tidak ada lead/lag signifikan di bottoms — semua capitulate bersamaan. Berbeda dengan pre-recovery dimana STH leads.

**Anomali kritis 2022 — HARUS DIPAHAMI:**

| Cycle | LTH lebih negatif dari STH? | Penjelasan |
|-------|------------------------------|------------|
| 2018 | Tidak (LTH -0.37, STH -0.57, gap +0.20) | STH lebih menderita — normal |
| 2022 | **Ya** (LTH -0.31, STH -0.21, gap -0.10) | LTH lebih menderita — anomali |

Kenapa terbalik di 2022: banyak LTH yang membeli di cycle peak 2021 ($60K–$69K) dan sudah menjadi LTH (>155 hari) saat bottom — cost basis mereka jauh lebih tinggi. Sementara STH yang baru beli setelah crash punya cost basis lebih rendah. Implikasi: "LTH lebih negatif dari STH" di bear bottom adalah sinyal bahwa koreksi dari cycle puncak sangat besar sampai buyer cycle sebelumnya jadi LTH dan masih rugi. Di cycle berikutnya, kalau pattern berlanjut, LTH bisa lebih menderita dari STH lagi.

**Diminishing depth per cycle:**

| Cycle | NUPL bottom | STH bottom | LTH bottom |
|-------|------------|------------|------------|
| 2018 | -0.424 | -0.569 | -0.366 |
| 2022 | -0.288 | -0.206 | -0.309 |
| Trend | Less deep | Less deep | Comparable |

Bear bottom 2022 tidak sedalam 2018. Jika pattern berlanjut, bear bottom berikutnya mungkin NUPL hanya sampai -0.15 to -0.20. Threshold entry "beli saat NUPL < -0.30" akan miss next bear bottom.

### 2.8 PRE DETECTION START OF BULL MARKET

**Events:** Pre Detection 2019 Ref (Feb 22), Pre Detection 2019 (Mar 21–26), Pre Detection 2023 (Jan 10–12)

**Nilai:**

| Event | NUPL | STH-NUPL | LTH-NUPL | Harga |
|-------|------|----------|----------|-------|
| Pre Detection 2019 Ref | -0.121 | -0.072 | -0.141 | $3,943 |
| Pre Detection 2019 | -0.085 | -0.012 | -0.116 | $4,039 |
| Pre Detection 2023 (Jan 10) | -0.132 | -0.022 | -0.161 | $17,444 |
| Pre Detection 2023 (Jan 12) | -0.047 | 0.052 | -0.073 | $18,853 |

**Pattern:**
- NUPL masih negatif tapi sudah mulai naik dari bottom. Range: -0.132 to -0.047.
- STH-NUPL mendekati nol atau sudah positif: -0.072 to +0.052. STH sudah hampir breakeven atau sudah positif — recent buyers mulai untung, tanda bahwa akumulasi terjadi.
- LTH-NUPL masih negatif tapi lebih dalam: -0.161 to -0.073. LTH masih underwater.

**Ciri khas pre-detection:** STH-NUPL recover lebih cepat dari LTH-NUPL. STH mendekati nol atau sudah positif sementara LTH masih -0.07 to -0.16. Ini karena akumulator baru (yang beli di bottom) masuk sebagai STH dan mulai profit, sementara LTH yang beli di cycle sebelumnya masih loss. Selama bear decline biasa, STH dan LTH cenderung turun bersama — di Pre Detection, STH mulai naik (atau berhenti turun) sementara LTH masih stagnant/negative. Divergence ini menandakan accumulation fresh money sedang terjadi.

**7 hari setelah Pre Detection 2019:** STH melompat dari -0.012 ke positive territory. Harga naik signifikan. **14 hari setelah Pre Detection 2023:** NUPL dari -0.132 ke 0.139, STH dari -0.022 ke 0.183. Breakout cepat.

**Lead/lag Pre Detection ke Start of Bull:**

| Pair | STH Pre Det → Start of Bull | NUPL Pre Det → Start of Bull |
|------|-------------------------------|--------------------------------|
| 2019 | ~35 hari | ~35 hari |
| 2023 | ~31 hari | ~31 hari |

Interval konsisten sekitar satu bulan antara Pre Detection dan Start of Bull Confirmation.

### 2.9 START OF BULL MARKET CONFIRMATION

**Events:** Start of Bull 2019 (Apr 25), Start of Bull 2023 (Feb 10–12)

**Nilai:**

| Event | NUPL | STH-NUPL | LTH-NUPL | Harga |
|-------|------|----------|----------|-------|
| 2019 | 0.156 | 0.185 | 0.145 | $5,249 |
| 2023 | 0.082–0.091 | 0.106–0.116 | 0.075–0.085 | $21,632–$21,863 |

**Pattern definitive:**
- Semua tiga metrik positif. Ini adalah first time setelah bear dimana NUPL, STH, dan LTH semuanya positif bersamaan.
- STH-NUPL > LTH-NUPL (0.185 > 0.145 di 2019, 0.106 > 0.075 di 2023). Ini menandakan bahwa recent buyers lebih profitable dari long-term holders — structural shift yang hanya terjadi di early bull.
- Gap STH-LTH negatif atau mendekati nol: -0.040 (2019), -0.031 (2023). Ini berbalik dari gap lebar di bear.
- 30 hari setelah Start of Bull 2019: NUPL ke 0.570, harga naik 120% ($5,249 → $11,528). 30 hari setelah Start of Bull 2023: NUPL ke 0.200, harga naik 14% ($21,790 → $24,764). 2019 jauh lebih explosive — ini juga part of diminishing returns.

**Trigger untuk monitoring:**
- NUPL crossing dari negatif ke positif bukan trigger — itu bisa terjadi sebelum Start of Bull.
- STH crossing ke positif = Pre Detection signal.
- **STH crossing ke atas LTH dan semua tiga metrik positif bersamaan = Start of Bull Confirmation.**

### 2.10 UPPER RANGE RECOVERY

**Events:** Upper Range 2019 (Failed, Jun 26), Upper Range Apr 2023, Upper Range Jun-Jul 2023

**Nilai:**

| Event | NUPL | STH-NUPL | LTH-NUPL | Harga | Status |
|-------|------|----------|----------|-------|--------|
| 2019 (Failed) | 0.608 | 0.425 | 0.676 | $12,830 | Reversal: -23% dalam 30d |
| Apr 2023 | 0.347 | 0.243 | 0.377 | $30,496 | Continued bull |
| Jun-Jul 2023 | 0.318–0.350 | 0.067–0.112 | 0.380–0.411 | $29,930–$31,481 | Extended sideways, lanjut naik |

**Upper Range 2019 yang FAILED:**
- NUPL 0.608 dan STH 0.425 terlalu tinggi untuk fase recovery. Ini sebenarnya mini-euphoria bukan recovery. STH 0.425 artinya recent buyers sangat profitable — overheated.
- 30 hari kemudian harga turun dari $12,830 ke ~$9,935 (-23%). Upper Range 2019 seharusnya dikategorikan sebagai local top yang gagal, bukan upper range recovery.
- Lesson: Upper range recovery yang genuine punya NUPL di range 0.30–0.40, bukan 0.60. Kalau NUPL sudah di 0.55–0.65 dan harga belum ATH, kemungkinan ini bukan upper range recovery — ini local top yang akan koreksi.

**2023 upper ranges:**
- NUPL 0.32–0.35, STH 0.07–0.24, LTH 0.38–0.41. Ini adalah genuine upper range recovery: NUPL moderate, STH modest profit, LTH modest profit. Market belum overheated. Di fase ini, STH masih jauh lebih rendah dari LTH, mencerminkan bahwa cost basis baru (post-bear) belum menjadi dominant.

---

## 3. RULE RANGES — SIGNAL THRESHOLDS

### 3.1 SELL SIGNALS — Detect Early Exit Opportunities

#### Rule S1: NUPL > 0.55 — Caution Zone Entry

**Logic:** Ketika NUPL di atas 0.55, market sudah di territory overheated secara historis. Ini bukan sell signal langsung, tapi zona dimana setiap kenaikan berikutnya harus dipertanyakan.

**Test results dari data:**
- Triggered di 10 dari 11 top-like events (cycle peaks + local tops + lower highs) yang relevan: hit rate tinggi tapi tidak sempurna.
- Missed: Lower High 2025 (NUPL 0.515) — di bawah threshold meski sudah jadi konfirmasi lower high.
- False positives: NUPL > 0.55 juga terjadi selama bull dips di awal 2021 cycle (Bull Dip Jan 2021 NUPL 0.687, Sep 2017 NUPL 0.638) — ini bukan sell signal, ini buy the dip territory.
- Cost of being wrong (false sell): kalau sell di NUPL 0.55 dan ini bull dip, kamu miss remaining upside. Dari Bull Dip Jan 2021 ke Cycle Peak Apr 2021: harga naik dari $35,551 ke $63,551 (+79%).

**Reliability per cycle — breakdown threshold per tier:**

| Threshold | Cycle 2017 | Cycle 2021 | Cycle 2025 | Hit rate | Assessment |
|-----------|-----------|-----------|-----------|---------|-----------|
| NUPL > 0.75 + STH > 0.40 | ✓ Triggered | ✗ Not triggered | ✗ Not triggered | 1/3 | OBSOLETE |
| NUPL > 0.65 + STH > 0.20 | ✓ | ✓ (Local tops) | ✗ | 2/3 cycle peaks | Partially valid |

Threshold tunggal "NUPL > 0.55" terlalu tinggi untuk 2025 cycle (peak hanya 0.562) tapi terlalu rendah untuk 2017 cycle (triggered jauh sebelum peak). Fixed threshold sell tidak reliable lintas cycle — butuh pendekatan adaptive (relative ke cycle-nya sendiri, bukan absolute level).

**Recommendation:** Gunakan sebagai warning zone, bukan trigger. NUPL > 0.55 → mulai monitor STH-NUPL dan LTH-STH gap lebih ketat. Jangan jual berdasarkan NUPL saja.

#### Rule S2: STH-NUPL < 0.10 di Konteks Market yang Sudah Naik (NUPL > 0.50)

**Logic:** Kalau market overall sudah naik (NUPL > 0.50) tapi STH-NUPL di bawah 0.10, ini berarti recent buyers hampir breakeven meskipun harga secara historis tinggi. Ini menandakan exhaustion: buying power baru masuk di harga tinggi dan tidak punya buffer.

**Test results:**
- Hit di Cycle Peak 2025 (STH 0.082), Lower High 2021 (STH 0.062), Lower High 2025 (STH 0.013), Lower High 2025 Confirmation (STH -0.001)
- Hit rate: 4 dari 4 events di 2021-2025 cycle dimana ini triggered → semuanya diikuti decline signifikan
- NOT triggered di 2017 events (STH masih di 0.27–0.53 di semua tops) — ini signal yang muncul hanya di later cycles karena diminishing returns
- False positive potential: STH < 0.10 juga terjadi di bull dips (misal Bull Dip Sep 2020 STH -0.013 dengan NUPL 0.386). Tapi di situ NUPL < 0.50, jadi filter NUPL > 0.50 mencegah false signal.

**Cost of being wrong:** Kalau ini false signal dan market masih naik, kamu sell terlalu early. Tapi dari data, setiap kali combo NUPL > 0.50 + STH < 0.10 terjadi, decline followed dalam 30 hari. Worst case dalam data: sell di Lower High 2025 (harga $114,584) → 30 hari kemudian harga $88,655. Being right saved -23%.

**Reliability:** Hanya applicable di 2021+ cycles. Di cycle sebelumnya, STH jauh lebih tinggi di peaks. Untuk next cycle, threshold mungkin perlu diturunkan lebih lanjut kalau diminishing returns berlanjut.

**Konfirmasi tambahan — STH drop magnitude (bukan cuma level absolut):** Selain level absolut STH < 0.10, drop STH > 0.15 dari recent high dalam 30 hari (dengan NUPL masih > 0.50) juga konsisten menandakan lower high setup:

| Instance | STH drop | Hasil |
|----------|---------|-------|
| Jan 2018 | 0.54 → 0.27, drop 0.27 | ✓ Lower high confirmed |
| Nov 2021 | 0.25 → 0.06, drop 0.19 | ✓ Lower high confirmed |
| Okt 2025 | 0.08 → 0.01, drop 0.07 | ✓ Lower high confirmed |

Hit rate: 3/3. Catatan: di 2025, drop absolutnya kecil (0.07) karena STH sudah sangat rendah — sebaiknya dievaluasi sebagai persentase dari peak, bukan nilai absolut, supaya tetap applicable saat STH makin compressed tiap cycle.

#### Rule S3: LTH-STH Gap > 0.60 di NUPL > 0.50

**Logic:** Gap besar antara LTH dan STH profit menandakan disconnect: long-term holders masih sangat nyaman tapi short-term holders borderline. Ini secara historis precedes distribution phase.

**Test results:**
- Triggered di: Cycle Peak 2025 (gap 0.620), Lower High 2018 (0.686), Lower High 2021 (0.657), Lower High 2025 (0.661), Mid-Cycle Correction Start (0.706), Local Top Apr 2021 ATH (0.608)
- Di semua 6 cases, decline followed dalam 30 hari
- NOT triggered di genuine bull dips atau bear bottoms (gap biasanya <0.55 di bull dips, dan negatif di bottoms)
- Hit rate: 6/6 = 100% tapi sample sangat kecil

**Caveat:** Di 2017 cycle, gap di Cycle Peak (0.433) dan Lower High (0.686) sangat berbeda. Gap di cycle peak 2017 lebih rendah karena STH juga sangat profitable. Rule ini lebih applicable di later cycles.

### 3.2 BUY SIGNALS — Detect Early Entry Opportunities

#### Rule B1: NUPL < 0 — Deep Accumulation Zone

**Logic:** NUPL negatif berarti market secara aggregate underwater. Historically, ini hanya terjadi di bear market lows dan selalu diikuti oleh recovery.

**Test results:**
- Triggered di 8 dari 8 bear bottom dan pre-detection events: hit rate 100%
- FALSE SIGNAL WARNING: NUPL < 0 bisa bertahan lama (bulan) sebelum bottom benar-benar tercapai. Di 2018: NUPL pertama negatif sekitar Nov 2018 tapi bottom baru Des 2018. Di 2022: NUPL negatif di Jun 2022 (Luna crash) tapi final bottom baru Des 2022 — 6 bulan kemudian.
- Cost of being early: kalau buy saat NUPL pertama kali < 0 di Jun 2022 (NUPL -0.084), harga masih turun dari ~$19,627 ke $15,774 (-20% additional drawdown). Tapi kalau hold, 1 tahun kemudian harga lebih dari 2x.
- NUPL < -0.20 lebih precise untuk "near bottom" — triggered di semua 4 deepest lows (2018 Tier 1: -0.364, Window End: -0.274, Actual Price Low: -0.288, Final Low: -0.214).
- **Diminishing depth risk:** Kalau threshold-nya NUPL < -0.30, ini hanya menangkap 2018 (-0.42) tapi MISS 2022 (terdalam cuma -0.29). Bear bottom depth mengecil tiap cycle — threshold fixed "< -0.30" berisiko miss bottom di cycle berikutnya.

#### Rule B2: STH-NUPL Crosses Zero from Below (di konteks NUPL < 0.20)

**Logic:** Saat STH-NUPL berbalik dari negatif ke positif sementara NUPL masih rendah, ini menandakan akumulator baru mulai profit — new money entering and working.

**Test results:**
- Pre Detection 2019: STH dari -0.012 ke positive territory → harga naik 33% dalam 30 hari
- Pre Detection 2023: STH dari -0.022 ke 0.052 dalam 2 hari → harga naik 21% dalam 14 hari
- Start of Bull 2019: STH 0.185 (sudah positif, confirmed) → 30 hari: +120%
- Start of Bull 2023: STH 0.106 (positif, confirmed) → 30 hari: +14%
- Hit rate: 4/4 pre-detection dan start-of-bull events
- False signal: Tidak terdeteksi di data, tapi sample sangat kecil (n=4)

#### Rule B3: STH-NUPL < -0.10 di Konteks NUPL > 0.30 — Bull Dip Buy

**Logic:** STH sudah loss >10% sementara market overall masih healthy (NUPL > 0.30). Short-term pain in long-term bull = buying opportunity.

**Test results dari bull dips:**
- Triggered di 8 dari 15 bull dips (53%)
- Performance 30 hari setelah signal:
  - Bull Dip Jul 2024: +0.3% (weak)
  - Bull Dip Yen Carry Trade: -2.1% (slightly negative!)
  - Bull Dip Sep 2024: +27.3%
  - Bull Dip Mar-Apr 2025: +26.8%
  - Bull Dip Aug-Sep 2023: +3.6% (weak)
- Average 30-day return: +11.2% (excluding outlier 2017)
- **Key warning:** 2 dari 8 signals menghasilkan near-flat return (Jul 2024 dan Yen Carry Trade). Ini bukan guaranteed profit.

**Filter tambahan yang meningkatkan accuracy:** LTH-NUPL > 0.50. Kalau LTH masih strongly positive, bull structure intact. Di 8 triggered bull dips, 6 punya LTH > 0.50 dan rata-rata returnnya lebih tinggi.

**Versi dengan filter NUPL > 0.35 dan LTH > 0.55 (lebih ketat):**

| Instance | STH | LTH | Result |
|----------|-----|-----|--------|
| Sep 2020 | -0.015 | 0.510 | ✓ Bull lanjut |
| Jun 2023 | -0.051 | 0.273 | ✓ Bull lanjut |
| Agt 2023 | -0.113 | 0.298 | ✓ Bull lanjut |
| Jul 2024 | -0.147 | 0.654 | ✓ (sideways 30d, lanjut) |
| Agt 2024 | -0.203 | 0.640 | ✓ (sideways 30d, lanjut) |
| Mar-Apr 2025 | -0.215 | 0.691 | ✓ Rally ke local top |

Hit rate untuk "bull lanjut" (toleransi sideways dulu sebelum rally): 6/6. Tapi 2 dari 6 (Jul-Agt 2024) sideways 30 hari dulu baru rally — kalau pakai leverage, periode sideways ini tetap bisa makan biaya/margin meski thesis akhirnya benar.

#### Rule B4: Semua Tiga Metrik Negatif Bersamaan

**Logic:** NUPL < 0, STH-NUPL < 0, dan LTH-NUPL < 0. Ini adalah maximum capitulation — bahkan veteran holders underwater.

**Test results:**
- Triggered di: Bear Bottom 2018 Tier 1, Window End, Bear Bottom Actual Price Low 2022, FTX Collapse, Final Low 2022
- Hit rate: 5/5 — semuanya terjadi di bear bottom zone
- 12-month forward return dari semua instances: strongly positive (>100%)
- Caveat: signal bisa muncul bulan-bulan sebelum actual bottom (Jun 2022 vs Des 2022). Timing entry masih challenging. Sama seperti Rule B1, threshold yang terlalu ketat (mis. NUPL < -0.30 DAN LTH < -0.25) berisiko miss bottom yang lebih shallow di cycle berikutnya — diminishing depth berlaku di sini juga.

---

### 3.3 DIVERGENCE HARGA vs INDIKATOR

Divergence di sini berbeda dari interaksi antar metrik di Section 4. Di sini yang dianalisis adalah ketika **harga bergerak satu arah, tapi indikator bergerak arah berlawanan** — classic divergence dalam analisis teknikal, diterapkan pada NUPL family.

Analisis menggunakan pivot lows pada harga, window ±14 hari, filter >10% price move dan >0.03 indikator diff. Data mencakup 2017–2026.

---

#### 3.3.1 Regular Bullish Divergence (Harga: Lower Low | Indikator: Higher Low)

Sinyal bahwa selling pressure melemah meskipun harga masih turun. Potential reversal incoming.

**Temuan kritis: Hanya STH-NUPL yang secara konsisten membentuk regular bull divergence.** NUPL dan LTH-NUPL hampir tidak pernah. Ini logis secara struktural — STH cost basis paling sensitif terhadap price action, sehingga bahkan saat harga masih lower low, STH bisa higher low kalau ada akumulasi baru di level harga lebih tinggi dari trough sebelumnya.

**Episode 1 — Bear 2018 (Serangkaian pivot lows)**

STH-NUPL Raw dan SMA15 membentuk regular bull div dari beberapa pasang pivot lows menuju Jan–Feb 2019:
- Feb 5, 2018 ($6,913) → Jan 13, 2019 ($3,588): Price −48%, STH Raw +0.261 (−0.575 → −0.314)
- Mar 30, 2018 ($6,964) → Jan 13, 2019 ($3,588): Price −48.5%, STH Raw +0.261 | STH SMA15 +0.092
- Jun 28, 2018 ($5,914) → Jan 13, 2019 ($3,588): Price −39%, STH Raw +0.090

Forward return dari Jan 13, 2019: **+1.7% (30d), +9.7% (60d), +42.7% (90d)**
Forward return dari Feb 7, 2019 (Window End): **+16.2% (30d), +54.4% (60d), +132% (90d)**

Catatan: Divergence muncul berulang kali selama bear berlangsung, bukan sekali lalu confirmed. Yang reliable adalah *cluster* — ketika STH membentuk higher lows berulang sementara harga masih turun, itu adalah evidence akumulasi yang mengering.

**Episode 2 — COVID Flash Crash Mar 2020**

NUPL SMA15 dan STH-NUPL SMA15: Dec 17, 2019 ($6,854) → Mar 12, 2020 ($4,837)
Price: −29%, NUPL SMA15: +0.056 (0.233 → 0.289), STH SMA15: +0.152 (−0.215 → −0.064)

Forward return dari Mar 12, 2020: **+59% (30d), +91% (60d), +89% (90d)**

Catatan: Ini adalah satu-satunya episode di mana NUPL (bukan hanya STH) membentuk regular bull div yang kuat. Terjadi karena COVID crash adalah flash crash — sangat dalam tapi cepat, sehingga NUPL tidak sempat turun se-ekstrem harga.

**Episode 3 — Bear 2022 (Multi-pivot, paling banyak konfirmasi)**

STH-NUPL Raw+SMA15 membentuk serangkaian regular bull div sepanjang bear 2022:
- Mar 13, 2022 ($37,830) → Oct 2, 2022 ($19,055): Price −50%, STH +0.065 (Raw), +0.081 (SMA15)
  Forward dari Oct 2: **+7.5% (30d), −10.9% (60d), −13.2% (90d)** ← FALSE, FTX belum terjadi
- Mar 13, 2022 → Nov 21, 2022 ($15,774): Price −58%, STH Raw +0.032 (sangat tipis)
  Forward dari Nov 21: **+6.7% (30d), +43.8% (60d), +53.9% (90d)** ← TRUE
- Mar 13, 2022 → Des 19, 2022 ($16,442): Price −56.5%, STH Raw +0.122, SMA15 +0.091
  Forward dari Des 19: **+25.8% (30d), +49.4% (60d), +70.6% (90d)** ← Paling kuat
- Oct 2 → Des 19 ($16,442): Price −13.7%, STH +0.057 Raw, +0.040 SMA15
  Forward dari Des 19: sama seperti di atas

Lesson dari 2022: Signal terbaik bukan yang paling awal muncul, tapi yang paling dekat dengan actual bottom. Oct 2 trigger gagal karena FTX collapse belum terjadi. Entry berbasis divergence perlu dikombinasikan dengan konfirmasi lain (Rule B4 / all-three-negative).

**Kemudian, sebagai finalisasi episode ini:**
Mar 2022 → Feb 10, 2023 (Start of Bull): Price −43%, STH Raw dari −0.238 ke +0.106 (+0.344) — crossover ke positif
Forward: **+2.4% (30d), +39.7% (60d), +24.8% (90d)**

**Kesimpulan regular bull div:**

| Kondisi | Reliability | Forward Return 90d |
|---------|------------|-------------------|
| STH div di actual bottom (Des 2018, Des 2022) | Tinggi | +42–132% |
| STH div di early bear (pre-bottom) | Rendah | Masih turun −10 to −13% dalam 60d |
| NUPL div di flash crash | Medium-Tinggi | +89% (n=1, COVID anomaly) |
| LTH div | Tidak ada pattern | N/A |

---

#### 3.3.2 Hidden Bullish Divergence (Harga: Higher Low | Indikator: Lower Low)

Sinyal bahwa uptrend masih berlanjut meski indikator melemah. Bullish continuation dalam konteks bull market.

**FALSE signal yang paling berbahaya:** Hidden bull div di area peak atau awal bear.

**False Episode — Mid-Cycle Bottom 2021 → Des 2021:**
LTH-NUPL, NUPL, dan STH-NUPL semuanya membentuk hidden bull div: harga naik dari $29,837 ke $46,192 (+55%), tapi semua metrik lebih rendah di Des 2021 dibanding Jul 2021.
Forward dari Des 17, 2021: **−11% (30d), −12% (60d), −59% (90d)** ← MAJOR FALSE SIGNAL

Kenapa false: ini bukan bull dip biasa. LTH declining dari 0.75 ke 0.65 dalam 3 bulan adalah distribusi yang menyamar. Hidden bull div di territory NUPL >0.45 yang diikuti LTH declining steeply = trap.

**False Episode — Mar 2025 → Des 2025:**
NUPL + LTH hidden div: harga naik dari $76,270 ke $85,516 (+12%), tapi NUPL turun 0.426 → 0.342, LTH turun 0.657 → 0.563.
Forward dari Des 18, 2025: **+11.2% (30d), −19.4% (60d), −16.7% (90d)** ← FALSE

Konteks: Bear market sudah dimulai (Cycle Peak Okt 2025, Lower High sudah konfirmasi). Hidden bull div dalam confirmed bear = trap.

---

**TRUE signals — Bear-to-Bull transition:**

**Oct 2022 → Start of Bull 2023:**
NUPL SMA15 dan LTH SMA15: harga naik dari $19,055 ke $21,632 (+13.5%), NUPL SMA15 turun 0.315 → 0.137, LTH SMA15 turun 0.430 → 0.129.
Forward dari Feb 10, 2023: **+2.4% (30d), +39.7% (60d), +24.8% (90d)** ← TRUE

Konteks: Ini terjadi di zona transisi bear ke bull (NUPL masih <0.10, keduanya baru keluar dari negatif). LTH dan NUPL lower low di harga higher low karena SMA masih membawa weight dari FTX bottom sebelumnya.

**Yen Carry Trade (Aug 2024) → Oct 2024:**
LTH-NUPL SMA15 hidden div: harga naik dari $54,026 ke $60,662 (+12%), LTH SMA15 turun 0.682 → 0.608.
Forward dari Oct 2, 2024: **+62% (30d), +60% (60d), +68.5% (90d)** ← Sangat kuat

**Sep 2024 → Mar-Apr 2025:**
STH-NUPL hidden div: harga naik dari $53,998 ke $76,270 (+41%), STH makin negatif di harga lebih tinggi.
Forward dari Apr 8, 2025: **+44.6% (30d), +45.9% (60d), +53% (90d)** ← TRUE

---

**TRUE signals — Mid-bull dip series (moderate):**

| Episode | Price Change | 30d Return | 90d Return |
|---------|------------|------------|------------|
| Start Bull 2023 → Jun 2023 dip (STH) | +16% | +20.6% | +2.7% |
| Jan 2024 → Mei 2024 (STH) | +48% | +15.7% | +13.5% |
| Jan 2024 → Jul 2024 (STH) | +41% | +0.3% | +11% (weak) |
| Jan 2024 → Aug 2024 Yen (STH) | +37% | +7.4% | +80.9% |

---

**Filter kritis untuk hidden bull div:**

Hidden bull div tidak reliable berdiri sendiri. Dua filter yang membedakan true vs false:

1. **NUPL level saat signal muncul:** Kalau NUPL >0.45 dan hidden bull div terbentuk, suspect false — kemungkinan ini distribusi yang menyamar. Kalau NUPL <0.20, jauh lebih reliable.

2. **Arah LTH:** Kalau LTH declining lebih dari 0.05 per bulan selama periode hidden div, ini bukan "indicator softening naturally" — ini distribusi aktif. Hidden div dengan LTH declining steep = trap (Dec 2021 case).

---

#### 3.3.3 Rangkuman Divergence Rules

| Signal | Metrik | Kondisi Trigger | Reliability | Tindakan |
|--------|--------|----------------|-------------|---------|
| Regular Bull Div | STH-NUPL | Price LL, STH HL, dalam bear zone | Medium-High kalau dekat actual bottom | Akumulasi bertahap, bukan all-in |
| Regular Bull Div | STH-NUPL | Price LL, STH HL, di awal bear | Low — bisa terus turun | Hanya sebagai radar, tunggu konfirmasi B4 |
| Regular Bull Div | NUPL | Price LL, NUPL HL | Medium (hanya terbukti di flash crash) | Perlu cross-check kondisi flash vs sustained |
| Hidden Bull Div | STH/LTH | Price HL, indikator LL, NUPL <0.20 | Medium-High | Entry atau tambah posisi |
| Hidden Bull Div | STH/LTH | Price HL, indikator LL, NUPL >0.45 | Low — likely trap | Jangan diikuti, cek LTH trend |
| Hidden Bull Div | LTH declining steep | Price HL, LTH LL dan terus turun | False signal | Ini distribusi, bukan dip |

**Yang tidak pernah terjadi di data:** LTH-NUPL membentuk regular bull divergence yang meaningful. LTH terlalu smooth dan lagging untuk membentuk pivot patterns yang tajam. LTH berguna sebagai filter konteks, bukan sebagai divergence generator.

---

## 4. INTERAKSI ANTAR KETIGA METRIK

### 4.1 Kapan Ketiganya Sejalan

**Semua naik bersama (bullish alignment):** Terjadi di early-to-mid bull market. Contoh: Start of Bull 2023, semua di range 0.075–0.106 dan naik bersamaan. Ini adalah fase paling "clean" untuk entry — semua cohort mulai profit, tidak ada internal stress.

**Semua turun bersama (bearish alignment):** Terjadi di bear market decline. Contoh: Bear Decline Mid 2018 ke Low 2018, semua turun bersamaan. Di fase ini tidak ada tempat bersembunyi — exit strategy harus sudah selesai sebelum phase ini.

### 4.2 Kapan Diverge dan Apa Artinya

**Divergence Paling Berbahaya — STH negatif + LTH masih tinggi positif:**
Ini terjadi di Lower High 2021 (STH 0.062, LTH 0.719, gap 0.657) dan Lower High 2025 (STH 0.013, LTH 0.674, gap 0.661). Recent buyers sudah stres tapi veteran masih complacent.

Kenapa berbahaya: LTH yang masih profitable bisa membuat market terlihat "healthy" pada aggregate NUPL (masih 0.51–0.57). Tapi foundation sudah rapuh karena marginal buyer — yang menentukan price direction di margin — sudah loss. Ketika LTH akhirnya mulai distribute (karena harga terus turun), cascade effect terjadi.

**Divergence Bullish — STH positif + LTH masih negatif:**
Terjadi di Pre Detection dan Start of Bull. STH mulai profit (akumulator baru berhasil) sementara LTH masih loss (holder lama belum recover). Ini structural shift positif karena menunjukkan new demand di level harga saat ini.

Di Start of Bull 2019: STH 0.185 > LTH 0.145. Di Start of Bull 2023: STH 0.106 > LTH 0.075. Dalam kedua kasus, STH sedikit di atas LTH — artinya buyer baru lebih profitable dari veteran. Ini hanya terjadi saat market sudah bottomed dan mulai trending up dari basis yang solid.

**Mid-Cycle Correction divergence — STH extreme negative + LTH still solid:**
Mid-Cycle Correction Bottom 2021: STH -0.437, LTH 0.759. Gap 1.196. Ini menandakan crash yang severe bagi recent buyers tapi LTH conviction tetap intact. Karena LTH masih kuat, market recover setelah STH capitulation selesai.

Ini penting untuk membedakan mid-cycle correction dari start of bear: kalau LTH mulai declining steeply juga (menuju 0.60 atau lower), ini bukan correction lagi — ini distribusi.

### 4.3 Kombinasi Signal Paling Reliable Per Regime

| Regime | Primary Signal | Confirming Signal | Confidence |
|--------|---------------|-------------------|------------|
| Cycle Peak | NUPL > 0.55 + STH declining | LTH-STH gap expanding | Medium (diminishing returns make absolute levels unreliable) |
| Lower High | STH < 0.05 + NUPL > 0.50 | LTH-STH gap > 0.60 | High (4/4 in 2021-2025) |
| Bull Dip | STH < -0.05 + LTH > 0.50 | NUPL masih > 0.30 | Medium (not all recover quickly) |
| Bear Bottom | NUPL < -0.20 + semua negatif | STH mulai recover menuju 0 | High (5/5 historically) |
| Start of Bull | STH > 0 + LTH ≈ 0 atau sedikit positif | STH > LTH (crossover) | High (but n=2) |
| Mid-Cycle Corr. | STH < -0.30 + LTH > 0.70 | Gap > 1.0 | Medium-High (but n=1) |

---

## 5. FAILURE MODES — BAGIAN TERPENTING

### 5.1 NUPL Failure Modes

**F1: Diminishing Peak Values**
NUPL peak di 2017: 0.80, di 2021: 0.66, di 2025: 0.56. Setiap fixed threshold menjadi invalid di cycle berikutnya. Kalau kamu set "sell when NUPL > 0.75" berdasarkan 2017, kamu tidak akan pernah sell di 2021 atau 2025 karena threshold itu tidak pernah tercapai lagi.

**Mitigation:** Jangan pakai fixed threshold. Gunakan relative position — seberapa tinggi NUPL relatif terhadap cycle-nya sendiri, bukan relatif terhadap cycle sebelumnya. Atau gunakan rate of change (seberapa cepat NUPL naik) bukan absolute level.

**F2: NUPL Ambiguity di Mid-Range (0.40–0.55)**
NUPL 0.45 bisa berarti: bull dip (buy opportunity), bear decline (jangan beli), atau upper range recovery (hold). Tanpa STH dan LTH decomposition, NUPL di range ini nearly useless untuk regime identification.

**Dari data:** Bear Decline Start 2018 NUPL 0.492, Bull Dip Jan 2024 NUPL 0.453, Bear Market Decline Mid 2022 NUPL 0.477, Bull Dip Mei 2024 NUPL 0.505. Semua di range 0.45–0.51 tapi outcomes sangat berbeda. NUPL saja tidak bisa membedakan ini.

**F3: NUPL Lagging di Fast Crashes**
Karena Realized Cap bergerak lambat, NUPL tidak capture flash crash severity secara real-time. FTX Collapse (Nov 8, 2022): NUPL "hanya" -0.135 padahal market dalam kepanikan total. Actual Price Low (Nov 21) NUPL -0.288 tapi market sentiment jauh lebih buruk dari yang angka tunjukkan.

**F4: NUPL Negatif ≠ Sudah di Bottom**
Nov 2022, NUPL sudah -0.13 saat FTX. Harga masih turun 15% lebih ke $15.7K. "Beli saat NUPL negatif" tanpa konfirmasi lain bisa entry terlalu early dan kena drawdown tambahan.

**F5: NUPL Positif Tinggi Bisa Terjadi di Failed Rally**
Jun 2019, NUPL 0.61 di $12,830 (Upper Range 2019 yang gagal). Harga kemudian turun -23% dalam 30 hari. NUPL tinggi bukan jaminan bull lanjut.

### 5.2 STH-NUPL Failure Modes

**F1: Terlalu Noisy untuk Medium-Term Signals**
STH-NUPL bisa swing drastis dalam hari. Dari data: Cycle Peak 2017 STH 0.534, lalu 30 hari kemudian 0.006 — drop 0.528 dalam sebulan. Tapi juga: Bull Dip Sep 2017 STH dari 0.246 ke 0.072 dalam 7 hari, lalu recover. Noise ini membuat sulit membedakan "dip yang akan recover" vs "start of sustained decline" dalam real-time.

**F2: False Buy Signals di Late Bull**
STH-NUPL < -0.10 triggered di Bull Dip Jul 2024 (STH -0.147) tapi 30-day return hanya +0.3%. Dan di Yen Carry Trade (STH -0.203) return -2.1%. Ini bukan catastrophic losses, tapi juga bukan the confident buy signal yang diharapkan.

Penyebab: di late cycle, bull dip bisa transition menjadi extended sideways atau bahkan start of decline. STH-NUPL sendiri tidak bisa membedakan "dip in strong bull" vs "dip in exhausted bull."

**F3: Diminishing Returns Bahkan Lebih Parah dari NUPL**
STH peak drop: 0.597 → 0.301 → 0.089. Di cycle berikutnya, STH mungkin peak di <0.05. Ini berarti semua STH-based thresholds perlu di-recalibrate setiap cycle. Rule yang bekerja di 2021 (STH > 0.20 = overheated) mungkin tidak applicable di next cycle.

**F4: STH Positif ≠ Bull Market**
Nov 4, 2022, STH dan NUPL keduanya sempat positif. FTX collapse terjadi 4 hari kemudian. Fundamental event (black swan) bisa mengalahkan on-chain signal — jangan act pada single crossover tanpa konfirmasi multi-hari.

**F5: Dip Depth Tidak Proporsional dengan Severity Fundamental**
COVID (price -50% dalam 1 hari): STH -0.69. Yen carry trade (price -20% dalam beberapa hari): STH -0.20. STH depth tidak reliable sebagai proxy untuk severity fundamental risk yang sedang terjadi.

### 5.3 LTH-NUPL Failure Modes

**F1: Terlalu Lambat sebagai Signal**
LTH-NUPL hampir selalu lagging. Di Cycle Peak 2017, LTH peak 8 hari setelah price peak. Di Cycle Peak 2021, 19 hari setelah. Sebagai sell signal, LTH terlambat.

**F1B: LTH Positif ≠ Harga Tidak Bisa Drop Lebih Jauh**
LTH 0.70–0.75 saat mid-cycle correction 2021, padahal harga turun -50% dari local top. LTH positif hanya bilang LTH holder tidak menderita — tidak ada klaim tentang price trajectory ke depan.

**F2: Dapat Memberikan False Sense of Security**
Di Lower High 2025 dan Lower High 2021, LTH masih di 0.67–0.72 — yang terlihat "healthy." Tapi 30 hari kemudian, harga crash 20%+. LTH yang masih tinggi bisa membuat kamu berpikir "bull masih oke" padahal distribution sudah dimulai.

**F3: Anomali 2022 — LTH Lebih Loss dari STH**
Di Bear Bottom Actual Price Low 2022: LTH -0.309, STH -0.206. Biasanya LTH > STH, tapi di 2022 terbalik karena banyak pembelian 2021 (di harga tinggi) sudah masuk kategori LTH. Ini menunjukkan bahwa LTH != smart money. LTH hanyalah "belum jual selama 155 hari" — bisa jadi hodler yakin, bisa jadi hodler yang stuck.

### 5.4 Yang Paling Sering Gagal

**Ranking berdasarkan data:**
1. **STH-NUPL** paling sering gagal sebagai standalone signal. Noise tinggi, false buy signals di late bull (Jul 2024, Aug 2024), dan diminishing returns paling parah.
2. **NUPL** mid-range ambiguity adalah kelemahan terbesar. Di range 0.40–0.55, NUPL basically uninformative tanpa decomposition.
3. **LTH-NUPL** paling reliable tapi paling lambat. Jarang memberikan false signal, tapi sering terlambat untuk actionable timing.

### 5.5 Apa yang Bisa Membuat Threshold Historis Invalid di Cycle Berikutnya

1. **Institutional adoption continuing:** Lebih banyak coins held oleh institusi yang punya holding period > 155 hari by default → LTH proportion meningkat, LTH-NUPL structurally lebih tinggi.
2. **ETF dynamics:** ETF inflows/outflows bisa menggeser STH-NUPL secara unpredictable karena wrapping/unwrapping behavior berbeda dari on-chain native.
3. **Longer cycles:** Kalau cycle semakin panjang, threshold temporal (155 hari untuk LTH/STH split) mungkin perlu adjustment.
4. **Structural deleveraging:** Kalau market secara structural lebih deleveraged di next cycle (less leverage, more spot), NUPL extremes mungkin lebih moderat bahkan dari 2025.
5. **Wrapped BTC dan L2:** Coins on Lightning, wrapped pada Ethereum, dll mungkin tidak ter-track sebagai moved, biasing LTH-NUPL upward.

---

## 6. MAPPING KE REGIME CATEGORIES

### Regime Decision Framework

| Regime | NUPL Range | STH-NUPL | LTH-NUPL | Gap (LTH−STH) | Ratio (LTH/STH) | Weight |
|--------|-----------|----------|----------|----------------|-----------------|--------|
| **Cycle Peak** | >0.55 (diminishing) | Declining dari peak | Plateauing/lagging | 0.43–0.62, expanding | 1.8–8.6 (rising) | HIGH (tapi perlu cross-check MVRV, SOPR) |
| **Local Top** | 0.58–0.74 | 0.11–0.39 | Stable high 0.69–0.92 | 0.47–0.64 | 2.4–6.8 | MEDIUM (NUPL alone insufficient) |
| **Lower High** | 0.51–0.70 | <0.07 (2021+) | Still high 0.65–0.96 | >0.60, lebar | >11 sampai 73+ | HIGH (STH near zero kuat; ratio extreme confirm) |
| **Bull Dip** | 0.02–0.69 | Often < 0 | Still positive >0.11 | 0.40–0.88 (lebar) | Mixed sign (LTH+, STH−) | MEDIUM (use with SOPR confirmation) |
| **Mid-Cycle Corr.** | 0.35–0.66 | <−0.30 | Still >0.70 | **>1.0 (unik)** | Mixed sign ~−1.4 to −2.6 | HIGH (gap >1.0 adalah signature eksklusif) |
| **Bear Decline** | 0.21–0.49 declining | <0 | 0.41–0.90 declining | 0.38–0.94 narrowing | Mixed sign, besar negatif | MEDIUM (trend matters more than level) |
| **Bear Bottom** | <0 (deepest <−0.20) | <−0.12 | Often <0 | Near zero atau negatif | 0.57–2.06 (both negative) | HIGH (all-negative + gap near zero definitif) |
| **Pre Detection** | −0.13 to −0.05 | Near 0, recovering | Still negative | −0.07 to −0.14 (negatif!) | Both negative, 2–10 | MEDIUM-HIGH (gap negatif = structural recovery) |
| **Start of Bull** | 0.08–0.16 | >0, STH > LTH | ~0 to slightly positive | **−0.03 to −0.04 (negatif)** | **0.71–0.79 (both pos, <1)** | HIGH (ratio <1 adalah fingerprint eksklusif) |
| **Upper Range** | 0.33–0.35 (excl. 2019 failure) | 0.11–0.24 | 0.38–0.39 | 0.13–0.28 | 1.6–3.5 | MEDIUM (Upper Range 2019 ratio 1.59 masih cukup sehat) |

### Kapan Beri Weight Tinggi vs Rendah

**Weight tinggi pada NUPL family:**
- Bear bottom identification: semua negatif + gap near zero adalah nearly definitive signal
- Start of bull confirmation: ratio <1 (both positive) + gap negatif = fingerprint eksklusif (n=2, tapi sangat clean)
- Lower high detection: STH near zero + gap >0.60 + ratio >11 kuat
- Mid-cycle correction: gap >1.0 belum pernah terjadi di fase lain

**Weight rendah pada NUPL family:**
- Distinguishing local top vs cycle peak: NUPL dan gap overlap terlalu besar, perlu MVRV atau SOPR
- Timing precision: NUPL tidak pernah tepat untuk pinpoint entry/exit timing
- Mid-range ambiguity (NUPL 0.40–0.55): bisa apa saja, perlu indikator lain
- Ratio saat STH dekat nol: ratio explodes ke angka besar (50, 100, 500) karena denominator tiny — perhatikan arah perubahan sign, bukan magnitude

### Red Flags Spesifik yang Trigger Immediate Attention

1. **STH-NUPL drops below 0 saat NUPL > 0.50:** Recent buyers underwater tapi market looks "fine." Jika LTH-STH gap > 0.60 dan ratio mulai berubah sign → very suspicious, likely lower high territory.

2. **Ratio melompat ke >15 atau berubah sign berulang kali dalam seminggu:** STH berada di zero-crossing zone yang unstable. Setiap kali ini terjadi di konteks NUPL > 0.50, ini adalah early warning bear territory. Bandingkan: Bear Market Decline Mid 2022 ratio bergerak 57 → −257 → 325 dalam 8 hari sebelum Luna crash.

3. **LTH-NUPL mulai declining steeply (>0.05/minggu) dari territory >0.65:** LTH mulai distribute. Kalau ini terjadi saat gap masih lebar dan ratio masih tinggi, bears sudah dimulai meskipun aggregate NUPL terlihat sehat.

4. **Semua tiga metrik negatif setelah sebelumnya positif:** Capitulation phase. Gap akan mendekati nol dari atas — monitor ratio toward 1.0 (both negative). Saat ratio ~1.0 both negative, itu zona Window End type — bottom dekat.

5. **STH-NUPL > LTH-NUPL (gap negatif) saat keduanya positif dan rendah (<0.20):** Structural shift dari bear ke bull. Ratio turun di bawah 1.0. Ini early bull signal — sangat reliable tapi jangan deploy leverage di sini, masih terlalu early.

6. **LTH-NUPL crossing ke negatif:** Bear market sesungguhnya dikonfirmasi. Review semua posisi, terutama leverage — LTV buffer harus diperiksa segera kalau ada posisi loan aktif.

**Quick reference (untuk scan cepat tiap minggu):**

🔴 LTH-NUPL crossing ke negatif → bear market dikonfirmasi, cek LTV buffer.
🔴 STH-NUPL drop >0.15 dari recent high dalam <30 hari + harga masih >85% ATH → potensi lower high, early warning ketat.
🔴 STH dan NUPL brief positif dalam konteks bear → potensi false signal, tunggu konfirmasi multi-minggu.
🟡 LTH-NUPL menurun progresif 3+ bulan saat harga sideways → silent distribution.
🟡 STH-NUPL sangat negatif (<-0.30) tapi LTH masih >0.65 → kemungkinan mid-cycle atau deep bull dip, cross-check apakah LTH juga mulai turun.
🟡 STH mulai naik lebih cepat dari LTH dari zona negatif → Pre Detection signal, monitor ketat untuk Start of Bull.

---

## 7. CONFIDENCE LEVELS DAN KNOWN LIMITATIONS

### Apa yang High Confidence

- Bear bottom identification via all-three-negative + gap near zero: 2 full episodes (2019 Window End, 2022 cluster), high conviction
- Start of bull via ratio <1 (both positive) + gap negatif: 2/2, paling distinctive fingerprint dalam seluruh dataset
- Lower high detection via STH near zero + gap >0.60 + ratio >11: 4/4 di 2021-2025
- Mid-cycle correction via gap >1.0: belum pernah terjadi di fase lain (n=1, tapi eksklusif)
- Ratio sign flip atau extreme (>50) saat NUPL >0.50 → danger zone: terjadi di setiap bear start dan lower high dalam dataset

### Apa yang Medium Confidence

- Bull dip buy signals via STH < -0.10: works 6/8 times tapi 2 failures (flat returns) di late 2024
- Cycle peak warning via NUPL > 0.55: works tapi threshold shifting setiap cycle
- Bear decline start detection: pattern terlihat consistent tapi hard to distinguish from deep bull dip in real-time
- Gap trajectory saat bear decline: gap narrowing dari >0.90 ke <0.40 adalah progression marker, tapi speed bervariasi

### Apa yang Low Confidence — Perlu Di-Verify

- Apakah diminishing returns linear? Kita punya 3 data points — bisa jadi asymptotic (converging to some floor) bukan linear decline
- Mid-cycle correction identification: n=1, terlalu kecil untuk generalize
- Upper range recovery: n=3 dengan 1 failure (2019), unreliable standalone
- Ratio behavior di next cycle: dengan STH semakin compressed, ratio extreme akan semakin sering terjadi → threshold "extreme" perlu recalibration
- Semua threshold numerik berlaku di next cycle? Unknown — ETF, institutional adoption, dan structural changes bisa shift semuanya

### Apa yang Perlu Dilakukan Selanjutnya

1. Cross-reference dengan MVRV Z-Score untuk validate cycle peak detection — NUPL ambiguity di 0.55 range perlu dipecahkan
2. Cross-reference dengan SOPR untuk validate bull dip vs bear decline di NUPL 0.40–0.55 range
3. Monitor apakah diminishing returns terus berlanjut atau mulai floor — next cycle peak NUPL prediction: 0.47–0.50? Atau lower?
4. Backtest combined scoring system: NUPL score + MVRV score + SOPR score → aggregate regime identification

---

## 7B. CATATAN UNTUK POSISI SAAT INI

Berdasarkan data terakhir (Lower High 2025 Confirmation, Okt 28, 2025):
- NUPL: 0.507
- STH-NUPL: -0.001 (baru crossing negatif)
- LTH-NUPL: 0.669

**Posisi dalam mapping:** Bear Market Decline, fase awal.

LTH masih di 0.669 — jauh dari negatif. Berdasarkan trajectory 2018 dan 2022:
- 2018: LTH mulai di 0.903 saat decline start, butuh ~4 bulan untuk turun ke negatif
- 2022: LTH mulai di ~0.63, turun ke negatif lebih cepat (~3 bulan, dipercepat Luna crash)
- 2025: LTH mulai di 0.669 — estimasi kasar, perlu 3–5 bulan untuk mendekati negatif jika trajectory konsisten

Per Jun 2026, NUPL sudah di kisaran 0.355–0.420, LTH masih di area 0.56–0.58 — bear decline berlanjut sesuai trajectory tapi belum mencapai deep capitulation.

**Yang harus dimonitor:** LTH-NUPL mendekati 0.30 = deep bear territory, approaching capitulation. LTH crossing nol = Bear Bottom Near territory sedang terbentuk.

---

## 8. GAP (LTH−STH) DAN RATIO (LTH/STH) — DERIVED METRICS

Dua derived metrics ini tidak perlu data tambahan — cukup dari LTH-NUPL dan STH-NUPL yang sudah ada. Tapi pattern yang muncul dari keduanya memberikan dimensi ekstra yang tidak terlihat dari ketiga metrik secara terpisah.

### 8.1 Gap = LTH-NUPL − STH-NUPL

**Definisi operasional:** Selisih profit antara long-term holders dan recent buyers. Positif artinya LTH lebih profitable dari STH (normal). Negatif artinya STH lebih profitable dari LTH (structural reversal, hanya di early bull).

**Reference values per regime dari data:**

| Regime | Gap Range | Catatan |
|--------|-----------|---------|
| Cycle Peak | 0.43–0.62 | Gap melebar cycle ke cycle karena STH makin compressed |
| Local Top | 0.47–0.64 | Tumpang tindih dengan cycle peak |
| Lower High | 0.657–0.686 | Konsisten lebar (0.65+) di semua cycle terkonfirmasi |
| Bull Dip | 0.40–0.89 | Lebar, tapi LTH masih solid positif |
| **Mid-Cycle Correction Bottom** | **>1.0 (1.12–1.20)** | **Eksklusif — tidak pernah terjadi di fase lain** |
| Bear Decline Start | 0.62–0.94 | Gap mulai lebar saat STH jatuh ke negatif |
| Bear Decline Mid/Late | 0.38–0.86 | Narrowing seiring LTH ikut turun |
| Bear Bottom (deep) | −0.12 to +0.21 | Near zero atau negatif — LTH dan STH sama-sama distress |
| Pre Detection | −0.07 to −0.14 | **Negatif** — STH recovering lebih cepat dari LTH |
| Start of Bull | **−0.03 to −0.04** | **Negatif dan kecil** — crossover zone |
| Upper Range Recovery | 0.13–0.28 | Moderate, kedua cohort sama-sama modest profit |

**Tiga pola paling distinctive:**

1. **Gap >1.0:** Secara eksklusif terjadi di Mid-Cycle Correction (Jun–Jul 2021). Tidak pernah muncul di regime lain. Kalau terlihat di future cycles, ini adalah signature yang sangat kuat untuk mid-cycle, bukan bear market.

2. **Gap negatif (STH > LTH) dengan keduanya positif:** Hanya di Start of Bull 2019 (−0.040) dan Start of Bull 2023 (−0.031). Ini artinya buyer baru yang akumulasi di bottom sudah profit, sementara holder lama baru saja keluar dari negatif. Structural reversal.

3. **Gap negatif dengan keduanya negatif:** Pre Detection dan sekitar bear bottom. LTH lebih dalam negatif dari STH (di 2022 cycle, karena buyer 2021 sudah masuk kategori LTH). Gap mendekati nol di window end type bottoms.

**Diminishing returns pada gap:** Gap di Cycle Peak bertumbuh setiap cycle (0.43 → 0.46 → 0.62) karena STH peak values collapse lebih cepat dari LTH. Ini berarti di next cycle, gap >0.70 bisa menjadi "normal" di Cycle Peak territory — threshold danger zone perlu dinaikkan.

---

### 8.2 Ratio = LTH-NUPL / STH-NUPL

Ratio mengamplifikasi gap, terutama saat STH mendekati nol. Interpretasinya bergantung pada sign keduanya:

**Lima zona ratio:**

**Zona 1 — Ratio 0 sampai <1 (Both Positive):**
STH lebih profitable dari LTH. Hanya terjadi di Start of Bull 2019 (0.785) dan Start of Bull 2023 (0.706). Ini adalah fingerprint paling eksklusif dalam seluruh dataset. Jika terlihat di future cycles dengan kedua metrik positif dan rendah (<0.20), ini adalah high-confidence start of bull signal.

**Zona 2 — Ratio 1.5 sampai 4 (Both Positive):**
Range normal bull market mid-stage. Cycle Peak 2017 berada di sini (1.8–2.0). Local Top 2024 = 3.0–3.9. Upper Range 2023 = 1.6–5.7. Bull masih sehat, tidak ada extreme stress.

**Zona 3 — Ratio 4 sampai 15 (Both Positive):**
Late bull atau bull dip territory. Gap melebar tapi STH masih positif. Bull Dip Jan 2024: 8–18. Cycle Peak 2025: 8–11. Local Top Jan 2025: 5–7. Mulai perlu waspada.

**Zona 4 — Ratio >15 atau Sign Flip berulang (STH mendekati nol):**
STH di zero-crossing zone. Ratio tidak stabil — bisa dari +73 ke −561 dalam sehari (Lower High 2025 Confirmation). Angka absolutnya tidak bermakna, yang bermakna adalah: *ini tanda STH hampir tepat di breakeven*. Konteks menentukan apakah ini bull dip atau lower high. Filter: kalau NUPL >0.50 dan gap >0.60, ini lower high territory.

Contoh concrete dari data:
- Bear Decline Start 2018: ratio −24.9, lalu esok harinya bear dimulai
- Bear Market Decline Mid 2022: ratio 57 → −257 → 325 dalam 8 hari → Luna crash
- Lower High 2025: ratio 50 → 73 → −561 → confirmed bear decline

**Zona 5 — Both Negative (Bear Bottom Zone):**
Ratio positif tapi interpretasi terbalik: ratio = |LTH loss| / |STH loss|.
- Ratio <1: STH lebih dalam loss dari LTH (typical, karena 2018-era buyer sudah jadi LTH tapi dengan cost basis lebih rendah)
- Ratio ~1: Semua cohort equally distressed → deep capitulation → bottom signal
- Ratio >1 (both negative): LTH lebih dalam loss dari STH → 2022 anomaly (buyer 2021 di puncak sudah jadi LTH)

Bear Bottom 2018 Tier 1: ratio 0.586 (STH lebih loss, tapi recovery eventual terjadi)
Bear Bottom Window End: ratio 1.044 ← near-perfect equalization → classic bottom
Bear Bottom 2022 Actual Price Low: ratio 1.498 (LTH lebih loss)
Bear Bottom 2022 Final Low: ratio 2.058 (LTH jauh lebih loss, anomali 2022)

**Pattern kritis:** Both-negative ratio mendekati 1.0 adalah salah satu kondisi yang paling mendahului recovery besar. Window End Jan 2019 (ratio 1.044) → 90 hari kemudian +132%. FTX Collapse ratio 1.212 → dalam 90 hari harga naik >50%.

---

### 8.3 Tiga Tipe Konvergensi dan Divergensi Antar Metrik

**Convergence Type 1 — Distress Convergence (Near Bottom):**
Semua tiga metrik mendekati nilai yang sama di zona negatif. Gap mendekati nol dari atas. Ratio mendekati 1.0. Ini adalah "equalized pain" — tidak ada cohort yang lebih beruntung dari yang lain. Terjadi di Bear Bottom Window End 2019 dan sekitar FTX collapse 2022. Selalu diikuti recovery jangka menengah.

**Convergence Type 2 — Low-Level Positive Convergence (Start of Bull):**
Semua tiga positif tapi rendah dan berdekatan, dengan STH sedikit di atas LTH. Gap negatif kecil. Ratio di bawah 1.0. Ini adalah "fresh start" — semua cohort profit kecil, buyer baru sedikit lebih untung dari holder lama. Terjadi di Start of Bull 2019 dan 2023. Paling clean sebagai entry confirmation.

**Convergence Type 3 — Mid-Cycle Near-Perfect Convergence (Anomali 2023):**
Bull Dip Mar 2023 menghasilkan NUPL ≈ STH ≈ LTH ≈ 0.023, gap hampir nol, ratio 1.02. Ini bukan typical convergence — terjadi karena bull cycle baru saja dimulai dari zero sehingga tidak ada cohort yang sudah punya "compound profit." Tidak ada analog di 2017 atau 2021.

**Divergence Type 1 — LTH Turun Sementara STH Recover (Bullish):**
Terjadi di Pre Detection dan awal Start of Bull. LTH masih negatif dan semakin dalam (buyer cycle sebelumnya masih processing loss), sementara STH recover ke near-zero atau positif (akumulator baru di bottom mulai profit). Gap bergerak dari mildly negatif ke semakin negatif kemudian mulai positif. Ini adalah divergence paling bullish dalam dataset.

**Divergence Type 2 — STH Turun Sementara LTH Masih Tinggi (Bearish):**
Terjadi di setiap bear decline start dan lower high. Gap melebar dari LTH yang stable ke STH yang jatuh. Aggregate NUPL masih terlihat sehat (0.45–0.50) tapi sudah cracked di lapisan STH. Ini adalah divergence paling berbahaya untuk di-ignore karena NUPL menyembunyikannya. Contoh: Bear Decline Start 2018 (NUPL 0.492 terlihat "oke" tapi STH sudah −0.036) → 30 hari kemudian harga −25%.

**Divergence Type 3 — Ratio Sign Instability (Transition Warning):**
Ketika ratio berulang kali berganti sign dalam periode singkat (STH bergerak dari sedikit positif ke sedikit negatif dan kembali), itu adalah tanda STH tepat di breakeven level. Ini terjadi tepat sebelum transisi besar: Bear Decline Mid 2022 sebelum Luna, Lower High 2025 sebelum bear confirmed. Bukan untuk di-trade langsung, tapi sebagai context bahwa pasar sedang di decision point kritis.

---

### 8.4 Diminishing Returns pada Gap dan Ratio (Cross-Cycle)

| Cycle | Cycle Peak Gap | Cycle Peak Ratio | Lower High Gap | Bear Bottom Min Gap |
|-------|---------------|-----------------|----------------|---------------------|
| 2017 | 0.433 | 1.81 | 0.686 | +0.214 (2018 Tier 1) |
| 2021 | 0.459 | 2.53 | 0.657 | −0.123 (2022 Final Low) |
| 2025 | 0.620 | 8.58 | 0.661 | N/A (bear ongoing) |

Cycle Peak gap **naik** setiap cycle karena STH collapse lebih cepat dari LTH. Cycle Peak ratio naik sangat drastis (1.8 → 2.5 → 8.6) — STH di 2025 hampir breakeven di puncak cycle.

Implikasi untuk next cycle: Cycle Peak gap bisa >0.70. Ratio di Cycle Peak bisa >15. Lower High ratio mungkin >100 secara rutin. Threshold yang "extreme" di 2025 cycle akan menjadi "normal" di next cycle — perlu recalibration saat entering next bull.

Bear bottom gap minimum bervariasi: 2018 masih +0.21 (LTH less underwater than STH), 2022 turun ke −0.12 (LTH more underwater). Kalau trend berlanjut, 2026+ bear bottom mungkin punya gap lebih negatif karena buyer 2024-2025 (sekarang jadi LTH) punya cost basis tinggi.

---

### 8.5 Checklist Penggunaan Gap dan Ratio dalam Analisis

Saat menganalisis current market, check secara berurutan:

1. **Apakah semua tiga metrik negatif?** → Bear bottom zone. Cek gap: kalau <0.10 (near zero atau negatif) → deep capitulation, potential bottom window.

2. **Apakah gap negatif dengan keduanya positif dan rendah?** → Start of bull fingerprint. Konfirmasi ratio <1.0.

3. **Apakah ratio berganti sign atau >50 dengan NUPL >0.50?** → STH di zero-crossing, danger zone. Jangan tambah posisi, monitor ketat.

4. **Apakah gap >0.60 dengan NUPL >0.50?** → Lower high atau cycle peak territory. Bukan bull dip.

5. **Apakah gap >1.0 dengan STH sangat negatif (<−0.30) dan LTH masih >0.70?** → Mid-cycle correction signature. Bila recovery terjadi, ini bisa menjadi re-entry point, bukan bear.

6. **Apakah gap sedang narrowing dari >0.80 ke <0.50 secara gradual?** → Bear market progression, masih jauh dari bottom. Monitor kapan semua tiga metrik mencapai negatif.