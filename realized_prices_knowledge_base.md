# Knowledge Base: Realized Price, STH Realized Price, LTH Realized Price

**Version:** 1.0
**Created:** 31 Mei 2026
**Data Source:** ChartInspect.com (Glassnode-sourced)
**Coverage:** Maret 2017 – Mei 2026 (3 full cycles: 2017, 2021, 2025)

---

## 1. DEFINISI & MEKANIK

### 1.1 Realized Price (RP)

**Apa yang diukur:** Rata-rata harga di mana seluruh supply Bitcoin terakhir kali bergerak on-chain, weighted by volume. Ini bukan harga pasar — ini "cost basis" agregat dari seluruh network.

**Analogi:** Bayangkan semua pemegang Bitcoin punya tiket masuk dengan harga beli masing-masing. Realized Price adalah rata-rata dari semua tiket itu. Kalau harga pasar di atas RP, secara agregat semua orang profit. Kalau di bawah, secara agregat semua orang rugi.

**Mekanik:**
- Setiap UTXO (koin) dinilai berdasarkan harga saat terakhir kali berpindah (on-chain transaction)
- Total value semua UTXO ÷ total supply = Realized Price
- Bergerak LAMBAT karena merupakan rata-rata dari jutaan koin dengan harga yang sangat beragam
- Hanya berubah kalau koin berpindah — koin yang diam di wallet tidak mengubah RP

**Karakteristik pergerakan dari data:**
- RP SELALU naik sepanjang bull market (new capital masuk di harga lebih tinggi)
- RP mulai FLAT atau sedikit turun di bear market (transfer terjadi di harga lebih rendah)
- RP adalah floor support yang sangat kuat di bear market — harga jarang lama-lama di bawah RP
- Rate of change RP jauh lebih lambat dari harga — ini lagging indicator by design

### 1.2 Short-Term Holder Realized Price (STH RP)

**Apa yang diukur:** Cost basis rata-rata dari koin yang dipegang < 155 hari (roughly 5 bulan). Ini mewakili harga rata-rata "new money" — orang yang baru beli.

**Analogi:** Kalau RP adalah rata-rata harga tiket SEMUA penonton di stadion, STH RP adalah rata-rata tiket orang yang baru beli dalam 5 bulan terakhir. Ini orang-orang yang paling sensitif terhadap pergerakan harga karena belum punya "buffer" unrealized profit yang besar.

**Mekanik:**
- Koin yang terakhir berpindah < 155 hari yang lalu
- Bergerak JAUH lebih cepat dari RP karena sample-nya berubah terus
- Sangat dipengaruhi oleh price action terbaru — kalau harga naik, STH RP naik (orang beli di harga tinggi)
- STH RP yang naik = ada demand baru masuk, tapi juga berarti cost basis baru lebih tinggi
- STH RP yang turun = demand berkurang, atau orang-orang yang beli mahal sudah sell/move

**Karakteristik pergerakan dari data:**
- STH RP naik CEPAT di rally karena banyak pembelian baru di harga tinggi
- STH RP turun di koreksi karena: (a) high-cost buyers sell at loss → keluar dari sample, (b) new buyers masuk di harga lebih rendah
- Di bear market lanjutan, STH RP turun tapi lebih lambat dari harga (always lagging)

### 1.3 Long-Term Holder Realized Price (LTH RP)

**Apa yang diukur:** Cost basis rata-rata dari koin yang dipegang > 155 hari. Ini mewakili "conviction holders" — orang yang sudah melewati setidaknya satu koreksi besar dan tetap hold.

**Analogi:** Ini harga tiket para penonton yang sudah ada di stadion dari pertandingan-pertandingan sebelumnya dan tidak pernah keluar. Cost basis mereka biasanya jauh lebih rendah karena mereka beli di cycle sebelumnya.

**Mekanik:**
- Koin yang terakhir berpindah > 155 hari yang lalu
- Bergerak SANGAT lambat — hanya berubah kalau: (a) koin "lulus" dari STH ke LTH (aging), (b) LTH menjual koin mereka
- Di bull market: LTH RP naik LAMBAT karena koin yang di-hold selama bull sebelumnya "aging in" dengan cost basis rendah
- Di bear market: LTH RP justru NAIK karena koin yang dibeli di harga tinggi selama bull market "aging" melewati 155 hari dan masuk kategori LTH
- Ini COUNTERINTUITIVE dan sangat penting: LTH RP naik di bear market bukan karena LTH beli lebih mahal, tapi karena high-cost-basis coins mature into LTH territory

---

## 2. HISTORICAL BEHAVIOR PER REGIME TRANSITION

### 2.1 CYCLE PEAK

**Events:** Cycle Peak 2017 (Dec 8-19), Cycle Peak 2021 Nov 8 (Oct 20-Nov 9), Cycle Peak 2025 (Oct 5-7)

**Metrik di Transition Point:**

| Cycle | Price | RP | STH RP | LTH RP | Price/RP | Price/STH | STH/LTH |
|-------|-------|----|--------|--------|----------|-----------|---------|
| 2017 | $16,690–$19,538 | $3,792–$4,664 | $7,612–$9,321 | $539–$551 | 3.90 | 1.95 | 15.62 |
| 2021 | $58,544–$67,525 | $22,589–$23,771 | $46,155–$51,011 | $15,836–$15,927 | 2.69 | 1.28 | 3.05 |
| 2025 | $121,430–$124,715 | $54,499–$54,759 | $113,430–$113,764 | $36,828–$36,828 | 2.28 | 1.10 | 3.09 |

**Pola Konsisten:**
- Price/RP di cycle peak: MENURUN tiap cycle (3.90 → 2.69 → 2.28). Ini diminishing returns — setiap cycle, harga tidak setinggi kelipatan dari cost basis agregat seperti cycle sebelumnya.
- Price/STH juga menurun (1.95 → 1.28 → 1.10). Ini sangat penting — di 2025, price nyaris tidak punya buffer di atas STH RP saat peak. New money hampir tidak profit saat peak.
- STH/RP ratio konsisten di sekitar 2.0 di semua cycle peaks (2.00, 2.11, 2.08). Ini mungkin structural constant.
- STH/LTH sangat tinggi di 2017 (15.62) karena LTH masih punya cost basis sangat rendah. Di 2021 dan 2025 sudah normalize ke ~3.0.

**Sebelum Peak (30 hari):**
- Price momentum bervariasi: +17.6% (2017), +44.6% (2021), +7.6% (2025)
- STH RP selalu naik tapi slower than price: +5.5%, +5.2%, +2.6%
- LTH RP barely moves: +1.3%, +10.1%, +0.4%
- RP naik steady: +5.3%, +5.8%, +2.4%
- **Pola kunci:** Price rally cepat sementara STH RP tidak bisa catch up. Semakin besar gap antara price momentum dan STH RP momentum, semakin unsustainable rally-nya.

**Sesudah Peak (30 hari):**
- Price drop: -16.5% (2017), -23.2% (2021), -10.3% (2025)
- STH RP masih naik di 2017 (+19.3%) dan 2021 (+1.5%), tapi sudah mulai turun di 2025 (-1.3%)
- LTH RP naik di semua cycle: +40.8%, +1.0%, +2.2% — karena high-cost coins mulai aging into LTH
- Price di atas STH RP: 97% (2017), 80% (2021), hanya 20% (2025). Trend ini sangat jelas — di cycle terbaru, price langsung breakdown di bawah STH RP setelah peak.

**Structural shift yang harus dicatat:** Di cycle 2025, margin of safety (Price/STH) di peak hanya 1.10 — artinya new money hampir tidak punya profit cushion. Ini membuat sell pressure lebih cepat terjadi karena new buyers turn underwater almost immediately. Ini berbeda fundamental dari 2017 dimana Price/STH masih 1.95 di peak.

### 2.2 LOCAL TOP

**Events:** Mar 2021, Apr 2021 ATH, Mar 2024 ATH, Des 2024 ATH, Jan 2025 ATH, Jul-Aug 2025 ATH

**Metrik di Transition Point (median values):**
- Price/RP median: 2.45
- Price/STH median: 1.16
- STH/LTH median: 3.05
- STH/RP median: 2.09

**Pola Konsisten:**
- Price/STH selalu > 1.0 di local top. Ini pembeda kunci dari cycle peak terbaru dan lower high — di local top, market MASIH punya buyer yang in-profit.
- Price/STH menurun di setiap successive local top: Mar 2021 (1.57) → Apr 2021 (1.43) → Mar 2024 (1.31) → Des 2024 (1.26) → Jan 2025 (1.15) → Jul-Aug 2025 (1.12). Degradasi ini adalah warning sign — setiap ATH baru semakin "tipis" margin-nya.
- STH RP naik lebih cepat dari LTH RP sebelum local top (STH catch-up rally), tapi price masih lead.
- Price above STH RP: 100% of days untuk semua local tops KECUALI Jan 2025 (83%) dan Jul-Aug 2025 (90%). Penurunan ini precursor ke cycle peak.

**Bagaimana membedakan Local Top vs Cycle Peak:**
- Local Top: Price/STH > 1.10, masih ada ruang. Setelahnya, price mungkin turun tapi recover.
- Cycle Peak / near-peak: Price/STH approach 1.0, hampir tidak ada ruang. Setelahnya, breakdown persistent.
- Dari data: ketika Price/STH turun dari 1.57 (Mar 2021) ke 1.12 (Jul-Aug 2025) secara progressif, ini signal bahwa cycle sedang matang. Setiap ATH berikutnya semakin "forced" dan kurang supported oleh actual buying power.

**Sebelum Local Top (30d):** Price momentum rata-rata +15-35%, STH RP catch-up +7-23%, LTH RP flat atau turun (LTH belum sell).

**Sesudah Local Top (30d):** Price bervariasi (-14.5% hingga +4.8%). Kalau price tetap di atas STH RP 100%, kemungkinan hanya local top dan masih ada upside. Kalau mulai ada breakdown (Jan 2025: 83%, Jul-Aug 2025: 90%), warning semakin kuat.

### 2.3 LOWER HIGH CONFIRM

**Events:** Lower High 2018 (Jan 1-8), Lower High 2019 (Aug 6-8), Lower High 2021 (Nov 30-Dec 2), Lower High 2025 (Oct 26-27), Lower High 2025 Confirmation (Oct 28)

**Metrik di Transition Point:**

| Event | Price/RP | Price/STH | STH/LTH | Price above STH 30d before | Price above STH 30d after |
|-------|----------|-----------|---------|---------------------------|--------------------------|
| 2018 | 3.30 | 1.62 | 15.97 | 100% | 62% |
| 2019 | 2.16 | 1.32 | 2.23 | 100% | 100% |
| 2021 | 2.33 | 1.07 | 3.34 | 100% | 3% |
| 2025 | 2.05 | 1.01 | 3.02 | 47% | 0% |
| 2025 Conf | 2.03 | 1.00 | 3.02 | 53% | 0% |

**Pola yang paling penting:**
- Price/STH di lower high MENURUN setiap cycle yang diobservasi: 1.62 → 1.32 → 1.07 → 1.01 → 1.00
- Di 2025, Price/STH = 1.00 di lower high confirmation — price literally touching STH RP. Ini berarti **semua new money at breakeven** saat lower high terbentuk.
- 30d setelah lower high: price above STH RP turun drastis. 2021: 3%. 2025: 0%.
- **Signal rule: kalau Price/STH turun ke ≤ 1.05 saat harga membentuk lower high setelah cycle peak, ini high-confidence bear confirmation.**
- Lower High 2019 adalah outlier: Price/STH masih 1.32, dan price tetap di atas STH RP 100% setelahnya. Tapi konteks berbeda — ini mini-cycle (Upper Range 2019 failed), bukan full cycle peak. Structurally distinct.

**Interaksi kunci:**
- STH RP sebelum lower high sudah mulai flat atau naik sangat lambat (+1.1% di 2025), sementara price turun (-2.0%). Ini compression — price coming down to meet STH RP.
- LTH RP mulai naik sedikit di semua lower high (+0.8% to +1.6% 30d before) — aging effect dimulai.

### 2.4 BULL DIP

**Events:** 15 instances across all cycles

**Ini regime dengan variasi terbesar.** Bull dips di data ini sangat heterogen — dari yang sangat ringan (Mar 2017) sampai yang parah (Mar-Apr 2025).

**Metrik summary:**
- Price/RP range: 1.02 – 3.44 (median 1.76)
- Price/STH range: 0.82 – 1.57 (median 0.99)
- STH/LTH range: 1.00 – 9.31 (median 2.10)

**Dua kategori bull dip yang SANGAT berbeda dalam data:**

**Tipe 1 — "Healthy Dip" (Price tetap di atas atau dekat STH RP):**
- Mar 2017: Price/STH = 1.05, recovery cepat
- Jul 2017: Price/STH = 1.08, recovery cepat
- Sep 2017: Price/STH = 1.28, strong recovery
- Jun 2020: Price/STH = 1.04, recovery +20% dalam 30d
- Jan 2021: Price/STH = 1.39, recovery +40% dalam 30d
- Mar 2023: Price/STH = 1.09, recovery +21% dalam 30d
- Jan 2024: Price/STH = 1.02, recovery +21% dalam 30d
- Ciri: Price above STH RP 100% of time, atau hanya touch briefly. Recovery cepat dan kuat.

**Tipe 2 — "Stressed Dip" (Price breakdown di bawah STH RP):**
- Sep 2020: Price/STH = 1.00 (borderline)
- Jun 2023: Price/STH = 0.98, semi-recovery
- Aug-Sep 2023: Price/STH = 0.92, sluggish recovery
- Mei 2024: Price/STH = 0.98, brief dip
- Jul 2024: Price/STH = 0.91, extended below STH
- Aug 2024 (Yen): Price/STH = 0.86, deepest bull dip
- Sep 2024: Price/STH = 0.87, persistent below STH
- Mar-Apr 2025: Price/STH = 0.93, extended below STH
- Ciri: Price di bawah STH RP untuk extended period. Recovery lebih lambat, dan kalau terjadi berturut-turut, ini warning bahwa cycle matang.

**Pola lintas cycle:**
- Early cycle bull dips cenderung Tipe 1 (healthy). Late cycle bull dips cenderung Tipe 2 (stressed).
- Di cycle 2024-2025: hampir semua bull dips adalah Tipe 2. Price di bawah STH RP becomes the norm, bukan exception. Ini red flag yang sangat jelas bahwa cycle sudah mature.
- **Rule: Ketika bull dips mulai konsisten di bawah STH RP (Price/STH < 1.0), cycle sedang memasuki fase akhir.** Dari data: di cycle 2024-2025, bull dips mulai breakdown sejak Mei 2024, dan ini confirmed saat Yen Carry Trade (Aug 2024) di mana Price/STH mencapai 0.86.

### 2.5 MID-CYCLE CORRECTION

**Events:** Mid-Cycle Correction Start (May 8, 2021), Mid-Cycle Correction Bottom (Jun 22-Jul 21, 2021)

**Hanya ada 1 sample.** Reliability statistik sangat rendah, tapi data tetap instructive.

**Metrik:**
- Start: Price/STH = 1.25, Price/RP = 2.95, STH/LTH = 8.72
- Bottom: Price/STH = 0.74 (minimum 0.67), Price/RP = 1.75, STH/LTH = 5.50

**Pola unik:**
- Price crash dari $59K ke $29K (-50%) sementara STH RP barely move ($47K → $44.7K). Ini karena crash terlalu cepat — STH RP lag.
- LTH RP melonjak dari $5,401 ke $9,385 (+74%) dalam 2 bulan. Ini paling dramatic di seluruh dataset — coins yang dibeli di $30K-$60K "aging" into LTH territory.
- STH/LTH masih tinggi (5.5 di bottom), sangat berbeda dari bear bottom (< 1.2). Ini salah satu cara membedakan mid-cycle correction dari actual bear market.

**Pembeda dari bear market:** Di mid-cycle correction, STH/LTH masih > 3.0 bahkan di bottom. Di bear bottom, STH/LTH converge ke < 1.2. Kalau STH/LTH masih tinggi saat price crash, kemungkinan ini correction, bukan regime change.

### 2.6 BEAR MARKET DECLINE

**Events:** Bear Decline Start 2018, Bear Decline Mid 2018, Bear Decline Low 2018, Bear Decline Mid 2019, Bear Market Decline Mid 2022, Bear Decline Start 2025, Bear Market Decline Mid 2026

**Metrik summary:**
- Price/RP median: 1.83
- Price/STH median: 0.99
- STH/LTH median: 2.56

**Pola konsisten:**
- Price di bawah STH RP di hampir semua bear decline points (price above STH RP: 0-23% of time sebelum dan sesudah).
- LTH RP NAIK di semua bear markets sementara price turun. Data bear periods:
  - Bear 2018: Price -78.7%, LTH RP +539.5%, STH RP -53.3%
  - Bear 2021-22: Price -76.4%, LTH RP +29.7%, STH RP -62.7%
  - Bear 2025-26 (ongoing): Price -36.1%, LTH RP +32.0%, STH RP -31.4%
- STH/LTH ratio compresses aggressively: 15.71 → 1.15 (2018), 3.20 → 0.92 (2021-22), 3.09 → 1.61 (2025-26, masih ongoing)
- STH RP momentum turns negative early in bear decline — ini lagging tapi confirming signal.

**Struktural shift 2025-26:** LTH RP masih naik (+32%) meskipun price "hanya" turun -36% (vs -78% di 2018). Convergence STH/LTH belum selesai di Mei 2026 (masih 1.61), suggesting bear market bisa masih ongoing.

### 2.7 BEAR BOTTOM NEAR

**Events:** Bear Bottom 2018 Tier 1 (Dec 11-17), Bear Bottom Window End (Jan 30-Feb 6, 2019), Bear Bottom 2019 Tier 2 (Nov 25-Dec 18), COVID Flash Crash (Mar 13-17, 2020), Bear Bottom FTX (Nov 8, 2022), Bear Bottom Actual Price Low (Nov 21, 2022), Bear Bottom Final Low (Dec 19, 2022)

**Metrik summary:**
- Price/RP median: 1.26 — banyak yang di bawah 1.0 (harga di bawah aggregate cost basis)
- Price/STH median: 0.80 — STH holders deep underwater
- STH/LTH median: 1.96

**Pola paling kuat — Convergence:**

STH/LTH converges ke < 1.0 di KEDUA major bear bottoms:
- Bear Bottom 2018-2019: STH/LTH terendah = 0.890 (period Dec 2018 – Apr 2019)
- Bear Bottom 2022-2023: STH/LTH terendah = 0.880 (period Oct 2022 – Apr 2023)

Ketika STH/LTH < 1.0, artinya: cost basis short-term holders LEBIH RENDAH dari cost basis long-term holders. Ini terjadi karena LTH membawa "bagasi" pembelian mahal dari bull cycle, sementara STH yang baru masuk sudah membeli di harga bear market yang rendah. Ini ultimate capitulation indicator — old money rugi lebih besar dari new money.

**Price/RP di bottoms:**
- Bear Bottom 2018 Tier 1: Price/RP = 0.70 (harga 30% di bawah aggregate cost basis)
- Bear Bottom Window End: Price/RP = 0.78
- Bear Bottom Actual Price Low 2022: Price/RP = 0.78
- Bear Bottom Final Low 2022: Price/RP = 0.82
- COVID Flash Crash: Price/RP = 0.96 (almost at RP, karena crash sangat cepat)

**Rule range: Price/RP < 0.85 historically = accumulation zone.** Tapi caveat besar: pada 2019 Tier 2, Price/RP = 1.21 (masih di ATAS RP) — bottom bisa terjadi di atas RP di cycle non-traditional.

**Depth below STH RP di bottoms:**
- Deepest: Bear Bottom 2018 Tier 1 = Price/STH 0.637 (36% di bawah STH RP)
- COVID Flash: Price/STH 0.649
- Mid-Cycle Correction 2021: Price/STH 0.666 (tapi ini bukan bear bottom, ini correction)
- FTX Collapse: Price/STH 0.897 (relatively shallow)
- Bear Bottom Final Low 2022: Price/STH 0.896

### 2.8 PRE DETECTION START OF BULL MARKET

**Events:** Pre Detection 2019 Ref (Feb 22), Pre Detection 2019 (Mar 21-26), Pre Detection 2023 (Jan 10-12)

**Metrik summary:**
- Price/RP median: 0.91
- Price/STH median: 0.98
- STH/LTH median: 0.90

**Pola paling kuat:**
- Price masih di bawah RP (Price/RP 0.88–0.96) — market secara agregat masih rugi
- Price mulai mendekati STH RP dari bawah (Price/STH 0.93–1.05)
- STH/LTH masih < 1.0 — convergence masih aktif
- STH/RP < 1.0 — STH cost basis masih di bawah aggregate cost basis
- **Yang membedakan ini dari bear bottom: price trend sudah mulai stabilize/naik meskipun semua metric masih "bearish".** Ini fase di mana momentum berubah tapi metrics belum confirm.
- Price crosses ABOVE STH RP terjadi di sekitar pre-detection: Mar 20, 2019 dan Jan 11, 2023. Ini salah satu early signal paling reliable.

### 2.9 START OF BULL MARKET CONFIRMATION

**Events:** Start of Bull 2019 (Apr 25), Start of Bull 2023 (Feb 10-12)

**Metrik summary:**
- Price/RP: 1.10–1.19
- Price/STH: 1.12–1.23
- STH/LTH: 0.95–0.97

**Pola confirmation:**
- Price sudah CLEAR di atas STH RP (Price/STH > 1.10) — new money in profit
- Price sudah di atas RP (Price/RP > 1.0) — market overall profit
- STH/LTH masih < 1.0 — menunjukkan ini masih EARLY, bukan late cycle
- Price above STH RP: 93-100% of days sebelum confirmation
- Setelah confirmation, price bisa choppy (-3.8% 30d after Start of Bull 2023) tapi tetap di atas STH RP

**Kunci:** STH/LTH < 1.0 + Price > STH RP + Price > RP = bull confirmed but still early. Ini zona dimana leverage mulai masuk akal menurut strategy table.

### 2.10 UPPER RANGE RECOVERY

**Events:** Upper Range 2019 Failed (Jun 26), Upper Range Mar 2023 (Apr 14-17), Upper Range Jun-Jul 2023 (Jun 24-Jul 17)

**Perhatian: Upper Range 2019 (Failed) membuktikan bahwa upper range bisa GAGAL.** Price naik ke $12,830 (Price/RP 2.55, Price/STH 1.74), tapi ini ternyata local top yang kemudian membentuk lower high dan decline. STH/LTH masih rendah (1.77) menunjukkan ini early cycle move yang overextended.

**Metrik summary:**
- Price/RP: 1.47–2.55
- Price/STH: 1.07–1.74
- STH/LTH: 1.22–1.77

Upper Range 2023 events lebih sehat — STH/LTH sekitar 1.2–1.5, Price/STH 1.08–1.32. Masih early enough bahwa ada upside.

---

## 3. RULE RANGES — SELL SIGNALS

### 3.1 RULE: Price/STH Degradation Across Successive ATHs

**Premise:** Di setiap ATH berturut-turut dalam satu cycle, Price/STH ratio turun progressively. Ketika ratio ini turun ke < 1.15, cycle top semakin dekat.

**Data evidence:**

| ATH Event | Price/STH | What Happened After |
|-----------|-----------|---------------------|
| Mar 2021 ATH | 1.57 | +$2K more upside (Apr ATH), lalu correction |
| Apr 2021 ATH | 1.43 | Mid-cycle correction -50% |
| Mar 2024 ATH | 1.31 | Consolidation, dips, kemudian continuation |
| Des 2024 ATH | 1.26 | Another ATH (Jan 2025), tapi marginal |
| Jan 2025 ATH | 1.15 | Drawdown -25%, recovery, lalu final peak |
| Jul-Aug 2025 ATH | 1.12 | Cycle Peak dalam 2 bulan |

**Threshold proposed: Price/STH < 1.15 saat ATH = mulai reduce exposure.**

- Hit rate: 3/3 (Jan 2025 → peak dalam 3 bulan, Jul-Aug 2025 → peak dalam 2 bulan, Apr 2021 → mid-cycle crash)
- False signal: Belum ada yang pure false, tapi Apr 2021 di 1.43 ternyata masih punya Nov 2021 ATH setelahnya. Jadi threshold 1.15 lebih conservative dan specific.
- Cost of being wrong: Kalau sell terlalu early di 1.15, maximum upside missed (dari Jan 2025 ATH $106K ke Jul-Aug 2025 ATH $123K) = ~16%. Manageable.
- Cycle variation: Hanya applicable di cycle dimana multiple ATHs terjadi. Single-peak cycles (2017) tidak memberikan kesempatan ini.

**Caveat penting:** Threshold 1.15 based pada 2 data points (2021 dan 2024-25). Sample terlalu kecil untuk high confidence. Gunakan sebagai alert, bukan trigger otomatis.

### 3.2 RULE: Price Breakdown Below STH RP di Late Cycle

**Premise:** Ketika price mulai konsisten trade di bawah STH RP (Price/STH < 1.0 untuk majority of days), cycle sedang berakhir.

**Data evidence:**

| Period | Price above STH RP (% days) | What Happened |
|--------|----------------------------|---------------|
| Late 2024 (Jul-Sep) bull dips | 10-47% | Masih recovery ke ATH Des 2024 |
| Mar-Apr 2025 bull dip | 47-63% | Recovery ke Jul-Aug ATH |
| Aug-Sep 2025 (post Jul-Aug ATH) | 50% range | Cycle Peak Oct 2025, lalu bear |
| Oct 2025 Lower High | 47% before, 0% after | Confirmed bear start |

**Threshold proposed: Ketika price above STH RP turun ke < 50% secara sustained (>2 minggu), ini late-cycle warning. Kalau turun ke 0%, bear confirmed.**

- Hit rate: 2/2 major cycles (2021: Lower High Desember 2021, price above STH RP turun ke 3%. 2025: Lower High Oktober 2025, turun ke 0%)
- False signal: 2024 bull dips (Jul-Sep) juga showed < 50%, tapi market recovered. Ini false signal kalau dibaca sebagai "bear start" — tapi accurate kalau dibaca sebagai "late cycle."
- Cost of being wrong: Sell di pertama kali price consistently below STH RP (Jul 2024, ~$57K) → price masih naik ke $124K. Cost: 117% upside missed. VERY EXPENSIVE jika digunakan sebagai standalone signal.
- **Implikasi: Ini bukan sell signal sendiri. Ini context signal — memberi tahu bahwa cycle sudah mature, dan sizing/leverage harus dikurangi progressively.**

### 3.3 RULE: Price/RP Cycle Peak Range

**Premise:** Historically, cycle peaks terjadi saat Price/RP di atas range tertentu.

**Data evidence:**
- 2017 peak: Price/RP = 3.90–4.39
- 2021 peak: Price/RP = 2.69–2.99
- 2025 peak: Price/RP = 2.22–2.28

**Trend: Peak Price/RP menurun setiap cycle.** Tapi decline rate juga berkurang (1.21 gap 2017→2021, 0.41 gap 2021→2025).

**Threshold proposed: Price/RP > 2.20 = heightened risk zone di cycle 2025+.**

- Hit rate: 3/3 cycle peaks (semua di atas 2.20)
- False signal: Local tops juga bisa mencapai Price/RP > 2.20 (Mar 2024 ATH = 2.73, Des 2024 ATH = 2.63). Jadi ini not specific enough — ada false positives.
- Perbaikan: Combine dengan Price/STH < 1.15 di ATH untuk filter. Kalau Price/RP > 2.20 DAN Price/STH < 1.15 saat ATH, confidence lebih tinggi.

### 3.4 RULE: Lower High Confirmation via Price/STH ≤ 1.05

**Premise:** Kalau setelah cycle peak, harga membentuk lower high dan Price/STH ≤ 1.05 pada saat itu, bear market confirmed.

**Data evidence:**
- Lower High 2021: Price/STH = 1.07 → 30d after, price above STH hanya 3%. Bear confirmed.
- Lower High 2025: Price/STH = 1.01 → 30d after, price above STH = 0%. Bear confirmed.
- Lower High 2025 Confirmation: Price/STH = 1.00 → immediate bear.
- Lower High 2018: Price/STH = 1.62 → masih tinggi, tapi konteks berbeda (2017 had much higher Price/STH overall)
- Lower High 2019: Price/STH = 1.32 → ini mini-cycle, different context

**Hit rate (post-2020 cycles):** 2/2
**False signal:** None detected dalam recent cycles
**Cost of being wrong:** Kalau Price/STH ≤ 1.05 saat lower high tapi market recovers → aku perlu cari data di mana ini terjadi. Dari dataset, ini belum pernah terjadi di major cycle.

**Confidence: TINGGI untuk recent cycles (post-2020).** Kalau combined dengan falling Price/STH across ATHs, ini salah satu signal paling reliable untuk bear confirmation.

---

## 4. RULE RANGES — BUY SIGNALS

### 4.1 RULE: STH/LTH Convergence < 1.0 = Accumulation Zone

**Premise:** Ketika STH/LTH turun di bawah 1.0, ini historically bottom territory.

**Data evidence:**
- 2018-2019: STH/LTH < 1.0 dari ~Jan 2019 sampai ~Apr 2019. Minimum 0.890. Price dari ~$3,500 ke ~$5,200 selama period. Start of Bull confirmed Apr 25, 2019.
- 2022-2023: STH/LTH < 1.0 dari ~Oct 2022 sampai ~Apr 2023. Minimum 0.880. Price dari ~$19,000 ke ~$29,000 selama period. Start of Bull confirmed Feb 10-12, 2023.

**Hit rate:** 2/2 major bear cycles
**Duration:** 3-6 bulan di zona convergence sebelum bull confirmed
**Price/RP selama convergence:** Rata-rata 0.91 (2019) dan 1.04 (2022-23). Perhatikan: di 2022-23, Price/RP tidak pernah turun se-rendah 2018-19. Cycle evolution.

**Threshold proposed: STH/LTH < 1.2 = mulai accumulate. STH/LTH < 1.0 = aggressive accumulate.**

- False signal: Tidak ada dalam dataset. Setiap kali STH/LTH < 1.0, bottom sudah terjadi atau sedang terjadi.
- Cost of being wrong: Kalau buy saat STH/LTH < 1.0 tapi price masih turun 10-20% — dari data, maximum additional drawdown setelah STH/LTH crosses below 1.0 relatif terbatas. Di 2018-19, price drop lanjutan ~7% setelah convergence (dari $3,500 ke $3,280). Di 2022-23, price sudah rally saat STH/LTH < 1.0 tercapai.
- **Ini salah satu signal paling reliable di dataset untuk buying.**

### 4.2 RULE: Price/RP < 1.0 = Aggregate Market Underwater

**Premise:** Ketika Price turun di bawah Realized Price, seluruh network secara rata-rata dalam kerugian. Ini historically rare dan powerful buy signal.

**Data evidence:**
- 2018-2019: Price/RP < 1.0 dari ~Nov 2018 sampai ~Apr 2019. Minimum 0.70.
- 2022-2023: Price/RP < 1.0 dari ~Jun 2022 sampai ~Jan 2023. Minimum 0.78.
- COVID 2020: Price/RP briefly dip ke 0.91-0.96 (hanya beberapa hari).

**Hit rate:** 3/3 instances preceded major recoveries
**Duration:** 5-7 bulan di kedua major bear cycles

**Threshold proposed: Price/RP < 1.0 = accumulation window. Price/RP < 0.85 = aggressive accumulation.**

- False signal: Tidak ada dalam dataset. Price never stays below RP for extended time dan selalu recover.
- Cost of being wrong: Bisa turun lebih lanjut setelah Price/RP drops below 1.0 (2018: dari 1.0 ke 0.70 = additional 30% drawdown). Ini DCA territory, bukan lump sum.
- **Catatan kritis untuk bear 2025-26:** Per Mei 2026, Price/RP masih ~1.3 (berdasarkan data terakhir: price $78K, RP ~$55K). Belum mencapai < 1.0. Kalau bear berlanjut, ada potensi turun lebih jauh sebelum mencapai true accumulation zone.

### 4.3 RULE: Price Reclaims STH RP dari Bawah = Early Bull Signal

**Premise:** Ketika price crosses di atas STH RP setelah extended period di bawah, ini often signals regime shift.

**Data evidence — key crossovers:**
- Apr 26, 2020 (Price $7,677 > STH $7,562): Setelah COVID crash. Bull market followed.
- Sep 24, 2020 (Price $10,736 > STH $10,397): After Sep 2020 dip. Massive bull run followed.
- Aug 7, 2021 (Price $44,595 > STH $44,262): After mid-cycle correction. Recovery ke ATH.
- Jan 11, 2023 (Price $17,938 > STH $17,829): Pre-detection. Bull confirmed within 1 month.
- Oct 28, 2024 (Price $69,931 > STH $63,702): Strong breakout. Rally to ATH Des 2024.

**Hit rate:** 5/5 dari major crossovers above → led to significant upside
**False signal:** Beberapa minor crossovers yang didn't lead to sustained move (2020 Jan-Feb: multiple crosses back and forth). But major ones (after extended period below) were reliable.
**Filtering rule:** Only count crossovers after price has been below STH RP for > 14 days consistently.

### 4.4 RULE: Healthy Bull Dip — Price/STH > 1.0

**Premise:** Bull dips where Price remains above STH RP are buying opportunities.

**Data evidence (all dips where Price/STH > 1.0 at low):**
- Mar 2017 (1.05): Recovery ✓
- Jul 2017 (1.08): Recovery ✓
- Sep 2017 (1.28): Recovery ✓
- Jun 2020 (1.04): Recovery +20% in 30d ✓
- Jan 2021 (1.39): Recovery +40% in 30d ✓
- Sep 2020 (1.00 borderline): Recovery +16% ✓
- Mar 2023 (1.09): Recovery +21% ✓
- Jan 2024 (1.02): Recovery +21% ✓

**Hit rate:** 8/8 — every bull dip where Price stayed above STH RP recovered within 30 days.

**Contrast with bull dips where Price/STH < 1.0:**
- Jun 2023 (0.98): Partial recovery ✓ (still worked, but slower)
- Aug-Sep 2023 (0.92): Sluggish, choppy recovery
- Jul 2024 (0.91): Extended consolidation
- Aug 2024 Yen (0.86): Eventually recovered, but volatile
- Sep 2024 (0.87): Slow recovery
- Mar-Apr 2025 (0.93): Recovery, tapi cycle peaked within 6 months

**Conclusion:** Price/STH > 1.0 dips have 100% hit rate for quick recovery. Price/STH < 1.0 dips also recovered but with lower certainty, slower speed, and often signaled late cycle.

---

## 5. INTERAKSI ANTAR KETIGA METRIK

### 5.1 Kapan Ketiga Metrik Sejalan

**Semua bullish (Price > STH RP > RP, all rising):**
- Terjadi di: Early-to-mid bull market (2023 Mar-Dec, 2024 Jan-Mar, 2017 Apr-Nov, 2020 Oct-2021 Mar)
- Artinya: Momentum kuat, new money masuk dan profitable, old money hold. Buy dips aggressively.

**Semua bearish (Price < STH RP, STH RP declining, LTH RP rising, RP flat/declining):**
- Terjadi di: Bear market (2018 Mar-Dec, 2022 May-Dec, 2025 Nov-2026)
- Artinya: New money underwater dan leaving. Old money absorbing high-cost coins via aging. Avoid leverage.

### 5.2 Divergences Paling Penting

**Divergence 1: STH RP naik tapi Price turun (atau flat) — LATE CYCLE WARNING**
Ini terjadi ketika:
- Rally terjadi → STH RP catch up
- Kemudian price retrace, tapi STH RP masih elevated karena lag
- Hasil: Price breakdown di bawah STH RP

Contoh: Jul-Sep 2024. STH RP stayed at $62K-$65K sementara price berkali-kali turun ke $54K-$58K. STH RP "sticky" di level tinggi karena banyak orang beli di rally, tapi harga tidak sustain. Ini pattern yang berulang di late cycle.

**Divergence 2: LTH RP naik sementara Price turun — BEAR MARKET SIGNATURE**
Ini pola paling consistent di seluruh dataset:
- 2018: Price -78.7%, LTH RP +539.5%
- 2021-22: Price -76.4%, LTH RP +29.7%
- 2025-26: Price -36.1%, LTH RP +32.0%

Mekanik: Koin yang dibeli di harga tinggi selama bull "mature" melewati 155 hari. Koin-koin ini membawa cost basis tinggi ke LTH pool, menaikkan rata-rata LTH RP. Ini bukan karena LTH membeli mahal — ini aging effect.

**Divergence 3: STH/LTH compressing sementara Price flat — BOTTOM FORMING**
Ketika STH/LTH mendekati 1.0 dan price sudah berhenti turun, ini signal paling kuat bahwa capitulation selesai.
- 2019 (Feb-Mar): STH/LTH = 0.90-0.94, price flat di $3,500-$4,000. Bottom formed.
- 2023 (Jan-Feb): STH/LTH = 0.88-0.92, price stabilizing $16K-$18K. Bottom formed.

**Divergence 4: Price > STH RP tapi STH/LTH masih < 1.0 — BULL CONFIRMED EARLY**
Ini yang terjadi di Start of Bull:
- Apr 2019: Price/STH = 1.23, tapi STH/LTH = 0.95. Price sudah breakout tapi structure masih bottom-like.
- Feb 2023: Price/STH = 1.13, STH/LTH = 0.97. Same pattern.
- Artinya: "Early bird" signal. Cycle baru dimulai tapi belum banyak yang notice.

### 5.3 Kombinasi Signal Paling Reliable Per Regime

| Regime | Primary Signal | Secondary Confirmation | Confidence |
|--------|---------------|----------------------|------------|
| Cycle Peak | Price/STH < 1.15 saat ATH + degrading across ATHs | Price/RP > 2.20 | Medium-High |
| Lower High Confirm | Price/STH ≤ 1.05 saat lower high | Price above STH < 50% | High (recent) |
| Bear Bottom | STH/LTH < 1.0 | Price/RP < 1.0 | High |
| Start of Bull | Price > STH RP sustained + STH/LTH < 1.0 | Price/RP > 1.0 | High |
| Healthy Bull Dip | Price/STH > 1.0 di low | STH RP still rising | High |
| Late Cycle Bull Dip | Price/STH < 1.0 persistent | STH RP momentum negative | Medium |

### 5.4 Divergences Paling Berbahaya Kalau Diabaikan

1. **Price/STH degradasi across successive ATHs yang diabaikan = missed cycle peak.** Dari 1.57 ke 1.12 di cycle 2021-2025. Kalau seseorang hanya fokus di ATH price tanpa monitor Price/STH, mereka tidak akan lihat warning.

2. **Persistent price below STH RP di bull market yang diabaikan = caught in bear transition.** Jul-Sep 2024 bull dips sudah menunjukkan Price/STH < 0.90, tapi market masih rally ke ATH Des 2024. Ini bisa membuat orang complacent — "pernah below STH RP dan recover, pasti recover lagi." Sampai akhirnya tidak recover.

3. **LTH RP rising + STH/LTH compressing yang diabaikan saat hold position = late realization bear sudah dimulai.** LTH RP rise 30+ hari setelah peak menandakan coin aging masif terjadi — ini confirming indicator, bukan leading.

---

## 6. FAILURE MODES

### 6.1 Realized Price (RP) — Failure Modes

**RP sebagai support gagal di extreme events:**
- COVID March 2020: Price crashed dari $8K ke $5.1K, menembus RP ($5,661). Tapi recovery sangat cepat (within 40 days). RP "support" failed temporarily di flash crash.
- 2018 bear: Price di bawah RP selama ~5 bulan. RP bukan inviolable floor — bisa ditembus dan stay below.

**RP terlalu lambat untuk timing:**
- RP bergerak sangat lambat, sehingga threshold-based signals (Price/RP > 2.0 = overheated) bisa trigger terlalu early dan stay triggered for months. Dari Mar 2024 (Price/RP = 2.73) sampai Oct 2025 (Price/RP = 2.28), selalu di atas 2.0 selama 19 bulan. Ini terlalu lama untuk actionable sell signal.

**RP bisa misleading di structural shifts:**
- Kalau ada massive institutional adoption (ETF inflows, corporate treasury), RP bisa naik JAUH lebih cepat dari biasanya, membuat historical thresholds tidak berlaku. Ini sudah terlihat: RP naik dari $20K (Jan 2023) ke $55K (Oct 2025) — 175% dalam 33 bulan. Jika RP acceleration berlanjut, Price/RP peak mungkin semakin rendah di cycle berikutnya (di bawah 2.0?).

### 6.2 STH Realized Price (STH RP) — Failure Modes

**STH RP misleading di low-volume, drifting markets:**
- Ketika volume rendah, STH RP bisa tetap "stuck" di level tinggi meskipun market sudah weak. Contoh: Jul-Sep 2024, STH RP di $62K-$65K sementara price turun ke $54K. STH RP tidak turun karena few transactions terjadi di harga rendah — mostly holders tidak bergerak.
- Ini membuat Price/STH terlihat sangat bearish padahal sebenarnya market hanya low-activity, bukan actively selling.

**STH RP whipsaw di volatile periods:**
- Selama COVID crash, Price/STH turun ke 0.59 — extreme reading. Tapi ini karena crash terjadi sangat cepat sementara STH RP masih di level pre-crash. Dalam 40 hari price sudah kembali di atas STH RP. Signal bearish dari Price/STH yang extreme itu misleading jika diambil at face value.

**STH definition bisa berubah:**
- 155-day threshold adalah arbitrary. Glassnode bisa mengubahnya. Kalau threshold berubah, semua historical analysis berubah.

**Cycle ini STH RP converge lebih cepat:**
- Di 2017, Price/STH bisa mencapai 2.15 di peak. Di 2025, hanya 1.10. Structural compression ini mungkin terus berlanjut, membuat threshold yang effective di cycle ini irrelevant di cycle berikutnya.

### 6.3 LTH Realized Price (LTH RP) — Failure Modes

**LTH RP SANGAT lagging:**
- LTH RP baru mulai naik signifikan 2-3 bulan SETELAH peak. Ini zero value sebagai leading indicator untuk peak detection.
- Berguna hanya sebagai confirmation: "apakah bear market sudah dimulai?" Ya, kalau LTH RP sudah naik 20%+ sementara price turun.

**Magnitude LTH RP move diminishing:**
- 2018: LTH RP naik +539% selama bear. Ini karena starting point sangat rendah ($671).
- 2021-22: LTH RP naik +30%.
- 2025-26: LTH RP naik +32% so far.
- Di cycle mendatang, persentase perubahan LTH RP di bear mungkin semakin kecil karena starting point semakin tinggi.

**LTH RP bisa misleading kalau exchange holdings berubah:**
- Kalau exchange memegang banyak koin lama (cold storage), coins ini masuk LTH tapi bukan "conviction holders." LTH RP bisa distorted oleh exchange holdings.

### 6.4 Metrik yang Paling Sering Gagal

**STH RP paling sering memberikan false signal.** Dari data:
- Price crosses below STH RP terjadi 50+ kali dalam dataset. Banyak di antaranya bukan regime change tapi temporary crosses.
- Di bull market 2024-2025, Price/STH < 1.0 terjadi berkali-kali (Jul 2024, Aug 2024, Sep 2024, Mar-Apr 2025) — setiap kali bisa dibaca sebagai "bear signal" tapi ternyata masih bull dip.
- **Standalone, Price below STH RP BUKAN reliable bear signal.** Harus dikombinasikan dengan durasi (>14 hari sustained), trend (successive dips semakin deep), dan konfirmasi dari metric lain.

**RP paling jarang gagal** tapi juga paling tidak berguna untuk timing karena terlalu lambat.

**LTH RP tidak pernah "gagal" — tapi juga tidak pernah berguna sebagai trading signal karena terlalu lagging.** Nilai utamanya adalah structural confirmation.

---

## 7. MAPPING KE REGIME CATEGORIES

### Decision Tree

```
STEP 1: Cek Price vs STH RP
├── Price > STH RP (secara sustained, >80% hari dalam 30 hari terakhir)
│   ├── STEP 2a: Cek Price/STH level
│   │   ├── Price/STH > 1.30 → Likely EARLY-MID BULL (healthy territory)
│   │   ├── Price/STH 1.10-1.30 → MID-LATE BULL atau LOCAL TOP territory
│   │   │   └── Cek: apakah Price/STH degrading across successive ATHs?
│   │   │       ├── Ya → Late cycle, reduce exposure progressively
│   │   │       └── Tidak → Masih healthy
│   │   └── Price/STH 1.00-1.10 → DANGER ZONE
│   │       └── Cek: is this an ATH or post-ATH lower high?
│   │           ├── ATH dengan Price/STH < 1.15 → CYCLE PEAK WARNING
│   │           └── Lower high dengan Price/STH < 1.05 → BEAR CONFIRMED
│   └── STEP 2b: Cek STH/LTH
│       ├── STH/LTH < 1.0 → Very early bull (START OF BULL territory)
│       ├── STH/LTH 1.0-2.0 → Early-mid bull (UPPER RANGE RECOVERY)
│       ├── STH/LTH 2.0-3.0 → Mid bull (normal bull territory)
│       └── STH/LTH > 3.0 → Extended bull (heightened risk)
│
└── Price < STH RP (secara sustained)
    ├── STEP 2c: How deep?
    │   ├── Price/STH 0.95-1.00 → BULL DIP atau EARLY BEAR
    │   │   └── Cek durasi: < 14 hari → likely bull dip. > 30 hari → bear transition
    │   ├── Price/STH 0.85-0.95 → BEAR DECLINE atau DEEP BULL DIP
    │   │   └── Cek STH/LTH: > 2.0 → could still be late bull dip. < 2.0 → bear
    │   ├── Price/STH 0.70-0.85 → BEAR BOTTOM NEAR territory
    │   │   └── Cek Price/RP: < 1.0 → strong accumulation zone
    │   └── Price/STH < 0.70 → EXTREME CAPITULATION (rare, flash crash)
    │
    └── STEP 2d: Cek STH/LTH
        ├── STH/LTH < 1.0 → BEAR BOTTOM (accumulation zone)
        ├── STH/LTH 1.0-1.5 → Bear bottom forming atau PRE DETECTION
        │   └── Cek: is Price/STH approaching 1.0 from below?
        │       ├── Ya → PRE DETECTION / START OF BULL imminent
        │       └── Tidak → Still in bear
        └── STH/LTH > 1.5 → BEAR DECLINE (masih jauh dari bottom)
```

### Weight Guidelines

**Beri weight TINGGI pada ketiga metrik ini ketika:**
- Sedang menentukan apakah ini bull dip atau bear transition (Price vs STH RP relationship kritis)
- Sedang menentukan apakah bear bottom sudah terjadi (STH/LTH convergence)
- Monitoring cycle maturity (Price/STH degradation across ATHs)
- Confirming regime change (Price reclaim/break STH RP setelah extended period di sisi lain)

**Beri weight RENDAH ketika:**
- Timing intraday atau intraweek moves (semua terlalu lagging)
- Mengukur severity of correction saat terjadi (RP-based metrics lag, gunakan price-level support/resistance)
- Market didominasi oleh extreme external events (COVID, regulatory shock) — flash crashes make STH RP signals temporarily useless
- Volume sangat rendah (summer doldrums, holiday periods) — STH RP bisa stuck dan misleading

### Red Flags yang Harus Trigger Immediate Attention

1. **Price/STH < 1.05 saat membentuk lower high setelah peak** → Drop everything, assess bear positioning
2. **STH/LTH compression accelerating (turun >0.3 dalam 2 bulan)** → Bear market underway, reduce exposure
3. **Price crosses below STH RP dan STAYS below >14 hari setelah period sustained above** → Regime change probable
4. **LTH RP naik >15% dalam 3 bulan sementara price turun** → Bear market confirmed structurally
5. **Price/RP approaching 1.0 dari atas** → Either deep correction or bear market. Jika combined dengan STH/LTH < 1.5, likely bear.

---

## 8. APA YANG BISA MEMBUAT THRESHOLD HISTORIS TIDAK BERLAKU

### 8.1 Structural Factors

1. **ETF Inflows mengubah demand structure.** ETF buyers tidak create UTXO movements yang sama seperti retail on-chain. Ini bisa membuat STH/LTH dynamics berubah karena ETF coins mungkin "diam" di custodian tanpa on-chain movement.

2. **Diminishing Price/STH spread di peak.** Dari 1.95 (2017) ke 1.10 (2025). Kalau trend berlanjut, cycle berikutnya mungkin peak dengan Price/STH < 1.05, making the metric less useful karena margin terlalu tipis.

3. **RP acceleration.** RP naik dari $500 (2017) ke $55,000 (2025). Kalau institutional adoption semakin besar, RP bisa naik sangat cepat sehingga Price/RP peak levels semakin rendah (mungkin < 2.0 di cycle berikutnya).

4. **Changing holder behavior.** Kalau STH holders become more "diamond hands" (hold meskipun underwater), STH RP behavior di corrections bisa berubah.

### 8.2 Yang Relatif Stabil

1. **STH/RP ratio di cycle peak:** Konsisten ~2.0 di semua cycles (2.00, 2.11, 2.08). Ini mungkin structural karena mencerminkan hubungan fundamental antara new money cost basis dan aggregate cost basis.

2. **STH/LTH < 1.0 sebagai bear bottom signal:** Terjadi di kedua major cycles. Mechanics-nya (aging effect) tidak berubah kecuali definisi 155 hari berubah.

3. **LTH RP rises in bear markets:** Selama definisi LTH tetap time-based, ini akan terus terjadi karena mekaniknya immutable.

---

## 9. STATUS BEAR 2025-2026 (SNAPSHOT MEI 2026)

**Berdasarkan data terakhir dalam CSV (sekitar Mei 2026):**
- Estimated Price: ~$78K
- Estimated STH RP: ~$78K (Price/STH ≈ 1.0)
- Estimated LTH RP: ~$49K
- Estimated RP: ~$54K
- STH/LTH: ~1.6

**Assessment:**
- Price/RP ≈ 1.4 → Masih di ATAS RP. Belum mencapai accumulation zone (Price/RP < 1.0).
- STH/LTH = 1.6 → Masih di ATAS convergence zone (< 1.2). Bear bottom belum terbentuk berdasarkan historical pattern.
- Price ≈ STH RP → Price sekitar breakeven untuk STH. Belum deep capitulation.
- LTH RP masih naik (dari $37K di Oct 2025 ke ~$49K) → Bear market aging effect masih ongoing.

**Implikasi untuk strategy table:** Data menunjukkan ini **Bear Market Decline** — bukan Bear Bottom Near. STH/LTH perlu compress lebih ke < 1.2 (dan idealnya < 1.0) untuk signal bottom. Price/RP perlu turun lebih dekat ke 1.0 (idealnya di bawah). Ini konsisten dengan "phase 7: Bear Market Decline" di regime categories.

**Caveat:** Ini cycle pertama dengan ETF dynamics. Historical convergence levels mungkin tidak berlaku identik. Tapi sampai ada evidence baru, default ke historical framework.


