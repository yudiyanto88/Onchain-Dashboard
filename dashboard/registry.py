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
    kind: str = "line"                # "line" atau "histogram"
    smoothing: bool = True            # ikut digandakan oleh kontrol Smoothing
    short: str | None = None          # nama di tombol sorot; bawaannya kata pertama label
    alpha: float = 1.0                # < 1 = tembus pandang (dipakai batang histogram)
    group: str | None = None          # kelompok legend; bawaannya label sendiri
    hidden_default: bool = False      # lahir dalam keadaan mati di legend
    pane: str = "main"                # "main" atau "extra" (pane tambahan paling bawah)
    precision: int = 2                # desimal di sumbu, label nilai terakhir, dan tooltip
                                      # (harga 0; rasio 2; nanti funding rate bisa 5)
    whole_from: float | None = None   # angka sebesar ini ke atas ditulis tanpa desimal
                                      # (LTH-SOPR: 1.318 tapi 384, bukan 384.000)
    complement_color: str | None = None  # warna garis pasangan (Loss) saat Profit dan
                                         # Loss sama-sama menyala (MetricFamily.complement)
    negative_color: str | None = None    # histogram: warna batang bernilai negatif
                                         # (color dipakai untuk batang positif)
    unit: str | None = None       # satuan untuk saklar MetricFamily.unit_switch ("BTC"/"USD")
    pair: str | None = None       # kolom seri pasangan satuan pertama; seri ini pindah ke sisi
                                  # sumbu seberang saat keduanya menyala (lihat lw_chart)
    compact: bool = False         # angka ringkas K/M/B (40.81B)


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
        # Z-Score digambar sebagai batang dari garis nol, bukan garis: bentuknya
        # langsung membedakannya dari tiga rasio di atas. Tidak ikut smoothing —
        # yang rolling sudah merupakan penghalusan, dan yang full-history bergerak
        # seiring MVRV Ratio yang penghalusannya sudah tersedia sendiri.
        # Nama pendek ditentukan sendiri: bawaannya kata pertama, dan ketiga seri
        # MVRV ini akan sama-sama menulis "MVRV" di tombol sorot.
        # Z-Score tinggal di pane sendiri paling bawah, menyala lewat kotak Z-Score.
        # Batangnya tembus pandang supaya dua kelompok bisa menyala bersamaan.
        # Warna Z-Score ikut induknya (navy MVRV): pane-nya terpisah dari garis MVRV,
        # jadi tidak bisa tertukar. Navy lebih gelap dari hijau Rolling, jadi dibuat
        # lebih pekat (0.80, kontras 2.54:1 ke latar chart; pada 0.55 cuma 1.83:1).
        # Pasangan navy + violet ditolak: sama-sama biru gelap saat bertumpuk
        # (jarak Lab 24 untuk mata normal, 10 saat buta warna; navy + hijau 61/59).
        # dim 0.45 x alpha 0.80 = redup 1.44:1, setara violet lama (1.40:1).
        Series("MVRV Z-Score", "MVRV Z-Score", color="#0070a6", axis="left",
               dim=0.45, kind="histogram", smoothing=False, short="Z", alpha=0.80,
               pane="extra"),
        # Tiga jendela rolling satu kelompok legend: namanya keterangan, angka
        # jendelanya kotak kecil yang bisa diklik sendiri-sendiri — sama seperti
        # angka periode smoothing. Hanya 1Y yang menyala di awal.
        Series("Rolling Z-Score (1y)", "MVRV Z-Score 1Y", color="#97c459", axis="left",
               dim=0.45, kind="histogram", smoothing=False, short="Z roll", alpha=0.55,
               pane="extra", group="Rolling Z-Score"),
        Series("Rolling Z-Score (2y)", "MVRV Z-Score 2Y", color="#97c459", axis="left",
               dim=0.45, kind="histogram", smoothing=False, alpha=0.55,
               pane="extra", group="Rolling Z-Score", hidden_default=True),
        Series("Rolling Z-Score (4y)", "MVRV Z-Score 4Y", color="#97c459", axis="left",
               dim=0.45, kind="histogram", smoothing=False, alpha=0.55,
               pane="extra", group="Rolling Z-Score", hidden_default=True),
    ],
    reference_lines=[RefLine(1.0, "Neutral (1.0)")],
    extra_label="Z-Score",
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
        # Gap SMA90 − SMA60(SMA90), rumus KB SOPR §12 (lihat data.load_sopr). Batang ikut
        # warna induknya (rust STH), sama seperti Z-Score ikut navy MVRV. 5 desimal: KB
        # menulis nilai seperti +0.00096. dim 0.41 x alpha 0.80 = redup 1.44:1, setara Z-Score.
        Series("STH-SOPR Gap", "STH-SOPR Gap", color="#bf5546", axis="left", dim=0.41,
               kind="histogram", smoothing=False, short="Gap", alpha=0.80,
               pane="extra", precision=5),
    ],
    # Batas untung/rugi (definisi SOPR, bukan ambang framework), di sumbu kiri dan kanan.
    reference_lines=[RefLine(1.0, "Break-even (1.0)", all_axes=True)],
    extra_label="SOPR Gap",
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
        # Gap LTH − STH (KB NUPL §8.1): batang rust, dim sama dengan SOPR Gap (redup 1.44:1).
        Series("Gap (LTH − STH)", "NUPL Gap", color="#bf5546", axis="left", dim=0.41,
               kind="histogram", smoothing=False, short="Gap", alpha=0.80,
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


# Urutan di sini = urutan menu sidebar; kelompok muncul menurut halaman pertamanya.
# Halaman pertama jadi halaman bawaan (alamat localhost:8503/).
FAMILIES = {f.title: f for f in [MARKET_VALUATION, PRICE_LEVELS, SOPR, NUPL, SUPPLY_IN_PROFIT,
                                   FUNDING_OI]}
