# Handoff — Upgrade Dashboard Streamlit (v2)

Ditulis ulang: 13 September 2026 (pembaruan kedua). Untuk dilanjutkan di sesi Claude Code berikutnya.
(Versi sebelumnya ditulis 11 dan 12 September 2026; isinya sudah dilebur ke sini.)

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
- **Pendekatan yang dipilih:** satu renderer dipakai semua halaman, konfigurasi metrik terpisah. Coba satu halaman dulu. Dashboard lama (`app.py`) tidak boleh terganggu.
- **Posisi sekarang:** prioritas 1, 2, dan 4 sudah matang untuk **satu halaman** (Market Valuation). Prioritas 3 (navigasi seluruh halaman) belum disentuh sama sekali.

---

## 2. Cara kerja yang disukai user

- Chat pakai **bahasa Indonesia yang simpel**, singkat tapi jelas. Istilah teknis (MVRV, SOPR, dll.) tetap English. **Teks di dashboard pakai bahasa Inggris.**
- User **tidak bisa menilai dari kode atau kode hex warna**. Untuk urusan tampilan/warna, **langsung buat widget pratinjau inline** (`show_widget`) memakai data CSV asli — bukan file HTML terpisah. Localhost dipakai untuk mengecek dashboard sungguhan.
- User sering bilang **"jangan eksekusi dulu"**. Jelaskan pemahaman, tunggu konfirmasi, baru kerjakan. Kalau user mengirim foto, itu cara tercepat menyamakan maksud.
- Kalau ada pilihan, beri **rekomendasi beserta untung-rugi**, bukan sekadar daftar opsi.
- **Klaim harus dibuktikan.** Kalau pengukuran meragukan, bilang belum sah dan ulangi dengan cara lain. User beberapa kali menerima koreksi semacam ini dan menghargainya.
- Kalau diminta mengecilkan/optimasi sesuatu, **pertimbangkan efeknya ke elemen lain** (lebar, tinggi, jarak, rasio huruf), bukan satu sisi saja.

---

## 3. Keputusan PENDING — tanyakan dulu ke user

### 3.1 Halaman metrik berikutnya — sudah diputuskan 13 Sep 2026
**Price Levels** (`data_price_level.csv`) duluan: isinya batas zona framework v2 (STH RP, RP, LTH RP, CVDD, 200DMA) dan bentuknya mirip MVRV, jadi renderer sekarang bisa dipakai hampir apa adanya. **Pengelompokan navigasi 17 halaman masih belum dibahas** — tanyakan saat halaman kedua selesai.

### 3.2 Slider rentang di bawah chart — ditunda (dikonfirmasi lagi 13 Sep 2026)
Gaya navigator TradingView: chart mini berisi seluruh sejarah, dengan kotak geser yang bisa ditarik dan diubah lebarnya, tersinkron dua arah dengan chart utama. Tidak ada bawaannya di lightweight-charts 4.2.3, jadi harus digambar sendiri di dalam chart. Karena hidup di dalam chart, tidak memicu reload Streamlit. Pekerjaan sedang-berat. Alasan ditunda: 16 halaman lain belum ada.

### 3.3 Memindahkan kontrol Line style ke dalam chart — masih terbuka
Tujuannya supaya mengubah gaya garis tidak memuat ulang chart. User sempat memilih "kerjakan", lalu sepakat menunggu: keluhan aslinya adalah zoom hilang saat reload, dan itu sudah diperbaiki 13 Sep. Setelah dipakai beberapa hari, tanyakan lagi apakah masih terasa perlu. Penjelasan lengkap ada di bagian 7.

### 3.4 Bentuk MVRV Z-Score — sudah diputuskan dan dikerjakan 13 Sep 2026
Z-Score tinggal di **pane ketiga paling bawah** pada halaman Market Valuation, dinyalakan lewat kotak **Z-Score** (Hidden / Bottom pane). Rinciannya di bagian 4. Sempat dicoba digabung ke chart MVRV sebagai histogram — ditolak user karena terlalu padat dan skala Log mengacaukan semuanya. Ide halaman terpisah dan tombol pengalih chart tidak dipakai.

### 3.6 Desain judul halaman — ditahan sampai Z-Score beres, sekarang boleh ditanyakan
User menilai subjudul "MVRV Oscillators" di bawah lencana "Market Valuation" kurang tegas sebagai tanda halaman MVRV. Tiga usulan sudah dipratinjau lewat widget inline:
- **A** — nama halaman jadi tipografi dengan garis aksen tipis.
- **B** — kategori jadi tulisan kecil di atas, nama metrik naik jadi judul besar.
- **C** (rekomendasi Claude) — bentuk jejak "Market Valuation / **MVRV Oscillators**".

Catatan: pratinjau itu dibuat saat ide "tab pengalih chart" masih hidup. Karena Z-Score akhirnya jadi pane ketiga, bagian tab di pratinjau tidak berlaku lagi — **buat pratinjau ulang tanpa tab** sebelum user memilih.

### 3.5 Kotak L / R untuk pilihan sumbu — ditahan
Ide user: tombol Left/Right diganti dua kotak kecil "L" dan "R" bergaya kotak angka periode di legend. Hasil ukur: **tidak menghemat lebar sama sekali** (lebar popover ditentukan baris CHART HEIGHT, bukan baris axis), hanya menghemat tinggi ±14 px per baris. Ditahan sampai ada halaman dengan garis banyak — bukan khusus HODL Waves, metrik lain juga bisa. Kalau dipakai, pakai untuk semua halaman sekaligus.

---

## 4. Yang sudah selesai

### File dan struktur
| File | Isi |
|---|---|
| `app_v2.py` | Entry point v2, sidebar, seluruh CSS global (termasuk aturan `:fullscreen`). Port 8502. |
| `dashboard/registry.py` | Konfigurasi keluarga metrik (`MetricFamily`, `Series`, `RefLine`). Menambah halaman = menambah satu `MetricFamily`. |
| `dashboard/metric_page.py` | Tata letak halaman: header, kontrol, gaya garis smoothing, rencana garis. |
| `dashboard/charts.py` | Memilih mesin chart (Lightweight / Plotly). Dataclass `Line`. |
| `dashboard/lw_chart.py` | Chart lightweight-charts yang digambar langsung di browser via `st.iframe`. Pane dibangun dari daftar (harga / metrik / tambahan), legend, sorot, geser sumbu, zoom tersimpan, tangga adaptif, tombol layar penuh. |
| `dashboard/data.py` | Loader CSV, SMA/EMA, filter tanggal, Z-Score rolling 1Y/2Y/4Y. |

Hanya **Market Valuation** yang sudah dibuat (`data_mvrv.csv`: MVRV, STH MVRV, LTH MVRV + garis acuan Neutral 1,0, plus MVRV Z-Score dan Rolling Z-Score di pane tambahan).

### Kontrol di halaman (8 kotak, semuanya bergaya sama)
- **Range** — preset **1m / 3m / 6m / 1y / 4y / All** (huruf kecil sejak 13 Sep supaya seragam dengan "7d" dan "1y"; nilai di baliknya tetap "1M" dst.) plus tanggal From/To yang disejajarkan satu baris. Default **All**.
- **Smoothing** — tab SMA/EMA, kisi 3×3 (Off, 7d, 14d, 30d, 60d, 90d, 200d, 365d, 730d), input periode sendiri + tombol Add. Multi-periode.
- **Scale** — Auto/Linear/Log terpisah untuk metrik (kiri) dan BTC (kanan).
- **BTC price** — Overlay (default) / Separate pane / Hidden.
- **Z-Score** — Hidden (default) / Bottom pane. Kotak ini hanya muncul untuk keluarga metrik yang punya seri `pane="extra"`. Saat Hidden, seri Z-Score **tidak dikirim sama sekali** (bukan sekadar disembunyikan), supaya sumbu pane metrik tidak ikut menghitungnya.
- **Display** — tinggi chart 600/720/860/1000 px + sumbu kiri/kanan per garis, **termasuk BTC Price** (ditambah 13 Sep). Tiap baris: nama di kiri, tombol Left/Right di kanan. Kotak BTC Price mati sendiri saat mode harga bukan Overlay ("Only for BTC price = Overlay"), karena di Separate pane harga punya pane sendiri. Nilai di kotak Display menulis Left / Right / Mixed dan **sengaja tidak menghitung BTC** — kalau ikut dihitung, keadaan bawaan (metrik kiri, harga kanan) selalu menulis "Mixed" dan jadi tidak berarti apa-apa.
- **Chart** — Lightweight (default) / Plotly.
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
- Warna garis: MVRV navy `#0070a6`, STH rust `#bf5546`, LTH teal `#0b8e89`, BTC oranye `#F7931A`. Semua garis utama 1,5 px.
- Aksen kontrol: **teal gelap `#006d77`** dengan latar 40% + garis tepi + teks putih. Sidebar dan menu tetap ungu `#a855f7`.
- Judul halaman: teks putih di atas **latar teal gelap**, plus tulisan kecil "Latest data: <tanggal>".
- Popover ringkas: jarak tepi 12–14 px, judul kecil 11 px, tombol 12 px / tinggi minimal 26 px.
- Kotak tanggal tanpa latar abu, isinya rata tengah, kalender bawaan browser diwarnai lewat `accent-color`.
- Baris KPI **sudah dibuang**.
- **Ukuran kontrol dirapatkan (13 Sep).** Tombol aksen 45×32 → 33×26 px, kotak tanggal 40 → 28 px. Streamlit memaku tinggi tombol di 32 px, jadi `height` harus ditimpa langsung — `min-height` dan padding tidak mempan. Hasil: popover Display 240×372 → 234×254, Range 253×158 → 253×140, Smoothing 186×204.
- **Judul kecil di semua popover seragam** (11 px, huruf besar, renggang): PRESET, FROM, TO, SMOOTHING, nama metrik, BTC PRICE, CHART HEIGHT, AXIS. Label bawaan widget dimatikan (`label_visibility="collapsed"`).
- **Perataan kiri:** huruf pertama judul halaman, subjudul, baris tombol, dan tepi kiri chart semuanya di satu garis. Kotak lencana teal lurus dengan kotak tombol; subjudul digeser 10 px sebesar jarak dalam lencana.
- **Tulisan di dalam tombol rata tengah.** Streamlit memasang teks `st.button` sebagai baris *inline* di kotak baris yang lebih tinggi daripada hurufnya, jadi huruf duduk di garis dasar (2,3 px di bawah tengah) sementara semua segmented control duduk 0,5 px di atas tengah. Dinormalkan lewat CSS (`display:block` + `line-height`). Seluruh kontrol sudah diukur ulang dan rata; dua yang sengaja tidak ditengahkan: menu sidebar (label rata kiri) dan nama metrik di legend (didahului contoh garis berwarna).

### Perilaku
- **Legend dikelompokkan per metrik**: satu label untuk garis utama, lalu angka periode smoothing sebagai titik kecil yang bisa diklik sendiri-sendiri. Empat kelompok muat satu baris tanpa geser samping; kalau kepanjangan, membungkus ke baris berikutnya.
- **Kelompok legend tanpa garis utama** (dipakai Rolling Z-Score): kalau tidak ada seri yang namanya persis nama kelompok, nama kelompok jadi keterangan (bukan tombol) dan semua anggotanya jadi kotak angka: "Rolling Z-Score **1y · 2y · 4y**". Angka di kotak dinaikkan 1 px (tinta "1y" sempat meleset 1,5 px ke bawah karena ekor huruf y; sekarang 0,5 px).
- **Seri boleh lahir dalam keadaan mati** (`hidden_default=True`, dipakai 2y dan 4y). Chart menyimpan daftar `seen` di `localStorage`; nilai bawaan hanya diterapkan pada seri yang belum pernah muncul, jadi pilihan user tidak ditimpa di kunjungan berikutnya.
- **Tombol sorot memakai nama pendek** dari registry (`short`) kalau ada: None · MVRV · STH · LTH · BTC · **Z** · **Z roll**. Tanpa `short`, bawaannya kata pertama label — dan tiga seri berawalan "MVRV" jadi kembar.
- **Mode sorot bisa lebih dari satu garis.** Klik lagi untuk mematikan, None mengosongkan. Garis yang tidak disorot diredupkan pada kontras 1,70:1 (MVRV 0,49 · STH 0,44 · LTH 0,39 · BTC 0,28).
- **Menarik chart atas-bawah menggeser sumbu milik garis yang disorot** (bisa dua sumbu sekaligus, jarak sama). Tanpa sorotan, perilaku bawaan library. Klik dua kali mengembalikan semua sumbu ke Auto. Penguncian baru terjadi kalau tarikan jelas vertikal (≥ 6 px dan lebih tegak daripada mendatar), supaya menggeser ke samping tidak mengunci sumbu.
- **Zoom dan posisi bertahan** saat Streamlit menggambar ulang chart, termasuk saat berganti Overlay ↔ Separate pane. Disimpan sebagai posisi bar (bukan tanggal) di `localStorage`, dengan sidik data supaya tombol Range tetap menang. Cara kerjanya: zoom simpanan dipasang ulang sampai rentang yang tampil benar-benar cocok, dan fase pemulihan itu tetap hidup sampai lebar sumbu harga mengendap (±2 detik) — lihat bagian 10 kenapa memeriksa sekali di awal tidak cukup. Fase berhenti begitu pengguna menyentuh chart, dan menyerah setelah 6 detik supaya zoom baru tetap bisa disimpan.
- **Tombol layar penuh ada di dalam chart**, ujung kanan baris sorot, dipisah garis tipis. Satu tombol bersimbol: "Full" masuk layar penuh, berganti jadi "Exit" saat aktif; Esc juga keluar dan tombolnya ikut menyesuaikan (`fullscreenchange`). Klik di dalam chart sudah merupakan gestur pengguna, jadi `requestFullscreen()` dipanggil langsung — tidak ada status di Python, tidak ada skrip penyisip. User sudah mengujinya di browser sendiri dan menyatakannya sesuai.
- **Saat layar penuh, chart mengisi sisa tinggi jendela.** Tinggi iframe dan wadahnya ditimpa sementara, pane dibagi ulang menurut perbandingan tinggi awalnya, lalu dikembalikan persis saat keluar. Ikut menyesuaikan kalau ukuran jendela berubah.
- **Baris legend dan tombol diluruskan ke area gambar**, bukan ke tepi iframe: jarak kiri = lebar sumbu kiri, jarak kanan = lebar sumbu kanan, **minimal 10 px** (tanpa minimal itu, saat semua metrik di sumbu kiri, tombol Full menempel ke batas chart — ditemukan user).
- **Garis tangga adaptif**: di bawah 6 piksel per hari polanya berubah jadi putus panjang, di atas itu kembali jadi tangga penuh. Data tidak diubah.
- **LTH otomatis pindah ke sumbu kanan** saat BTC dipisah ke pane sendiri, dan kembali ke kiri saat Overlay.
- Legend on/off dan mode sorot bekerja di browser tanpa reload, tersimpan di `localStorage` key `dash_v2_<family.key>`.
- Klik di dalam chart dan tombol Escape menutup popover yang terbuka.
- **Pane dibangun dari daftar**, bukan dipaku dua: `price` (harga BTC bila dipisah) → `main` (metrik) → `extra` (Z-Score). Zoom, geser, dan lebar sumbu semua pane tersinkron; sumbu waktu hanya di pane paling bawah. Pembagian tinggi: tiga pane 30/45/25 %, harga+metrik 45/55 %, metrik+Z-Score 70/30 %. Pane `extra` **selalu linear** — Z-Score melewati nol, jadi Log tidak berlaku; hasilnya Log di pane metrik aman lagi dipakai.
- **MVRV Z-Score**: histogram violet `#7f77dd`, transparan 55 %. **Rolling Z-Score 1y/2y/4y**: histogram hijau `#97c459`, transparan 55 %, dihitung di `data.py` dari MVRV Ratio terhadap rata-rata dan simpangan 365/730/1460 hari (data 2y mulai 2013, 4y mulai 2014). Keduanya **tanpa smoothing** (`smoothing=False`). Warna dipilih lewat jarak Lab terhadap empat warna garis yang ada, termasuk simulasi buta warna (violet 39/18, hijau 58/16; kandidat mustard dibuang karena jaraknya cuma 2 dari oranye BTC saat buta warna).

### Teknis
- Streamlit di laptop user: **1.63.0**, dikunci `streamlit==1.63.0` di `requirements.txt`.
- Dashboard v2 **wajib dijalankan dengan tema teal gelap** (lihat bagian 11). Tanpa itu, warna aksen kembali merah dan latar popover jadi putih.
- `app.py` lama diuji di 1.63.0: 12 halaman tanpa error. Diubah sekali atas permintaan user (wrapper `renderLightweightCharts` + `minBarSpacing`).
- `components.html` sudah diganti `st.iframe` (dengan fallback).
- **Field baru `Series` di registry** (13 Sep): `kind` ("line"/"histogram"), `smoothing`, `short`, `alpha`, `group`, `hidden_default`, `pane` ("main"/"extra"). `Line` di `charts.py` ikut membawa `kind`, `short`, `hidden_default`. `lw_chart.render()` sekarang menerima `extra_lines`.

---

## 5. Keputusan final — jangan dibahas ulang

- **Timeframe (Daily/Weekly/…) dihapus.** Resampling `.last()` membuang data dan menggeser tanggal cross sampai 6 hari — berisiko untuk K3/K4. Pakai SMA/EMA.
- **Default Range = All.** Ide "muat semua tapi tampil 1 tahun" dan menyalin bundle komponen chart dibatalkan.
- **OHLC di-skip.** ChartInspect memang tidak punya OHLC (bagian 10).
- **Baris KPI dibuang**, diganti tulisan "Latest data".
- **Palet garis final:** MVRV navy, STH rust, LTH teal `#0b8e89` (bukan aqua terang). Ketiganya dipilih supaya setara terang; syarat warna sengaja dilonggarkan (user menarik permintaan "MVRV harus paling menonjol").
- **Aksen kontrol teal gelap `#006d77`**, gaya latar 40%. Sidebar dan judul sidebar tetap ungu.
- **Judul halaman berlatar teal**, bukan teks teal (teks teal gelap di latar gelap kontrasnya hanya 3,1).
- **Gaya smoothing:** titik-titik → tangga → pita, seperti tabel di bagian 4. Gaya menempel pada periodenya.
- **Simbol/marker untuk membedakan garis smoothing ditolak user** (terlalu ramai).
- **Legend berkelompok per metrik** (bukan satu label per garis).
- **Tebal garis 1,5 px** untuk semua garis utama termasuk BTC.
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

---

## 6. Usulan yang disetujui user tapi belum diterapkan

- Latar brand `#0D1117` untuk halaman (sekarang `#0e1117` bawaan Streamlit dan chart `#131722`).
- Font **JetBrains Mono** untuk angka dan sumbu; Inter untuk label (sesuai brand bible user).
- Ide user yang ditunda: **overlay dua chart bertumpuk** (chart BTC di belakang, chart metrik transparan di depan, sumbu BTC di luar) untuk menampung banyak skala sekaligus. Batasan sudah dicek: sumbu harga selalu menempel pada area gambar, jadi sumbu ketiga berangka harus digambar sendiri; `setCrosshairPosition` dan latar transparan tersedia. User menilai ini "slightly over modif" untuk kebutuhan sekarang.

---

## 7. Belum dikerjakan

- **Halaman metrik lainnya** dan **navigasi seluruh halaman** (prioritas 3).
- **Desain judul halaman** — bagian 3.6.
- **Gradasi warna histogram Z-Score** — ditunda user, bagian 5.
- **Legend padat di layar sempit.** Dengan Z-Score menyala ada enam kelompok plus harga. Di panel browser Claude (504 px) legendnya sampai terdesak habis oleh tombol sorot; di layar user belum ada keluhan. Tinggi baris legend dipaku 40 px, jadi kalau membungkus dua baris, baris kedua terpotong.
- **Range All tidak selalu memuat seluruh sejarah.** Sesudah ganti Range, chart kadang terbuka di ±70 bar terakhir, dan pernah terlihat memuat penuh lalu mundur sendiri ke bar bawaan ±1 detik kemudian. Ini jalur `fitContent` (tanpa zoom simpanan), bukan jalur pemulihan zoom yang sudah diperbaiki — **sudah begitu sebelum perbaikan 13 Sep**, dan belum diusut. Kalau dikerjakan, mulai dari perilaku yang sama: lebar area gambar berubah sesudah tampilan awal.
- **Riwayat masalah tombol layar penuh (selesai, lalu seluruh mekanismenya diganti tombol di dalam chart — disimpan sebagai catatan).** Cara kerja lama:
  1. Kotak **Screen** (Normal | Full) hanya mengubah `st.session_state[f"{k}_screen"]`. Saat "Full", `render_metric_page()` menyuntikkan CSS yang menyembunyikan sidebar, header, dan toolbar Streamlit sehingga chart memenuhi jendela.
  2. Layar penuh browser **tidak bisa dipanggil dari Python**, karena `requestFullscreen()` wajib dipanggil di dalam gestur klik. Jadi `app_v2.py` menyisipkan `_FULLSCREEN_SCRIPT` lewat `st.iframe`; skrip itu berjalan di dalam iframe, mengambil `window.parent.document`, mencari kelompok tombol yang berisi "Full" dan "Normal", lalu memasang pendengar klik fase-capture pada keduanya (`attach()` + `MutationObserver`, penanda `dataset.fsBound`).
  3. "Full" memanggil `doc.documentElement.requestFullscreen()`, "Normal" memanggil `doc.exitFullscreen()`.
  - **Sebab yang terbukti:** klik Full/Normal itu sendiri membuat Streamlit membangun ulang iframe skrip (mode Full menambah satu blok CSS, jadi urutan elemen bergeser). Konteks JavaScript lama mati bersama iframe-nya, tapi tombolnya tetap elemen DOM yang sama dan penanda `fsBound = '1'` ikut menempel — skrip baru mengira sudah terpasang lalu melewatinya. Sesudah rerun pertama tidak ada lagi pendengar yang hidup: Full (klik pertama) bekerja, Normal tidak pernah. Penanda `fsBound = 1` justru bukti pendengar mati, bukan bukti terpasang.
  - **Perbaikannya:** penanda diberi nomor unik per muatan skrip (`const ID = 'fs' + Math.random()...`), jadi konteks yang sedang hidup selalu memasang pendengarnya sendiri. Pendengar mati dari iframe lama tetap menempel tapi tidak pernah berbunyi.
  - **Catatan uji:** layar penuh sungguhan tidak bisa diuji dari panel browser Claude — panel itu memblokir Fullscreen API (`TypeError: Permissions check failed`, bahkan dari halaman utama). Yang bisa diuji dari sana cuma pemasangan ulang pendengarnya. User yang mengonfirmasi hasil akhirnya di browser sendiri.
  - **Akhir cerita:** atas usul user, tombolnya dipindah ke dalam chart. Kotak Screen, `_FULLSCREEN_SCRIPT` (58 baris), state `{k}_screen`, dan blok CSS penyembunyi kerangka dibuang semua; yang tersisa hanya aturan `:fullscreen` di `app_v2.py`.
- **Mesin Plotly ketinggalan.** Fitur baru hanya ada di Lightweight: legend berkelompok, mode sorot, geser sumbu, zoom tersimpan, tangga adaptif, pane tambahan, tombol layar penuh. Plotly hanya ikut bentuk garis, tebal, pita, dan histogram (`go.Bar`); garis pane tambahan digabung ke chart metrik.
- **Slider rentang di bawah chart** — lihat 3.2.
- **Memindahkan Line style ke dalam chart** — lihat 3.3. Sebabnya: semua kontrol hidup di Python, dan setiap klik membuat Streamlit menggambar ulang komponen chart (iframe baru). Legend dan sorot tidak memuat ulang karena sudah hidup di dalam chart. Range dan Smoothing tidak bisa dipindah kecuali rata-rata bergerak dihitung di browser.
- **Sudah commit dua kali (13 Sep), belum push, belum deploy.** Commit pertama (`d0623dd`) berisi `app_v2.py`, `dashboard/`, `.claude/launch.json`, `handoff.md`, dan `requirements.txt`; commit kedua berisi pane Z-Score, tombol layar penuh di dalam chart, dan perapian kontrol. `.claude/settings.local.json` sengaja tidak ikut (pengaturan lokal). Perubahan repo lain yang belum di-commit (CLAUDE.md, `auto_update.py`, `references/`, puluhan file `research/`) **tidak disentuh** — itu pekerjaan user sendiri. Streamlit Cloud masih menjalankan `app.py`. Deploy v2 masuk akal setelah halaman-halamannya lengkap, dan itu keputusan user. Catatan: di Streamlit Cloud, tema teal gelap harus dipasang lewat `.streamlit/config.toml` — dan file itu dipakai bersama `app.py`, jadi tampilan dashboard lama ikut berubah. Tanyakan dulu.
- **Bersih-bersih kode:**
  - CSS `button[kind="pills"]` di `app_v2.py` tidak terpakai lagi (legend pindah ke dalam chart);
  - ada tiga aturan `div[data-testid="stButton"] button p` yang saling menumpuk di `app_v2.py` (font-size, margin, line-height) — bekerja, tapi sebaiknya disatukan;
  - `default_selection` / `default_series()` di `registry.py` tidak terpakai.
- **Ide untuk nanti:** memantau LTV intraday memakai harga 10 menit dari ChartInspect (bagian 10). Harga terendah intraday lebih relevan untuk risiko likuidasi daripada harga penutupan harian.

---

## 8. Data: file CSV dan kolomnya

Semua file punya kolom `date`. Kolom `btc_price` ada di sebagian besar file.

| File | Kolom |
|---|---|
| `data_mvrv.csv` ✅ dipakai | btc_price, mvrv_ratio, sth_mvrv, lth_mvrv, mvrv_zscore |
| `data_price_level.csv` | btc_price, sth_cost_basis, lth_cost_basis, realized_price, cvdd, active_realized_price, MVRV 0σ, true_market_mean_price, 200_dma, 50_wma, 200_wma, cum_pl_price, pl_price_ratio |
| `data_aviv.csv` | btc_price, aviv_ratio, aviv_mean, aviv_upper_1sd, aviv_upper_2sd, aviv_lower_1sd, aviv_lower_2sd, price_at_aviv_mean, price_at_aviv_plus_1_sigma, price_at_aviv_plus_2_sigma, price_at_aviv_minus_1_sigma, investor_cap, active_realized_price, liveliness |
| `data_momentum.csv` | btc_price, asopr, lth_sopr, sth_sopr, net_realized_pl_usd, nupl, sth_nupl, lth_nupl |
| `data_pl.csv` | btc_price, daily_realized_profit_btc, daily_realized_loss_btc, rpl_ratio, sth_pl_ratio, lth_pl_ratio, rrp, rrl, relative_realized_pl |
| `data_supply.csv` | btc_price, lth_supply_btc, sth_supply_btc, pct_lth_in_profit, pct_sth_in_profit, pct_lth_in_loss, pct_sth_in_loss, percent_btc_in_profit, percent_btc_in_loss |
| `data_hodl_waves.csv` | btc_price, lalu `supply_<band>` dan `realized_cap_<band>` untuk **12** band: 0-1d, 1d-1w, 1w-1m, 1m-3m, 3m-6m, 6m-12m, 1y-2y, 2y-3y, 3y-5y, 5y-7y, 7y-10y, 10y+ |
| `data_realized_cap.csv` | btc_price, realized_cap_usd, lth_realized_cap_usd, sth_realized_cap_usd |
| `data_rhodl.csv` | btc_price, rhodl_ratio, realized_cap_1w, realized_cap_1_2y |
| `data_cdd.csv` | cdd, vdd_30d_ma, vdd_365d_ma, vdd_multiple (tanpa btc_price) |
| `data_exchange.csv` | btc_price, total_balance, net_flow, inflow, outflow |
| `data_derivatives.csv` | btc_price, funding_rate, total_oi |
| `data_futures_basis.csv` | btc_price, annualized_basis_3m, avg_tenor_days, n_exchanges, binance/deribit/okx/bybit_basis_annualized (file masih sangat kecil) |
| `data_sentiment.csv` | btc_price, trend_bitcoin, trend_crypto, trend_ethereum, trend_nft, wiki_bitcoin, wiki_cryptocurrency, wiki_ethereum, wiki_blockchain |
| `data_lth_flow.csv` | lth_pl_price, lth_pl_flow_btc (tanpa btc_price) |
| `data_apparent_demand.csv` | btc_price, apparent_demand |
| `data_fg.csv` | Fear & Greed |
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
2. **Syarat sengaja dilonggarkan** (permintaan user): cukup dua — tidak mirip oranye BTC, dan masih bisa dibedakan penderita buta warna dengan batas longgar. Syarat lama yang dicabut: MVRV harus paling menonjol, jarak ke warna aksen tombol, dan jarak ke hijau KPI (KPI sudah tidak ada).
3. **Pelajaran:** jangan paksa semua garis sama terang. Kalau terangnya sama, bedanya tinggal hue — dan hue justru yang hilang bagi mata buta warna. Perbedaan terang yang tipis membantu. Contoh nyata: menggelapkan aqua LTH agar setara navy membuat keduanya makin mirip (ΔE normal turun dari 17 ke 11); solusinya menggeser sedikit ke hijau (`#0b8e89`).
4. **Persentase redup saat disorot** dihitung per warna supaya semua garis redup punya kontras sama, sekarang **1,70:1** terhadap latar chart `#131722`: MVRV 0,49 · STH 0,44 · LTH 0,39 · BTC 0,28. Rumusnya: cari opasitas α sehingga warna yang dicampur ke latar chart punya kontras itu.
5. Karena user tidak bisa menilai dari kode hex, **selalu tunjukkan pratinjau widget dengan data asli** sebelum bertanya.

---

## 10. Jebakan teknis yang sudah ditemukan

### Streamlit
- **Setelah mengubah file di `dashboard/`, restart server v2.** Streamlit membaca ulang `app_v2.py` setiap render, tapi modul di `dashboard/` yang sudah dimuat tidak dibaca ulang.
- **`st.rerun()` memotong satu putaran.** Widget yang belum sempat digambar (misalnya isi popover Line style) **nilainya dibuang Streamlit**. Karena itu gaya garis disimpan di gudang terpisah `st.session_state[f"{k}_lstyles"]` (dict biasa), sedangkan widget hanya cerminan yang disemai ulang tiap render.
- **Tombol tidak boleh mengubah nilai widget di badan `if st.button(...)`** — Streamlit menolak dengan `StreamlitWidgetAlreadyInstantiatedError`. Pakai `on_click=` callback, yang berjalan sebelum halaman digambar ulang.
- **`st.rerun()` membuang nilai widget yang belum sempat digambar.** Bukan cuma isi popover yang sedang terbuka: *semua* kontrol yang letaknya sesudah titik rerun ikut hilang nilainya. Gejalanya di sini: menekan tombol periode Smoothing membuat kotak Screen balik sendiri ke "Normal" padahal browser masih layar penuh (kotak Screen digambar paling ujung). Obatnya bukan menambal satu per satu — hapus `st.rerun()`-nya, pakai `on_click=`. Sesudah itu Display, Chart, dan Line style ikut aman.
- **Iframe komponen dibangun ulang kalau urutan elemen di atasnya berubah**, walau isinya sama persis. Penanda tetap yang ditulis ke DOM halaman induk (mis. `dataset.xxx = '1'`) akan bertahan padahal konteks yang menulisnya sudah mati — pakai nomor unik per muatan, jangan nilai tetap.
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

### lightweight-charts 4.2.3
- **`minBarSpacing` kecil (0.005)** supaya `fitContent()` sanggup menampilkan ~5.900 titik harian.
- **`fitContent()` tidak bekerja selama lebar chart 0.** Hasilnya chart berhenti di lebar bar bawaan (±160 hari terakhir), dan kalau ikut disimpan, chart selalu terbuka di rentang itu. Tampilan awal karena itu diulang lewat poller sampai lebar > 0.
- **Kesiapan harus diukur dari pane utama.** Pane harga (Separate pane) punya skala waktu tersembunyi, jadi `timeScale().width()`-nya selalu 0.
- **`chart.resize(w, h, true)` mengubah rentang yang tampil** kalau ukurannya beda. Jangan dipakai sebagai "paksa gambar ulang" saat mengukur — ini sempat membuat hasil pengukuran palsu di sesi ini.
- **Lebar sumbu harus disamakan antar-pane** (`minimumWidth`), kalau tidak, tanggal yang sama jatuh di posisi berbeda. Disinkronkan ulang setelah zoom/geser karena panjang label berubah.
- **Sinkron zoom Separate pane** memakai seri jangkar tak terlihat di tiap pane (jumlah bar sama) plus sinkron logical range, dengan pengaman "hanya geser kalau rentangnya beda".
- **Pola garis hanya lima:** Solid, Dotted, Dashed, LargeDashed, SparseDotted. Panjang putusnya ikut tebal garis.
- **`lineType`**: Simple / WithSteps / Curved. Tangga hanya terlihat kalau satu bar memakan beberapa piksel.
- **`priceScale().width()` bernilai 0 sampai chart benar-benar menggambar.** Perataan baris legend ke area gambar karena itu diulang tiap 150 ms selama 4 detik pertama. Di panel browser Claude yang sering membeku nilainya bisa tetap 0 sampai ada gerakan mouse — itu artefak panel, bukan bug.
- **Lebar area gambar baru mengendap 1–2 detik sesudah chart tampil**, karena lebar sumbu harga menyesuaikan panjang label ("300000.00" vs "1.50") dan kedua pane disamakan. Chart mempertahankan **lebar bar**, bukan rentangnya, jadi area yang menyusut menggeser tepi kiri. Inilah sebab zoom mengecil sedikit demi sedikit tiap kali berganti Overlay ↔ Separate pane (2931 → 3104 → 3268 → 3422 dalam tiga kali ganti). Memeriksa sekali sesudah memasang zoom **tidak cukup** — geserannya datang belakangan, saat pemeriksaan sudah selesai.
- **Tidak ada perintah mengatur rentang sumbu harga di v4.** Rentang dikunci lewat `autoscaleInfoProvider` pada semua garis di sumbu itu. v5 (5.2.1) punya `IPriceScaleApi.setVisibleRange`, tapi upgrade mengubah hampir seluruh kode chart.
- **Menarik angka sumbu = mengubah skala** (`handleScale`), bukan menggeser. Menarik area gambar hanya menggeser sumbu "utama" pane, dan hanya kalau autoscale-nya mati.
- **Fullscreen API pernah ditolak** (`TypeError: Permissions check failed`) — lihat bagian 7.
- **ChartInspect tidak punya OHLC:** menu chart mereka menulis "No OHLC data for this asset"; endpoint harian cuma `btc_price`; endpoint intraday `https://chartinspect.com/api/charts/crypto/intraday-price?cryptocurrency=bitcoin&resolution=10&from=<unix>&to=<unix>` mengembalikan `{t, p}` dengan `tierLimited: true` dan `freeIntradayWindowDays: 30`. Untuk bitcoin hanya resolusi 10 menit yang tersedia.

### Alat kerja
- **Menguji di panel browser Claude tidak selalu bisa dipercaya.** Pembacaan lewat API chart kadang tidak mencerminkan yang tergambar (lebar panel berubah, frame dibekukan, perintah zoom programatik jadi no-op). Yang terbukti andal: **screenshot** + **gulungan mouse sungguhan** (`WheelEvent`) + membaca `localStorage`.
  - Frame chart membeku kalau panel lama tidak menerima input sungguhan; `setVisibleLogicalRange` jadi no-op **diam-diam**. Satu gulungan mouse sungguhan membangunkannya, sesudah itu perintah programatik bekerja lagi. Klik JavaScript ke widget Streamlit (`el.click()`) tetap bekerja walau frame chart beku — itu cara paling andal untuk menjalankan uji berulang.
  - **Panel browser Claude memblokir Fullscreen API sepenuhnya.** Apa pun yang menyangkut layar penuh sungguhan harus diuji user di browsernya sendiri.
  - **Panel browser Claude tidak bisa membuka berkas lokal (`file://`).** Untuk pratinjau pakai widget inline (`show_widget`) dengan data yang disampel ringkas, misalnya mingguan, bukan berkas HTML.
  - **Mengukur apakah tulisan benar-benar di tengah:** kotak baris (`Range.getBoundingClientRect()`) bisa terlihat rata padahal tintanya tidak — huruf berekor seperti "y" menarik tinta ke bawah. Ukur tinta lewat `canvas.measureText()` (`actualBoundingBoxAscent/Descent`) dan hitung posisi garis dasar dari `line-height`.
  - Pola uji yang terbukti berguna: pasang pengambil cuplikan di halaman induk (`setInterval` 25–40 ms) yang mencatat rentang tiap chart + isi `localStorage`, lalu jalankan pergantian mode lewat klik JavaScript. Itu yang memunculkan urutan "zoom terpasang di 1,1 detik → lebar menyusut di 2,1 detik → nilai geser tersimpan di 2,4 detik".
- Screenshot kadang timeout kalau jendela aplikasi tertutup jendela lain.
- **Kalau chart terbuka di zoom aneh, atau sorot/legend tersisa dari percobaan lama**, kosongkan penyimpanannya: `localStorage.removeItem('dash_v2_market_valuation')` lalu muat ulang halaman. Key-nya `dash_v2_<family.key>`, berisi `highlights`, `hidden`, `bars`, dan `sig`.
- **Heredoc di Bash merusak backslash dan kutip** pada skrip Python yang panjang (pola `\n`, backtick JS). Untuk patch yang rumit, tulis skrip ke file dulu lalu jalankan.
- **Windows MAX_PATH:** membuat venv di path temp yang panjang membuat `pip install streamlit` gagal di tengah jalan. Pakai path pendek.
- **GitHub Actions tidak membaca `requirements.txt`** (workflow memasang `requests pandas numpy` sendiri), jadi mengunci versi Streamlit tidak mengganggu update data harian.
- **Git:** repo punya banyak perubahan lain yang belum di-commit dari pekerjaan user sebelumnya (`CLAUDE.md`, `auto_update.py`, `references/`, puluhan file di `research/`). **Jangan commit semuanya sekaligus** — hanya file dashboard yang relevan, dan hanya kalau user minta.

---

## 11. Cara menjalankan

Dashboard lama:

```bash
streamlit run app.py --server.port 8501
```

Dashboard v2 (wajib dengan tema teal gelap):

```bash
streamlit run app_v2.py --server.port 8502 --theme.base dark --theme.primaryColor "#006d77"
```

Konfigurasi yang sama ada di `.claude/launch.json`: `dashboard-lama` (8501), `dashboard-v2` (8502), `dashboard-v2-uji` (8503, dipakai sesi Claude Code supaya tidak bentrok dengan server milik user).

---

## 12. Langkah pertama yang disarankan untuk sesi baru

1. Baca `CLAUDE.md` dan dokumen ini.
2. Jalankan `dashboard-v2-uji`, buka halaman Market Valuation, dan lihat sendiri keadaannya sebelum mengubah apa pun.
3. Tanyakan **desain judul halaman** (bagian 3.6) dengan pratinjau ulang tanpa tab, lalu lanjutkan ke **Price Levels** (bagian 3.1).
4. Untuk urusan tampilan apa pun, buat widget pratinjau dengan data asli lebih dulu, lalu tunggu pilihan user. Untuk warna garis baru, jalankan uji palet di bagian 9 sebelum menunjukkan pratinjau.
5. Sesudah mengubah apa pun di `dashboard/`, **restart server** — modul yang sudah dimuat tidak dibaca ulang.
6. Kalau ada keluhan tampilan yang terdengar kecil ("kurang rata", "kebesaran"), **ukur dulu di halaman hidup** lewat `getBoundingClientRect` dan `getComputedStyle`, jangan menebak dari kode. Semua perbaikan tata letak 13 Sep ketemu dengan cara itu, dan dua tebakan pertama meleset.
