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
    default_selection: list[str] | None = None
    metric_scale_default: str = "Auto"
    price_scale_default: str = "Log"

    def default_series(self):
        if self.default_selection is not None:
            return self.default_selection
        return [s.label for s in self.series]


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
    ],
    reference_lines=[RefLine(1.0, "Neutral (1.0)")],
)


FAMILIES = {f.title: f for f in [MARKET_VALUATION]}
