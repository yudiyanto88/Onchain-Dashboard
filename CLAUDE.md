# CLAUDE.md — Onchain Dashboard

## SIAPA AKU

Bitcoin investor Indonesia. Bukan developer, bukan data scientist.
Pakai AI sebagai tool bantu analisis — bukan pengganti judgment.
Data utama: ChartInspect.com (Glassnode-sourced), export ke CSV.

Pengalaman yang relevan: Oktober 2025 hampir terliquidasi karena tidak memperhitungkan simultaneous worst-case scenarios. Setiap analisis yang menyentuh leverage atau sizing harus ingat ini.

---

## ISI REPO INI

- `auto_update.py` — tarik data harian dari ChartInspect API, simpan ke CSV
- `app.py` — Streamlit dashboard untuk visualisasi
- `data_*.csv` — file data on-chain harian
- `alerts/alert_check.py` — cek kondisi framework, kirim notif Telegram
- `references/` — knowledge base files (KB v1.4) dan Decision_Framework v1.md

---

## FRAMEWORK INVESTASI

Framework aktif menggunakan zona Z1–Z5 dan decision nodes K1–K6.

**Setiap task yang menyentuh logika framework — zona, K-node, threshold, sinyal, kondisi entry/exit — baca `references/Decision_Framework v1.md` dulu sebelum mulai.**

Ringkasan singkat zona (untuk orientasi cepat saja):

| Zona | Kondisi harga | K aktif |
|------|--------------|---------|
| Z1 | Price < STH RP, STH RP < RP | K4 |
| Z1b | STH RP ≤ Price < RP, STH RP masih < LTH RP | K4 wrap-up |
| Z2 | STH RP ≈ RP ≈ LTH RP (konvergen, jarak < 2%) | K5 mulai |
| Z3 | RP ≤ Price < AVIV Mean | K5 aktif |
| Z4 | AVIV Mean ≤ Price < AVIV Upper | K6 / K2 |
| Z5 | Price ≥ AVIV Upper | K1 / K2 |

Level batas zona:
- STH RP = rata-rata harga beli holder < 155 hari
- RP = Realized Price, rata-rata harga beli semua holder
- LTH RP = rata-rata harga beli holder > 155 hari
- AVIV Mean = rata-rata harga beli investor aktif
- AVIV Upper = AVIV Mean + 0.5 SD
- CVDD = batas bawah historis paling ekstrem

---

## HARD LIMITS LTV

Berlaku di semua kondisi. Tidak ada sinyal on-chain yang bisa override ini.

| LTV | Aksi |
|-----|------|
| 52% | Batas atas saat deploy |
| 55% | Batas absolut, hanya kalau ada dana top-up yang sudah pasti cair |
| 58–60% | Jual collateral, bawa LTV balik ke 53–54% |
| 62–63% | Jual lebih besar, target 55% |
| 65% | Jual besar sekarang, target di bawah 50% |

**LTV 60% = jual collateral dan bayar loan sekarang. Tidak perlu analisis. Tidak perlu tunggu.**

---

## CARA KERJA DI REPO INI

Dua tool, dua fungsi berbeda:
- **Claude Code CLI (ini)** → komputasi: baca CSV, jalankan script, analisis data, debug kode, commit hasil
- **Claude.ai (browser)** → reasoning: evaluasi sinyal, keputusan framework, interpretasi

Jangan campur tugas. Claude Code tidak membuat keputusan investasi. Claude.ai tidak menulis kode produksi.

**Setiap sesi Claude Code:**
1. Baca file ini sebagai konteks repo
2. Kalau task menyentuh logika framework → baca `references/Decision_Framework v1.md`
3. Kalau task menyentuh metrik spesifik → baca KB v1.4 yang relevan dari `references/`
4. Jangan ubah `auto_update.py` atau `app.py` kecuali diminta eksplisit

---

## BAHASA

Bahasa Indonesia. Technical terms (MVRV, SOPR, LTV, aSOPR, AVIV, dll) tetap English.
