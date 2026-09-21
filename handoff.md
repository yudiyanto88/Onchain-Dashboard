# Handoff — Dashboard Streamlit v2

Diperbarui 21 Sep 2026 (versi ringkas; terakhir sesudah `1ad0aa6`). Versi lengkap sebelum diringkas — cerita pengerjaan tiap fitur, opsi yang ditolak, hasil ukur piksel — ada di `archive/handoff_riwayat_2026-09-17.md` (buka hanya kalau perlu detail sejarah; nomor bagian 3.x yang disebut di bawah merujuk ke file itu).

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

- **Live (15 halaman, 6 kelompok):** Valuation (MVRV · Price Levels · AVIV · Realized Cap) · Profitability (SOPR · NUPL · Unrealized P/L · Supply in Profit) · Holder Behavior (HODL Waves · RHODL Ratio · LTH/STH Supply) · Exchange (Exchange Flow) · Derivatives (Funding Rates & Open Interest) · Sentiment & Macro (Fear & Greed · BTC vs Stocks & Gold). Semua halaman: slider rentang, nyaman di HP, kontrol diingat per halaman, tombol Style di chart.
- **Langkah pertama sesi baru:**
  1. Cek server `dashboard-v2-uji` (bagian 2), buka halaman, lihat keadaannya sebelum mengubah apa pun.
  2. Tanyakan apakah Streamlit Cloud perlu **Reboot app** sesudah push terakhir (`dashboard/` berubah).
  3. Tanyakan apakah **Cohort State** (bagian 6) sudah boleh dilanjutkan, lalu **halaman berikutnya** (kandidat dan hasil cek data di bagian 7 — jangan dicek ulang; rencana VIX / Dollar & Yields di bagian 6).
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
- **Localhost uji: http://localhost:8503** (server `dashboard-v2-uji` di `.claude/launch.json`); "nyalakan localhost" = server ini. **Wajib restart sesudah mengubah `dashboard/`** — tanpa itu kode baru tidak terbaca. Cek dulu `curl http://localhost:8503/_stcore/health`: server bisa tetap hidup sesudah sesi Claude Code ditutup, dan sisa sesi lama hanya bisa dimatikan dengan izin user (`preview_stop` tidak mempan, `Stop-Period`-style `Stop-Process` ditolak pengaman). User juga bisa menjalankan sendiri: `streamlit run app.py --server.port 8503`.
- **Handoff:** jangan diedit tanpa persetujuan; daftarkan usulan poin dulu (kecuali user sudah minta dicatat).
- **Git:** commit hanya file dashboard yang relevan + handoff, dan hanya kalau user minta. Repo punya banyak perubahan user yang belum di-commit (`CLAUDE.md`, `references/`, `research/`) — jangan ikut. Sebelum push **merge dulu dari GitHub** (`git fetch`; `git diff --name-only HEAD...origin/main` — kalau hanya `data_*.csv` dan `alerts/logs/`, aman). Sesudah push yang mengubah `dashboard/`, ingatkan **Manage app → ⋮ → Reboot app** bila versi online error (Streamlit Cloud tidak membaca ulang modul).

---

## 3. Halaman live

Semua: BTC oranye `#F7931A` (kecuali HODL Waves), key localStorage `dash_v2_<key>`. Warna kohort konsisten: semua holder navy `#0070a6`, STH rust `#bf5546`, LTH teal `#0b8e89`. Garis ambang framework **tidak** dipasang di halaman mana pun (keputusan framework).

| Menu / alamat | Loader & kolom | Bawaan & bentuk | Catatan data / keputusan |
|---|---|---|---|
| **MVRV** `/` (key `market_valuation`) | `load_mvrv` — `data_mvrv.csv`; Rolling Z-Score 1y/2y/4y dihitung | BTC Separate pane, metrik & harga Log; LTH MVRV sumbu kanan; **Median MVRV biru langit `#6fb6de`** sumbu kiri, nyala awal; ref Neutral 1.0; pane bawah **Z-Score** (Hidden, sumbu kanan): Z-Score navy 80 % + Rolling hijau `#97c459` 55 % (2y/4y mati awal) | LTH MVRV bisa puluhan (2011: 374). Z-Score full-history untuk aturan, rolling untuk mata (KB MVRV). Tanpa pita "extreme" berambang tetap. Median MVRV dari `data_median_mvrv.csv` (loader bersama `_median_mvrv`): puncak siklus di atas MVRV rata-rata (2013: 11,3 vs 4,95), dasar tetap ~1; bukan bagian framework v2 |
| **Price Levels** `/price-levels` | `load_price_levels` — `data_price_level.csv` + AVIV Mean/Upper dari `data_aviv.csv` | Overlay, satu sumbu kanan, skala Auto. STH RP, Realized Price, LTH RP, **True Market Mean hijau zamrud `#3fa96b`**, **Median RP biru langit `#6fb6de`**, AVIV Mean `#7b65d2`, AVIV Upper `#a58df0`, CVDD `#a8963f`; mati awal: MVRV 0σ, 200 DMA, 50 WMA, 200 WMA (abu). Pane bawah **Price / CVDD** (Hidden, `extra_scale="Log"`, sumbu kanan, olive); **Price / RP** navy mati awal | Price/CVDD dipakai framework v2 K4 (#4 < 1,10; flag ≤ 1,0) — garis ambang tidak dipasang; Price/RP untuk divergence KB §4.3. AVIV dihitung ulang `btc_price/aviv_ratio × band` (kolom `price_at_aviv_*` salah basis ±9–10 %), 84 hari pertama disembunyikan (`_aviv_awal`). Detail data di docstring `load_price_levels`. Median RP dari `data_median_mvrv.csv`, warnanya sengaja sama dengan Median MVRV di halaman MVRV (satu metrik satu warna, pola kohort); TMM pindah ke hijau zamrud karena warna itu dilepas |
| **AVIV** `/aviv` | `load_aviv` — `data_aviv.csv` (satuan rasio) | Separate pane, Log/Log; AVIV Ratio navy, Mean violet, Upper (+0.5σ) violet muda, sumbu kanan; kelompok **σ Bands** (+1σ +2σ −1σ −2σ, abu, mati awal); pane bawah **Deviation (σ)** menyala awal (`extra_default`), sumbu kanan | Rasio ≥ Upper ⇔ harga ≥ AVIV Upper (1.279 hari sejak 2011). Band bawah negatif s/d 2014 dikosongkan |
| **Realized Cap** `/realized-cap` (key `realized_cap`) | `load_realized_cap` — `data_realized_cap.csv` (% dan 30d change dihitung) | Separate pane, metrik & harga Log; total navy, LTH teal, STH rust (compact 1.07T); saklar **USD \| %** (bawaan USD; % tanpa garis total); **Realized Cap 30d Change (%)** batang di pane harga sumbu kiri, Overlay/Hidden → pane bawah kanan (pola LTH/STH Supply) | Kelompok Valuation (penyebut MVRV; RP = RC ÷ supply). 30d change 2011–2013 ratusan persen → batang sesudahnya gepeng, **sengaja tidak dikosongkan** (user: cukup di-zoom). Tidak dipakai framework. Detail di docstring `load_realized_cap` |
| **SOPR** `/sopr` | `load_sopr` — `data_momentum.csv` | Separate pane, Log/Log; LTH-SOPR sumbu kanan; Break-even 1.0 di semua sumbu; pane **SOPR Gap** (Hidden, sumbu kanan) | **Gap = SMA90(STH-SOPR) − SMA60 dari SMA90 itu (KB §12)** — `alert_check.py` memakai SMA60 − SMA90 (bagian 6). SOPR 3 desimal, gap 5, LTH ≥ 100 tanpa desimal |
| **NUPL** `/nupl` | `load_nupl` — `data_momentum.csv` | Separate pane, metrik Auto, harga Log; ketiga garis sumbu kanan; Break-even 0; pane **NUPL Gap** (LTH − STH, Hidden, sumbu kanan) | Ratio LTH/STH sengaja tidak dimuat (melompat saat STH ≈ 0). Sumbu tidak dipaku −1..1 |
| **Unrealized P/L** `/unrealized-pl` (key `unrealized_pl`) | `load_unrealized_pl` — **dihitung sendiri** dari `data_hodl_waves.csv` + `data_realized_cap.csv` + `data_supply.csv` | Judul "Relative Unrealized Profit & Loss by Cohort"; Separate pane, harga Log, metrik Auto; 4 garis **semua positif**: LTH profit teal + LTH rugi aqua `#38d1b4` di **sumbu kiri**, STH profit rust + STH rugi `#dc9390` di **sumbu kanan** (STH jauh lebih kecil). Tanpa garis NUPL | Tiap band umur: nilai pasar (porsi supply × market cap) − nilai beli (porsi realized cap × realized cap); selisih + masuk profit, − masuk rugi; band 6m+ = LTH. Untung − rugi = NUPL dari MVRV (selisih maks 0,00015 seluruh 5.908 hari). Overlay ditolak 18 Sep: harga menumpang sumbu metrik dan menggepengkannya. Nilai 2010–2011 ekstrem dibiarkan (zoom) |
| **Supply in Profit** `/supply-in-profit` | `load_supply` — `data_supply.csv` | Separate pane, sumbu 0–100 kanan; saklar **Profit / Loss** di chart (boleh dua-duanya/mati); warna Loss saat keduanya: `#839df0` `#dc9390` `#38d1b4` | Loss = 100 − Profit (kembaran di browser). 1 desimal |
| **HODL Waves** `/hodl-waves` (key `hodl_waves`) | `load_hodl_waves` — `data_hodl_waves.csv` (`RC <band>`, `Supply <band>`) | **Overlay, garis BTC putih** (`btc_color`, `btc_dim` 0,17); 12 band area bertumpuk (`kind="stack"`), muda di bawah, spektrum `#d73027 … #9e7bd6`; saklar **Realized Cap \| Supply** (bawaan Realized Cap); tanpa Highlight/smoothing | Mematikan band di legend menumpuk ulang sisanya. Dulu bernama "RHODL Waves" `/rhodl-waves` |
| **RHODL Ratio** `/rhodl-ratio` | `load_rhodl_ratio` — `data_hodl_waves.csv` | Judul "RHODL Ratio (6m–2y ÷ 1d–3m)"; **Overlay, metrik Auto, harga Log**; garis navy sumbu kiri | = RC (6m–12m + 1y–2y) ÷ (1d–1w + 1w–1m + 1m–3m), cocok persis `research/findings/_cohort_state_plane.csv`. **Bukan** `rhodl_ratio` di `data_rhodl.csv`. 86 % varians dari penyebut → jangan dibaca sendirian. Calon tempat Cohort State |
| **LTH/STH Supply** `/lth-sth-supply` (key `holder_supply`) | `load_holder_supply` — `data_supply.csv` (`lth/sth_supply_btc`; % dan LTH 30d Change dihitung) | Judul "Long- & Short-Term Holder Supply"; Separate pane, harga Log; garis LTH teal & STH rust (sumbu kanan saat Separate); saklar **BTC \| %** di chart (bawaan BTC, compact 16.51M). **LTH 30d Change** batang naik teal / turun rust (alpha 0,60) **di pane harga, di belakang harga, sumbu kiri**; saat BTC Overlay/Hidden pindah ke **pane bawah sumbu kanan** (tidak pernah hilang) | LTH + STH = supply beredar. Tidak entity-adjusted: koin lama pindah dompet → STH lalu kembali LTH 155 hari kemudian, jadi batang 30d sesekali ekstrem (± 1 juta BTC) — bukan bug. 30d = hari kalender. Riwayat stabil. Tidak dipakai framework. Tanggal lompatan di docstring `load_holder_supply` |
| **Exchange Flow** `/exchange-flow` (kelompok Exchange) | `load_exchange` — `data_exchange.csv` + harga dari `data_mvrv.csv` | Separate pane; Exchange Balance navy (sumbu kanan saat Separate); pane **Net Flow** menyala awal: batang **masuk teal / keluar rust**, **sumbu kanan**; tanpa garis Zero, tanpa smoothing | `net_flow` + = masuk bursa; selisih saldo = net flow. Nilai sebelum 2012 dikosongkan (pindah dompet ratusan ribu BTC sehari); hari inflow = outflow = 0 (8 hari 2026) = data kosong → arus dikosongkan, saldo tetap. Harga file ini beda sumber → pakai `data_mvrv`. Detail di docstring `load_exchange` |
| **Funding Rates & Open Interest** `/funding-oi` | `load_derivatives` — `data_derivatives.csv` (+13 kolom `oi_<bursa>`) | Separate pane; funding batang dua warna (teal/rust) kanan, OI garis violet kiri, satu pane; ref Zero ikut sumbu funding; saklar **OI BTC \| USD** (boleh dua-duanya); pane **OI Change (1d)** (Hidden) | Funding tanpa satuan (4 desimal). `total_oi` = jumlah 13 bursa; ΔOI hanya bursa yang OI > 0 kemarin & hari ini (cakupan bursa bertambah 2020–2025). OI USD = OI × harga |
| **Fear & Greed** `/fear-greed` | `load_fear_greed` — `data_fg.csv` + harga dari `data_mvrv.csv` | Separate pane, sumbu 0–100 kanan; garis bergradasi rust→abu→teal; **SMA30 Band kuning `#F7E9A8` menyala awal**; nama kelas di tooltip | Kelas API: ≤25 Extreme Fear · 26–46 Fear · 47–54 Neutral · 55–75 Greed · ≥76 Extreme Greed. Label nilai terakhir SMA30 di sumbu tertulis bulat (format seri pertama) |
| **BTC vs Stocks & Gold** `/btc-stocks-gold` (key `btc_tradfi`) | `load_btc_tradfi(window)` — `data_tradfi.csv` (Pipeline 23, Yahoo `^GSPC`/`GC=F`) + harga dari `data_mvrv.csv`; libur bursa di-ffill | Overlay, harga Log kanan, Z kiri. Z log(BTC/pembanding) **batang rust (atas nol) / teal (bawah)** 80 %; saklar **S&P 500 | Gold** di chart, boleh dua-duanya: S&P 35 % padat + Gold **garis olive `#a8963f`**. **Kotak Window menggantikan Smoothing**: 6m · 1y · 2y · 4y + isian hari, bawaan 365d | Rumus = `research/analyze_btc_spx_zscore.py`. Tanpa ambang ±2/titik sinyal (riset: masih hipotesis) |

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
- Pane: `price` (BTC Separate pane) → `main` → `extra` (`extra_label`, `extra_default`, skala `extra_scale` bawaan linear; sisi sumbu dari `Series.axis`, bawaan kiri — semua pane bawah kanan kecuali OI Change).
- Seri `pane="price"` digambar di pane harga sebelum garis BTC; sisinya selalu linear; saat Overlay/Hidden pindah ke pane bawah sumbu kanan. Pembatas antar pane putih 22 % (`#panes > div + div::before`).
- Zoom dan lebar sumbu tersinkron; sumbu waktu hanya di pane terbawah; slider rentang (isi BTC Log) di bawah semua.
- Sumbu: `axis` bawaan + `separate_axis` saat Separate pane (aturan user: metrik berskala sama ke kanan saat Separate pane). `metric_range` (sumbu tetap, angka bulat tanpa desimal, di luar rentang kosong). Angka sumbu disembunyikan (lebar tetap) kalau semua garis di sisi itu mati. Seri mati diparkir ke skala lain supaya format sumbu tidak kacau.
- Jenis seri: garis, histogram (`negative_color` dua warna), gradasi per titik (`gradient`), area bertumpuk (`kind="stack"`, `stack_index`, `stack_cols` + `stack_units`), kembaran Loss (`complement`).
- Legend berkelompok (garis utama + kotak angka periode/anggota), `hidden_default` (sekali, dicatat di `seen`), Highlight multi (redup kontras 1,70:1; disembunyikan kalau hanya BTC), tarik chart menggeser sumbu garis yang disorot, klik dua kali reset.
- Saklar di chart: Profit/Loss, satuan (`unit_switch`/`unit`/`pair`/`compact`), bobot tumpukan (`stack_units`). Tersimpan di localStorage.
- `Series.show_when` ("alone"/"together" menurut saklar satuan; "together" tanpa group = kembaran, induk = seri berkolom sama), `alpha_together`; `MetricFamily.window_days` ({label: hari}) = kotak Window ganti Smoothing, `loader(window)`.
- Format angka per seri: `precision`, `whole_from`, `compact` (K/M/B/T); garis acuan mewarisi format metrik di sumbunya. Data dikirim dengan desimal `max(4, precision+1)`.
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
- Semua garis utama **2 px** (`LINE_WIDTH`). Palet kohort navy/rust/teal setara terang. **Navy `#0070a6` = warna dasar metrik utama semua halaman** (kecuali pengecualian yang disetujui); cornflower `#5b8def` ditolak (mirip violet AVIV, lebih terang dari rust/teal). Uji buta warna = cek cepat, bukan syarat mutlak.
- Legend berkelompok per metrik; **BTC Price selalu terakhir** di legend, tombol sorot, tooltip. Tanpa simbol/marker smoothing. Tingkat terang legend / angka periode / tombol sorot sengaja berbeda (hierarki). Label "Highlight" setara tombol.
- Kotak Display tidak menghitung BTC. Popover Scale memakai nama metrik.
- Tombol layar penuh satu, di dalam chart. Line style di **tombol Style dalam chart (opsi B)**, bukan popover dan bukan klik kanan kotak periode.
- Tooltip bawaan **Cursor**, latar 94 %.
- Garis pembatas antar pane **22 %** (dipilih dari 10/16/22/28 %). Pane bawah dengan legend tetap masuk legend (Price/CVDD: supaya Price/RP bisa dinyalakan).
- Slider rentang: isi BTC, semua halaman, 52 px. Range memindahkan jendela (pilihan B).
- HP: tahap 2 (chart lebih pendek, angka ringkas, tombol legend besar) **ditolak**. Angka sumbu terpotong di tepi pane dibiarkan.
- Z-Score di pane ketiga (bukan di chart MVRV), histogram polos (gradasi ditunda), tanpa pita ambang tetap.
- **Unrealized P/L dihitung sendiri, bukan dari endpoint `relative-unrealized-pl-by-cohort`.** Sisi untung kedua sumber sama (LTH 0,349 vs 0,350 pada 18 Agt 2026), tapi sisi rugi endpoint jauh lebih besar (0,501 vs 0,156) sehingga NUPL-nya berlawanan tanda dengan halaman NUPL (−0,15 vs +0,23) dan tidak bisa direkonsiliasi dengan realized cap ChartInspect sendiri. NUPL tetap satu sumber: halaman NUPL.
- Keputusan per halaman ada di tabel bagian 3.

---

## 6. Ditahan / ditunda / belum diputuskan (tanyakan dulu)

- **Cohort State (DITAHAN user 17 Sep — "ada yang perlu dipastikan dulu"):** dua sumbu (Demand Impulse dan Aged Cohort Turnover) jadi empat state, rencananya digabung ke halaman **RHODL Ratio**. **Penghalang: data ACT belum ada di CSV repo** — butuh pipeline baru di `auto_update.py` yang menyimpan `data_profit_by_age.csv`, dan izin user masih ditahan. Rumus, nama state, warna, dan jawaban user ada di `archive/handoff_riwayat_2026-09-17.md` (bagian "Dipindah dari handoff ringkas"); analisanya di `research/analyze_cohort_state_plane.py`. Bukan bagian framework v2.
- **CDD/VDD (ditunda user, belum butuh):** `vdd_multiple` di CSV berisik (VDD harian ÷ MA365). Usulan waktu itu: rumus Glassnode `vdd_30d_ma / vdd_365d_ma`, ref 1,0, CDD batang navy, VDD violet. Research menolak "VDD multiple < 1" sebagai filter. Angka per siklus ada di arsip.
- **Realized P/L (ditunda):** `data_pl.csv` — `rpl_ratio` dan `sth/lth_pl_ratio` rusak (melonjak/macet). Yang sehat: profit/loss BTC, `rrp`, `rrl`, `relative_realized_pl`. Tidak ada KB; kalau dilanjutkan, KB dulu di Claude.ai, ratio dihitung ulang dari jumlah 30 hari.
- **Temuan framework (user cek di Claude.ai; jangan ubah framework/data_dictionary):** `Decision_Framework v2.md` menulis "703 hari Z5"; rumus AVIV benar = **1.279 hari**, dengan kolom `price_at_aviv_*` salah basis = 710 → angka framework kemungkinan dari kolom salah basis (masih dianjurkan `references/data_dictionary.md`).
- **Rumus gap STH-SOPR `alerts/alert_check.py` (`_sth_sopr_ma_gap`) = SMA60 − SMA90, beda dari KB §12** (10 Jan 2021: +0.01141 vs KB +0.02447; dipakai trigger K1 dan alarm bear). Menunggu user; jangan dibetulkan diam-diam.
- **Pola umum seri yang "numpang" di pane harga (`Series.pane="price"`) — belum diputuskan (user 17 Sep: bahas nanti kalau ada kasus lain).** Sekarang hanya LTH 30d Change; perilakunya (pindah ke pane bawah sumbu kanan saat Overlay/Hidden) tertulis di `metric_page` untuk semua seri `pane="price"`.
- **`data_relative_unrealized_pl_by_cohort.csv` + pipeline 20 `auto_update.py` dibiarkan jalan** (keputusan user 18 Sep) sebagai pembanding, tidak dipakai halaman mana pun. Data berhenti 30 hari di belakang (paywall versi gratis).
- **Ingatan kontrol setelah reload** (pilihan b, lewat URL query) — belum diminta.
- **Kotak L/R untuk pilihan sumbu** — ditahan (tidak menghemat lebar).
- **Tombol Range di celah kanan baris kontrol** (preset + kalender dua bulan gaya CryptoQuant) — ditahan user ("belum perlu").
- **Usulan disetujui tapi belum diterapkan:** latar brand `#0D1117`; font JetBrains Mono (angka/sumbu) + Inter (label). Ide overlay dua chart bertumpuk untuk banyak skala — dinilai user "slightly over modif".
- **Belum dibahas/dilaporkan kecil:** label nilai terakhir bertumpuk di sumbu saat banyak smoothing (kandidat: `lastValueVisible` false untuk smoothing — tanya dengan pratinjau); Supply in Profit saat Profit & Loss mati legend tidak dicoret; gradasi histogram Z-Score; judul HODL Waves tidak berubah saat saklar Supply.
- **Rencana macro (user 21 Sep, belum dikerjakan):** halaman **VIX** (`^VIX`) dan **Dollar & Yields** (DXY `DX-Y.NYB`, US 2Y/10Y dari FRED DGS2/DGS10 — `data_treasury_2y.csv` cuma bulanan, spread 10Y−2Y). Ticker Yahoo = satu baris `TRADFI_TICKERS`.
- **Ide nanti:** pantau LTV intraday dengan harga 10 menit ChartInspect (`https://chartinspect.com/api/charts/crypto/intraday-price?cryptocurrency=bitcoin&resolution=10&from=<unix>&to=<unix>`, `{t, p}`, gratis 30 hari).

---

## 7. Data: CSV, kualitas, kandidat halaman

Semua file punya `date`; sebagian besar punya `btc_price`. Bukan untuk halaman: `data_master_all_metrics.csv`, `data_*_events.csv`.

**Sudah dipakai halaman** (kolom & keputusan ada di bagian 3): `data_mvrv.csv` · `data_price_level.csv` (TMM ≈ harga ÷ AVIV Ratio, beda harian ±5 %; `cum_pl_price`, `pl_price_ratio` belum dipakai) · `data_aviv.csv` (`price_at_aviv_*` **salah basis**; `liveliness`, `investor_cap` belum dipakai) · `data_momentum.csv` (`net_realized_pl_usd` belum dipakai) · `data_supply.csv` · `data_hodl_waves.csv` · `data_realized_cap.csv` · `data_derivatives.csv` · `data_exchange.csv` · `data_fg.csv` · `data_median_mvrv.csv` · `data_tradfi.csv`.

| File belum dipakai | Kolom | Status |
|---|---|---|
| `data_pl.csv` | realized profit/loss BTC, rpl_ratio, sth/lth_pl_ratio, rrp, rrl, relative_realized_pl | ⚠️ ratio rusak (bagian 6) |
| `data_relative_unrealized_pl_by_cohort.csv` | sth/lth_rup, sth/lth_rul, sth/lth_nupl | ⚠️ sisi rugi tidak konsisten dengan realized cap (bagian 5); halaman Unrealized P/L memakai hitungan sendiri |
| `data_rhodl.csv` | rhodl_ratio, realized_cap_1w, realized_cap_1_2y | kandidat |
| `data_cdd.csv` | cdd, vdd_30d_ma, vdd_365d_ma, vdd_multiple (tanpa harga) | ditunda (bagian 6) |
| `data_apparent_demand.csv` | apparent_demand | kandidat |
| `data_treasury_2y.csv` | treasury_2y_yield (bulanan) | kandidat |
| `data_lth_flow.csv` | lth_pl_price, lth_pl_flow_btc | skip |
| `data_futures_basis.csv` | annualized_basis_3m, … | skip |
| `data_sentiment.csv` | trend_*, wiki_* | skip (Google) |

**`auto_update.py`** (audit ponytail 21 Sep, CSV terbukti identik): helper `simpan()` dan `baca_median_mvrv()`; normalisasi tanggal hanya di `fetch_data` dan saat membaca CSV. Pipeline 23: hari bursa saja, sejarah ditarik ulang tiap jalan, ticker gagal = kolom lama tetap.

**Hasil cek kualitas kandidat (17 Sep; jangan diulang kecuali data berubah):**
- **RHODL (`data_rhodl.csv`):** = persen RC 1d–1w ÷ 1y–2y, tanpa pengali umur pasar Glassnode; puncak 443 (2011), p99 sejak 2012 = 37. Didominasi penyebut.
- **Apparent Demand:** hari pertama −952k (artefak), lonjakan +325k 22 Nov 2025; dua kali diuji sebagai sinyal → REJECT (data_dictionary).
- **Treasury 2Y:** bulanan 1976 – Agt 2026.
- **Skip:** LTH Flow (`lth_pl_flow_btc` bukan BTC, dibulatkan 4 desimal, 171 hari macet); Futures Basis (1 baris); Google Trends (ditulis ulang tiap update). Wikipedia views stabil sejak Jul 2015.
- **Median MVRV (`data_median_mvrv.csv`, cek 18 Sep 2026):** 5.878 baris, 17 Jul 2010 – 18 Sep 2026; min 0,60 · median 1,78 · maks 73,77 (2011). Baris resmi berhenti 18 Agt 2026 lalu melompat ke 18 Sep 2026 — **30 hari kosong**, dan baris terakhir itu `source = urpd_formula` (dihitung dari URPD, bukan angka resmi). Keputusan user 18 Sep: tampilkan apa adanya. `series_points` membuang baris kosong, jadi garisnya tersambung melewati lubang, tidak putus.
- **`data_tradfi.csv` (21 Sep):** sejak 4 Jan 2010, tanpa 0/macet, lonjakan > 10 % hanya asli (Mar 2020, Jan 2026), 6 tanggal libur beda.
- **Revisi ChartInspect:** 10 Sep 2026 (commit data `c99e761`) seluruh sejarah AVIV, realized cap HODL, VDD MA, LTH flow dihitung ulang (median 0,1–0,6 %, terbesar ±12 % Mar 2020); revisi kecil 27 Agt. Di luar itu data on-chain stabil.

**Perhatian umum:** angka ChartInspect tidak entity-adjusted (tidak sama dengan Glassnode). Kalau halaman menyentuh threshold/zona/sinyal framework, **baca `references/Decision_Framework v2.md` dulu**; Claude Code tidak mengambil keputusan investasi.

---

## 8. Cara memilih warna

1. Skrip `validate_palette.js` skill dataviz tidak ada di mesin ini → pakai hitungan Python sekali pakai: hex → CIE Lab, jarak ΔE76 tiap calon terhadap semua warna garis yang ada, ulangi setelah simulasi deuteranopia & protanopia (ambil terkecil). Selalu ikutkan oranye BTC `#F7931A`.
2. Patokan longgar (permintaan user): tidak mirip oranye BTC; normal ≥ ±30, buta warna ≥ ±14. Buang calon yang jaraknya satu digit ke oranye saat buta warna (mustard `#c9a227` = 2).
3. Jangan paksa semua garis sama terang — beda terang tipis membantu mata buta warna.
4. Opasitas redup Highlight dihitung per warna supaya kontras redup **1,70:1** terhadap latar chart `#131722` (MVRV 0,49 · STH 0,44 · LTH 0,39 · BTC 0,28 · putih 0,17).
5. Selalu tunjukkan pratinjau widget dengan data asli sebelum bertanya.
6. Satu metrik = satu warna di semua halaman (aturan user 18 Sep 2026, seperti kohort navy/rust/teal): Median MVRV dan Median RP sama-sama `#6fb6de`. Kalau warna itu sudah dipakai garis lain di halaman tujuan, garis lama yang pindah.
7. Terang antar garis sejenis disamakan: `#8fd3ff` (11,02:1 terhadap latar chart) mengalahkan garis lain, `#6fb6de` (8,03:1) setara. Ukur kontras ke `#131722`, bukan menebak dari hex.

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
- **Sumbu Log di pane pendek hanya menampilkan 1–4 angka** kalau rentangnya lebar: pane bawah Price/CVDD (0,4–300) dan pane harga halaman berdata sejak 2010 (Exchange Flow, AVIV, LTH/STH Supply: $0,05–$120k). Penyebab belum dipastikan (dugaan: angka rapat dibuang / tertutup label nilai terakhir) — dibiarkan (keputusan user 17 Sep).
- **Unrealized P/L per band hanya batas bawah:** rincian cuma 12 band, jadi koin rugi di dalam band yang rata-rata untung tidak terhitung. Kedua sisi mengecil dalam jumlah yang sama, nilai bersihnya tetap tepat (dibuktikan: menggabungkan 12 band jadi 1 kelompok memberi untung 0,193 / rugi 0,000 — bersihnya sama).
- **Histogram rapat + rgba tembus pandang tampak pekat di Range All** (alpha menumpuk per piksel) → redup pakai warna padat `campurLatar`.
- **`RefLine` hanya digambar di pane tengah** (`metric_page`, dari seri non-`extra`) → garis acuan untuk pane bawah belum bisa; memasangnya di halaman berskala besar menarik sumbu pane tengah ke nilai itu.

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
- **Panel browser Claude tidak selalu bisa dipercaya:** frame chart membeku tanpa input (screenshot/hover membangunkannya), screenshot kadang timeout (ulangi), dan viewport emulasi kadang memotong gambar → verifikasi lewat `find`/`javascript_tool` (mis. `getComputedStyle`) kalau gambar tidak muncul. "Range All tidak penuh" = artefak frame belum tergambar. Garis silang hanya lewat `computer hover` (baca `#tip`); klik JS ke widget Streamlit (`el.click()`) andal; satu langkah zoom per skrip lalu screenshot.
- Panel memblokir Fullscreen API, `file://`, dan gerakan jari → layar penuh dan sentuh diuji user (lewat Streamlit Cloud; localhost tidak terbuka dari HP user). Pratinjau pakai `show_widget` dengan data disampel mingguan/dua mingguan. Uji layar penuh semu: `Object.defineProperty(document,'fullscreenEnabled',{configurable:true,get:()=>false})`.
- Membaca format angka seri dari browser: `series.priceFormatter().format(v)`.
- Chart terbuka di zoom/legend aneh dari percobaan lama → `localStorage.removeItem('dash_v2_<key>')` lalu reload.
- Windows MAX_PATH: venv di path temp panjang membuat `pip install streamlit` gagal.

---

## 10. Cara menjalankan

```bash
streamlit run app.py
```

`.claude/launch.json`: `dashboard-lama` (8501, `archive/app_v1.py`), `dashboard-v2` (8502), `dashboard-v2-uji` (8503, dipakai sesi Claude Code). Tema dibaca dari `.streamlit/config.toml`; opsi `--theme.*` di launch.json nilainya sama dan sudah menyertakan `--theme.base dark`.
