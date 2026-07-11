# Data Dictionary — Peta Kolom Semua File CSV

Dibuat: 2026-07-11. Sumber data: ChartInspect.com (Glassnode-sourced), di-update harian oleh `auto_update.py`.

**Cara pakai:** sebelum menguji klaim apapun, cek di sini dulu — datanya ada atau nggak, di file mana, nama kolomnya apa. Kalau kolom tidak ada di sini, klaim itu `NEEDS-DATA-WE-DONT-HAVE`.

**File paling praktis:** `data_master_all_metrics.csv` (105 kolom, 2009-01-03 s/d sekarang) — gabungan semua metrik dalam satu file. Untuk analisis, biasanya cukup load file ini saja.

**Catatan file `*_events.csv`:** versi dari file yang sama plus kolom `event` (label kejadian historis). Tidak selalu ter-update sampai hari ini — cek tanggal terakhirnya sebelum dipakai.

---

## Ketersediaan data (rentang tanggal)

| File | Mulai | Terakhir | Catatan |
|------|-------|----------|---------|
| `data_master_all_metrics.csv` | 2009-01-03 | update harian | Gabungan semua. Kolom yang mulai lebih lambat berisi kosong di awal |
| `data_derivatives.csv` | **2020-02-28** | update harian | Funding rate & OI baru ada 1.5 siklus — sample kecil! |
| `data_fg.csv` | **2018-02-01** | update harian | Fear & Greed baru ada 2 siklus |
| `data_exchange.csv` | 2010-07-16 | ⚠️ cek — kadang telat update | Exchange flow |
| Sisanya | 2010-07-17 atau 2009-01-03 | update harian | Full history |

**Aturan rigor:** metrik yang datanya baru mulai 2018/2020 TIDAK bisa diuji lintas semua siklus. Wajib disebutkan di findings kalau pakai metrik ini.

---

## Harga & Level On-chain (batas zona framework)

File: `data_price_level.csv` / master. Ini kolom-kolom yang menentukan zona Z1–Z5.

| Kolom | Artinya |
|-------|---------|
| `btc_price` | Harga BTC harian (close) |
| `sth_cost_basis` | **STH RP** — rata-rata harga beli holder < 155 hari. Batas Z1 |
| `lth_cost_basis` | **LTH RP** — rata-rata harga beli holder > 155 hari |
| `realized_price` | **RP** — rata-rata harga beli semua holder. Batas Z2/Z3 |
| `cvdd` | Batas bawah historis paling ekstrem. Flag ekstrem di Z1 |
| `active_realized_price` | Rata-rata harga beli investor aktif (basis AVIV). Di master ada `_x` (dari price_level) dan `_y` (dari aviv) — isinya sama |
| `MVRV 0σ` | Level harga saat MVRV = rata-rata historisnya |
| `true_market_mean_price` | Cointime true market mean |
| `200_dma`, `50_wma`, `200_wma` | Moving average teknikal (200 hari, 50 minggu, 200 minggu) |
| `cum_pl_price` | Cumulative P/L price level |
| `pl_price_ratio` | Rasio harga terhadap cum_pl_price |

## AVIV (batas Z3/Z4/Z5)

File: `data_aviv.csv` / master.

| Kolom | Artinya |
|-------|---------|
| `aviv_ratio` | Rasio AVIV mentah (market cap aktif / investor cap) |
| `aviv_mean` | Rata-rata historis aviv_ratio — dalam satuan ratio, BUKAN harga |
| `aviv_upper_1sd`, `aviv_upper_2sd` | Mean + 1/2 standar deviasi (satuan ratio) |
| `aviv_lower_1sd`, `aviv_lower_2sd` | Mean − 1/2 standar deviasi (satuan ratio) |
| `price_at_aviv_mean` | **AVIV Mean dalam USD** — batas Z3/Z4. Ini yang dipakai framework |
| `price_at_aviv_plus_1_sigma` | Basis hitung **AVIV Upper** framework: `aviv_mean + 0.5 * (price_at_aviv_plus_1_sigma - aviv_mean)`... ⚠️ lihat catatan di bawah |
| `price_at_aviv_plus_2_sigma`, `price_at_aviv_minus_1_sigma` | Level harga di +2SD / −1SD |
| `investor_cap` | Investor capitalization (USD) |
| `liveliness` | Rasio aktivitas coin lama vs total |

> ⚠️ **AVIV Upper framework = +0.5 SD**, dihitung: `price_at_aviv_mean + 0.5 * (price_at_aviv_plus_1_sigma - price_at_aviv_mean)`. Pola established ada di `research/analyze_k3_stage_comparison.py` — ikuti itu, jangan hitung ulang sendiri.

## MVRV

File: `data_mvrv.csv` / master.

| Kolom | Artinya |
|-------|---------|
| `mvrv_ratio` | Market cap / Realized cap. Basis sinyal K1 #1 |
| `sth_mvrv` | MVRV holder baru (<155 hari). Dipakai K1 #3, K2 kondisi 1 |
| `lth_mvrv` | MVRV holder lama (>155 hari). Dipakai K4 kondisi 1 |
| `mvrv_zscore` | Z-score MVRV **full-history**. Untuk rolling 1 tahun (alat bantu visual K1 #1), hitung sendiri dari `mvrv_ratio` — lihat KB MVRV v1.4 § Catatan Tambahan |

## SOPR & P/L Momentum

File: `data_momentum.csv`, `data_pl.csv` / master.

| Kolom | Artinya |
|-------|---------|
| `asopr` | Adjusted SOPR — profit/loss rata-rata coin yang bergerak hari itu. >1 = jual untung |
| `sth_sopr` | SOPR holder baru. Dipakai K1 #4 (gap MA90-MA60), K2 kondisi 2 |
| `lth_sopr` | SOPR holder lama. Dipakai K4 kondisi 2 (<0.50 = kapitulasi LTH) |
| `nupl`, `sth_nupl`, `lth_nupl` | Net Unrealized Profit/Loss (total / STH / LTH). ⚠️ Sudah diuji & DICABUT sebagai tie-breaker K2 — lihat video_index |
| `net_realized_pl_usd` | Realized profit − loss harian (USD) |
| `daily_realized_profit_btc`, `daily_realized_loss_btc` | Volume profit/loss harian (BTC) |
| `rpl_ratio` | Rasio realized profit/loss |
| `sth_pl_ratio`, `lth_pl_ratio` | Rasio P/L per kohort |
| `rrp`, `rrl`, `relative_realized_pl` | Realized profit/loss relatif terhadap market cap |

## Supply in Profit/Loss

File: `data_supply.csv` / master.

| Kolom | Artinya |
|-------|---------|
| `percent_btc_in_profit` | % total supply yang untung. Dipakai K1 #5 (>90% & turun), K2 kondisi 3 (>60%), K4 kondisi 3 (<50%) |
| `percent_btc_in_loss` | Kebalikannya |
| `pct_sth_in_profit`, `pct_sth_in_loss` | % supply STH untung/rugi. K4 kondisi 3 (STH profit <10%), K5 staging (STH Loss ≥50%) |
| `pct_lth_in_profit`, `pct_lth_in_loss` | % supply LTH untung/rugi. K2 kondisi 4 (stabilitas LTH) |
| `lth_supply_btc`, `sth_supply_btc` | Jumlah supply per kohort (BTC) |

## Sentiment & Derivatives

| Kolom | File | Artinya |
|-------|------|---------|
| `Fear & Greed` | `data_fg.csv` / master | Index 0–100. Dipakai K5 staging (<50 = deploy). ⚠️ Data mulai 2018 |
| `funding_rate` | `data_derivatives.csv` / master | Funding rate perpetual futures. ⚠️ Data mulai 2020, sudah diuji untuk K5 — lihat video_index |
| `total_oi` | sama | Total open interest. ⚠️ Data mulai 2020 |
| `trend_*`, `wiki_*` | `data_sentiment.csv` / master | Google Trends & Wikipedia views (bitcoin, crypto, ethereum, nft/blockchain) |

## Metrik lain (BELUM ada KB-nya — pakai ekstra hati-hati)

| Kolom | File | Artinya |
|-------|------|---------|
| `cdd` | `data_cdd.csv` / master | Coin Days Destroyed — coin lama bergerak = CDD tinggi |
| `vdd_30d_ma`, `vdd_365d_ma`, `vdd_multiple` | sama | Value Days Destroyed MA & multiple (VDD multiple tinggi = distribusi coin lama) |
| `total_balance`, `net_flow`, `inflow`, `outflow` | `data_exchange.csv` / master | Balance & aliran BTC di exchange. net_flow positif = masuk exchange (tekanan jual potensial) |
| `rhodl_ratio`, `realized_cap_1w`, `realized_cap_1_2y` | `data_rhodl.csv` / master | RHODL = rasio realized cap 1 minggu vs 1-2 tahun. Historis: puncak siklus |
| `supply_<band>`, `realized_cap_<band>` | `data_hodl_waves.csv` / master | HODL waves — supply & realized cap per umur coin (0-1d s/d 10y+) |
| `lth_pl_price`, `lth_pl_flow_btc` | `data_lth_flow.csv` / master | LTH profit/loss price level & aliran BTC LTH |
| `realized_cap_usd`, `lth_realized_cap_usd`, `sth_realized_cap_usd` | `data_realized_cap.csv` / master | Realized cap total & per kohort |
| `apparent_demand` | `data_apparent_demand.csv` / master | Apparent Demand (30-hari perubahan circulating supply, gaya Glassnode) — proxy laju permintaan baru. Ditambah 2026-07-11 dari `research/findings/video_whale-accumulation-2025_findings.md`. Belum ada threshold/rule di framework, belum ada KB — pakai ekstra hati-hati. Full history sejak 2010-07-17 |

---

## Yang TIDAK ada di data kita

Kalau video mengklaim pakai metrik ini, verdict-nya `NEEDS-DATA-WE-DONT-HAVE`:

- Data per-exchange (Binance flow, Coinbase premium, dll) — kita cuma punya agregat
- Whale/entity metrics (jumlah address, balance whale, entity-adjusted)
- Miner metrics (hash rate, miner reserve, Puell Multiple)
- Stablecoin metrics (SSR, stablecoin supply)
- On-chain volume, active addresses, fees
- Options data (skew, IV) — cuma punya funding & OI futures
- Data intraday — semua data kita harian
