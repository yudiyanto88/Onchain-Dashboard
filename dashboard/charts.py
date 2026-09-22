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
    negative_color: str | None = None    # histogram: warna batang negatif (positif = color)
    unit: str | None = None              # satuan untuk saklar satuan di chart
    pair: str | None = None              # kolom seri pasangan satuan (pindah sisi sumbu)
    compact: bool = False                # angka ringkas K/M/B
    gradient: list | None = None         # warna garis per titik menurut nilai [[nilai, hex], ...]
    value_labels: list | None = None     # nama kelas per rentang [[batas atas, nama], ...]
    stack_index: int | None = None       # kind "stack": urutan band dari bawah (0 = paling muda)
    stack_cols: dict | None = None       # kind "stack": kolom per bobot {"Realized Cap": col, ...}
    show_when: str | None = None         # "alone" / "together" menurut saklar satuan
    alpha_together: float | None = None  # opasitas batang saat semua satuan menyala
    fill_with: str | None = None         # arsiran ke garis berkolom ini (lihat Series)
    fill_colors: tuple | None = None
    fill_alpha: float = 0.35
    base: float = 0.0                    # patokan area kind "baseline"


def render(df, lines, price_line, extra_lines, height, metric_mode, price_mode, key,
           tooltip="Cursor", metric_range=None, complement=None, view=None,
           unit_switch=None, unit_label="", stack_units=None, extra_mode="Auto",
           price_extra=None):
    """Legend dan sorot diproses di browser; key dipakai untuk menyimpan pilihan."""
    lw_chart.render(df, lines, price_line, extra_lines, height,
                    metric_mode, price_mode, key, tooltip, metric_range, complement, view,
                    unit_switch, unit_label, stack_units, extra_mode, price_extra)
