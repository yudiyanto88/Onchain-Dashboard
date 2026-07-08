# SUPPLY IN PROFIT & LOSS — KNOWLEDGE BASE DOCUMENT

**Version:** 2.0 | **Updated:** 2026-06-21
**Data source:** ChartInspect.com (Glassnode-sourced)
**Data range:** 2016-01-01 to 2026-06-16
**Total data points:** updated per dataset terbaru | **Transition events analyzed:** 51 events across 10 regime categories

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
| Cycle Peak 2017 | $16,349 | 97.7 | 94.9 | 100.0 | 5.1 | 0.0 |
| Cycle Peak 2021 (Nov 8) | $66,027 | 98.2 | 92.0 | 100.0 | 8.0 | 0.0 |
| Cycle Peak 2025 | $123,537 | 99.4 | 97.6 | 100.0 | 2.4 | 0.0 |

**Signal fingerprint:** Total profit 97–99%, STH profit 92–98%, LTH profit = 100.0% di semua 3 events, LTH loss = 0.0% di semua events.

**Leading/lagging behavior:** STH profit adalah coincident indicator yang paling informatif — mengikuti pergerakan harga ke atas dan mencapai puncak di sekitar cycle peak (3/3 coincident). Di 2021, sempat dip ke 3% saat mid-cycle correction (-90 hari dari window start), lalu naik kembali ke 92–98% saat actual peak — menunjukkan recovery total bukan sinyal dini. LTH profit tetap di 100.0% di sepanjang periode sebelum dan selama event (3/3 stable/lagging) — tidak bergerak sebelum peak dan tidak memberikan sinyal apapun tentang timing. Total profit stable di atas 95% di seluruh 90 hari sebelum event (3/3 stable) — bukan leading signal, sudah terlalu tinggi terlalu lama.

**Post-transition (90 hari setelah hari pertama event window):** Rata-rata perubahan: Total profit turun ~25pp, STH profit turun ~60pp, LTH profit turun ~11pp.
- 2017: STH profit 94.9% → 60.6% (−34pp). LTH profit tetap 100% (tidak bergerak sama sekali — extreme lagging).
- 2021: STH profit 92.0% → 16.5% (−76pp). LTH profit 100% → 85.6% (mulai turun tapi lambat).
- 2025: STH profit 97.6% → 28.3% (−69pp). LTH profit 100% → 82.4%.

STH profit adalah indikator yang paling cepat merespons post-peak — turun rata-rata 60pp dalam 90 hari pertama. LTH profit adalah yang paling lambat (lagging sekitar 1–3 bulan).

**Cross-cycle observation:** Range sangat tight: total profit konsisten 97–99% di ketiga cycle peak, tanpa diminishing returns yang terlihat. Yang berubah adalah KECEPATAN penurunan post-peak — 2021 dan 2025 lebih cepat collapse (STH profit turun ke <30% dalam 60 hari) dibanding 2017 (lebih gradual).

**⚠️ Confidence note:** 3 data points saja. Konsistensi yang terlihat bisa jadi artifact dari sample size kecil, bukan statistical law.

---

### 1.2 LOCAL TOP
**6 events: Mar 2021, Apr 2021 (ATH), Mar 2024 (ATH), Des 2024 (ATH), Jan 2025 (ATH), Jul-Aug 2025 (ATH)**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Local Top Mar 2021 | $61,186 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 |
| Local Top Apr 2021 (ATH) | $63,551 | 98.7 | 96.3 | 100.0 | 3.7 | 0.0 |
| Local Top Mar 2024 (ATH) | $71,472 | 97.3 | 88.2 | 100.0 | 11.8 | 0.0 |
| Local Top Des 2024 (ATH) | $98,402 | 97.5 | 88.9 | 100.0 | 12.8 | 0.0 |
| Local Top Jan 2025 (ATH) | $99,994 | 96.7 | 87.8 | 100.0 | 12.2 | 0.0 |
| Local Top Jul-Aug 2025 (ATH) | $119,057 | 100.0 | 100.0 | 100.0 | 0.0 | 0.0 |

**Signal fingerprint:** Total profit 97–100%, STH profit 88–100%, LTH profit = 100.0% di semua 6 events tanpa exception, LTH loss = 0.0%.

**Masalah kritis: Local Top dan Cycle Peak TIDAK bisa dibedakan dari metrik ini saja.** Range-nya overlap sempurna — total profit 97–100% di keduanya, LTH profit 100% di keduanya. Supply in profit/loss tidak bisa menjawab "ini local top yang akan recover, atau ini the top?"

**Leading/lagging behavior:** LTH profit tetap 100% di semua 6 events (6/6 stable) — tidak ada sinyal sama sekali dari metrik ini. STH profit menjadi informatif hanya saat dikombinasikan dengan price action post-event — sebelum event, STH profit naik bersama harga (coincident).

**Post-transition (90 hari setelah hari pertama event window):** Variasi sangat lebar — paling membedakan antar local tops:
- Local Top Mar 2021: STH profit masih 86.7% di +60 hari (koreksi ringan). Baru crash ke 7.2% di +90 hari saat May 2021 crash (−93pp).
- Local Top Apr 2021 (ATH): sudah masuk mid-cycle correction, pola sama.
- Local Top Mar 2024 (ATH): +90d STH profit = 74.4% (−14pp). Harga masih tinggi.
- Local Top Des 2024 (ATH): +90d STH profit = 40.5% (−48pp). Harga koreksi ke ~$96K.
- Local Top Jan 2025 (ATH): koreksi moderat berlanjut ke Bear Decline.
- Local Top Jul-Aug 2025 (ATH): +30d STH profit = 68.5% (−31.5pp). Menuju cycle peak berikutnya.

Range perubahan STH profit dalam 90 hari: −14pp sampai −93pp. Variasi ekstrem ini menunjukkan post-transition behavior local top sangat bergantung pada apakah koreksi adalah bull dip atau awal bear.

**Structural shift:** STH profit di local top: 100% (Mar 2021) → 88% (2024) → 88% (Jan 2025) → kembali 100% saat Jul-Aug 2025 (ATH baru yang kuat). Pola ini menunjukkan setiap ATH baru dalam cycle yang sama cenderung punya STH yang lebih rendah — sampai ada breakout ATH yang kuat, di mana STH kembali ke 100%. LTH profit = 100% di SEMUA local tops tanpa exception — konsisten tapi terbatas kegunaannya, tidak membedakan local top dari cycle peak maupun bull dip yang kuat.

**⚠️ Confidence note:** Kategori "local top" hanya bisa diidentifikasi secara retrospektif. Saat event terjadi, profil metrik identik dengan cycle peak — tidak ada cara membedakannya dari supply data saja.

---

### 1.3 LOWER HIGH CONFIRM TOP CYCLE
**4 events: 2018, 2021, 2025 (dua events berdekatan)**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Lower High 2018 | $13,783 | 81.7 | 60.8 | 100.0 | 39.2 | 0.0 |
| Lower High 2021 | $56,995 | 81.8 | 45.3 | 95.3 | 54.6 | 4.7 |
| Lower High 2025 | $114,584 | 83.5 | 31.7 | 100.0 | 37.2 | 0.0 |
| Lower High 2025 Conf | $112,964 | 88.1 | 51.0 | 100.0 | 49.0 | 0.0 |

**Signal fingerprint:** Total profit **82–88%** (median 82.7%), STH profit 32–61%, LTH profit 95–100%, LTH loss 0–5%.

**Ini regime yang paling terdefinisi dari perspektif total profit.** Range 82–88% secara konsisten lebih rendah dari Cycle Peak (97–99%) dan Local Top (97–100%). Gap antara total profit yang masih relatif tinggi dan STH profit yang sudah tertekan (32–61%) adalah karakteristik khas lower high.

**Leading/lagging:** STH profit adalah yang paling leading dari semua metrik di sini. Di semua 4 events, STH profit sudah turun secara signifikan SEBELUM hari pertama event:
- 2018: STH profit -90d = 82.1%, -30d = 90.2%, 0d = 60.8% (turun tajam dalam 30 hari terakhir)
- 2021: STH profit -90d = 65.9%, -30d = 76.1%, 0d = 45.3%
- 2025: STH profit -90d = 80.6%, -30d = 47.0%, 0d = 31.7% (penurunan masif di 30 hari terakhir)

Pola ini menunjukkan STH profit sebagai leading signal ke lower high — sudah dalam tren turun sebelum lower high terkonfirmasi (4/4 leading).

LTH profit: 2021 sedikit turun ke 95.3% (satu-satunya kasus LTH profit < 100% di lower high), sedangkan 2018 dan 2025 tetap 100% — LTH masih menahan supply, lagging (3/4 stable, 1/4 slight decline). Total profit turun lebih lambat dari STH profit, lebih leading dari LTH profit (coincident, 4/4).

**Post-transition (90 hari setelah hari pertama lower high window):**
- 2018: +90d → Total profit 61.9% (−19.8pp), STH profit 9.1% (−51.7pp), LTH profit tetap 100%.
- 2021: +60d → Total profit 63.5% (−18.3pp), STH profit 9.0% (−36.3pp), LTH profit 78.8% (−16.5pp).
- 2025: +30d → Total profit 63.9% (−19.6pp), STH profit 13.4% (−18.3pp), LTH profit 84.1% (−15.9pp).

Konsisten: STH profit collapse ke single digits dalam 60–90 hari di semua 3 cycle lower highs — ini adalah point of no return, setelah lower high terkonfirmasi, bear market decline dimulai.

**Cross-cycle shift:** STH profit DI TITIK lower high menurun cycle ke cycle: 60.8% (2018) → 45.3% (2021) → 31.7–51.0% (2025). Setiap lower high terjadi dengan proporsi STH yang lebih besar sudah underwater — pasar makin "mature" di distribusi. LTH profit di lower high 2021 sedikit lebih rendah (95.3%) dibanding 2018 dan 2025 (100%) — mencerminkan mid-cycle correction sebelumnya di 2021 yang sudah mengurangi LTH profit.

**⚠️ Confidence note:** Lower High 2025 punya 2 events (Lower High dan Confirmation) dalam 2 hari, diperlakukan sebagai satu periode event. Secara fungsional, ini 3 cycle lower highs yang terdokumentasi.

---

### 1.4 BULL DIP
**15 events across 2017–2025 — sample terbesar**

| Event | Year | Price | Total Profit | STH Profit | LTH Profit |
|-------|------|-------|:---:|:---:|:---:|
| Bull Dip Mar 2017 | 2017 | $967 | 83.7 | 45.9 | 99.1 |
| Bull Dip Jul 2017 | 2017 | $1,989 | 79.5 | 38.5 | 100.0 |
| Bull Dip Sep 2017 | 2017 | $4,138 | 84.7 | 63.3 | 100.0 |
| Bull Dip Jun 2020 | 2020 | $9,291 | 73.8 | 48.5 | 82.5 |
| Bull Dip Sep 2020 | 2020 | $10,173 | 79.0 | 52.0 | 87.4 |
| Bull Dip Jan 2021 | 2021 | $35,551 | 93.2 | 79.2 | 100.0 |
| Bull Dip Mar 2023 | 2023 | $22,429 | 64.3 | 70.3 | 62.7 |
| Bull Dip Jun 2023 | 2023 | $25,766 | 61.5 | 26.1 | 70.2 |
| Bull Dip Aug-Sep 2023 | 2023 | $26,069 | 60.0 | 9.9 | 72.6 |
| Bull Dip Jan 2024 | 2024 | $41,320 | 79.3 | 47.9 | 86.6 |
| Bull Dip Mei 2024 | 2024 | $58,341 | 81.8 | 35.0 | 97.5 |
| Bull Dip Jul 2024 | 2024 | $57,082 | 74.2 | 7.5 | 96.1 |
| Bull Dip Agt (Yen Carry) | 2024 | $58,174 | 74.9 | 5.8 | 96.0 |
| Bull Dip Sep 2024 | 2024 | $56,210 | 71.4 | 4.4 | 86.6 |
| Bull Dip Mar-Apr 2025 | 2025 | $86,294 | 78.1 | 21.1 | 100.0 |

**Signal fingerprint:** Total profit **60–93%** (spread 33pp), STH profit **4–79%** (spread 75pp), LTH profit 63–100% (spread 37pp). Ini adalah regime dengan range terlebar di dataset — supply metrics sangat tidak reliable sebagai standalone signal di sini.

**Leading/lagging:** Tidak ada pola leading yang konsisten untuk bull dips. Di sebagian events (terutama 2023), STH profit sudah rendah sebelum dip — tapi ini lebih mencerminkan posisi dalam cycle daripada early warning dari dip itu sendiri. Di Bull Dip Jan 2021, STH profit tetap tinggi (79%) bahkan saat dip — tidak ada tanda sebelumnya. LTH profit paling stable (11/15 tetap di atas 80% pada hari pertama event). Post-transition (90 hari): 12/15 events menunjukkan kenaikan harga yang meaningful setelah dip — konfirmasi retrospektif, bukan leading signal.

**Structural shift lintas cycle yang paling penting:**

**Pattern 2024:** Tiga bull dip di 2024 (Jul, Agt, Sep) punya STH profit single digits (4–8%) dengan LTH profit 86–96%. Gap ini ekstrem — hampir semua pembeli baru underwater, sementara LTH tetap deep in profit. Belum pernah terjadi di 2017 atau 2021 bull dips dengan magnitude seperti ini.

**2023 bull dips adalah outlier berbahaya:** Bull Dip Mar–Aug 2023 punya total profit 60–64% dan LTH profit 63–73% — range yang secara visual mirip bear bottom (40–48% dan 55–60%). Perbedaan kunci yang menyelamatkan dari salah identifikasi: LTH loss di 2023 dips = 27–37%, sedangkan di actual bear bottoms = 40–45%. Margin tipis yang sangat mudah diabaikan.

**Tabel komparasi langsung:**

| Metrik | Bear Bottom 2022 | Bull Dip Aug-Sep 2023 | Bull Dip Jul 2024 |
|--------|-----------------|----------------------|------------------|
| Total Profit | 44.5% | 60.0% | 74.2% |
| LTH Profit | 56.2% | 72.6% | 96.1% |
| LTH Loss | 43.8% | 25.8% | 3.9% |
| STH Loss | 100.0% | 90.1% | 92.5% |

**LTH loss adalah satu-satunya metrik yang secara reliable membedakan bear bottom dari bull dip — termasuk dari bull dip yang paling parah.**

**⚠️ Confidence note:** Bull Dip Jan 2021 punya total profit 93.2% — highest di semua bull dips. False sense of "this is not a dip" dari metrik ini sangat mungkin di sini.

---

### 1.5 MID-CYCLE CORRECTION
**2 events: May 2021 (start), Jun-Jul 2021 (bottom) — hanya 1 episode, 2 snapshots**

| Event | Price | Total Profit | STH Profit | LTH Profit |
|-------|-------|:---:|:---:|:---:|
| Mid-Cycle Start (May 2021) | $59,074 | 92.5 | 78.6 | 100.0 |
| Mid-Cycle Bottom (Jun-Jul 2021) | $32,517 | 70.9 | 10.6 | 97.2 |

**Signal behavior:** Dari start ke bottom dalam ~6 minggu: total profit turun 21.6pp, STH profit collapse 68pp (79% → 11%), LTH profit turun hanya 2.8pp (100% → 97.2%). Pola "STH wipeout dengan LTH hampir intact" — signature khas mid-cycle correction.

**Differentiator kritis dari bear market:** Pada titik nadir mid-cycle correction Juli 2021, STH loss mencapai 92–97% — nyaris identik dengan bear bottom 2018 dan 2022. Namun LTH loss hanya 2.8% vs 42–44% di actual bear bottoms. **LTH loss adalah satu-satunya pembeda yang reliable secara real-time.**

**Post-transition (dari Mid-Cycle Bottom, Jun 22 2021):**
- +30d: Total profit 66.4%, STH profit 3.1%, LTH profit 91.2% (STH masih sangat tertekan)
- +60d: Total profit 82.3%, STH profit 56.0%, LTH profit 91.6% (recovery STH mulai)
- +90d: Total profit 83.2%, STH profit 63.8%, LTH profit 89.5% (pasar kembali solid)

Recovery total profit dari 70.9% ke 83.2% dalam 90 hari — konsisten dengan "koreksi yang berhasil" bukan start of bear.

**⚠️ Masalah besar: Hanya 1 episode (2021).** Tidak ada basis yang cukup untuk generalize. Real-time, titik nadir mid-cycle 2021 terlihat MIRIP early bear market dari supply metrics saja. Konfirmasi dari MVRV dan LTH realized price diperlukan untuk diferensiasi yang lebih reliabel.

---

### 1.6 BEAR MARKET DECLINE
**7 snapshots dari raw data across 2018, 2019, 2022, 2025–2026**

*Berbeda dari regime lain — ini bukan event windows dengan label spesifik di data, melainkan snapshots dipilih di key moments dalam bear decline untuk menggambarkan sequence metrik.*

| Snapshot | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Bear Decline Start 2018 (Mar 6) | $10,849 | 76.7 | 46.7 | 100.0 | 53.3 | 0.0 |
| Bear Decline Mid 2018 (Jun 3) | $7,689 | 63.8 | 21.5 | 86.7 | 78.5 | 13.3 |
| Bear Decline Pre-Crash 2018 (Sep 15) | $6,389 | 57.9 | 26.8 | 68.0 | 73.2 | 32.0 |
| Bear Decline Post-Upper-Range 2019 (Jul 22) | $10,335 | 83.0 | 64.5 | 90.4 | 35.5 | 9.6 |
| Bear Decline Mid 2022 (Mar 27) | $46,829 | 81.1 | 70.8 | 84.2 | 29.2 | 15.8 |
| Bear Decline Start 2025 (Oct 23) | $110,138 | 83.5 | 31.7 | 100.0 | 68.3 | 0.0 |
| Bear Decline Mid 2026 (Jan 14) | $96,918 | 78.1 | 60.2 | 85.5 | 39.8 | 14.5 |

**Signal fingerprint:** Total profit 58–83% (median 78.1%), LTH profit 68–100% — masih elevated tapi declining secara gradual. LTH loss mulai naik dari 0% ke 30%+ seiring bear berlanjut.

**Feature kritis — sequence LTH profit dalam satu bear cycle (2018 sebagai reference):**

| Periode | LTH Profit | LTH Loss | Catatan |
|---------|-----------|---------|---------|
| Bear start (Mar 2018) | 100.0% | 0.0% | LTH masih aman penuh |
| Bear mid (Jun 2018) | 86.7% | 13.3% | LTH mulai terkena |
| Bear late (Sep 2018) | 68.0% | 32.0% | LTH dalam pain signifikan |
| Bear bottom (Des 2018) | 56.2% | 43.8% | Capitulation approach |

**LTH profit adalah lagging indicator di bear market** — tetap 100% di awal bear decline, memberikan false comfort sebelum akhirnya erode ke 55–60% di bottom.

**Sequence 2025–2026 yang sedang berjalan:**

| Periode | LTH Profit | LTH Loss | Total Profit |
|---------|-----------|---------|-------------|
| Bear start (Oct 2025) | 100.0% | 0.0% | 83.5% |
| Bear mid (Jan 2026) | 85.5% | 14.5% | 78.1% |
| Current (Jun 2026) | 60.6% | 39.4% | 53.9% |

Sequence ini konsisten dengan pola 2018. LTH loss di 39.4% (Juni 2026) sudah mendekati — tapi belum mencapai — historical bear bottom range (40–45%).

**Leading indicator pattern:** STH profit dan total profit adalah LEADING indicators di bear decline (bergerak lebih cepat dari LTH). STH profit sudah collapse jauh sebelum LTH profit bereaksi — terlihat jelas di semua 3 cycle bear declines.

**Post-Upper-Range 2019 outlier:** Bear Decline 2019 punya total profit 83.0% dan LTH profit 90.4% — jauh lebih tinggi dari bear declines lain. Ini karena 2019 "bear decline" setelah failed Upper Range terjadi dari level yang lebih tinggi dan LTH belum terakumulasi cukup losses. Bear decline mid-cycle bisa terlihat berbeda dari bear post-peak.

---

### 1.7 BEAR BOTTOM NEAR
**6 events across 2018, 2019, 2020, 2022**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Bear Bottom 2018 (Tier 1) | $3,441 | 40.2 | 0.0 | 56.3 | 100.0 | 43.7 |
| Bear Bottom Window End 2019 | $3,510 | 43.2 | 15.4 | 54.7 | 84.6 | 45.3 |
| COVID Flash Crash 2020 | $5,632 | 46.3 | 7.0 | 59.9 | 93.0 | 40.1 |
| Bear Bottom FTX 2022 | $18,550 | 46.2 | 0.5 | 57.7 | 99.5 | 42.3 |
| Bear Bottom Actual Low 2022 | $15,774 | 44.5 | 0.0 | 56.2 | 100.0 | 43.8 |
| Bear Bottom Final Low 2022 | $16,442 | 47.9 | 18.2 | 55.8 | 81.8 | 44.2 |

**Signal fingerprint:** Total profit **40–48%** (median 44.5%), STH profit **0–18%** (median 7.0%), LTH profit **55–60%** (median 56.2%), LTH loss **40–45%** (median 43.8%)

**Ini adalah regime dengan signal paling konsisten dari LTH metrics.** LTH profit di 54–60% dan LTH loss di 40–46% muncul berulang di true cycle bottoms. Bukan 0%, bukan 10% — selalu di kisaran yang sangat spesifik ini.

**Leading/lagging:** LTH profit dan LTH loss STABLE menjelang bottom (6/6) — tidak bergerak drastis di hari-hari sebelum event. LTH metrics naik secara gradual selama months sebelum bear bottom dan mencapai range 40–45% (LTH loss) saat bottom terjadi — ini lagging, bukan leading. STH loss LEADING — sudah spike ke 80–100% SEBELUM actual price bottom:
- 2018: STH loss sudah 97% pada −15 hari dari bottom Desember 2018, saat harga masih $3,872.
- 2022: STH loss sudah di 90–95% selama 2 bulan sebelum actual bottom (harga masih $19K).

Total profit LEADING — sudah turun ke range 48–55% sebelum mencapai absolute bottom (40–48%).

**Post-transition (90 hari setelah bear bottom):**
- 2018 (BB Tier 1 → +90d): Total profit 40.2% → 54.9% (+14.7pp). STH profit 0% → 55.6% (+55.6pp) — recovery sangat cepat.
- 2022 (Actual Low → +60d): Total profit 44.5% → 66.8% (+22.3pp). STH profit 0% → 92% (+92pp dalam 60 hari) — explosive recovery.

STH profit recovery yang sangat cepat setelah bear bottom adalah salah satu konfirmasi terkuat bahwa bottom sudah berlalu.

**Key differentiator dari mid-cycle correction:**

| Metrik | Mid-Cycle Bot 2021 | Bear Bottom 2018 | Bear Bottom 2022 |
|--------|--------------------|-----------------|-----------------|
| LTH Profit | 97.2% | 56.3% | 56.2% |
| LTH Loss | 2.8% | 43.7% | 43.8% |
| STH Loss | 92.3% | 100.0% | 99.5% |

STH loss hampir identik (~92–100%) di kedua scenarios. Satu-satunya differentiator yang reliable: LTH loss. Mid-cycle punya LTH loss 2.8%, bear bottom punya 43–44%.

**STH profit = 0.0%:** Terjadi 2 kali (Bear Bottom Tier 1 2018 dan Actual Low 2022). Ini absolute capitulation — SETIAP short-term holder underwater. Historis merupakan kondisi pembelian terbaik, tapi bisa bertahan beberapa minggu. Bukan signal untuk timing exact entry, tapi untuk zona akumulasi.

**⚠️ Confidence note:** Hanya 2 actual cycle bear bottoms (2018 dan 2022). COVID flash crash (2020) punya karakter berbeda — sangat cepat dan sebagian besar bukan organic bear market. Range LTH loss 40–46% berdasarkan 2 cycle — perlu validasi di cycle berikutnya.

---

### 1.8 PRE DETECTION START OF BULL MARKET
**3 events: 2019 (ref), 2019, 2023**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Pre Detection 2019 Ref | $3,943 | 55.9 | 58.7 | 54.8 | 41.3 | 45.2 |
| Pre Detection 2019 | $4,039 | 60.9 | 76.6 | 54.4 | 23.4 | 45.6 |
| Pre Detection 2023 | $17,444 | 58.5 | 67.6 | 56.1 | 32.4 | 43.9 |

**Signal fingerprint:** Total profit **56–61%**, STH profit **59–77%**, LTH profit **54–57%**, LTH loss **44–46%**

**Pattern yang sangat konsisten:** LTH profit di 54–57% (spread hanya 2.7pp) dan LTH loss di 43–46% (spread 2.3pp) — metrik tightest range di seluruh dataset. Pre-detection terjadi setelah bottom, di mana LTH belum cukup profit kembali.

**Key signature: STH profit SUDAH LEBIH TINGGI dari LTH profit.** Counter-intuitive — biasanya LTH lebih profitable karena beli lebih rendah. Tapi di pre-detection phase, LTH yang beli di puncak cycle sebelumnya masih underwater, sementara STH yang beli di bottom sudah profit karena harga naik dari low.

**Leading/lagging:** STH profit mengalami perubahan terbesar — naik dari sangat rendah (0–20%) di bear bottom ke 59–77% di pre-detection. Ini COINCIDENT dengan recovery price, bukan leading (3/3 coincident dengan price). LTH profit tidak bergerak dari bear bottom ke pre-detection (masih 54–57%, hampir identik dengan bear bottom level) — mengkonfirmasi bahwa LTH belum recover, hanya STH yang sudah profit. Total profit naik dari ~40–48% (bear bottom) ke 56–61% (pre-detection) — coincident.

**Post-transition (90 hari setelah pre-detection):**
- PD2019 (+90d): Total profit 88.3% (+27.4pp). STH profit 95.9% (+19.3pp). LTH profit 85.6% (+31.2pp). Massive recovery — price mencapai $8,993.
- PD2023 (+90d): Total profit 70.7% (+12.2pp). STH profit 77.4% (+9.8pp). LTH profit 68.7% (+12.6pp). Recovery lebih lambat dibanding 2019.

**Divergensi penting 2023 vs 2019:** Recovery 2023 lebih lambat karena LTH yang beli di 2021 ATH masih dalam pain jauh lebih lama. LTH loss di 2019 turun dari 45% ke 14% dalam 90 hari setelah pre-detection, sementara di 2023 turunnya lebih gradual.

---

### 1.9 START OF BULL MARKET CONFIRMATION
**2 events: 2019, 2023**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Start of Bull 2019 | $5,249 | 64.3 | 81.4 | 57.2 | 18.6 | 42.8 |
| Start of Bull 2023 | $21,632 | 64.5 | 75.1 | 61.6 | 24.9 | 38.4 |

**Signal fingerprint:** Total profit **64.3–64.5%** (spread hanya 0.2pp), STH profit **75–81%**, LTH profit **57–62%**, LTH loss **38–43%**

Dua data points dengan total profit yang nyaris identik adalah salah satu konsistensi paling striking dalam dataset ini. Caveat: hanya 2 data points, layak dijadikan referensi anchor, bukan hard rule.

**Transisi dari Pre Detection ke Start of Bull:** STH profit naik dari 59–77% (PD) ke 75–81% (SB) — kenaikan modest. LTH profit naik dari 54–56% (PD) ke 57–62% (SB) — mulai recovery tapi masih rendah. Total profit naik dari 56–61% (PD) ke ~64.5% (SB) — kenaikan ~5pp. LTH loss turun dari 44–46% (PD) ke 38–43% (SB) — LTH mulai mendapat relief.

**Post-transition:**
- SB2019 (+60d): Total profit 90.8% (+26.5pp), STH profit 95.3% (+13.9pp), LTH profit 89.2% (+32pp). LTH profit recovery sangat kuat — naik 32pp dalam 60 hari.
- SB2023 (+60d): Total profit 71.5% (+7pp), STH profit 80.3% (+5.2pp), LTH profit 68.9% (+7.3pp). Recovery jauh lebih lambat dari 2019.

**Post-transition anomali:** Di SB2023, 30 hari pertama setelah konfirmasi justru total profit turun sedikit (ke 58.1%) sebelum naik kembali — initial bull confirmation bukan linear, ada pullback.

**⚠️ Confidence note:** 2 data points saja. Gunakan sebagai referensi direction, bukan hard rule.

---

### 1.10 UPPER RANGE RECOVERY
**3 events: 2019 (Failed), Mar 2023, Jun-Jul 2023**

| Event | Price | Total Profit | STH Profit | LTH Profit | STH Loss | LTH Loss |
|-------|-------|:---:|:---:|:---:|:---:|:---:|
| Upper Range 2019 (Failed) | $12,830 | 95.4 | 100.0 | 93.6 | 0.0 | 6.4 |
| Upper Range Mar 2023 | $30,496 | 77.4 | 95.2 | 71.4 | 4.8 | 28.6 |
| Upper Range Jun-Jul 2023 | $30,547 | 77.4 | 93.0 | 73.5 | 7.0 | 26.5 |

**Outlier jelas: Upper Range 2019 (Failed)** punya profil sangat berbeda dari 2023 events — total profit 95.4% vs 77.4%, LTH profit 93.6% vs 71–74%. Gap sebesar ini bukan noise — mencerminkan perbedaan struktural: 2019 "upper range" terjadi setelah recovery sangat cepat dari $3.4K ke $12.8K (hampir 4x dalam 6 bulan), sehingga hampir semua supply sudah kembali profit. 2023 upper range terjadi setelah bear market lebih panjang, di mana banyak LTH dari 2021 masih underwater.

**2023 pattern (lebih representatif untuk multi-cycle):** STH profit 93–95% (sangat tinggi — pembeli baru dari bear bottom sudah profit besar), tapi LTH profit hanya 71–74% karena LTH dari cycle 2021 masih belum recover.

**Post-transition:**
- UR2019 (+90d): Total profit 75.5% (−19.9pp dari 95.4%). STH profit turun dari 100% ke 40.5%. Harga turun dari $12,830 ke $10,125 — konfirmasi "Failed" dari historical label.
- UR_Mar2023 (+30d): Total profit turun ke 64.7%, STH profit turun dari 95.2% ke 44.5%. Kemudian recovery ke $30.4K.

Upper Range Recovery diikuti volatilitas tinggi — STH profit bisa drop 50pp dalam 30 hari sebelum naik lagi. Ini mencerminkan distribusi dari pembeli awal yang ambil profit.

---

## SECTION 2: RULE RANGES — SIGNAL THRESHOLDS

### 2A. SELL SIGNALS

**Sell events analyzed:** Cycle Peak (3) + Local Top (6) + Lower High (4) = 13 events

#### Total Supply in Profit

| Threshold | Triggered | Hit Rate | Key False Signals | Notes |
|-----------|:---------:|:--------:|-------------------|-------|
| ≥97% | 8/13 (62%) | Semua benar (CP+LT) | — | Ketat, tapi tidak menangkap lower high sama sekali |
| ≥95% | 9/13 (69%) | Semua benar (CP+LT) | — | Sama coverage seperti ≥97% (gap bersih 96.7%→100.0% LT vs 88.1% LH tertinggi) |
| ≥90% | 9/13 (69%) | Sama seperti ≥95% | — | Lower high TIDAK ADA yang mencapai 90% — beda dari temuan versi data lama |
| ≥85% | 10/13 (77%) | 9 benar + 1 di Lower High 2025 Conf (88.1%) | Bull Dip Jan 2021 (93.2%) | 1 false signal — drawdown setelahnya tetap rally lanjutan, bukan top |
| ≥80% | 13/13 (100%) | Semua sell event tertangkap | 4 bull dips (Mar 2017, Sep 2017, Jan 2021, Mei 2024 — semua di 80-94%) | Terlalu longgar, tidak usable standalone |

**Rekomendasi:** ≥95% total profit sebagai alert kuat untuk Cycle Peak/Local Top — 0 false signal dari bull dip di level ini. Tapi tidak menangkap Lower High sama sekali (semua Lower High di 82–88%, di bawah threshold ini) — Lower High butuh sinyal lain (lihat STH profit di bawah).

#### STH Supply in Profit

| Threshold | Triggered | False Signal Risk |
|-----------|:---------:|-------------------|
| ≥95% | 4/13 (31%) | Sangat tight — hanya CP2025 dan 3 Local Top tertinggi |
| ≥90% | 7/13 (54%) | Masih 0 false signal dari bull dip |
| ≥85% | 9/13 (69%) | **0 false signal** — bull dip tertinggi (Jan 2021) di 79.2%, masih di bawah |
| ≥60% | 10/13 (77%) | Mulai menangkap Lower High 2018 (60.8%) |
| ≥50% | 11/13 (85%) | Tambah Lower High 2025 Conf (51.0%) |

**Rekomendasi:** STH profit ≥85% sebagai sell alert untuk Cycle Peak/Local Top — sangat reliable, gap bersih dari bull dip tertinggi (87.8% LT terendah vs 79.2% bull dip tertinggi). Untuk Lower High secara spesifik, gunakan threshold STH profit ≤60% DENGAN total profit masih >80% — kombinasi inilah signature khas lower high (lihat bagian gabungan di bawah).

#### Combined Sell Signal (RECOMMENDED)

**Total profit ≥95% AND STH profit ≥85% — untuk Cycle Peak/Local Top:**
- Triggered di: ketiga Cycle Peak + 5 dari 6 Local Top (Local Top Mar 2024 STH 88.2% masuk, semua lainnya juga masuk)
- 9/13 sell events (69% coverage)
- **0 false signal dari bull dip**
- Trade-off: tidak menangkap Lower High sama sekali — perlu sinyal terpisah untuk regime itu

**Total profit 80-88% AND STH profit ≤60% — untuk Lower High secara spesifik:**
- Triggered di: semua 4 Lower High events
- Ini adalah signature unik Lower High — total profit "masih terlihat sehat" sementara STH sudah collapse
- Tidak overlap dengan bull dip manapun di data (bull dip dengan total profit 80-88% punya STH profit jauh lebih tinggi)

---

### 2B. BUY SIGNALS

**Buy events analyzed:** Bear Bottom (6) + Bull Dip (15) + Pre Detection (3) + Start of Bull (2) = 26 events

#### Total Supply in Profit — Buy Thresholds

| Threshold | Triggered | Notes |
|-----------|:---------:|-------|
| ≤50% | 6/26 (23%) | Hanya bear bottom events — deep capitulation |
| ≤60% | 9/26 (35%) | Tambah 1 bull dip (Aug-Sep 2023, 60.0%) dan 2 Pre Detection |
| ≤65% | 14/26 (54%) | Lebih luas — termasuk beberapa bull dip lagi dan kedua Start of Bull |

**⚠️ Critical caveat:** Total profit ≤50% HANYA triggered di bear bottom events di data ini — tidak ada false signal dari regime lain. Tapi timing uncertainty besar: total profit bisa stay di bawah 50% berminggu-minggu sampai berbulan-bulan. Ini "accumulation window open," bukan "buy now."

#### STH Supply in Loss — Capitulation Buy Threshold

| Threshold | Triggered | Notes |
|-----------|:---------:|-------|
| ≥95% | 4/26 (15%) | Ultra-tight: bear bottom ekstrem + 1 bull dip ekstrem (Sep 2024, 95.6%) |
| ≥90% | 8/26 (31%) | Tambah bull dip Jul & Agt 2024 |
| ≥80% | 10/26 (38%) | Semua bear bottom + 4 bull dip ekstrem |

**Rekomendasi:** STH loss ≥90% sebagai strong buy signal — tapi sudah mulai overlap dengan bull dip ekstrem cycle 2024-2025 (lihat Section 1.4), jadi tidak bisa standalone, perlu dikombinasikan dengan total profit.

#### Combined Buy Signal (RECOMMENDED)

**Total profit ≤50% AND STH loss ≥90%:**
- Triggered di 4 dari 6 bear bottom (Bear Bottom 2018 Tier 1, COVID, FTX, Actual Low 2022 — Bear Bottom Window End 2019 dan Final Low 2022 tidak masuk karena STH loss-nya 84.6% dan 81.8%)
- **0 false signal dari bull dip** — kombinasi ini bersih
- Signals yang muncul adalah extreme capitulation — timing window masih uncertain tapi quality sangat tinggi

**Total profit ≤60% AND STH profit ≤15%:**
- Broader coverage
- Menambah beberapa bull dip ekstrem (Jul 2024, Agt 2024, Sep 2024) — perlu hati-hati karena ini area overlap dengan bear bottom signature

---

## SECTION 3: METRIC INTERACTIONS

### 3A. STH vs LTH Divergence — Pattern Utama

**Pattern 1: LTH profit tinggi, STH profit collapse (Gap >50pp)**

Ini adalah divergence pattern paling sering muncul — 13 instances di data. Interpretasinya BUKAN satu-arah:

| Outcome | Count | Events |
|---------|:-----:|--------|
| Followed by recovery (bull dip/mid-cycle) | 9/13 | Jul 2017 (+112%), Mid-Cycle Bottom 2021 (+88%), Sep 2024 (+85%), Aug 2024 (+53%), etc |
| Followed by continued decline (bear) | 2/13 | Bear Decline Start 2018 (-38%), Bear Decline Start 2025 (-34%) |
| Sideways | 2/13 | Halving 2024 (-0.1%), Mei 2024 (+16%) |

**Takeaway:** LTH high + STH low divergence sendiri BUKAN bearish atau bullish signal. Harus dikombinasikan dengan arah pergerakan LTH profit: jika LTH profit STABIL (tetap >95%), kemungkinan besar bull dip. Jika LTH profit MULAI TURUN, lebih mungkin bear transition.

**Pattern 2: Both STH dan LTH profit rendah (capitulation)**

| Event | LTH Profit | STH Profit | Total Profit |
|-------|:---:|:---:|:---:|
| Bear Bottom 2018 (Tier 1) | 56.3 | 0.0 | 40.2 |
| Bear Bottom Window End 2019 | 54.7 | 15.4 | 43.2 |
| COVID Flash Crash | 59.9 | 7.0 | 46.3 |
| FTX Collapse | 57.7 | 0.5 | 46.2 |
| Actual Price Low | 56.2 | 0.0 | 44.5 |
| Final Low 2022 | 55.8 | 18.2 | 47.9 |

**Semua 6 events followed by recovery** (lihat Section 1.7 untuk angka post-transition spesifik). LTH profit <60% + STH profit <20% = true capitulation territory. Hit rate 6/6, tapi durasi di bottom bervariasi — 2018 bottom berlangsung beberapa bulan, 2022 bottoming process juga ~6 minggu.

### 3B. Pre Detection Divergence — Signal Unik

Di fase Pre Detection, terjadi crossover di mana **STH profit > LTH profit:**

| Event | STH Profit | LTH Profit | Gap |
|-------|:---:|:---:|:---:|
| Pre Detection 2019 Ref | 58.7 | 54.8 | STH +3.9 |
| Pre Detection 2019 | 76.6 | 54.4 | STH +22.2 |
| Pre Detection 2023 | 67.6 | 56.1 | STH +11.5 |

**Ini terjadi karena STH (recent buyers di bottom) sudah profit sementara LTH (buyers dari cycle sebelumnya) masih underwater.** Pattern ini HANYA muncul di pre-detection phase — ini potential leading indicator yang unik.

### 3C. Concordance vs Divergence Summary

| Regime | STH-LTH Concordant | STH-LTH Divergent | Interpretation |
|--------|:------------------:|:------------------:|----------------|
| Start of Bull | 2/2 (100%) | 0/2 | Semua bergerak sejalan — broad-based recovery |
| Bull Dip | 9/15 (60%) | 6/15 | Mixed — divergence sering karena LTH stable sementara STH collapse |
| Bear Market Decline | 4/7 (57%) | 3/7 | Divergence terjadi di early bear (LTH stable, STH falling) |
| Bear Bottom Near | ~2/6 (33%)* | ~4/6 (67%)* | Dominan divergent — STH mulai recover sementara LTH masih turun |
| Pre Detection | 0/3 (0%) | 3/3 | Selalu divergent — STH naik, LTH masih turun/stable |
| Cycle Peak | 1/3 (33%) | 2/3 | LTH maxed out (stable), STH volatile |

*Bear Bottom Near sebelumnya dihitung atas 7 events (termasuk Bear Bottom 2019 Tier 2 yang sekarang dihapus dari dataset). Rasio di atas sudah disesuaikan ke 6 events, tapi proporsi exact butuh re-verifikasi karena klasifikasi concordant/divergent untuk event yang dihapus tidak diketahui.

**Takeaway:** Divergence pola STH naik + LTH turun/stable muncul di Bear Bottom → Pre Detection → Start of Bull sequence. Ini adalah recovery signature. Divergence pola STH turun + LTH stable muncul di Cycle Peak → Lower High → Bear Decline sequence. Ini adalah topping signature.

---

## SECTION 4: FAILURE MODES

### 4A. Total Supply in Profit — Kapan Gagal

**False sell signals (total profit tinggi tapi bukan top):**

| Event | Total Profit | Actual Regime | Notes |
|-------|:---:|-------------|---------------|
| Bull Dip Jan 2021 | 93.2 | Bull Dip | Satu-satunya bull dip yang menembus ≥90% total profit — diikuti rally lanjutan, bukan top. Massive missed upside kalau dijadikan sell trigger standalone |

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
| Bull Dip Agt 2024 | 5.8% | Bull Dip | Price dropped further -7% before recovering → temporary false bottom |

**Kenapa gagal:** STH profit bisa hit 0% di cascade liquidation event (FTX) sementara harga belum selesai turun. STH profit 0% menunjukkan semua recent buyers underwater, tapi BUKAN berarti semua selling pressure sudah habis — bisa ada forced liquidation dan panic selling lanjutan.

**STH noise level:** STH profit bisa bergerak 50+pp dalam seminggu. Di Jul 2017, STH profit bergerak dari 59% ke 39% dalam 5 hari, lalu kembali ke 91% dalam 3 hari setelahnya. Ini membuat daily readings unreliable — smoothing (7-day average) lebih berguna.

---

### 4C. LTH Supply in Profit — Kapan Gagal

**LTH profit memberikan FALSE COMFORT di early bear market:**

| Phase | LTH Profit | Price | Apa Yang Terjadi |
|-------|:---:|-------|------------------|
| Bear Start 2018 (Mar) | 100.0% | $10,849 | LTH semua masih profit → "everything is fine" |
| Bear Mid 2018 (Jun) | 86.7% | $7,689 | Baru mulai turun — sudah -29% dari start |
| Bear Late 2018 (Sep) | 68.0% | $6,389 | Pain signifikan, mendekati bottom |
| Bear Bottom 2018 (Des) | 56.3% | $3,441 | Capitulation zone |
| Bear Start 2025 (Okt) | 100.0% | $110,138 | Hampir identik — LTH all profit saat bear dimulai |
| Bear Mid 2026 (Jan) | 85.5% | $96,918 | LTH masih 86% profit, tapi sudah -12% dari start |
| Current (Jun 2026) | 60.6% | $66,076 | Mendekati — tapi belum mencapai — zona bear bottom (55-60%) |

**Ini adalah failure mode terpenting dari LTH profit:** Karena LTH membeli di harga jauh lebih rendah (seringkali 1-2 cycle sebelumnya), LTH profit tetap tinggi JAUH ke dalam bear market. Investor yang hanya melihat LTH profit >90% bisa merasa "aman" sementara harga sudah turun signifikan.

**LTH profit baru mulai memberikan sinyal meaningful (turun ke <60%) saat bear market sudah advanced — ini terlalu lambat untuk protective action.**

**Structural shift potensial untuk cycle berikutnya:** Cycle 2025-2026 menunjukkan LTH profit turun dari 100% ke 60.6% dalam ~8 bulan (Okt 2025 → Jun 2026), dibanding 2018 yang turun dari 100% ke 56.3% dalam ~9 bulan (Mar → Des 2018) — kecepatan yang cukup mirip, sedikit lebih cepat di cycle ini. Cross-check dengan MVRV dan SOPR diperlukan sebelum menyimpulkan apakah bear bottom zone (LTH loss 40-45%) akan tercapai dengan pola yang sama.

---

### 4D. Metric Reliability Ranking

Berdasarkan konsistensi range di dalam regime yang sama (lower = tighter range = more reliable). Ranking ini konsisten dengan pola yang terlihat di seluruh Section 1 (LTH profit/loss berulang kali disebut sebagai metrik dengan range paling tight per regime, STH paling lebar):

| Rank | Metric | Reliability | Verdict |
|:----:|--------|:------------------------:|---------|
| 1 | LTH Profit | **Tightest** | **Most reliable** — consistent ranges per regime |
| 2 | LTH Loss | Tightest | Mirror of LTH profit — same reliability |
| 3 | Total Profit | Moderate | Useful but overlapping ranges across regimes |
| 4 | Total Loss | Moderate | Mirror of total profit |
| 5 | STH Profit | **Widest** | **High variance** — ranges too wide for standalone use |
| 6 | STH Loss | Widest | Mirror of STH profit — same high variance |

**Implikasi untuk signal framework:** LTH metrics sebagai anchor/context (di mana kita dalam big picture), total metrics sebagai primary signal, STH metrics sebagai confirming/divergence indicator. Jangan pernah trade STH signals alone.

---

## SECTION 5: REGIME MAPPING — QUICK REFERENCE

### Decision Matrix

| Regime | Total Profit | STH Profit | LTH Profit | LTH Loss | Signal Paling Kuat |
|--------|:---:|:---:|:---:|:---:|:---:|
| **Cycle Peak** | 97–99% | 92–98% | 100% | 0% | LTH Profit = 100% + Total > 97% |
| **Local Top** | 97–100% | 88–100% | 100% | 0% | Identik dengan Cycle Peak — tidak bisa dibedakan |
| **Lower High** | 82–88% | 32–61% | 95–100% | 0–5% | STH Profit drop ke <65% dengan Total masih >80% |
| **Bull Dip** | 60–93% | 4–79% | 63–100% | 0–25% | LTH Profit > 80% = bukan bear bottom |
| **Mid-Cycle Correction** | 70–93% | 10–79% | 97–100% | 0–3% | LTH Loss < 5% saat STH Loss > 80% |
| **Bear Market Decline** | 58–83% | 22–71% | 68–100% | 0–32% | LTH Loss naik progresif 0% → 30%+ |
| **Bear Bottom Near** | 40–48% | 0–18% | 55–60% | 40–45% | LTH Loss ≥ 42% + Total < 48% |
| **Pre Detection** | 56–61% | 59–77% | 54–57% | 43–46% | STH Profit > LTH Profit (inverted) |
| **Start of Bull** | ~64% | 75–81% | 57–62% | 38–43% | Total Profit cross 64% dari bawah |
| **Upper Range Recovery** | 77–95% | 93–100% | 71–94% | 6–29% | STH Profit sangat tinggi, LTH Profit recovering |

### When to Give These Metrics HIGH Weight

- **Bear Bottom identification:** Total profit <48% + LTH loss ≥40% + STH profit <10% → strong accumulation signal
- **Pre Detection / Start of Bull:** STH profit > LTH profit → unique signal, very tight ranges
- **Lower High identification:** Total profit drop dari >95% ke 82-88% sementara STH profit collapse ke <61% — kombinasi inilah yang bersih, bukan total profit saja

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

## SECTION 6: CURRENT STATE ANALYSIS (Per 16 Juni 2026, $66,076)

| Metric | Current Value | Nearest Regime Match |
|--------|:---:|----------------------|
| Total Profit | 53.9% | Antara Bear Bottom Near (40-48%) dan Pre Detection (56-61%) |
| STH Profit | 21.9% | Bear Bottom range (0-18%) dengan slight upside |
| LTH Profit | 60.6% | Approaching bear bottom (55-60%) dari atas |
| STH Loss | 78.1% | Approaching bear bottom threshold (80-100%) |
| LTH Loss | 39.4% | Belum mencapai bear bottom range (40-45%) — gap 0.6pp |

**Semua metrik menunjukkan Bear Market Decline yang sudah sangat advanced, mendekati Bear Bottom Near zone.** LTH loss di 39.4% adalah yang paling kritikal untuk dipantau — jika mencapai 40%+, itu jadi sinyal bear bottom paling reliable berdasarkan historical data (lihat Section 1.7).

**⚠️ Perlu diverifikasi:** Apakah LTH loss akan mencapai 40-45% di cycle ini, atau ada structural shift (pertumbuhan ETF, institutional holders) yang mengubah range historis? Cross-check dengan MVRV dan SOPR diperlukan sebelum membuat kesimpulan final tentang proximity to bottom. Ini BUKAN call bahwa bottom dekat atau jauh — ini positioning information.

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
| Lower High signals | **MEDIUM** | 4 events, good consistency pada total profit |
| Bull Dip signals | **LOW** | 15 events tapi ranges terlalu lebar — unreliable standalone |
| STH-based signals overall | **LOW-MEDIUM** | High variance, best used as confirming indicator |
| Future cycle applicability | **UNCERTAIN** | ETF structural change, faster LTH maturation |
