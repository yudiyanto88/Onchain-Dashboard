# Handoff — Dashboard Streamlit v2

Diperbarui 17 Sep 2026 (versi ringkas, commit sesudah `d1dff1d`). Versi lengkap sebelum diringkas — cerita pengerjaan tiap fitur, opsi yang ditolak, hasil ukur piksel — ada di `archive/handoff_riwayat_2026-09-17.md` (buka hanya kalau perlu detail sejarah; nomor bagian 3.x yang disebut di bawah merujuk ke file itu).

Baca dokumen ini dan `CLAUDE.md` sebelum mulai. Semua yang ditandai **ditahan/ditunda** harus ditanyakan ke user dulu.

**Cara memperbarui dokumen ini (supaya tetap ringkas, target < 35 KB):**
- Susunan tetap: 1 Status · 2 Cara kerja user · 3 Halaman live (tabel) · 4 Arsitektur · 5 Keputusan final · 6 Ditahan/ditunda · 7 Data & cek kualitas · 8 Warna · 9 Jebakan teknis · 10 Cara menjalankan.
- Halaman baru = satu baris di tabel bagian 3, bukan bagian cerita baru.
- Tulis hasil dan keputusan saja. Cerita pengerjaan, opsi yang ditolak, dan hasil ukur piksel tidak masuk; kalau perlu disimpan, tambahkan ke file arsip di `archive/`.
- Item yang selesai dihapus dari bagian 6, bukan dicoret.
- Jebakan teknis hanya yang masih bisa terulang; hapus kalau fiturnya sudah tidak ada.
- Perubahan handoff diusulkan ke user dulu sebelum ditulis.
- **Saat user konfirmasi akan lanjut di sesi baru:** sesudah handoff diperbarui (dan di-commit/push kalau diminta), tulis **prompt pembuka sesi baru langsung di chat** — sesuaikan dengan status terakhir. Prompt itu tidak disimpan di handoff.

---

## 1. Status dan langkah berikutnya

- **Live (10 halaman, 5 kelompok):** Valuation (MVRV · Price Levels · AVIV) · Profitability (SOPR · NUPL · Supply in Profit) · Holder Behavior (HODL Waves · RHODL Ratio) · Derivatives (Funding Rates & Open Interest) · Sentiment & Macro (Fear & Greed). Semua halaman: slider rentang, nyaman di HP, kontrol diingat per halaman, tombol Style di chart.
- **Langkah pertama sesi baru:**
  1. Cek server `dashboard-v2-uji` (bagian 2), buka halaman, lihat keadaannya sebelum mengubah apa pun.
  2. Tanyakan apakah Streamlit Cloud perlu **Reboot app** sesudah push terakhir (`dashboard/` berubah).
  3. Tanyakan apakah **Cohort State** (bagian 6) sudah boleh dilanjutkan, lalu **halaman berikutnya** (kandidat dan hasil cek data di bagian 7 — jangan dicek ulang).
- **Menambah halaman:** satu `MetricFamily` di `dashboard/registry.py` (+ loader di `data.py`). Urutan kerja yang disukai user: cek kualitas data (nilai macet, lonjakan, satuan, cakupan, revisi) → pratinjau widget dengan data asli + uji palet (bagian 8) → tunggu pilihan user → kerjakan di localhost → user bilang valid → merge dari GitHub → commit → push.

---

## 2. Cara kerja yang disukai user

- Chat **bahasa Indonesia simpel**, singkat tapi jelas; istilah teknis tetap English. **Teks di dashboard bahasa Inggris.**
- User **tidak bisa menilai dari kode atau hex warna** → untuk tampilan/warna selalu **widget pratinjau inline (`show_widget`) dengan data CSV asli**, lalu tunggu pilihan.
- User sering bilang **"jangan eksekusi dulu"**: jelaskan pemahaman, tunggu konfirmasi. Foto dari user = cara tercepat menyamakan maksud.
- Beri **rekomendasi + untung-rugi**, bukan sekadar daftar opsi.
- **Klaim harus dibuktikan**; kalau pengukuran meragukan, bilang belum sah dan ulangi dengan cara lain.
- Kalau mengecilkan/mengoptimasi sesuatu, pertimbangkan efek ke elemen lain (lebar, tinggi, jarak).
- **Keluhan tampilan sekecil piksel hampir selalu benar → ukur dulu di halaman hidup** (`getBoundingClientRect`, `getComputedStyle`), jangan menebak dari kode.
- **Selera tampilan:** kontrol ringkas, lambang ketimbang kata, ukuran seragam, kedudukan lurus dengan elemen sekitar.
- **Localhost uji: http://localhost:8503** (server `dashboard-v2-uji` dari `.claude/launch.json`). "Nyalakan localhost" = server ini. **Restart sesudah mengubah `dashboard/`** (modul yang sudah dimuat tidak dibaca ulang). **Server ikut mati kalau sesi Claude Code ditutup/dibuka ulang** — cek `curl http://localhost:8503/_stcore/health`. Kalau port dipakai server sesi lain, `preview_start` menolak: pakai server itu atau minta user. User juga bisa menjalankan sendiri: `streamlit run app.py --server.port 8503`.
- **Handoff:** jangan diedit tanpa persetujuan; daftarkan usulan poin dulu (kecuali user sudah minta dicatat).
- **Git:** commit hanya file dashboard yang relevan + handoff, dan hanya kalau user minta. Repo punya banyak perubahan user yang belum di-commit (`CLAUDE.md`, `auto_update.py`, `references/`, `research/`) — jangan ikut. Sebelum push **merge dulu dari GitHub** (`git fetch`; `git diff --name-only HEAD...origin/main` — kalau hanya `data_*.csv` dan `alerts/logs/`, aman). Sesudah push yang mengubah `dashboard/`, ingatkan **Manage app → ⋮ → Reboot app** bila versi online error (Streamlit Cloud tidak membaca ulang modul).

---

## 3. Halaman live

Semua: BTC oranye `#F7931A` (kecuali HODL Waves), key localStorage `dash_v2_<key>`. Warna kohort konsisten: semua holder navy `#0070a6`, STH rust `#bf5546`, LTH teal `#0b8e89`. Garis ambang framework **tidak** dipasang di halaman mana pun (keputusan framework).

| Menu / alamat | Loader & kolom | Bawaan & bentuk | Catatan data / keputusan |
|---|---|---|---|
| **MVRV** `/` (key `market_valuation`) | `load_mvrv` — `data_mvrv.csv`; Rolling Z-Score 1y/2y/4y dihitung | BTC Separate pane, metrik & harga Log; LTH MVRV sumbu kanan; ref Neutral 1.0; pane bawah **Z-Score** (Hidden): Z-Score navy 80 % + Rolling hijau `#97c459` 55 % (2y/4y mati awal) | LTH MVRV bisa puluhan (2011: 374). Z-Score full-history untuk aturan, rolling untuk mata (KB MVRV). Tanpa pita "extreme" berambang tetap |
| **Price Levels** `/price-levels` | `load_price_levels` — `data_price_level.csv` + AVIV Mean/Upper dari `data_aviv.csv` | Overlay, satu sumbu kanan, skala Auto. STH RP, Realized Price, LTH RP, AVIV Mean `#7b65d2`, AVIV Upper `#a58df0`, CVDD `#a8963f`; mati awal: MVRV 0σ, 200 DMA, 50 WMA, 200 WMA (abu) | AVIV dihitung ulang `btc_price/aviv_ratio × band` (kolom `price_at_aviv_*` salah basis ±9–10 %). 84 hari pertama AVIV disembunyikan (`_aviv_awal`) |
| **AVIV** `/aviv` | `load_aviv` — `data_aviv.csv` (satuan rasio) | Separate pane, Log/Log; AVIV Ratio navy, Mean violet, Upper (+0.5σ) violet muda, sumbu kanan; kelompok **σ Bands** (+1σ +2σ −1σ −2σ, abu, mati awal); pane bawah **Deviation (σ)** menyala awal (`extra_default`) | Rasio ≥ Upper ⇔ harga ≥ AVIV Upper (1.279 hari sejak 2011). Band bawah negatif s/d 2014 dikosongkan |
| **SOPR** `/sopr` | `load_sopr` — `data_momentum.csv` | Separate pane, Log/Log; LTH-SOPR sumbu kanan; Break-even 1.0 di semua sumbu; pane **SOPR Gap** (Hidden) | **Gap = SMA90(STH-SOPR) − SMA60 dari SMA90 itu (KB §12)** — `alert_check.py` memakai SMA60 − SMA90 (bagian 6). SOPR 3 desimal, gap 5, LTH ≥ 100 tanpa desimal |
| **NUPL** `/nupl` | `load_nupl` — `data_momentum.csv` | Separate pane, metrik Auto, harga Log; ketiga garis sumbu kanan; Break-even 0; pane **NUPL Gap** (LTH − STH, Hidden) | Ratio LTH/STH sengaja tidak dimuat (melompat saat STH ≈ 0). Sumbu tidak dipaku −1..1 |
| **Supply in Profit** `/supply-in-profit` | `load_supply` — `data_supply.csv` | Separate pane, sumbu 0–100 kanan; saklar **Profit / Loss** di chart (boleh dua-duanya/mati); warna Loss saat keduanya: `#839df0` `#dc9390` `#38d1b4` | Loss = 100 − Profit (kembaran di browser). 1 desimal |
| **HODL Waves** `/hodl-waves` (key `hodl_waves`) | `load_hodl_waves` — `data_hodl_waves.csv` (`RC <band>`, `Supply <band>`) | **Overlay, garis BTC putih** (`btc_color`, `btc_dim` 0,17); 12 band area bertumpuk (`kind="stack"`), muda di bawah, spektrum `#d73027 … #9e7bd6`; saklar **Realized Cap \| Supply** (bawaan Realized Cap); tanpa Highlight/smoothing | Mematikan band di legend menumpuk ulang sisanya. Dulu bernama "RHODL Waves" `/rhodl-waves` |
| **RHODL Ratio** `/rhodl-ratio` | `load_rhodl_ratio` — `data_hodl_waves.csv` | Judul "RHODL Ratio (6m–2y ÷ 1d–3m)"; **Overlay, skala Auto/Auto**; garis navy sumbu kiri | = RC (6m–12m + 1y–2y) ÷ (1d–1w + 1w–1m + 1m–3m), cocok persis `research/findings/_cohort_state_plane.csv`. **Bukan** `rhodl_ratio` di `data_rhodl.csv`. 86 % varians dari penyebut → jangan dibaca sendirian. Calon tempat Cohort State |
| **Funding Rates & Open Interest** `/funding-oi` | `load_derivatives` — `data_derivatives.csv` (+13 kolom `oi_<bursa>`) | Separate pane; funding batang dua warna (teal/rust) kanan, OI garis violet kiri, satu pane; ref Zero ikut sumbu funding; saklar **OI BTC \| USD** (boleh dua-duanya); pane **OI Change (1d)** (Hidden) | Funding tanpa satuan (4 desimal). `total_oi` = jumlah 13 bursa; ΔOI hanya bursa yang OI > 0 kemarin & hari ini (cakupan bursa bertambah 2020–2025). OI USD = OI × harga |
| **Fear & Greed** `/fear-greed` | `load_fear_greed` — `data_fg.csv` + harga dari `data_mvrv.csv` | Separate pane, sumbu 0–100 kanan; garis bergradasi rust→abu→teal; **SMA30 Band kuning `#F7E9A8` menyala awal**; nama kelas di tooltip | Kelas API: ≤25 Extreme Fear · 26–46 Fear · 47–54 Neutral · 55–75 Greed · ≥76 Extreme Greed. Label nilai terakhir SMA30 di sumbu tertulis bulat (format seri pertama) |

---

## 4. Arsitektur

| File | Isi |
|---|---|
| `app.py` | Entry point, `st.navigation` berkelompok (`_halaman(family)`), sidebar, seluruh CSS global (termasuk `:fullscreen`, `html.penuh-semu`, `@media max-width 768px`) |
| `.streamlit/config.toml` | Tema: `base = "dark"`, `primaryColor = "#006d77"` |
| `dashboard/registry.py` | `Series`, `RefLine`, `MetricFamily` (semua field dijelaskan di komentar) + daftar `FAMILIES` (urutan = urutan menu) |
| `dashboard/data.py` | Loader CSV (cache 1 jam), SMA/EMA, filter, `HODL_BANDS`, `_aviv_awal` |
| `dashboard/metric_page.py` | Header, 7 kotak kontrol (Range · Smoothing · Scale · BTC price · [pane bawah] · Display · Tooltip), ingatan kontrol (`{k}_mem`), gaya bawaan smoothing, rencana garis |
| `dashboard/charts.py` | Dataclass `Line` + `render()` yang meneruskan ke `lw_chart` |
| `dashboard/lw_chart.py` | Chart lightweight-charts 4.2.3 di `st.iframe`: `TEMPLATE` (HTML/CSS/JS) + `render()` |
| `archive/app_v1.py` | Dashboard v1 (arsip) |

**Kemampuan renderer (dipakai lewat registry):**
- Pane: `price` (BTC Separate pane) → `main` → `extra` (pane bawah, selalu linear; `extra_label`, `extra_default`). Zoom dan lebar sumbu tersinkron; sumbu waktu hanya di pane terbawah; slider rentang (isi BTC Log) di bawah semua.
- Sumbu: `axis` bawaan + `separate_axis` saat Separate pane (aturan user: metrik berskala sama ke kanan saat Separate pane). `metric_range` (sumbu tetap, angka bulat tanpa desimal, di luar rentang kosong). Angka sumbu disembunyikan (lebar tetap) kalau semua garis di sisi itu mati. Seri mati diparkir ke skala lain supaya format sumbu tidak kacau.
- Jenis seri: garis, histogram (`negative_color` dua warna), gradasi per titik (`gradient`), area bertumpuk (`kind="stack"`, `stack_index`, `stack_cols` + `stack_units`), kembaran Loss (`complement`).
- Legend berkelompok (garis utama + kotak angka periode/anggota), `hidden_default` (sekali, dicatat di `seen`), Highlight multi (redup kontras 1,70:1; disembunyikan kalau hanya BTC), tarik chart menggeser sumbu garis yang disorot, klik dua kali reset.
- Saklar di chart: Profit/Loss, satuan (`unit_switch`/`unit`/`pair`/`compact`), bobot tumpukan (`stack_units`). Tersimpan di localStorage.
- Format angka per seri: `precision`, `whole_from`, `compact`; garis acuan mewarisi format metrik di sumbunya. Data dikirim dengan desimal `max(4, precision+1)`.
- Tooltip Fixed/Cursor/Off (satu pilihan untuk semua halaman, `tooltip_pref`), periode smoothing jadi kolom, `value_labels`.
- **Tombol Style** (panel `#gaya`, pojok kanan atas): bentuk Solid/Dotted/Dashed/Step/Band + tebal per periode smoothing, tanpa memuat ulang chart, tersimpan `state.gaya`; hanya muncul kalau ada smoothing. Python memberi gaya bawaan berurutan Dotted → Step → Band (`smoothing_style_default` per halaman). Step jadi putus panjang kalau < 6 px per bar.
- Layar penuh tombol **Full** di chart (Fullscreen API; iPhone: kelas `penuh-semu`), tombol **Scale** hanya perangkat sentuh (`vertTouchDrag`, tidak disimpan). Sidebar `initial_sidebar_state="auto"`.
- Zoom bertahan saat rerun (posisi bar + sidik data `sig`; tombol Range tetap menang). Range tidak memotong data, hanya rentang tampil (`C.view`).
- **Yang bertahan:** legend, Highlight, zoom, saklar, gaya garis → localStorage (juga setelah reload). Kontrol Python → `{k}_mem` hanya selama tab terbuka; reload = bawaan.

---

## 5. Keputusan final — jangan dibahas ulang

- Tanpa timeframe Daily/Weekly (resampling menggeser tanggal cross); pakai SMA/EMA. Default Range **All**. Tanpa OHLC (ChartInspect tidak punya). Tanpa baris KPI (diganti "Latest data").
- **Teal gelap `#006d77` warna utama** (isian, garis, lencana; tulisan di atasnya putih). **Tidak pernah jadi warna huruf** — tulisan teal pakai `#2aa6b0`.
- Judul halaman **gaya B2**: lencana kelompok teal kecil + nama metrik 18,4 px tebal 600.
- Menu `st.navigation`, kelompok **jenis metrik** (bukan peran framework), nama menu pendek, judul kelompok `#2aa6b0`.
- Semua garis utama **2 px** (`LINE_WIDTH`). Palet kohort navy/rust/teal setara terang. Uji buta warna = cek cepat, bukan syarat mutlak.
- Legend berkelompok per metrik; **BTC Price selalu terakhir** di legend, tombol sorot, tooltip. Tanpa simbol/marker smoothing. Tingkat terang legend / angka periode / tombol sorot sengaja berbeda (hierarki). Label "Highlight" setara tombol.
- Kotak Display tidak menghitung BTC. Popover Scale memakai nama metrik.
- Tombol layar penuh satu, di dalam chart. Line style di **tombol Style dalam chart (opsi B)**, bukan popover dan bukan klik kanan kotak periode.
- Tooltip bawaan **Cursor**, latar 94 %.
- Slider rentang: isi BTC, semua halaman, 52 px. Range memindahkan jendela (pilihan B).
- HP: tahap 2 (chart lebih pendek, angka ringkas, tombol legend besar) **ditolak**. Angka sumbu terpotong di tepi pane dibiarkan.
- Z-Score di pane ketiga (bukan di chart MVRV), histogram polos (gradasi ditunda), tanpa pita ambang tetap.
- Keputusan per halaman ada di tabel bagian 3.

---

## 6. Ditahan / ditunda / belum diputuskan (tanyakan dulu)

- **Cohort State (DITAHAN user 17 Sep — "ada yang perlu dipastikan dulu"):** analisa `research/analyze_cohort_state_plane.py` + `plot_cohort_state_plane.py` + `findings/_cohort_state_plane.csv` (s/d 7 Sep).
  - Demand Impulse (DI) = RC 1d–3m ÷ SMA90 − 1 → persentil 1.460 hari (min 60 %); cukup `data_hodl_waves.csv`.
  - Aged Cohort Turnover (ACT) = BTC dibelanjakan kohort 6m–2y (profit + loss BTC band 5 & 6 endpoint `realized-profit-by-age`; band_5 = 6m–12m, band_6 = 1y–2y, terverifikasi) ÷ BTC dipegang kohort ((supply 6m–12m + 1y–2y)/100 × (lth_supply_btc + sth_supply_btc)), SMA30 → persentil 4 tahun.
  - State: histeresis per sumbu (≥ 60 tinggi, ≤ 40 rendah, pindah setelah 10 hari), empat kombinasi DORMANSI/SEPI · DISTRIBUSI/LEPAS TANPA BID · TRANSFER/TANGAN BERGANTI · AKUMULASI/MODAL MASUK PASOKAN TERKUNCI. 60 episode sejak Mar 2013, median 76 hari.
  - **Penghalang:** data ACT tidak ada di CSV repo (analisa lama membaca `rpba.pkl` di scratchpad sesi lain, s/d 9 Sep). Butuh pipeline baru di `auto_update.py` yang menyimpan `data_profit_by_age.csv` (profit/loss BTC 12 band) — **izin user ditahan**. Workflow sudah `git add .`.
  - Jawaban user: bentuk state (pita tipis B vs latar pane A) ditahan; persentil disembunyikan dulu; nama state Inggris (Quiet · Selling, no bid · Changing hands · Inflow, supply locked) keep dulu; letak: digabung ke halaman **RHODL Ratio**. Warna pratinjau: Quiet `#6e7681`, Selling `#bf5546`, Changing `#a8963f` (bukan mustard — dekat oranye BTC bagi buta warna), Inflow `#3f6fd8`, DI `#5b8def`, ACT `#e0705c`.
  - Catatan tafsir: state terlambat ≥ 10 hari; persentil bergeser kalau data direvisi. Bukan bagian framework v2.
- **CDD/VDD (ditunda user, belum butuh):** `vdd_multiple` CSV = VDD harian ÷ MA365 (berisik; p99 12,3, maks 59,9). Rumus Glassnode `vdd_30d_ma / vdd_365d_ma` halus (p99 6,5; puncak 2013 8,4 · 2017 5,2 · 2021 4,5 · 2024 4,4). Usulan waktu itu: rumus 30d/365d, ref 1,0, CDD batang navy, VDD violet, harga dari `data_mvrv.csv`. Research menolak "VDD multiple < 1" sebagai filter.
- **Realized P/L (ditunda):** `data_pl.csv` — `rpl_ratio` melonjak ratusan juta saat loss < 1 BTC (77 hari), `sth_pl_ratio`/`lth_pl_ratio` macet (179/246 hari sama dengan kemarin). Yang sehat: profit/loss BTC, `rrp`, `rrl`, `relative_realized_pl`. Tidak ada KB; kalau dilanjutkan, KB dulu di Claude.ai, ratio dihitung ulang dari jumlah 30 hari.
- **Temuan framework (user cek di Claude.ai; jangan ubah framework/data_dictionary):** `Decision_Framework v2.md` menulis "703 hari Z5"; rumus AVIV benar = **1.279 hari**, dengan kolom `price_at_aviv_*` salah basis = 710 → angka framework kemungkinan dari kolom salah basis (masih dianjurkan `references/data_dictionary.md`).
- **Rumus gap STH-SOPR `alerts/alert_check.py` (`_sth_sopr_ma_gap`) = SMA60 − SMA90, beda dari KB §12** (10 Jan 2021: +0.01141 vs KB +0.02447; dipakai trigger K1 dan alarm bear). Menunggu user; jangan dibetulkan diam-diam.
- **`auto_update.py` punya perubahan user yang belum di-commit** (pipeline 19 Treasury 2Y). Kalau perlu commit hunk lain: `git diff` → saring hunk → `git apply --cached`.
- **Ingatan kontrol setelah reload** (pilihan b, lewat URL query) — belum diminta.
- **Kotak L/R untuk pilihan sumbu** — ditahan (tidak menghemat lebar).
- **Tombol Range di celah kanan baris kontrol** (preset + kalender dua bulan gaya CryptoQuant) — ditahan user ("belum perlu").
- **Usulan disetujui tapi belum diterapkan:** latar brand `#0D1117`; font JetBrains Mono (angka/sumbu) + Inter (label). Ide overlay dua chart bertumpuk untuk banyak skala — dinilai user "slightly over modif".
- **Belum dibahas/dilaporkan kecil:** label nilai terakhir bertumpuk di sumbu saat banyak smoothing (kandidat: `lastValueVisible` false untuk smoothing — tanya dengan pratinjau); Supply in Profit saat Profit & Loss mati legend tidak dicoret; gradasi histogram Z-Score; judul HODL Waves tidak berubah saat saklar Supply.
- **Ide nanti:** pantau LTV intraday dengan harga 10 menit ChartInspect (`https://chartinspect.com/api/charts/crypto/intraday-price?cryptocurrency=bitcoin&resolution=10&from=<unix>&to=<unix>`, `{t, p}`, gratis 30 hari).

---

## 7. Data: CSV, kualitas, kandidat halaman

Semua file punya `date`; sebagian besar punya `btc_price`. Bukan untuk halaman: `data_master_all_metrics.csv`, `data_*_events.csv`.

| File | Kolom | Status |
|---|---|---|
| `data_mvrv.csv` | btc_price, mvrv_ratio, sth_mvrv, lth_mvrv, mvrv_zscore | dipakai (MVRV; harga untuk F&G) |
| `data_price_level.csv` | sth_cost_basis, lth_cost_basis, realized_price, cvdd, active_realized_price, MVRV 0σ, true_market_mean_price, 200_dma, 50_wma, 200_wma, cum_pl_price, pl_price_ratio | dipakai (Price Levels) |
| `data_aviv.csv` | aviv_ratio, aviv_mean, aviv_upper/lower_1sd/2sd, price_at_aviv_* (**salah basis**), investor_cap, active_realized_price, liveliness | dipakai (Price Levels, AVIV) |
| `data_momentum.csv` | asopr, lth_sopr, sth_sopr, net_realized_pl_usd, nupl, sth_nupl, lth_nupl | dipakai (SOPR, NUPL) |
| `data_supply.csv` | lth/sth_supply_btc, pct_lth/sth_in_profit/loss, percent_btc_in_profit/loss | dipakai (Supply in Profit) |
| `data_hodl_waves.csv` | `supply_<band>`, `realized_cap_<band>` (12 band: 0-1d … 10y+, satuan %) | dipakai (HODL Waves, RHODL Ratio) |
| `data_derivatives.csv` | funding_rate, total_oi, `oi_<13 bursa>` (BTC) | dipakai (Funding & OI) |
| `data_fg.csv` | Fear & Greed (tanpa harga) | dipakai (Fear & Greed) |
| `data_pl.csv` | realized profit/loss BTC, rpl_ratio, sth/lth_pl_ratio, rrp, rrl, relative_realized_pl | ⚠️ ratio rusak (bagian 6) |
| `data_realized_cap.csv` | realized_cap_usd, lth/sth_realized_cap_usd | kandidat |
| `data_rhodl.csv` | rhodl_ratio, realized_cap_1w, realized_cap_1_2y | kandidat |
| `data_cdd.csv` | cdd, vdd_30d_ma, vdd_365d_ma, vdd_multiple (tanpa harga) | ditunda (bagian 6) |
| `data_exchange.csv` | total_balance, net_flow, inflow, outflow | kandidat |
| `data_apparent_demand.csv` | apparent_demand | kandidat |
| `data_treasury_2y.csv` | treasury_2y_yield (bulanan) | kandidat |
| `data_lth_flow.csv` | lth_pl_price, lth_pl_flow_btc | skip |
| `data_futures_basis.csv` | annualized_basis_3m, … | skip |
| `data_sentiment.csv` | trend_*, wiki_* | skip (Google) |

**Hasil cek kualitas kandidat (17 Sep; jangan diulang kecuali data berubah):**
- **Realized Cap:** bersih (LTH + STH = total ≤ 0,01 %); loncatan LTH +7,2 % 26 Apr 2026 wajar (koin 22 Nov 2025 genap 155 hari). Isinya ≈ RP × supply, mirip Price Levels.
- **Exchange:** net = in − out persis. ⚠️ 8 hari 2026 inflow = outflow = 0 (data kosong diisi nol: 8 Apr, 18–19 Apr, 7 & 10 Mei, 12 & 28 Jul, 5 Agt). ⚠️ `btc_price` beda sumber di 2026 (maks 16 %) → pakai harga `data_mvrv`. Lompatan −100k BTC 28 Jul 2021.
- **RHODL (`data_rhodl.csv`):** = persen RC 1d–1w ÷ 1y–2y, tanpa pengali umur pasar Glassnode; puncak 443 (2011), p99 sejak 2012 = 37. Didominasi penyebut.
- **Apparent Demand:** hari pertama −952k (artefak), lonjakan +325k 22 Nov 2025; dua kali diuji sebagai sinyal → REJECT (data_dictionary).
- **Treasury 2Y:** bulanan 1976 – Agt 2026; pipeline masih perubahan user yang belum di-commit.
- **Skip:** LTH Flow (`lth_pl_flow_btc` bukan BTC, dibulatkan 4 desimal, 171 hari macet); Futures Basis (1 baris); Google Trends (ditulis ulang tiap update). Wikipedia views stabil sejak Jul 2015.
- **Revisi ChartInspect:** 10 Sep 2026 (commit data `c99e761`) seluruh sejarah AVIV, realized cap HODL, VDD MA, LTH flow dihitung ulang (median 0,1–0,6 %, terbesar ±12 % Mar 2020); revisi kecil 27 Agt. Di luar itu data on-chain stabil.

**Perhatian umum:** angka ChartInspect tidak entity-adjusted (tidak sama dengan Glassnode). Kalau halaman menyentuh threshold/zona/sinyal framework, **baca `references/Decision_Framework v2.md` dulu**; Claude Code tidak mengambil keputusan investasi.

---

## 8. Cara memilih warna

1. Skrip `validate_palette.js` skill dataviz tidak ada di mesin ini → pakai hitungan Python sekali pakai: hex → CIE Lab, jarak ΔE76 tiap calon terhadap semua warna garis yang ada, ulangi setelah simulasi deuteranopia & protanopia (ambil terkecil). Selalu ikutkan oranye BTC `#F7931A`.
2. Patokan longgar (permintaan user): tidak mirip oranye BTC; normal ≥ ±30, buta warna ≥ ±14. Buang calon yang jaraknya satu digit ke oranye saat buta warna (mustard `#c9a227` = 2).
3. Jangan paksa semua garis sama terang — beda terang tipis membantu mata buta warna.
4. Opasitas redup Highlight dihitung per warna supaya kontras redup **1,70:1** terhadap latar chart `#131722` (MVRV 0,49 · STH 0,44 · LTH 0,39 · BTC 0,28 · putih 0,17).
5. Selalu tunjukkan pratinjau widget dengan data asli sebelum bertanya.

---

## 9. Jebakan teknis

### Streamlit 1.63.0 (dikunci di `requirements.txt`; GitHub Actions tidak membacanya)
- **`st.navigation` membuang nilai widget halaman lain** walau key sama → nilai yang harus bertahan disimpan di key biasa (`{k}_mem`, `tooltip_pref`), widget disemai dari situ.
- **`st.rerun()` membuang nilai widget yang belum sempat digambar** di putaran itu → jangan pakai; ubah nilai lewat `on_click=`/`on_change=` callback. Mengubah nilai widget di badan `if st.button(...)` → `StreamlitWidgetAlreadyInstantiatedError`.
- **Iframe komponen dibangun ulang kalau urutan elemen di atasnya berubah**; penanda tetap di DOM induk bisa tertinggal dari konteks mati → pakai nomor unik per muatan.
- Opsi `--theme.*` apa pun membuat tema jadi terang → wajib `--theme.base dark`.
- Jangan `display:none` pada `stHeader` (tombol pembuka sidebar ada di dalamnya); pakai `pointer-events:none` pada `header *`, nyalakan lagi untuk `stExpandSidebarButton`.
- `stMarkdownContainer` dan caption punya `margin-bottom:-16px` (isi jatuh 8 px di kolom `vertical_alignment="center"`) → batalkan dengan `margin-bottom:16px`.
- Tinggi tombol dipaku 32 px → timpa `height` langsung. Teks `st.button` duduk di garis dasar → `display:block` + `line-height` pada `p`.
- Isi popover di portal terpisah → CSS lewat `[data-testid="stPopoverBody"]`. Popover tertutup oleh `click` di luar/Escape (chart meneruskan keduanya ke induk).
- Kalender tanggal milik browser → hanya `accent-color`. Atribut 1.63: radio terpilih `data-selected`. Fokus bawaan merah → timpa teal.
- `st.navigation` menaruh menu di atas sidebar → dibalik dengan flex `order`. `st.Page` fungsi: identitas dari `url_path`; halaman `default=True` beralamat `/`.
- Sidebar yang baru dibuka terbaca lebar 0 ±1 detik (animasi).
- Legend di dalam chart tidak bisa membuat pane → saklar pane harus kontrol Python.

### lightweight-charts 4.2.3
- `minBarSpacing` 0.005 supaya `fitContent()` muat ~5.900 titik. `fitContent()` gagal selama lebar chart 0 → tampilan awal diulang lewat poller.
- Kesiapan diukur dari pane utama (skala waktu pane harga tersembunyi, lebar 0). `priceScale().width()` 0 sampai chart menggambar.
- Tebal garis tidak dibulatkan → pakai bilangan bulat (2 px), pecahan tampak tipis.
- `chart.resize(w,h,true)` mengubah rentang tampil → jangan dipakai untuk "paksa gambar ulang".
- Lebar sumbu antar-pane harus disamakan (`minimumWidth`), diulang setelah zoom. Lebar area gambar mengendap 1–2 detik (label sumbu) → zoom yang dipasang harus dijaga selama fase pemulihan, bukan dicek sekali.
- Sumbu berentang tetap lewat `autoscaleInfoProvider` tetap memakai ruang tepi 20/10 % → `scaleMargins` kecil + formatter kosongkan di luar rentang. Tidak ada perintah atur rentang sumbu di v4 (hanya v5).
- **Format angka sumbu & label nilai terakhir diambil dari seri PERTAMA di skala itu, walau seri itu mati** → garis acuan mewarisi precision; seri mati diparkir (`priceScaleId: 'parkir_<kolom>'`).
- Memindah seri antar-sumbu: `applyOptions({priceScaleId})`. Warna angka per sumbu: `priceScale(side).applyOptions({textColor})`.
- Warna per titik mengalahkan warna seri → saat Highlight redup, `setData` ulang.
- Seri tambahan buatan browser (kembaran Loss, band bertumpuk) harus ikut `seriesOn`, `resetScales`, dan daftar tangga. Seri `visible:false` tidak ikut autoscale.
- **Seri yang dibuat belakangan tergambar di atas** → band bertumpuk dibuat duluan (tua → muda), garis sesudahnya.
- Menarik angka sumbu = mengubah skala (`handleScale`); menarik area hanya menggeser sumbu utama pane yang autoscale-nya mati.
- Pola garis hanya 5 (Solid, Dotted, Dashed, LargeDashed, SparseDotted); tangga hanya terlihat kalau satu bar beberapa piksel.

### Alat kerja
- **`TEMPLATE` di `lw_chart.py` string Python biasa** → JavaScript tanpa backslash (regex `[(]([0-9]+)[)]`). Cek: `python -W error::SyntaxWarning`, lalu ekstrak `<script>` ke file dan `node --check`.
- **Patch file:** file repo CRLF/LF campur → baca bytes, olah `\n`, kembalikan ke aslinya. Heredoc Bash panjang dengan banyak kutip bisa gagal di-parse → tulis skrip Python ke scratchpad dengan Write, lalu jalankan. `git commit -m` di PowerShell rusak dengan kutip ganda → `git commit -F <file>`.
- Output Python di Windows: `PYTHONIOENCODING=utf-8` kalau mencetak σ/→.
- **Panel browser Claude tidak selalu bisa dipercaya:** frame chart membeku kalau lama tanpa input (screenshot/hover membangunkannya); `setVisibleLogicalRange` antre sampai frame berikutnya → satu langkah per skrip lalu screenshot. Garis silang tidak bisa dipicu dari JS → pakai `computer hover`, baca `#tip`. Klik JS ke widget Streamlit (`el.click()`) tetap andal. Screenshot di viewport emulasi kadang terpotong 1:1 → untuk interaksi pakai event sintetis dengan posisi `getBoundingClientRect`. Screenshot kadang timeout → ulangi. "Range All tidak penuh" di panel = artefak frame belum tergambar.
- Panel Claude memblokir Fullscreen API dan tidak bisa membuka `file://` → layar penuh diuji user; pratinjau pakai `show_widget` (data disampel mingguan/dua mingguan; pastikan JSON benar-benar ditempel). Uji layar penuh semu: `Object.defineProperty(document,'fullscreenEnabled',{configurable:true,get:()=>false})`.
- Emulasi HP (`resize_window` mobile) mengaktifkan `pointer: coarse`, tapi gerakan jari tidak bisa ditiru → uji sentuh oleh user (localhost tidak terbuka dari HP user; uji lewat Streamlit Cloud).
- Membaca format angka seri dari browser: `series.priceFormatter().format(v)`.
- Chart terbuka di zoom/legend aneh dari percobaan lama → `localStorage.removeItem('dash_v2_<key>')` lalu reload.
- Windows MAX_PATH: venv di path temp panjang membuat `pip install streamlit` gagal.

---

## 10. Cara menjalankan

```bash
streamlit run app.py
```

`.claude/launch.json`: `dashboard-lama` (8501, `archive/app_v1.py`), `dashboard-v2` (8502), `dashboard-v2-uji` (8503, dipakai sesi Claude Code). Tema dibaca dari `.streamlit/config.toml`; opsi `--theme.*` di launch.json nilainya sama dan sudah menyertakan `--theme.base dark`.
