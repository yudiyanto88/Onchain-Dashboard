"""Konfigurasi keluarga metrik.

Menambah halaman baru = menambah satu MetricFamily di sini.
Tidak perlu menulis kode render.
"""
from dataclasses import dataclass, field
from typing import Callable

from . import data


@dataclass
class Series:
    """Satu garis di chart."""
    label: str
    col: str
    color: str
    axis: str = "left"                # sumbu bawaan: "left" atau "right"
    dim: float = 0.3                  # opasitas saat seri lain disorot
    separate_axis: str | None = None  # sumbu saat harga BTC dipindah ke pane sendiri
    kind: str = "line"                # "line", "histogram" (batang) atau "baseline" (area dari nol)
    smoothing: bool = True            # ikut digandakan oleh kontrol Smoothing
    short: str | None = None          # nama di tombol sorot; bawaannya kata pertama label
    alpha: float = 1.0                # < 1 = tembus pandang (batang histogram, isian area)
    group: str | None = None          # kelompok legend; bawaannya label sendiri
    hidden_default: bool = False      # lahir dalam keadaan mati di legend
    pane: str = "main"                # "main", "extra" (pane tambahan paling bawah), atau
                                      # "price" (di pane harga BTC saat Separate pane, di belakang
                                      # garis harga; saat Overlay/Hidden pindah ke pane bawah)
    precision: int = 2                # desimal di sumbu, label nilai terakhir, dan tooltip
                                      # (harga 0; rasio 2; nanti funding rate bisa 5)
    whole_from: float | None = None   # angka sebesar ini ke atas ditulis tanpa desimal
                                      # (LTH-SOPR: 1.318 tapi 384, bukan 384.000)
    complement_color: str | None = None  # warna garis pasangan (Loss) saat Profit dan
                                         # Loss sama-sama menyala (MetricFamily.complement)
    negative_color: str | None = None    # histogram/baseline: warna nilai negatif
                                         # (color dipakai untuk nilai positif)
    unit: str | None = None       # satuan untuk saklar MetricFamily.unit_switch ("BTC"/"USD")
    pair: str | None = None       # kolom seri pasangan satuan pertama; seri ini pindah ke sisi
                                  # sumbu seberang saat keduanya menyala (lihat lw_chart)
    compact: bool = False         # angka ringkas K/M/B (40.81B)
    # Garis bergradasi: warna tiap titik diinterpolasi dari daftar [nilai, hex] (Fear & Greed).
    gradient: list | None = None
    smoothing_color: str | None = None   # warna garis smoothing kalau beda dari color
    smoothing_precision: int | None = None  # desimal garis smoothing kalau beda (F&G: 0 vs 1)
    # Nama kelas di tooltip ("69 · Greed"): daftar [batas atas inklusif, nama], urut naik.
    value_labels: list | None = None
    # Area bertumpuk (kind="stack", HODL Waves): urutan band dari bawah dan kolom per bobot.
    stack_index: int | None = None
    stack_cols: dict | None = None
    # Seri bersatuan yang hanya tampil pada keadaan saklar tertentu: "alone" = satuannya satu-
    # satunya yang menyala, "together" = semua satuan menyala (BTC vs Stocks & Gold: Gold
    # area saat sendirian, garis saat bersama S&P 500). Seri "together" tanpa group = kembaran
    # tanpa legend; nyala/mati dan sorotnya ikut seri legend dengan kolom yang sama.
    show_when: str | None = None
    # Opasitas isian saat semua satuan menyala (S&P 500 diredupkan supaya garis Gold terbaca).
    alpha_together: float | None = None
    # Arsiran di antara garis ini dan garis berkolom fill_with (Futures Basis vs 2Y): warna
    # fill_colors[0] saat garis ini di atas, fill_colors[1] saat di bawah, opasitas fill_alpha.
    fill_with: str | None = None
    # Patokan area kind "baseline": warna berganti di nilai ini (rasio: 1.0; bawaan 0).
    base: float = 0.0
    fill_colors: tuple[str, str] | None = None
    fill_alpha: float = 0.35


@dataclass
class RefLine:
    """Garis acuan horizontal, misalnya batas netral MVRV di 1.0."""
    value: float
    label: str
    # False: satu garis di sumbu metrik utama. True: satu garis di setiap sumbu yang
    # memuat metrik — dipakai SOPR, yang LTH-SOPR-nya punya sumbu sendiri di kanan
    # dengan batas untung/rugi di 1.0 yang letaknya berbeda dari sumbu kiri.
    all_axes: bool = False
    # Kolom seri yang diikuti sumbunya. Dipakai halaman yang satu pane-nya memuat dua skala
    # (funding di satu sumbu, OI di sumbu lain): garis nol harus di sumbu funding, bukan OI.
    follow: str | None = None


@dataclass
class MetricFamily:
    key: str
    title: str      # nama pendek di menu sidebar ("MVRV")
    subtitle: str   # judul besar halaman ("MVRV Oscillators")
    loader: Callable
    series: list[Series]
    # Kelompok menu sidebar, juga lencana teal di atas judul halaman ("Valuation").
    # Pengelompokan jenis metrik, dipilih user 14 Sep 2026.
    group: str = ""
    # Alamat halaman (localhost:8503/sopr): reload tetap di halaman yang sama.
    url_path: str = ""
    reference_lines: list[RefLine] = field(default_factory=list)
    metric_scale_default: str = "Auto"
    price_scale_default: str = "Log"
    # Nama kotak kontrol untuk pane tambahan paling bawah (seri pane="extra"),
    # misalnya "Z-Score" atau nanti "Net flow". Kotaknya hanya muncul kalau ada seri itu.
    extra_label: str = "Bottom pane"
    extra_default: bool = False   # True = pane tambahan menyala sejak awal (AVIV Deviation)
    # Skala pane tambahan: "Auto" (linear) atau "Log" untuk rasio yang selalu positif (Price/CVDD).
    extra_scale: str = "Auto"
    # Saklar bobot area bertumpuk di dalam chart, mis. ("Realized Cap", "Supply"); pilih satu.
    stack_units: tuple[str, ...] | None = None
    # Warna garis harga BTC kalau bukan oranye bawaan (HODL Waves: putih) dan opasitas redupnya
    # (dihitung supaya kontras redup 1,70:1 terhadap latar chart, seperti garis lain).
    btc_color: str | None = None
    btc_dim: float = 0.28
    # Keadaan awal kotak BTC price ("Overlay" / "Separate pane" / "Hidden").
    # Nilainya sama dengan pilihan di metric_page.
    btc_mode_default: str = "Overlay"
    # Rentang tetap sumbu metrik, mis. (0, 100) untuk persen supply. None = ikut data.
    metric_range: tuple[float, float] | None = None
    # Kolom tooltip untuk metrik yang punya pasangan 100 − nilai, mis. ("Profit", "Loss").
    complement: tuple[str, str] | None = None
    # Saklar satuan di dalam chart, mis. ("BTC", "USD"); seri bertanda Series.unit ikut saklar.
    unit_switch: tuple[str, ...] | None = None
    unit_label: str = ""          # keterangan kecil sebelum saklar ("OI")
    # Kotak Window menggantikan kotak Smoothing (BTC vs Stocks & Gold): label tombol -> jendela
    # rolling dalam hari; loader dipanggil dengan jendela terpilih. None = kotak Smoothing biasa.
    window_days: dict[str, int] | None = None
    window_default: int = 365
    smoothing_default: list[int] = field(default_factory=list)   # periode menyala sejak awal
    # Gaya bawaan per periode, mis. {30: "Band"}; periode lain ikut urutan Dotted/Step/Band.
    smoothing_style_default: dict[int, str] = field(default_factory=dict)


MARKET_VALUATION = MetricFamily(
    key="market_valuation",   # tetap: dipakai key localStorage dash_v2_market_valuation
    title="MVRV",
    subtitle="MVRV Oscillators",
    group="Valuation",
    url_path="mvrv",
    loader=data.load_mvrv,
    # Bawaan (permintaan user 15 Sep 2026): BTC Separate pane, sumbu MVRV Log. LTH MVRV bisa
    # puluhan di puncak siklus; dengan Log, MVRV dan STH di sekitar 1 tidak ikut rata, dan
    # saat Separate pane LTH pindah ke sumbu kanan (separate_axis).
    # Pane Z-Score tetap linear (lw_chart.render), jadi nilai negatifnya aman.
    btc_mode_default="Separate pane",
    metric_scale_default="Log",
    price_scale_default="Log",
    series=[
        # Navy/rust/teal dibuat setara terangnya supaya tidak ada garis yang mendominasi.
        # Teal LTH lolos uji buta warna terhadap rust, tapi cukup mirip navy saat garis
        # berdempetan; label sumbu dan tombol Highlight membantu membedakannya.
        # dim dihitung per warna supaya semua garis redup berkontras sama (1.70:1 terhadap
        # latar chart): bentuknya masih terbaca, garis yang disorot tetap menonjol.
        Series("MVRV", "MVRV", color="#0070a6", axis="left", dim=0.49),
        Series("STH MVRV", "STH MVRV", color="#bf5546", axis="left", dim=0.44),
        # LTH MVRV bisa puluhan di puncak siklus (MVRV dan STH jarang di atas 6),
        # jadi saat sumbu kanan kosong ia dipindah ke sana supaya punya skala sendiri.
        Series("LTH MVRV", "LTH MVRV", color="#0b8e89", axis="left", dim=0.39,
               separate_axis="right"),
        # Median MVRV: harga beli koin di tengah sebaran (data_median_mvrv.csv), jadi
        # puncak siklusnya di atas MVRV rata-rata dan dasarnya tetap di sekitar 1.
        # Biru langit dipilih user 18 Sep 2026 dari pratinjau; nadanya diturunkan di hari yang
        # sama karena #8fd3ff (terang 11,02:1 terhadap latar chart) mengalahkan navy MVRV.
        # #6fb6de terang 8,03:1, jarak Lab ke garis terdekat 28 normal, 28 saat
        # deuteranopia/protanopia — masih jauh di atas patokan buta warna (14).
        # Sumbu kiri bersama MVRV dan STH: skala Log bawaan menampung puncak 2011 (73,8).
        # Bukan bagian framework v2 — tidak ada garis ambang.
        Series("Median MVRV", "Median MVRV", color="#6fb6de", axis="left", dim=0.27,
               short="Median"),
        # Z-Score digambar sebagai area dari garis nol, bukan garis: bentuknya
        # langsung membedakannya dari tiga rasio di atas. Tidak ikut smoothing —
        # yang rolling sudah merupakan penghalusan, dan yang full-history bergerak
        # seiring MVRV Ratio yang penghalusannya sudah tersedia sendiri.
        # Nama pendek ditentukan sendiri: bawaannya kata pertama, dan ketiga seri
        # MVRV ini akan sama-sama menulis "MVRV" di tombol sorot.
        # Z-Score tinggal di pane sendiri paling bawah, menyala lewat kotak Z-Score.
        # Areanya tembus pandang supaya dua kelompok bisa menyala bersamaan.
        # Warna Z-Score ikut induknya (navy MVRV): pane-nya terpisah dari garis MVRV,
        # jadi tidak bisa tertukar. Navy lebih gelap dari hijau Rolling, jadi dibuat
        # lebih pekat (0.80, kontras 2.54:1 ke latar chart; pada 0.55 cuma 1.83:1).
        # Pasangan navy + violet ditolak: sama-sama biru gelap saat bertumpuk
        # (jarak Lab 24 untuk mata normal, 10 saat buta warna; navy + hijau 61/59).
        # dim 0.45 x alpha 0.80 = redup 1.44:1, setara violet lama (1.40:1).
        # Pane bawah memakai sumbu kanan (permintaan user 17 Sep 2026), begitu juga SOPR Gap
        # dan AVIV Deviation.
        Series("MVRV Z-Score", "MVRV Z-Score", color="#0070a6", negative_color="#0070a6", axis="right",
               dim=0.45, kind="baseline", smoothing=False, short="Z", alpha=0.45,
               pane="extra"),
        # Tiga jendela rolling satu kelompok legend: namanya keterangan, angka
        # jendelanya kotak kecil yang bisa diklik sendiri-sendiri — sama seperti
        # angka periode smoothing. Hanya 1Y yang menyala di awal.
        Series("Rolling Z-Score (1y)", "MVRV Z-Score 1Y", color="#97c459", negative_color="#97c459", axis="right",
               dim=0.45, kind="baseline", smoothing=False, short="Z roll", alpha=0.35,
               pane="extra", group="Rolling Z-Score"),
        Series("Rolling Z-Score (2y)", "MVRV Z-Score 2Y", color="#97c459", negative_color="#97c459", axis="right",
               dim=0.45, kind="baseline", smoothing=False, alpha=0.35,
               pane="extra", group="Rolling Z-Score", hidden_default=True),
        Series("Rolling Z-Score (4y)", "MVRV Z-Score 4Y", color="#97c459", negative_color="#97c459", axis="right",
               dim=0.45, kind="baseline", smoothing=False, alpha=0.35,
               pane="extra", group="Rolling Z-Score", hidden_default=True),
    ],
    reference_lines=[RefLine(1.0, "Neutral (1.0)")],
    extra_label="Z-Score",
)



MVRV_MOMENTUM = MetricFamily(
    key="mvrv_momentum",
    title="MVRV Momentum",
    subtitle="MVRV Momentum",
    group="Valuation",
    url_path="mvrv-momentum",
    loader=data.load_mvrv_momentum,
    # Pilihan user 22 Sep 2026 dari pratinjau (acuan: chart Glassnode "MVRV Momentum Is Turning
    # Positive"): osilator sebagai area teal (di atas patokan) / rust (di bawah) dengan harga BTC
    # Overlay; saklar tiga varian, bawaan Momentum (dipakai K2). Pane bawah MVRV Ratio + rata-rata
    # sepanjang sejarah, Hidden awal. Garis ambang framework tidak dipasang.
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        Series("MVRV Momentum (SMA30 − SMA30 of SMA30)", "MVRV Momentum", color="#0b8e89",
               negative_color="#bf5546", axis="left", dim=0.45, kind="baseline", alpha=0.45,
               smoothing=False, short="Momentum", precision=3, unit="Momentum"),
        Series("MVRV / SMA180", "MVRV / SMA180", color="#0b8e89", negative_color="#bf5546",
               axis="left", dim=0.45, kind="baseline", base=1.0, alpha=0.45, smoothing=False,
               short="÷180", precision=3, unit="÷ SMA180"),
        Series("MVRV / SMA365", "MVRV / SMA365", color="#0b8e89", negative_color="#bf5546",
               axis="left", dim=0.45, kind="baseline", base=1.0, alpha=0.45, smoothing=False,
               short="÷365", precision=3, unit="÷ SMA365"),
        Series("MVRV Ratio", "MVRV", color="#0070a6", axis="right", dim=0.49, short="MVRV",
               smoothing=False, pane="extra"),
        Series("All-time Mean", "MVRV Mean", color="#8b949e", axis="right", dim=0.45,
               short="Mean", smoothing=False, pane="extra"),
    ],
    unit_switch=("Momentum", "÷ SMA180", "÷ SMA365"),
    extra_label="MVRV Ratio",
)


PRICE_LEVELS = MetricFamily(
    key="price_levels",
    title="Price Levels",
    subtitle="Price Levels",
    group="Valuation",
    url_path="price-levels",
    loader=data.load_price_levels,
    # Semua level satuannya harga: satu sumbu (kanan) bersama BTC. Skala bawaan linear
    # ("Auto" = linear yang menyesuaikan zoom; "Linear" di kontrol = rentang dikunci).
    metric_scale_default="Auto",
    price_scale_default="Auto",
    series=[
        # Kohort memakai warna yang sama dengan halaman MVRV: STH rust, semua holder (RP)
        # navy, LTH teal — mata langsung mengenali kohortnya di halaman mana pun.
        Series("STH RP", "STH RP", color="#bf5546", axis="right", dim=0.44,
               short="STH", precision=0),
        # Ditulis lengkap di legend: singkatan "RP" belum tentu dikenal pembaca. STH RP dan
        # LTH RP tetap singkat (keputusan user 14 Sep 2026); tombol sorot tetap "RP".
        Series("Realized Price", "RP", color="#0070a6", axis="right", dim=0.49, short="RP",
               precision=0),
        Series("LTH RP", "LTH RP", color="#0b8e89", axis="right", dim=0.39,
               short="LTH", precision=0),
        # True Market Mean (Cointime): dasar AVIV — AVIV Mean/Upper = TMM x rata-rata rasio AVIV.
        # Menyala sejak awal. Biru langit dilepas 18 Sep 2026: warna itu dipakai Median MVRV di
        # halaman MVRV, dan user minta satu metrik = satu warna di semua halaman (pola kohort
        # navy/rust/teal), jadi biru langit ikut Median RP dan TMM pindah ke hijau zamrud.
        # Jarak hijau zamrud: 33 normal (terdekat LTH RP teal), 17 deuteranopia (STH RP),
        # 18 protanopia (CVDD). Redup 1,70:1 pada dim 0.32. Tidak dipakai framework v2.
        Series("True Market Mean", "True Market Mean", color="#3fa96b", axis="right", dim=0.32,
               short="TMM", precision=0),
        # Median Realized Price: pasangan harga dari Median MVRV di halaman MVRV.
        # Median RP memakai biru langit yang sama dengan Median MVRV di halaman MVRV
        # (permintaan user 18 Sep 2026): satu metrik dikenali dari warnanya di halaman mana pun,
        # seperti kohort navy/rust/teal. Warna ini ditukar dengan True Market Mean, yang pindah
        # ke hijau zamrud. Jarak #6fb6de sesudah tukar: 25 normal (abu 0σ), 18 deuteranopia,
        # 22 protanopia. Redup 1,70:1 pada dim 0.27.
        Series("Median RP", "Median RP", color="#6fb6de", axis="right", dim=0.27,
               short="Med RP", precision=0),
        # AVIV Mean dan Upper satu pasang batas zona: satu keluarga violet, dibedakan terang.
        # Uji jarak Lab (patokan longgar handoff bagian 9): terdekat RP–AVIV Mean 16 saat
        # buta warna; Mean–Upper sengaja mirip (17 normal). Terang dijaga setara kohort.
        Series("AVIV Mean", "AVIV Mean", color="#7b65d2", axis="right", dim=0.42,
               short="AVIV M", precision=0),
        Series("AVIV Upper", "AVIV Upper", color="#a58df0", axis="right", dim=0.30,
               short="AVIV U", precision=0),
        # Kuning tua: terdekat BTC 43 (normal), STH RP 17 (buta warna). Magenta ditolak:
        # saat buta warna jaraknya ke violet AVIV cuma 6.
        Series("CVDD", "CVDD", color="#a8963f", axis="right", dim=0.32,
               short="CVDD", precision=0),
        # Konteks, mati sejak awal: abu-abu dibedakan terang supaya tidak bersaing dengan
        # tujuh garis utama. MVRV 0σ menurut KB satu gugus dengan AVIV Mean.
        Series("MVRV 0σ", "MVRV 0σ", color="#8b949e", axis="right", dim=0.32,
               short="0σ", precision=0, hidden_default=True),
        Series("200 DMA", "200 DMA", color="#b4b2a9", axis="right", dim=0.26,
               short="200D", precision=0, hidden_default=True),
        Series("50 WMA", "50 WMA", color="#6e7681", axis="right", dim=0.42,
               short="50W", precision=0, hidden_default=True),
        Series("200 WMA", "200 WMA", color="#d3d1c7", axis="right", dim=0.22,
               short="200W", precision=0, hidden_default=True),
        # Pane bawah (disetujui user 17 Sep 2026 dari pratinjau): Price/CVDD dipakai framework v2
        # di K4 (kondisi #4 < 1,10; flag <= 1,0) — garis ambang tidak dipasang. Skala Log supaya
        # jarak ke 1,0 terbaca di semua siklus (2010-2013 rasionya sampai 72). Warna ikut induknya.
        # Angka >= 10 tanpa desimal di sumbu (50, bukan 50.00).
        Series("Price / CVDD", "Price / CVDD", color="#a8963f", axis="right", dim=0.32,
               kind="line", smoothing=False, short="P/CVDD", pane="extra", precision=2,
               whole_from=10),
        # Price/RP mati sejak awal: pasangan divergence KB Price Level §4.3 (Price/CVDD > 1
        # sementara Price/RP < 1).
        Series("Price / RP", "Price / RP", color="#0070a6", axis="right", dim=0.49,
               kind="line", smoothing=False, short="P/RP", pane="extra", precision=2,
               whole_from=10, hidden_default=True),
    ],
    extra_label="Price / CVDD",
    extra_scale="Log",
)


AVIV = MetricFamily(
    key="aviv",
    title="AVIV",
    subtitle="AVIV Ratio",
    group="Valuation",
    url_path="aviv",
    loader=data.load_aviv,
    # Dipilih user 17 Sep 2026 dari pratinjau data mingguan: warna B (rasio navy seperti metrik
    # dasar di halaman lain, band violet seperti AVIV di Price Levels), pane Deviation menyala
    # sejak awal, sumbu AVIV Log. BTC di pane sendiri seperti halaman Valuation lain.
    # Mean dan Upper (+0,5σ) = batas Z4/Z5 framework v2 dalam satuan rasio; keduanya garis
    # data (bergerak), bukan garis ambang tetap.
    btc_mode_default="Separate pane",
    metric_scale_default="Log",
    price_scale_default="Log",
    extra_label="Deviation",
    extra_default=True,
    series=[
        # Semua garis berskala sama, jadi saat BTC di pane sendiri pindah ke sumbu kanan
        # (aturan user 15 Sep 2026). Uji jarak Lab: rasio–Mean 45 normal / 16 buta warna,
        # Mean–Upper 17 / 16 (sengaja sekeluarga, sama seperti Price Levels).
        Series("AVIV Ratio", "AVIV Ratio", color="#0070a6", axis="left", separate_axis="right",
               dim=0.49, short="AVIV", precision=3),
        # Band tidak ikut smoothing: rata-rata historisnya sudah bergerak sangat lambat.
        Series("AVIV Mean", "AVIV Mean", color="#7b65d2", axis="left", separate_axis="right",
               dim=0.42, short="Mean", precision=3, smoothing=False),
        Series("AVIV Upper (+0.5σ)", "AVIV Upper", color="#a58df0", axis="left",
               separate_axis="right", dim=0.30, short="Upper", precision=3, smoothing=False),
        # Band konteks satu kelompok legend (kotak kecil +1σ · +2σ · −1σ · −2σ), mati sejak awal.
        # Abu gelap, dibedakan dari violet lewat warna (jarak ke Mean 58 / 47).
        *[Series(f"σ Bands ({nama})", f"AVIV {nama}", color="#6e7681", axis="left",
                 separate_axis="right", dim=0.42, short="σ", precision=3, smoothing=False,
                 group="σ Bands", hidden_default=True)
          for nama in ["+1σ", "+2σ", "−1σ", "−2σ"]],
        # Jarak rasio dari Mean dalam σ: area navy seperti Z-Score ikut MVRV (redup 1.44:1).
        Series("Deviation (σ)", "AVIV Deviation", color="#0070a6", negative_color="#0070a6", axis="right", dim=0.45,
               kind="baseline", smoothing=False, short="Dev", alpha=0.45, pane="extra",
               precision=2),
    ],
)


REALIZED_CAP = MetricFamily(
    key="realized_cap",
    title="Realized Cap",
    subtitle="Realized Cap",
    group="Valuation",
    url_path="realized-cap",
    loader=data.load_realized_cap,
    # Disetujui user 17 Sep 2026 dari pratinjau: total navy, LTH teal, STH rust; skala metrik Log;
    # saklar USD | % (bawaan USD); area perubahan 30 hari seperti LTH/STH Supply. Kelompok
    # Valuation (penyebut MVRV; Realized Price = Realized Cap / supply). Tidak dipakai framework v2.
    btc_mode_default="Separate pane",
    metric_scale_default="Log",
    price_scale_default="Log",
    unit_switch=("USD", "%"),
    series=[
        Series("Realized Cap", "Realized Cap", color="#0070a6", axis="left", separate_axis="right",
               dim=0.49, short="RC", precision=0, unit="USD", compact=True),
        Series("LTH Realized Cap", "LTH Realized Cap", color="#0b8e89", axis="left",
               separate_axis="right", dim=0.39, short="LTH", precision=0, unit="USD", compact=True),
        Series("STH Realized Cap", "STH Realized Cap", color="#bf5546", axis="left",
               separate_axis="right", dim=0.44, short="STH", precision=0, unit="USD", compact=True),
        # Porsi terhadap total (garis total tidak punya versi %: selalu 100).
        Series("LTH Realized Cap (%)", "LTH Realized Cap %", color="#0b8e89", axis="left",
               separate_axis="right", dim=0.39, short="LTH %", precision=1, unit="%",
               pair="LTH Realized Cap"),
        Series("STH Realized Cap (%)", "STH Realized Cap %", color="#bf5546", axis="left",
               separate_axis="right", dim=0.44, short="STH %", precision=1, unit="%",
               pair="STH Realized Cap"),
        # Modal masuk/keluar: di pane harga di belakang BTC (sumbu kiri); Overlay/Hidden -> pane
        # bawah sumbu kanan. Naik teal, turun rust. Selalu persen.
        Series("Realized Cap 30d Change (%)", "Realized Cap 30d Change", color="#0b8e89",
               negative_color="#bf5546", axis="left", dim=0.45, kind="baseline",
               smoothing=False, alpha=0.45, short="RC 30d", pane="price", precision=1),
    ],
)


SOPR = MetricFamily(
    key="sopr",
    title="SOPR",
    subtitle="Spent Output Profit Ratio",
    group="Profitability",
    url_path="sopr",
    loader=data.load_sopr,
    # LTH-SOPR harian melonjak sampai puluhan, bahkan di 2024 (30) dan 2025 (24), jadi tidak
    # boleh berbagi sumbu dengan aSOPR/STH-SOPR (0,9–1,2). Karena itu harga BTC dipisah ke
    # pane sendiri sejak awal dan LTH-SOPR memakai sumbu kanan; skala Log supaya LTH 0,50
    # tetap terbaca di dekat puncak. Dekat 1,0 skala Log praktis sama dengan linear.
    # Dipilih user 13 Sep 2026 (tata letak B dari tiga pratinjau).
    # Pane Gap mati sejak awal (keputusan user 14 Sep 2026), apa pun mode harga BTC.
    btc_mode_default="Separate pane",
    metric_scale_default="Log",
    price_scale_default="Log",
    series=[
        # Warna ikut kohort seperti dua halaman sebelumnya: semua holder navy, STH rust,
        # LTH teal. SOPR 3 desimal: nilainya selalu dekat 1,00 (0,995 dan 1,004).
        Series("aSOPR", "aSOPR", color="#0070a6", axis="left", dim=0.49,
               short="aSOPR", precision=3),
        Series("STH-SOPR", "STH-SOPR", color="#bf5546", axis="left", dim=0.44,
               short="STH", precision=3),
        # Di atas 100 (2011, 2013) tanpa desimal: sumbunya tidak menulis "1,200.000".
        Series("LTH-SOPR", "LTH-SOPR", color="#0b8e89", axis="left", dim=0.39,
               separate_axis="right", short="LTH", precision=3, whole_from=100),
        # Gap SMA90 − SMA60(SMA90), rumus KB SOPR §12 (lihat data.load_sopr). Area ikut
        # warna induknya (rust STH), sama seperti Z-Score ikut navy MVRV. 5 desimal: KB
        # menulis nilai seperti +0.00096. dim 0.41 x alpha 0.80 = redup 1.44:1, setara Z-Score.
        Series("STH-SOPR Gap", "STH-SOPR Gap", color="#bf5546", negative_color="#bf5546", axis="right", dim=0.41,
               kind="baseline", smoothing=False, short="Gap", alpha=0.45,
               pane="extra", precision=5),
    ],
    # Batas untung/rugi (definisi SOPR, bukan ambang framework), di sumbu kiri dan kanan.
    reference_lines=[RefLine(1.0, "Break-even (1.0)", all_axes=True)],
    extra_label="SOPR Gap",
)


UNREALIZED_PL = MetricFamily(
    key="unrealized_pl",
    title="Unrealized P/L",
    subtitle="Relative Unrealized Profit & Loss by Cohort",
    group="Profitability",
    url_path="unrealized-pl",
    loader=data.load_unrealized_pl,
    # Disetujui user 18 Sep 2026 dari pratinjau: empat garis semua positif (seperti ChartInspect),
    # sisi rugi memakai warna terang kohortnya (pola Supply in Profit). Tanpa garis NUPL: NUPL
    # dibaca di halaman NUPL saja, satu sumber (lihat docstring load_unrealized_pl). Tidak dipakai
    # framework v2, jadi tanpa garis ambang.
    # LTH di sumbu kiri, STH di sumbu kanan: STH jauh lebih kecil (0,015 vs 0,370), jadi kalau
    # satu sumbu garis STH menempel nol. Harga BTC karena itu di pane sendiri (dicoba Overlay
    # 18 Sep 2026: harga menumpang salah satu sumbu metrik dan menggepengkannya).
    btc_mode_default="Separate pane",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        Series("LTH Unrealized Profit", "LTH Unrealized Profit", color="#0b8e89", axis="left",
               dim=0.39, short="LTH P", precision=3),
        Series("STH Unrealized Profit", "STH Unrealized Profit", color="#bf5546", axis="right",
               dim=0.44, short="STH P", precision=3),
        Series("LTH Unrealized Loss", "LTH Unrealized Loss", color="#38d1b4", axis="left",
               dim=0.25, short="LTH L", precision=3),
        Series("STH Unrealized Loss", "STH Unrealized Loss", color="#dc9390", axis="right",
               dim=0.29, short="STH L", precision=3),
    ],
)


NUPL = MetricFamily(
    key="nupl",
    title="NUPL",
    subtitle="Net Unrealized Profit/Loss",
    group="Profitability",
    url_path="nupl",
    loader=data.load_nupl,
    # Disetujui user 15 Sep 2026 dari pratinjau data mingguan. BTC di pane sendiri seperti
    # MVRV/SOPR/Supply. Skala metrik linear (Auto): NUPL punya nilai negatif, jadi Log tidak
    # berlaku. Sumbu tidak dipaku −1..1 walau 2011 menarik sumbu sampai −3.6 di Range All:
    # sumbu tetap akan memotong lembah 2011 dan tidak menyesuaikan zoom.
    # Garis ambang KB (0.55, 0.50, −0.20, ...) sengaja tidak dipasang: KB sendiri menyebut
    # ambang tetap tidak andal lintas siklus, dan framework v2 tidak memakai NUPL.
    # Pane Gap mati sejak awal (permintaan user).
    btc_mode_default="Separate pane",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        # Warna ikut kohort: semua holder navy, STH rust, LTH teal. 3 desimal seperti KB.
        # Ketiganya berskala sama, jadi saat BTC di pane sendiri semuanya pindah ke sumbu
        # kanan (separate_axis, permintaan user 15 Sep 2026); saat Overlay kembali ke kiri
        # supaya tidak berbagi sumbu dengan harga.
        Series("NUPL", "NUPL", color="#0070a6", axis="left", separate_axis="right", dim=0.49,
               short="NUPL", precision=3),
        Series("STH-NUPL", "STH-NUPL", color="#bf5546", axis="left", separate_axis="right", dim=0.44,
               short="STH", precision=3),
        Series("LTH-NUPL", "LTH-NUPL", color="#0b8e89", axis="left", separate_axis="right", dim=0.39,
               short="LTH", precision=3),
        # Gap LTH − STH (KB NUPL §8.1): area rust, dim sama dengan SOPR Gap (redup 1.44:1).
        Series("Gap (LTH − STH)", "NUPL Gap", color="#bf5546", negative_color="#bf5546", axis="right", dim=0.41,
               kind="baseline", smoothing=False, short="Gap", alpha=0.45,
               pane="extra", precision=3),
    ],
    # Batas untung/rugi agregat (definisi NUPL, bukan ambang framework).
    reference_lines=[RefLine(0.0, "Break-even (0)")],
    extra_label="NUPL Gap",
)


SUPPLY_IN_PROFIT = MetricFamily(
    key="supply_in_profit",
    title="Supply in Profit",
    subtitle="Supply in Profit",
    group="Profitability",
    url_path="supply-in-profit",
    loader=data.load_supply,
    # Persen supply dibaca sebagai level ("sudah di bawah 50%?"), jadi sumbunya tetap 0–100:
    # di Range 1y dengan Auto sumbu bisa cuma 55–70 dan turun 3 poin terlihat seperti jatuh.
    # Loss = 100 − Profit persis di data (selisih maks 0,0014), jadi bukan garis sendiri
    # melainkan kolom tooltip. Keduanya dipilih user 14 Sep 2026 dari pratinjau.
    metric_range=(0, 100),
    complement=("Profit", "Loss"),
    # Harga BTC di pane sendiri sejak awal (permintaan user 14 Sep 2026).
    btc_mode_default="Separate pane",
    series=[
        # Warna ikut kohort: semua holder navy, STH rust, LTH teal. Satu desimal seperti KB.
        # Sumbu kanan saat BTC di pane sendiri, kiri saat Overlay (sama seperti NUPL, 15 Sep 2026).
        # Nama legend tanpa kata "Supply" (sudah ada di judul halaman): versi panjang membuat
        # legend pecah dua baris di layar 1440 (keputusan user 14 Sep 2026).
        # Warna Loss saat Profit dan Loss sama-sama menyala (set B, dipilih user 14 Sep 2026):
        # sekeluarga tapi lebih terang — navy -> lavender, rust -> merah muda, teal -> aqua.
        # Uji jarak Lab: antar-Loss 28 normal / 28 buta warna (campur putih 50% cuma 18 / 14);
        # terlemah LTH vs STH Loss saat buta warna 13 (normal 64). Kalau hanya Loss yang
        # menyala, garis Loss memakai warna kohort asli.
        Series("Total in Profit", "Total Supply in Profit", color="#0070a6",
               axis="left", separate_axis="right", dim=0.49, short="Total", precision=1,
               complement_color="#839df0"),
        Series("STH in Profit", "STH Supply in Profit", color="#bf5546",
               axis="left", separate_axis="right", dim=0.44, short="STH", precision=1,
               complement_color="#dc9390"),
        Series("LTH in Profit", "LTH Supply in Profit", color="#0b8e89",
               axis="left", separate_axis="right", dim=0.39, short="LTH", precision=1,
               complement_color="#38d1b4"),
    ],
)


HODL_WAVES = MetricFamily(
    key="hodl_waves",
    title="HODL Waves",
    subtitle="HODL Waves",
    group="Holder Behavior",
    url_path="hodl-waves",
    loader=data.load_hodl_waves,
    # Dipilih user 17 Sep 2026 dari pratinjau: area bertumpuk 12 band umur, warna spektrum
    # (muda merah -> tua ungu), band muda di bawah, saklar bobot Realized Cap | Supply di chart
    # (bawaan Realized Cap = RHODL Waves; Supply = HODL Waves). Tidak dipakai framework v2.
    # Nama "HODL Waves" (sempat "RHODL Waves"), harga BTC Overlay di atas band dengan garis
    # putih seperti ChartInspect; RHODL Ratio pindah ke halaman sendiri (keputusan user 17 Sep).
    btc_mode_default="Overlay",
    btc_color="#ffffff",
    btc_dim=0.17,
    metric_scale_default="Auto",
    price_scale_default="Log",
    metric_range=(0, 100),
    stack_units=("Realized Cap", "Supply"),
    series=[
        # Band tidak ikut smoothing dan tidak punya tombol sorot (13 tombol terlalu padat).
        # Mematikan band di legend menumpuk ulang band yang tersisa (lihat tumpuk() di lw_chart).
        Series(nama, f"RC {nama}", color=warna, axis="left", separate_axis="right", dim=0.35,
               kind="stack", smoothing=False, precision=1, stack_index=i,
               stack_cols={"Realized Cap": f"RC {nama}", "Supply": f"Supply {nama}"})
        for i, ((_, nama), warna) in enumerate(zip(data.HODL_BANDS, [
            "#d73027", "#f46d43", "#fdae61", "#fee08b", "#d9ef8b", "#a6d96a",
            "#66bd63", "#1a9850", "#35978f", "#2166ac", "#5e4fa2", "#9e7bd6"]))
    ],
)


RHODL_RATIO = MetricFamily(
    key="rhodl_ratio",
    title="RHODL Ratio",
    subtitle="RHODL Ratio (6m–2y ÷ 1d–3m)",
    group="Holder Behavior",
    url_path="rhodl-ratio",
    loader=data.load_rhodl_ratio,
    # Dari analisa Cohort State Plane (research/analyze_cohort_state_plane.py). Halaman sendiri
    # atas permintaan user 17 Sep 2026 (dipisah dari HODL Waves). Sementara hanya rasio ini;
    # Demand Impulse, Aged Cohort Turnover, dan pita state ditahan (handoff 3.27) — kalau
    # dilanjutkan, ditambahkan ke halaman ini. Judul menyebut rumusnya supaya tidak tertukar
    # dengan RHODL Ratio gaya Glassnode (data_rhodl.csv, 1d-1w / 1y-2y).
    # Harga BTC Overlay satu pane dengan rasio (permintaan user 17 Sep 2026).
    # Skala harga BTC Log sejak awal (permintaan user 17 Sep 2026, sebelumnya Auto).
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        # Navy seperti metrik dasar di halaman lain. Overlay: rasio sumbu kiri, harga kanan;
        # kalau BTC dipindah ke pane sendiri, rasio pindah ke sumbu kanan.
        Series("RHODL Ratio", "RHODL Ratio", color="#0070a6", axis="left", separate_axis="right",
               dim=0.49, short="RHODL", precision=2),
    ],
)


HOLDER_SUPPLY = MetricFamily(
    key="holder_supply",
    title="LTH/STH Supply",
    subtitle="Long- & Short-Term Holder Supply",
    group="Holder Behavior",
    url_path="lth-sth-supply",
    loader=data.load_holder_supply,
    # Disetujui user 17 Sep 2026 dari pratinjau: garis (bukan area bertumpuk), warna kohort,
    # saklar satuan BTC | % di chart (bawaan BTC), harga BTC di pane sendiri. Tidak dipakai
    # framework v2, tanpa garis ambang.
    btc_mode_default="Separate pane",
    metric_scale_default="Auto",
    price_scale_default="Log",
    unit_switch=("BTC", "%"),
    series=[
        Series("LTH Supply", "LTH Supply", color="#0b8e89", axis="left", separate_axis="right",
               dim=0.39, short="LTH", precision=0, unit="BTC", compact=True),
        Series("STH Supply", "STH Supply", color="#bf5546", axis="left", separate_axis="right",
               dim=0.44, short="STH", precision=0, unit="BTC", compact=True),
        # Persen supply beredar: pasangan satuan BTC, pindah ke sumbu seberang kalau dua-duanya
        # menyala (lihat Series.pair).
        Series("LTH Supply (%)", "LTH Supply %", color="#0b8e89", axis="left",
               separate_axis="right", dim=0.39, short="LTH %", precision=1, unit="%",
               pair="LTH Supply"),
        Series("STH Supply (%)", "STH Supply %", color="#bf5546", axis="left",
               separate_axis="right", dim=0.44, short="STH %", precision=1, unit="%",
               pair="STH Supply"),
        # Di pane harga, di belakang garis BTC, sumbu kiri (pilihan user 17 Sep 2026: "pane bawah
        # digabung dengan BTC price"). Naik teal, turun rust. Lompatan pindah dompet koin lama
        # ikut tampil (mis. -1,03 juta Nov 2025, +1,13 juta Apr 2026). Selalu BTC.
        Series("LTH 30d Change", "LTH 30d Change", color="#0b8e89", negative_color="#bf5546",
               axis="left", dim=0.45, kind="baseline", smoothing=False, alpha=0.45,
               short="LTH 30d", pane="price", precision=0, compact=True),
    ],
)


EXCHANGE_FLOW = MetricFamily(
    key="exchange_flow",
    title="Exchange Flow",
    subtitle="Exchange Balance & Net Flow",
    group="Exchange",
    url_path="exchange-flow",
    loader=data.load_exchange,
    # Disetujui user 17 Sep 2026 dari pratinjau (susunan A): harga BTC di pane sendiri, saldo
    # bursa di pane tengah, net flow batang di pane bawah yang menyala sejak awal. Tidak dipakai
    # framework v2 dan belum ada KB, jadi tanpa garis ambang.
    btc_mode_default="Separate pane",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        # Navy = warna dasar metrik utama di semua halaman (keputusan user 17 Sep 2026; sempat
        # cornflower #5b8def, yang terlalu mirip violet AVIV dan lebih terang dari rust/teal).
        Series("Exchange Balance", "Exchange Balance", color="#0070a6", axis="left",
               separate_axis="right", dim=0.49, short="Balance", precision=0, compact=True),
        # Warna menurut tanda seperti funding: masuk bursa (positif) teal, keluar (negatif) rust.
        # Sempat dibalik menurut arti; diganti user 17 Sep 2026 supaya batang di atas nol tidak
        # merah (terkecoh). Sebelum 2012 dan 8 hari kosong 2026 tidak digambar.
        # Sumbu kanan, sejajar sumbu harga dan saldo di atasnya (permintaan user 17 Sep 2026).
        Series("Net Flow", "Net Flow", color="#0b8e89", negative_color="#bf5546", axis="right",
               dim=0.45, kind="histogram", smoothing=False, alpha=0.80, short="Net",
               pane="extra", precision=0, compact=True),
    ],
    # Tanpa garis Zero: garis acuan hanya bisa di pane tengah (akan menarik sumbu saldo ke 0);
    # batang net flow sudah tumbuh dari nol.
    extra_label="Net Flow",
    extra_default=True,
)


FUNDING_OI = MetricFamily(
    key="funding_oi",
    title="Funding Rates & Open Interest",   # nama menu (permintaan user 16 Sep 2026)
    subtitle="Funding Rates & Open Interest",
    group="Derivatives",
    url_path="funding-oi",
    loader=data.load_derivatives,
    # Disetujui user 16 Sep 2026 dari pratinjau: funding batang dua warna, funding dan OI satu
    # pane (sumbu berbeda), perubahan OI di pane bawah. Data mulai Mar 2020; tidak ada KB.
    # Framework v2 hanya memakai funding < 0 (pengubah ukuran K2); ambang lain tidak dipasang.
    btc_mode_default="Separate pane",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        # Funding: batang dari nol, positif teal, negatif rust. Saat BTC di pane sendiri funding
        # di sumbu kanan dan OI di kiri; saat Overlay ditukar supaya funding tidak berbagi
        # sumbu dengan harga. Satuan tidak ditulis (tidak disebut sumber). 4 desimal.
        Series("Funding Rate", "Funding Rate", color="#0b8e89", negative_color="#bf5546",
               axis="left", separate_axis="right", dim=0.45, kind="histogram", alpha=0.80,
               short="Funding", precision=4),
        # OI adalah jumlah (selalu positif), jadi garis, bukan batang. Violet seperti AVIV Mean.
        Series("Open Interest (BTC)", "Open Interest", color="#7b65d2", axis="right",
               separate_axis="left", dim=0.42, short="OI", precision=0, unit="BTC"),
        # OI USD = OI BTC x harga hari itu (API tidak mengirim USD). Violet muda, pasangan
        # AVIV Mean/Upper. Saklar BTC | USD (16 Sep 2026): kalau dua-duanya menyala, USD pindah
        # ke sisi sumbu seberang bila kosong (funding dimatikan), kalau tidak skala tanpa angka.
        Series("Open Interest (USD)", "Open Interest USD", color="#a58df0", axis="right",
               separate_axis="left", dim=0.30, short="OI USD", precision=0, unit="USD",
               pair="Open Interest", compact=True),
        # Perubahan OI harian (bersih dari bursa yang baru masuk): batang dua warna seperti
        # funding (naik teal, turun rust). Batang ikut satuan pertama yang menyala.
        Series("OI Change BTC (1d)", "OI Change", color="#0b8e89", negative_color="#bf5546",
               axis="left", dim=0.45, kind="histogram", smoothing=False, alpha=0.80,
               short="ΔOI", pane="extra", precision=0, unit="BTC"),
        Series("OI Change USD (1d)", "OI Change USD", color="#0b8e89", negative_color="#bf5546",
               axis="left", dim=0.45, kind="histogram", smoothing=False, alpha=0.80,
               short="ΔOI", pane="extra", precision=0, unit="USD", compact=True),
    ],
    reference_lines=[RefLine(0.0, "Zero", follow="Funding Rate")],
    extra_label="OI Change",
    unit_switch=("BTC", "USD"),
    unit_label="OI",
)


FUTURES_BASIS = MetricFamily(
    key="futures_basis",
    title="Futures Basis vs 2Y",
    subtitle="BTC 3M Futures Basis vs US 2Y Treasury",
    group="Derivatives",
    url_path="futures-basis",
    loader=data.load_futures_basis,
    # Pilihan user 22 Sep 2026 dari pratinjau (acuan: chart Glassnode "Crypto has yielded less
    # than Treasuries"): basis navy, 2Y abu sebagai patokan (pengecualian satu-metrik-satu-warna:
    # 2Y navy di halaman US Treasury Yields), BTC Overlay kanan Log. Arsiran di antara basis dan
    # 2Y: teal saat crypto memberi yield lebih besar, rust saat di bawah Treasury. Selisihnya
    # juga ada di pane bawah (kind "baseline"), Hidden awal.
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        # Arsiran teal/rust di antara basis dan 2Y seperti chart Glassnode (pilihan user
        # 22 Sep 2026, cara "tumpuk area" di lw_chart).
        Series("BTC 3M Annualized Basis (%)", "Basis 3M", color="#0070a6", axis="left", dim=0.49,
               short="Basis", fill_with="US 2Y", fill_colors=("#0b8e89", "#bf5546")),
        Series("US 2Y Yield (%)", "US 2Y", color="#8b949e", axis="left", dim=0.45, short="2Y",
               smoothing=False),
        Series("Basis - 2Y (pp)", "Basis - 2Y", color="#0b8e89", negative_color="#bf5546",
               axis="right", dim=0.45, kind="baseline", smoothing=False, alpha=0.45,
               short="Spread", pane="extra"),
    ],
    extra_label="Basis - 2Y",   # Hidden awal: arsiran di pane atas sudah menunjukkan selisihnya
)


FEAR_GREED = MetricFamily(
    key="fear_greed",
    title="Fear & Greed",
    subtitle="Crypto Fear & Greed Index",
    group="Sentiment",
    url_path="fear-greed",
    loader=data.load_fear_greed,
    # Disetujui user 16 Sep 2026 dari pratinjau: garis bergradasi
    # halus menurut nilai, SMA30 menyala sejak awal dengan satu warna. Framework v2 memakai
    # F&G < 30 (K2), < 50 (K5) dan F&G SMA30 (konteks K1/K4); garis ambang itu tidak dipasang.
    # BTC di pane sendiri sejak awal (sempat Overlay satu pane; diganti permintaan user 16 Sep
    # 2026). F&G pindah ke sumbu kanan lewat separate_axis, kembali ke kiri saat Overlay.
    btc_mode_default="Separate pane",
    metric_scale_default="Auto",
    price_scale_default="Log",
    metric_range=(0, 100),
    smoothing_default=[30],
    # SMA30 berbentuk pita (Band, transparan 60 %) sejak awal (permintaan user 16 Sep 2026).
    smoothing_style_default={30: "Band"},
    series=[
        # Gradasi: rust (takut) -> merah muda -> abu (netral) -> aqua -> teal (serakah); bukan
        # merah-hijau supaya aman untuk buta warna, sekeluarga dengan warna funding.
        # SMA30 kuning pucat supaya menonjol di atas garis harian yang ramai.
        # Kelas resmi dari API: Extreme Fear <=25, Fear 26-46, Neutral 47-54, Greed 55-75,
        # Extreme Greed >=76 (dibaca dari valueClassification, 16 Sep 2026).
        Series("Fear & Greed", "Fear & Greed", color="#8b949e", axis="left",
               separate_axis="right", dim=0.45, short="F&G", precision=0, whole_from=0,
               # Nilai harian bilangan bulat (69); SMA30 satu desimal seperti framework (92.4).
               smoothing_precision=1,
               gradient=[[0, "#bf5546"], [25, "#bf5546"], [40, "#dc9390"], [50, "#8b949e"],
                         [62, "#38d1b4"], [75, "#0b8e89"], [100, "#0b8e89"]],
               smoothing_color="#F7E9A8",
               value_labels=[[25, "Extreme Fear"], [46, "Fear"], [54, "Neutral"],
                             [75, "Greed"], [100, "Extreme Greed"]]),
    ],
)


VIX = MetricFamily(
    key="vix",
    title="VIX",
    subtitle="CBOE Volatility Index (VIX)",
    group="Sentiment",
    url_path="vix",
    loader=data.load_vix,
    # Pilihan user 21 Sep 2026 dari pratinjau: Overlay (VIX sumbu kiri linear, BTC kanan Log)
    # dan garis acuan 20. Data resmi Cboe lewat Pipeline 24 (bukan Yahoo, lihat auto_update.py).
    btc_mode_default="Overlay",
    metric_scale_default="Auto",  # Auto = linear dengan autoscale; "Linear" di dashboard = sumbu dikunci
    price_scale_default="Log",
    series=[
        Series("VIX", "VIX", color="#0070a6", axis="left", dim=0.49, precision=2),
    ],
    reference_lines=[RefLine(20.0, "20")],
)


TREASURY_YIELDS = MetricFamily(
    key="treasury_yields",
    title="US Treasury Yields",
    subtitle="US Treasury Yields (2Y & 10Y)",
    group="Macro",
    url_path="treasury-yields",
    loader=data.load_yields,
    # Pilihan user 21 Sep 2026 dari pratinjau: 2Y + 10Y + pane spread; tampilan awal 2Y saja
    # (10Y mati di legend, pane spread Hidden). Overlay seperti VIX: yield sumbu kiri, BTC kanan
    # Log. 10Y violet: jarak ke oranye BTC 126, ke navy 45, buta warna min 34.
    # Data FRED DGS2/DGS10 lewat Pipeline 25 auto_update.py.
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        Series("US 2Y Yield (%)", "US 2Y", color="#0070a6", axis="left", dim=0.49, short="2Y"),
        Series("US 10Y Yield (%)", "US 10Y", color="#7b65d2", axis="left", dim=0.45, short="10Y",
               hidden_default=True),
        # Area teal saat 10Y di atas 2Y, rust saat terbalik (negatif). Tanpa garis Zero:
        # garis acuan hanya bisa di pane tengah; area sudah tumbuh dari nol.
        Series("10Y - 2Y Spread (pp)", "10Y-2Y", color="#0b8e89", negative_color="#bf5546",
               axis="right", dim=0.45, kind="baseline", smoothing=False, alpha=0.45,
               short="Spread", pane="extra"),
    ],
    extra_label="10Y - 2Y",
)


DXY = MetricFamily(
    key="dxy",
    title="DXY",
    subtitle="US Dollar Index (DXY)",
    group="Macro",
    url_path="dxy",
    loader=data.load_dxy,
    # Pilihan user 22 Sep 2026 dari pratinjau: halaman sendiri (bukan digabung dengan yields),
    # Overlay seperti VIX (DXY sumbu kiri, BTC kanan Log), garis acuan 100 = nilai dasar indeks
    # (Mar 1973). Data Yahoo DX-Y.NYB lewat Pipeline 23 auto_update.py.
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        Series("DXY", "DXY", color="#0070a6", axis="left", dim=0.49, precision=2),
    ],
    reference_lines=[RefLine(100.0, "100")],
)


SSR = MetricFamily(
    key="ssr",
    title="SSR",
    subtitle="Stablecoin Supply Ratio (SSR)",
    group="Liquidity",
    url_path="ssr",
    loader=data.load_ssr,
    # Pilihan user 23 Sep 2026 dari pratinjau: SSR standar (market cap BTC / supply stablecoin,
    # bukan proksi harga), mulai 2018, Overlay, SSR navy sumbu kiri Log, BTC kanan Log, tanpa
    # garis acuan. Data: Pipeline 27 auto_update.py (sejarah blockchain + DefiLlama).
    btc_mode_default="Overlay",
    metric_scale_default="Log",
    price_scale_default="Log",
    series=[
        Series("SSR", "SSR", color="#0070a6", axis="left", dim=0.49, precision=2),
    ],
)


EXCHANGE_RATIO = MetricFamily(
    key="exchange_ratio",
    title="Exchange Ratio",
    subtitle="Exchange Stablecoin Ratio (BTC ÷ Stablecoin Reserves)",
    group="Liquidity",
    url_path="exchange-ratio",
    loader=data.load_exchange_ratio,
    # Pilihan user 23 Sep 2026 dari pratinjau: halaman sendiri (bukan saklar di SSR), Overlay, rasio
    # navy kiri, BTC Log kanan; pane Reserves (BTC violet, stablecoin teal, USD ringkas) nyala awal.
    # Hanya 19 bursa DefiLlama (tanpa Coinbase dkk.): untuk membedah bentuk, bukan level CryptoQuant.
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        Series("Exchange Ratio", "Exchange Ratio", color="#0070a6", axis="left", dim=0.49, precision=3),
        Series("BTC Reserve (USD)", "BTC Reserve", color="#7b65d2", axis="right", dim=0.45,
               short="BTC Res", precision=0, compact=True, pane="extra", smoothing=False),
        Series("Stablecoin Reserve (USD)", "Stablecoin Reserve", color="#0b8e89", axis="right", dim=0.39,
               short="Stable", precision=0, compact=True, pane="extra", smoothing=False),
    ],
    extra_label="Reserves",
    extra_default=True,
)


# Urutan di sini = urutan menu sidebar; kelompok muncul menurut halaman pertamanya.
# Halaman pertama jadi halaman bawaan (alamat localhost:8503/).
BTC_TRADFI = MetricFamily(
    key="btc_tradfi",
    title="BTC vs Stocks & Gold",
    subtitle="BTC Relative Strength vs S&P 500 & Gold",
    group="Macro",
    url_path="btc-stocks-gold",
    loader=data.load_btc_tradfi,
    # Permintaan user 21 Sep 2026 dari gambar riset: Z-Score log(BTC / pembanding) sebagai
    # area dua warna, harga BTC menumpang (Overlay, sumbu kanan Log). Di atas nol rust, di
    # bawah nol teal (gambar riset: merah atas, hijau bawah). Saklar S&P 500 | Gold di chart,
    # boleh dua-duanya: saat bersama, isian S&P diredupkan ke 35 % dan Gold jadi garis olive
    # (pilihan user dari pratinjau). Jendela rolling dipilih di kotak Window (bawaan 365 hari),
    # menggantikan Smoothing. Garis ambang ±2 dan titik sinyal sengaja tidak dipasang: riset
    # menyimpulkan sinyalnya masih hipotesis, dan dashboard tidak memasang ambang.
    # Data S&P/emas: Pipeline 23 auto_update.py (Yahoo), hanya hari bursa, di-ffill di loader.
    btc_mode_default="Overlay",
    metric_scale_default="Auto",
    price_scale_default="Log",
    series=[
        Series("BTC / S&P 500 Z-Score", "S&P 500 Z", color="#bf5546", negative_color="#0b8e89",
               axis="left", dim=0.45, kind="baseline", smoothing=False, alpha=0.45,
               alpha_together=0.35, short="S&P", unit="S&P 500"),
        Series("BTC / Gold Z-Score", "Gold Z", color="#bf5546", negative_color="#0b8e89",
               axis="left", dim=0.45, kind="baseline", smoothing=False, alpha=0.45,
               short="Gold", unit="Gold", show_when="alone"),
        # Olive seperti CVDD (Price Levels): jarak ke oranye BTC 43 normal, 28 deuteranopia,
        # 17 protanopia; dipilih user 21 Sep 2026. Redup 1,70:1 pada dim 0.32.
        Series("Gold Z-Score (line)", "Gold Z", color="#a8963f", axis="left", dim=0.32,
               smoothing=False, unit="Gold", show_when="together"),
    ],
    unit_switch=("S&P 500", "Gold"),
    window_days={"6m": 180, "1y": 365, "2y": 730, "4y": 1460},
)


# Batang -> area (kind "baseline", pilihan user 22 Sep 2026): semua histogram kecuali data harian
# yang loncat-loncat (Funding Rate, OI Change, Net Flow) — di sana batang lebih jujur.
FAMILIES = {f.title: f for f in [MARKET_VALUATION, MVRV_MOMENTUM, PRICE_LEVELS, AVIV, REALIZED_CAP, SOPR, NUPL, UNREALIZED_PL, SUPPLY_IN_PROFIT,
                                   HODL_WAVES, RHODL_RATIO, HOLDER_SUPPLY, EXCHANGE_FLOW,
                                   FUNDING_OI, FUTURES_BASIS, FEAR_GREED, VIX, BTC_TRADFI, TREASURY_YIELDS, DXY, SSR, EXCHANGE_RATIO]}
