"""Rencana garis yang dikirim ke chart.

render_metric_page() menyusun daftar Line, lalu menggambarnya lewat lw_chart.
Mesin Plotly dibuang 13 Sep 2026: semua fitur hanya dibuat untuk Lightweight, jadi
Plotly selalu tertinggal. Kodenya masih ada di commit 37697ce kalau suatu saat perlu.
"""
from dataclasses import dataclass

from . import lw_chart


@dataclass
class Line:
    """Satu garis yang harus digambar."""
    name: str
    col: str
    color: str
    axis: str            # "left" atau "right"
    width: float = 1.5
    style: int = 0             # pola garis: 0 penuh, 1 titik, 2 putus, 3 putus panjang
    steps: bool = False        # garis tangga (lineType WithSteps)
    alpha: float = 1.0         # < 1 = pita tembus pandang
    group: str | None = None   # seri induk untuk legend & sorot; None = garis acuan
    hidden_default: bool = False  # lahir dalam keadaan mati di legend
    dim: float = 0.3           # opasitas saat seri lain disorot
    kind: str = "line"         # "line" atau "histogram" (batang dari garis nol)
    short: str | None = None   # nama pendek di tombol sorot
    precision: int = 2         # desimal di sumbu, label nilai terakhir, dan tooltip
    whole_from: float | None = None  # angka sebesar ini ke atas ditulis tanpa desimal
    complement_color: str | None = None  # warna garis pasangan (Loss) saat keduanya menyala


def render(df, lines, price_line, extra_lines, height, metric_mode, price_mode, key,
           tooltip="Cursor", metric_range=None, complement=None, view=None):
    """Legend dan sorot diproses di browser; key dipakai untuk menyimpan pilihan."""
    lw_chart.render(df, lines, price_line, extra_lines, height,
                    metric_mode, price_mode, key, tooltip, metric_range, complement, view)
