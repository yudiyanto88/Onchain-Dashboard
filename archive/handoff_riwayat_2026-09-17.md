# Handoff — Upgrade Dashboard Streamlit (v2)

Ditulis ulang: 17 September 2026 (pembaruan kedua belas: HODL Waves Overlay putih, halaman RHODL Ratio, Cohort State ditahan — di-push 17 Sep).
(Pembaruan kesebelas 17 Sep: halaman RHODL Waves, ingatan kontrol per halaman, tombol Style di dalam chart — dinyatakan valid user dan di-push 17 Sep; CDD/VDD ditunda).
(Pembaruan kesepuluh 17 Sep: halaman AVIV live — commit `045cd9a`; cek kualitas data 11 kandidat halaman; revisi data ChartInspect 10 Sep; temuan hitungan hari Z5 di framework; halaman berikutnya dipilih user: CDD/VDD).
(Pembaruan kesembilan 16 Sep: halaman NUPL, Funding Rates & Open Interest, Fear & Greed; OI per bursa di `auto_update.py`; saklar OI BTC | USD; angka sumbu per pane; Realized P/L ditunda — commit `24e1fe1`, `3fe3619`, dan commit Fear & Greed + handoff sesudahnya — semua live). Untuk dilanjutkan di sesi Claude Code berikutnya.
(Pembaruan kedelapan 15 Sep: dashboard nyaman di HP, tombol Scale untuk layar sentuh, layar penuh semu di iPhone, MVRV bawaan Separate pane + Log — commit `32a8abd` dan `024807a`.)
(Pembaruan ketujuh 14 Sep: slider rentang di bawah chart, Range memindahkan jendela (pilihan B), Supply in Profit bawaan Separate pane — commit `8bb65d7`.)
(Pembaruan keenam 14 Sep: halaman Supply in Profit, saklar Profit/Loss, sumbu 0–100, rapikan Price Levels, BTC terakhir di legend.)
(Pembaruan kelima 14 Sep: halaman SOPR, kotak Tooltip, menu berkelompok `st.navigation`, commit `073a997`.)
(Pembaruan keempat 13 Sep: v2 live, Price Levels, tooltip, garis 2 px. Versi 11 dan 12 Sep sudah dilebur ke sini.)

Baca dokumen ini dan `CLAUDE.md` sebelum mulai. Bagian **3 (keputusan pending)** harus ditanyakan ke user dulu — jangan langsung diterapkan.

---

## 1. Tujuan dan permintaan awal user

- **Tujuan:** upgrade dashboard Streamlit supaya halaman metriknya terasa seperti ChartInspect. Bukan menyalin kode mereka, tapi meniru pola tampilan dan cara pakainya dengan data sendiri (CSV hasil `auto_update.py`).
- **Urutan prioritas dari user:**
  1. Layout halaman metrik
  2. Fitur charting
  3. Struktur navigasi
  4. Tampilan
- **Pembagian halaman:** satu halaman per keluarga metrik (sekitar 17 halaman).
- **Pendekatan yang dipilih:** satu renderer dipakai semua halaman, konfigurasi metrik terpisah. Coba satu halaman dulu. Dashboard lama tidak boleh terganggu — sampai 13 Sep 2026, saat v2 menggantikannya (v1 diarsipkan di `archive/app_v1.py`).
- **Posisi sekarang (17 Sep 2026):** sepuluh halaman dalam lima kelompok menu — Valuation (MVRV, Price Levels, AVIV), Profitability (SOPR, NUPL, Supply in Profit), Holder Behavior (HODL Waves, RHODL Ratio), Derivatives (Funding Rates & Open Interest), Sentiment & Macro (Fear & Greed). Semuanya dengan slider rentang (bagian 3.2), nyaman di HP (bagian 3.15), kontrol diingat per halaman dan tombol Style di chart (bagian 3.24). HODL Waves (Overlay, garis BTC putih) dan RHODL Ratio (Overlay, Auto) live 17 Sep (bagian 3.26 dan 3.28). **Ditahan user:** halaman Cohort State (bagian 3.27). Halaman berikutnya belum dipilih (sisa kandidat bagian 3.23; CDD/VDD ditunda, bagian 3.25). Halaman baru tinggal menambah `MetricFamily` dengan `group` dan `url_path`.

---

## 2. Cara kerja yang disukai user

- Chat pakai **bahasa Indonesia yang simpel**, singkat tapi jelas. Istilah teknis (MVRV, SOPR, dll.) tetap English. **Teks di dashboard pakai bahasa Inggris.**
- User **tidak bisa menilai dari kode atau kode hex warna**. Untuk urusan tampilan/warna, **langsung buat widget pratinjau inline** (`show_widget`) memakai data CSV asli — bukan file HTML terpisah. Localhost dipakai untuk mengecek dashboard sungguhan.
- User sering bilang **"jangan eksekusi dulu"**. Jelaskan pemahaman, tunggu konfirmasi, baru kerjakan. Kalau user mengirim foto, itu cara tercepat menyamakan maksud.
- Kalau ada pilihan, beri **rekomendasi beserta untung-rugi**, bukan sekadar daftar opsi.
- **Klaim harus dibuktikan.** Kalau pengukuran meragukan, bilang belum sah dan ulangi dengan cara lain. User beberapa kali menerima koreksi semacam ini dan menghargainya.
- Kalau diminta mengecilkan/optimasi sesuatu, **pertimbangkan efeknya ke elemen lain** (lebar, tinggi, jarak, rasio huruf), bukan satu sisi saja.
- **User membuka dashboard uji di browsernya sendiri: http://localhost:8503** (server `dashboard-v2-uji` yang dijalankan sesi Claude Code). Biarkan server itu hidup, restart sesudah mengubah `dashboard/`, dan kalau user bilang "nyalakan localhost", yang dimaksud server itu. **Server ini ikut mati kalau sesi Claude Code ditutup atau dibuka ulang** (17 Sep: user melapor 8503 tidak jalan — port kosong, dinyalakan ulang). Cek dulu dengan `curl http://localhost:8503/_stcore/health`; kalau port dipakai server sesi lain, `preview_start` menolak — pakai server itu atau minta user. User juga bisa menjalankan sendiri: `streamlit run app.py --server.port 8503`.
- **User menguji sendiri lalu melapor dengan foto dan keluhan sekecil piksel** ("tidak sejajar", "belum center", "keluar batas chart"). Keluhan seperti itu hampir selalu benar — **ukur dulu di halaman hidup**, baru perbaiki. Di sesi 13 Sep, dua tebakan pertama tanpa pengukuran meleset.
- **Selera tampilan user:** kontrol yang ringkas, lambang ketimbang kata, ukuran seragam (tidak ada tombol yang lebih panjang atau pendek dari tetangganya), dan kedudukan lurus dengan elemen di sekitarnya. Pakai ini sebagai titik awal untuk 16 halaman berikutnya.

---

## 3. Keputusan PENDING — tanyakan dulu ke user

### 3.1 Halaman Price Levels — SELESAI 13 Sep 2026 (menu kedua, commit `54c8158`, live)
**Hasil:** loader `data.load_price_levels()` menggabungkan `data_price_level.csv` + AVIV dari `data_aviv.csv` (dihitung ulang dari kolom mentah). Satu sumbu kanan untuk semua garis termasuk BTC, **skala bawaan Auto** (= linear yang menyesuaikan zoom; pilihan "Linear" di kontrol justru mengunci rentang — namanya membingungkan, bisa diganti kalau user mau). ~~Subjudul sementara "On-chain Cost Basis"~~ — **14 Sep: judul besar jadi "Price Levels"** (permintaan user). **Legend "RP" ditulis "Realized Price"** (singkatan belum tentu dikenal pembaca); STH RP dan LTH RP tetap singkat, tombol sorot tetap "RP".
**Palet (dipratinjau, dipasang untuk dilihat user langsung — "beda terang dulu"):**

| Garis | Warna | dim (redup 1,70:1) | Catatan |
|---|---|---|---|
| STH RP | `#bf5546` rust | 0,44 | sama dengan STH MVRV (warna ikut kohort) |
| RP | `#0070a6` navy | 0,49 | sama dengan MVRV (semua holder) |
| LTH RP | `#0b8e89` teal | 0,39 | sama dengan LTH MVRV |
| AVIV Mean | `#7b65d2` violet | 0,42 | |
| AVIV Upper | `#a58df0` violet muda | 0,30 | satu keluarga dengan Mean, dibedakan terang (jarak 17 — sengaja mirip) |
| CVDD | `#a8963f` kuning tua | 0,32 | terdekat: BTC 43 (normal), STH RP 17 (buta warna) |
| MVRV 0σ / 200 DMA / 50 WMA / 200 WMA | `#8b949e` / `#b4b2a9` / `#6e7681` / `#d3d1c7` abu | 0,32 / 0,26 / 0,42 / 0,22 | mati sejak awal, dibedakan terang saja |

Uji palet: patokan longgar bagian 9 (normal ≥ 30, buta warna ≥ 14), terang dijaga setara kohort (kontras 3,3–5 untuk garis utama; CVDD 6,05). Ditolak: kombinasi "paling jauh" (AVIV/CVDD 2–3× lebih terang), magenta untuk CVDD (jarak ke violet AVIV 6 saat buta warna), merah muda (dekat rust). **Palet disetujui user apa adanya (13 Sep):** AVIV Upper tetap garis penuh violet muda, garis teknikal tetap abu-abu dibedakan terang. Pertanyaan garis putus-putus ditutup.
**AVIV 84 hari pertama (17 Jul–9 Okt 2010) disembunyikan** (disetujui user): rata-rata historis AVIV baru terbentuk dari segelintir hari, AVIV Mean jatuh ±300× di bawah harga dan menarik sumbu Log ke 0.0002. Aturannya berbasis data: hari sebelum rasio AVIV Mean/harga pertama kali 0,2–5 dikosongkan. Level sesudahnya tidak berubah.
**Highlight di halaman ini tetap dipakai** (disepakati): meredupkan garis lain dan menyaring tooltip tetap berguna meski sumbu hanya satu; fungsi tarik-sumbu memang tidak berguna di sini.
**Hasil cocok CSV:** tooltip 10 Oct 2021 — STH RP 43,376 · RP 21,731 · LTH RP 15,484 · AVIV Mean 40,932 · AVIV Upper 48,628 · CVDD 11,822 · BTC 54,695.

#### Catatan keputusan awal Price Levels (13 Sep 2026)
**Price Levels** (`data_price_level.csv`) duluan: isinya batas zona framework v2 (STH RP, RP, LTH RP, CVDD, 200DMA) dan bentuknya mirip MVRV, jadi renderer sekarang bisa dipakai hampir apa adanya.
**Isi halaman disetujui user 13 Sep 2026** (dasar: Decision Framework v2, KB Price Level v1.4, kolom CSV):
- **Menyala sejak awal** — BTC Price + 6 level framework v2: STH RP (`sth_cost_basis`), RP (`realized_price`), LTH RP (`lth_cost_basis`), AVIV Mean, AVIV Upper (+0,5σ), CVDD (`cvdd`). Nilai 7 Sep 2026: 78,905 · 70,965 · 53,193 · 49,349 · 89,771 · 102,301 · 50,054.
- **Tersedia tapi mati sejak awal** (`hidden_default=True`) — MVRV 0σ (`MVRV 0σ`; KB: satu gugus dengan AVIV Mean, bukan level terpisah), dan teknikal: 200 DMA (`200_dma`), 50 WMA (`50_wma`), 200 WMA (`200_wma`).
- **Tidak dimasukkan** — True Market Mean dan Active Realized Price (bahan hitung AVIV, garisnya dobel), `cum_pl_price` dan `pl_price_ratio` (tanpa KB).
- Usulan yang belum diputuskan: satu sumbu Log untuk semua garis termasuk BTC; pane bawah dikosongkan di versi pertama (kandidat nanti: Price/CVDD, STH RP/LTH RP); penanda zona Z1–Z5 **tidak** dibuat (keputusan framework, bagian 5).
- ⚠️ `references/data_dictionary.md` masih menyuruh memakai kolom `price_at_aviv_*`, bertentangan dengan README dan `app.py` (kolom itu salah basis ±9–10%). Dashboard mengikuti README/`app.py`. Dokumen referensi milik user — sudah dilaporkan, belum dikoreksi.

**Dibahas saat mulai mengerjakan Price Levels (ditunda user 13 Sep):** framework v2 juga memakai **AVIV Mean dan AVIV Upper** sebagai batas zona, dan keduanya ada di `data_aviv.csv`, bukan `data_price_level.csv`. Kalau halaman ini mau memuat semua batas zona, loader perlu menggabungkan dua file, dan level AVIV harus dihitung ulang dari `btc_price / aviv_ratio × aviv_mean` (kolom `price_at_aviv_*` salah basis). Baca `references/Decision_Framework v2.md` dulu sebelum mengusulkan isi halaman. ~~Pengelompokan navigasi 17 halaman masih belum dibahas~~ — diputuskan 14 Sep 2026 (bagian 3.11).

### 3.2 Slider rentang di bawah chart — SELESAI 14 Sep 2026 (commit `8bb65d7`, live)
Gaya navigator TradingView: chart mini berisi seluruh sejarah, dengan kotak geser yang bisa ditarik dan diubah lebarnya, tersinkron dua arah dengan chart utama. Tidak ada bawaannya di lightweight-charts 4.2.3, jadi digambar sendiri di dalam chart. Karena hidup di dalam chart, tidak memicu reload Streamlit.

**Hasil implementasi (`lw_chart.py`, blok "slider rentang"):**
- **Digambar di kanvas biasa, bukan `createChart` kedua** (menyimpang dari catatan teknis di bawah, dengan sengaja). Letak horizontalnya diambil langsung dari area gambar chart paling bawah: x = lebar sumbu kiri + logis × lebar skala waktu / (N − 1). Jadi slider selalu selebar area gambar tanpa perlu ikut sinkron `minimumWidth`, dan tidak ada label sumbu kedua yang bisa membuat lebarnya meleset. Rentang logis 0 … N−1 = seluruh lebar slider, sama dengan hasil `fitContent()` (terukur: Range All = bar 0–5903).
- **Geometri diambil dari chart paling bawah**, bukan `panes.main`: skala waktu pane yang tidak paling bawah bernilai lebar 0 (terukur di SOPR Separate pane: pane harga 0, pane utama 854).
- **Tinggi:** `NAV_H = 52` + jarak 6 px diambil dari tinggi pane (Python membagi `height − 58` ke pane; `sesuaikanTinggiLayar` ikut mengurangi). Tinggi bingkai tetap. Terukur MVRV 1440: pane selesai di 702, slider 708–760, bingkai 760. SOPR tiga pane (harga + metrik + Gap): slider tetap paling bawah, di dalam bingkai.
- **Isi:** kolom `BTC Price` selalu dikirim (juga saat garis BTC Hidden). Halaman tanpa kolom harga tidak mendapat slider (`C.nav = None`).
- **Interaksi:** pegangan menangkap sampai 7 px di luar tepi jendela dan paling banyak sepertiga lebar jendela ke dalam (supaya jendela sempit masih bisa digeser dari tengah); di tengah = geser; di luar jendela = lompat (berpusat di klik, lalu bisa langsung digeser). Jendela dijaga di dalam data, lebar minimal 8 bar. `setPointerCapture` supaya tarikan tidak putus. Kursor: ew-resize / grab / pointer.
- **Terukur:** tarik pegangan kanan 280,8 px → perkiraan bar 3967, hasil 3965; geser jendela → perkiraan 1241, hasil 1241; klik area gelap → 1937,78–5903 sesuai hitungan; lebar minimal tepat 8 bar; tanggal tepi jendela cocok dengan sumbu (3 Okt 2018 – 29 Jun 2021 untuk bar 3000–4000).
- **Zoom tersimpan tetap aman:** menyentuh slider memicu `mousedown` yang menghentikan fase pemulihan, jadi slider tidak pernah menyimpan rentang sementara. Rentang dari slider disimpan seperti zoom mouse.
- **Belum bisa diuji dari panel Claude:** layar penuh. User menyatakan semuanya ok di browsernya sendiri sebelum push.

**Range memindahkan jendela (pilihan B, dipilih user 14 Sep):** sebelumnya kotak Range memotong data, jadi di Range 1y slider hanya berisi 1 tahun. Sekarang chart selalu menerima seluruh sejarah; Range dan From/To hanya menentukan rentang tampil awal (`C.view`). Rinciannya di bagian 4 (Perilaku). Pilihan A (Range tetap memotong data) ditolak karena slider jadi kurang berguna di luar All.

**Sudah dipratinjau (widget, data Supply mingguan) dan disetujui user 14 Sep:**
- **Isi slider: BTC Price** (area tipis abu `#5b6b80`, skala Log) — ada di semua halaman, bentuk siklus mudah dikenali, tidak berubah saat legend dimatikan. Alternatif "metrik utama" ditolak (beda per halaman, Supply bergerigi).
- **Semua halaman**, paling bawah di bawah sumbu tanggal, **tinggi ±52 px**. Tinggi total chart tetap: pane di atasnya berkurang sebesar itu.
- **Interaksi:** geser kotak teal = pindah waktu; tarik pegangan kiri/kanan = melebar/menyempit (minimal ±8 bar); klik area gelap = lompat ke sana (kotak berpusat di klik). Zoom/geser di chart menggerakkan slider (dua arah).
- **Tampilan pratinjau:** area di luar jendela diberi selubung gelap `rgba(10,12,18,.62)`; jendela bergaris tepi `#006d77` 1 px dengan isian teal 10 %; pegangan 9×26 px `#006d77` sudut 3 px dengan dua garis kecil `#9fd4d8`; latar slider `#161b26`.
- **Tombol Range (1m…All) tetap ada** dan ikut menggerakkan slider, tapi menggeser slider tidak mengubah tulisan kotak Range (sama seperti zoom mouse sekarang).

**Catatan teknis dari pratinjau (ditulis sebelum implementasi; bagian chart kedua akhirnya tidak dipakai, lihat di atas):**
- Chart mini = `createChart` kedua dengan `handleScroll/handleScale: false`, garis silang dimatikan, `timeScale.visible: false`, dan **sumbu kiri/kanan tetap `visible` dengan `textColor` transparan** supaya area gambarnya selebar chart utama. Di dashboard lebar sumbu antar-pane sudah disinkronkan (`minimumWidth`) — slider harus ikut sinkron itu, kalau tidak jendela meleset dari tanggal chart.
- Jumlah bar slider harus sama dengan pane utama supaya posisi bisa dipetakan: `mini.timeScale().logicalToCoordinate(range.from/to)` untuk menggambar jendela, `coordinateToLogical(x)` untuk klik; tarikan dikonversi lewat piksel-per-bar = (x(N−1) − x(0)) / (N−1). Pakai `setPointerCapture` supaya tarikan tidak putus.
- Yang harus diurus di dashboard (belum ada di pratinjau): zoom tersimpan & fase pemulihan zoom (bagian 4 Perilaku, bagian 10 — jangan sampai slider memicu penyimpanan rentang sementara), Separate pane dan pane bawah (slider tetap paling bawah, sinkron dengan semua pane), layar penuh (`sesuaikanTinggiLayar` harus memperhitungkan tinggi slider), tinggi baris legend yang membungkus, dan panel browser Claude yang membekukan frame (ukur dengan screenshot/gerakan mouse sungguhan).
- Mulai dengan pratinjau localhost di satu halaman, ukur posisi jendela terhadap tanggal di sumbu, baru nyalakan untuk semua halaman.

### 3.3 Memindahkan kontrol Line style ke dalam chart — masih terbuka
Tujuannya supaya mengubah gaya garis tidak memuat ulang chart. User sempat memilih "kerjakan", lalu sepakat menunggu: keluhan aslinya adalah zoom hilang saat reload, dan itu sudah diperbaiki 13 Sep. Setelah dipakai beberapa hari, tanyakan lagi apakah masih terasa perlu. Penjelasan lengkap ada di bagian 7.
**17 Sep 2026:** dicek, masih belum dikerjakan (Line style masih popover Python). User bertanya letaknya kalau dipindah; dipratinjau tiga opsi: **B (saran) tombol "Style" di sebelah Full → panel kecil di pojok kanan atas chart, kotak Line style di baris kontrol dihapus**; A klik kanan/tekan lama kotak periode di legend; C tetap seperti sekarang. **User memilih B untuk dicoba — dikerjakan 17 Sep, lihat bagian 3.24.**

### 3.4 Bentuk MVRV Z-Score — sudah diputuskan dan dikerjakan 13 Sep 2026
Z-Score tinggal di **pane ketiga paling bawah** pada halaman Market Valuation, dinyalakan lewat kotak **Z-Score** (Hidden / Bottom pane). Rinciannya di bagian 4. Sempat dicoba digabung ke chart MVRV sebagai histogram — ditolak user karena terlalu padat dan skala Log mengacaukan semuanya. Ide halaman terpisah dan tombol pengalih chart tidak dipakai.

### 3.6 Desain judul halaman — sudah diputuskan dan dikerjakan 13 Sep 2026
User menilai subjudul "MVRV Oscillators" di bawah lencana "Market Valuation" kurang tegas sebagai tanda halaman MVRV. Pratinjau ulang tanpa tab: A (garis aksen), B (kategori kecil di atas, metrik jadi judul besar), C (jejak "Market Valuation / MVRV Oscillators"). Tanpa tab, alasan utama C hilang (lencana tidak lagi sekaligus jadi tab aktif) dan kotak teal padatnya mirip tombol aktif. User memilih **B**, lalu varian **B2** (kategori jadi lencana teal kecil), dengan judul **18,4 px tebal 600** (sama dengan menu sidebar). Rinciannya di bagian 4.

### 3.7 Angka di posisi kursor (tooltip) — diputuskan dan SELESAI 13 Sep 2026 (commit `87bc1d6`)
Hasil uji di halaman hidup (hover mouse sungguhan, viewport 1440): kotak di x = sumbu kiri 54 + 8, top = 8 px di bawah baris legend; kursor di sisi kiri (Jan 2011) → kotak pindah, tepi kanan = 980 − sumbu kanan 70 − 8. Isi 29 Sep 2022 (MVRV/STH/LTH × Value/7d/60d/365d + BTC 19,592) **cocok persis dengan CSV**. Highlight MVRV → hanya MVRV + BTC Price. Z-Score Hidden → tanpa baris Z; Bottom pane → MVRV Z-Score + Rolling Z-Score (1y), 2y/4y (mati) tidak ikut.

Chart sekarang hanya menampilkan nilai hari terakhir; nilai di tanggal lampau tidak bisa dibaca. Keputusan user setelah tiga pratinjau interaktif:
- **Bentuk: kotak tooltip** (gaya CryptoQuant). Opsi angka di dalam legend ditolak ("kurang enak bacanya").
- **Posisi: pojok kiri atas area gambar**, di bawah baris legend, di dalam batas sumbu. Kotak **menghindar kursor**: kalau kursor mendekati kotak, kotak pindah ke pojok kanan atas. Hanya muncul saat kursor ada di chart.
- **Rolling Z-Score satu baris mendatar** (permintaan user 13 Sep): judul kecil 1y · 2y · 4y di baris tepat di atasnya, angka di bawahnya; hanya jendela yang ON. Cocok CSV 04 Jul 2021: MVRV 1.82 · 60d 2.00 · Z 1.58 · 1y −0.90 · 2y −0.26 · BTC 35,319.
- **Isi: satu baris per metrik, periode smoothing jadi kolom** (Value · 7d · 60d · 365d). Baris tidak bertambah saat periode ditambah; kotak hanya melebar. Baris pertama tanggal (format "07 Sep 2026").
- **Saringan:** hanya garis yang ON di legend. Kalau Highlight aktif, hanya kelompok yang disorot. **BTC Price selalu tampil**, apa pun sorotannya (satu-satunya pengecualian, pilihan user). **Kalau kotak Z-Score = Hidden, baris MVRV Z-Score dan Rolling Z-Score tidak ditampilkan sama sekali** (ditegaskan user 13 Sep); Rolling 2y/4y hanya kalau ON.
- **Format angka** ikut poin audit 2+9 yang sudah diterima: rasio dan Z-Score 2 desimal, harga tanpa desimal dengan pemisah ribuan (78,905). Rencananya aturan desimal/format ditaruh per seri di registry, dipakai bersama oleh sumbu, label nilai terakhir, dan tooltip.
- Yang tetap: garis silang vertikal, titik di tiap garis, label tanggal di sumbu waktu (bawaan chart), label nilai terakhir di sumbu.

### 3.8 Tombol Range di celah kanan baris kontrol — ditahan user 13 Sep 2026
Ide: pindahkan Range ke celah kosong di kanan baris kontrol, gaya CryptoQuant (preset 1m·3m·6m·1y·4y·All + ikon kalender yang membuka panel From/To dengan kalender dua bulan dan Latest/Reset/Apply). Sudah dipratinjau. Catatan teknis: kotak tanggal Streamlit 1.63 hanya kolom ketik (react-aria), jadi kalender dua bulan harus dibuat sendiri sebagai komponen kecil; alternatif sederhana = kolom tanggal Streamlit + `st.form` (chart hanya dimuat ulang saat Apply). Tombol "now" versi CryptoQuant sebaiknya jadi "Latest" (tanggal data terakhir, bukan hari ini). Ide lain yang sempat dibahas untuk celah itu: tombol simpan gambar chart (untuk ditempel ke Claude.ai). Memindahkan tombol Highlight ke sana ditolak — butuh menempelkan tombol dari iframe ke halaman induk, rawan rusak. User: "belum perlu, kosongkan dulu".

### 3.9 Halaman ketiga: SOPR — SELESAI 14 Sep 2026 (commit `073a997`, live)
Dipilih user dari tiga pratinjau tata letak dengan data asli (A: semua SOPR di sumbu kiri + BTC digabung; **B: BTC di pane sendiri + LTH-SOPR sumbu kanan + Log**; C: seperti MVRV, LTH mati di awal).
- **Data:** `data.load_sopr()` dari `data_momentum.csv` (`asopr`, `sth_sopr`, `lth_sopr`, sejak 17 Jul 2010). NUPL di file yang sama sengaja tidak dimuat — halaman sendiri nanti.
- **Tata letak B:** `btc_mode_default="Separate pane"`, skala metrik dan harga Log, LTH-SOPR `separate_axis="right"` (ganti ke Overlay → LTH ke kiri; balik ke Separate pane → LTH ke kanan). Alasan: **LTH-SOPR harian masih melonjak di atas 20 sampai 2024 (29,7) dan 2025 (24,4)**, dulu 385 (2011) dan 294 (2013). Berbagi sumbu dengan aSOPR/STH-SOPR (0,9–1,2) membuat keduanya rata, bahkan di Range 1y.
- **Garis acuan Break-even 1.0 di setiap sumbu yang memuat metrik** (`RefLine.all_axes=True`): dua garis saat Separate pane, satu saat Overlay. Definisi SOPR, bukan ambang framework.
- **Warna ikut kohort:** aSOPR navy `#0070a6` (dim 0,49), STH-SOPR rust `#bf5546` (0,44), LTH-SOPR teal `#0b8e89` (0,39). Tombol sorot: aSOPR · STH · LTH · Gap.
- **Pane bawah "SOPR Gap"**: histogram rust alpha 0,80, dim 0,41 (redup 1,44:1, setara Z-Score). **Mati sejak awal** (keputusan user, apa pun mode harga BTC).
- **Rumus gap = KB SOPR v1.4 §12: SMA90(STH-SOPR) − SMA60 dari SMA90 itu.** Diuji tiga tafsiran terhadap angka KB; hanya ini yang cocok persis: +0.02447 (10 Jan 2021), +0.01313 (21 Okt 2021), +0.00770 (17 Jul 2025), cross turun 28 Mar 2021 · 30 Nov 2021 · 3 Feb 2025 · 18 Agt 2025. User menyetujui rumus ini untuk dashboard.
- **Desimal:** SOPR 3; gap 5 (KB menulis +0.00096; dengan 4 jadi "0.0010"); **LTH-SOPR ≥ 100 tanpa desimal** (`Series.whole_from=100`: sumbu menulis 1,200 · 500 · 180, di bawah 100 tetap 1.318).
- **Terukur:** tooltip 06 Feb 2021 cocok CSV (BTC 39,221 · aSOPR 1.073 · STH-SOPR 1.050 · LTH-SOPR 4.664 · Gap 0.01021); 11 May 2011 (5.50 · 1.449 · 1.327 · 47.338).
- Garis ambang framework (0,97 · 0,95 · 0,93 · 0,50) sengaja tidak dipasang — keputusan framework (bagian 5). Smoothing Off sejak awal (KB: LTH-SOPR harian terlalu berisik, minimal rata-rata 14 hari — user tinggal menyalakan).
- ⚠️ **Belum diputuskan (user cek di Claude.ai):** `alerts/alert_check.py` `_sth_sopr_ma_gap` menghitung **SMA60 − SMA90**, bukan rumus KB. Angka dan tanggal cross-nya berbeda (10 Jan 2021 = +0.01141; cross 2021 di 4 Mar, 15 Apr, 18 Okt, 10 Des). Dipakai trigger K1 dan sinyal 2 alarm bear di alert harian. Teks framework v2 "gap MA90−MA60" ambigu. **Jangan dibetulkan diam-diam.**

### 3.10 Kotak Tooltip — SELESAI 14 Sep 2026 (commit `073a997`)
Kotak kedelapan di ujung baris kontrol, pilihan **Fixed / Cursor / Off**, **bawaan Cursor**.
- **Fixed:** perilaku lama (kiri atas area gambar, pindah ke kanan atas kalau kursor mendekat).
- **Cursor:** gaya ChartInspect — kotak 16 px di kiri garis kursor, tengahnya sejajar kursor, dibatasi di dalam area pane. Kalau di kiri tidak cukup tempat, pindah ke kanan kursor. Terukur: jarak ke kursor 15,9 px, selisih tengah 0,2 px; di tepi kiri kotak mulai di kursor + 16.
- **Off:** tidak ada kotak; garis silang dan label sumbu tetap. Saran Claude untuk screenshot bersih ke Claude.ai.
- **Satu pilihan untuk semua halaman** (permintaan user). Disimpan di key biasa `tooltip_pref`; widget `tooltip_mode` hanya cerminan, karena `st.navigation` membuang nilai widget saat pindah halaman (bagian 10).
- **Latar tetap 94 %** (`rgba(28,34,48,0.94)`). Dipratinjau 100/94/80/65 %; user: lebih tembus membuat garis dan angka sama-sama tidak terbaca.

### 3.11 Menu berkelompok (`st.navigation`) — SELESAI 14 Sep 2026 (commit `073a997`)
Dipratinjau dua cara: A (radio lama + judul kelompok) dan **B (navigasi bawaan Streamlit)**, plus tiga pengelompokan (tanpa kelompok / **jenis metrik** / peran di framework). User memilih **B + jenis metrik**.
- **Alamat per halaman:** `localhost:8503/` (MVRV, halaman pertama = bawaan), `/price-levels`, `/sopr`. Reload tetap di halaman yang sama; bisa di-bookmark. Terukur.
- **Nama menu pendek** (`MetricFamily.title`: MVRV, Price Levels, SOPR); **nama kelompok** (`MetricFamily.group`) jadi judul kelompok di menu **dan** lencana teal di atas judul halaman (VALUATION, PROFITABILITY). `MetricFamily.key` tidak diubah (key localStorage tetap `dash_v2_market_valuation`).
- **Usulan kelompok lengkap (19 halaman dari daftar CSV; sudah dibuat per 17 Sep: MVRV, Price Levels, AVIV, SOPR, NUPL, Supply in Profit, HODL Waves dan RHODL Ratio (kelompok Holder Behavior), Funding & OI, Fear & Greed):** Valuation (MVRV · Price Levels · AVIV · RHODL) · Profitability (SOPR · NUPL · Realized P/L · Supply in Profit) · Holder Behavior (HODL Waves · Realized Cap · CDD/VDD · LTH Flow) · Flows & Demand (Exchange · Apparent Demand) · Derivatives (Funding & OI · Futures Basis) · Sentiment & Macro (Fear & Greed · Search Trends · Treasury 2Y). Menu hanya menampilkan halaman yang sudah ada.
- **Judul kelompok teal terang `#2aa6b0`** 11 px tebal 600 huruf kapital (pilihan 2 dari empat pratinjau). Alasan: warna abu `#8b90a0` (5,5:1) tebal kapital terlihat seterang menu tidak aktif `#c9d1d9` (11,4:1). Teal membedakan lewat warna dan senada dengan lencana kategori. Ditolak: abu, abu + garis, abu redup `#6e7681` (3,8:1, mirip "Highlight" redup yang dulu ditolak).
- **Menu:** 15 px `#c9d1d9`; aktif latar `#102e39` + garis kiri 3 px `#006d77`, tulisan putih 600; hover `#1e2330`. Huruf pertama judul kelompok dan nama menu sama-sama di x=33 (sebelum diluruskan 20 vs 33).
- **Tulisan merek tetap di atas menu** lewat CSS flex `order` (bawaan Streamlit menaruh menu paling atas). Garis pemisah bawaan disembunyikan. Jarak merek → judul kelompok 17 px.
- `expanded=True`: tanpa ini Streamlit menyembunyikan halaman ke-11 dst. di balik "View more".
- Judul kelompok bisa diklik untuk melipat kelompok (panah muncul saat hover) — fitur bawaan, dibiarkan.

### 3.12 Halaman keempat: Supply in Profit — SELESAI 14 Sep 2026
Dipilih user karena paling sering dipakai framework v2 setelah MVRV/SOPR (K1 sinyal 5, K2 veto 1 & 2, K4 kondisi 3, K5) dan KB-nya ada (`references/supply_in_profit_loss_knowledge_base v1.4.md`).
- **Data:** `data.load_supply()` dari `data_supply.csv`: `percent_btc_in_profit` → Total, `pct_sth_in_profit` → STH, `pct_lth_in_profit` → LTH. Kolom `*_in_loss` tidak dimuat — di data **selalu 100 − in_profit** (selisih maks 0,0014). `lth_supply_btc`/`sth_supply_btc` belum dipakai (tidak ada di KB/framework; kandidat pane bawah nanti).
- **Garis:** Total in Profit navy, STH in Profit rust, LTH in Profit teal (nama legend tanpa "Supply" — versi panjang membuat legend dua baris di 1440), BTC Price Overlay sumbu kanan Log. Menu "Supply in Profit", `url_path="supply-in-profit"`, kelompok Profitability, judul besar "Supply in Profit". Satu desimal (seperti KB).
- **Sumbu metrik tetap 0–100** (`MetricFamily.metric_range=(0, 100)`, pilihan user dari pratinjau Auto vs 0–100): halaman ini membaca level. Ruang tepi sumbu dipersempit (atas 0,06, bawah 0,04) dan **angka di luar 0–100 tidak ditulis** (sempat tertulis 120 · 110 · −10). Klik dua kali (reset sumbu) kembali ke 0–100.
- **Tooltip Profit | Loss** (`MetricFamily.complement=("Profit", "Loss")`): kolom Loss = 100 − Profit untuk nilai utama, sedikit diredupkan `#aeb6c2`; nama baris memakai nama pendek (Total · STH · LTH). Terukur 21 Jun 2021: 66.8 | 33.2 · 1.0 | 99.0 · 95.5 | 4.5 · BTC 31,682 — cocok CSV.
- Smoothing Off sejak awal (KB: STH harian bisa bergerak 50 poin/minggu; veto K2 kedua membandingkan LTH dengan SMA30 — user tinggal nyalakan 30d). Garis ambang framework (50 · 60 · 90) tidak dipasang.
- **BTC price bawaan Separate pane** (`btc_mode_default="Separate pane"`, permintaan user 14 Sep, commit `8bb65d7`): harga di pane atas, Supply 0–100 di pane bawahnya. Seri Supply tidak punya `separate_axis`, jadi tetap di sumbu kiri.

### 3.13 Saklar Profit / Loss di dalam chart — SELESAI 14 Sep 2026
Hanya di halaman yang punya `complement` (sekarang Supply in Profit). Proses keputusan: satu tombol "View" (A kotak kontrol / **B di dalam chart** / C di kotak Scale) → user minta Profit dan Loss bisa menyala bersamaan → dua saklar → boleh mati keduanya.
- **Letak:** di awal kelompok Highlight, dipisah garis tipis: `Profit` `Loss` │ Highlight … Hidup di browser (tanpa reload), tersimpan di localStorage (`showProfit`, `showLoss`, `lossShown`). Format lama `inverse` dipindahkan otomatis.
- **Empat keadaan:** Profit saja (seperti biasa) · keduanya (legend "Total · STH · LTH" dengan dua contoh warna, tooltip Profit | Loss) · Loss saja (legend "… in Loss", warna kohort asli, tooltip Loss | Profit) · keduanya mati (hanya BTC; tombol sorot tinggal BTC; tooltip tanpa judul kolom).
- **Warna Loss saat keduanya menyala — set B** (`Series.complement_color`): Total `#839df0` lavender, STH `#dc9390` merah muda, LTH `#38d1b4` aqua. Dicari lewat hitungan (corak bergeser ≤ ±25° dari kohort, kepekatan ≥ 30, STH digeser ke arah merah muda): antar-Loss 28 normal / 28 buta warna; terlemah LTH vs STH Loss saat buta warna 13 (normal 64). Ditolak: campur putih 50 % (Total Loss vs LTH Loss 18 / 14), 35 % (terlalu mirip Profit-nya), 65 % (buta warna 8), set kusam (keabu-abuan, STH jadi coklat), set peach (STH mendekati oranye BTC), garis Profit 1 px + Loss pita 50 % (dicoba lalu diganti warna oleh user).
- **Kembaran Loss:** tiap garis metrik di pane utama (utama dan smoothing) punya seri kedua 100 − nilai, bentuk garis sama, dibuat saat chart dibuat. Garis utama Loss ikut saklar legend induknya. **Smoothing Loss saat keduanya menyala: kotak angka kedua di legend** (tepi warna Loss, **mati di awal**); saat hanya Loss, kotak pertama yang mengaturnya. Kolom smoothing di tooltip berisi nilai Profit (Loss = 100 − itu).
- Terukur: kotak kedua STH → garis "STH in Loss SMA(30)" muncul; label nilai terakhir Loss = 100 − Profit; zoom tidak bergeser saat saklar ditekan; reload mempertahankan pilihan.

### 3.14 Urutan legend: BTC Price selalu terakhir — SELESAI 14 Sep 2026
Laporan user: di SOPR (Separate pane) BTC tampil pertama di legend dan tombol sorot, karena seri harga disisipkan paling depan. Kelompok legend kini diurutkan dengan BTC Price terakhir — berlaku semua halaman (legend, tombol sorot, tooltip).

### 3.15 Dashboard di HP — SELESAI 15 Sep 2026 (commit `32a8abd` dan `024807a`, live)
User bertanya apakah dashboard nyaman dibuka di HP. Diukur di localhost dengan viewport 375×812 (emulasi Android): tidak ada geser samping dan kontrol membungkus rapi, tapi ada delapan gangguan. Paling berat: geser jari atas-bawah di chart dipakai chart (bawaan `vertTouchDrag`), sehingga halaman nyaris tidak bisa digulir; sidebar langsung terbuka menutupi layar; area gambar cuma 218 dari 343 px; chart lebih tinggi dari layar; tombol legend 24 px; tombol pembuka sidebar menimpa lencana kategori; tooltip Cursor butuh mouse; tombol Full tidak jalan di iPhone.

**Tahap 1 (dikerjakan, dinyatakan ok user di Android dan iPhone):**
- `app.py`: `initial_sidebar_state="auto"` (dulu `"expanded"`) — sidebar tertutup di HP, tetap terbuka di layar lebar. Terukur: 375 px tertutup, 1440 px terbuka.
- `lw_chart.py` `chartOptions`: `handleScroll: { vertTouchDrag: false }` — geser jari atas-bawah menggulir halaman; geser kiri-kanan dan cubit tetap untuk chart. Mouse, trackpad, dan roda gulir tidak terpengaruh (`pressedMouseMove` dan `mouseWheel` tetap menyala). Slider: `touch-action: pan-y`.
- `app.py`: di layar ≤ 768 px `.block-container` diberi `padding-top: 3.25rem`, judul turun ke y=58 (tombol pembuka sidebar selesai di y=44). Aturan `:fullscreen` tetap menang karena lebih spesifik.
- Tampilan laptop terukur sama: judul y=15, chart x=380 y=121.

**Tombol Scale (khusus perangkat sentuh):** efek samping tahap 1, skala chart tidak bisa lagi digeser dengan jari. Tarik angka sumbu dengan jari juga dicoba user dan tidak bisa (halaman yang bergerak). Solusi: saklar "Scale" di baris Highlight, tepat sebelum Full, ikon "geser vertikal" (pilihan user no. 3 dari enam calon, bentuk B = ikon + kata, seragam dengan Full).
- Hanya muncul kalau `matchMedia('(pointer: coarse)')` benar; laptop (penunjuk utama mouse) tidak mendapat tombol ini. Laptop layar sentuh dengan mouse sebagai penunjuk utama juga tidak.
- Nyala = `vertTouchDrag: true` di semua pane; mati = `false`. **Tidak disimpan**: setiap chart dibuka, saklar mati, supaya halaman tidak terkunci diam-diam.
- Library membaca `handleScroll.vertTouchDrag` di setiap gerakan sentuh (dicek di kode 4.2.3: `treatVertTouchDragAsPageScroll: () => !options.handleScroll.vertTouchDrag`), jadi `applyOptions` langsung berlaku tanpa membangun ulang chart.

**Layar penuh semu untuk iPhone:** Safari dan Chrome di iPhone tidak menyediakan Fullscreen API untuk halaman (hanya video). Kalau `requestFullscreen` tidak ada atau `fullscreenEnabled` false, tombol Full memasang kelas `penuh-semu` pada `<html>` halaman induk. `app.py` memberi kelas itu aturan yang sama persis dengan `:fullscreen` (header, toolbar, sidebar, judul disembunyikan; jarak halaman dipangkas). `sedangPenuh()` = fullscreen asli **atau** kelas semu, jadi `sesuaikanTinggiLayar` memaskan chart ke tinggi jendela. Kelas menempel di halaman induk sehingga tetap terbaca sesudah Streamlit membangun ulang chart. Masuk mode ini menggulir halaman ke atas.
- Terukur (meniru browser tanpa API di 375×812): frame mulai y=160 tinggi 644 (dasar 804 = 812 − 8), slider terlihat, tombol "Exit"; Exit mengembalikan persis (frame y=255 tinggi 766).
- Laptop dan Android punya Fullscreen API, jadi tidak pernah masuk jalur ini (terukur di 1440: API ada, kelas kosong).
- Catatan user: di iPhone chart mode normal lebih panjang daripada mode Full (Full dipaskan ke tinggi layar, normal tetap 760 px dan halamannya digulir), dan saat Full halaman tidak bisa digulir. User menyatakan tidak masalah.

**Tahap 2 ditolak user:** chart lebih pendek, angka sumbu diringkas, dan tombol legend dibesarkan khusus HP tidak dikerjakan — user khawatir mengganggu tampilan laptop. Kalau suatu saat diminta lagi, perubahan bisa dibatasi ke layar sempit.

**Angka sumbu terpotong setengah di tepi pane** (dilaporkan user dari HP, juga terjadi di laptop, mis. "8,000,000" di atas sumbu harga): **wajar, bawaan library, bukan error**, dan tidak memengaruhi data. Opsi `priceScale.entireTextOnly: true` (ada di 4.2.3) akan menyembunyikan angka yang tidak muat utuh; **user memilih tidak diubah**. Batang Z-Score yang terlihat rata di atas pada foto yang sama kemungkinan besar karena skala pane sudah digeser dengan tombol Scale menyala (autoscale mati); ketuk dua kali mengembalikannya ke Auto.

**Cara menguji di HP:** localhost tidak bisa dibuka dari HP user lewat `http://192.168.1.5:8503` (Streamlit sudah mendengar di semua alamat; kemungkinan diblokir Windows Firewall atau Surfshark VPN — pengaturan keamanan, tidak diubah Claude). Pengujian sentuh dilakukan user lewat Streamlit Cloud setelah push.

### 3.16 Halaman MVRV: bawaan BTC Separate pane + sumbu Log — SELESAI 15 Sep 2026 (commit `32a8abd`)
Permintaan user. `MARKET_VALUATION` di registry: `btc_mode_default="Separate pane"`, `metric_scale_default="Log"`, `price_scale_default="Log"`. Sempat dipasang Overlay karena salah paham, lalu diganti. Terukur: 2 pane, semua sumbu Log, LTH MVRV otomatis ke sumbu kanan (`separate_axis`), kotak Display menulis "Mixed". Pane Z-Score tetap linear.

### 3.17 Halaman NUPL — SELESAI 16 Sep 2026 (commit `24e1fe1`, live)
Dasar: KB NUPL v1.4 (framework v2 tidak memakai NUPL). Dipratinjau dengan data mingguan, disetujui user.
- **Data:** `data.load_nupl()` dari `data_momentum.csv` (`nupl`, `sth_nupl`, `lth_nupl`, sejak 17 Jul 2010). `NUPL Gap` = LTH-NUPL − STH-NUPL (KB §8.1). **Ratio LTH/STH tidak dimuat**: KB §8.2 menyebut angkanya melompat tanpa makna saat STH dekat nol (+73 ke −561 sehari).
- **Tampilan:** menu "NUPL" (Profitability, `/nupl`), judul "Net Unrealized Profit/Loss". Garis NUPL navy, STH-NUPL rust, LTH-NUPL teal, 3 desimal. Garis acuan Break-even (0). BTC Separate pane, skala metrik linear (Auto; ada nilai negatif). Pane bawah "NUPL Gap" histogram rust, **mati sejak awal** (permintaan user).
- **Sumbu tidak dipaku −1..1** (pilihan user dari pratinjau): lembah 2011 (STH −3.6, NUPL −1.5) membuat Range All gepeng, tapi zoom/Range 4y lega dan data 2011 tidak terpotong.
- **Sumbu kanan saat Separate pane** (permintaan user, juga untuk Supply in Profit): `separate_axis="right"` di ketiga garis, kembali ke kiri saat Overlay. Aturan user: metrik yang skalanya sama pindah ke kanan; kecuali seperti LTH-SOPR/LTH-MVRV yang skalanya jauh berbeda.
- **Terukur cocok KB:** 28 Okt 2025 NUPL 0.507 · STH −0.001 · LTH 0.669; 21 Nov 2022 STH −0.206 · LTH −0.309 (NUPL −0.286 vs KB −0.288, kemungkinan revisi data); Gap 22 Jun 2021 1.196 (KB 1.20), 10 Feb 2023 −0.031.
- Garis ambang KB (0.55, 0.50, −0.20, …) tidak dipasang: KB sendiri menyebut ambang tetap tidak andal lintas siklus.

### 3.18 Realized P/L — DITUNDA 16 Sep 2026 (keputusan user: skip)
Data `data_pl.csv` bermasalah dan tidak ada KB. Temuan (sejak 2020, 2.450 hari):
- `rpl_ratio` melonjak sampai ratusan juta karena 77 hari realized loss < 1 BTC (mis. 0.0002 BTC 31 Des 2020 vs profit 51.504 BTC); 70 hari > 1.000.
- `sth_pl_ratio` / `lth_pl_ratio` **macet**: sama persis dengan hari sebelumnya di 179 / 246 hari (mis. LTH 3.302.512 lima hari berturut 24–28 Mar 2024 padahal profit/loss berbeda).
- Yang sehat: `daily_realized_profit_btc`, `daily_realized_loss_btc` (kecuali 77 hari tadi), `rrp`, `rrl`, `relative_realized_pl` (= rrp − rrl), `rpl_ratio` = profit ÷ loss persis.
- Usulan kalau dilanjutkan: buat KB dulu di Claude.ai; ratio dihitung ulang dari jumlah 30 hari profit ÷ loss (sejak 2016: 0.11–101, median 2.1); STH/LTH ratio jangan dipakai.

### 3.19 Halaman Funding Rates & Open Interest — SELESAI 16 Sep 2026 (commit `3fe3619`, live)
Tidak ada KB. Framework v2 hanya memakai funding < 0 (pengubah ukuran K2). Semua bentuk dipilih user dari pratinjau.
- **Data:** `data.load_derivatives()` dari `data_derivatives.csv`. Baris sebelum harga pertama (OI mulai 28 Feb 2020, harga/funding 31 Mar 2020) dibuang.
  - **Funding:** satuan tidak ditulis ChartInspect (median 0.0062, kemungkinan % per 8 jam) → ditampilkan tanpa satuan, 4 desimal. 364 dari 2.353 hari negatif.
  - **OI:** dicek di API `futures-open-interest`: `total_oi` = **persis jumlah 13 bursa** (CME, Binance, Bybit, Hyperliquid, Bitget, OKX, Deribit, Coinbase, BitMEX, Kraken, Bitfinex, MEXC, Huobi), selisih 0 di 2.385 hari. Satuan tidak ditulis; dari besarnya **BTC** (CME 107.248 × 75.990 = 8,2 miliar USD). Halaman ChartInspect punya pilihan "Unit: USD".
  - **Cakupan bursa bertambah:** CME 5 Jun 2020, Bitget 13 Agt 2021, Coinbase 2 Des 2023, Hyperliquid 25 Des 2024, MEXC 21 Mar 2025 — total OI melompat di hari itu. OI CME sama persis Sabtu–Minggu (bursa tutup) — wajar.
- **`auto_update.py` diubah (izin user):** hanya blok `# 3. PIPELINE: DERIVATIVES` — daftar `OI_EXCHANGES` dan 13 kolom `oi_<bursa>` ikut disimpan ke CSV (kolom lama tetap di depan). Efek: `data_master_all_metrics.csv` ikut bertambah 13 kolom saat script lengkap jalan di GitHub Actions. CSV lokal diisi dengan menjalankan **hanya blok Derivatives** (skrip sekali pakai yang mengeksekusi header + blok 3 dari `auto_update.py`), bukan seluruh script. Perubahan user yang belum di-commit di file yang sama (pipeline 19 Treasury 2Y) **tidak ikut commit** (hanya hunk Derivatives di-stage lewat `git apply --cached`).
- **OI Change (ΔOI) bersih:** jumlah `diff()` per bursa, hanya bursa yang OI-nya > 0 kemarin **dan** hari ini — hari bursa masuk cakupan atau sehari bernilai 0 tidak dihitung. Terukur: 5 Jun 2020 +53.921 → +9.528; 21 Mar 2025 +20.766 → −9.295; 30 Apr 2020 −91.759 → −23.108. Tanpa kolom `oi_*`, jatuh ke selisih `total_oi`.
- **Tampilan:** menu "Funding Rates & Open Interest" (kelompok Derivatives, `/funding-oi`). BTC Separate pane. **Funding + OI satu pane** (permintaan user): funding batang dua warna (positif teal, negatif rust) di sumbu kanan; OI garis violet `#7b65d2` di sumbu kiri (OI jumlah selalu positif → garis, bukan batang). Garis "Zero" mengikuti sumbu funding (`RefLine.follow`). Mode Overlay: funding kiri, OI kanan (berbagi dengan harga). Pane bawah "OI Change (1d)" batang dua warna, mati sejak awal.
- **Saklar OI BTC | USD** di baris Highlight (`OI [BTC] [USD] │ Highlight …`; label "OI" supaya tidak tertukar tombol sorot "BTC"). Boleh menyala dua-duanya, tersimpan di localStorage (`unitOn`).
  - OI USD = `total_oi` × harga hari itu, violet muda `#a58df0`, format ringkas (40.82B). ΔOI USD = ΔOI BTC × harga.
  - Sisi sumbu: satu OI menyala → sisi OI (kiri); dua-duanya → USD pindah ke sisi seberang **kalau kosong** (funding dimatikan), kalau tidak skala sendiri tanpa angka. Semua kombinasi terukur 16 Sep.
  - ΔOI: batang ikut satuan pertama yang menyala; tooltip menampilkan baris ΔOI untuk semua satuan yang menyala (dua baris, bukan dua kolom).

### 3.20 Angka sumbu disembunyikan per pane — SELESAI 16 Sep 2026 (commit `3fe3619`, semua halaman)
Permintaan user: kalau semua garis di satu sisi sebuah pane dimatikan di legend, **hanya angkanya** yang hilang — lebar sumbu tetap, pane tetap sejajar, area gambar tidak melebar. Caranya `priceScale(side).applyOptions({textColor: 'rgba(0,0,0,0)'})` (lebar dihitung dari panjang teks, bukan warnanya). Garis acuan (Zero, Break-even, Neutral) tidak dihitung sebagai garis menyala dan ikut disembunyikan. Terukur MVRV: LTH MVRV mati → angka kanan pane MVRV hilang, angka BTC pane atas tetap, lebar sumbu tetap 70 px.

### 3.21 Halaman Fear & Greed — SELESAI 16 Sep 2026 (live; di-push atas permintaan user sebelum pindah sesi)
Dasar: framework v2 memakai F&G < 30 (K2: dip kelas dalam), F&G < 50 (K5 staging), F&G SMA30 (konteks K1/K4). Tidak ada KB.
- **Data:** `data.load_fear_greed()` dari `data_fg.csv` (sumber Alternative.me lewat ChartInspect, 3.145 hari sejak 1 Feb 2018, 2 tanggal bolong, nilai bulat 5–95). CSV tidak punya harga → digabung dari `data_mvrv.csv` (identik dengan `bitcoinPrice` API).
- **Kelas resmi dari API** (`valueClassification`): Extreme Fear ≤25 · Fear 26–46 · Neutral 47–54 · Greed 55–75 · Extreme Greed ≥76.
- **Tampilan (pilihan user dari pratinjau):** menu "Fear & Greed" (kelompok **Sentiment & Macro**, `/fear-greed`), judul "Crypto Fear & Greed Index". **BTC Separate pane** (sempat Overlay satu pane, diganti user), F&G di sumbu kanan tetap 0–100, angka bulat.
  - **Garis bergradasi halus** per titik menurut nilai: rust `#bf5546` (0–25) → `#dc9390` (40) → abu `#8b949e` (50) → aqua `#38d1b4` (62) → teal `#0b8e89` (75–100). Bukan merah-hijau (aman buta warna, sekeluarga warna funding). Ditolak: pita batas kelas di latar, batang warna kelas, gradasi per kelas.
  - **SMA30 menyala sejak awal**, bentuk **Band** (tebal 3 px, transparan 60 %) warna kuning pucat `#F7E9A8`, satu desimal (SMA30 10 Jan 2021 = 92.4, cocok framework).
  - **Tooltip** menulis nama kelas berwarna gradasi: 08 Jan 2021 `93 · Extreme Greed` · 30d 92.2 · BTC 40,736 (cocok CSV).
- Garis ambang framework (30, 50) tidak dipasang.
- Catatan kecil yang belum diminta diubah: label nilai terakhir SMA30 di sumbu tertulis bulat (65) karena library memakai format seri pertama di sumbu itu; nilai tepat (64.7) ada di tooltip.

### 3.22 Halaman AVIV — SELESAI 17 Sep 2026 (commit `045cd9a`, live)
Dipilih user dari hasil cek data 11 kandidat (bagian 3.23): satu-satunya kandidat yang dipakai framework v2 (batas Z4/Z5). Pratinjau widget data mingguan, tiga pilihan user.
- **Data:** `data.load_aviv()` dari `data_aviv.csv`, satuan rasio. Band dihitung dari `aviv_mean` dan `aviv_upper_1sd` (σ = upper_1sd − mean): Upper = mean + 0,5σ (framework, tidak ada di CSV), ±1σ, ±2σ. Kolom band lain di CSV identik (selisih < 1e-14). **Rasio ≥ Upper persis sama dengan harga ≥ AVIV Upper di Price Levels** (terukur: 1.279 hari sejak 2011 di keduanya). Band bawah negatif sampai 12 Jun 2014 (−1σ) / 1 Okt 2014 (−2σ) → dikosongkan (Log tidak bisa, rasio tidak pernah negatif). Pane bawah **Deviation (σ)** = (rasio − mean) / σ: 0 = Mean, +0,5 = Upper.
- **84 hari pertama disembunyikan** dengan aturan yang sama seperti Price Levels; aturannya kini fungsi bersama `data._aviv_awal()` (hasil Price Levels tidak berubah).
- **Tampilan (pilihan user):** menu "AVIV" (Valuation, di bawah Price Levels, `/aviv`), judul "AVIV Ratio". **Warna B** — AVIV Ratio navy `#0070a6` (metrik dasar navy, konsisten dengan halaman lain), AVIV Mean violet `#7b65d2`, AVIV Upper (+0.5σ) violet muda `#a58df0` (sama dengan Price Levels). Ditolak: A (rasio violet + band abu; jaraknya lebih besar, tapi rasio tidak navy). Uji Lab B: rasio–Mean 45 normal / 16 buta warna, Mean–Upper 17 / 16.
  - **Sumbu AVIV Log**, BTC Separate pane Log; semua garis AVIV `separate_axis="right"`.
  - **σ Bands** satu kelompok legend (kotak `+1σ` `+2σ` `−1σ` `−2σ`), abu `#6e7681`, mati sejak awal. Band dan Mean/Upper tidak ikut smoothing.
  - **Pane Deviation menyala sejak awal** (pilihan user): field baru `MetricFamily.extra_default=True`; `_init_state` memakai Bottom pane sebagai bawaan. Histogram navy alpha 0,80, dim 0,45.
  - Rasio 3 desimal, Deviation 2. Legend dua baris di 1440 px (ada kelompok σ Bands).
- **Terukur:** tooltip 30 Dec 2016 cocok CSV — AVIV 1.551 · Mean 1.078 · Upper 1.295 · +1σ 1.512 · −2σ 0.211 · Deviation 1.09 · BTC 970. MVRV tetap Z-Score Hidden sejak awal.
- Garis ambang tetap tidak dipasang (Mean/Upper adalah seri data yang bergerak, bukan ambang tetap).

### 3.23 Cek kualitas data kandidat halaman — 17 Sep 2026
Dicek per CSV: tanggal bolong, nilai macet (sama dengan kemarin sejak 2016), lonjakan (perubahan harian robust-z > 20), satuan, cakupan, kecocokan `btc_price` dengan `data_mvrv.csv`, dan **revisi historis** (membandingkan CSV di setiap commit data 15 Agt–16 Sep). Tidak perlu diulang kecuali data berubah.

| Kandidat | Kualitas data | Framework v2 / KB |
|---|---|---|
| AVIV | Bagus sejak 2012; rasio > 5 hanya 83 hari sebelum 2012; band bawah negatif s/d 2014; `price_at_aviv_*` salah basis | Ya (Z3/Z4/Z5); KB MVRV & Price Level — **sudah dibuat, 3.22** |
| HODL Waves | **Paling bersih**: 12 band supply dan realized cap selalu berjumlah 100%; bolong hanya 5 hari Jan 2009; loncatan antarband wajar (koin menua melewati batas, mis. 21 Mei 2026 3m-6m → 6m-12m = 6 bulan sesudah 22 Nov 2025). Butuh bentuk chart baru (area bertumpuk) | Tidak |
| CDD / VDD | CDD bersih, tanpa nol/NaN sejak 2012; lonjakan nyata (Mt.Gox 28 Mei 2024 518 juta, whale 4 Jul 2025 420 juta). ⚠️ `vdd_multiple` = VDD harian ÷ MA365 (bukan 30d ÷ 365d seperti Glassnode). File tanpa harga. Bolong 5 hari Jan 2009 | Tidak (research menolak "VDD multiple < 1" sebagai filter) — **dipilih berikutnya** |
| Realized Cap | Bersih: LTH + STH = total (≤ 0,01%). Loncatan LTH +7,2% 26 Apr 2026 wajar (koin 22 Nov 2025 genap 155 hari). Isi ≈ RP × supply, mirip Price Levels | Tidak |
| Exchange | net = in − out persis; Δbalance ≈ net_flow. ⚠️ 8 hari 2026 inflow = outflow = 0 (8 Apr, 18–19 Apr, 7 & 10 Mei, 12 & 28 Jul, 5 Agt) — data kosong diisi nol. ⚠️ `btc_price` beda sumber di 2026 (152 hari beda > 0,5%, maks 16% 5 Feb) → ambil harga dari `data_mvrv`. Lompatan −100k BTC 28 Jul 2021. Berakhir sehari lebih awal | Tidak |
| RHODL | = persen realized cap band 1d-1w ÷ 1y-2y (tanpa pengali umur pasar Glassnode; `realized_cap_1w` = band 1d-1w saja, satuan %). Puncak 443 (2011), p99 sejak 2012 = 37, median 0,40. Didominasi penyebut | Tidak |
| Apparent Demand | Hari pertama −952k (artefak). Lonjakan +325k 22 Nov 2025 (p99 sejak 2016 ±58k). data_dictionary: dua kali diuji sebagai sinyal → REJECT | Tidak |
| Treasury 2Y | Bulanan, 1976 – 1 Agt 2026 (garis tangga di chart harian). Pipeline masih perubahan user yang belum di-commit | Tidak |
| LTH Flow | ❌ `lth_pl_flow_btc` bukan BTC (−0,20…+0,06, dibulatkan 4 desimal → 171 hari sama dengan kemarin; revisi 10 Sep sampai 1100%). Arti `lth_pl_price` tidak jelas (2,2× LTH cost basis) | Tidak — skip |
| Futures Basis | ❌ Hanya 1 baris (22 Agt 2026) | Tidak — skip |
| Search Trends | ❌ Google Trends ditulis ulang tiap update (±160 hari lama berubah per hari; 9 Sep 4.980 hari). Sebelum ±2019 bentuk tangga (data bulanan). Wikipedia stabil (mulai Jul 2015) | Tidak — skip (Google) |

**Revisi data ChartInspect 10 Sep 2026 (commit data `c99e761`):** seluruh sejarah AVIV, realized cap HODL, VDD MA, dan LTH flow dihitung ulang. Besarnya kecil sejak 2016: median 0,1–0,6%, p99 1–4%, terbesar ±12% (12–13 Mar 2020); `aviv_mean` median +0,23%. MVRV hanya 62 hari, supply HODL dan CDD praktis tidak berubah. Revisi kecil juga 27 Agt (±65 hari). Di luar dua tanggal itu data on-chain stabil antar-update. Artinya angka lama bisa bergeser sedikit; bukan penghalang.

**⚠️ Temuan framework (belum diputuskan, user cek di Claude.ai; framework tidak diubah):** `Decision_Framework v2.md` menulis "703 hari Z5" (2011–2026). Dengan rumus AVIV yang benar (dashboard, `alert_check.py`) = **1.279 hari**; dihitung ulang dengan kolom `price_at_aviv_*` yang salah basis = **710 hari** (selisih 7 kemungkinan dari revisi 10 Sep). Jadi angka framework kemungkinan besar berasal dari kolom salah basis — yang masih dianjurkan `references/data_dictionary.md`. Angka framework lain yang dihitung dari kolom itu mungkin ikut terpengaruh. Per tahun (rumus benar): 2013 48 · 2016 90 · 2017 355 · 2018 24 · 2019 36 · 2020 65 · 2021 229 · 2024 185 · 2025 235 (plus 2010 113, 2011 12).

### 3.24 Kontrol diingat per halaman + tombol Style di dalam chart — SELESAI 17 Sep 2026 (valid menurut user, di-push bersama RHODL Waves)
**Item 1, pilihan a (ingat selama tab browser terbuka):** `_init_state` menyimpan nilai terakhir setiap kontrol halaman ke gudang biasa `st.session_state[f"{k}_mem"]` dan memakainya lagi kalau key widget dibuang `st.navigation`. Berlaku untuk Range (preset/From/To), Smoothing (jenis; periode memang sudah key biasa), Scale, BTC price, pane bawah, Display (tinggi + sumbu per garis). Reload browser = sesi baru = kembali ke bawaan (pilihan b lewat URL query belum dikerjakan; bisa ditambah di atasnya). Terukur: SOPR Range 1y → MVRV → SOPR tetap 1y; MVRV Scale metrik Linear + smoothing 30/90 tetap sesudah pindah ke SOPR dan balik. Tidak ada peringatan Streamlit.
**Item 2, opsi B (Line style di dalam chart):**
- Kotak **Line style di baris kontrol dihapus** (8 → 7 kotak): popover, `_render_line_style`, `_reset_line_style`, `_style_summary`, lambang `STYLE_GLYPHS/ICONS`, `import base64`. Python tetap memberi **gaya bawaan** per periode (`_assign_styles`: Dotted → Step → Band, `smoothing_style_default` F&G tetap), tanpa membaca widget.
- **Tombol "Style"** (ikon tiga garis, kelas `hl fsbtn`) di baris sorot, sesudah pemisah dan sebelum Scale/Full. Klik → **panel `#gaya`** 236 px di pojok kanan atas area gambar, tepat di bawah baris legend (rata dengan jarak kanan bar). Isi per periode: "SMA 30D" + tebal (px), lima lambang SVG (Solid · Dotted · Dashed · Step · Band), slider tebal 0,5–5 langkah 0,25; tombol "Reset to default". Tanpa smoothing: keterangan "Turn on Smoothing to style its lines." Klik di luar panel atau Esc menutup.
- **Tanpa memuat ulang chart** (terukur `bootedAt` sama): `pasangGaya` mengubah `spec.style/steps/alpha/width` lalu `applyOptions` (garis + kembaran Loss), warna tepi kotak periode di legend, lalu `apply()` (warna pita) dan `sesuaikanTangga(true)` (daftar garis tangga kini dihitung ulang tiap kali). Band = alpha 0,60 seperti dulu. Ganti bentuk tidak mengubah tebal (sama dengan perilaku popover lama).
- **Tersimpan di localStorage per halaman** (`state.gaya = {"30": {name, width}}`), jadi **bertahan juga setelah reload** dan saat chart dibangun ulang (terukur: Band SMA30 tetap sesudah pindah halaman). Satu pilihan per periode untuk semua garis (MVRV/STH/LTH SMA30 sama).
- Terukur MVRV 1440: panel top 62 (bar 60), Band → warna rgba 0,6 ketiga garis SMA30; Step 90 lebar 4 → lineType 1, pola putus panjang di zoom All (3).
- Catatan kecil: CSS `stSlider` "px" dan `stButtonGroup code` di `app.py` dulu untuk popover Line style, sekarang tidak terpakai (dibiarkan).

### 3.25 CDD/VDD — DITUNDA 17 Sep 2026 (keputusan user: belum butuh)
Sudah dipratinjau (data harian 2024–16 Sep 2026), belum diputuskan. Bahan untuk nanti:
- **`vdd_multiple` CSV = VDD harian ÷ MA365** (VDD = CDD × harga; cocok median 0,999). Sangat berisik: perubahan harian median 0,36; p99 sejak 2012 = 12,3; maks 59,9; lonjakan Mt.Gox 28 Mei 2024 = 52.
- **Rumus Glassnode 30d MA ÷ 365d MA** (dihitung dari `vdd_30d_ma / vdd_365d_ma`): halus (perubahan harian 0,016), p99 6,5, maks 8,4; puncak per siklus 2013 8,4 · 2017 5,2 · 2021 4,5 · 2024 4,4 · 2026 0,93.
- Usulan Claude waktu itu: rumus 30d/365d, garis acuan 1,0 (definisi, bukan ambang), CDD batang navy (Linear/Log dipratinjau), VDD Multiple violet, BTC Separate pane, harga dari `data_mvrv.csv` (CSV tanpa harga), mulai 17 Jul 2010. Research menolak "VDD multiple < 1" sebagai filter (findings_framework_review 17 Jul 2026).

### 3.26 Halaman RHODL Waves → HODL Waves — SELESAI 17 Sep 2026 (versi pertama `e7768f6`; ganti nama, Overlay, dan rapikan valid menurut user, di-push)
Dipilih user sesudah CDD/VDD ditunda. Pratinjau widget (data dua mingguan 2011–2026) dengan dua pilihan warna dan urutan; user memilih **A (spektrum), band muda di bawah, dan saklar Supply | Realized Cap**.
- **Data:** `data.load_hodl_waves()` dari `data_hodl_waves.csv`: kolom `RC <band>` (realized_cap_*) dan `Supply <band>` (supply_*), 12 band dari `data.HODL_BANDS` (24h · 1d–1w · 1w–1m · 1m–3m · 3m–6m · 6m–12m · 1y–2y · 2y–3y · 3y–5y · 5y–7y · 7y–10y · 10y+). Baris sebelum harga BTC pertama (2009 – 16 Jul 2010) dibuang. Kedua bobot selalu berjumlah 100.
- **Tampilan:** menu "RHODL Waves", kelompok baru **Holder Behavior** (sesudah Profitability), `/rhodl-waves`. BTC Separate pane Log. Sumbu 0–100 (`metric_range`), tanpa ruang bawah (`scaleMargins` atas 0,03 bawah 0) supaya dasar pane = 0 %. Warna spektrum muda → tua: `#d73027 #f46d43 #fdae61 #fee08b #d9ef8b #a6d96a #66bd63 #1a9850 #35978f #2166ac #5e4fa2 #9e7bd6`. Satu desimal.
- **Jenis seri baru `kind="stack"`** (`Series`/`Line`: `stack_index`, `stack_cols`; `MetricFamily.stack_units`): tiap band = `addAreaSeries` dari garis kumulatif ke dasar pane (top/bottom/lineColor sama, lebar 1, tanpa label nilai terakhir dan penanda kursor). Dibuat dari band tertua (kumulatif 100) ke termuda supaya area kecil tergambar di atas. Legend dan tooltip memakai urutan sendiri: legend muda → tua; **tooltip tua di atas** (sama dengan susunan warna).
- **`tumpuk()`** menghitung kumulatif di browser dari band yang menyala, dengan kolom bobot yang dipilih; dipanggil `apply()` dan hanya bekerja kalau bobot atau daftar band berubah. **Mematikan band di legend menumpuk ulang band yang tersisa** (terukur: 24h mati → 1d–1w pindah ke dasar, 10y+ 100 → 99,15).
- **Saklar bobot `Realized Cap | Supply`** di baris sorot (pilih satu; bawaan Realized Cap = RHODL Waves, Supply = HODL Waves), tersimpan di localStorage (`state.stackUnit`). Tooltip membaca kolom bobot aktif. Tanpa memuat ulang chart.
- Band tidak punya tombol Highlight (12 tombol terlalu padat) dan tidak ikut smoothing; baris sumbunya tidak muncul di popover Display.
- **Terukur:** tooltip 09 Nov 2020 cocok CSV — Realized Cap 24h 3.1 · 1d–1w 10.3 · 1w–1m 13.4 · 2y–3y 17.5 · 3y–5y 3.7 · 10y+ 0.0; Supply 24h 1.4 · 1d–1w 4.8 · 3y–5y 10.2 · 10y+ 9.8; BTC 15,330. MVRV, Supply in Profit, Funding & OI, Fear & Greed tetap termuat tanpa error.
- **Rapikan 17 Sep (sesudah push `e7768f6`, belum di-commit, diminta user):**
  - Angka sumbu berentang tetap (0–100) ditulis bulat kalau nilainya bulat (100, 90 — bukan 100.0); pecahan tetap memakai precision (66.8). Berlaku juga Supply in Profit dan Fear & Greed. Terukur lewat `priceFormatter().format`: 100→"100", 66.8→"66.8", 105→"".
  - Tombol Style hanya muncul kalau ada garis smoothing (terukur MVRV: Off → tidak ada, SMA 30d → ada).
  - Kelompok Highlight (label + None + tombol) disembunyikan kalau tidak ada yang bisa disorot selain BTC; pemisah sebelum Style/Full ikut disembunyikan.
  - Legend: band bertumpuk duluan, kelompok lain sesudahnya dalam urutan asli (sort stabil; halaman lain tidak berubah — terukur MVRV/SOPR/Funding).
- **Riwayat RHODL Ratio di halaman ini (17 Sep, sudah dibatalkan):** sempat pane bawah, lalu garis di pane harga BTC (dengan dukungan `Series.pane="price"` + skala tumpang `ovl_`). User lalu memilih **dua halaman terpisah** (lihat 3.28); dukungan `pane="price"` **dibuang lagi** karena tidak terpakai — renderer kembali seperti sebelum 17 Sep untuk bagian itu.
- **Ganti susunan 17 Sep (keputusan user dari usulan "pisah dua halaman"):**
  - Nama menu dan judul **"HODL Waves"** (seperti ChartInspect, karena ada saklar Supply), `key="hodl_waves"`, alamat **`/hodl-waves`** (dulu `/rhodl-waves`; localStorage lama `dash_v2_rhodl_waves` tidak dipakai lagi). Saklar bawaan tetap Realized Cap.
  - **BTC price bawaan Overlay** (harga di atas band, sumbu kanan Log; band sumbu kiri 0–100), seperti foto ChartInspect user.
  - **Garis BTC putih `#ffffff`** (permintaan user; oranye tenggelam di band 1w–1m/1m–3m). Field baru `MetricFamily.btc_color` + `btc_dim` (putih 0,17 = redup 1,70:1; oranye tetap 0,28). Hanya halaman ini; halaman lain tetap oranye (terukur RHODL Ratio `#F7931A`).
  - **Urutan gambar:** band dibuat **sebelum** seri lain (dulu sesudah), supaya garis harga Overlay tergambar di atas area (terukur: sebelum perbaikan garis putih tertutup band).
  - Baris tombol: `Realized Cap | Supply │ Full` (Highlight tersembunyi, tidak ada smoothing).
- User 17 Sep bertanya risiko kalau Line style memakai opsi A (klik kotak periode di legend) alih-alih B — dijawab di chat, belum ada keputusan ganti.

### 3.27 Halaman Cohort State (Cohort State Plane) — DITAHAN 17 Sep 2026 (user perlu memastikan sesuatu dulu)
User meminta analisa RHODL Ratio dari sesi lain dimasukkan ke dashboard (mengirim gambar `research/cohort_state_plane.png`). Sementara hanya RHODL Ratio yang ditampilkan (bagian 3.26); sisanya ditahan.
**Sumber:** `research/analyze_cohort_state_plane.py` (hitung) + `research/plot_cohort_state_plane.py` (gambar) + `research/findings/_cohort_state_plane.csv` (data s/d 7 Sep 2026), 9–10 Sep 2026. Memori `rhodl-didominasi-penyebut`: 86% varians rasio dari penyebut, korelasi −0,82 → baca tiga angka berdampingan.
- **RHODL Ratio** = RC (6m–12m + 1y–2y) ÷ (1d–1w + 1w–1m + 1m–3m).
- **Demand Impulse (DI):** fresh_share (RC 1d–3m) ÷ SMA90 − 1 → persentil jendela 1.460 hari (min 60 %). Hanya butuh `data_hodl_waves.csv`.
- **Aged Cohort Turnover (ACT):** BTC dibelanjakan kohort 6m–2y (profit + loss BTC band 5 dan 6 dari endpoint `realized-profit-by-age`) ÷ BTC yang dipegang kohort itu ((supply 6m–12m + 1y–2y)/100 × (lth_supply_btc + sth_supply_btc)), SMA30 → persentil 4 tahun.
- **State:** histeresis per sumbu (tinggi kalau ≥ 60, rendah kalau ≤ 40, pindah hanya setelah 10 hari berturut), empat kombinasi: DORMANSI/SEPI, DISTRIBUSI/LEPAS TANPA BID, TRANSFER/TANGAN BERGANTI, AKUMULASI/MODAL MASUK PASOKAN TERKUNCI. Mulai 7 Mar 2013, 60 episode, median 76 hari; hari per state: Dormansi 1.589 · Transfer 1.285 · Akumulasi 1.088 · Distribusi 971. Terakhir 7 Sep 2026: RHODL 3,45 · DI p73 · ACT p12 · Akumulasi. Tanpa lookahead (persentil hanya jendela ke belakang).
- **Cek data 17 Sep:** pemetaan band terverifikasi (band_5_net_usd = `rpl_m6_12m`, band_6 = `rpl_y1_2y`, selisih 0). Band 5/6 profit/loss BTC sejak 2013: tanpa NaN, tanpa tanggal bolong, tidak ada nilai macet; banyak hari bernilai 0 (loss band 5: 2.616 hari; profit band 5: 803) — wajar (seluruh kohort untung atau rugi). Persentil 4 tahun cepat (0,03 detik untuk 5.900 hari).
- **Penghalang:** data ACT **tidak ada di CSV repo**. Analisa lama membaca `rpba.pkl` di scratchpad sesi lain (`C:/Users/yudiy/AppData/Local/Temp/claude/.../2b546005-.../scratchpad/rpba.pkl`, s/d 9 Sep 2026). `auto_update.py` memanggil endpoint itu dua kali (pipeline 2 dan 9) tapi hanya menyimpan rasio turunan. Butuh pipeline baru yang menyimpan `data_profit_by_age.csv` (profit/loss BTC 12 band); workflow `update_data.yml` sudah `git add .`.
- **Pratinjau widget (data mingguan)** sudah ditunjukkan: pita state (B) vs latar pane (A), DI + ACT dengan pita 40–60, RHODL Ratio opsional; warna state gelap: Quiet `#6e7681`, Selling no bid `#bf5546`, Changing hands `#a8963f` (bukan mustard — mustard nyaris sama dengan oranye BTC bagi buta warna), Inflow supply locked `#3f6fd8`; DI `#5b8def`, ACT `#e0705c`.
- **Jawaban user 17 Sep:** (1) izin ubah `auto_update.py` — **tahan**; (2) bentuk state pita/latar — **tahan**; (3) RHODL Ratio — **tampilkan sekarang** (akhirnya halaman sendiri, bagian 3.28), persentil DI/ACT **disembunyikan dulu**; (4) nama state Inggris (Quiet · Selling, no bid · Changing hands · Inflow, supply locked) — **keep dulu** (belum dipakai); (5) letak menu "Cohort State" di Holder Behavior di bawah RHODL Waves — **ya, tapi ditahan** (sekarang rencananya digabung ke halaman RHODL Ratio, 3.28), user perlu memastikan sesuatu dulu.
- **Catatan tafsir yang sudah disampaikan:** state terlambat minimal 10 hari (histeresis); persentil bergeser kalau ChartInspect merevisi data (seperti 10 Sep); pratinjau mingguan menyembunyikan episode pendek. Bukan bagian framework v2 (research menyebut framework belum punya ukuran kedatangan pembeli baru di K4) — keputusan framework tetap di Claude.ai.

### 3.28 Halaman RHODL Ratio — SELESAI 17 Sep 2026 (valid menurut user, di-push)
User ingin melihat HODL Waves + harga saja di satu tempat, dan membandingkan RHODL Ratio + harga di tempat lain; memilih **dua halaman terpisah** (alternatif satu halaman dengan saklar/legend ditolak: pane kosong tetap memakan tempat).
- **Data:** `data.load_rhodl_ratio()` dari `data_hodl_waves.csv`: realized cap (6m–12m + 1y–2y) ÷ (1d–1w + 1w–1m + 1m–3m), baris sebelum harga pertama dibuang. **Cocok persis** dengan `research/findings/_cohort_state_plane.csv` di 5.906 hari (tooltip 10 Aug 2026 = 4.00; 16 Sep = 3.487). Rentang 0–6,72 (maks 26 Okt 2022). **Bukan** `rhodl_ratio` di `data_rhodl.csv` (1d–1w ÷ 1y–2y).
- **Tampilan:** menu "RHODL Ratio" (Holder Behavior, di bawah HODL Waves), `/rhodl-ratio`, judul **"RHODL Ratio (6m–2y ÷ 1d–3m)"** (rumus di judul supaya tidak tertukar). Garis navy `#0070a6`, 2 desimal, ikut smoothing. **BTC Overlay satu pane dengan rasio, skala Auto untuk keduanya** (permintaan user 17 Sep, sempat Separate pane + Log): rasio sumbu kiri, harga oranye sumbu kanan; kalau BTC dipindah ke Separate pane, rasio ke sumbu kanan. Terukur: satu pane, kiri dan kanan mode 0 (linear), kotak Scale "Auto", Display "Left".
- **Rencana:** kalau Cohort State (3.27) dilanjutkan, Demand Impulse, Aged Cohort Turnover, dan pita state ditambahkan **ke halaman ini**, bukan halaman ketiga.
- Pengingat memori `rhodl-didominasi-penyebut`: 86 % varians dari penyebut — rasio tinggi bisa berarti modal segar hilang ATAU kohort lama menahan.

### 3.5 Kotak L / R untuk pilihan sumbu — ditahan
Ide user: tombol Left/Right diganti dua kotak kecil "L" dan "R" bergaya kotak angka periode di legend. Hasil ukur: **tidak menghemat lebar sama sekali** (lebar popover ditentukan baris CHART HEIGHT, bukan baris axis), hanya menghemat tinggi ±14 px per baris. Ditahan sampai ada halaman dengan garis banyak — bukan khusus HODL Waves, metrik lain juga bisa. Kalau dipakai, pakai untuk semua halaman sekaligus.

---

## 4. Yang sudah selesai

### File dan struktur
| File | Isi |
|---|---|
| `app.py` | Entry point v2 (dulu `app_v2.py`, diganti nama 13 Sep saat v2 live), menu `st.navigation` berkelompok (14 Sep), sidebar, seluruh CSS global (termasuk aturan `:fullscreen`). |
| `.streamlit/config.toml` | Tema v2: `base = "dark"`, `primaryColor = "#006d77"`. Dipakai Streamlit Cloud dan `streamlit run app.py` lokal. |
| `archive/app_v1.py` | Dashboard v1 (dulu `app.py`), diarsipkan 13 Sep beserta perbaikan `minBarSpacing`. |
| `dashboard/registry.py` | Konfigurasi keluarga metrik (`MetricFamily`, `Series`, `RefLine`). Menambah halaman = menambah satu `MetricFamily`. |
| `dashboard/metric_page.py` | Tata letak halaman: header, kontrol, gaya garis smoothing, rencana garis. |
| `dashboard/charts.py` | Memilih mesin chart (Lightweight / Plotly). Dataclass `Line`. |
| `dashboard/lw_chart.py` | Chart lightweight-charts yang digambar langsung di browser via `st.iframe`. Pane dibangun dari daftar (harga / metrik / tambahan), legend, sorot, geser sumbu, zoom tersimpan, tangga adaptif, tombol layar penuh. |
| `dashboard/data.py` | Loader CSV, SMA/EMA, filter tanggal, Z-Score rolling 1Y/2Y/4Y. |

Halaman yang sudah dibuat: **MVRV** (`data_mvrv.csv`: MVRV, STH MVRV, LTH MVRV + garis acuan Neutral 1,0, plus MVRV Z-Score dan Rolling Z-Score di pane tambahan), **Price Levels** (bagian 3.1), **SOPR** (bagian 3.9), **Supply in Profit** (bagian 3.12–3.13).

### Kontrol di halaman (8 kotak, semuanya bergaya sama; Tooltip ditambah 14 Sep, bagian 3.10)
- **Range** — preset **1m / 3m / 6m / 1y / 4y / All** (huruf kecil sejak 13 Sep supaya seragam dengan "7d" dan "1y"; nilai di baliknya tetap "1M" dst.) plus tanggal From/To yang disejajarkan satu baris. Default **All**. **Sejak 14 Sep (pilihan B) Range tidak memotong data**, hanya menentukan rentang tampil awal — lihat Perilaku.
- **Smoothing** — tab SMA/EMA, kisi 3×3 (Off, 7d, 14d, 30d, 60d, 90d, 200d, 365d, 730d), input periode sendiri + tombol Add. Multi-periode.
- **Scale** — Auto/Linear/Log terpisah untuk metrik (kiri) dan BTC (kanan).
- **BTC price** — Overlay / Separate pane / Hidden. Bawaan per halaman lewat `MetricFamily.btc_mode_default`: MVRV, SOPR, Supply in Profit = Separate pane; Price Levels = Overlay.
- **Z-Score** — Hidden (default) / Bottom pane. Kotak ini hanya muncul untuk keluarga metrik yang punya seri `pane="extra"`. Nama kotaknya diambil dari `MetricFamily.extra_label` (MVRV: "Z-Score"; bawaan "Bottom pane"), karena isi pane bawah beda per halaman. Saat Hidden, seri Z-Score **tidak dikirim sama sekali** (bukan sekadar disembunyikan), supaya sumbu pane metrik tidak ikut menghitungnya.
- **Display** — tinggi chart 600/720/860/1000 px + sumbu kiri/kanan per garis, **termasuk BTC Price** (ditambah 13 Sep). Tiap baris: nama di kiri, tombol Left/Right di kanan. Kotak BTC Price mati sendiri saat mode harga bukan Overlay ("Only for BTC price = Overlay"), karena di Separate pane harga punya pane sendiri. Nilai di kotak Display menulis Left / Right / Mixed dan **sengaja tidak menghitung BTC** — kalau ikut dihitung, keadaan bawaan (metrik kiri, harga kanan) selalu menulis "Mixed" dan jadi tidak berarti apa-apa.
- ~~**Chart** — Lightweight / Plotly~~ — **dibuang 13 Sep 2026** bersama mesin Plotly. Semua fitur hanya dibuat untuk Lightweight, jadi Plotly selalu tertinggal dan tiap fitur baru harus dibuat dua kali. Kodenya masih ada di commit `37697ce` kalau suatu saat perlu. `plotly` tetap di `requirements.txt` karena dipakai `app.py` lama.
- **Line style** — per garis smoothing: bentuk dan tebal (slider 0,5–5 px, langkah 0,25). Nilai di kotak menulis Off / Default / Custom, plus tombol **Reset to default**. Bentuk ditampilkan **sebagai lambang saja**, namanya ada di tooltip tanda tanya: Solid `────`, Dotted `····`, Dashed `╌╌╌╌` (teks monospace lewat format kode, tepat empat karakter), Step dan Band berupa **gambar SVG 31×12 px** (Step: satu anak tangga naik, garis saja; Band: balok 4,5 px dengan transparansi sama dengan pita di chart, 0,60). Kelima tombol terukur sama lebar, 49 px.
- Kotak **Screen sudah dihapus** — tombol layar penuh pindah ke dalam chart (lihat Perilaku).

### Gaya garis smoothing (bawaan)
Gaya diberikan menurut urutan periode dan **menempel pada periodenya** — mematikan periode lain tidak menggeser gaya periode yang masih menyala.

| Urutan | Bentuk | Tebal |
|---|---|---|
| ke-1 | Dotted (titik-titik) | 2 px |
| ke-2 | Step (garis tangga) | 1,5 px |
| ke-3 | Band (pita tembus pandang 60%) | 3 px |

Periode ke-4 dan seterusnya mengulang ketiga gaya itu dengan garis 0,5 px lebih tebal. Warna selalu mengikuti metrik induknya.

### Tampilan
- Warna garis: MVRV navy `#0070a6`, STH rust `#bf5546`, LTH teal `#0b8e89`, BTC oranye `#F7931A`. Semua garis utama **2 px** (sejak 13 Sep; sebelumnya 1,5 px — lihat bagian 5).
- **Header Streamlit transparan, tombol pembuka sidebar kembali** (13 Sep, laporan user: setelah sidebar ditutup tombolnya tidak muncul). Dulu `stHeader` di-`display:none`, padahal `stExpandSidebarButton` tinggal di dalamnya (terukur 0×0 px). Sekarang header dan semua anaknya `background: transparent; pointer-events: none`, Deploy/menu/`stToolbarActions` tetap `display:none`, hanya tombol pembuka sidebar `pointer-events: auto`. Terukur (1440): tombol 28×28 px, klik mengenai tombol, sidebar terbuka lagi; judul halaman dan tombol Range tidak tertutup; aturan `:fullscreen` tetap menyembunyikan header.
- **Teal gelap `#006d77` warna utama dashboard** (keputusan user 13 Sep 2026). Aksen kontrol: latar teal 40% + garis tepi + teks putih.
  - `#006d77` **tidak dipakai sebagai warna huruf**: kontrasnya 3,1:1 di latar halaman `#0e1117` dan 2,9:1 di sidebar `#151924`. Pakai sebagai isian, garis tepi, lencana, atau garis aksen; tulisan di atasnya putih (6,1:1). Kalau tulisan memang harus berwarna teal, pakai teal terang `#2aa6b0` (hue sama, 6,0:1 di sidebar).
  - **Sidebar ikut teal** (13 Sep): menu aktif bergaris kiri `#006d77` dengan latar `#102e39` (teal 25% di atas sidebar); tulisan "ON-CHAIN DASHBOARD v2" `#2aa6b0`. Ungu `#a855f7` sudah tidak dipakai di v2. Sejak 14 Sep menu memakai `st.navigation` dengan judul kelompok teal terang (bagian 3.11); CSS radio lama dibuang.
- **Judul halaman (gaya B2, 13 Sep):** kategori (`family.title`, sama dengan nama menu sidebar) jadi lencana kecil — 11 px, huruf besar, renggang 0,12em, tebal 600, putih di atas `#006d77`, sudut 4 px. Di bawahnya nama metrik (`family.subtitle`) jadi judul **1,15rem (18,4 px) tebal 600 putih**, sama dengan menu sidebar, dengan "Latest data: <tanggal>" sebaris di kanan (0,72rem `#8b90a0`, rata garis dasar). Dibangun dari `div`, bukan `h3`, supaya Streamlit tidak menambah ikon tautan. Terukur: tepi kiri lencana, judul, tombol, dan chart sama-sama di x=380 (viewport 1440); jarak judul ke tombol 14,6 px (sama dengan judul lama).
- Popover ringkas: jarak tepi 12–14 px, judul kecil 11 px, tombol 12 px / tinggi minimal 26 px.
- Kotak tanggal tanpa latar abu, isinya rata tengah, kalender bawaan browser diwarnai lewat `accent-color`.
- Baris KPI **sudah dibuang**.
- **Ukuran kontrol dirapatkan (13 Sep).** Tombol aksen 45×32 → 33×26 px, kotak tanggal 40 → 28 px. Streamlit memaku tinggi tombol di 32 px, jadi `height` harus ditimpa langsung — `min-height` dan padding tidak mempan. Hasil: popover Display 240×372 → 234×254, Range 253×158 → 253×140, Smoothing 186×204.
- **Judul kecil di semua popover seragam** (11 px, huruf besar, renggang): PRESET, FROM, TO, SMOOTHING, nama metrik, BTC PRICE, CHART HEIGHT, AXIS. Label bawaan widget dimatikan (`label_visibility="collapsed"`).
- **Perataan kiri:** huruf pertama judul halaman, subjudul, baris tombol, dan tepi kiri chart semuanya di satu garis. Kotak lencana teal lurus dengan kotak tombol; subjudul digeser 10 px sebesar jarak dalam lencana.
- **Tulisan di dalam tombol rata tengah.** Streamlit memasang teks `st.button` sebagai baris *inline* di kotak baris yang lebih tinggi daripada hurufnya, jadi huruf duduk di garis dasar (2,3 px di bawah tengah) sementara semua segmented control duduk 0,5 px di atas tengah. Dinormalkan lewat CSS (`display:block` + `line-height`). Seluruh kontrol sudah diukur ulang dan rata; dua yang sengaja tidak ditengahkan: menu sidebar (label rata kiri) dan nama metrik di legend (didahului contoh garis berwarna).

### Perilaku
- **Legend dikelompokkan per metrik**: satu label untuk garis utama, lalu angka periode smoothing sebagai titik kecil yang bisa diklik sendiri-sendiri. Empat kelompok muat satu baris tanpa geser samping; kalau kepanjangan, membungkus ke baris berikutnya.
- **Awal baris legend selalu lurus** (13 Sep). Nama kelompok yang bukan tombol (Rolling Z-Score) diberi jarak dalam dan garis tepi transparan yang sama dengan tombol (`span.lg`: padding 3px 8px, border 1px). Sebelumnya contoh warnanya mulai 9 px lebih kiri setiap kali kelompok ini membuka baris baru. Terukur: contoh warna semua kelompok mulai 9 px dari tepi kelompoknya, teks di tengah (12 px).
- **Kelompok legend tanpa garis utama** (dipakai Rolling Z-Score): kalau tidak ada seri yang namanya persis nama kelompok, nama kelompok jadi keterangan (bukan tombol) dan semua anggotanya jadi kotak angka: "Rolling Z-Score **1y · 2y · 4y**". Angka di kotak dinaikkan 1 px (tinta "1y" sempat meleset 1,5 px ke bawah karena ekor huruf y; sekarang 0,5 px).
- **Seri boleh lahir dalam keadaan mati** (`hidden_default=True`, dipakai 2y dan 4y). Chart menyimpan daftar `seen` di `localStorage`; nilai bawaan hanya diterapkan pada seri yang belum pernah muncul, jadi pilihan user tidak ditimpa di kunjungan berikutnya.
- **Tombol sorot memakai nama pendek** dari registry (`short`) kalau ada: None · MVRV · STH · LTH · BTC · **Z** · **Z roll**. Tanpa `short`, bawaannya kata pertama label — dan tiga seri berawalan "MVRV" jadi kembar.
- **Mode sorot bisa lebih dari satu garis.** Klik lagi untuk mematikan, None mengosongkan. Garis yang tidak disorot diredupkan pada kontras 1,70:1 (MVRV 0,49 · STH 0,44 · LTH 0,39 · BTC 0,28).
- **Menarik chart atas-bawah menggeser sumbu milik garis yang disorot** (bisa dua sumbu sekaligus, jarak sama). Tanpa sorotan, perilaku bawaan library. Klik dua kali mengembalikan semua sumbu ke Auto. Penguncian baru terjadi kalau tarikan jelas vertikal (≥ 6 px dan lebih tegak daripada mendatar), supaya menggeser ke samping tidak mengunci sumbu.
- **Slider rentang di bawah chart** (14 Sep, semua halaman): BTC Price skala Log, jendela teal yang bisa digeser, ditarik lebarnya (minimal 8 bar), atau dipindah dengan klik di area gelap. Zoom/geser chart dan tombol Range ikut menggerakkan slider; menggeser slider tidak mengubah tulisan kotak Range. Rincian dan hasil ukur di bagian 3.2.
- **Range memindahkan jendela, bukan memotong data** (14 Sep, pilihan B). `metric_page.py` memanggil `apply_filters` dengan `dmin..dmax` (seluruh sejarah) dan mengirim tanggal From/To sebagai `view`. Di browser tanggal itu diubah ke posisi bar (bar pertama ≥ From, bar terakhir ≤ To) lalu dipasang lewat mekanisme pemulihan zoom yang sama. **Tanggal Range ikut sidik data** (`sig` = jumlah bar : tanggal awal : tanggal akhir : From : To), jadi menekan Range tetap menang atas zoom tersimpan, sedangkan rerun lain (smoothing, skala, BTC price) memulihkan zoom terakhir. Terukur: Range 1y → chart 14 Sep 2025 – 14 Sep 2026, slider tetap berisi 2010–2026; geser slider lalu nyalakan SMA 30d → zoom tetap di bar 4625–4990. Setelah Range 1y, chart tetap bisa digeser ke tahun sebelumnya. Peringatan "No data in this date range" kini diperiksa dari rentang tampil. Sisa perubahan sekali: zoom yang tersimpan dengan format sidik lama diabaikan sekali.
- **Zoom dan posisi bertahan** saat Streamlit menggambar ulang chart, termasuk saat berganti Overlay ↔ Separate pane. Disimpan sebagai posisi bar (bukan tanggal) di `localStorage`, dengan sidik data supaya tombol Range tetap menang. Cara kerjanya: zoom simpanan dipasang ulang sampai rentang yang tampil benar-benar cocok, dan fase pemulihan itu tetap hidup sampai lebar sumbu harga mengendap (±2 detik) — lihat bagian 10 kenapa memeriksa sekali di awal tidak cukup. Fase berhenti begitu pengguna menyentuh chart, dan menyerah setelah 6 detik supaya zoom baru tetap bisa disimpan.
- **Tombol layar penuh ada di dalam chart**, ujung kanan baris sorot, dipisah garis tipis. Satu tombol bersimbol: "Full" masuk layar penuh, berganti jadi "Exit" saat aktif; Esc juga keluar dan tombolnya ikut menyesuaikan (`fullscreenchange`). Klik di dalam chart sudah merupakan gestur pengguna, jadi `requestFullscreen()` dipanggil langsung — tidak ada status di Python, tidak ada skrip penyisip. User sudah mengujinya di browser sendiri dan menyatakannya sesuai.
- **Saat layar penuh, judul halaman disembunyikan dan jarak kiri-kanan dipangkas dari 80 px jadi 16 px** (13 Sep, permintaan user dengan acuan tata letak CryptoQuant — hanya kerangka halaman; isi, posisi, dan desain di dalam chart sengaja tidak diubah, termasuk legend). Aturannya `:fullscreen` di `app_v2.py`; judul ditandai kelas `page-title`. Diuji dengan meniru aturan itu lewat kelas pada `<html>` di viewport 1920×1080: baris tombol naik ke y=24, chart dari x=380 lebar 1460 jadi x=16 lebar 1888. Layar penuh sungguhan harus dicek user di browsernya sendiri.
- **Saat layar penuh, chart mengisi sisa tinggi jendela.** Tinggi iframe dan wadahnya ditimpa sementara, pane dibagi ulang menurut perbandingan tinggi awalnya, lalu dikembalikan persis saat keluar. Ikut menyesuaikan kalau ukuran jendela berubah.
- **Tinggi baris legend ikut isinya** (13 Sep, opsi B). Kalau legend atau kelompok Highlight tidak muat satu baris, baris baru ditambahkan dan **tinggi pane chart dikurangi sebesar itu** — tinggi total chart di halaman tetap, legend tidak pernah terpotong, sumbu waktu tetap terlihat. Satu baris tetap 40 px. Legend minimal 320 px; kalau sisa tempat lebih sempit, kelompok Highlight turun ke baris sendiri, rata kanan. Sebelumnya tinggi dipaku 40 px: di layar 1440 dengan Z-Score + 3 smoothing, baris MVRV/STH terpotong ke atas dan Rolling Z-Score tertutup chart. Hasil ukur sesudah perbaikan (Z-Score + smoothing 7/60/365):

  | Layar | Baris legend | Pane (atas + bawah) | Pane bawah pas di dasar bingkai |
  |---|---|---|---|
  | 1440, polos | 1 (40 px) | 720 (sama dengan dulu) | ya |
  | 1440 | 3 | 475 + 204 | ya |
  | 1100 | 3 + Highlight baris sendiri | 456 + 195 | ya |
  | 1920 | 2 | 495 + 212 | ya |

  Cara kerja: `C.frameHeight` dikirim dari Python; tinggi pane = tinggi bingkai − tinggi baris legend sebenarnya − jarak antar-pane (`sesuaikanTinggiLayar`), dipicu ResizeObserver pada baris legend **dan** dari `rapikanBar` (cadangan, lihat bagian 10). Sinkron sumbu hanya dijadwalkan kalau tinggi benar-benar berubah, supaya `rapikanBar` ↔ sinkron sumbu tidak berputar.
- **Celah kosong di kiri saat chart melebar sudah diperbaiki** (13 Sep). Library mempertahankan lebar bar, bukan rentang. Sekarang: kalau sebelum lebar berubah seluruh data sedang tampil (bar 0 sampai terakhir), chart dipaskan ulang (`fitContent`); kalau sedang zoom ke rentang pendek, dibiarkan. Terukur: Range All, lebar 980 → 1460 px, bar pertama tetap di x = −1.
- **Baris legend dan tombol diluruskan ke area gambar**, bukan ke tepi iframe: jarak kiri = lebar sumbu kiri, jarak kanan = lebar sumbu kanan, **minimal 10 px** (tanpa minimal itu, saat semua metrik di sumbu kiri, tombol Full menempel ke batas chart — ditemukan user).
- **Garis tangga adaptif**: di bawah 6 piksel per hari polanya berubah jadi putus panjang, di atas itu kembali jadi tangga penuh. Data tidak diubah.
- **LTH otomatis pindah ke sumbu kanan** saat BTC dipisah ke pane sendiri, dan kembali ke kiri saat Overlay.
- Legend on/off dan mode sorot bekerja di browser tanpa reload, tersimpan di `localStorage` key `dash_v2_<family.key>`.
- **Yang bertahan dan yang kembali ke default saat halaman di-reload** (dijelaskan ke user 13 Sep): legend on/off, Highlight, dan zoom **bertahan** (localStorage). Semua kontrol Python — Range, Smoothing, Scale, BTC price, pane bawah, Display, **Line style** — **kembali ke default**, karena disimpan di sesi server Streamlit dan reload membuka sesi baru. Membuat kontrol Python ikut diingat = pekerjaan terpisah, belum diminta.
- **Tombol Highlight hanya untuk kelompok yang punya garis menyala** (13 Sep, semua halaman). Kelompok yang dimatikan seluruhnya juga dilepas dari sorotan, supaya chart tidak meredupkan semua garis demi garis yang tidak kelihatan. Terukur: MVRV — STH MVRV dimatikan → tombol STH hilang, sorotan STH dilepas; dinyalakan lagi → kembali. Price Levels — 12 tombol → 8.
- **Aturan format angka tambahan** (13 Sep): untuk precision 0, nilai 0 tetap "0" (sumbu linear), tick semu antara −0,01 dan 0 dikosongkan (sumbu Log sempat menulis "-0.0001"), angka positif < 0,01 ditulis dua angka penting (0.00015). Angka negatif sungguhan tetap tampil (−10,000; −50.00). Versi pertama sempat mengosongkan semua nilai ≤ 0 dan menghapus label 0 di sumbu linear — ketahuan dari screenshot, sudah diperbaiki.
- Klik di dalam chart dan tombol Escape menutup popover yang terbuka.
- **Pane dibangun dari daftar**, bukan dipaku dua: `price` (harga BTC bila dipisah) → `main` (metrik) → `extra` (Z-Score). Zoom, geser, dan lebar sumbu semua pane tersinkron; sumbu waktu hanya di pane paling bawah. Pembagian tinggi: tiga pane 30/45/25 %, harga+metrik 45/55 %, metrik+Z-Score 70/30 %. Pane `extra` **selalu linear** — Z-Score melewati nol, jadi Log tidak berlaku; hasilnya Log di pane metrik aman lagi dipakai.
- **MVRV Z-Score**: histogram **navy `#0070a6`** (ikut warna induknya, MVRV), **pekat 80 %**. **Rolling Z-Score 1y/2y/4y**: histogram hijau `#97c459`, transparan 55 %, dihitung di `data.py` dari MVRV Ratio terhadap rata-rata dan simpangan 365/730/1460 hari (data 2y mulai 2013, 4y mulai 2014). Keduanya **tanpa smoothing** (`smoothing=False`). Dikonfirmasi user 13 Sep 2026 (lihat bagian 5).
  - Kenapa navy 80 %, bukan 55 %: navy lebih gelap dari hijau; pada 55 % kontrasnya ke latar chart cuma 1,83:1, pada 80 % 2,54:1. Redup saat mode sorot (`dim` 0,45 × 0,80) = 1,44:1, setara violet lama (1,40:1), jadi `dim` tidak diubah.
  - Warna lama sebelum 13 Sep: violet `#7f77dd` untuk Z-Score (dipilih lewat jarak Lab, 39/18 terhadap garis yang ada).

### Teknis
- Streamlit di laptop user: **1.63.0**, dikunci `streamlit==1.63.0` di `requirements.txt`.
- Dashboard v2 **wajib dijalankan dengan tema teal gelap** (lihat bagian 11). Tanpa itu, warna aksen kembali merah dan latar popover jadi putih.
- Dashboard v1 (sekarang `archive/app_v1.py`) diuji di 1.63.0: 12 halaman tanpa error. Diubah sekali atas permintaan user (wrapper `renderLightweightCharts` + `minBarSpacing`).
- `components.html` sudah diganti `st.iframe` (dengan fallback).
- **Format angka per seri** (13 Sep): field `precision` di `Series` (registry) dan `Line` (charts), bawaan 2; harga BTC `BTC_PRECISION = 0` di `metric_page.py`, garis smoothing mewarisi precision induknya. Di `lw_chart.py`, `formatSeri(spec)` memasang `priceFormat: {type: 'custom'}` pada tiap seri, jadi sumbu, label nilai terakhir, label garis silang, dan tooltip memakai fungsi yang sama, `angka(v, p)`: pemisah ribuan en-US; untuk precision 0, harga < 100 tetap 2 desimal dan harga < 1 sampai 4 desimal tanpa nol di belakang (0.60, 0.0495) supaya harga BTC 2010 tidak terbaca "0". Terukur: 0.60 · 0.15 · 0.0495 · 8.09 · 100 · 78,905 · 1,600,000.
- **Tooltip membaca periode smoothing dari nama seri** "<metrik> <SMA|EMA>(<periode>)" (dibuat di `metric_page.py`). Kelompok tanpa garis utama (Rolling Z-Score) → tiap anggota satu baris. Nilai diambil dari `D.cols` lewat indeks tanggal, bukan dari `param.seriesData`, supaya pane mana pun yang disentuh kursor menghasilkan isi yang sama. Hanya pane yang sedang memegang tooltip boleh menyembunyikannya (saat pindah pane, pane lama melapor kosong sesudah pane baru mengisi).
- **Field baru `MetricFamily.extra_label`** (13 Sep): nama kotak kontrol pane bawah. `default_selection` / `default_series()` dibuang (tidak terpakai). `charts.py` sekarang hanya berisi `Line` dan `render()` yang meneruskan ke `lw_chart`.
- **Field baru `Series` di registry** (13 Sep): `kind` ("line"/"histogram"), `smoothing`, `short`, `alpha`, `group`, `hidden_default`, `pane` ("main"/"extra"). `Line` di `charts.py` ikut membawa `kind`, `short`, `hidden_default`. `lw_chart.render()` sekarang menerima `extra_lines`.
- **Field baru 14 Sep:**
  - `MetricFamily.group` (kelompok menu + lencana judul), `MetricFamily.url_path` (alamat halaman), `MetricFamily.btc_mode_default` (keadaan awal kotak BTC price; SOPR "Separate pane" — `_init_state` langsung memakai `separate_axis` kalau bawaannya Separate pane).
  - `Series.whole_from` / `Line.whole_from`: angka sebesar ini ke atas ditulis tanpa desimal (`angka(v, p, bulatDari)` dan `angkaSeri(spec, v)` di `lw_chart.py`).
  - `RefLine.all_axes`: satu garis acuan di setiap sumbu yang memuat metrik.
  - `lw_chart.render(..., tooltip=)` dan `C.tooltip` di browser (`posisikanTooltip`).
- **Garis acuan mewarisi `precision` dan `whole_from` metrik di sumbunya** (14 Sep) — lihat bagian 10 kenapa.
- **Field baru pembaruan keenam (14 Sep):** `MetricFamily.metric_range` (sumbu metrik tetap, dikirim sebagai `C.metricRange`), `MetricFamily.complement` (`C.complement`, judul kolom tooltip + saklar), `Series.complement_color` / `Line.complement_color` (warna kembaran Loss). `lw_chart.render(..., metric_range=, complement=)` dan `charts.render` meneruskannya.
- **Di browser (`lw_chart.py`):** `rentangTetap(spec)` memasang `autoscaleInfoProvider` 0–100 + formatter yang mengosongkan angka di luar rentang; `handle.kembar` = seri Loss; `bisaDibalik(spec)` = garis metrik pane utama (bukan BTC, bukan garis acuan); `apply()` mengatur nyala/warna Profit, Loss, kotak smoothing Loss (`titikLoss`), label kelompok (`labelKelompok`), dan saklar. Kelompok legend diurutkan BTC Price terakhir.
- **Pembaruan kedelapan (15 Sep):** di browser `adaFullscreenApi()`, `sedangSemu()`, kelas `penuh-semu` (`KELAS_SEMU`), tombol `skalaBtn` (hanya kalau `sentuh`); `app.py` aturan `html.penuh-semu …` di samping setiap aturan `:fullscreen` dan `@media (max-width: 768px)` untuk jarak atas. Tidak ada field Python baru selain bawaan MVRV di registry.
- **Pembaruan kesembilan (16 Sep), field baru:**
  - `Series`: `negative_color` (histogram dua warna), `unit` / `pair` / `compact` (saklar satuan, pasangan sisi sumbu, format K/M/B), `gradient` (garis bergradasi `[[nilai, hex], …]`), `smoothing_color`, `smoothing_precision`, `value_labels` (nama kelas di tooltip).
  - `RefLine.follow` (garis acuan di sumbu seri tertentu).
  - `MetricFamily`: `unit_switch`, `unit_label`, `smoothing_default` (periode menyala sejak awal), `smoothing_style_default` (gaya per periode, mis. `{30: "Band"}`; dipakai `_default_style` di `metric_page.py`).
  - `Line` di `charts.py` membawa field yang sama; `charts.render` / `lw_chart.render` menerima `unit_switch`, `unit_label` → `C.unitSwitch`, `C.unitLabel`.
  - Di browser (`lw_chart.py`): `warnaiTitik` (warna per titik, diwarnai ulang saat diredupkan Highlight), `warnaGradasi` / `cssGradasi`, `angkaRingkas`, `satuanTampil` / `satuanTooltip`, `aturSisiSumbu` (pindah `priceScaleId` + parkir seri mati), `aturAngkaSumbu` (warna angka sumbu per pane), `handle.sisi` (sisi sumbu sekarang; `seriesOn` dan tarik-sumbu memakainya), `labelNilai`.
  - Loader baru: `load_nupl`, `load_derivatives`, `load_fear_greed`.
- **Field baru pembaruan ketujuh (14 Sep):** `lw_chart.NAV_H = 52`, `NAV_COL = "BTC Price"`; `C.nav` (kolom isi slider atau None), `C.navHeight`, `C.view` (tanggal From/To). `lw_chart.render(..., view=)` dan `charts.render(..., view=)`. Di browser: `gambarNav()` (dipanggil dari `rapikanBar` dan dari perubahan rentang chart), `rentangRange`, `zoomSimpanan`; `pulihkanZoom` sekarang = zoom tersimpan atau rentang Range.
- **Desimal data yang dikirim ke chart ikut precision seri** (14 Sep): `_num(v, digits)` dengan `digits = max(4, precision + 1)` untuk nilai < 1000. Sebelumnya dipaku 4 desimal, sehingga gap 5 desimal tampil dari angka yang sudah terpotong.

---

## 5. Keputusan final — jangan dibahas ulang

- **Timeframe (Daily/Weekly/…) dihapus.** Resampling `.last()` membuang data dan menggeser tanggal cross sampai 6 hari — berisiko untuk K3/K4. Pakai SMA/EMA.
- **Default Range = All.** Ide "muat semua tapi tampil 1 tahun" **sebagai default** dan menyalin bundle komponen chart dibatalkan. (Sejak 14 Sep data memang selalu dimuat penuh karena pilihan B, tapi default tetap All.)
- **OHLC di-skip.** ChartInspect memang tidak punya OHLC (bagian 10).
- **Baris KPI dibuang**, diganti tulisan "Latest data".
- **Palet garis final:** MVRV navy, STH rust, LTH teal `#0b8e89` (bukan aqua terang). Ketiganya dipilih supaya setara terang; syarat warna sengaja dilonggarkan (user menarik permintaan "MVRV harus paling menonjol").
- **Teal gelap `#006d77` warna utama seluruh dashboard**, termasuk sidebar (13 Sep 2026, menggantikan keputusan lama "sidebar tetap ungu"). Aksen kontrol gaya latar 40%.
- **Teal gelap tidak pernah jadi warna huruf** (kontras 3,1 / 2,9). Teal dipakai sebagai latar, garis, atau lencana; tulisan teal memakai `#2aa6b0`.
- **Judul halaman gaya B2**: lencana kategori teal kecil + nama metrik sebagai judul 18,4 px tebal 600. Gaya A (garis aksen) dan C (jejak dengan lencana di nama metrik) ditolak.
- **Histogram MVRV Z-Score navy 80 %, Rolling hijau.** Usulan navy + violet sudah diuji dan ditolak: sama-sama biru gelap saat bertumpuk (jarak Lab 24 untuk mata normal, 10 saat buta warna; navy + hijau 61/59).
- **Uji buta warna = cek cepat, bukan syarat mutlak** (disepakati 13 Sep). Gunanya terutama menangkap warna yang bedanya cuma corak dengan terang mirip, yang juga sulit dibedakan mata normal saat garis tipis/redup. Jadi penting kalau dashboard dibuka untuk umum.
- **Gaya smoothing:** titik-titik → tangga → pita, seperti tabel di bagian 4. Gaya menempel pada periodenya.
- **Simbol/marker untuk membedakan garis smoothing ditolak user** (terlalu ramai).
- **Legend berkelompok per metrik** (bukan satu label per garis).
- **Tebal garis 2 px** untuk semua garis utama termasuk BTC (`LINE_WIDTH` di `metric_page.py`, diputuskan user 13 Sep setelah membandingkan di localhost; menggantikan 1,5 px). Alasan: library tidak membulatkan tebal garis data, jadi 1,5 px di layar rasio piksel 1 tampak seperti 1 px tajam + tepi samar. Garis smoothing tidak diubah (titik-titik 2 px kini setebal garis utama, dibedakan polanya; pita 3 px).
- **Popover Scale memakai nama metrik** (misalnya "MVRV OSCILLATORS"), bukan kata "Metric".
- **Tata letak panel bertumpuk tidak dipakai** untuk halaman MVRV.
- **Tingkat terang legend, angka periode, dan mode sorot sengaja berbeda** (kontras 14,5 / 10,0 / 5,8 : 1). Itu hierarki: isi chart → anak isi → alat. Menyamakannya juga memperkecil beda antara tombol sorot aktif (putih, 17,9:1) dan yang tidak aktif. Dibahas 13 Sep, diputuskan tetap.
- **Label "Highlight" tetap setara tombol di sebelahnya** (12 px `#8B949E`). Versi redup 11 px `#6E7681` sudah dicoba dan ditolak: jadi sulit dibaca.
- **Kotak Display tidak menghitung BTC** — lihat bagian 4.
- **MVRV Z-Score di pane ketiga, bukan di chart MVRV dan bukan halaman terpisah.** Alasan utama bukan kerapian tapi skala: Z-Score punya nilai negatif (terendah −0,66), jadi begitu sumbunya dipasang Log bagian negatifnya hilang tanpa peringatan. Digabung ke chart MVRV sudah dicoba dan ditolak (terlalu padat).
- **Histogram Z-Score polos satu warna.** Gradasi warna menurut nilai (gaya ChartInspect) ditunda; bisa dibuat dengan warna per titik di `addHistogramSeries`, tapi gradasi di dalam satu batang tidak bisa.
- **Tidak ada pita "Extreme Overvaluation" berambang tetap.** KB MVRV v1.4 §5.3B: ambang ekstrem Z-Score turun struktural tiap siklus (9,24 → 3,66 → 2,53) karena dilusi sejarah, jadi pita di angka tetap menyesatkan. Kalau suatu saat butuh penanda zona, itu keputusan framework — baca Decision Framework v2 dulu, jangan diselipkan ke pekerjaan tampilan.
- **Z-Score full-history untuk aturan, rolling untuk mata.** Jendela rolling bisa dipilih (1y/2y/4y), tapi mengganti jendela tidak membuatnya jadi sinyal — kesimpulan KB berlaku untuk metodenya, bukan untuk angka 365 hari.
- **Tombol layar penuh satu saja, di dalam chart**, keluar lewat Esc. Kotak Screen di baris kontrol dihapus.
- **Line style tanpa nama, lambang saja** (nama di tooltip). Step = pilihan B (satu anak tangga naik).
- **Halaman SOPR tata letak B** (BTC Separate pane, LTH-SOPR sumbu kanan, Log), **rumus gap KB §12**, desimal SOPR 3 / gap 5, LTH-SOPR ≥ 100 tanpa desimal, pane Gap mati sejak awal (14 Sep, bagian 3.9).
- **Tooltip: Fixed / Cursor / Off, bawaan Cursor, satu pilihan untuk semua halaman, latar 94 %** (14 Sep, bagian 3.10). Latar lebih tembus ditolak.
- **Menu: `st.navigation` (cara B), kelompok jenis metrik, nama menu pendek, judul kelompok teal terang `#2aa6b0`** (14 Sep, bagian 3.11). Pengelompokan "peran di framework" ditolak: menu ikut dirombak setiap framework berganti versi.
- **Supply in Profit: sumbu 0–100, tooltip Profit | Loss, legend "Total/STH/LTH in Profit"** (14 Sep, bagian 3.12). Loss bukan garis dari Python — kembaran 100 − nilai di browser.
- **Saklar Profit/Loss di dalam chart, dua-duanya bebas (boleh mati bersamaan), warna Loss set B, smoothing Loss lewat kotak kedua di legend (mati di awal)** (14 Sep, bagian 3.13).
- **BTC Price selalu terakhir** di legend, tombol sorot, dan tooltip (14 Sep, bagian 3.14).
- **Price Levels: judul "Price Levels", legend "Realized Price"** (STH RP/LTH RP tetap singkat) (14 Sep).
- **Slider rentang: isi BTC Price, semua halaman, 52 px, di dalam chart, digambar di kanvas** (14 Sep, bagian 3.2) — selesai, commit `8bb65d7`.
- **Range memindahkan jendela, data selalu seluruh sejarah (pilihan B)** (14 Sep). Pilihan A (Range memotong data, slider ikut terpotong) ditolak.
- **Supply in Profit: BTC price bawaan Separate pane** (14 Sep, bagian 3.12).
- **HP: sidebar "auto", geser jari atas-bawah menggulir halaman, tombol Scale khusus perangkat sentuh (tidak disimpan), layar penuh semu hanya untuk browser tanpa Fullscreen API** (15 Sep, bagian 3.15). **Tahap 2 khusus HP ditolak** (khawatir mengganggu laptop).
- **Angka sumbu terpotong setengah di tepi pane dibiarkan** — wajar, bawaan library; `entireTextOnly` tidak dipasang (15 Sep, bagian 3.15).
- **MVRV: bawaan BTC Separate pane, sumbu metrik dan harga Log** (15 Sep, bagian 3.16).
- **NUPL:** tanpa Ratio LTH/STH, sumbu tidak dipaku, pane Gap mati sejak awal, metrik di sumbu kanan saat Separate pane (16 Sep, bagian 3.17). **Supply in Profit** juga metrik kanan saat Separate pane.
- **Realized P/L ditunda** sampai ada KB dan keputusan ratio mana yang dipercaya (16 Sep, bagian 3.18).
- **Funding & OI:** satu pane (funding batang dua warna kanan, OI garis kiri), ΔOI bersih per bursa di pane bawah (mati awal), saklar BTC | USD boleh dua-duanya, USD pindah ke sisi kosong (16 Sep, bagian 3.19). Menu bernama "Funding Rates & Open Interest".
- **Angka sumbu per pane disembunyikan tanpa mengubah lebar** saat semua garis di sisi itu mati (16 Sep, bagian 3.20).
- **Fear & Greed:** BTC Separate pane, garis gradasi halus rust→abu→teal, SMA30 Band kuning pucat menyala sejak awal, nama kelas di tooltip, tanpa garis ambang framework (16 Sep, bagian 3.21).

---

## 6. Usulan yang disetujui user tapi belum diterapkan

- Latar brand `#0D1117` untuk halaman (sekarang `#0e1117` bawaan Streamlit dan chart `#131722`).
- Font **JetBrains Mono** untuk angka dan sumbu; Inter untuk label (sesuai brand bible user).
- Ide user yang ditunda: **overlay dua chart bertumpuk** (chart BTC di belakang, chart metrik transparan di depan, sumbu BTC di luar) untuk menampung banyak skala sekaligus. Batasan sudah dicek: sumbu harga selalu menempel pada area gambar, jadi sumbu ketiga berangka harus digambar sendiri; `setCrosshairPosition` dan latar transparan tersedia. User menilai ini "slightly over modif" untuk kebutuhan sekarang.

---

## 7. Belum dikerjakan

- ~~Slider rentang di bawah chart~~ — selesai 14 Sep (bagian 3.2, commit `8bb65d7`).
- ~~Push halaman Fear & Greed~~ — selesai 16 Sep (bagian 3.21). User belum sempat mengecek di browsernya sendiri sebelum push; kalau ada keluhan tampilan, ukur dulu di halaman hidup.
- **Halaman Cohort State — DITAHAN user** (bagian 3.27): tunggu kepastian user dan izin ubah `auto_update.py`.
- **Halaman metrik berikutnya — belum dipilih** (RHODL Waves selesai 17 Sep, bagian 3.26). Sembilan dari usulan 19 sudah ada (bagian 3.11); hasil cek data sisa kandidat di bagian 3.23. **CDD/VDD ditunda user** (bagian 3.25). Realized P/L ditunda (bagian 3.18); LTH Flow, Futures Basis, Google Trends di-skip (bagian 3.23).
- **Temuan "703 vs 1.279 hari Z5" di framework v2** — menunggu user di Claude.ai (bagian 3.23). Jangan ubah framework atau data_dictionary.
- **`auto_update.py` masih punya perubahan user yang belum di-commit** (pipeline 19 Treasury 2Y + `data_treasury_2y.csv` di daftar master). Jangan ikut di-commit tanpa izin; kalau perlu commit hunk lain, stage per hunk (`git diff` → saring hunk → `git apply --cached`).
- **Detail kecil Supply in Profit yang sudah dilaporkan ke user, belum diminta diubah:** saat saklar Profit dan Loss sama-sama mati, nama di legend tetap tampil normal (tidak dicoret) walau garisnya tidak ada; dengan smoothing menyala legend kembali dua baris (kotak angka dobel) dan label nilai terakhir di sumbu kiri makin padat (lihat poin label bertumpuk di bawah).
- ~~Semua kontrol Python diingat per halaman~~ — **dikerjakan 17 Sep, pilihan a (selama tab terbuka), menunggu uji user (bagian 3.24).** Catatan lama: Sekarang Range, Smoothing, Scale, BTC price, pane bawah, Display, dan Line style kembali ke bawaan setiap pindah halaman (terukur: Range 1y di SOPR → All setelah ke MVRV dan balik), karena `st.navigation` membuang nilai widget halaman lain. Pola solusinya sudah ada: gudang key biasa + widget sebagai cerminan (`TIP_STORE` untuk Tooltip, `{key}_lstyles` untuk Line style). Belum diputuskan: cukup selama sesi browser, atau juga setelah reload (butuh URL query atau localStorage).
- **Rumus gap STH-SOPR di `alerts/alert_check.py` berbeda dari KB §12** — menunggu keputusan user di Claude.ai (bagian 3.9). Jangan diubah tanpa diminta.
- ~~Desain judul halaman~~ dan ~~warna histogram Z-Score~~ — selesai 13 Sep 2026 (bagian 3.6, 4, 5).
- **Lambang Step dan Band (gambar SVG) duduk 1,2 px berbeda secara vertikal** dari tiga lambang teks di sebelahnya. Di screenshot tidak terlihat dan user belum mengeluh; kalau dilaporkan, geser gambar 1 px ke atas.
- **Gradasi warna histogram Z-Score** — ditunda user, bagian 5.
- **Label nilai terakhir di sumbu bertumpuk** (terlihat 13 Sep, belum dibahas dengan user). Dengan smoothing 3 periode menyala, halaman MVRV punya 12 label nilai terakhir berderet di sumbu kiri (MVRV/STH/LTH × garis utama + 3 smoothing) dan saling menimpa. Sudah ada sebelum pekerjaan 13 Sep. Kandidat solusi (belum dipilih): label nilai terakhir hanya untuk garis utama (`lastValueVisible` false untuk garis smoothing — nilainya tetap terbaca di tooltip), atau hanya untuk garis yang disorot. Tanyakan dulu dengan pratinjau.
- ~~Legend padat di layar sempit~~ — selesai 13 Sep (tinggi baris legend ikut isinya, bagian 4).
- ~~Celah kosong di kiri chart saat chart melebar dengan zoom All~~ — selesai 13 Sep (bagian 4).
- **Range All tidak selalu memuat seluruh sejarah — tidak terulang di chart yang sudah tergambar, kemungkinan artefak panel** (diusut 13 Sep). Terlihat lagi 14 Sep di panel Claude (SOPR All mulai ±2012); di browser user SOPR mulai 2010 — artefak panel, bukan bug. Rentang direkam tiap 100 ms sambil mengganti Range 1y → All: tampilan "±160 bar terakhir" hanya ada **sebelum chart pertama kali tergambar** (lebar sumbu masih 0, area gambar = lebar penuh bingkai). Begitu frame tergambar (dipicu screenshot), rentangnya langsung penuh (bar 0–5896) dan tidak mundur. Cocok dengan panel browser Claude yang membekukan frame. Kode tidak diubah. Kalau user melihatnya di browsernya sendiri, usut dari situ.
- **Riwayat masalah tombol layar penuh (selesai, lalu seluruh mekanismenya diganti tombol di dalam chart — disimpan sebagai catatan).** Cara kerja lama:
  1. Kotak **Screen** (Normal | Full) hanya mengubah `st.session_state[f"{k}_screen"]`. Saat "Full", `render_metric_page()` menyuntikkan CSS yang menyembunyikan sidebar, header, dan toolbar Streamlit sehingga chart memenuhi jendela.
  2. Layar penuh browser **tidak bisa dipanggil dari Python**, karena `requestFullscreen()` wajib dipanggil di dalam gestur klik. Jadi `app_v2.py` menyisipkan `_FULLSCREEN_SCRIPT` lewat `st.iframe`; skrip itu berjalan di dalam iframe, mengambil `window.parent.document`, mencari kelompok tombol yang berisi "Full" dan "Normal", lalu memasang pendengar klik fase-capture pada keduanya (`attach()` + `MutationObserver`, penanda `dataset.fsBound`). (Nama file waktu itu `app_v2.py`; sekarang `app.py`.)
  3. "Full" memanggil `doc.documentElement.requestFullscreen()`, "Normal" memanggil `doc.exitFullscreen()`.
  - **Sebab yang terbukti:** klik Full/Normal itu sendiri membuat Streamlit membangun ulang iframe skrip (mode Full menambah satu blok CSS, jadi urutan elemen bergeser). Konteks JavaScript lama mati bersama iframe-nya, tapi tombolnya tetap elemen DOM yang sama dan penanda `fsBound = '1'` ikut menempel — skrip baru mengira sudah terpasang lalu melewatinya. Sesudah rerun pertama tidak ada lagi pendengar yang hidup: Full (klik pertama) bekerja, Normal tidak pernah. Penanda `fsBound = 1` justru bukti pendengar mati, bukan bukti terpasang.
  - **Perbaikannya:** penanda diberi nomor unik per muatan skrip (`const ID = 'fs' + Math.random()...`), jadi konteks yang sedang hidup selalu memasang pendengarnya sendiri. Pendengar mati dari iframe lama tetap menempel tapi tidak pernah berbunyi.
  - **Catatan uji:** layar penuh sungguhan tidak bisa diuji dari panel browser Claude — panel itu memblokir Fullscreen API (`TypeError: Permissions check failed`, bahkan dari halaman utama). Yang bisa diuji dari sana cuma pemasangan ulang pendengarnya. User yang mengonfirmasi hasil akhirnya di browser sendiri.
  - **Akhir cerita:** atas usul user, tombolnya dipindah ke dalam chart. Kotak Screen, `_FULLSCREEN_SCRIPT` (58 baris), state `{k}_screen`, dan blok CSS penyembunyi kerangka dibuang semua; yang tersisa hanya aturan `:fullscreen` di `app.py` (dulu `app_v2.py`).
- ~~Mesin Plotly ketinggalan~~ — mesin Plotly dibuang 13 Sep (bagian 4).
- **Memindahkan Line style ke dalam chart** — lihat 3.3. Sebabnya: semua kontrol hidup di Python, dan setiap klik membuat Streamlit menggambar ulang komponen chart (iframe baru). Legend dan sorot tidak memuat ulang karena sudah hidup di dalam chart. Range dan Smoothing tidak bisa dipindah kecuali rata-rata bergerak dihitung di browser.
- **v2 SUDAH LIVE sejak 13 Sep 2026** (push `07164da..db1260d`, disetujui user). Langkah yang dijalankan: `app.py` (v1, termasuk perubahan 15 baris `minBarSpacing` yang belum di-commit) → `archive/app_v1.py`; `app_v2.py` → `app.py` supaya pengaturan Streamlit Cloud tidak perlu diubah; `.streamlit/config.toml` ditambahkan (tema teal gelap — dulu ditahan karena bentrok dengan v1); tulisan sidebar "Experimental build…" dihapus; README, `.claude/launch.json`, dan komentar `alerts/alert_check.py` disesuaikan. 12 commit data dari GitHub di-merge dulu (hanya CSV + `alerts/logs`, bersih), kedua halaman diuji dengan data terbaru (13 Sep) sebelum push. `.claude/settings.local.json` dan perubahan repo milik user (`CLAUDE.md`, `auto_update.py`, `references/`, `research/`) **tidak disentuh dan tidak di-push**. Alamat Streamlit Cloud belum diketahui sesi ini — minta ke user kalau perlu mengecek versi online.
- **Alur kerja yang disepakati (13 Sep):** trial and error di **localhost** dulu; baru setelah valid di-commit, lalu push ke GitHub (Streamlit Cloud deploy otomatis). Sebelum push, **selalu merge dulu dari GitHub** — GitHub Actions meng-commit data setiap hari, jadi repo lokal hampir selalu tertinggal.
- ~~Bersih-bersih kode~~ — selesai 13 Sep: CSS `button[kind="pills"]` dan `stPill` dibuang, aturan tombol `stButton` yang menumpuk disatukan, `default_selection` / `default_series()` dibuang. Diukur sebelum-sesudah dengan keadaan sama (smoothing 7/60/365): tombol kisi periode tetap 48,3 × 26 px, huruf 13,12 px, jarak dalam 3px 6px.
- **Ide untuk nanti:** memantau LTV intraday memakai harga 10 menit dari ChartInspect (bagian 10). Harga terendah intraday lebih relevan untuk risiko likuidasi daripada harga penutupan harian.

---

## 8. Data: file CSV dan kolomnya

Semua file punya kolom `date`. Kolom `btc_price` ada di sebagian besar file.

| File | Kolom |
|---|---|
| `data_mvrv.csv` ✅ dipakai | btc_price, mvrv_ratio, sth_mvrv, lth_mvrv, mvrv_zscore |
| `data_price_level.csv` | btc_price, sth_cost_basis, lth_cost_basis, realized_price, cvdd, active_realized_price, MVRV 0σ, true_market_mean_price, 200_dma, 50_wma, 200_wma, cum_pl_price, pl_price_ratio |
| `data_aviv.csv` ✅ dipakai (Price Levels, AVIV) | btc_price, aviv_ratio, aviv_mean, aviv_upper_1sd, aviv_upper_2sd, aviv_lower_1sd, aviv_lower_2sd, price_at_aviv_mean, price_at_aviv_plus_1_sigma, price_at_aviv_plus_2_sigma, price_at_aviv_minus_1_sigma, investor_cap, active_realized_price, liveliness |
| `data_momentum.csv` | btc_price, asopr, lth_sopr, sth_sopr, net_realized_pl_usd, nupl, sth_nupl, lth_nupl |
| `data_pl.csv` ⚠️ ratio bermasalah (bagian 3.18) | btc_price, daily_realized_profit_btc, daily_realized_loss_btc, rpl_ratio, sth_pl_ratio, lth_pl_ratio, rrp, rrl, relative_realized_pl |
| `data_supply.csv` | btc_price, lth_supply_btc, sth_supply_btc, pct_lth_in_profit, pct_sth_in_profit, pct_lth_in_loss, pct_sth_in_loss, percent_btc_in_profit, percent_btc_in_loss |
| `data_hodl_waves.csv` ✅ dipakai (HODL Waves, RHODL Ratio) | btc_price, lalu `supply_<band>` dan `realized_cap_<band>` untuk **12** band: 0-1d, 1d-1w, 1w-1m, 1m-3m, 3m-6m, 6m-12m, 1y-2y, 2y-3y, 3y-5y, 5y-7y, 7y-10y, 10y+ |
| `data_realized_cap.csv` | btc_price, realized_cap_usd, lth_realized_cap_usd, sth_realized_cap_usd |
| `data_rhodl.csv` | btc_price, rhodl_ratio, realized_cap_1w, realized_cap_1_2y |
| `data_cdd.csv` | cdd, vdd_30d_ma, vdd_365d_ma, vdd_multiple (tanpa btc_price) |
| `data_exchange.csv` | btc_price, total_balance, net_flow, inflow, outflow |
| `data_derivatives.csv` ✅ dipakai | btc_price, funding_rate, total_oi, lalu (sejak 16 Sep 2026) `oi_cme`, `oi_binance`, `oi_bybit`, `oi_hyperliquid`, `oi_bitget`, `oi_okx`, `oi_deribit`, `oi_coinbase`, `oi_bitmex`, `oi_kraken`, `oi_bitfinex`, `oi_mexc`, `oi_huobi` (BTC; total_oi = jumlahnya) |
| `data_futures_basis.csv` | btc_price, annualized_basis_3m, avg_tenor_days, n_exchanges, binance/deribit/okx/bybit_basis_annualized (file masih sangat kecil) |
| `data_sentiment.csv` | btc_price, trend_bitcoin, trend_crypto, trend_ethereum, trend_nft, wiki_bitcoin, wiki_cryptocurrency, wiki_ethereum, wiki_blockchain |
| `data_lth_flow.csv` | lth_pl_price, lth_pl_flow_btc (tanpa btc_price) |
| `data_apparent_demand.csv` | btc_price, apparent_demand |
| `data_fg.csv` ✅ dipakai | Fear & Greed (tanpa btc_price; loader mengambil harga dari data_mvrv.csv) |
| `data_treasury_2y.csv` | treasury_2y_yield |

Bukan untuk halaman: `data_master_all_metrics.csv` (file hasil generate) dan `data_*_events.csv` (file lama).

**Perhatian untuk halaman berikutnya:**
- Kolom `price_at_aviv_*` di `data_aviv.csv` **basis harganya salah** (tercatat di README). Hitung ulang dari `btc_price / aviv_ratio × aviv_mean`, seperti yang dilakukan `app.py`.
- Angka ChartInspect **tidak entity-adjusted**, jadi tidak akan sama dengan Glassnode.
- RHODL didominasi penyebutnya; tampilkan komponennya, jangan rasionya saja.
- **LTH MVRV bisa puluhan** di puncak siklus (2013: 47 · 2017: 36 · 2018: 26 · 2021: 12,5; 2011 bahkan 374), sementara MVRV maksimum 6 dan STH 2,8. Sejak 2013, LTH di atas 10 terjadi 571 dari 4.998 hari. Karena itu LTH otomatis pindah ke sumbu kanan saat Separate pane; untuk rentang panjang, pakai skala Log.
- Kalau halaman menyentuh threshold, zona, atau sinyal framework, **baca `references/Decision_Framework v2.md` dulu** (aturan `CLAUDE.md`). Claude Code tidak mengambil keputusan investasi.

---

## 9. Cara memilih warna untuk halaman baru

1. Muat skill **dataviz**. Jalankan `scripts/validate_palette.js` dari folder skill itu:
   `node validate_palette.js "<warna1>,<warna2>,...,#F7931A" --mode dark --surface "#131722" --pairs all`
   Selalu ikutkan oranye BTC `#F7931A`. Status FAIL "lightness band" untuk oranye boleh diabaikan, karena itu garis harga utama.
   - **Catatan 13 Sep:** skrip itu **tidak ditemukan** di mesin ini (skill dataviz tidak terpasang sebagai folder lokal). Sebagai gantinya dipakai hitungan Python sekali pakai — skripnya tidak disimpan di repo, buat ulang kalau perlu: ubah hex ke CIE Lab, hitung jarak ΔE (CIE76) tiap calon terhadap semua warna garis yang ada, lalu ulangi setelah kedua warna disimulasikan deuteranopia dan protanopia (ambil jarak terkecil). Patokan yang dipakai untuk warna Z-Score: jarak normal ≥ ±30 dan jarak buta warna ≥ ±14 dianggap lolos longgar; calon yang jaraknya satu digit terhadap oranye BTC saat buta warna dibuang (mustard `#c9a227` = 2).
2. **Syarat sengaja dilonggarkan** (permintaan user): cukup dua — tidak mirip oranye BTC, dan masih bisa dibedakan penderita buta warna dengan batas longgar. Syarat lama yang dicabut: MVRV harus paling menonjol, jarak ke warna aksen tombol, dan jarak ke hijau KPI (KPI sudah tidak ada).
3. **Pelajaran:** jangan paksa semua garis sama terang. Kalau terangnya sama, bedanya tinggal hue — dan hue justru yang hilang bagi mata buta warna. Perbedaan terang yang tipis membantu. Contoh nyata: menggelapkan aqua LTH agar setara navy membuat keduanya makin mirip (ΔE normal turun dari 17 ke 11); solusinya menggeser sedikit ke hijau (`#0b8e89`).
4. **Persentase redup saat disorot** dihitung per warna supaya semua garis redup punya kontras sama, sekarang **1,70:1** terhadap latar chart `#131722`: MVRV 0,49 · STH 0,44 · LTH 0,39 · BTC 0,28. Rumusnya: cari opasitas α sehingga warna yang dicampur ke latar chart punya kontras itu.
5. Karena user tidak bisa menilai dari kode hex, **selalu tunjukkan pratinjau widget dengan data asli** sebelum bertanya.

---

## 10. Jebakan teknis yang sudah ditemukan

### Streamlit
- **Streamlit Cloud juga tidak membaca ulang `dashboard/` setelah push.** 14 Sep: sesudah push `073a997`, versi online error `AttributeError` di `family.group` — `app.py` baru, `registry.py` lama masih di memori. Kode di GitHub benar; obatnya user membuka **Manage app → ⋮ → Reboot app**. Setiap push yang mengubah `dashboard/` (field baru di registry, fungsi baru), ingatkan user untuk reboot bila muncul error sejenis.
- **Setelah mengubah file di `dashboard/`, restart server v2.** Streamlit membaca ulang `app.py` setiap render, tapi modul di `dashboard/` yang sudah dimuat tidak dibaca ulang.
- **`st.rerun()` memotong satu putaran.** Widget yang belum sempat digambar (misalnya isi popover Line style) **nilainya dibuang Streamlit**. Karena itu gaya garis disimpan di gudang terpisah `st.session_state[f"{k}_lstyles"]` (dict biasa), sedangkan widget hanya cerminan yang disemai ulang tiap render.
- **Tombol tidak boleh mengubah nilai widget di badan `if st.button(...)`** — Streamlit menolak dengan `StreamlitWidgetAlreadyInstantiatedError`. Pakai `on_click=` callback, yang berjalan sebelum halaman digambar ulang.
- **`st.rerun()` membuang nilai widget yang belum sempat digambar.** Bukan cuma isi popover yang sedang terbuka: *semua* kontrol yang letaknya sesudah titik rerun ikut hilang nilainya. Gejalanya di sini: menekan tombol periode Smoothing membuat kotak Screen balik sendiri ke "Normal" padahal browser masih layar penuh (kotak Screen digambar paling ujung). Obatnya bukan menambal satu per satu — hapus `st.rerun()`-nya, pakai `on_click=`. Sesudah itu Display, Chart, dan Line style ikut aman.
- **Iframe komponen dibangun ulang kalau urutan elemen di atasnya berubah**, walau isinya sama persis. Penanda tetap yang ditulis ke DOM halaman induk (mis. `dataset.xxx = '1'`) akan bertahan padahal konteks yang menulisnya sudah mati — pakai nomor unik per muatan, jangan nilai tetap.
- **Jangan sembunyikan `header[data-testid="stHeader"]` dengan `display:none`** — tombol pembuka sidebar (`stExpandSidebarButton`) ada di dalamnya. Dan `pointer-events: none` pada header saja tidak cukup: `stToolbar` di dalamnya menyalakan lagi penangkap kliknya sendiri dan menutupi klik di atas judul halaman. Terapkan ke `header ... *`, lalu nyalakan kembali hanya untuk tombol pembuka sidebar.
- **Wadah teks (`stMarkdownContainer`) punya `margin-bottom: -16px`.** Tinggi tata letaknya jadi 16 px lebih pendek daripada kotak yang terlihat. Kalau dipakai bersama `st.columns(vertical_alignment="center")`, isinya jatuh 8 px di bawah garis tengah. Batalkan dengan `margin-bottom: 16px` pada div sendiri.
- **Tinggi tombol dipaku 32 px oleh Streamlit.** `min-height` dan `padding` tidak bisa mengecilkannya; `height` harus ditimpa langsung.
- **Teks `st.button` dipasang sebagai baris *inline*** di kotak baris yang lebih tinggi daripada hurufnya, jadi duduk di garis dasar (2,3 px di bawah tengah) sementara `st.segmented_control` duduk 0,5 px di atas tengah. Perbaikannya `display:block` + `line-height` pada `p` di dalam tombol.
- **Label `st.segmented_control` menerima Markdown gambar, termasuk data URI SVG** (`![nama](data:image/svg+xml;base64,...)`), dan lebar tombolnya tidak berubah. Sudah diuji. Gambar tidak ikut berganti warna putih saat opsinya dipilih — kotaknya tetap menyala teal, jadi tanda pilihan tetap jelas.
- **Supaya lambang teks selebar sama, tulis sebagai kode** (`` `────` ``): Streamlit memakai Source Code Pro (monospace), jadi empat karakter apa pun = 31,2 px. Kotak abu bawaan kode dihilangkan lewat CSS `[data-testid="stButtonGroup"] button code`.
- **Legend di dalam chart tidak bisa membuat pane.** Pane dibangun saat chart digambar dari sisi Python, jadi saklar pane (kotak Z-Score) harus kontrol Python, bukan tombol legend.
- **Caption punya `margin-bottom: -16px` bawaan.** Wadahnya jadi lebih pendek dari tulisannya dan tertimpa elemen di bawah. Dinetralkan di CSS popover.
- **Memberi opsi `--theme.*` apa pun membuat tema dasar jadi terang.** Wajib menyertakan `--theme.base dark`.
- **Isi popover dirender di portal terpisah**; CSS tidak bisa diturunkan dari `div[data-testid="stPopover"]`. Pakai `[data-testid="stPopoverBody"]`.
- **Popover tertutup oleh event `click` di luar atau Escape**, bukan `mousedown`/`pointerdown`. Chart meneruskan keduanya ke halaman induk (awal `<script>` di `TEMPLATE`).
- **Kalender tanggal adalah milik browser** (input `type=date`), muncul di luar halaman dan tidak bisa di-CSS. Warnanya diatur lewat `accent-color` pada input.
- **Nama atribut berubah di 1.63:** opsi radio terpilih memakai `data-selected` (dulu `data-checked`), dan bulatan radio bukan lagi anak pertama label. CSS sidebar lama diam-diam berhenti bekerja karena ini.
- Elemen yang sedang difokus memakai bayangan merah bawaan; ditimpa dengan bayangan teal (`:focus-visible` dan `[data-focus-visible]`).
- **Pindah halaman lewat `st.navigation` membuang nilai widget, walau key dan widget-nya sama persis di tiap halaman** (terukur 14 Sep: Tooltip Fixed di SOPR jadi Cursor lagi di MVRV; dengan `st.radio` lama tidak terjadi untuk widget yang sama). Nilai yang harus bertahan disimpan di key biasa `st.session_state` (bukan key widget), lalu widget disemai dari situ dan `on_change` menulis balik.
- **`st.navigation` menaruh menu di paling atas sidebar**, di atas isi `with st.sidebar`. Urutannya dibalik lewat `[data-testid="stSidebarContent"] { display:flex; flex-direction:column }` + `order` pada `stSidebarHeader` (0), `stSidebarUserContent` (1), `stSidebarNav` (2). Test id lain: `stNavSectionHeader` (judul kelompok, ada panah lipat tersembunyi), `stSidebarNavLink` (aktif = `aria-current="page"`), `stSidebarNavSeparator`.
- **`st.Page` dengan fungsi:** identitas halaman dihitung dari `url_path` (`calc_hash`), nama bawaan dari `__name__`. Halaman dibuat lewat pabrik `_halaman(family)` dengan `__name__` unik + `url_path` eksplisit. Halaman `default=True` beralamat root (`/`).
- **Sesaat setelah sidebar dibuka, lebarnya terbaca 0 dan teks merek pecah per huruf** — itu animasi pembuka, bukan bug. Ukur ulang sesudah ±1 detik (terukur 300 px).

### lightweight-charts 4.2.3
- **`minBarSpacing` kecil (0.005)** supaya `fitContent()` sanggup menampilkan ~5.900 titik harian.
- **Tebal garis data tidak dibulatkan** (dicek di kode 4.2.3): garis seri digambar `lineWidth × pixelRatio` apa adanya; hanya garis kisi dan garis silang yang `Math.floor`. Tebal pecahan (1,5) di layar rasio 1 jatuh di antara piksel dan tampak tipis. Bilangan bulat (2) tajam.
- **`fitContent()` tidak bekerja selama lebar chart 0.** Hasilnya chart berhenti di lebar bar bawaan (±160 hari terakhir), dan kalau ikut disimpan, chart selalu terbuka di rentang itu. Tampilan awal karena itu diulang lewat poller sampai lebar > 0.
- **Kesiapan harus diukur dari pane utama.** Pane harga (Separate pane) punya skala waktu tersembunyi, jadi `timeScale().width()`-nya selalu 0.
- **`chart.resize(w, h, true)` mengubah rentang yang tampil** kalau ukurannya beda. Jangan dipakai sebagai "paksa gambar ulang" saat mengukur — ini sempat membuat hasil pengukuran palsu di sesi ini.
- **Lebar sumbu harus disamakan antar-pane** (`minimumWidth`), kalau tidak, tanggal yang sama jatuh di posisi berbeda. Disinkronkan ulang setelah zoom/geser karena panjang label berubah.
- **Sinkron zoom Separate pane** memakai seri jangkar tak terlihat di tiap pane (jumlah bar sama) plus sinkron logical range, dengan pengaman "hanya geser kalau rentangnya beda".
- **Pola garis hanya lima:** Solid, Dotted, Dashed, LargeDashed, SparseDotted. Panjang putusnya ikut tebal garis.
- **`lineType`**: Simple / WithSteps / Curved. Tangga hanya terlihat kalau satu bar memakan beberapa piksel.
- **`priceScale().width()` bernilai 0 sampai chart benar-benar menggambar.** Perataan baris legend ke area gambar karena itu diulang tiap 150 ms selama 4 detik pertama. Di panel browser Claude yang sering membeku nilainya bisa tetap 0 sampai ada gerakan mouse — itu artefak panel, bukan bug.
- **Lebar area gambar baru mengendap 1–2 detik sesudah chart tampil**, karena lebar sumbu harga menyesuaikan panjang label ("300000.00" vs "1.50") dan kedua pane disamakan. Chart mempertahankan **lebar bar**, bukan rentangnya, jadi area yang menyusut menggeser tepi kiri. Inilah sebab zoom mengecil sedikit demi sedikit tiap kali berganti Overlay ↔ Separate pane (2931 → 3104 → 3268 → 3422 dalam tiga kali ganti). Memeriksa sekali sesudah memasang zoom **tidak cukup** — geserannya datang belakangan, saat pemeriksaan sudah selesai.
- **Sumbu berentang tetap lewat `autoscaleInfoProvider` tetap memakai ruang tepi bawaan** (atas 20 %, bawah 10 %), jadi sumbu 0–100 menulis 120 · 110 · −10. Obatnya `scaleMargins` kecil + formatter yang mengosongkan angka di luar rentang (14 Sep).
- **Seri tambahan yang dibuat di browser (kembaran Loss) harus ikut semua mekanisme yang memakai daftar seri**: kunci geser-sumbu (`seriesOn`) — kalau tidak, rentang 0–100 kembaran bergabung dengan rentang yang dikunci dan sumbu tidak bisa digeser; reset sumbu (`resetScales`); pola garis tangga adaptif (`garisTangga`). Seri yang tidak terlihat (`visible: false`) tidak ikut autoscale.
- **Format angka sumbu diambil dari seri pertama di sumbu itu.** Garis acuan disisipkan paling depan (`plan.insert(0, …)`), jadi precision bawaannya (2) sempat membuat sumbu SOPR menulis 1.25 dan bukan 1.250 (14 Sep). Garis acuan kini mewarisi `precision` dan `whole_from` metrik di sumbunya.
- **Tidak ada perintah mengatur rentang sumbu harga di v4.** Rentang dikunci lewat `autoscaleInfoProvider` pada semua garis di sumbu itu. v5 (5.2.1) punya `IPriceScaleApi.setVisibleRange`, tapi upgrade mengubah hampir seluruh kode chart.
- **Menarik angka sumbu = mengubah skala** (`handleScale`), bukan menggeser. Menarik area gambar hanya menggeser sumbu "utama" pane, dan hanya kalau autoscale-nya mati.
- **Fullscreen API pernah ditolak** (`TypeError: Permissions check failed`) — lihat bagian 7.
- **ChartInspect tidak punya OHLC:** menu chart mereka menulis "No OHLC data for this asset"; endpoint harian cuma `btc_price`; endpoint intraday `https://chartinspect.com/api/charts/crypto/intraday-price?cryptocurrency=bitcoin&resolution=10&from=<unix>&to=<unix>` mengembalikan `{t, p}` dengan `tierLimited: true` dan `freeIntradayWindowDays: 30`. Untuk bitcoin hanya resolusi 10 menit yang tersedia.

### Alat kerja
- **TEMPLATE di `lw_chart.py` adalah string Python biasa (bukan raw).** Backslash apa pun di JavaScript-nya — termasuk di komentar — dibaca Python sebagai escape sequence (`"\d"` → SyntaxWarning, gagal kalau warning dijadikan error). Tulis regex tanpa backslash (`[(]([0-9]+)[)]`). Cek dengan `python -W error::SyntaxWarning`.
- **Garis silang chart tidak bisa dipicu dari JavaScript saat panel beku** (13 Sep). `dispatchEvent(MouseEvent)` ke canvas dan `chart.setCrosshairPosition()` sama-sama tidak memunculkan tooltip. Yang berhasil: `computer hover` (gerakan mouse sungguhan dari panel), lalu baca isi `#tip` lewat JavaScript. Screenshot sering timeout; ulangi sekali, biasanya berhasil.
- **ResizeObserver di dalam chart tidak berbunyi saat panel membekukan frame** (13 Sep). Tinggi baris legend sudah 81 px tapi pane tidak dikurangi, karena pengamatnya menunggu frame digambar. Jadi penghitungan tinggi juga dipanggil dari `rapikanBar`, yang ikut timer 150 ms di 4 detik pertama. Di browser biasa ResizeObserver bekerja; cadangan ini untuk keadaan frame tidak digambar.
- **Lebar sumbu terbaca 0 membuat pengukuran lebar legend tidak sah** (13 Sep). Sebelum chart tergambar, `priceScale().width()` = 0 sehingga `rapikanBar` memberi jarak 10/10 px; legend terukur 995 px dan "muat satu baris" di 1920. Dengan sumbu sungguhan (kiri 48, kanan 72) legend hanya 895 px dan butuh dua baris. Sebelum menyimpulkan apa pun soal lebar legend, pastikan lebar sumbu sudah bukan 0 (bangunkan frame dengan screenshot).
- **Menguji di panel browser Claude tidak selalu bisa dipercaya.** Pembacaan lewat API chart kadang tidak mencerminkan yang tergambar (lebar panel berubah, frame dibekukan, perintah zoom programatik jadi no-op). Yang terbukti andal: **screenshot** + **gulungan mouse sungguhan** (`WheelEvent`) + membaca `localStorage`.
  - Frame chart membeku kalau panel lama tidak menerima input sungguhan; `setVisibleLogicalRange` jadi no-op **diam-diam**. Satu gulungan mouse sungguhan membangunkannya, sesudah itu perintah programatik bekerja lagi. Klik JavaScript ke widget Streamlit (`el.click()`) tetap bekerja walau frame chart beku — itu cara paling andal untuk menjalankan uji berulang.
  - **Saat frame beku, `setVisibleLogicalRange` tidak hilang tapi antre** (koreksi 14 Sep atas catatan "no-op" di atas): perintahnya diterapkan begitu frame berikutnya digambar, sedangkan `getVisibleLogicalRange` terus membaca nilai lama sampai saat itu. Akibatnya uji berantai dalam satu skrip (langkah 2 membaca hasil langkah 1) menghasilkan angka palsu — hanya perintah terakhir yang menang. Pola yang berhasil: satu langkah per skrip → screenshot (membangunkan frame) → baca hasil di skrip berikutnya.
  - **Screenshot di viewport emulasi (mis. 1440×1000) kadang tampil diperkecil penuh, kadang terpotong 1:1 di pojok kiri atas**, dengan bingkai koordinat 800×556 yang sama. Klik berdasarkan koordinat bisa jatuh di tempat yang salah (14 Sep: klik yang dimaksud untuk slider mengenai chart). Untuk uji interaksi pakai `PointerEvent` sintetis ke elemen lewat JavaScript, dengan posisi dari `getBoundingClientRect`.
  - **Panel browser Claude memblokir Fullscreen API sepenuhnya.** Apa pun yang menyangkut layar penuh sungguhan harus diuji user di browsernya sendiri.
  - **Panel browser Claude tidak bisa membuka berkas lokal (`file://`).** Untuk pratinjau pakai widget inline (`show_widget`) dengan data yang disampel ringkas, misalnya mingguan, bukan berkas HTML.
  - **Mengukur apakah tulisan benar-benar di tengah:** kotak baris (`Range.getBoundingClientRect()`) bisa terlihat rata padahal tintanya tidak — huruf berekor seperti "y" menarik tinta ke bawah. Ukur tinta lewat `canvas.measureText()` (`actualBoundingBoxAscent/Descent`) dan hitung posisi garis dasar dari `line-height`.
  - Pola uji yang terbukti berguna: pasang pengambil cuplikan di halaman induk (`setInterval` 25–40 ms) yang mencatat rentang tiap chart + isi `localStorage`, lalu jalankan pergantian mode lewat klik JavaScript. Itu yang memunculkan urutan "zoom terpasang di 1,1 detik → lebar menyusut di 2,1 detik → nilai geser tersimpan di 2,4 detik".
- Screenshot kadang timeout kalau jendela aplikasi tertutup jendela lain.
- **Emulasi HP di panel Claude** (`resize_window` preset mobile) mengaktifkan `pointer: coarse` dan user agent Android, jadi tombol khusus sentuh bisa dicek keberadaannya. Gerakan jari sungguhan tidak bisa ditiru (klik panel = mouse); perilaku sentuh harus diuji user di HP. Screenshot di mode ini kadang tampil berulang empat petak — artefak panel, isinya tetap bisa dibaca.
- **Format angka sumbu dan label nilai terakhir diambil dari seri PERTAMA di skala itu — walau seri itu mati** (dicek di kode 4.2.3: `_formatterSource()` = `dataSources[0]`). Saat seri bersatuan/berpasangan pindah skala, seri mati di skala tujuan harus "diparkir" ke skala lain (`priceScaleId: 'parkir_<kolom>'`); kalau tidak, angka sumbu USD tertulis "2,000,000,000". Garis acuan yang diparkir disembunyikan.
- **Memindah seri antar-sumbu cukup `series.applyOptions({priceScaleId})`** (library memanggil `moveSeriesToScale`). Warna angka per sumbu: `priceScale(side).applyOptions({textColor})`.
- **Warna per titik:** data `{time, value, color}` berlaku untuk histogram dan garis. Warna titik mengalahkan warna seri, jadi saat Highlight meredupkan seri, data harus di-`setData` ulang dengan warna redup.
- **`git commit -m @'…'@` di PowerShell 5.1 rusak kalau pesannya berisi tanda kutip ganda** (argumen terpecah, muncul `pathspec … did not match`). Tulis pesan ke file lalu `git commit -F <file>`.
- **Patch file lewat skrip Python:** file repo memakai CRLF — baca dengan `newline=''`, olah dengan `\n`, kembalikan ke CRLF, tulis dengan `newline=''`. Heredoc Bash panjang yang berisi banyak tanda kutip bisa gagal di-parse; tulis skripnya ke file dulu.
- **Pratinjau `show_widget` dengan data tertanam:** pastikan JSON benar-benar ditempel, bukan placeholder (16 Sep dua kali terkirim widget rusak).
- **Menguji layar penuh semu tanpa iPhone:** di halaman induk jalankan `Object.defineProperty(document, 'fullscreenEnabled', {configurable: true, get: () => false})`, klik Full di chart, ukur, lalu Exit dan `delete document.fullscreenEnabled`.
- **Kalau chart terbuka di zoom aneh, atau sorot/legend tersisa dari percobaan lama**, kosongkan penyimpanannya: `localStorage.removeItem('dash_v2_market_valuation')` lalu muat ulang halaman. Key-nya `dash_v2_<family.key>`, berisi `highlights`, `hidden`, `bars`, dan `sig`.
- **Heredoc di Bash merusak backslash dan kutip** pada skrip Python yang panjang (pola `\n`, backtick JS). Untuk patch yang rumit, tulis skrip ke file dulu lalu jalankan.
- **Windows MAX_PATH:** membuat venv di path temp yang panjang membuat `pip install streamlit` gagal di tengah jalan. Pakai path pendek.
- **GitHub Actions tidak membaca `requirements.txt`** (workflow memasang `requests pandas numpy` sendiri), jadi mengunci versi Streamlit tidak mengganggu update data harian.
- **Sebelum push, merge dulu dari GitHub.** GitHub Actions meng-commit CSV dan `alerts/logs` setiap hari, jadi repo lokal hampir selalu tertinggal. Cek dulu `git diff --name-only HEAD...origin/main`: kalau isinya hanya `data_*.csv` dan `alerts/logs/`, merge aman walau ada perubahan user yang belum di-commit. Kalau menyentuh file yang sedang diubah user, berhenti dan tanya.
- **Git:** repo punya banyak perubahan lain yang belum di-commit dari pekerjaan user sebelumnya (`CLAUDE.md`, `auto_update.py`, `references/`, puluhan file di `research/`). **Jangan commit semuanya sekaligus** — hanya file dashboard yang relevan, dan hanya kalau user minta.

---

## 11. Cara menjalankan

Dashboard v2 (versi live). Tema teal gelap dibaca otomatis dari `.streamlit/config.toml`:

```bash
streamlit run app.py
```

Dashboard v1 (arsip):

```bash
streamlit run archive/app_v1.py --server.port 8501
```

Konfigurasi di `.claude/launch.json`: `dashboard-lama` (8501, `archive/app_v1.py`), `dashboard-v2` (8502, `app.py`), `dashboard-v2-uji` (8503, `app.py`, dipakai sesi Claude Code supaya tidak bentrok dengan server milik user). Kedua konfigurasi v2 masih memberi opsi `--theme.*`; itu tidak bentrok dengan `config.toml` (nilainya sama). Ingat: opsi `--theme.*` apa pun wajib disertai `--theme.base dark`.

---

## 12. Langkah pertama yang disarankan untuk sesi baru

1. Baca `CLAUDE.md` dan dokumen ini.
2. Jalankan `dashboard-v2-uji`, buka halaman Market Valuation, dan lihat sendiri keadaannya sebelum mengubah apa pun.
3. **Tanyakan apakah Streamlit Cloud perlu Reboot app sesudah push 17 Sep dan apakah halaman Cohort State (bagian 3.27) sudah boleh dilanjutkan**, lalu **tanyakan halaman berikutnya** (RHODL Waves dan bagian 3.24 sudah live; tanyakan apakah Streamlit Cloud perlu Reboot app; CDD/VDD ditunda, bagian 3.25) — sudah ada sepuluh halaman (MVRV, Price Levels, AVIV, SOPR, NUPL, Supply in Profit, HODL Waves, RHODL Ratio, Funding Rates & Open Interest, Fear & Greed); Realized P/L ditunda (bagian 3.18); sisa usulan di bagian 3.11, hasil cek data semua kandidat di bagian 3.23 (jangan diulang). Halaman baru = satu `MetricFamily` dengan `group` dan `url_path`. Pakai gaya judul B2, aturan teal (bagian 4–5), `precision`/`whole_from` per seri, uji palet bagian 9, dan **cek kualitas data dulu** (nilai macet, lonjakan, satuan, cakupan) seperti bagian 3.18–3.19. Aturan sumbu dari user: metrik berskala sama ke kanan saat Separate pane. Pending yang bisa ditanyakan: ingatan kontrol setelah reload (pilihan b, bagian 3.24), rumus gap `alert_check.py` (bagian 3.9). Kerjakan di localhost dulu; push hanya setelah user menyatakan valid.
4. Untuk urusan tampilan apa pun, buat widget pratinjau dengan data asli lebih dulu, lalu tunggu pilihan user. Untuk warna garis baru, jalankan uji palet di bagian 9 sebelum menunjukkan pratinjau.
5. Sesudah mengubah apa pun di `dashboard/`, **restart server** — modul yang sudah dimuat tidak dibaca ulang.
6. Kalau ada keluhan tampilan yang terdengar kecil ("kurang rata", "kebesaran"), **ukur dulu di halaman hidup** lewat `getBoundingClientRect` dan `getComputedStyle`, jangan menebak dari kode. Semua perbaikan tata letak 13 Sep ketemu dengan cara itu, dan dua tebakan pertama meleset.

---

## Dipindah dari handoff ringkas (17 Sep 2026, sore)

Rincian di bawah dipindah dari `handoff.md` supaya dokumen ringkasnya tetap di bawah 35 KB. Statusnya tidak berubah.

### Cohort State (ditahan user 17 Sep 2026)

- **Cohort State (DITAHAN user 17 Sep — "ada yang perlu dipastikan dulu"):** analisa `research/analyze_cohort_state_plane.py` + `plot_cohort_state_plane.py` + `findings/_cohort_state_plane.csv` (s/d 7 Sep).
  - Demand Impulse (DI) = RC 1d–3m ÷ SMA90 − 1 → persentil 1.460 hari (min 60 %); cukup `data_hodl_waves.csv`.
  - Aged Cohort Turnover (ACT) = BTC dibelanjakan kohort 6m–2y (profit + loss BTC band 5 & 6 endpoint `realized-profit-by-age`; band_5 = 6m–12m, band_6 = 1y–2y, terverifikasi) ÷ BTC dipegang kohort ((supply 6m–12m + 1y–2y)/100 × (lth_supply_btc + sth_supply_btc)), SMA30 → persentil 4 tahun.
  - State: histeresis per sumbu (≥ 60 tinggi, ≤ 40 rendah, pindah setelah 10 hari), empat kombinasi DORMANSI/SEPI · DISTRIBUSI/LEPAS TANPA BID · TRANSFER/TANGAN BERGANTI · AKUMULASI/MODAL MASUK PASOKAN TERKUNCI. 60 episode sejak Mar 2013, median 76 hari.
  - **Penghalang:** data ACT tidak ada di CSV repo (analisa lama membaca `rpba.pkl` di scratchpad sesi lain, s/d 9 Sep). Butuh pipeline baru di `auto_update.py` yang menyimpan `data_profit_by_age.csv` (profit/loss BTC 12 band) — **izin user ditahan**. Workflow sudah `git add .`.
  - Jawaban user: bentuk state (pita tipis B vs latar pane A) ditahan; persentil disembunyikan dulu; nama state Inggris (Quiet · Selling, no bid · Changing hands · Inflow, supply locked) keep dulu; letak: digabung ke halaman **RHODL Ratio**. Warna pratinjau: Quiet `#6e7681`, Selling `#bf5546`, Changing `#a8963f` (bukan mustard — dekat oranye BTC bagi buta warna), Inflow `#3f6fd8`, DI `#5b8def`, ACT `#e0705c`.
  - Catatan tafsir: state terlambat ≥ 10 hari; persentil bergeser kalau data direvisi. Bukan bagian framework v2.

### CDD/VDD (ditunda)

- **CDD/VDD (ditunda user, belum butuh):** `vdd_multiple` CSV = VDD harian ÷ MA365 (berisik; p99 12,3, maks 59,9). Rumus Glassnode `vdd_30d_ma / vdd_365d_ma` halus (p99 6,5; puncak 2013 8,4 · 2017 5,2 · 2021 4,5 · 2024 4,4). Usulan waktu itu: rumus 30d/365d, ref 1,0, CDD batang navy, VDD violet, harga dari `data_mvrv.csv`. Research menolak "VDD multiple < 1" sebagai filter.

### Catatan kualitas data yang sudah pindah ke baris halaman (bagian 3 handoff)

- **Realized Cap:** bersih (LTH + STH = total ≤ 0,01 %); loncatan LTH +7,2 % 26 Apr 2026 wajar (koin 22 Nov 2025 genap 155 hari). Isinya ≈ RP × supply, mirip Price Levels.
- **Exchange:** +43,8k BTC masuk 8 Sep 2026, saldo tetap di level baru (3,36M → 3,40M) — transaksi besar atau dompet bursa baru di sumber. Net = in − out persis. 8 hari 2026 inflow = outflow = 0 (8 Apr, 18–19 Apr, 7 & 10 Mei, 12 & 28 Jul, 5 Agt). `btc_price` file ini beda sumber di 2026 (maks 16 %). Lompatan −100k BTC 28 Jul 2021.
- **LTH/STH Supply:** LTH + STH = 20,09 juta BTC (17 Sep 2026). Lompatan pindah dompet: −280k 4 Des 2018 → +289k 8 Mei 2019; −536k 22 Nov 2025 → +598k 26 Apr 2026 (batang 30d −1,03 juta Nov 2025, +1,13 juta Apr 2026). Revisi riwayat < 0,1 %.
- **Price/CVDD:** di bawah 1,0 hanya 14 Jan 2015 & 21 Nov 2022 (KB Glassnode: 9 & 21 Nov 2022 — beda karena ChartInspect tidak entity-adjusted). CVDD = 0 sampai 16 Jul 2010, jadi rasionya kosong.
- **Realized Cap 30d change:** 2011–2013 sampai +413 %.
