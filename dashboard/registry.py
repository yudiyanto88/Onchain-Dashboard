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


@dataclass
class RefLine:
    """Garis acuan horizontal, misalnya batas netral MVRV di 1.0."""
    value: float
    label: str


@dataclass
class MetricFamily:
    key: str
    title: str
    subtitle: str
    loader: Callable
    series: list[Series]
    reference_lines: list[RefLine] = field(default_factory=list)
    metric_scale_default: str = "Auto"
    price_scale_default: str = "Log"
    # Nama kotak kontrol untuk pane tambahan paling bawah (seri pane="extra"),
    # misalnya "Z-Score" atau nanti "Net flow". Kotaknya hanya muncul kalau ada seri itu.
    extra_label: str = "Bottom pane"


MARKET_VALUATION = MetricFamily(
    key="market_valuation",
    title="Market Valuation",
    subtitle="MVRV Oscillators",
    loader=data.load_mvrv,
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
    subtitle="On-chain Cost Basis",
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
        Series("RP", "RP", color="#0070a6", axis="right", dim=0.49, short="RP", precision=0),
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


# Urutan di sini = urutan menu sidebar.
FAMILIES = {f.title: f for f in [MARKET_VALUATION, PRICE_LEVELS]}
