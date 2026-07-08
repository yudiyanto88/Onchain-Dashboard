# SOPR FAMILY KNOWLEDGE BASE
## aSOPR, LTH-SOPR, STH-SOPR — Historical Behavior, Rule Ranges & Failure Modes

**Version:** 1.4
**Data Source:** ChartInspect.com (Glassnode-sourced) 
**Data Coverage:** 2016 – Jun 2026  
**Last Updated:** 20 Jun 2026

---

## CATATAN SEBELUM MEMBACA

**Definisi singkat:**
- **aSOPR** = profit/loss ratio aggregate seluruh koin yang berpindah tangan hari itu (>1h hold, noise removed)
- **LTH-SOPR** = sama, khusus koin yang dipegang >155 hari
- **STH-SOPR** = sama, khusus koin yang dipegang <155 hari
- Nilai >1.0 = rata-rata transfer hari itu profitable. Nilai <1.0 = rata-rata rugi.

**Tentang event dalam data:** Kolom "event" di CSV menandai jendela tanggal di sekitar setiap regime transition. "First date" = tanggal pertama event window dan digunakan sebagai reference nilai SOPR saat transisi. Pre-transition = 30 hari sebelum first date. Post-transition = 30 hari setelah last date event window.

---

## 1.1 CYCLE PEAK

**Events dalam data:** Cycle Peak 2017 (Des 8–19), Cycle Peak 2021 Nov 8 (Okt 20 – Nov 9), Cycle Peak 2025 (Okt 5–7)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Cycle Peak 2017 (Des 8) | $16,349 | 1.1767 | 16.476 | 1.1354 |
| Cycle Peak 2021 (Okt 20) | $66,027 | 1.0730 | 1.898 | 1.0511 |
| Cycle Peak 2025 (Okt 5) | $123,537 | 1.0255 | 2.244 | 1.0077 |

Aggregate across all days in event windows: aSOPR avg 1.069, median 1.041 | LTH-SOPR avg 7.663, median 2.284 | STH-SOPR avg 1.038, median 1.019

**Pre-transition behavior (30 hari sebelum):**

Cycle Peak 2017 — aSOPR avg 1.126, trend RISING. STH-SOPR avg 1.085, trend RISING. LTH-SOPR avg 11.486, trend RISING. Semua tiga metrik bergerak naik bersama secara sustained. aSOPR beberapa kali tembus 1.15+ di minggu-minggu sebelum peak.

Cycle Peak 2021 — aSOPR avg 1.028, trend RISING. STH-SOPR avg 1.015, trend RISING. LTH-SOPR avg 1.987, trend RISING. Pola naik tetap ada tapi jauh lebih subdued. aSOPR praktis tidak pernah tembus 1.05 secara sustained.

Cycle Peak 2025 — aSOPR avg 1.024, trend FLAT. STH-SOPR avg 1.004, trend FLAT. LTH-SOPR avg 1.700, trend RISING. aSOPR dan STH-SOPR hampir tidak menunjukkan momentum jelas. Hanya LTH-SOPR yang masih RISING.

Trend summary 30d before: aSOPR RISING 2/3, FLAT 1/3 | LTH-SOPR RISING 3/3 | STH-SOPR RISING 2/3, FLAT 1/3

**Post-transition behavior (30 hari setelah last date):**

2017: aSOPR avg 1.047, LTH-SOPR avg 14.130, STH-SOPR avg 1.014. Nilai masih elevated karena Lower High Jan 2018 terjadi dalam periode ini.

2021: aSOPR avg 1.011, LTH-SOPR avg 2.207, STH-SOPR avg 0.997. Turun lebih cepat dari 2017. STH-SOPR sudah di bawah 1.0.

2025: aSOPR avg 1.017, LTH-SOPR avg 1.705, STH-SOPR avg 0.993. STH-SOPR juga sudah di bawah 1.0 dalam 30 hari post-peak.

**Pola konsisten lintas cycle:**

- LTH-SOPR RISING di 30 hari sebelum semua 3 cycle peaks — ini satu-satunya metrik yang 100% konsisten pre-peak
- Semua tiga metrik berada di atas 1.0 di first date setiap cycle peak — belum ada cycle peak yang terjadi saat salah satu metrik di bawah 1.0
- STH-SOPR mulai turun ke bawah 1.0 dalam 30 hari post-peak di 2021 dan 2025 (signal awal reversal)

**Perubahan dari cycle ke cycle (CRITICAL):**

- aSOPR di first date: 1.177 → 1.073 → 1.026. Compressed drastis. Fixed threshold "aSOPR > 1.10 = sell" akan miss peak 2021 dan 2025 sepenuhnya.
- LTH-SOPR di first date: 16.48 → 1.90 → 2.24. Drop 88% dari 2017 ke 2021. Ini bukan noise — ini structural shift karena semakin banyak coins yang sudah terdistribusi di harga tinggi. LTH di 2025 banyak yang beli di $30–60K, profit multipliernya jauh lebih kecil dari LTH 2017 yang beli di $1–3K.
- STH-SOPR di first date: 1.135 → 1.051 → 1.008. Semakin mendekati 1.0. Di 2025, STH-SOPR hampir tidak ada signal sama sekali di cycle peak.
- LTH-SOPR sebagai trend indicator tetap RISING (3/3), tapi absolute levelnya tidak bisa dipakai sebagai threshold.

---

## 1.2 LOCAL TOP

**Events dalam data:** Local Top Mar 2021 (2 hari), Local Top Apr 2021 ATH (3 hari), Local Top Mar 2024 ATH (4 hari), Local Top Des 2024 ATH (26 hari), Local Top Jan 2025 ATH (14 hari), Local Top Jul–Aug 2025 ATH (33 hari)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Local Top Mar 2021 | $61,186 | 1.0876 | 8.186 | 1.0684 |
| Local Top Apr 2021 (ATH) | $63,551 | 1.0794 | 8.109 | 1.0560 |
| Local Top Mar 2024 (ATH) | $71,472 | 1.0765 | 2.347 | 1.0493 |
| Local Top Des 2024 (ATH) | $98,402 | 1.1513 | 2.349 | 1.0984 |
| Local Top Jan 2025 (ATH) | $99,994 | 1.0535 | 2.758 | 1.0398 |
| Local Top Jul–Aug 2025 (ATH) | $119,057 | 1.0323 | 2.132 | 1.0135 |

Aggregate across all event window days: aSOPR avg 1.067, median 1.066 | LTH-SOPR avg 4.567, median 2.656 | STH-SOPR avg 1.035, median 1.028

**Pre-transition behavior (30 hari sebelum):**

Local Top Mar 2021 — aSOPR avg 1.084, trend DECLINING. LTH-SOPR avg 6.768, trend RISING. STH-SOPR avg 1.051, trend DECLINING. aSOPR dan STH-SOPR sudah mulai melemah sebelum top, tapi LTH-SOPR masih naik.

Local Top Apr 2021 (ATH) — aSOPR avg 1.057, trend FLAT. LTH-SOPR avg 7.336, trend RISING. STH-SOPR avg 1.025, trend DECLINING. Pola mirip Mar 2021 — LTH masih akumulasi profit tapi STH mulai menurun.

Local Top Mar 2024 (ATH) — aSOPR avg 1.067, trend RISING. LTH-SOPR avg 2.144, trend RISING. STH-SOPR avg 1.035, trend RISING. Satu-satunya local top di mana semua tiga metrik RISING sebelumnya — mencerminkan bull run yang lebih clean.

Local Top Des 2024 (ATH) — aSOPR avg 1.047, trend RISING. LTH-SOPR avg 1.900, trend RISING. STH-SOPR avg 1.022, trend RISING. Juga semua RISING tapi dengan level yang lebih rendah dari Mar 2024.

Local Top Jan 2025 (ATH) — aSOPR avg 1.040, trend DECLINING. LTH-SOPR avg 2.650, trend DECLINING. STH-SOPR avg 1.007, trend FLAT. Pre-30d sudah melemah — harga naik ke ATH tapi profitability menurun.

Local Top Jul–Aug 2025 (ATH) — aSOPR avg 1.044, trend RISING. LTH-SOPR avg 3.057, trend RISING. STH-SOPR avg 1.007, trend RISING. Secara trend masih RISING tapi absolute level sangat compressed — 33 hari local top dengan aSOPR rata-rata hanya 1.031, sangat sulit untuk di-time.

Trend summary 30d before: aSOPR RISING 3/6, DECLINING 2/6, FLAT 1/6 | LTH-SOPR RISING 5/6, DECLINING 1/6 | STH-SOPR RISING 3/6, DECLINING 2/6, FLAT 1/6

**Post-transition behavior (30 hari setelah last date):**

- Mar 2021 → Apr 2021: aSOPR avg 1.057, masih elevated karena jeda ke local top berikutnya singkat
- Apr 2021 → mid-cycle: aSOPR turun ke 1.035, STH-SOPR 1.004 — mulai mendekati zona koreksi
- Mar 2024 → Apr 2024: aSOPR avg 1.046, LTH-SOPR 2.748 — level masih terjaga
- Des 2024 → Jan 2025: aSOPR avg 1.040, LTH-SOPR 2.650 — transisi mulus ke local top berikutnya
- Jan 2025 → Feb 2025: aSOPR turun ke 1.016, STH-SOPR 0.994 — penurunan mulai visible
- Jul–Aug 2025 → Sep-Okt 2025: aSOPR avg 1.021, STH-SOPR 0.999 — melandai menuju Cycle Peak

**Pola konsisten lintas cycle:**

- LTH-SOPR RISING sebelum 5 dari 6 local tops — paling reliable sebagai pre-signal
- Semua enam local tops memiliki aSOPR di atas 1.03 di first date tanpa exception
- STH-SOPR di atas 1.00 di semua 6 events
- Post-local top, STH-SOPR yang pertama turun — biasanya dalam 14–21 hari setelah event berakhir

**Perubahan dari cycle ke cycle:**

- aSOPR di first date 2021 (avg Mar+Apr): 1.083. Di 2024–2025 (avg empat events): 1.060. Menurun tapi lebih moderat dari penurunan di cycle peaks.
- LTH-SOPR structural drop yang sama: 8.1 (2021) → 2.3–2.8 (2024–2025) → 2.1 (Jul 2025)
- Local Top Jul–Aug 2025 punya pola yang berbeda secara durasi — 33 hari dengan signal yang sangat compressed adalah yang paling sulit diidentifikasi dalam seluruh dataset.

---

## 1.3 UPPER RANGE RECOVERY

**Events dalam data:** Upper Range 2019 Failed Rally (Jun 26), Halving 2020 Context (Mei 11), Upper Range Mar 2023 (Apr 14–17), Upper Range Jun–Jul 2023 (Jun 24 – Jul 17), Halving 2024 Context (Apr 19)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Upper Range 2019 (Failed) | $12,830 | 1.1851 | 1.865 | 1.1529 |
| Halving 2020 Context | $8,641 | 0.9832 | 1.455 | 0.9697 |
| Upper Range Mar 2023 | $30,496 | 1.0288 | 1.174 | 1.0262 |
| Upper Range Jun–Jul 2023 | $30,547 | 1.0215 | 1.561 | 1.0141 |
| Halving 2024 Context | $63,851 | 1.0286 | 2.502 | 1.0034 |

Aggregate across all event window days: aSOPR avg 1.044, median 1.010 | LTH-SOPR avg 1.632, median 1.455 | STH-SOPR avg 1.029, median 1.007

**Pre-transition behavior (30 hari sebelum):**

Upper Range 2019 — aSOPR avg 1.045, trend RISING. LTH-SOPR avg 1.377, trend RISING. STH-SOPR avg 1.038, trend RISING. Semua RISING — rally ke $12.8K datang dengan momentum profitability yang kuat dari breakout bear market.

Halving 2020 Context — aSOPR avg 1.019, trend RISING. LTH-SOPR avg 1.011, trend RISING. STH-SOPR avg 1.018, trend RISING. Semua RISING tapi pada level yang moderat. LTH-SOPR baru saja kembali ke atas 1.0 setelah COVID crash.

Upper Range Mar 2023 — aSOPR avg 1.015, trend DECLINING. LTH-SOPR avg 0.998, trend DECLINING. STH-SOPR avg 1.025, trend DECLINING. Semua DECLINING — harga naik ke $30K tapi profitability tertekan karena banyak LTH yang masih rugi. LTH-SOPR belum kembali ke atas 1.0 secara sustained.

Upper Range Jun–Jul 2023 — aSOPR avg 1.005, trend FLAT. LTH-SOPR avg 1.141, trend DECLINING. STH-SOPR avg 1.002, trend FLAT. LTH-SOPR baru saja kembali ke atas 1.0 tapi masih volatile.

Halving 2024 Context — aSOPR avg 1.044, trend DECLINING. LTH-SOPR avg 2.660, trend DECLINING. STH-SOPR avg 1.007, trend DECLINING. Semua DECLINING karena terjadi setelah Local Top Mar 2024 ($73K) — ini adalah pullback zone.

Trend summary 30d before: aSOPR RISING 2/5, DECLINING 2/5, FLAT 1/5 | LTH-SOPR RISING 2/5, DECLINING 3/5 | STH-SOPR RISING 2/5, DECLINING 2/5, FLAT 1/5

**Post-transition behavior (30 hari setelah last date):**

- 2019: aSOPR 1.039, LTH-SOPR 2.172 — rally ke $13K berlanjut sebentar sebelum pullback besar
- Halving 2020: aSOPR 1.016, LTH-SOPR 1.227 — market masih konsolidasi, tapi LTH-SOPR naik (recovery berlanjut)
- Mar 2023: aSOPR 1.015, LTH-SOPR 1.257 — Bull Dip Jun 2023 terjadi setelah ini (koreksi ke $25K)
- Jun–Jul 2023: aSOPR 0.997, LTH-SOPR 1.158 — sideways kemudian turun ke Bull Dip Aug-Sep 2023
- Halving 2024: aSOPR 1.019, LTH-SOPR 2.347 — konsolidasi berlanjut sebelum rally akhir tahun

**Pola konsisten lintas cycle:**

- LTH-SOPR di sekitar 1.0 (baru kembali dari bawah 1.0 atau masih di dekat 1.0) adalah karakteristik utama Upper Range Recovery — ini berbeda dari Local Top atau Cycle Peak di mana LTH-SOPR sudah jauh di atas 1.0
- aSOPR dan STH-SOPR di atas 1.0 tapi tidak elevated — menunjukkan market yang profitable tapi belum euphoric
- Fase ini adalah transisi, bukan momentum — pre-trend tidak konsisten karena bisa datang dari rally maupun pullback

**Perubahan dari cycle ke cycle:**

- LTH-SOPR di Upper Range 2019: 1.87 (baru saja cross above 1.0 dari posisi < 0.5). Di 2023: 0.87–1.56 (masih struggle di sekitar 1.0). Di 2024: 2.50 (sudah di atas 1.0 sejak lama karena bull sudah mature).
- Ini mencerminkan context yang berbeda: di 2019, Upper Range adalah fase awal setelah bear panjang. Di 2023, Upper Range terjadi saat banyak LTH masih rugi karena ATH belum dilampaui. Di 2024, Upper Range terjadi dalam konteks bull market yang sudah berjalan.
- Upper Range 2019 menunjukkan spike besar aSOPR (1.185) yang tidak terulang di 2023 atau 2024 — ini karena supply yang tersedia untuk dijual (dan profit-taking) lebih besar di 2019 setelah akumulasi panjang selama bear.

---

## 1.4 BULL DIP

**Events dalam data:** 15 events dari 2017 sampai 2025 (Mar 2017, Jul 2017, Sep 2017, Jun 2020, Sep 2020, Jan 2021, Mar 2023, Jun 2023, Aug-Sep 2023, Jan 2024, Mei 2024, Jul 2024, Agt 2024 Yen Carry Trade, Sep 2024, Mar-Apr 2025)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Bull Dip Mar 2017 | $967 | 0.9741 | 1.771 | 0.9473 |
| Bull Dip Jul 2017 | $1,989 | 0.9423 | 3.855 | 0.9314 |
| Bull Dip Sep 2017 | $4,138 | 1.0119 | 5.165 | 0.9972 |
| Bull Dip Jun 2020 | $9,291 | 0.9837 | 0.960 | 0.9852 |
| Bull Dip Sep 2020 | $10,173 | 0.9663 | 1.153 | 0.9628 |
| Bull Dip Jan 2021 | $35,551 | 1.0888 | 4.159 | 1.0339 |
| Bull Dip Mar 2023 | $22,429 | 0.9521 | 0.632 | 1.0023 |
| Bull Dip Jun 2023 | $25,766 | 0.9883 | 1.137 | 0.9846 |
| Bull Dip Aug-Sep 2023 | $26,069 | 0.9750 | 1.022 | 0.9730 |
| Bull Dip Jan 2024 | $41,320 | 1.0415 | 1.534 | 1.0288 |
| Bull Dip Mei 2024 | $58,341 | 0.9768 | 1.825 | 0.9652 |
| Bull Dip Jul 2024 | $57,082 | 0.9962 | 1.389 | 0.9585 |
| Bull Dip Agt 2024 (Yen) | $58,174 | 0.9877 | 2.213 | 0.9731 |
| Bull Dip Sep 2024 | $56,210 | 0.9852 | 1.400 | 0.9795 |
| Bull Dip Mar–Apr 2025 | $86,294 | 1.0026 | 2.057 | 0.9941 |

Aggregate across all event window days: aSOPR avg 0.999, median 1.002 | LTH-SOPR avg 2.146, median 1.762 | STH-SOPR avg 0.987, median 0.992

**Pre-transition behavior (30 hari sebelum):**

aSOPR DECLINING sebelum 9 dari 15 events (60%) — signal yang cukup reliable. Harga dan profitability menurun menjelang dip karena sellers mulai aktif.

STH-SOPR DECLINING sebelum 10 dari 15 events (67%) — signal pre-dip yang paling konsisten. Short-term holders mulai rugi sebelum dip resmi terjadi.

LTH-SOPR tidak konsisten: RISING di 8/15, DECLINING di 6/15. Tidak reliable sebagai pre-signal untuk bull dip.

Event yang TIDAK mengikuti pola (aSOPR RISING sebelum dip): Bull Dip Jan 2021, Bull Dip Aug-Sep 2023, Bull Dip Jan 2024. Di ketiga ini, market sedang dalam momentum kuat sebelum terjadi koreksi tiba-tiba.

**Post-transition behavior (30 hari setelah last date):**

TEMUAN PALING RELIABLE: aSOPR reclaim 1.0 dalam 1–2 hari setelah event window berakhir di **semua 15 events tanpa exception**. Ini adalah konfirmasi post-facto terkuat bahwa suatu dip adalah genuine bull dip.

aSOPR post-dip 30d avg per era:
- 2017: avg 1.079 (high momentum recovery)
- 2020-21: avg 1.046 (solid recovery)
- 2023-25: avg 1.015 (muted recovery, consistent dengan market structure yang lebih mature)

LTH-SOPR > 1.0 di 30d post-dip di semua era — LTH tetap profit, konfirmasi bahwa bear belum terjadi.

**Pola konsisten lintas cycle:**

- aSOPR reclaim 1.0 dalam 1–2 hari post-event = konfirmasi bull dip terkuat dari dataset (15/15)
- STH-SOPR di bawah 1.0 di first date: terjadi di 13 dari 15 events. Dua pengecualian: Bull Dip Jan 2021 (STH 1.034) dan Bull Dip Mar 2023 (STH 1.002) — keduanya terjadi di lingkungan yang sangat bullish dengan much higher market enthusiasm.
- LTH-SOPR > 1.0 di 13 dari 15 events. Dua pengecualian: Jun 2020 (LTH 0.960) dan Mar 2023 (LTH 0.632) — keduanya terjadi saat LTH aggregate masih under water dari siklus sebelumnya.

**Perubahan dari cycle ke cycle:**

- 2017 era (3 dips): STH-SOPR bisa turun sangat dalam ke 0.895, aSOPR ke 0.912. Dip severe tapi singkat (5–9 hari).
- 2020–21 era (3 dips): STH-SOPR lebih moderat (0.960–0.985). Durasi lebih panjang (17–21 hari). Jan 2021 anomali dengan STH-SOPR 1.034 di first date — dip terjadi dalam bull yang sangat kuat.
- 2023–25 era (9 dips): STH-SOPR compressed di 0.917–1.029. Durasi bervariasi 1–35 hari. Mar–Apr 2025 adalah bull dip terpanjang dalam dataset (35 hari) — menandakan market yang lebih lelah tapi belum bear.
- LTH-SOPR di bull dips menurun signifikan antar era: 2017 avg 3.608 → 2020-21 avg 2.261 → 2023-25 avg 1.553. Ini bukan signal bahwa bull dip lebih lemah — ini structural compression yang sama seperti di cycle peaks.

---

## 1.5 MID-CYCLE CORRECTION

**Events dalam data:** Mid-Cycle Correction Start (Mei 8, 2021), Mid-Cycle Correction Bottom (Jun 22 – Jul 21, 2021)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Mid-Cycle Correction Start (Mei 8) | $59,074 | 1.0449 | 7.093 | 1.0314 |
| Mid-Cycle Correction Bottom (Jun 22) | $32,517 | 0.9839 | 2.268 | 0.9737 |

Aggregate across all days dalam kedua event windows: aSOPR avg 1.019, median 1.018 | LTH-SOPR avg 4.829, median 4.688 | STH-SOPR avg 1.004, median 1.006

**Pre-transition behavior (30 hari sebelum):**

Correction Start (Mei 2021) — aSOPR avg 1.047, trend DECLINING. LTH-SOPR avg 7.190, trend DECLINING. STH-SOPR avg 1.013, trend DECLINING. Semua tiga sudah DECLINING sebelum correction dimulai — ada advance warning tapi subtle. Market sudah kehilangan momentum profitability bahkan sebelum harga jatuh.

Correction Bottom (Jun 22) — aSOPR avg 0.994, trend FLAT. LTH-SOPR avg 3.450, trend DECLINING. STH-SOPR avg 0.978, trend RISING. STH mulai slightly recover (RISING) tapi LTH masih menurun — bottom yang belum sepenuhnya terbentuk di awal window.

Trend summary: aSOPR DECLINING 1/2, FLAT 1/2 | LTH-SOPR DECLINING 2/2 | STH-SOPR DECLINING 1/2, RISING 1/2

**Post-transition behavior (30 hari setelah last date):**

Post-Correction Start (30d after Mei 8): aSOPR avg 0.991, LTH-SOPR avg 4.408, STH-SOPR avg 0.972. Market sudah dalam correction mode — aSOPR di bawah 1.0, STH-SOPR turun ke 0.972.

Post-Correction Bottom (30d after Jul 21): aSOPR avg 1.041, LTH-SOPR avg 2.304, STH-SOPR avg 1.015. Recovery dimulai — aSOPR kembali ke atas 1.0 dan STH-SOPR mengikuti. Harga naik dari ~$30K kembali ke $40K+ dalam periode ini.

**Pola konsisten:**

- LTH-SOPR > 1.0 sepanjang seluruh periode mid-cycle correction (minimum 1.496) — ini pembeda utama dari bear market genuine. Long-term holders tidak pernah rugi meskipun harga turun 50%.
- STH-SOPR turun sustained ke bawah 0.97 selama period bottom — lebih dalam dan lebih lama dari bull dip biasa. Di bottom window (30 hari), STH-SOPR minimum 0.859.
- aSOPR turun ke 0.867 saat bottom — lebih dalam dari sebagian besar bull dips tapi masih lebih tinggi dari bear bottom genuine.
- Duration bottom: 30 hari. Vs bull dip yang biasanya 5–35 hari dengan STH di bawah 1.0 hanya sebagian hari.

**Perubahan dari cycle ke cycle:**

Hanya satu mid-cycle correction dalam dataset (2021). Data terbatas untuk menyimpulkan pola perubahan antar cycle. Perlu minimal dua datapoints untuk generalisasi. ⚠️ *Belum diverifikasi apakah cycle 2024-2025 memiliki mid-cycle correction yang setara.*

---

## 1.6 LOWER HIGH CONFIRM TOP CYCLE

**Events dalam data:** Lower High 2018 (Jan 1–8), Lower High 2021 (Nov 30 – Des 2), Lower High 2025 (Okt 26–27), Lower High 2025 Conformation (Okt 28)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Lower High 2018 (Jan 1) | $13,783 | 1.0044 | 14.889 | 0.9885 |
| Lower High 2021 (Nov 30) | $56,995 | 1.0051 | 1.585 | 0.9966 |
| Lower High 2025 (Okt 26) | $114,584 | 1.0281 | 2.484 | 1.0075 |
| Lower High 2025 Conformation (Okt 28) | $112,964 | 1.0469 | 1.751 | 0.9990 |

Aggregate across all event window days: aSOPR avg 1.039, median 1.037 | LTH-SOPR avg 6.035, median 2.312 | STH-SOPR avg 1.011, median 1.002

**Pre-transition behavior (30 hari sebelum):**

Lower High 2018 — aSOPR avg 1.114, trend DECLINING. LTH-SOPR avg 16.324, trend RISING. STH-SOPR avg 1.074, trend DECLINING. aSOPR dan STH-SOPR DECLINING meskipun harga masih di area $15–17K. LTH-SOPR masih RISING karena coins 2017 yang masih sangat profitable.

Lower High 2021 — aSOPR avg 1.029, trend DECLINING. LTH-SOPR avg 2.529, trend DECLINING. STH-SOPR avg 1.009, trend DECLINING. Semua tiga DECLINING. Market kehilangan momentum profitability di semua cohort.

Lower High 2025 — aSOPR avg 1.024, trend DECLINING. LTH-SOPR avg 1.752, trend DECLINING. STH-SOPR avg 1.000, trend DECLINING. Semua tiga DECLINING. STH-SOPR hampir tepat di 1.0 (equilibrium) menjelang lower high.

Lower High 2025 Conformation — aSOPR avg 1.025, trend DECLINING. LTH-SOPR avg 1.822, trend DECLINING. STH-SOPR avg 1.000, trend DECLINING. Sama dengan event sebelumnya — ini adalah konfirmasi 2 hari kemudian.

Trend summary 30d before: **aSOPR DECLINING 4/4 (100%)** | LTH-SOPR DECLINING 3/4, RISING 1/4 | **STH-SOPR DECLINING 4/4 (100%)**

**Post-transition behavior (30 hari setelah last date):**

- Post-LH 2018: aSOPR 0.987, LTH-SOPR 7.987, STH-SOPR 0.960. aSOPR sudah di bawah 1.0, STH-SOPR turun ke 0.96 — bear market mulai terbentuk.
- Post-LH 2021: aSOPR 0.999, LTH-SOPR 1.725, STH-SOPR 0.989. Masih dekat 1.0 tapi arah turun sudah jelas.
- Post-LH 2025: aSOPR 1.014, LTH-SOPR 1.487, STH-SOPR 0.985. Sedikit di atas 1.0 untuk aSOPR tapi STH-SOPR sudah melemah.

**Pola konsisten lintas cycle:**

- aSOPR dan STH-SOPR DECLINING 4/4 (100%) sebelum lower high — ini signal paling konsisten dalam seluruh dataset. Divergence antara harga yang naik ke area ATH vs profitability yang menurun adalah red flag terkuat yang bisa dideteksi dari SOPR.
- aSOPR di first date always > 1.0 di semua 4 events — belum ada lower high yang terjadi dengan aSOPR di bawah 1.0.
- STH-SOPR di first date selalu di sekitar 1.0 (0.988–1.007 untuk 3 dari 4 events) — STH hampir tidak profit, distribusi terjadi dari LTH dan medium-term holders.

**Perubahan dari cycle ke cycle:**

- aSOPR saat lower high: 1.004 (2018), 1.005 (2021), 1.028–1.047 (2025). Sedikit naik di 2025 tapi secara level tetap dalam range 1.0–1.05.
- LTH-SOPR saat lower high: 14.889 (2018), 1.585 (2021), 2.484 (2025). Structural compression yang sangat jelas — sama dengan pola di cycle peaks. LTH-SOPR di lower high 2021 dan 2025 jauh lebih rendah.
- Di 2025, ada dua event "Lower High" yang berdekatan (Okt 26–27 dan Okt 28) — ini menunjukkan pasar yang mencoba menembus resistance tapi gagal dua kali berturut-turut. SOPR readings hampir identik di keduanya.

---

## 1.7 BEAR BOTTOM NEAR

**Events dalam data:** Bear Bottom 2018 Tier 1 (Des 11–17), Bear Bottom Window End 2019 (Jan 30 – Feb 6), COVID Bottom Flash Crash (Mar 13–17, 2020), Bear Bottom FTX Collapse (Nov 8, 2022), Bear Bottom Actual Price Low (Nov 21, 2022), Bear Bottom Final Low (Des 19, 2022)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Bear Bottom 2018 Tier 1 (Des 11) | $3,441 | 0.8211 | 0.400 | 0.9316 |
| Bear Bottom Window End (Jan 30) | $3,510 | 0.9525 | 0.630 | 0.9838 |
| COVID Bottom Flash Crash (Mar 13) | $5,632 | 0.9065 | 0.608 | 0.9274 |
| Bear Bottom FTX Collapse (Nov 8) | $18,550 | 0.9381 | 0.522 | 0.9544 |
| Bear Bottom Actual Price Low (Nov 21) | $15,774 | 0.9150 | 0.423 | 0.9636 |
| Bear Bottom Final Low (Des 19) | $16,442 | 0.9250 | 0.507 | 0.9375 |

Aggregate across all event window days: aSOPR min 0.821, max 0.980, avg 0.931, median 0.929 | LTH-SOPR min 0.343, max 0.740, avg 0.515, median 0.512 | STH-SOPR min 0.912, max 0.990, avg 0.955, median 0.954

**Pre-transition behavior (30 hari sebelum):**

Pre-trend tidak konsisten — tidak ada single pattern yang reliable. Beberapa events preceded by rally (bear market relief bounce), beberapa preceded by sustained decline.

Bear Bottom 2018 Tier 1 — aSOPR RISING (ada relief bounce sebelumnya dari $6K). LTH-SOPR RISING tapi masih sangat rendah (0.852). STH-SOPR DECLINING (sellers masih aktif).

Bear Bottom Window End 2019 — aSOPR RISING. LTH-SOPR RISING. Ini adalah after-bottom consolidation period, pre-30d sudah termasuk bottom Des 2018.

COVID Flash Crash — aSOPR DECLINING, LTH-SOPR DECLINING. Ini adalah event unik — crash cepat dari $9K ke $4.8K dalam hari, tanpa periode bear market yang panjang sebelumnya.

FTX Collapse — aSOPR RISING (recovery dari posisi lebih rendah). LTH-SOPR RISING. Crash FTX terjadi dari harga $20K yang sudah turun dari $69K — ada relief rally sebelum FTX collapse.

Bear Bottom Actual Price Low — aSOPR DECLINING. LTH-SOPR DECLINING. Harga terus turun dari $18.5K ke $15.7K setelah FTX.

Bear Bottom Final Low — aSOPR FLAT. LTH-SOPR DECLINING. Satu bulan konsolidasi yang melemah.

Trend summary 30d before: aSOPR RISING 3/6, DECLINING 2/6, FLAT 1/6 | LTH-SOPR RISING 3/6, DECLINING 3/6 | STH-SOPR DECLINING 4/6, RISING 2/6

**Post-transition behavior (30 hari setelah last date):**

| Event | aSOPR 30d avg | LTH-SOPR 30d avg | STH-SOPR 30d avg |
|-------|--------------|-----------------|-----------------|
| Bear Bottom 2018 Tier 1 | 0.958 | 0.630 | 0.984 |
| Bear Bottom Window End 2019 | 0.980 | 0.600 | 0.999 |
| COVID Flash Crash | 0.989 | 0.859 | 0.994 |
| Bear Bottom FTX Collapse | 0.941 | 0.525 | 0.984 |
| Bear Bottom Actual Price Low | 0.966 | 0.555 | 0.993 |
| Bear Bottom Final Low | 0.979 | 0.584 | 1.007 |

Post-bottom: aSOPR perlahan recover tapi masih di bawah 1.0 di semua events 30d setelahnya — recovery dari bear bottom berlangsung lambat. LTH-SOPR juga masih sangat rendah. STH-SOPR yang paling cepat mendekati 1.0 (Final Low 2022 sudah di 1.007).

**Pola konsisten lintas cycle:**

- LTH-SOPR < 0.65 di semua 6 events tanpa exception — ini threshold paling reliable untuk "bear bottom region"
- aSOPR < 0.95 di 5 dari 6 events (exception: Bear Bottom Window End di 0.953 — ini adalah post-bottom consolidation, bukan aktual bottom)
- STH-SOPR < 0.99 di semua 6 events
- Pre-trend tidak reliable — tidak bisa memprediksi bear bottom dari SOPR movement sebelumnya
- Post-bottom recovery: STH-SOPR recover lebih cepat dari LTH-SOPR. Ketika STH-SOPR reclaim 1.0, itu sinyal Pre Detection mulai

**Perubahan dari cycle ke cycle:**

- LTH-SOPR minimum per cycle: 2018 cycle bottom (Des 2018) = 0.272. 2022 cycle bottom (Nov 2022) = 0.343. Keduanya jauh di bawah 0.50 — deep capitulation dari long-term holders.
- COVID crash: LTH-SOPR 0.608–0.716 — lebih tinggi dari bear market bottoms karena ini flash crash, bukan structural bear. LTH-SOPR tidak turun se-dalam karena waktunya singkat (5 hari event, total < 2 bulan untuk LTH-SOPR di bawah 1.0).
- 2026 current: LTH-SOPR minimum so far 0.647 (Mar 11, 2026). Lebih dalam dari COVID tapi belum mencapai 2018 atau 2022 levels. Apakah ini bear yang lebih ringan atau capitulation masih akan datang — belum bisa ditentukan dari data saat ini. ⚠️ *Membutuhkan monitoring ongoing.*

---

## 1.8 PRE DETECTION START OF BULL MARKET

**Events dalam data:** Pre Detection 2019 Ref (Feb 22), Pre Detection 2019 (Mar 21–26), Pre Detection 2023 (Jan 10–12)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Pre Detection 2019 Ref (Feb 22) | $3,943 | 0.9927 | 0.609 | 1.0041 |
| Pre Detection 2019 (Mar 21) | $4,039 | 0.9840 | 0.676 | 1.0014 |
| Pre Detection 2023 (Jan 10) | $17,444 | 0.9734 | 0.526 | 1.0092 |

Aggregate across all event window days: aSOPR avg 0.987, median 0.982 | LTH-SOPR avg 0.584, median 0.553 | STH-SOPR avg 1.007, median 1.004

**Pre-transition behavior (30 hari sebelum):**

Pre Detection 2019 Ref — aSOPR avg 0.969, trend RISING. LTH-SOPR avg 0.535, trend RISING. STH-SOPR avg 0.990, trend RISING. Semua dalam recovery mode — aSOPR naik dari level yang lebih rendah.

Pre Detection 2019 (Mar 21) — aSOPR avg 0.987, trend RISING. LTH-SOPR avg 0.632, trend DECLINING. STH-SOPR avg 1.001, trend FLAT. aSOPR RISING tapi LTH-SOPR masih DECLINING — LTH masih rugi tapi tekanannya mulai berkurang.

Pre Detection 2023 — aSOPR avg 0.969, trend DECLINING. LTH-SOPR avg 0.560, trend RISING. STH-SOPR avg 0.995, trend RISING. Berbeda dari 2019 — di sini aSOPR masih DECLINING tapi STH-SOPR mulai RISING dengan LTH juga starting to recover.

Trend summary 30d before: aSOPR RISING 2/3, DECLINING 1/3 | LTH-SOPR RISING 2/3, DECLINING 1/3 | STH-SOPR RISING 2/3, FLAT 1/3

**Post-transition behavior (30 hari setelah last date):**

- Post-PreDetection 2019 Ref: aSOPR 0.987, LTH-SOPR 0.595, STH-SOPR 1.001 — stabil, pasar mengkonsolidasi
- Post-PreDetection 2019 Mar: aSOPR 1.010, LTH-SOPR 0.776, STH-SOPR 1.022 — aSOPR mulai sustained di atas 1.0, ini lead ke Start of Bull
- Post-PreDetection 2023: aSOPR 1.010, LTH-SOPR 0.716, STH-SOPR 1.023 — sama, aSOPR naik ke atas 1.0

**Pola konsisten lintas cycle (PALING KRITIS):**

- **STH-SOPR > 1.0 di first date semua 3 events tanpa exception** (1.004, 1.001, 1.009) sementara aSOPR dan LTH-SOPR masih di bawah 1.0. Ini adalah divergence signature Pre Detection: buyers baru (STH) sudah mulai profit, tapi market aggregate dan long-term holders masih rugi.
- aSOPR masih di bawah 1.0 di semua 3 events (0.993, 0.984, 0.973) — market belum profitable secara aggregate
- LTH-SOPR masih jauh di bawah 1.0 (0.609, 0.676, 0.526) — LTH masih dalam posisi rugi

**Perubahan dari cycle ke cycle:**

- STH-SOPR divergence di atas 1.0 tetap konsisten di 2019 dan 2023 — ini signal yang preserved across cycles
- LTH-SOPR level di Pre Detection: 0.609-0.676 (2019) vs 0.526 (2023). 2023 lebih dalam karena banyak LTH yang beli di area $40-60K di 2021 masih sangat under water.
- aSOPR recovery rate lebih lambat di 2023 dibanding 2019 — mencerminkan market yang lebih besar dan lebih berat untuk bergerak

---

## 1.9 START OF BULL MARKET CONFIRMATION

**Events dalam data:** Start of Bull 2019 (Apr 25), Start of Bull 2023 (Feb 10–12)

**Nilai di first date transition:**

| Event | Price | aSOPR | LTH-SOPR | STH-SOPR |
|-------|-------|-------|----------|----------|
| Start of Bull 2019 (Apr 25) | $5,249 | 0.9869 | 0.674 | 0.9945 |
| Start of Bull 2023 (Feb 10) | $21,632 | 0.9866 | 0.890 | 0.9905 |

Aggregate across all event window days: aSOPR avg 0.990, median 0.990 | LTH-SOPR avg 0.719, median 0.722 | STH-SOPR avg 0.997, median 0.998

**Pre-transition behavior (30 hari sebelum):**

Start of Bull 2019 — aSOPR avg 1.010, trend FLAT (dari level Pre Detection yang elevated). LTH-SOPR avg 0.776, trend RISING. STH-SOPR avg 1.022, trend DECLINING. Pre-30d mencakup Pre Detection period — dari sana aSOPR 1.0+ tapi saat event day sendiri turun ke 0.987.

Start of Bull 2023 — aSOPR avg 1.010, trend DECLINING. LTH-SOPR avg 0.700, trend RISING. STH-SOPR avg 1.025, trend DECLINING. Sama — pre-30d elevated dari Pre Detection, tapi event day sendiri di bawah 1.0.

Trend summary 30d before: aSOPR FLAT 1/2, DECLINING 1/2 | **LTH-SOPR RISING 2/2** | STH-SOPR DECLINING 2/2

**Post-transition behavior (30 hari setelah last date):**

Start of Bull 2019: aSOPR 1.034, LTH-SOPR 1.023, STH-SOPR 1.040. aSOPR mulai sustained di atas 1.0. LTH-SOPR naik ke 1.023 — hampir kembali ke atas 1.0 dan akan melewati 1.0 dalam beberapa minggu setelah ini.

Start of Bull 2023: aSOPR 0.995, LTH-SOPR 0.799, STH-SOPR 1.008. Lebih lambat — aSOPR masih fluktuatif di sekitar 1.0. LTH-SOPR masih 0.8. Bull 2023 butuh waktu lebih lama untuk establish.

**Pola konsisten:**

- aSOPR di first date kedua events identik hampir persis: 0.9869 dan 0.9866 — keduanya tepat di bawah 1.0. Ini counter-intuitive: "Start of Bull" terjadi saat aSOPR masih di bawah 1.0.
- LTH-SOPR RISING sebelum kedua events (2/2) — satu-satunya pre-signal yang konsisten. LTH mulai recover dari bottom, meskipun belum di atas 1.0.
- STH-SOPR tepat di sekitar 0.99–1.00 — hampir equilibrium tapi bukan di atas 1.0 seperti di Pre Detection.
- Interpretasi: Start of Bull adalah ketika price sudah establish above certain level dan momentum mulai, tapi hari-hari spesifik ini bisa terjadi di dalam price consolidation atau pullback kecil yang membuat SOPR momentarily turun.

**Perubahan dari cycle ke cycle:**

- 2019: LTH-SOPR di event day 0.674, di 30d post sudah 1.023 — recovery cepat. Naik ke Upper Range $12K+ dalam 2 bulan.
- 2023: LTH-SOPR di event day 0.890, di 30d post masih 0.799 — recovery lebih lambat. Bull 2023 berlangsung gradual, bukan explosive.
- Perbedaan ini mencerminkan structural context: di 2019, bear sudah sangat dalam dan buyback kuat terjadi saat harga $3–5K. Di 2023, banyak LTH yang masih under water dari level $40-60K sehingga LTH-SOPR butuh lebih lama untuk recover ke atas 1.0.

---

## LAMPIRAN A: FLAG UNTUK VERIFIKASI (Historical Behavior)

**⚠️ Data yang membutuhkan cross-check di ChartInspect:**

1. **LTH-SOPR minimum values**: 0.272 (2019) dan 0.343 (2022) adalah values kritis untuk calibrating Bear Bottom Near. Perlu cross-check dengan ChartInspect karena nilai ini highly data-source dependent.

2. **Current bear market (2026)**: Data ends Jun 16, 2026. LTH-SOPR minimum so far: 0.647. Status ongoing, membutuhkan monitoring mingguan.

3. **Pre-2016 data**: Dataset tidak mencakup cycle 2013 dan 2015 bear. SOPR family behavior di era tersebut mungkin berbeda dan bisa memberikan additional pattern insight.

---

## 2. RULE RANGES — SIGNAL THRESHOLDS

### 2.1 aSOPR: SELL ZONE (aSOPR 7d > 1.05)

Threshold: aSOPR 7-hari MA > 1.05 sebagai tanda profitability elevated — potential sell alert atau take-profit zone.

**Statistik dari data (2016–2026):**
- Total episodes triggered: 30 episodes, 519 hari
- True sell signals (price 30d after event end lebih rendah dari peak): 23/30 (77%)
- False sell signals (price 30d setelah masih naik): 7/30 (23%)

**False signals yang signifikan:**
- Mei 2017, Okt–Des 2020, Jul–Agt 2021 — semua terjadi di tengah bull run yang belum selesai. Sell di sini berarti miss 30–130% upside berikutnya.
- Okt 2024 (triggered saat $69K, harga naik ke $106K sebulan kemudian) — bull run 2024 belum selesai.

**True signals yang benar:**
- Des 2017 episode (aSOPR 1.47, peak $19.5K): 30d setelah peak turun -45.6% — paling reliable
- Mar 2024 (aSOPR 1.36, peak $73K): 30d setelah -9.8% — moderate
- Jul 2025 (aSOPR 1.31, peak $119.8K): 30d setelah -2.0% — lemah tapi masih directionally benar

**Cost of being wrong:** Kalau exit saat aSOPR > 1.05 di false signal episode, opportunity cost rata-rata +30–130% yang di-miss. Di Oct 2024 ($69K), miss run ke $106K (+54%) dalam sebulan.

**Reliability per cycle:**
- 2017: Sangat reliable. aSOPR mencapai 1.20–1.47 dan berkorelasi kuat dengan tops.
- 2020–2021: Moderate. Trigger berkali-kali selama bull. False signals di atas 1.05 terjadi di Okt-Des 2020 dan Feb-Mar 2021 sebelum actual peak Nov 2021.
- 2024–2025: Lemah untuk timing. aSOPR > 1.05 trigger di Mar 2024 (sebelum $73K ATH yang kemudian koreksi) dan Nov 2024 — tapi interval antara trigger dan actual top semakin pendek, membuat timing lebih sulit.

**Kesimpulan:** aSOPR > 1.05 memberikan signal "profitability elevated" yang tepat 77% kali mengindikasikan harga lebih rendah 30 hari kemudian, tapi threshold ini terlalu sering trigger di mid-bull run. Bukan timing signal untuk cycle peak.

---

### 2.2 STH-SOPR: SELL ZONE (STH-SOPR 7d > 1.03)

Threshold: STH-SOPR 7-hari MA > 1.03 sebagai tanda short-term holders taking aggressive profits.

**Statistik dari data:**
- Total episodes: 32 episodes, 425 hari
- True sell signals: 22/32 (69%)
- False sell signals: 10/32 (31%)

**Episodes terkuat (true signals):**
- Des 2017–Jan 2018: STH max 1.329, 30d setelah -27.2 dan -37.4%. Paling reliable.
- Feb–Mar 2021: STH max 1.141/1.100, 30d setelah -5.6% dan -5.4%
- Feb–Mar 2024: STH max 1.196, 30d setelah -7.7%. Moderate signal yang benar.
- Nov–Des 2024: STH max 1.098, 30d setelah -0.3 dan -7.2%. Masih directionally correct.

**False signals:**
- Nov 2020 (STH 1.100, peak $19.1K): 30d setelah naik +7.4% — mid-bull, belum selesai
- Jun 2019 (STH 1.153, peak $12.8K): 30d setelah -17.5% — ini true, tapi bukan cycle top
- Okt 2020 (STH 1.031, peak $13.6K): 30d setelah +17.6% — mid-bull false signal

**Structural change:** STH-SOPR peaks semakin terkompresi. Di 2017 bisa mencapai 1.33 di cycle peak; di 2024 puncaknya hanya 1.20 (Mar 2024 ATH) dan 1.10 (Nov 2024 ATH). Threshold 1.03 masih relevan tapi signal-nya semakin lebih sering dan kurang exclusive.

**Cost of being wrong:** Miss 17–54% upside di false signal episodes.

---

### 2.3 aSOPR: BUY ZONE (aSOPR 7d < 0.97)

Threshold: aSOPR 7-hari MA < 0.97 sebagai tanda market-wide capitulation.

**Statistik dari data:**
- Total episodes: 22 episodes, 252 hari
- Konteks BEAR MARKET GENUINE (LTH-SOPR juga < 1.0): 2018 dan 2022 long episodes
- FALSE SIGNALS (LTH-SOPR masih > 1.0 = mid-cycle / bull dip):
  - Mei 2021: aSOPR 0.953, LTH-SOPR 3.0–4.3. Harga $34–37K, recovery ke $67K.
  - Jun 2021: aSOPR 0.867 (1 hari), LTH-SOPR 2.7. Harga $31.6K, recovery ke $67K.
  - Mar 2023: aSOPR 0.866, LTH-SOPR 0.632 — ini ambiguous karena LTH juga < 1.0, tapi harga justru naik dari $20K ke $30K dalam 30 hari (+36.6%)
  - 2026 episodes: aSOPR 0.90–0.97 — konteks bear market ongoing

**30d return setelah episode aSOPR < 0.97:**
- Setelah extended 2018-2019 episode: +20.2%
- Setelah COVID crash 2020: +41.3%
- Setelah Jun 2021 dip (false bear): +5.9% dalam 30d, +130% dalam 5 bulan
- Setelah FTX 2022 episode: +7.1%
- Setelah Final Low Des 2022: +30.5%

**Pembeda krusial:** Gunakan LTH-SOPR untuk konteks. aSOPR < 0.97 dengan LTH-SOPR > 1.5 = kemungkinan besar mid-cycle atau bull dip besar. aSOPR < 0.97 dengan LTH-SOPR < 1.0 = genuine bear capitulation territory.

---

### 2.4 LTH-SOPR: BEAR CONFIRMATION (Sustained < 1.0)

Threshold: LTH-SOPR < 1.0 secara sustained, dibedakan berdasarkan durasi.

**Episodes sustained dari data:**

| Episode | Durasi | Min LTH | Min Price | Konteks |
|---------|--------|---------|-----------|---------|
| Jun 2018 – Mei 2019 | 291 hari | 0.272 | $3,281 | 2018 bear market full cycle |
| Feb 2020 – Mei 2020 | 46 hari | 0.558 | $4,837 | COVID flash crash |
| Apr 2022 – Apr 2023 | 318 hari | 0.346 | $15,774 | 2022 bear market full cycle |
| Feb 2026 – ongoing | 97+ hari | 0.647 | $60,811 | Current bear market |

**Short episodes (< 20 hari) — banyak false signals:**
- 37 episodes singkat (1–10 hari) yang tersebar di 2016, 2019-2020, 2023 — kesemuanya tidak mengindikasikan bear market yang sustained. Banyak terjadi selama 2023 bull run ($26–30K range) ketika LTH yang beli di 2021 masih under water.

**Rule yang reliable:**
- Episode < 7 hari: high probability false signal, abaikan atau gunakan sebagai minor caution
- Episode 7–29 hari: moderate concern, perlu konfirmasi dari aSOPR dan STH-SOPR
- Episode ≥ 30 hari: dari data, selalu associated dengan genuine bear market atau extended distress (COVID)
- Episode ≥ 100 hari: established bear market tanpa pengecualian dalam dataset

**Hit rate LTH episode ≥ 30 hari sebagai "genuine bear":** 4/4 episodes (100%). Tidak ada false positive untuk sustained episode.

**Cost of being wrong kalau ignore:** Sebaliknya — kalau ignore bahwa LTH-SOPR sudah di bawah 1.0 selama 30+ hari, kamu masih hold di bear market dan expose diri ke potensi drawdown lebih dalam.

---

### 2.5 STH-SOPR Reclaim 1.0 Setelah Extended Period Below

Ini bukan threshold statis, tapi event-driven signal.

**Pattern dari data:** Setelah period panjang STH-SOPR < 1.0 (>14 hari), sustained reclaim ke atas 1.0 untuk 5+ hari berturut-turut adalah salah satu signal paling reliable untuk Pre Detection / Start of Bull.

**Dari Pre Detection events:** STH-SOPR > 1.0 di semua 3 events (1.004, 1.001, 1.009) sementara LTH dan aSOPR masih di bawah 1.0. Divergence ini — STH kembali profit dulu sebelum yang lain — adalah karakteristik structural dari transisi bear-ke-bull.

---

## 3. INTERAKSI ANTAR METRIK SOPR FAMILY

### 3.1 Ketika Semua Sejalan — High Confidence Zone

**Semua tiga > 1.0 dan naik (RISING trend):**
Terjadi 49.1% dari seluruh hari dalam dataset. Ini adalah kondisi bull market "healthy" — market aggregate profitable, LTH distribusi dengan profit, STH juga profit. High confidence: pasar dalam mode bullish. Tapi bukan timing signal spesifik karena berlangsung lama.

**Semua tiga < 1.0 secara sustained (> 14 hari berturut-turut):**
Dari data, episode panjang (>14 hari) terjadi di: 2018 bear market (143 hari Jun 2018 – Nov 2018 terus berlanjut), 2019 (partial), 2022 (74 hari Apr-Agt, kemudian 113 hari Agt 2022 – Jan 2023), 2026 (41 hari Feb-Apr, lalu dilanjut). Ini adalah kondisi maximum distress. Setiap kali ini terjadi dalam dataset, harga akhirnya berbalik ke atas — tapi timing bottomnya tidak bisa diprediksi dari SOPR saja.

**Semua tiga DECLINING trend sebelum suatu price level:**
Terjadi konsisten sebelum Lower High Confirm (4/4 untuk aSOPR dan STH-SOPR). Ini adalah red flag terkuat — harga mungkin masih tinggi tapi semua profitability metrics melemah.

### 3.2 Divergence LTH > 1.0 + STH < 1.0 — Bull Dip Signature

Terjadi 1.102 hari dalam dataset. Ini adalah "classic bull dip" combo: long-term holders masih sangat profit (tidak panik), short-term holders selling at loss (panik jangka pendek).

**Reliability:** Meskipun 1.102 hari tergolong banyak, hanya 107 hari (9.7%) yang benar-benar dalam labeled bull dip events. Sisanya adalah periode sekitar bull dips, konsolidasi normal, dan transisi antar regime. Ini berarti combo ini perlu dikombinasikan dengan konteks price action dan tren untuk actionable.

**Signal lebih kuat jika:**
- LTH-SOPR > 1.5 (bukan hanya di atas 1.0)
- aSOPR antara 0.97–1.02 (bukan < 0.95 yang mengindikasikan lebih dalam)
- Recovery aSOPR kembali ke atas 1.0 dalam 1–3 hari

### 3.3 Divergence STH > 1.0 + LTH < 1.0 — Pre Detection / Transisi

Terjadi 301 hari. Ini adalah signature transisi dari bear-ke-bull: buyers baru (STH) sudah profit dari bottom, tapi long-term holders yang masuk di harga lebih tinggi masih rugi.

**Ini adalah LAGGING signal untuk Bear Bottom dan LEADING signal untuk Pre Detection.** Kapan STH mulai > 1.0 sementara LTH masih < 1.0, itu artinya harga sudah naik cukup untuk winners kecil tapi belum cukup untuk winners besar.

**Penting:** Dari 301 hari ini, hanya 7 hari overlap dengan labeled Pre Detection events dan 2 hari dengan Start of Bull. Sisanya tersebar di seluruh recovery period. Ini bukan karena signal salah — ini karena Pre Detection events hanya berlangsung beberapa hari, sedangkan kondisi ini bisa berlangsung berminggu-minggu.

### 3.4 LTH Declining Sementara Harga Rising — Distribution Warning

Terjadi 286 hari (price +5%+ in 7d while LTH-SOPR fell 5%+). Ini adalah divergence yang paling sering tidak diperhatikan. Harga naik tapi LTH sudah tidak ikut naik profitnya — bisa berarti LTH distributing ke buyers baru.

**Episode signifikan yang perlu diperhatikan:**
- Nov 2017 – Des 2017: terjadi sebelum Cycle Peak 2017. Harga masih naik ke $19.5K tapi LTH profit mulai compressed.
- Mar 2021 – Apr 2021: terjadi sebelum Local Top Mar dan Apr 2021.
- Okt–Nov 2021: terjadi sebelum dan setelah Cycle Peak 2021.
- Feb–Mar 2024 dan Okt 2024: muncul di sekitar local tops 2024.

**Catatan:** Signal ini terlalu sering muncul (286 hari) untuk jadi standalone sell trigger. Gunakan sebagai early warning bahwa distribusi mulai terjadi, bukan sebagai action signal.

### 3.5 Kombinasi Paling Reliable per Action

**Untuk konfirmasi Bear Market:**
LTH-SOPR < 1.0 sustained + aSOPR < 0.97 recurring → Bear confirmed. Hit rate dari data: semua long bear episodes memenuhi kedua kondisi ini.

**Untuk Pre Detection / Early Bull signal:**
STH-SOPR > 1.0 + aSOPR antara 0.97–1.01 + LTH-SOPR masih < 1.0 tapi rising trend → Pre Detection zone. Ini adalah setup yang paling actionable dari data.

**Untuk Bull Dip confirmation:**
LTH-SOPR > 1.5 + aSOPR bounce kembali ke atas 1.0 dalam 1–2 hari + STH-SOPR approaching 1.0 from below → Bull dip confirmed. aSOPR reclaim 1.0 dalam 1–2 hari post-event terjadi di semua 15 bull dip events.

**Untuk Top Warning:**
aSOPR dan STH-SOPR DECLINING trend selama 14+ hari meskipun harga sideways atau naik → distribution pattern. Terjadi di 4/4 Lower High events dan di banyak local tops.

---

## 4. FAILURE MODES — BAGIAN TERPENTING

### 4.1 aSOPR Failure Modes

**FAILURE 1: Fixed upper threshold tidak berlaku post-2017 (PALING KRITIS)**

aSOPR cycle peak values:
- 2017: 1.177 di first day, max event window 1.195
- 2021: 1.073 di first day, max 1.130 dalam window
- 2025: 1.025 di first day, max 1.075 dalam window

Threshold "aSOPR > 1.10 untuk jual" atau "aSOPR > 1.15 untuk reduce position" tidak pernah terpenuhi di cycle peak 2021 dan 2025. Seseorang yang menggunakan rule ini dari 2017 akan hold sepanjang entire cycle 2021 dan 2025 tanpa pernah mendapat sell signal.

**FAILURE 2: Mid-cycle false capitulation signals (BERBAHAYA untuk loan/leverage)**

Mei 2021: aSOPR turun ke 0.953 saat harga $34.7K. LTH-SOPR masih 3.8–4.3. Kalau pakai aSOPR < 0.97 sebagai "capitulation = buy" di sini tanpa konfirmasi LTH, hasilnya adalah buy yang kemudian turun lagi ke $29.8K (further drawdown -14%) sebelum recovery ke $67K.

Jun 2021: aSOPR turun ke 0.867 satu hari saat harga $31.6K. Terlihat seperti deep capitulation. LTH-SOPR: 2.7. Ini adalah classic trap — signal terlihat extreme tapi konteks LTH menunjukkan ini masih mid-cycle.

**Perbedaan yang diselamatkan oleh LTH-SOPR:**
- 2021 mid-cycle: LTH-SOPR 2.7–4.3 (jauh di atas 1.0) → bukan genuine bear
- 2022 bear: LTH-SOPR 0.35–0.65 (jauh di bawah 1.0) → genuine bear

**FAILURE 3: Tidak reliable sebagai standalone signal di ambiguous price zones**

aSOPR antara 0.97–1.03 terjadi 54% dari seluruh hari dalam dataset. Range ini overlap dengan hampir semua regime categories kecuali deep capitulation dan extreme euphoria. Di zone ini, aSOPR tidak memberi informasi directional apapun tanpa konteks metrik lain.

---

### 4.2 LTH-SOPR Failure Modes

**FAILURE 1: LTH-SOPR > 3.0 sebagai sell signal terlalu awal dan terlalu lama**

Di 2021: LTH-SOPR > 3.0 mulai sekitar Desember 2020 dan berlangsung hampir terus-menerus sampai Juni 2021. Ini mencakup periode dari $29K (Desember 2020) sampai $29K (Jun 2021 bottom). Kalau jual saat LTH-SOPR pertama melewati 3.0, kamu jual di $29K dan miss seluruh run ke $63K.

**FAILURE 2: LTH-SOPR < 1.0 juga terjadi selama 2023 bull run**

Jun–Okt 2023: LTH-SOPR dip di bawah 1.0 berkali-kali (11 episodes, sebagian 1–3 hari, satu episode 11 hari) saat harga di $25K–$30K range. Ini terjadi karena banyak LTH yang membeli di $40–60K area di 2021 masih under water meskipun pasar sedang dalam mode recovery.

Jika interpretasi "LTH < 1.0 = bear market" diterapkan rigid di sini, kesimpulannya salah — harga justru naik ke $70K+ dalam 6 bulan berikutnya.

**Pembeda:** Ini adalah brief dips (1–11 hari) bukan sustained episode (>30 hari). Aturan durasi adalah pembeda kritis.

**FAILURE 3: LTH-SOPR absolute minimum berbeda tiap cycle**

- 2018–2019 bear bottom: LTH-SOPR minimum 0.272
- 2022 bear bottom: LTH-SOPR minimum 0.346
- 2026 bear current minimum: 0.647

Tidak ada fixed "bottom level" untuk LTH-SOPR. Setiap cycle, structural composition LTH berbeda. LTH di 2025 banyak yang beli di $50–90K range — LTH-SOPR mereka tidak bisa turun se-dalam LTH di 2017 yang beli di $1–3K. Ini structural limit, bukan indicator that the bottom is in.

**FAILURE 4: LTH-SOPR lagging menyebabkan entry terlambat kalau ditunggu**

Di Start of Bull 2019 (Apr 25), LTH-SOPR masih 0.674. Kalau menunggu LTH-SOPR > 1.0 untuk konfirmasi bull, entry terjadi di sekitar Jun 2019 ketika harga sudah di $7K–$10K (naik 40–100% dari bottom). Dan bahkan di situ, LTH-SOPR hanya briefly menyentuh 1.0 sebelum kembali di bawah 1.0 selama pullback.

---

### 4.3 STH-SOPR Failure Modes

**FAILURE 1: Bull dip readings bisa lebih tinggi dari cycle peak readings**

Jan 2021 Bull Dip (harga $35K): STH-SOPR di first day = 1.034
Cycle Peak Nov 2021 (harga $67K): STH-SOPR di first day = 1.008

Bull dip reading lebih tinggi dari cycle peak. Ini counter-intuitive tapi mekaniknya jelas: di Jan 2021, banyak STH yang beli di $10–20K dan jual di $35K (profit besar). Di Nov 2021, market sudah sangat mature, coins yang tersedia untuk berpindah tangan adalah yang dibeli lebih mahal, sehingga profit multiplier STH lebih kecil.

Implikasi: tidak bisa pakai "STH-SOPR tinggi = harga tinggi relative to bottom" karena timing-nya tidak linear.

**FAILURE 2: STH-SOPR tidak bisa membedakan bull dip dari mid-cycle correction sendiri**

STH-SOPR di Mid-Cycle Correction Bottom (Jul 2021): avg 0.976, min 0.859
STH-SOPR di Bull Dip Jan 2021: avg 1.021, min 0.960
STH-SOPR di Bull Dip Sep 2017: avg 0.980, min 0.896

Range STH-SOPR yang overlap antara severe bull dips dan mid-cycle correction membuat pembedaan hanya dari STH saja tidak mungkin. Harus kombinasi dengan LTH-SOPR dan durasi.

**FAILURE 3: STH-SOPR extended period > 1.0 tidak mengindikasikan berapa lama bull akan bertahan**

STH-SOPR > 1.03 terjadi 32 episodes sepanjang dataset, termasuk banyak di tengah bull run 2017 dan 2020-2021. Setelah trigger, price bisa naik lagi 30–130% sebelum actual top. STH-SOPR tidak memberikan informasi tentang jarak harga dari top.

---

### 4.4 Ranking Failure Rate

Dari yang paling sering menghasilkan actionable misleading signal:

**1. aSOPR fixed upper threshold (paling sering fail untuk cycle tops):** Miss cycle peak 2021 dan 2025 sepenuhnya jika menggunakan threshold 2017.

**2. LTH-SOPR brief dips < 1.0 (banyak false bear signals):** 37 short episodes (1–10 hari) yang tersebar termasuk di tengah 2023 bull run. Tanpa filter durasi, ini memberikan terlalu banyak false alarms.

**3. aSOPR < 0.97 tanpa konteks LTH (false capitulation signals):** May dan Jun 2021 adalah contoh textbook.

**4. STH-SOPR sebagai solo indicator (terlalu banyak noise):** 32 episodes STH > 1.03, 31% di antaranya adalah false sell signals. 19 episodes STH < 0.97, banyak di tengah bear yang belum bottom.

**Kondisi market yang membuat SEMUA metrik SOPR kurang reliable:**
- Flash crashes (COVID Mar 2020): readings ekstrem dalam waktu sangat singkat, tidak mencerminkan structural bear
- Transisi regime ambiguous (2–4 minggu di antara labeled events): metrics oscillate tanpa clear trend
- Post-halving market structure shifts: perlu 2–3 bulan untuk stabilize

---

## 5. MAPPING KE REGIME CATEGORIES

### 5.1 Tabel Signature SOPR per Regime

| Regime | aSOPR | LTH-SOPR | STH-SOPR | Weight dalam Decision |
|--------|-------|----------|----------|-----------------------|
| **Cycle Peak** | 1.02–1.18 (diminishing) | 1.6–16 (diminishing) | 1.01–1.14 (diminishing) | RENDAH — terlalu compressed untuk timing |
| **Local Top** | 1.03–1.21 | 2.1–13 | 1.01–1.20 | MEDIUM — LTH RISING pre-top reliable |
| **Upper Range Recovery** | 1.00–1.19 | 0.6–2.5 (crossing 1.0) | 0.97–1.15 | MEDIUM — konteks LTH penting |
| **Bull Dip** | 0.95–1.09 | >1.0 (key) | 0.90–1.03 (typically below 1.0) | MEDIUM-HIGH — LTH > 1.0 + aSOPR reclaim |
| **Mid-Cycle Correction** | 0.87–1.20 | >1.5 (key) | 0.86–1.03 (below 1.0 sustained) | HIGH — LTH > 1.0 distinguishes from bear |
| **Lower High Confirm** | 1.00–1.13 | 1.6–14 | 0.99–1.09 | HIGH — pre-trend DECLINING 4/4 |
| **Bear Market Decline** | 0.90–1.05 | <1.0 sustained | 0.93–1.02 | HIGH — LTH < 1.0 sustained |
| **Bear Bottom Near** | 0.82–0.98 | 0.27–0.74 | 0.91–0.99 | HIGH — absolute levels reliable |
| **Pre Detection Start Bull** | 0.97–1.02 | 0.5–0.7 (still < 1.0) | >1.0 (key divergence) | HIGH — STH > LTH divergence |
| **Start of Bull Confirmation** | ~0.99 | 0.67–0.89 (still < 1.0) | ~0.99 | MEDIUM — context + LTH direction |

### 5.2 Kapan SOPR Family Harus Diberi Weight Tinggi

**Beri weight tinggi:**
- Konfirmasi bear market: LTH-SOPR sustained < 1.0 > 30 hari — ini signal dengan near-zero false positives dalam dataset
- Identifikasi Lower High: aSOPR dan STH-SOPR DECLINING secara trend sementara harga sideways/naik — 4/4 hit rate
- Konfirmasi bull dip (post-facto): aSOPR reclaim 1.0 dalam 1–2 hari setelah dip — 15/15 hit rate
- Pre Detection: STH-SOPR > 1.0 sementara LTH-SOPR masih < 1.0 — 3/3 events

**Beri weight rendah / perlu multi-signal:**
- Menentukan cycle peak timing: SOPR terlalu compressed di 2021 dan 2025 untuk solo timing
- Membedakan bull dip dari mid-cycle correction in real-time: butuh price magnitude dan duration sebagai tambahan
- Menentukan exact bottom: LTH-SOPR minimum berbeda tiap cycle, tidak ada fixed level

### 5.3 Red Flags yang Harus Trigger Immediate Attention

1. **LTH-SOPR crossing below 1.0 dan bertahan > 7 hari:** Activate bear protocols, monitor LTV jika ada loan aktif.

2. **aSOPR dan STH-SOPR keduanya DECLINING trend selama 14+ hari sementara harga flat atau naik:** Distribution signal — Lower High territory. Ini adalah pre-bear warning yang paling reliable dalam dataset.

3. **STH-SOPR sustained below 0.97 selama > 14 hari:** Bukan simple bull dip — pasar dalam sustained distress. Bedakan dari bear dengan cek LTH-SOPR.

4. **Semua tiga metrik di bawah 1.0 secara bersamaan untuk > 7 hari berturut-turut:** Deep bear market atau extreme event. Catat sebagai potential extreme-fear / capitulation area.

5. **LTH-SOPR RISING sementara STH-SOPR DECLINING pada harga yang sama:** LTH mungkin distributing ke STH yang langsung under water. Classic distribution-at-top pattern sebelum local tops (terjadi di 5/6 local top events).

6. **STH-SOPR > 1.0 sementara LTH-SOPR masih < 1.0 setelah periode bear panjang:** Pre Detection signal. Harga mungkin sudah 30–50% dari bottom sebelum kondisi ini terjadi — ini bukan "beli di bottom" signal tapi "trend sudah berubah" signal.

---

## LAMPIRAN B: FLAG UNTUK VERIFIKASI (Rule Ranges & Mapping)

⚠️ **Data yang membutuhkan cross-check di ChartInspect:**

1. **LTH-SOPR minimum historical values:** 0.272 (Jan 2019) dan 0.346 (Nov 2022) adalah kritis untuk calibrating "Bear Bottom Near" threshold. Perlu konfirmasi di ChartInspect.

2. **Episode LTH-SOPR < 1.0 di 2023 bull run:** Data menunjukkan banyak brief dips di bawah 1.0 antara Jun-Okt 2023 saat harga $26–30K. Perlu konfirmasi apakah ini artifact data atau genuine readings — karena jika genuine, ini adalah kasus paling kuat untuk "duration rule" sebagai filter.

3. **Current bear market (2026):** LTH-SOPR minimum 0.647 per Jun 16, 2026. Episode LTH < 1.0 sudah 97 hari. Membutuhkan monitoring ongoing untuk update ke Knowledge Base.

4. **aSOPR dan STH-SOPR exact definitions:** ChartInspect menggunakan Glassnode sebagai source. Perlu konfirmasi bahwa definisi STH/LTH boundary (155 hari) dan "adjusted" filtering konsisten dengan yang digunakan di sini.

---

## 6. KOREKSI METODOLOGI: Retrospective Pattern vs Forward-Looking Signal Precision

⚠️ **Koreksi terhadap framing di Section 1.6 dan 3.4 di atas.**

Section 1.6 menyatakan "aSOPR dan STH-SOPR DECLINING 4/4 sebelum Lower High" dan Section 3.4 menyebut "LTH declining while price rising = distribution warning" (286 hari kemunculan). Kedua klaim ini **benar secara deskriptif** tapi **menyesatkan kalau dibaca sebagai trigger forward-looking**, karena mencampur dua pertanyaan berbeda:

- P(metrik declining | sudah tau ini Lower High) — ini yang dihitung di 1.6, hasilnya 4/4 (100%)
- P(ini akan jadi Lower High | metrik declining) — ini yang dibutuhkan untuk actionable signal

**Test base rate (scan seluruh history, bukan dikondisikan dari event yang sudah diketahui):**

| Pattern | Episodes (seluruh history, clustered ≥3 hari) | Dekat labeled top (±10-20d) | Price masih naik 10%+ dalam 60d (false signal) |
|---|---|---|---|
| LTH declining 5%+ (7d) + price naik 5%+ (7d) | 43 | 7 (16%) | 22 (51%) |
| aSOPR + STH declining bareng + price naik | 9 | 1 (11%) | 6 (67%) |

Kedua pattern punya precision rendah (11-16%) sebagai forward trigger. Base rate occurrence-nya terlalu sering dibanding jumlah actual top event, sehingga sebagian besar kemunculan pattern ini cuma noise di tengah bull run yang lanjut naik.

**Kenapa LTH-SOPR lebih noisy secara struktural — volatilitas 7-hari % change:**

| Metrik | Std dev 7d-change | Max abs swing |
|---|---|---|
| aSOPR | 0.046 | 48% |
| STH-SOPR | 0.032 | 47% |
| LTH-SOPR | **0.480** | **1,178%** |

LTH-SOPR ~10x lebih volatile dari aSOPR/STH-SOPR. Contoh: Jan–Feb 2021, di tengah bull run sehat tanpa distribution event, LTH-SOPR bergerak dari 4.02 ke 6.86 (+70%) murni karena efek mekanik cost basis LTH yang jauh di bawah harga pasar — bukan signal perilaku jual riil.

**Implikasi praktis:** Pattern "declining while price rising" itu *necessary but not sufficient* — muncul di hampir semua Lower High, tapi juga di mayoritas pullback biasa yang lanjut naik. Jangan dipakai standalone untuk exit decision. Kombinasikan dengan: durasi overbought sebelumnya, magnitude price extension, dan konfirmasi dari MVRV.

---

## 7. SMA15 SIGNAL RELIABILITY

### 7.1 Noise reduction tapi crossing 1.0 bukan sinyal baik

SMA15 mengurangi crossing frequency 89-92% dibanding raw value (aSOPR: 745→80 crossings; LTH: 362→30; STH: 871→100). Tapi **crossing level 1.0 sebagai trigger entry/exit gagal sebagai signal**:

| Signal | n | Win rate | Avg return 30d |
|---|---|---|---|
| aSOPR SMA15 cross ABOVE 1.0 (bullish) | 39 | 18/39 (46%) | **-3.0%** |
| aSOPR SMA15 cross BELOW 1.0 (bearish) | 40 | 22/40 (55%) | -3.2% |

Win rate cross-above di bawah coin flip, avg return negatif — konsisten di kedua konteks bull/bear (price vs SMA200). **SMA15 crossing 1.0 itu lagging, bukan leading.**

### 7.2 Whipsaw zones di periode paling kritis

Periode dengan 4+ crossing dalam 60 hari (flip-flop zone): **Des 2021–Feb 2022** (Lower High 2021 zone), **Mar–Jun 2022** (Bear Decline confirming), **Des 2025–Feb 2026** (recent top zone). Whipsaw paling parah justru muncul di momen paling penting untuk decision-making.

### 7.3 Percentile-based dynamic threshold jauh lebih baik dari fixed threshold

| Signal | Threshold | n | Win rate | Avg return |
|---|---|---|---|---|
| **STH-SOPR SMA15 < 10th percentile** | < 0.9816 | 19 | **79%** | **+20.0% (60d)** |
| LTH-SOPR SMA15 < 10th percentile | < 0.774 | 6 | 67% | +70.5% (90d) |
| LTH-SOPR SMA15 > 90th percentile | > 4.615 | 4 | 50% | mixed (coin flip) |

**STH-SOPR SMA15 di bawah 10th percentile adalah buy signal paling reliable di seluruh analisis SOPR family** — 79% win rate, hanya 19 episode dalam 10 tahun (selektif, gak overtrigger). LTH-SOPR extreme low juga kuat tapi sample size kecil (n=6, satu false signal Okt-Nov 2018 karena bear belum selesai). LTH-SOPR extreme high gak reliable sebagai sell signal (coin flip).

⚠️ **Catatan lookahead bias:** Percentile 10 dihitung pakai full-sample 2016-2026. Cek pakai expanding window:

| Data sampai... | Percentile 10 cutoff |
|---|---|
| 2018-12-31 | 0.9736 |
| 2020-12-31 | 0.9775 |
| 2022-12-31 | 0.9776 |
| 2024-12-31 | 0.9806 |
| 2026-06-16 (full sample) | 0.9816 |

Drift kecil (~0.8% selama 8 tahun) untuk STH-SOPR sisi bawah — minor tapi nyata. Untuk implementasi live, gunakan expanding/rolling percentile (dihitung ulang tiap hari pakai data sampai hari itu), bukan percentile statis dari backtest historis.

---

## 8. DIVERGENCE ANALYSIS — REGULAR & HIDDEN BULLISH

**Metodologi:** deteksi local price minima (10-day window), bandingkan pasangan low berurutan (gap 15-150 hari), filter hanya yang punya struktur swing valid (bounce ≥5% di antara dua low — 93% dari kandidat lolos validitas ini).

- **Regular bullish divergence**: harga lower low, indikator higher low → reversal signal
- **Hidden bullish divergence**: harga higher low, indikator lower low → continuation signal

### Hasil

| Metrik | Regular Bull (n, win%, avg ret30) | Hidden Bull (n, win%, avg ret30) |
|---|---|---|
| aSOPR | 13, 85%, +11.4% | 17, 76%, +20.0% |
| LTH-SOPR | 16, 75%, +5.7% | 20, 60%, +12.4% |
| **STH-SOPR** | **11, 100%, +19.8%** | **17, 88%, +33.7%** |

### Finding utama: STH-SOPR divergence adalah sinyal paling reliable di seluruh SOPR family

- Regular bullish divergence STH-SOPR: **11/11 (100%) hit rate**. Setiap kali harga bikin lower low tapi STH-SOPR bikin higher low, market naik dalam 30 hari setelahnya — tanpa exception di dataset 10 tahun.
- Hidden bullish divergence STH-SOPR: 15/17 (88%), avg return +33.7% — return tertinggi dari semua kategori.

**Contoh konkret:**
- Regular bullish: 25 Jun 2021 ($31,631, STH=0.859) → 20 Jul 2021 ($29,837, STH=0.960) → +56.7% dalam 30 hari (Mid-Cycle Correction Bottom)
- Hidden bullish terkuat: 24 Okt 2017 ($5,526, STH=1.031) → 12 Nov 2017 ($5,885, STH=0.993) → **+190.7% dalam 30 hari** (pre-cycle peak 2017 blow-off)

**Kenapa STH-SOPR lebih reliable dari LTH-SOPR untuk divergence:** konsisten dengan temuan volatility di Section 6 — cost basis STH lebih dekat ke harga pasar, jadi pergerakannya lebih murni mencerminkan tekanan jual-beli riil. LTH-SOPR Hidden Bull cuma 60% win rate — paling lemah dari semua kategori.

⚠️ **Catatan kehati-hatian:**
- Sample size 11-20 instance per kategori — cukup untuk pola, belum cukup untuk statistical confidence tinggi (10 tahun data, bukan ratusan cycle)
- Banyak instance regular bullish STH-SOPR cluster di sekitar bear bottom 2022 dan mid-cycle correction 2021 — kemungkinan non-independence
- Analisis ini retrospective — identifikasi local min butuh ±10 hari konfirmasi setelahnya. Entry real-time akan sedikit lebih telat dari titik low yang tercatat.

**Rekomendasi:** STH-SOPR divergence (regular dan hidden bullish) jadi kandidat prioritas tertinggi untuk masuk scoring framework Phase 3.

---

## 9. aSOPR EMA CROSSOVER CANDIDATES

**Sumber:** Backtest eksternal (periode 2013-2025, algorithmic event detection: window=90d, min drawdown=28%, min runup=65%, merge=60d), divalidasi sebagian terhadap project's labeled events (2016+).

### 9.1 Top 3 Pairs — Klaim Sumber Asli

**UP Crossover (Accumulate/Buy):**

| Pair | Avg Lead | Med Lead | Hit Rate @60d | Detection | Precision | False+/yr |
|---|---|---|---|---|---|---|
| EMA90/SMA80 | 62d | 47d | 71% | 11/11 | 29.8% | 2.5 |
| EMA55/SMA35 | 64d | 65d | 62% | 11/11 | 27.3% | 3.7 |
| EMA60/SMA30 | 42d | 25d | 63% | 11/11 | 31.7% | 3.2 |

**DOWN Crossover (Distribute/Sell):**

| Pair | Avg Lead | Med Lead | Hit Rate @60d | Detection | Precision | False+/yr |
|---|---|---|---|---|---|---|
| EMA90/SMA80 | 60d | 50d | 67% | 9/10 | 22.4% | 2.9 |
| EMA60/SMA30 | 45d | 23d | 61% | 9/10 | 25.9% | 3.1 |
| EMA55/SMA35 | 37d | 41d | 58% | 9/10 | 23.8% | 3.7 |

**Threshold filter yang disarankan sumber asli:**

| Direction | Threshold | Logic |
|---|---|---|
| UP (buy) | EMA ≤ 0.99–1.00 | aSOPR ditekan — holder jual rugi/impas |
| DOWN (sell) | EMA ≥ 1.01–1.015 | aSOPR elevated — holder jual untung berlebihan |

EMA90/SMA80: gunakan 1.015/0.99 (strict). EMA55/SMA35 & EMA60/SMA30: bisa pakai 1.01/1.00 (lebih longgar).

**Sequential firing di cycle events** — bottom: EMA55/SMA35 UP (~64d sebelum) → EMA90/SMA80 UP (~62d) → EMA60/SMA30 UP (~42d, konfirmasi). Peak: EMA90/SMA80 DOWN (~60d, earliest) → EMA60/SMA30 DOWN (~45d) → EMA55/SMA35 DOWN (~37d, closest to peak).

### 9.2 Validasi Project — Temuan Penting

**Raw crossover EMA90/SMA80 itu whipsaw parah, bukan sinyal langka:** 1,956 UP crossings dan 43 DOWN crossings dalam 10 tahun data project (~196 UP signal/tahun) — jauh dari "False+/yr: 2.5" yang diklaim. Penyebab: EMA90 dan SMA80 periode hampir sama, dua garis saling nempel dan crossing di fluktuasi kecil. **Threshold filter (EMA≤1.00/≥1.01) yang melakukan hampir seluruh kerja filtering**, bukan crossover-nya sendiri.

**Setelah filter+merge 45 hari diterapkan (7 UP signal, 17 DOWN signal dalam 10 tahun), test terhadap labeled event project:**

| Direction | Match ke labeled event | Precision | Detection rate |
|---|---|---|---|
| UP (buy) | 1/7 (14%) | 14% | **2/5 Bear Bottom event MISS TOTAL** (2018 Tier 1 & Window End 2019 — capitulation terdalam di dataset gak ke-detect) |
| DOWN (sell) | 10/17 (59%) | 59% | **13/13 peak/top event ter-detect** (100%), lead time 2-170 hari, avg ~51d (konsisten dengan klaim ~50-60d) |

**Kesimpulan:** DOWN/sell crossover signal jauh lebih reliable dari UP/buy crossover signal saat diuji terhadap event labeling project ini. UP signal gagal total di periode bear paling penting (2018-2019).

⚠️ **Catatan:** Validasi ini gak sepenuhnya apple-to-apple dengan sumber asli (beda date range 2013-2025 vs 2016+, beda definisi "major event" — 11 bottom/10 peak algoritmik vs 5 Bear Bottom/13 peak labeled di project ini).

**Rekomendasi penggunaan:** Prioritaskan DOWN/sell crossover sebagai sinyal pendukung distribusi/top warning. UP/buy crossover signal perlu dipakai dengan kehati-hatian tinggi — jangan dijadikan standalone trigger untuk entry, terutama di periode bear market dalam dimana signal ini historically gagal fire sama sekali.

---

## 10. LTH/STH RATIO & FIVE DIVERGENCE STATES FRAMEWORK

### 10.1 Definisi

- **LTH/STH Ratio** = LTH-SOPR ÷ STH-SOPR. Mengukur relatif besar profit yang direalisasikan LTH dibanding STH pada waktu yang sama.
- **Spread (L−S)** = LTH-SOPR − STH-SOPR. Ukuran absolut perbedaan profitability antar cohort.
- **STH-aSOPR** = STH-SOPR − aSOPR. Positif artinya STH outperforms aggregate (unusual — biasanya LTH profit mengangkat aSOPR di atas STH).

### 10.2 LTH/STH Ratio Zones & Per-Regime Statistics

✅ **Tervalidasi terhadap data project (2016-2026):**

| Regime | Min | Median | Max | n | 
|---|---|---|---|---|
| Cycle Peak | 1.101 | 2.455 | 25.657 | 36 |
| Local Top | 1.288 | 2.270 | 12.781 | 82 |
| Mid-Cycle Correction | 1.562 | 2.343 | 11.668 | 31 |
| Bull Dip | 0.523 | 1.543 | 6.483 | 174 |
| Lower High Confirm | 1.591 | 9.365 | 53.252 | 14 |
| Bear Bottom Near | 0.365 | 0.525 | 0.759 | 23 |
| Pre Detection | 0.459 | 0.551 | 0.679 | 10 |
| Start of Bull | 0.632 | 0.723 | 0.899 | 4 |

Dua regime paling tightly bounded: **Pre Detection (0.459–0.679)** dan **Start of Bull (0.632–0.899)** — paling reliably identifiable dari data on-chain.

### 10.3 Five Divergence States

Klasifikasi harian berdasarkan posisi relatif LTH-SOPR, STH-SOPR, dan threshold 1.0:

- **State A** — LTH > STH, keduanya > 1.0. Normal bull market, LTH distributing, STH following.
- **State B** — LTH > STH, STH < 1.0. LTH masih profit, new buyers stressed. Bull dip / early bear decline.
- **State C** — STH > LTH, keduanya > 1.0. New buyers outperforming LTH. Rare.
- **State D** — STH > 1.0, LTH < 1.0. **PRE-BULL SIGNAL paling distinctive.** LTH belum recover, STH near-bottom sudah profit.
- **State E** — STH > LTH, keduanya < 1.0. Deep capitulation, STH losing less dari LTH.
- **State F** — LTH > STH, keduanya < 1.0. Biasanya di hari transisi tipis edge bear territory.

**Distribusi state full dataset (2016-2026, n=3,820 hari):** A:1,860 (49%) | B:1,102 (29%) | E:529 (14%) | D:301 (8%) | C:14 (0.4%) | F:14 (0.4%)

### 10.4 State D sebagai Pre-Bull Detector

✅ **Tervalidasi pada level harian.** Rule: isolated 1-2 hari = noise/false signal. Sustained oscillation D↔E 2-4 minggu = strong Pre Detection signal.

| Periode | Pola | Outcome |
|---|---|---|
| Jul 2018 | Isolated 1-2 hari (2 Jul, 7 Jul terpisah oleh E days) | **False signal** — price $6,604→$3,281 (-50%) ke Bear Bottom Des 2018 |
| Feb–Mei 2019 | Sustained oscillation D↔E (65 hari cluster, 31 transisi) | Bull market dimulai Apr 2019, price $3,658→$10,103 |
| Jan–Apr 2023 | Sustained oscillation D↔E (68 hari cluster, 20 transisi) | Bull market dimulai Feb 2023, price $16,904→$26,820 |
| Feb–Jun 2026 | Sporadic, campur dengan A/B (`BEBBEEBBBEEEDEDEFFEEEAEDDDDAAEDDDDEBEEEEEEBEED`) | **Status: monitoring** — belum establish pola D↔E bersih seperti 2019/2023 |

Verifikasi sequence harian (sample tiap 3 hari) konfirmasi karakter oscillation genuine di 2019 dan 2023, vs pola jauh lebih messy di 2026 (campur B/A/D/E, belum jadi sinyal pre-detection yang confirmed).

### 10.5 State Patterns per Regime — Tervalidasi

| Regime | Dominant state (data aktual) | Status |
|---|---|---|
| Cycle Peak | A 89%, B 11% | ✅ |
| Local Top | A 90%, B 10% | ✅ (directionally) |
| Upper Range Recovery | A 71%, D 13%, B 10%, C/E 3% | ✅ |
| Bull Dip | B 61%, A 29%, E 7% | ✅ "B→A" |
| Mid-Cycle Correction | B 94%, A 6% | ✅ "B persists" |
| Lower High Confirm | A 64%, B 36% | ✅ "A→B transition" |
| Bear Bottom Near | **E 100%** | ✅ "E dominant" |
| Pre Detection | D 70%, E 30% | ✅ "D↔E frequent" |
| Start of Bull | D 50%, E 50% | ✅ |

### 10.6 STH-aSOPR Sign Flip sebagai Mechanical Confirm

Di semua bull market regime: STH-aSOPR selalu **negatif**. Di Bear Bottom dan Pre Detection: balik **positif**.

| Regime | STH-aSOPR avg | LTH-aSOPR avg | n |
|---|---|---|---|
| Cycle Peak | -0.0270 | +6.6166 | 36 |
| Local Top | -0.0298 | +1.7871 | 82 |
| Upper Range Recovery | -0.0047 | +0.3118 | 31 |
| Bull Dip | -0.0121 | +1.0122 | 174 |
| Mid-Cycle Correction | -0.0170 | +1.7163 | 31 |
| Lower High Confirm | -0.0283 | +10.0826 | 14 |
| Bear Bottom Near | **+0.0246** | -0.4126 | 23 |
| Pre Detection | **+0.0197** | -0.4083 | 10 |
| Start of Bull | **+0.0066** | -0.2487 | 4 |

**Rule (tervalidasi):** Sign flip dari negatif ke positif sustained (3+ hari berturut-turut) = mechanical confirmation memasuki Bear Bottom/Pre Detection territory. First sustained 3-day flip menuju Bear Bottom 2018: **1 Nov 2018** — mendahului actual bottom (14 Des 2018) ~6 minggu.

### 10.7 Ratio Sebagai Regime Differentiator — Limitasi

Bull Dip ratio range sangat lebar (0.523–6.483 di data project, vs klaim asli 0.523–7.820) — terlalu lebar untuk standalone identifier.

- Jun 2020 bull dip: ratio **0.974** ✅ exact match (LTH masih underwater post-COVID)
- Sep 2017 bull dip: ratio 5.179 di first day (klaim asli 6.689) — nilai 6.024–6.163 muncul beberapa hari kemudian dalam window yang sama. Arah dan magnitude konsisten, tanggal spesifik kemungkinan beda hari dalam window sama.

---

## 11. STH-SOPR BOLLINGER BAND — BULL DIP SIGNAL

**Status: User-verified independen.**

### 11.1 Setup

Referensi: chart STH-SOPR dengan Bollinger Band dari CryptoQuant (BB 28,2). Tujuan: cari setting optimal untuk nangkap bull dip entry, dianalisis dari data 2016–2025.

Metodologi: 18 bull dip bottom teridentifikasi di 2023-2025, 33 di 2016-2022. Signal = first day STH-SOPR cross di bawah lower Bollinger Band, de-duplicated setiap 7 hari. Metrik evaluasi: Recall (% dip tertangkap), Precision (% signal valid), Avg G30d/G60d, Bear FP (false positive per tahun).

### 11.2 Grid Search — BB Period vs Std Dev

30 kombinasi diuji (period: 14/20/28/30/50/60 × std_dev: 1.5/1.75/2.0/2.25/2.5). Trade-off konsisten lintas semua setting:

| std_dev rendah (1.5) | std_dev tinggi (2.5) |
|---|---|
| Recall tinggi (nangkap lebih banyak dip) | Recall rendah (banyak terlewat) |
| Precision rendah (lebih banyak noise) | Precision tinggi (hampir selalu valid) |
| Signal lebih banyak | Signal sedikit |
| Bear FP lebih banyak | Bear FP lebih sedikit |

Gain per signal lebih besar di std_dev tinggi — hanya fire saat dip paling dalam yang historis recovery-nya lebih besar. Period (28 vs 50 vs 60) pengaruhnya lebih kecil dari std_dev; period lebih panjang = band lebih smooth, lebih jarang fire, gain 60d cenderung lebih tinggi.

### 11.3 Setting Terbaik per Tujuan

- **Prioritas recall** (gak mau miss dip): BB(28, 1.5) — recall 88.9%, precision 67.7%, G30d +11.4%, 31 signal, 8 bear FP di 2023-2025.
- **Prioritas precision** (hanya masuk saat yakin): BB(28, 2.5) — recall 50%, precision 90.9%, G30d +15.5%, G60d +23.4%, 11 signal, 6 bear FP.
- **Sweet spot gain terbesar**: BB(60, 2.25) — precision 91.7%, G60d +29.3%. Hanya fire saat dip paling ekstrem.
- **Image baseline** BB(28, 2.0) — di tengah. Recall 55.6%, precision 76.5%, G30d +13.0%. Balanced, bukan terbaik di salah satu sisi.

### 11.4 Validasi Cross-Cycle (2016-2022)

Semua setting mengalami penurunan performa di cycle lama, terutama recall:

| Setting | Recall 23-25 | Recall 16-22 | Bear FP 23-25 | Bear FP 16-22 |
|---|---|---|---|---|
| BB(28,1.5) | 88.9% | 57.6% | 8 | 34 |
| BB(28,2.0) | 55.6% | 42.4% | 8 | 23 |
| BB(28,2.5) | 50.0% | 33.3% | 6 | 16 |

Dua penyebab utama: (1) Dip 2016-2017 lebih "spike" dan singkat — market lebih kecil, lebih volatile, BB kurang sensitif menangkapnya. (2) Bear market 2018 dan 2022 masing-masing ~1 tahun — jauh lebih panjang dari bear 2025 (~7 bulan), sehingga bear FP jauh lebih banyak.

### 11.5 Filter Tambahan: Price ≤ STH Realized Price

Ide: signal hanya valid jika harga ≤ STH RP di hari yang sama (STH-SOPR tertekan + STH aggregate underwater bersamaan).

**Hasil 2023-2025:**

| Config | Recall | Precision | Signals |
|---|---|---|---|
| BB(28,1.5) saja | 83.3% | 67.7% | 31 |
| BB(28,1.5) + price ≤ STH RP | 50.0% | **92.9%** | 14 |
| BB(28,2.0) saja | 55.6% | 76.5% | 17 |
| BB(28,2.0) + price ≤ STH RP | 44.4% | **90.9%** | 11 |

Precision lompat drastis. Dari 14 signal yang lolos di BB(28,1.5)+filter, hampir semua valid, dengan gain +22.1%. Yang dibuang filter (9 dip di 2023-2025): semua di periode harga masih jauh di atas STH RP — early bull 2023, bull run post-ETF Mar 2024, ATH period Jan 2025. Dip ini memang terjadi tapi secara fundamental harga belum cukup stressed.

Bear FP tidak bergerak di kedua setting (tetap 8) — di bear market, harga SUDAH di bawah STH RP by definition, jadi filter selalu lolos. Bear FP hanya bisa disaring oleh regime gating (S2 latch), bukan price filter.

**Hasil 2016-2022:** filter ini gagal total — recall jatuh ke 9.1%. Di cycle lama, bull dip hampir tidak pernah menyentuh STH RP karena market trending up aggressively. Filter yang dirancang untuk sideways/choppy bull tidak applicable ke parabolic bull.

**Kesimpulan filter:** hanya relevan untuk market condition seperti 2023-2025 (bull market sideways/choppy), bukan parabolic trending up. Jika next cycle lebih mirip 2017/2021, filter ini akan miss hampir semua dip.

⚠️ **Catatan data:** Project ini belum punya kolom STH Realized Price di dataset utama (`data_momentum_events.csv`). Validasi independen terhadap angka di section ini belum bisa dilakukan oleh Claude — bagian Bollinger Band core (11.1-11.4) sudah direplikasi sebagian dan konsisten arahnya; bagian filter STH RP (11.5) murni berdasarkan verifikasi user. Kalau STH Realized Price ditambahkan ke dataset di kemudian hari, sebaiknya divalidasi ulang.

### 11.6 Verifikasi Tambahan (Project)

Tiga tanggal signal yang ditandai di chart referensi (24.05.01, 24.07.05, 24.08.05) dikonfirmasi match persis ke labeled event project: **Bull Dip Mei 2024, Bull Dip Jul 2024, Bull Dip Agt (Yen Carry Trade)**. Mekanisme perhitungan Bollinger Band juga tervalidasi: STH-SOPR (0.965) cross di bawah lower band BB(28,2.0) yang dihitung (0.973) persis di tanggal 2024-05-01, match exact dengan chart.

---

## 12. STH-SOPR MA90 / MA90-MA60 GAP-AND-CROSS FRAMEWORK

### 12.1 Konstruksi Indikator

**MA90:** Simple Moving Average 90 hari dari STH-SOPR. Smooth enough untuk menghilangkan daily noise, tapi tetap responsive terhadap perubahan profitability regime.

**MA90-MA60:** Simple Moving Average 60 hari dari MA90 (double-smoothed). Ini baseline yang bergerak lebih lambat — menangkap "trend of the trend." Ketika MA90 di atas MA90-MA60, profitability STH sedang improving. Ketika di bawah, deteriorating.

**Gap:** MA90 minus MA90-MA60. Positif = momentum improving, negatif = momentum deteriorating. Magnitude gap menunjukkan seberapa cepat perubahan terjadi.

**Data source:** CSV terpisah dari ChartInspect.com (STH-SOPR dengan SMA90d pre-computed). MA60-of-MA90 dihitung sebagai derived metric.

---

### 12.2 Tiga Signal Types

**Signal A — Gap Peak + Decline → Local Top Warning (Reduce Loan)**

Ketika gap antara MA90 dan MA90-MA60 sudah peaked dan mulai menurun, ini menandakan profitability momentum STH sudah melemah meskipun harga mungkin masih naik. Signal ini bukan precision timing tool — ini early warning untuk mulai reduce loan exposure.

**Signal B — Bearish Cross Setelah Local Top → Regime Shift ke Bull Dip**

Ketika MA90 crosses di bawah MA90-MA60 setelah local top terjadi, ini mengkonfirmasi regime transition ke period koreksi. Bearish cross = profitability trend sudah secara definitif berubah arah.

**Signal C — Bearish Cross Setelah Cycle Peak → Lower High Confirmation**

Pattern yang sama tapi setelah cycle peak. Bearish cross di konteks ini mengkonfirmasi bahwa recovery selanjutnya akan membentuk lower high, bukan new ATH.

---

### 12.3 Signal A — Gap Peak + Decline: Historical Evidence

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

### 12.4 Signal B — Bearish Cross Setelah Local Top: Historical Evidence

| Bearish Cross Date | Harga | Setelah Event | Yang Terjadi Setelahnya |
|---|---|---|---|
| 28 Mar 2021 | $55,808 | Local Top Mar 2021 (+15d) | Mid-Cycle Correction: drop ke $29K (−50%) |
| 28 Apr 2024 | $63,130 | Local Top Mar 2024 (+45d) | Bull dips berturut-turut (Mei, Jul, Agt 2024) |
| 3 Feb 2025 | $101,436 | Local Top Jan 2025 (+14d) | Bull Dip Mar–Apr 2025: drop ke $76K (−25%) |

**Hit rate:** 3/3 — bearish cross setelah local top selalu diikuti koreksi signifikan.

**Caveat severity:** Mar 2021 cross memunculkan mid-cycle correction (−50%), bukan bull dip biasa. Bearish cross sendiri tidak bisa bedakan severity koreksi yang akan terjadi. Perlu combine dengan indikator lain (durasi STH < 0.97 dari Section 2, aSOPR level, dll) untuk assess severity.

---

### 12.5 Signal C — Bearish Cross Setelah Cycle Peak: Historical Evidence

| Bearish Cross Date | Harga | Setelah Event | Yang Terjadi Setelahnya |
|---|---|---|---|
| 19 Jan 2018 | $12,037 | Cycle Peak 2017 (+33d) | Lower High Jan 2018, lalu bear market |
| 30 Nov 2021 | $56,995 | Cycle Peak 2021 (+22d) | Lower High Nov-Des 2021, lalu bear market |

**Hit rate:** 2/2 (sample kecil).

**Timing:** Bearish cross dates hampir persis di tanggal Lower High di regime taxonomy. 30 Nov 2021 = Lower High date di data original. Ini bukan coincidence — profitability momentum breakdown dan lower high formation terjadi secara simultan karena driven oleh mekanik yang sama: distribusi sudah selesai, demand baru tidak cukup.

---

### 12.6 Cycle 2025: Jul ATH vs Oct ATH — Bull Trap Thesis

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

### 12.7 Failure Modes & Limitasi

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

### 12.8 Integration dengan Framework Lain

Signal ini paling efektif kalau dipakai sebagai salah satu layer dalam multi-signal framework:

| Step | Signal | Action |
|---|---|---|
| 1. Early warning | Gap MA90−MA90-MA60 peaked dan mulai declining | Mulai kurangi loan exposure (Scale down) |
| 2. Confirmation | Bearish cross MA90 di bawah MA90-MA60 | Loan harus sudah reduced signifikan |
| 3. Severity check | Combine dengan STH-SOPR duration < 0.97 (Section 2), aSOPR level, EMA crossover direction (Section 9 — DOWN/sell crossover lebih reliable dari UP/buy) | Assess apakah ini bull dip, MCC, atau bear onset |
| 4. Regime ID | State D/E framework (Section 10), ratio zone | Confirm regime position setelah koreksi |

Cross-reference yang perlu dibangun:
- Apakah MVRV menunjukkan pattern serupa (momentum breakdown sebelum Oct 2025 ATH)? MVRV KB sudah dibangun — perlu dicek apakah ada signal momentum breakdown setara untuk Jul–Aug 2025 vs Oct 2025 window di MVRV family, belum divalidasi.
- Apakah NUPL divergence alignment ada?
- Supply in Profit trajectory selama Jul → Oct 2025 window?

NUPL dan Supply in Profit KB belum dibangun — validasi bull trap thesis di section 12.6 masih open question sampai ini selesai.

---

## 13. KONDISI SAAT INI — STATUS CHECK

**Readings terakhir (20 Mei 2026):**
- BTC: $77,563
- aSOPR: 0.887
- LTH-SOPR: 0.822
- STH-SOPR: 0.889

**Konteks dari trajectory yang lebih baru:** Bear episode (LTH-SOPR < 1.0 sustained) dimulai Feb 2026 dan masih berlangsung 97+ hari per data terakhir (Jun 16, 2026). LTH-SOPR sempat menyentuh minimum 0.647 pada 11 Mar 2026 — lebih dalam dari COVID flash crash (0.608–0.716) tapi belum mencapai level 2018 (0.272) atau 2022 (0.346). Reading 20 Mei 2026 (0.822) menunjukkan partial recovery dari titik terdalam Maret, tapi masih jauh di bawah 1.0.

**Assessment:** Readings 20 Mei 2026 berada di DEEP CAPITULATION territory — aSOPR di bawah 0.90 dan ketiga metrik di bawah 1.0, termasuk LTH-SOPR yang berarti long-term holders selling at a loss. Berdasarkan Rule 2.4 (Section 2), LTH-SOPR sustained < 1.0 selama 97+ hari sudah masuk kategori "established bear market" (≥30 hari = genuine bear, hit rate 4/4 di dataset historis).

**Yang belum terkonfirmasi:**
- aSOPR reclaim 1.0 sustained 7+ hari (belum terjadi)
- STH-SOPR reclaim 1.0 mendahului aSOPR (belum terjadi secara sustained)
- LTH-SOPR trending up secara konsisten meski masih di bawah 1.0
- State D↔E sustained oscillation 2-4 minggu (Section 10.4) — per data Feb–Jun 2026, pola masih sporadis dan campur dengan state A/B, belum establish pola bersih seperti Pre Detection 2019/2023

**Regime indication:** Bear Market Decline menuju Bear Bottom Near territory. Apakah cycle minimum LTH-SOPR (0.647, Mar 2026) sudah merupakan titik terdalam atau masih akan turun lebih jauh menuju level 2018/2022 — belum bisa ditentukan dari data SOPR saja.

**Bukan timing call.** Sesuai Rule B3/Section 2.5 dan State D framework, sinyal regime identification ini berarti "mulai monitor lebih ketat dan siapkan rencana accumulation bertahap," bukan "buy sekarang." Kalau ada posisi loan aktif, cek LTV buffer dulu sebelum sizing apapun.

---

## 14. LIMITATIONS & CONFIDENCE CAVEATS

1. **Sample size = 3 completed cycles** (2017, 2021, 2025-current). Statistical significance terbatas untuk sebagian besar rule — banyak yang berdasarkan n=2 sampai n=6. Pattern bisa berubah di cycle berikutnya.

2. **Diminishing returns terbukti konsisten di seluruh metrik.** aSOPR, LTH-SOPR, dan STH-SOPR semua menunjukkan compression setiap cycle. Threshold yang bekerja di cycle N menjadi kurang reliable di cycle N+1 — harus selalu di-recalibrate, bukan dipakai sebagai fixed number.

3. **SOPR family adalah PROFITABILITY metric, bukan PRICE metric.** Mereka mengukur kapan orang realize profit/loss, bukan ke mana harga akan pergi. Jangan dipakai sebagai price prediction tool.

4. **Retrospective pattern ≠ forward-looking signal precision (lihat Section 6).** Beberapa pattern yang descriptively terlihat 100% konsisten (misalnya "aSOPR+STH declining sebelum Lower High") ternyata hanya 11-16% precision kalau ditest sebagai forward trigger di seluruh history — base rate occurrence-nya jauh lebih sering dari actual top events. Selalu bedakan P(pattern | tahu hasilnya) dari P(hasil | pattern muncul).

5. **Exogenous shocks tidak terdeteksi.** COVID crash, FTX collapse, Yen carry trade unwind — semua datang tanpa on-chain warning dari SOPR. Risk management (position sizing, LTV buffer) harus tetap robust terlepas dari sinyal on-chain.

6. **LTH-SOPR adalah metrik paling noisy** (volatilitas 7-hari change ~10x lebih tinggi dari aSOPR/STH-SOPR — Section 6). Jangan pernah pakai daily reading untuk keputusan; minimum 14-hari average, dan tetap treat dengan skeptisisme tinggi dibanding aSOPR/STH-SOPR.

7. **Bull trap thesis (Section 12.6) masih open question**, belum di-cross-validate dengan MVRV, NUPL, atau Supply in Profit. Jangan treat Jul-Aug 2025 sebagai structural cycle peak yang confirmed sampai validasi cross-indicator selesai.

8. **Data current bear market (2026) masih ongoing** per cutoff Jun 16, 2026. Semua assessment di Section 13 perlu di-update mingguan seiring data baru masuk.

