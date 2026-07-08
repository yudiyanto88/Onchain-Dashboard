# Onchain Dashboard

Bitcoin on-chain analysis dashboard — personal investment framework oleh [@yudiyanto88](https://github.com/yudiyanto88).

Data source: [ChartInspect.com](https://chartinspect.com) (Glassnode-sourced), auto-update harian via GitHub Actions.

---

## Struktur Folder

Repo di-rapikan 8 Juli 2026 — root cuma isi script produksi, data, dan config. Semua riset/eksplorasi dipindah ke subfolder.

| Folder | Isi |
|--------|-----|
| `references/` | Framework aktif (`Decision_Framework v1.md`) + knowledge base v1.4 |
| `alerts/` | `alert_check.py` (cek kondisi zona/K-node, kirim Telegram) + `logs/` (snapshot harian) |
| `research/` | Semua script `analyze_*.py`, `chart_*.py`, `verify_*.py`, dan tools riset lain — dijalankan dari root repo (path CSV relatif ke root, bukan ke lokasi script) |
| `research/findings/` | Hasil temuan riset (`*_findings.md`, session notes) |
| `research/charts/` | Chart PNG hasil riset |
| `archive/` | Framework & knowledge base versi lama yang sudah digantikan, backup script |
| `models/` | Model ML tersimpan (`ml_zone_predictor.py` di `research/`) |
| `dcm_short_term_risk_score/`, `sth_accumulation_bands/`, `vshape_buy_score/` | Sub-proyek riset self-contained (script + data + output masing-masing) |

### Script Utama (root)
| File | Fungsi |
|------|--------|
| `app.py` | Streamlit dashboard |
| `auto_update.py` | Pipeline data harian (15 pipeline, dipicu GitHub Actions) |
| `requirements.txt` | Python dependencies |
| `CLAUDE.md` | Instruksi konteks untuk Claude Code session |

`research/debug_formula.py` — validasi formula Cumulative LTH P/L Price (dipicu manual via `.github/workflows/debug_formula.yml`).

### Data CSV (root)
| File | Isi |
|------|-----|
| `data_price_level.csv` | BTC price, STH/LTH cost basis, Realized Price, CVDD, True Market Mean, Active Realized Price, MVRV 0σ, Cum P/L Price, moving averages (200 DMA, 50 WMA, 200 WMA) |
| `data_mvrv.csv` | MVRV, STH MVRV, LTH MVRV |
| `data_momentum.csv` | aSOPR, LTH SOPR, STH SOPR, NUPL, STH NUPL, LTH NUPL, Net Realized P/L, STH/LTH P/L Ratio |
| `data_supply.csv` | LTH/STH supply (BTC), % LTH/STH in profit/loss, Total % in profit/loss |
| `data_aviv.csv` | AVIV Ratio, AVIV Mean/Upper bands (lihat catatan bug di bawah) |
| `data_derivatives.csv` | Funding Rate, Open Interest |
| `data_exchange.csv` | Exchange balance, net flow (data tersedia sampai Feb 2026) |
| `data_fg.csv` | Fear & Greed Index |
| `data_sentiment.csv` | Google Trends, Wikipedia pageviews (BTC, ETH, Crypto, dll) |
| `data_rhodl.csv` | RHODL Ratio |
| `data_hodl_waves.csv` | HODL Waves — supply & realized cap per age band |
| `data_realized_cap.csv` | Realized Cap (total, LTH, STH) |
| `data_cdd.csv` | Coin Days Destroyed, VDD Multiple |
| `data_lth_flow.csv` | LTH P/L Price, LTH P/L Flow (BTC) |
| `data_*_events.csv` | Annotasi event historis per metrik (dipakai script riset di `research/`, bukan dashboard) |
| `data_master_all_metrics.csv` | Gabungan semua CSV di atas (generated, jangan edit manual) |

---

## Auto-Update Pipeline

GitHub Actions menjalankan `auto_update.py` setiap hari. Pipeline berjalan 15 tahap secara berurutan — setiap tahap menarik data dari ChartInspect API, memproses, dan menyimpan ke CSV masing-masing. Pipeline 15 menggabungkan semua CSV ke `data_master_all_metrics.csv`.

---

## Catatan

- `data_exchange.csv` — endpoint ChartInspect berhenti update sejak Februari 2026
- `data_master_all_metrics.csv` — file generated, di-overwrite setiap run, jangan dijadikan sumber analisis utama
- `data_aviv.csv` — kolom turunan bawaan ChartInspect (`price_at_aviv_mean`, `price_at_aviv_plus_1_sigma`, dst) pakai basis harga yang salah (inflasi ~9-10%). `app.py` dan `alerts/alert_check.py` sudah menghitung ulang sendiri dari kolom mentah (`btc_price / aviv_ratio × aviv_mean`) — jangan pakai kolom `price_at_aviv_*` langsung di script baru
