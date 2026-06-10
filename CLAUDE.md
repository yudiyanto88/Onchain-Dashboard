# CLAUDE.md — Bitcoin On-Chain Analysis Framework
## Briefing untuk setiap Claude Code session

---

## SIAPA KAMU BEKERJA DENGAN SIAPA

Kamu bekerja dengan Yudiyanto, Bitcoin investor retail Indonesia yang membangun on-chain analysis framework secara sistematis. Tujuan ganda: (1) framework analisis solid untuk keputusan investasi pribadi, (2) knowledge base untuk konten edukasi Instagram.

**Bukan developer, bukan data scientist.** Investor yang menggunakan AI sebagai tool untuk mempercepat analisis, bukan menggantikan judgment.

**Bahasa:** Mixed Indonesian-English. Technical terms tetap English (MVRV, SOPR, LTV, capitulation, dll). Penjelasan dalam Bahasa Indonesia casual. Pronoun: "aku" dan "kamu".

---

## INVESTMENT PHILOSOPHY & HARD CONSTRAINTS

- Lebih khawatir miss upside daripada drawdown
- Comfortable hold through declines selama LTV terkelola
- Bear market onset adalah primary risk yang harus dideteksi dini

**Hard constraints yang tidak boleh dilanggar:**

1. **LTV buffer override segalanya.** Kalau ada posisi loan aktif, cek LTV SEBELUM analisis apapun. LTV > 50% = de-risk immediately. LTV 40-50% = monitor daily. LTV < 40% = proceed normal.

2. **Oktober 2025 Rule.** Setiap analisis yang menyentuh leverage atau sizing WAJIB tanya: *"Kalau BTC turun 30% DAN worst-case kedua terjadi bersamaan, apa yang terjadi?"* Worst case kedua: altcoin crash, fiat income disruption, exchange freeze, regulatory shock. Kalau jawaban = liquidation → sizing terlalu besar.

3. **Loan hanya dengan multi-indicator confirmation.** Bukan single signal.

4. **No leverage sebelum Start of Bull Confirmation** (PD1 → SB1 upgrade, 4+ of 5 triggers). Sebelum itu: spot only.

5. **Short hanya sebagai hedge**, bukan main trade.

---

## DOKUMEN REFERENSI DI REPO INI

Semua dokumen berikut ada di folder ini. Baca yang relevan sebelum analisis:

| File | Isi |
|------|-----|
| `signal_framework_v1.md` | Framework utama v1.0.3 — routing, signals, risk overlay |
| `MVRV_Knowledge_Base.md` | MVRV Z-Score, LTH-MVRV, STH-MVRV — mekanik, thresholds, failure modes |
| `nupl_knowledge_base.md` | NUPL, LTH-NUPL, STH-NUPL |
| `sopr_knowledge_base.md` | aSOPR, LTH-SOPR, STH-SOPR, MA gap signals |
| `kb_realized_prices.md` | STH/LTH Realized Price, MVRV 0σ, Cum PL Price |
| `supply_in_profit_loss_knowledge_base.md` | Supply in Profit/Loss, STH/LTH profit % |

---

## SIGNAL FRAMEWORK SUMMARY (v1.0.3)

### Layer 1 — Routing

**Step 1:** Price vs STH Realized Price (sustained >80% hari dalam 30 hari terakhir)
- Price > STH RP → ZONA ATAS → cek Step 2A
- Price < STH RP → ZONA BAWAH → cek Step 2B

**Step 2A (Zona Atas) — Total Supply in Profit:**
- > 95% → ZONA MERAH (S1, S2, S3 aktif)
- 80–95% → ZONA KUNING ATAS (late-cycle checks, BD1)
- 65–80% → ZONA HIJAU (BD1 aktif)

**Step 2B (Zona Bawah) — Total Supply in Profit:**
- > 65% → ZONA KUNING BAWAH (BD1 + BT1, full confirmation required)
- 50–65% → ZONA BIRU (PD1, SB1 aktif)
- < 50% → ZONA HIJAU TUA (BB1 aktif)

### Layer 2 — Signals (N-of-M Confirmation)

| Signal | Zona | Triggers | Min Confirmation | Action |
|--------|------|----------|-----------------|--------|
| S1 | MERAH | 6 triggers (MVRV, NUPL, SOPR, RP, Supply, SOPR MA Gap) | 3/6 | Reduce exposure 20-30% |
| S2 | MERAH | 6 triggers (lower high confirm, bear latch) | 3/6 | Full de-risk, exit leverage |
| BB1 | HIJAU TUA | 5 triggers (MVRV < 1.0, NUPL negatif, aSOPR < 0.93, STH/LTH RP, Supply < 50%) | 3/5 | Accumulate spot aggressively |
| PD1 | BIRU | 5 triggers (STH-MVRV cross LTH, NUPL gap, SOPR State D, Price approaching STH RP, STH profit > LTH) | 3/5 | Scale in cautiously, spot only |
| BD1 | HIJAU/KUNING | 7 triggers (bull dip confirmation) | 4/7 | Re-entry after dip |
| BT1 | KUNING BAWAH | 5 triggers (bear transition confirmation) | 3/5 | De-risk, ambiguous zone |
| LC1 | Semua | Monitoring alert — tidak actionable sendiri | — | Flag untuk manual review |

**S2 Latch:** Aktif sejak November 2025. Bear market confirmed. Belum ada PD1/SB1 trigger untuk reset.

### Known Open Issues (perlu diselesaikan di v1.1)

1. **Hysteresis** — belum ada buffer rule di zona boundary 50% (HIJAU TUA vs BIRU). Oscillasi harian bisa cause zone-flipping.
2. **Signal-status labeling** — routing ke zona tertentu ≠ signal triggered. Harus explicit.
3. **Persistent state** — BD1 hard gate ("S2 belum trigger") tidak bisa diverifikasi tanpa state log lintas sesi.

---

## DATA FILES DI REPO

| File CSV | Isi Utama |
|----------|-----------|
| `data_mvrv.csv` | MVRV Z-Score, LTH-MVRV, STH-MVRV |
| `data_supply.csv` | Total Supply in Profit/Loss, STH/LTH profit % |
| `data_price_level.csv` | STH RP, LTH RP, MVRV 0σ, Cum PL Price |
| `data_fg.csv` | Fear & Greed Index |
| `data_cdd.csv` | CDD, VDD Multiple |
| `data_momentum.csv` | aSOPR, STH-SOPR, LTH-SOPR dan MA variants |
| `data_master_all_metrics.csv` | Gabungan semua metrics |

**Sebelum analisis:** jalankan `git pull` di terminal untuk pastikan data terbaru.

---

## CARA KERJA YANG DIHARAPKAN

**Saat diminta weekly analysis:**
1. Baca `signal_framework_v1.md` untuk konteks routing dan signal definitions
2. Baca CSV yang relevan (minimal: `data_supply.csv`, `data_mvrv.csv`, `data_price_level.csv`, `data_momentum.csv`)
3. Jalankan routing Layer 1 dulu, baru Layer 2
4. Output format: Zona → Per-signal trigger check (tabel) → Assessment → Action items
5. Flag semua uncertainty secara eksplisit
6. Probabilistic language selalu: "cenderung", "historically", "pattern ini suggest" — bukan "pasti" atau "akan"

**Yang tidak boleh dilakukan:**
- Timing call atau price prediction
- Confident tanpa data — kalau tidak yakin, bilang tidak yakin
- Ignore signal conflict — tunjukkan konfliknya, jangan pilih satu
- Skip LTV check kalau ada posisi leverage aktif

**Kalau sinyal konflik:** default = reduce exposure, bukan add. Tunggu clarity.

---

## CURRENT STATE (terakhir diupdate: Juni 2026)

- **S2 Latch:** AKTIF sejak November 2025
- **Zona terakhir:** ZONA BIRU (borderline HIJAU TUA — Supply in Profit ~49-62% range)
- **Regime:** Bear Market Decline, mid-to-late stage
- **BB1:** 0-1/5 triggers met (belum actionable)
- **PD1:** 0/5 triggers met
- **Confidence:** MEDIUM

Update section ini setiap kali weekly analysis selesai.

---

## CHANGELOG CLAUDE.md

- v1.0 (10 Juni 2026): Initial creation. Based on signal_framework_v1.0.3, 5 KB documents, project instructions.
