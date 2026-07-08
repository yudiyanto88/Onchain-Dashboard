# Knowledge Base: Price Level Family — RP, STH/LTH RP, CVDD, MVRV 0σ, AVIV Mean & Upper 0.5σ Price

**Version:** 1.4 
**Created:** 21 Juni 2026
**Data Source:** ChartInspect.com (Glassnode-sourced)
**Coverage:** 1 Januari 2016 – 21 Juni 2026

**Metrik final di KB ini:** Realized Price (RP), STH Realized Price, LTH Realized Price, CVDD, MVRV 0σ, AVIV Mean Price, AVIV Upper 0.5σ Price.

---

## 0. CATATAN METODOLOGI & KARTU PERUBAHAN DARI VERSI SEBELUMNYA

### 0.1 Metodologi anchor

Untuk setiap event window di CSV, anchor date dipilih: harga tertinggi dalam window untuk Cycle Peak/Local Top/Lower High/Upper Range Recovery, harga terendah untuk Bull Dip/Bear Bottom, tanggal akhir window untuk Pre Detection/Start of Bull. **Ini beda dari KB v1.0 lama** yang kadang pakai range tanggal — jadi angka di dokumen ini bisa sedikit berbeda dari versi sebelumnya untuk event yang sama. Ini perbedaan titik sampling, bukan kontradiksi data.

### 0.2 Koreksi yang ditemukan dari proses re-verifikasi (penting, baca ini)

1. **Section 6.1 KB lama, klaim "Price/RP selalu di atas 2.0 dari Mar 2024 sampai Okt 2025 (19 bulan)" — SALAH, sudah dikoreksi.** Cek harian terhadap 573 hari di window itu: Price/RP turun ke **1.72** pada 6 Sep 2024 (Bull Dip Sep 2024), dan **129 dari 573 hari (22.5%) ada di bawah 2.0**. Window itu persistently elevated, tapi tidak monoton di atas 2.0.
2. **Section 6.3 KB lama, klaim LTH RP +539% di bear 2018 — anchor-nya tidak konsisten dengan section 2.6, sudah diseragamkan.** Angka $671 di KB lama adalah LTH RP di tanggal Lower High (6 Jan 2018), bukan di Cycle Peak (16 Des 2017) seperti anchor yang dipakai section 2.6 untuk metrik lain di tabel yang sama. Dengan anchor Cycle Peak yang konsisten, angkanya **+716%**, bukan +539%. Di dokumen ini, semua persentase perubahan LTH dihitung dari anchor Cycle Peak secara konsisten.
3. **Section 4.4 KB lama, rule "Healthy Bull Dip via Price/STH ≥ 1.0, 8/8 hit rate" — confidence diturunkan, bukan dihapus.** Dengan anchor "hari harga terendah literal" (paling konservatif), 4 dari 8 event yang dulu diklasifikasi "Healthy" (Mar 2017, Jul 2017, Sep 2017, Sep 2020) ternyata Price/STH-nya di bawah 1.0. Lebih penting: **daya pembeda rule ini hilang** — grup "Healthy" (n=4) dan "Stressed" (n=11) di recompute ini sama-sama 100% recover positif dalam 30 hari, termasuk recovery terkuat di seluruh dataset (Jul 2017, +118%) justru ada di grup "Stressed". Kemungkinan besar "bull dip selalu recover" adalah fungsi dari cara event di-label secara retrospektif (semua event "Bull Dip" di dataset per definisi adalah dip yang ujungnya jadi entry point), bukan fungsi dari level Price/STH spesifik. Lihat section 4.4 revisi di bawah.
4. **Section 5.2 KB lama, divergence 3, range STH/LTH "bottom forming" terlalu sempit — dilebarkan.** 2019 Feb-Mar: range aktual 0.890–0.981 (bukan 0.90-0.94). 2023 Jan-Feb: range aktual 0.880–0.996 (bukan 0.88-0.92).

### 0.3 Apa yang confirmed solid dari re-verifikasi (tidak berubah)

STH/LTH < 1.0 sebagai bear-bottom signal (nol false positive di 10 tahun data), STH/RP konstan ~2.0 di setiap cycle peak, RP acceleration +176% Jan2023→Okt2025, nilai breach RP saat COVID ($5,661, exact match), STH RP false-signal count (60 episode terpisah, konsisten dengan "50+"), dan pola diminishing Price/STH di setiap ATH berturutan — semua re-test dengan hasil presisi tinggi terhadap KB versi sebelumnya.

---

## 1. DEFINISI & MEKANIK

### 1.1 Realized Price (RP)

Rata-rata harga di mana seluruh supply BTC terakhir kali bergerak on-chain, weighted by volume — cost basis agregat seluruh network. Bergerak lambat, support kuat di bear market tapi bisa ditembus dan stay below selama berbulan-bulan (2018: ~5 bulan).

### 1.2 STH & LTH Realized Price

Cost basis rata-rata untuk koin yang dipegang <155 hari (STH, sensitif terhadap price action terbaru) dan >155 hari (LTH, conviction holders, naik di bear market karena "aging effect" — koin mahal dari bull market masuk kategori LTH, bukan karena LTH beli mahal).

### 1.3 CVDD (Cumulative Value-Days Destroyed)

Diciptakan Willy Woo. Rasio kumulatif USD value dari Coin-Days Destroyed terhadap umur network. **Floor paling kuat di seluruh keluarga metrik ini** — harga BTC cuma pernah di bawah CVDD selama **2 hari dalam 10 tahun** (9 & 21 Nov 2022, FTX collapse).

### 1.4 MVRV 0σ (M0s)

⚠️ Definisi tidak terverifikasi penuh dari dokumentasi ChartInspect resmi. Berdasarkan perilaku data, kemungkinan terkait RP × rata-rata historis MVRV (expanding window). Berfungsi sebagai bagian dari upper cost-basis cluster — bergerak smooth, lambat, sering jadi level yang ditembus pertama kali (tertinggi di antara metrik cost-basis) saat harga mulai decline dari puncak.

### 1.5 AVIV Mean Price & AVIV Upper 0.5σ Price

Diturunkan dari konsep AVIV Ratio (Active-Value-to-Investor-Value), riset Glassnode/ARK Cointime Economics. Raw data dari ChartInspect berbentuk rasio kecil (~1.05–1.30), bukan dollar — di KB ini, dikonversi ke dollar level via referensi cost-basis internal sehingga didapat **AVIV Mean Price** dan **AVIV Upper 0.5σ Price** dalam satuan dollar yang langsung bisa dibandingkan ke harga pasar.

**Catatan ketidakcocokan dengan riset:** Glassnode mengklaim AVIV Ratio historically mean/median dekat 1.0. Di dataset 2016-2026 ini, rasio AVIV yang dipakai punya **mean 1.24, median 1.20** — bukan 1.0. Kemungkinan karena window data cuma 10 tahun (bukan dari 2009), atau perbedaan metodologi recompute. **Jangan pakai "1.0" sebagai fair-value anchor — pakai threshold empiris dari dataset ini sendiri.**

### 1.6 Hierarki Struktural (Update Final)

Hierarki yang tersisa di KB ini **100% stabil sepanjang 10 tahun tanpa exception:**

**CVDD < Realized Price < AVIV Mean Price < AVIV Upper Price**

MVRV 0σ (M0s) berada di sekitar AVIV Mean Price tapi **urutan relatifnya TIDAK stabil** — AVIV Mean Price < M0s di 82% hari, tapi terbalik di 18% hari, terkonsentrasi di periode mid-late bull (2021, 2024). **Treat M0s dan AVIV Mean Price sebagai satu cluster "upper band", bukan dua level terpisah yang presisi-terurut.** M0s < AVIV Upper Price berlaku 95.8% dari waktu (cukup stabil untuk dipakai sebagai pengurutan kasar: M0s biasanya di bawah AVIV Upper).

STH dan LTH tidak masuk tangga ini — STH paling volatile (bisa di bawah RP saat bear deep, bisa di atas semua metrik termasuk AVIV Upper saat euphoria).

---

## 2. HISTORICAL BEHAVIOR PER REGIME TRANSITION

### 2.1 CYCLE PEAK

**Events:** 2017 (16 Des), 2021 (8 Nov), 2025 (6 Okt)

| Cycle | Price | Price/RP | Price/CVDD | Price/M0s | Price/AvivMean | Price/AvivUp | STH/LTH |
|---|---|---|---|---|---|---|---|
| 2017 | $19,538 | 4.39 | 11.22 | 2.32 | 2.48 | 2.06 | 35.6 |
| 2021 | $67,525 | 2.85 | 5.37 | 1.54 | 1.51 | 1.27 | 4.24 |
| 2025 | $124,715 | 2.28 | 2.98 | 1.25 | 1.30 | 1.13 | 3.39 |

**Diminishing di semua metrik tanpa kecuali** — termasuk STH/LTH yang juga compress drastis tiap cycle (35.6 → 4.24 → 3.39). Price/CVDD turun paling tajam secara persentase (73% dari 2017 ke 2025).

**Sinyal paling clean: AVIV Upper Price.** Di ketiga cycle peak, Price/AvivUp selalu >1.0 dan diminishing rapi (2.06 → 1.27 → 1.13) — dan dari analisis breach (section 4), justru periode "sustained di atas AVIV Upper" yang berakhir tepat di sekitar titik ini adalah salah satu sinyal paling reliable di seluruh dokumen.

### 2.2 LOCAL TOP

**6 events:** Mar 2021, Apr 2021 ATH, Mar 2024 ATH, Des 2024 ATH, Jan 2025 ATH, Jul-Aug 2025 ATH

| Event | Price/RP | Price/CVDD | Price/M0s | Price/AvivMean | Price/AvivUp |
|---|---|---|---|---|---|
| Mar 2021 | 3.78 | 7.53 | 2.65 | 1.97 | 1.66 |
| Apr 2021 (ATH) | 3.43 | 7.04 | 2.39 | 1.76 | 1.48 |
| Mar 2024 (ATH) | 2.75 | 3.62 | 1.78 | 1.54 | 1.30 |
| Des 2024 (ATH) | 2.70 | 3.64 | 1.81 | 1.46 | 1.24 |
| Jan 2025 (ATH) | 2.52 | 3.44 | 1.69 | 1.38 | 1.18 |
| Jul-Aug 2025 (ATH) | 2.38 | 3.12 | 1.55 | 1.35 | 1.18 |

**Degradasi progresif bersih di semua metrik, monoton, di setiap ATH berturutan** — paralel persis dengan pola Price/STH yang sudah established (1.57 → 1.43 → 1.31 → 1.26 → 1.15 → 1.12). Empat metrik independen (RP, CVDD, M0s, AVIV) semua confirm pola yang sama — ini memperkuat confidence bahwa diminishing-margin-at-ATH adalah pola struktural genuine.

### 2.3 LOWER HIGH CONFIRM TOP CYCLE

**4 events:** 2018, 2021, 2025, 2025 Confirmation

| Event | Price/RP | Price/CVDD | Price/M0s | Price/AvivMean | Price/AvivUp |
|---|---|---|---|---|---|
| 2018 | 3.31 | 8.37 | 1.91 | 1.87 | 1.55 |
| 2021 | 2.33 | 4.35 | 1.37 | 1.24 | 1.05 |
| 2025 | 2.06 | 2.66 | 1.24 | 1.18 | 1.03 |
| 2025 Confirmation | 2.03 | 2.61 | 1.21 | 1.16 | 1.02 |

**Temuan paling kuat dan paling actionable di seluruh dokumen: Price/AvivUp ≈ 1.0 di lower high (2021: 1.05, 2025: 1.03, 2025-Conf: 1.02).** Ini cross-confirmation independen terhadap rule lama "Price/STH ≤ 1.05 di lower high = bear confirmed" — dua metrik beda basis perhitungan, hasil konvergen ke threshold yang sama persis. Lower High 2018 tetap outlier (konteks cycle pertama, scale jauh berbeda).

### 2.4 BULL DIP

**15 events.** Pola Tipe 1 (Healthy)/Tipe 2 (Stressed) berdasarkan Price/RP atau Price/CVDD masih bisa dipakai untuk deskripsi kualitatif kedalaman dip, **TAPI lihat section 0.2 poin 3 — rule Price/STH≥1.0 sebagai pembeda kekuatan recovery TIDAK terbukti reliable di recompute ini.**

| Kelompok | Price/RP range | Recovery 30d |
|---|---|---|
| Semua 15 bull dip | 1.02 – 2.59 | **15/15 positif** (range +0.3% sampai +118%) |

**Tidak ada satupun bull dip di dataset ini yang gagal recover dalam 30 hari** — tapi ini selection bias dari cara dataset dilabel (event "Bull Dip" secara definisi adalah dip yang historically jadi entry point), bukan bukti predictive bahwa SEMUA dip akan recover. **Jangan jadikan "100% historical recovery rate" sebagai jaminan forward-looking.**

Yang tetap berguna sebagai deskripsi (bukan trigger): dip di awal cycle (2017, awal 2020-21) cenderung dangkal relatif ke RP (Price/RP 1.5-2.6); dip di pertengahan-akhir cycle (2023-2025) cenderung lebih dalam (Price/RP 1.0-1.8), konsisten dengan cycle yang makin matang.

### 2.5 MID-CYCLE CORRECTION

**n=1. Reliability rendah, treat sebagai catatan kualitatif.**

| | Price | Price/RP | Price/CVDD | STH/LTH |
|---|---|---|---|---|
| Start (8 Mei 2021) | $59,074 | 2.95 | 6.02 | 8.72 |
| Bottom (20 Jul 2021) | $29,837 | 1.54 | 2.79 | 5.50 |

**Pembeda paling jelas dari bear bottom genuine: Price/CVDD masih 2.79 (jauh di atas 1.0) dan STH/LTH masih 5.50 (jauh di atas <1.2 convergence zone) meski harga sudah crash -50%.** Kalau crash besar terjadi tapi dua metrik ini masih jauh dari level capitulation, kemungkinan ini correction dalam bull cycle, bukan bear market start — terlepas dari berapa persen harga sudah turun. (n=1, treat dengan hati-hati.)

### 2.6 BEAR MARKET DECLINE — DATA GAP

Tidak ada event berlabel ini di CSV. Proxy: 28 Okt 2025 (Lower High Confirmation) → 21 Jun 2026 (data terakhir, masih ongoing).

| | 6 Okt 2025 (Peak) | 21 Jun 2026 (sekarang) | Δ |
|---|---|---|---|
| Price | $124,715 | $64,154 | −48.6% |
| RP | $54,580 | $53,398 | hampir flat |
| CVDD | $41,890 | $48,840 | +16.6% |
| STH | $113,635 | $71,483 | −37.1% |
| LTH | $36,830 | $49,690 | +34.9% |
| STH/LTH | 3.09 | 1.44 | compress signifikan, **belum** <1.2 |

Pola bear-signature klasik (LTH naik, STH turun tajam) sudah jelas terlihat dan match pola 2018 & 2021-22. Status detail di section 9.

### 2.7 BEAR BOTTOM NEAR

**6 events**

| Event | Price/RP | Price/CVDD | Price/M0s | Price/AvivMean | STH/LTH |
|---|---|---|---|---|---|
| 2018 Tier 1 | 0.70 | 1.00 | 0.34 | 0.40 | 1.15 |
| Window End 2019 | 0.77 | 1.03 | 0.38 | 0.43 | 0.97 |
| COVID Flash | 0.91 | 1.13 | 0.46 | 0.51 | 1.63 |
| FTX Collapse | 0.88 | 1.16 | 0.43 | 0.48 | 0.98 |
| Actual Low 2022 | 0.78 | **0.98** | 0.39 | 0.42 | 0.92 |
| Final Low 2022 | 0.82 | 1.02 | 0.41 | 0.45 | 0.90 |

**Price/CVDD adalah metrik paling presisi untuk identifikasi bear bottom** — median 1.03, range sangat sempit (0.98–1.16) di 6 event lintas 2 cycle berbeda, jauh lebih konsisten dari Price/RP (range 0.70–0.91). Satu-satunya pelanggaran ke bawah 1.0 (0.982) adalah salah satu dari hanya 2 hari sepanjang 10 tahun harga pernah di bawah CVDD.

**STH/LTH tidak selalu di bawah 1.0 persis di titik harga terendah** (2018 Tier1=1.15, COVID=1.63) — convergence STH/LTH<1.0 terjadi di WINDOW sekitar bottom (lihat section 4.1), bukan harus persis di hari harga paling rendah. Jangan baca STH/LTH>1.0 di satu titik sebagai "belum bottom" tanpa cek window beberapa minggu sekitarnya.

### 2.8 PRE DETECTION START OF BULL MARKET

**3 events**

| Event | Price/RP | Price/CVDD | Price/AvivMean | STH/LTH |
|---|---|---|---|---|
| 2019 Ref | 0.89 | 1.18 | 0.554 | 0.940 |
| 2019 | 0.90 | 1.17 | 0.557 | 0.898 |
| 2023 | 0.96 | 1.16 | 0.550 | 0.884 |

**Pola kunci: Price/CVDD sudah konsisten >1.0 (1.16-1.18), confirming bottom sudah lewat, sementara Price/RP masih <1.0 (0.89-0.96), market masih net rugi.** Divergence CVDD-sudah-positif vs RP-belum-positif adalah early signal yang jelas untuk fase ini — CVDD duluan confirm, RP menyusul belakangan. Price/AvivMean luar biasa konsisten (0.550-0.557 di 3/3 instance, hampir identik).

### 2.9 START OF BULL MARKET CONFIRMATION

**2 events**

| Event | Price/RP | Price/CVDD | Price/AvivMean | STH/LTH |
|---|---|---|---|---|
| 2019 | 1.19 | 1.55 | 0.681 | 0.954 |
| 2023 | 1.10 | 1.34 | 0.628 | 0.967 |

**Temuan tidak intuitif: Price/AvivMean MASIH di bawah 1.0 (0.63-0.68) bahkan saat Start of Bull resmi confirmed, padahal Price/RP sudah positif (1.10-1.19).** Kalau pakai AVIV Mean Price sebagai konfirmasi "market sudah profitable" dengan threshold yang sama seperti RP (>1.0), kamu akan telat masuk jauh. STH/LTH juga masih <1.0 (0.95-0.97) — confirming ini masih fase EARLY, bukan late cycle, meski bull sudah resmi confirmed.

### 2.10 UPPER RANGE RECOVERY

**3 events**

| Event | Price/RP | Price/CVDD | Price/M0s | STH/LTH |
|---|---|---|---|---|
| 2019 (Failed) | 2.55 | 3.56 | 1.41 | 1.77 |
| Mar 2023 | 1.53 | 1.84 | 0.85 | 1.22 |
| Jun-Jul 2023 | 1.54 | 1.85 | 0.86 | 1.70 |

Upper Range 2019 yang akhirnya gagal punya Price/CVDD jauh lebih tinggi (3.56) dibanding dua Upper Range 2023 yang sehat (1.84-1.85) — konsisten dengan catatan overextended early-cycle move.

---

## 3. RULE RANGES — SELL SIGNALS

### 3.1 RULE (PRIMARY): Sustained Break di Bawah AVIV Upper 0.5σ = Cycle Top Warning

**Premise:** Harga sustained (14 hari+) di atas AVIV Upper Price = late-stage euphoria. Berakhirnya streak ini = early warning cycle sudah/segera top.

**Data evidence — SEMUA 12 episode sustained-above-band di 10 tahun, nol false positive:**

| Cycle | Streak berakhir | Cycle Peak aktual | Lower High Confirm | Lead time vs Lower High |
|---|---|---|---|---|
| 2017-18 | 16 Jan 2018 | 16 Des 2017 | 6 Jan 2018 | 10 hari setelah (lagging) |
| 2021 | 26 Nov 2021 | 8 Nov 2021 | 1 Des 2021 | 5 hari sebelum (leading) |
| 2025 | 15 Okt 2025 | 6 Okt 2025 | 26 Okt 2025 | **11 hari sebelum (leading)** |

**Lead-time membaik tiap cycle** — di 2025, sinyal ini muncul 11 hari sebelum lower high resmi terkonfirmasi.

- **Hit rate: 12/12 episode (100%).** Semua sustained-above-band episode match ke periode bull-euphoria yang genuine (2017 full bull run, Upper Range 2019 Failed yang persis ke-detect sebagai 23-hari episode terpisah, 2020-21 bull run, kedua leg 2021 ke Cycle Peak, Local Top Mar 2024, dan kedua leg 2024-2025 ke Cycle Peak Okt 2025).
- **False signal: tidak ditemukan.**
- **Confidence: TINGGI.** Ini rule paling robust di seluruh dokumen ini untuk sisi sell.

### 3.2 RULE: Lower High Confirmation via Price/AvivUp ≈ 1.0 (cross-confirmation untuk rule Price/STH ≤ 1.05 lama)

**Data evidence:** Lower High 2021 (1.05), 2025 (1.03), 2025 Conf (1.02) — semua mendekati 1.0. Lower High 2018 outlier (1.55, konteks beda).

- **Hit rate: 3/3 cycle terbaru.**
- **Confidence: Tinggi**, sebagai cross-check independen terhadap rule Price/STH yang sudah established — dua basis perhitungan beda, kesimpulan sama.

### 3.3 RULE: Price/CVDD Degradation Across Cycle — Secondary Confirmation Saja

Price/CVDD di cycle peak turun drastis tiap cycle (11.22 → 5.37 → 2.98) dan di local top juga monoton turun. **Threshold absolut tidak stabil** (basis CVDD tumbuh kumulatif, jadi Price/CVDD struktural akan terus mengecil tiap cycle terlepas dari market dynamics). Pakai sebagai rate-of-change check (apakah Price/CVDD di ATH baru lebih rendah dari ATH sebelumnya dalam cycle yang sama), bukan threshold mutlak. **Confidence: Medium**, n kecil (3 cycle peak).

### 3.4 RULE: Mid-Cycle Correction vs Bear — Price/CVDD dan STH/LTH sebagai Pembeda

Kalau crash besar (>40%) terjadi tapi Price/CVDD masih >2.0 DAN STH/LTH masih >3.0, kemungkinan besar mid-cycle correction, bukan bear market start. **n=1 (cuma 1 sample historis), jangan jadikan basis keputusan sizing besar tanpa konfirmasi tambahan.**

---

## 4. RULE RANGES — BUY SIGNALS

### 4.1 RULE (PRIMARY, CONFIRMED SOLID): STH/LTH < 1.0 = Accumulation Zone

**Re-verified ulang sesi ini: nol false positive di 10 tahun data.** STH/LTH<1.0 cuma terjadi di 2 window total (219 hari): 29 Jan–7 Mei 2019 dan 1 Nov 2022–1 Mar 2023 — keduanya match persis ke 2 bear bottom yang dikenal.

- **Threshold:** STH/LTH < 1.2 = mulai accumulate, < 1.0 = aggressive accumulate.
- **Hit rate: 2/2 major bear cycle, nol false signal.**
- **Confidence: TINGGI.** Rule paling reliable di seluruh dokumen untuk sisi buy.

### 4.2 RULE: Price/CVDD < 1.05 = Extreme Accumulation Zone

6/6 Bear Bottom Near event berada di range Price/CVDD 0.98-1.16. Harga cuma 2 hari pernah benar-benar di bawah CVDD sepanjang 10 tahun. **Hit rate: 6/6, nol false signal di luar konteks bear bottom genuine.** Sinyal ini baru bisa dikonfirmasi SETELAH harga sudah dekat/di bawah CVDD (bukan leading), tapi confidence-nya TINGGI begitu trigger.

### 4.3 RULE: Divergence Price/CVDD>1.0 sementara Price/RP<1.0 = Pre Detection Signal

3/3 instance Pre Detection menunjukkan pola CVDD sudah confirm bottom (>1.0) sementara RP masih negatif (<1.0). **Confidence: Medium-High**, tapi cuma dari 2 bear cycle (2018-19, 2022-23).

### 4.4 RULE (REVISI, CONFIDENCE DITURUNKAN): Healthy vs Stressed Bull Dip via Price/RP atau Price/CVDD

**Rule lama (Price/STH≥1.0) tidak reliable — lihat section 0.2 poin 3.** Yang masih bisa dipakai: Price/RP dan Price/CVDD di titik low bull dip berguna untuk **mengklasifikasikan kedalaman/konteks cycle** (dip awal-cycle vs dip late-cycle), tapi **JANGAN dipakai untuk memprediksi apakah dip akan recover atau tidak** — di dataset ini, kedalaman dip tidak berkorelasi jelas dengan kecepatan/kepastian recovery. **Confidence: Low untuk prediktif, Medium untuk deskriptif/kontekstual.**

---

## 5. INTERAKSI ANTAR METRIK

### 5.1 Tangga Struktural sebagai Confirmation Cascade

CVDD < RP < AVIV Mean < AVIV Upper berlaku 100% sepanjang waktu — baca posisi market sebagai "berapa anak tangga yang sudah ditembus":

- **Harga di atas AVIV Upper:** euphoria/cycle peak territory (section 3.1).
- **Harga di bawah AVIV Upper, di atas M0s:** mid-late bull, sehat tapi cek degradasi Price/STH across ATH.
- **Harga di antara RP dan AVIV Mean:** early-mid bull, masih sehat.
- **Harga di antara CVDD dan RP:** deep correction atau bear market.
- **Harga di bawah CVDD:** extreme capitulation (2 hari dalam 10 tahun).

### 5.2 Divergence Paling Penting

**CVDD confirm duluan, RP menyusul belakangan (section 2.8):** mekanisme — CVDD kumulatif sepanjang sejarah sehingga levelnya "tertanam" rendah, gampang ditembus balik begitu harga rally sedikit dari bottom. RP butuh waktu lebih lama karena rata-rata SEMUA koin termasuk yang baru dibeli murah ikut menarik RP turun dulu. **Kalau Price/CVDD sudah >1.0 tapi Price/RP masih <1.0, ini urutan normal recovery, bukan sinyal konflik yang mengkhawatirkan.**

**STH RP sticky di level tinggi saat low-volume drift (Jul-Sep 2024, re-verified):** STH RP stuck $61.8K-$65.9K sementara price dip ke $54.0K. STH tidak turun karena sedikit transaksi terjadi di harga rendah — ini bisa membuat Price/STH terlihat sangat bearish padahal market cuma low-activity.

**LTH RP naik sementara price turun — bear market signature, paling konsisten di seluruh dataset:**

| Bear | Price | LTH RP (anchor Cycle Peak, konsisten) |
|---|---|---|
| 2018 | -83.2% | **+716.2%** (revisi dari klaim lama +539%) |
| 2021-22 | -76.6% | +29.7% |
| 2025-26 (ongoing) | -48.6% | +34.9% |

### 5.3 Kombinasi Signal Paling Reliable per Regime

| Regime | Primary Signal | Confirmation | Confidence |
|---|---|---|---|
| Cycle Peak / Local Top | AVIV Upper sustained breach berakhir (3.1) | Price/STH degradation across ATH | TINGGI |
| Lower High Confirm | Price/STH ≤ 1.05 ATAU Price/AvivUp ≈ 1.0 | keduanya konvergen | TINGGI |
| Mid-Cycle Correction vs Bear | Price/CVDD > 2.0 + STH/LTH > 3.0 saat crash besar | — | Low (n=1) |
| Bear Bottom | STH/LTH < 1.0 | Price/CVDD < 1.05 | TINGGI |
| Pre Detection | Price/CVDD > 1.0, Price/RP < 1.0 (divergence) | — | Medium-High |
| Start of Bull Confirmed | Price > STH RP sustained, STH/LTH masih < 1.0 | — | TINGGI |

### 5.4 Divergence Paling Berbahaya Kalau Diabaikan

1. **AVIV Upper breach yang diabaikan = missed cycle top** — terutama karena lead-time-nya makin baik tiap cycle (11 hari di 2025).
2. **Persistent price below STH RP di bull market yang diabaikan = caught in bear transition.** Jul-Sep 2024 sudah menunjukkan Price/STH<0.90 berkali-kali tapi market masih rally ke ATH Des 2024 — bisa bikin complacent sampai akhirnya benar-benar tidak recover.
3. **STH/LTH > 1.0 di titik harga terendah literal (section 2.7) yang dibaca sebagai "belum bottom"** — padahal convergence <1.0 terjadi di window beberapa minggu sekitarnya, bukan harus persis di hari harga terendah.

---

## 6. FAILURE MODES

### 6.1 CVDD

Nyaris tidak pernah gagal sebagai floor (2 hari dalam 10 tahun) — tapi sample kegagalan sendiri minim, jadi belum bisa dipastikan akan tetap se-reliable ini di shock event yang lebih besar di masa depan. Murni backward-looking, tidak pernah bisa jadi leading indicator untuk top.

### 6.2 RP

Terlalu lambat untuk timing presisi (breach lag bisa 5-6 bulan dari peak). **Koreksi penting: klaim lama "selalu di atas threshold X selama Y bulan" perlu selalu di-double check harian** — section 0.2 poin 1 menemukan klaim seperti ini bisa salah kalau cuma dicek di titik awal-akhir tanpa cek tiap hari di antaranya.

### 6.3 STH RP

Paling sering memberikan false signal (60 episode breach terpisah di 10 tahun, banyak yang cuma bull dip biasa bukan bear). Misleading di low-volume drifting market (section 5.2). Definisi 155-hari arbitrary, bisa berubah oleh provider.

### 6.4 MVRV 0σ

Definisi exact tidak terverifikasi — treat pola perilakunya (bagian upper cluster, breach lebih cepat dari RP) sebagai indikatif, jangan bangun threshold presisi tanpa verifikasi independen ke ChartInspect.

### 6.5 AVIV Mean Price (sisi downside)

**Whipsaw risk nyata di sisi downside** — 3 episode terpisah breach-below sustained tepat di tengah recovery COVID 2020, persis sebelum bull run terkuat dalam sejarah BTC. **Jangan pakai AVIV Mean Price breach sebagai standalone bear-confirmation trigger** — pakai untuk klasifikasi posisi cycle (descriptive), bukan timing trigger. Ini kontras dengan AVIV Upper Price (sisi upside) yang justru nol false positive — asimetri ini harus diingat: dua sisi band yang sama punya reliability yang sangat berbeda.

### 6.6 Metrik yang Paling Sering "Disalahgunakan"

STH RP tetap paling sering disalahgunakan sebagai standalone trigger (high frequency, banyak noise). AVIV Mean Price (downside) berisiko disalahgunakan dengan cara yang sama kalau dipakai tanpa filter durasi. AVIV Upper Price (upside) dan Price/CVDD<1.05 (downside) adalah dua sinyal dengan risiko penyalahgunaan PALING RENDAH di dokumen ini — keduanya nol false positive di seluruh data historis.

---

## 7. MAPPING KE REGIME CATEGORIES

### Decision Tree

```
STEP 1: Cek posisi harga relatif ke AVIV Upper Price
├── Sustained (14d+) DI ATAS AVIV Upper → Late bull / Cycle Peak imminent territory
│   └── Breach DARI ATAS ke bawah baru terjadi → Cycle Top/Lower High warning (lead time historis 5-11 hari)
├── Di bawah AVIV Upper, di atas M0s → Mid-late bull, sehat tapi cek degradasi Price/STH across ATH
├── Di antara RP dan AVIV Mean → Early-mid bull
├── Di antara CVDD dan RP → Bear Market Decline (cek STH/LTH dan Price/CVDD untuk bedakan dari mid-cycle correction)
└── Di bawah CVDD → Extreme capitulation (sangat jarang, 2 hari/10 tahun)

STEP 2: Konfirmasi dengan STH/LTH
├── STH/LTH < 1.0 → Bear Bottom (accumulation zone, confidence TINGGI)
├── STH/LTH 1.0-1.5 → Bear bottom forming / Pre Detection (cek divergence CVDD vs RP)
├── STH/LTH 1.5-3.0 → Bear decline berlanjut, atau early-mid bull (cek arah trend harga)
└── STH/LTH > 3.0 → Extended bull, heightened risk kalau dikombinasi Price/STH degradation

STEP 3: Khusus saat crash besar (>40% dari recent high)
└── Cek Price/CVDD: > 2.0 + STH/LTH > 3.0 → kemungkinan Mid-Cycle Correction, bukan bear (n=1, hati-hati)
   < 2.0 dan STH/LTH menurun cepat → kemungkinan genuine bear transition
```

### Weight Guidelines

**Weight TINGGI:** STH/LTH untuk bear bottom call, Price/CVDD untuk extreme accumulation & pembeda mid-cycle-correction-vs-bear, AVIV Upper Price untuk cycle top call.

**Weight RENDAH:** AVIV Mean Price/M0s untuk standalone entry-exit timing tanpa filter durasi (whipsaw risk), STH RP sebagai standalone trigger tanpa kombinasi metrik lain, Price/STH sebagai pembeda kekuatan recovery bull dip (section 4.4 revisi).

### Red Flags

1. **Harga menembus CVDD dari atas** → extreme event level FTX-collapse, assess posisi segera.
2. **AVIV Upper Price breach dari atas setelah sustained period di atasnya** → cycle top warning, historis lead time 5-11 hari sebelum lower high resmi.
3. **STH/LTH compression >0.3 dalam 2 bulan** → bear market underway.
4. **LTH RP naik >15% dalam 3 bulan sementara price turun** → bear market confirmed structurally.

---

## 8. APA YANG BISA MEMBUAT THRESHOLD HISTORIS TIDAK BERLAKU

1. **CVDD tumbuh kumulatif** — Price/CVDD di cycle peak akan terus mengecil tiap cycle murni karena basis membesar, terlepas dari market dynamics. Baca relatif (vs cycle sebelumnya), bukan absolut.
2. **Definisi Active Supply / parameter dormancy bisa direvisi provider** — mempengaruhi AVIV Mean/Upper Price karena keduanya turunan dari True Market Mean yang sensitif ke definisi ini.
3. **ETF/institutional custody flows** bisa mengubah seberapa "aktif" supply terlihat on-chain, mendistorsi metrik berbasis Active Supply.
4. **Sample size kecil** untuk Mid-Cycle Correction (n=1), Start of Bull (n=2), Cycle Peak (n=3) — cycle berikutnya bisa jadi outlier yang membatalkan pola yang baru terlihat konsisten.

---

## 9. STATUS BEAR 2025-2026 (SNAPSHOT 21 JUNI 2026)

| Metrik | Nilai | Rasio thd Price |
|---|---|---|
| Price | $64,154 | — |
| RP | $53,398 | Price/RP = 1.20 |
| CVDD | $48,840 | Price/CVDD = 1.31 |
| STH | $71,483 | Price/STH = 0.90 |
| LTH | $49,690 | naik +34.9% sejak peak |
| STH/LTH | 1.44 | turun dari 3.09 di peak, **belum** <1.2 |

**Assessment:**
- **Price/CVDD = 1.31, jauh di atas threshold bear-bottom (1.05).** Capitulation genuine belum terjadi menurut metrik paling presisi di dokumen ini.
- **Price/RP = 1.20, masih di atas 1.0** — market agregat masih net profitable.
- **STH/LTH 1.44, jauh dari convergence <1.0** yang menandakan dua bear bottom sebelumnya.
- **Drawdown -48.6% dari cycle peak** — mendekati skala 2021-22 (-76%) tapi belum extreme.

**Konsisten dengan "Bear Market Decline" (kategori 7), bukan Bear Bottom Near.** Bear bottom genuine kemungkinan baru terkonfirmasi kalau Price/CVDD mendekati 1.0-1.1 DAN STH/LTH compress <1.2.

**Caveat:** cycle 2025-26 punya konteks ETF-era yang beda dari 2 siklus sebelumnya — convergence pattern historis mungkin tidak identik. Pakai sebagai default framework, update begitu data baru masuk.

---

*Dokumen ini final untuk siklus iterasi sesi ini. Update berikutnya disarankan setelah ada minimal 1 siklus bear-bottom-to-bull-confirm baru untuk menambah sample size pada rule berlabel n kecil (3.4, 4.4).*
