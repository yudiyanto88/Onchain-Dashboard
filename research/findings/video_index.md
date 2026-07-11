# Video & Research Index — Klaim yang Sudah Pernah Diuji

**Fungsi file ini:** memori antar-sesi. Sebelum menguji klaim dari video baru, cek dulu di sini — kalau klaim yang sama (atau mirip) sudah pernah diuji, pakai verdict lama, JANGAN tes ulang dari nol. Kalau mau menguji ulang dengan metodologi berbeda, sebutkan eksplisit kenapa hasil lama tidak cukup.

**Format verdict:**
- `ADD` — sudah masuk / layak masuk framework
- `REJECT` — diuji dan gagal, jangan dipakai
- `DICABUT` — sempat terlihat valid, lalu terbukti salah (mis. karena bias metodologi)
- `CONDITIONAL` — valid tapi dengan syarat/keterbatasan besar (baca findings-nya)
- `NEEDS-MORE-DATA` — belum bisa disimpulkan, tunggu data/cycle baru

---

## Seed — hasil riset internal sebelum sistem video breakdown ada

| Tanggal | Sumber | Klaim yang diuji | Verdict | File findings |
|---------|--------|------------------|---------|---------------|
| 2026-07-11 | Riset internal | NUPL/STH-NUPL sebagai tie-breaker K2 confidence scoring | **DICABUT** — separasi awal murni artefak lookahead bias; dengan nilai at-gate tidak ada separating power di bucket manapun | `k2_nupl_confidence_tiebreaker_findings.md` |
| 2026-07-10 | Riset internal | MVRV Z-score rolling 1Y divergence (price HH, Z LH) untuk K1 | **CONDITIONAL** — sisi TOP valid sebagai alat bantu visual K1 #1 (bukan syarat terpisah); sisi DIP jangan dipakai (efek rolling window). Sudah masuk KB MVRV v1.4 § Catatan Tambahan | `mvrv_zscore_rolling_divergence_k1_findings.md`, `mvrv_zscore_independence_check.md` |
| 2026-07-05 | Riset internal | STH Loss ≥50% + min(aSOPR,STH-SOPR) ≤0.98 sebagai K5 dip entry trigger | **CONDITIONAL** — valid di cycle 2022-2023 (2/2 positif) tapi tidak fire sama sekali di 2018-2019; n=2, hanya sebagai kandidat N-of-M, bukan gate tunggal | `k5_dip_entry_trigger_findings.md` |
| 2026-07-05 | Riset internal | Fear & Greed <50 (dan <45) di trough pullback sebagai K5 trigger | **CONDITIONAL** — 5/5 positif 30d tapi n=5, cuma 2 cycle (data F&G mulai 2018); pelengkap, bukan pengganti | `k5_fear_greed_trigger_findings.md` |
| 2026-07-05 | Riset internal | Funding rate ≤ −0.01 sebagai K5 trigger | **REJECT sebagai gate independen** — redundan dengan STH+SOPR, n=2, data cuma mulai 2020; maksimal supporting signal | `k5_funding_rate_findings.md` |
| 2026-07-05 | Riset internal | aSOPR Bollinger Band upper-touch di Z3 sebagai sinyal koreksi | **REJECT** — hit rate 20-33%, false rate 70-80% di semua 6 kombinasi | `asopr_bb_z3_findings.md` |
| 2026-07-05 | Riset internal | STH-SOPR BB upper-touch di Z3 | **REJECT sebagai standalone** — sedikit lebih baik dari aSOPR (32-36%) tapi tetap mayoritas false | `sth_sopr_bb_z3_findings.md` |
| 2026-07-05 | Riset internal | Price stretch dari STH RP sebagai sinyal koreksi K6 | **CONDITIONAL** — gradasi jelas (makin stretch makin besar peluang koreksi) tapi threshold absolut tidak konsisten antar cycle | `price_stretch_sth_rp_findings.md` |
| 2026-07-05 | Riset internal | STH-MVRV threshold sebagai proxy trigger K6 | **REJECT** — tidak bersih-monotonik, threshold tinggi didominasi data 2019 | `sth_mvrv_k6_trigger_findings.md` |
| 2026-07-05 | Riset internal | STH-MVRV higher-high divergence sebagai konfirmasi local high | **REJECT** — tidak menambah informasi vs price-based HH sendiri (n=20) | `local_high_sth_mvrv_divergence_findings.md` |
| 2026-07-05 | Riset internal | Kondisi K5 (F&G<50, STH Loss≥60%, SOPR≤0.98) fire saat bull dip Z4 = tanda breakdown | **CONDITIONAL (inverted signal)** — ≥1 kondisi fire di Z4 dip = 3/3 breakdown; 0/3 = hampir selalu recover. Berguna sebagai warning, bukan buy signal | `bull_dip_z4_conditions_findings.md` |
| 2026-07-05 | Riset internal | 3 kondisi capitulation sebagai genuine buy signal K2 di Z4 | **REJECT** — polanya terbalik: fire justru saat dip mau breakdown | `bull_dip_z4_k2_trigger_findings.md` |
| 2026-06-25 | Riset internal | SOPR SMA30 cross-down SMA365 sebagai deteksi bear onset | **CONDITIONAL** — confirming signal (telat 10-15 hari), bukan early warning; posisi: trigger tambahan PD1, dengan filter SMA30 ≤ 1.00 | `sopr_sma30_sma365_findings.md` |
| 2026-06-26 | Riset internal | SOPR peak divergence untuk S1/S2 | **ADD (proposal)** — direkomendasikan jadi two-stage alert system | `sopr_peak_divergence_findings.md` |

---

## Video yang sudah dibedah

*(diisi otomatis oleh `/video-breakdown` — satu baris per video)*

| Tanggal | Video | Klaim utama + verdict | File findings |
|---------|-------|----------------------|---------------|
