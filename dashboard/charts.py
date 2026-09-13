"""Dua mesin penggambar chart yang membaca rencana garis yang sama.

render_metric_page() menyusun daftar Line, lalu memilih salah satu mesin di sini.
Menambah mesin ketiga cukup menambah satu fungsi, tanpa menyentuh registry.
"""
from dataclasses import dataclass

import plotly.graph_objects as go
import streamlit as st
from plotly.subplots import make_subplots
from . import lw_chart

LIGHTWEIGHT, PLOTLY = "Lightweight", "Plotly"
ENGINES = [LIGHTWEIGHT, PLOTLY]

BG = "#131722"
GRID = "rgba(42,46,57,0.3)"
TEXT = "#d1d4dc"
BTC_COLOR = "#f7931a"


@dataclass
class Line:
    """Satu garis yang harus digambar, terlepas dari mesin mana yang dipakai."""
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


# Pola garis lightweight-charts diterjemahkan ke nama pola Plotly.
PLOTLY_DASH = {0: "solid", 1: "dot", 2: "dash", 3: "longdash", 4: "longdashdot"}


def _rgba(color, alpha):
    """Warna pita: hex diberi tingkat tembus pandang."""
    if alpha >= 1 or not color.startswith("#"):
        return color
    r, g, b = (int(color[i:i + 2], 16) for i in (1, 3, 5))
    return f"rgba({r},{g},{b},{alpha})"


def _log(mode):
    return mode == "Log"


# ------------------------------------------------------------- lightweight

def render_lightweight(df, lines, price_line, extra_lines, height,
                       metric_mode, price_mode, key):
    """Legend dan sorot diproses di browser; key dipakai untuk menyimpan pilihan."""
    lw_chart.render(df, lines, price_line, extra_lines, height,
                    metric_mode, price_mode, key)


# ------------------------------------------------------------------ plotly

def _plotly_trace(df, ln, axis_name):
    if ln.kind == "histogram":
        return go.Bar(
            x=df["Date"], y=df[ln.col], name=ln.name, yaxis=axis_name,
            marker=dict(color=_rgba(ln.color, ln.alpha)),
            hovertemplate="%{y:.4f}<extra>" + ln.name + "</extra>",
        )
    return go.Scattergl(
        x=df["Date"], y=df[ln.col], name=ln.name, yaxis=axis_name,
        mode="lines",
        line=dict(color=_rgba(ln.color, ln.alpha), width=ln.width,
                  dash=PLOTLY_DASH.get(ln.style, "solid"),
                  shape="hv" if ln.steps else "linear"),
        hovertemplate="%{y:.4f}<extra>" + ln.name + "</extra>",
    )


def _plotly_base(height):
    return dict(
        height=height,
        paper_bgcolor=BG, plot_bgcolor=BG,
        font=dict(color=TEXT, size=11),
        margin=dict(l=8, r=8, t=28, b=8),
        hovermode="x unified",
        dragmode="pan",
        legend=dict(orientation="h", yanchor="bottom", y=1.0, x=0,
                    bgcolor="rgba(0,0,0,0)"),
    )


def render_plotly(df, lines, price_line, extra_lines, height, metric_mode, price_mode, key):
    # Plotly belum mengenal pane tambahan; garisnya digabung ke chart metrik.
    lines = list(lines) + list(extra_lines or [])
    axis_type = "log" if _log(metric_mode) else "linear"
    price_type = "log" if _log(price_mode) else "linear"
    grid = dict(gridcolor=GRID, zeroline=False, showspikes=True,
                spikemode="across", spikethickness=1, spikecolor="#5a6072")

    if price_line is not None:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.45, 0.55], vertical_spacing=0.03)
        fig.add_trace(_plotly_trace(df, price_line, "y"), row=1, col=1)
        for ln in lines:
            fig.add_trace(_plotly_trace(df, ln, "y"), row=2, col=1)
        fig.update_yaxes(type=price_type, row=1, col=1, **grid)
        fig.update_yaxes(type=axis_type, row=2, col=1, **grid)
        fig.update_xaxes(**grid)
        fig.update_layout(**_plotly_base(height))
    else:
        fig = go.Figure()
        for ln in lines:
            fig.add_trace(_plotly_trace(df, ln, "y" if ln.axis == "left" else "y2"))
        layout = _plotly_base(height)
        layout.update(
            xaxis=dict(**grid),
            yaxis=dict(type=axis_type, side="left", **grid),
            yaxis2=dict(type=price_type, side="right", overlaying="y",
                        showgrid=False, zeroline=False),
        )
        fig.update_layout(**layout)

    st.plotly_chart(fig, use_container_width=True, key=key,
                    config={"scrollZoom": True, "displaylogo": False})
