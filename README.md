# Onchain Dashboard

Bitcoin on-chain analysis dashboard — personal investment framework oleh [@yudiyanto88](https://github.com/yudiyanto88).

Data source: [ChartInspect.com](https://chartinspect.com) (Glassnode-sourced), auto-update harian via GitHub Actions.

---

## Struktur File

### Script Utama
| File | Fungsi |
|------|--------|
| `app.py` | Streamlit dashboard |
| `auto_update.py` | Pipeline data harian (15 pipeline, dipicu GitHub Actions) |
| `debug_formula.py` | Script validasi formula Cumulative LTH P/L Price |
| `requirements.txt` | Python dependencies |

### Data CSV
| File | Isi |
|------|-----|
| `data_price_level.csv` | BTC price, STH/LTH cost basis, Realized Price, CVDD, True Market Mean, Active Realized Price, MVRV 0σ, Cum P/L Price, moving averages (200 DMA, 50 WMA, 200 WMA) |
| `data_mvrv.csv` | MVRV, STH MVRV, LTH MVRV |
| `data_momentum.csv` | aSOPR, LTH SOPR, STH SOPR, NUPL, STH NUPL, LTH NUPL, Net Realized P/L, STH/LTH P/L Ratio |
| `data_supply.csv` | LTH/STH supply (BTC), % LTH/STH in profit/loss, Total % in profit/loss |
| `data_derivatives.csv` | Funding Rate, Open Interest |
| `data_exchange.csv` | Exchange balance, net flow (data tersedia sampai Feb 2026) |
| `data_fg.csv` | Fear & Greed Index |
| `data_sentiment.csv` | Google Trends, Wikipedia pageviews (BTC, ETH, Crypto, dll) |
| `data_rhodl.csv` | RHODL Ratio |
| `data_hodl_waves.csv` | HODL Waves — supply & realized cap per age band |
| `data_realized_cap.csv` | Realized Cap (total, LTH, STH) |
| `data_cdd.csv` | Coin Days Destroyed, VDD Multiple |
| `data_lth_flow.csv` | LTH P/L Price, LTH P/L Flow (BTC) |
| `data_master_all_metrics.csv` | Gabungan semua CSV di atas (generated, jangan edit manual) |

---

## Auto-Update Pipeline

GitHub Actions menjalankan `auto_update.py` setiap hari. Pipeline berjalan 15 tahap secara berurutan — setiap tahap menarik data dari ChartInspect API, memproses, dan menyimpan ke CSV masing-masing. Pipeline 15 menggabungkan semua CSV ke `data_master_all_metrics.csv`.

---

## Catatan

- `data_exchange.csv` — endpoint ChartInspect berhenti update sejak Februari 2026
- `data_master_all_metrics.csv` — file generated, di-overwrite setiap run, jangan dijadikan sumber analisis utama
