# Short-Term Risk Score Session
*Tanggal: 4-5 Juli 2026*

---

## Latar Belakang

Menonton video YouTube "This Bitcoin Signal Has Nailed EVERY Dip" (On-Chain Mind, `dmxGLVVh3cc`) yang menampilkan 2 indikator custom:
1. **OCM Short-Term Risk Score** — komposit 8 faktor, oscillator 0-1.00, dengan zona high-risk (>70%) dan low-risk (<30%)
2. **OCM STH Accumulation Bands** — STH cost basis + standard deviation cloud (belum dikerjakan sesi ini)

Formula asli tidak diungkap (proprietary, dijual sebagai paid indicator suite). Sesi ini merekonstruksi indikator #1 dari definisi standar tiap metrik, lalu mengembangkan indikator kedua yang terpisah untuk deteksi V-shape correction.

---

## Bagian 1 — OCM Short-Term Risk Score (replikasi 8-faktor)

**Lokasi:** `dcm_short_term_risk_score/`

### 8 Komponen

| # | Komponen | Formula | Sumber data |
|---|----------|---------|-------------|
| 1 | Sharpe Ratio | rolling 30d mean/std log-return, annualized | `btc_price` |
| 2 | SSR (proxy) | `btc_price / stablecoin_supply_usd` | DefiLlama API (fetch baru) |
| 3 | MVRV Monthly Delta | `mvrv_ratio.diff(30)` | `mvrv_ratio` |
| 4 | STH-MVRV | langsung | `sth_mvrv` |
| 5 | SOPR Z-score | rolling 155d z-score dari `asopr` | `asopr` |
| 6 | Mayer Multiple | `btc_price / 200_dma` | `btc_price`, `200_dma` |
| 7 | Velocity RSI | RSI-14 dari 14d ROC harga (bukan RSI harga biasa) | `btc_price` |
| 8 | Microstructural Risk | blend 50/50: realized vol 14d + jarak absolut ke 200DMA (proxy ATR, karena tidak ada data OHLC) | `btc_price`, `200_dma` |

### Metodologi
- Normalisasi: **rolling percentile rank**, window 730 hari, min_periods 365
- Blend: **equal-weight** (12.5% tiap komponen) — bobot asli video tidak diketahui
- Smoothing: EMA-7
- Zona: >=70% HIGH_RISK, <=30% LOW_RISK

### Bug ditemukan & diperbaiki
`risk_raw` awalnya pakai `mean(skipna=False)` — satu komponen kosong (SSR, baru ada data dari Nov 2018 karena stablecoin supply historis baru mulai Nov 2017 + pemanasan window) bikin SELURUH skor sebelum itu jadi NaN, padahal 7 komponen lain sudah valid sejak **Jul 2011**. Fix: `skipna=True` + kolom `n_components` untuk transparansi. Coverage sekarang: 7-faktor dari 2011-07-16, 8-faktor penuh dari 2018-11-28.

### Uji sensitivitas (sebelum tuning bobot)
| Yang diuji | Hasil |
|---|---|
| SSR proxy vs SSR "asli" (pakai estimasi circulating supply BTC) | rank-correlation 0.9998 — negligible |
| Normalisasi percentile vs z-score+CDF | correlation 0.99, zone agreement 94.8% — moderate |
| Drop 1 komponen (microstructural) total dari blend | correlation 0.986, zone agreement 92.8% — moderate, dibatasi otomatis oleh bobot 1/8 |
| **Kesimpulan** | Skema bobot (equal vs performance-based asli video) adalah unknown terbesar yang belum diuji — prioritas #1 kalau mau tuning lanjut |

### Current state (data per 2026-07-02)
Risk Score **26.2%** (raw 35.6%) → **LOW_RISK zone**. Konsisten dengan status bear market di `CLAUDE.md` (S2 latch aktif sejak Nov 2025).

### Temuan visual histori penuh (2011-2026)
- Puncak Des 2017 (~$19k) tidak tercover (data mulai 2011-07, sebelum itu belum ada 7 komponen valid)
- Siklus 2021 double-top tertangkap paling jelas (2 puncak merah terpisah + dip hijau di antaranya, match dengan top Apr & Nov 2021)
- 2017 bull run: red band bertahan **hampir sepanjang tahun** (bukan cuma sesaat sebelum top) — extreme reading bisa bertahan berbulan-bulan, bukan sinyal timing presisi
- Green stretch Des 2025-sekarang adalah yang terpanjang/terdalam dibanding siklus manapun — beda karakter dari pullback sehat di uptrend (ini di tengah downtrend)

### Files
`fetch_stablecoin_supply.py`, `build_short_term_risk_score.py`, `chart_short_term_risk_score.py`, `check_vshape_metrics.py`, `chart_vshape_check.py`, `chart_velocity_microstructural.py`
`data_stablecoin_supply.csv`, `data_short_term_risk_score.csv`
`short_term_risk_score.png`, `price_vs_ssr.png`, `price_vs_mvrv_delta.png`, `price_vs_velocity_rsi.png`, `price_vs_microstructural.png`

---

## Bagian 2 — V-Shape Correction Detector (proyek terpisah)

**Lokasi:** `vshape_buy_score/`

**Tujuan:** deteksi koreksi tajam V-shape yang layak dibeli, berbeda dari Risk Score (yang mengukur siklus panjang). 6 tanggal referensi: 6-9 Mar 2023, 21 Jan 2024, 5 Sep 2020, 14-16 Jul 2017, 13-15 Sep 2017, 21 Sep 2021.

### Kandidat yang diuji dan ditolak
| Kandidat | Hasil | Verdict |
|---|---|---|
| SSR | 21 Jan 2024 nilainya 0.93 (percentile TERTINGGI, kebalikan ekspektasi) | ❌ tidak reliable, struktural (stablecoin supply stagnan pasca Terra/UST) |
| F&G Cadence 90D | cuma 2/4 tanggal (yang ada data) nunjukkin cadence negatif | ❌ window terlalu lambat untuk koreksi 3-9 hari |
| Fear & Greed (raw) | 2/6 ada data, tidak sampai extreme fear | ❌ lemah |
| Funding Rate flip negatif | cuma 1/4 tanggal hit | ❌ lemah |
| Exchange Net Flow | arah tidak konsisten | ❌ noise |
| RHODL Ratio | dirancang untuk siklus tahunan | ❌ salah timescale |
| STH-NUPL | 4/6 hit tapi redundant secara matematis dgn STH-MVRV | ❌ redundant |
| VDD Multiple | arah ambigu (top atau bottom) | ❌ tidak searah |
| **MVRV Monthly Delta** | 5/6 event di bawah percentile 15% | ✅ awalnya promising, akhirnya di-drop karena N-of-3 (3 metrik) sudah cukup solid tanpa dia |

### 4 metrik awal dari user → jadi 3 metrik final
1. ~~STH-SOPR & aSOPR terpisah~~ → digabung **MIN(aSOPR, STH-SOPR) <= 0.98** (solusi "kadang cuma salah satu spike": pakai OR/MIN, bukan pilih salah satu)
2. **STH % supply in loss >= 40%** — perlu filter tambahan (lihat bawah)
3. **RSI14 + Bollinger Bands(30, 1.5)** — breach lower band
4. ~~MVRV Monthly Delta~~ — di-drop, N-of-3 sudah solid tanpa ini

### Uji precision/recall (ground truth: drawdown >=8% dari puncak 10 hari trailing)
| Metrik | Fires | Precision | Recall |
|---|---|---|---|
| MIN(aSOPR,STH-SOPR)<=0.98 | 19.2% hari | 59.9% | 50.6% |
| STH%loss>=40% (raw, belum difilter) | **51.3% hari** | **33.2%** | 74.9% |
| RSI14+BB breach | 12.3% hari | 71.0% | 38.4% |

**STH%loss>=40% terlalu noisy** — nyala di separuh hari sejarah. Menaikkan threshold statis (sampai 70%) tidak banyak membantu (precision cuma 33%→45%, recall anjlok 74%→46%). **Fix yang berhasil: tambah filter rate-of-change** — `level>=40% AND naik>=10pt dalam 5 hari` → fires turun ke 14.9%, precision naik ke 52.8%, **tetap menangkap semua 6 tanggal referensi**.

### Skema final: N-of-3, threshold >=2-dari-3
| Threshold | Fires | Precision | Recall |
|---|---|---|---|
| >=1 dari 3 | 32.1% | 52.5% | 74.1% |
| **>=2 dari 3** | **11.4%** | **75.8%** | **38.0%** |
| >=3 dari 3 | 3.1% | 87.2% | 11.9% |

**>=2-dari-3 dipilih**: 322 episode terpisah (~22/tahun), precision 75.8%, dan **6/6 tanggal referensi tertangkap** (5 dari 6 malah capai penuh 3-dari-3, cuma Jan 2024 max di 2-dari-3), dengan toleransi ±2 hari.

### Percobaan yang GAGAL (dicoba, ditolak)
- **Composite kontinu (percentile rank, sama seperti Risk Score)**: 22.4% hari di BUY_ZONE, 164 episode — terlalu sering karena percentile rank secara matematis selalu menghasilkan ~30% hari di atas percentile ke-70, tidak otomatis menghasilkan kelangkaan
- **Persistence filter (2-5 hari)**: makin lama persistence, makin banyak tanggal referensi GAGAL ter-confirm (4/6→2/6) — V-shape correction itu tajam & singkat, bukan bertahan lama, jadi persistence memfilter arah yang salah

### Files
`build_vshape_buy_score.py`, `chart_vshape_buy_score.py`, `chart_metric_checks.py`
`data_vshape_buy_score.csv`
`vshape_buy_score.png`, `price_vs_sopr_signal.png`, `price_vs_sthloss_signal.png`, `price_vs_rsi_bb_signal.png`

### Status & next step
**Selesai (5 Juli 2026)** — `build_vshape_buy_score.py` sudah di-rebuild pakai skema final: 3 metrik boolean (c1_sopr, c2_sth_loss dengan filter rate-of-change, c3_rsi_bb), `confirm_count` 0-3, threshold `>=2-dari-3`. Re-run konfirmasi angka konsisten dengan validasi sebelumnya: fires 11.3% hari, precision 75.8%, recall 37.6%, 322 episode terpisah, rata-rata durasi 2.0 hari. 5/6 tanggal referensi hit persis di window; 21 Jan 2024 baru capai 2/3 di H+1 (22 Jan) — sesuai catatan toleransi ±2 hari, bukan bug.

`chart_vshape_buy_score.py` juga di-rebuild: panel bawah sekarang step-plot `confirm_count` (0-3) dengan garis threshold di 2, bukan skor kontinu smoothed. Output `vshape_buy_score.png` sudah ter-generate dan tervisualisasi dengan benar (density ~11% hari sesuai frekuensi terukur).

**Belum dikerjakan:** OCM STH Accumulation Bands (indikator ke-2 dari video sumber) — belum disentuh sama sekali di project ini.

---

## Bagian 3 — OCM STH Accumulation Bands (dikerjakan 5 Juli 2026, dikoreksi setelah nonton ulang video)

**Lokasi:** `sth_accumulation_bands/`

**Koreksi penting:** Branding channel/indikator yang benar adalah **"OCM"** (On-Chain Mind), bukan "DCM" — typo/mishearing yang terbawa dari sesi pertama (waktu itu belum benar-benar nonton videonya). Sudah dikoreksi di seluruh dokumen ini.

**v1 (build pertama) SALAH ARAH** — dibangun sebagai band simetris ±1sd/±2sd (ada zona DISTRIBUTION di atas cost basis). Setelah nonton ulang video (timestamp ~5:56-7:10, title on-screen "OCM STH Accumulation Bands"), ternyata strukturnya:
- Garis PUTIH (atas) = STH Cost Basis, jadi REFERENCE/TOP line
- Garis KUNING/EMAS = band pertama, di BAWAH cost basis
- Garis MERAH/PINK = band kedua, lebih jauh di bawah lagi
- Fill olive antara putih-kuning, fill maroon antara kuning-merah
- **TIDAK ADA band sama sekali di atas cost basis** — dicek langsung di frame Cycle Peak Okt 2025 (candle jauh di atas garis putih), tetap tidak ada shading atas. Ini murni buy-zone detector, bukan overbought/distribution tool, konsisten dengan narasi: "when we get down into the orange and red bands, that's where you find the best buying conditions" (tidak ada padanan kalimat untuk sisi atas).

**v2 (final) sudah di-rebuild one-sided** sesuai temuan ini.

### Metodologi (v2)
1. `ratio = btc_price / sth_cost_basis`, lalu `log_ratio = ln(ratio)`
2. Rolling std log_ratio, window 730 hari (2yr), min_periods 365 — window sama seperti OCM Risk Score
3. Band (bawah saja): `sth_cost_basis * exp(-k * rolling_std)`, k = 1, 2
4. Zona: NEUTRAL (price >= cost basis) → MILD_ACCUMULATION (di bawah cost basis, di atas -1sd) → DEEP_ACCUMULATION (di bawah -1sd, di atas -2sd) → EXTREME_ACCUMULATION (di bawah -2sd)

### Uji alternatif yang ditolak
**Expanding std (sejak inception) vs rolling 730d:** expanding std TERNYATA LEBIH BURUK — band jadi terlalu lebar karena ter-inflate volatilitas ekstrem 2011-2013. **Rolling 730d dipilih** (masih berlaku di v2, band width tidak berubah — cuma sisi atas yang dihapus).

### Validasi arah band v2 (sanity check, bukan precision/recall test)
| Event | Price/STH-RP | Semua NEUTRAL (cek: tidak ada band atas)? |
|---|---|---|
| Cycle Peak 2017 | max 2.19 | YES |
| Cycle Peak 2021 | max 1.43 | YES |
| Cycle Peak 2025 | max 1.10 | YES |

| Event | Min Price/STH-RP | Mild+ | Deep+ | Extreme |
|---|---|---|---|---|
| Bear Bottom 2018 | 0.64 | YES | YES | no |
| Bear Bottom 2022 (FTX) | 0.79 | YES | no | no |
| Bear Bottom 2022 (final low) | 0.90 | YES | no | no |
| COVID Flash Crash 2020 | 0.65 | YES | YES | YES |

**Temuan yang tetap berlaku dari v1:** Bear Bottom 2022 tidak sampai DEEP_ACCUMULATION (hanya MILD) — konsisten dengan temuan existing di [[project_onchain_dashboard]] (`realized_prices_knowledge_base.md`) soal Price/STH ratio yang COMPRESSING tiap cycle. Band makin lebar relatif terhadap ratio yang makin compressed di cycle 2022+, jadi makin sulit mencapai zona DEEP/EXTREME dibanding cycle 2017-2018.

### Frekuensi zona v2 (seluruh histori valid, 2011-2026)
NEUTRAL 58.0% | MILD_ACCUMULATION 29.9% | DEEP_ACCUMULATION 10.3% | EXTREME_ACCUMULATION 1.8%

### Current state (data per 2026-07-02)
Price $60,881 vs STH Cost Basis $69,197 (ratio 0.880) → zona **DEEP_ACCUMULATION** (di bawah -1sd $61,206, di atas -2sd $54,138). Konsisten dengan bear market status di CLAUDE.md.

### Files
`build_sth_accumulation_bands.py`, `chart_sth_accumulation_bands.py`
`data_sth_accumulation_bands.csv`, `sth_accumulation_bands.png`

### Status & next step
**Selesai dibangun, divalidasi arah, DAN dicocokkan visual terhadap video asli (v2).** Belum dilakukan: precision/recall test formal terhadap ground truth drawdown (seperti V-Shape Buy Score) — validasi sejauh ini masih sanity-check arah, bukan backtest kuantitatif. Kalau mau dipakai sebagai actionable trigger di `signal_framework_v1.md`, perlu uji lanjut dulu.

### Catatan metodologi umum
Video ini (dmxGLVVh3cc, 10:11) cuma nunjukin 2 indikator secara visual tanpa expose formula pasti — semua rekonstruksi di project ini (Risk Score 8-faktor, V-Shape Buy Score, Accumulation Bands) adalah interpretasi terbaik dari definisi standar on-chain metrics + sanity-check visual, BUKAN replikasi angka persis. Kalau ada keraguan soal kecocokan struktur visual/behavior di masa depan, cara paling reliable adalah nonton ulang segmen relevan pakai skill `/watch` daripada asumsi dari transkrip/memory saja.

---

## Data Sources
- `data_master_all_metrics.csv` — source utama (root), semua metrik on-chain + `btc_price`
- `data_stablecoin_supply.csv` — fetch baru dari DefiLlama (`dcm_short_term_risk_score/`)
- Ground truth "real correction" untuk precision/recall: `drawdown_10d = btc_price/rolling_max(10d) - 1 <= -8%`
