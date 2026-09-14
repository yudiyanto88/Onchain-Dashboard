"""Renderer tunggal untuk halaman metrik.

Satu fungsi render_metric_page() melayani semua keluarga metrik.
Perbaikan layout di sini langsung berlaku untuk seluruh halaman.
"""
import base64

import streamlit as st
from . import charts, data
from .charts import Line
from .registry import MetricFamily

PRESETS = ["1M", "3M", "6M", "1Y", "4Y", "All"]
# Ditampilkan huruf kecil (1m, 1y) supaya seragam dengan periode smoothing (7d)
# dan jendela Rolling Z-Score (1y). Nilai di baliknya tetap, jadi tanggal tidak berubah.
def _preset_label(preset):
    return preset if preset == "All" else preset.lower()
DEFAULT_PRESET = "All"

SMOOTH_KINDS = ["SMA", "EMA"]
# Kisi periode 3x3. "Off" mematikan semua periode sekaligus.
PERIOD_GRID = [["Off", 7, 14], [30, 60, 90], [200, 365, 730]]

# Mode skala sumbu.
AUTO, LINEAR, LOG = "Auto", "Linear", "Log"
SCALE_MODES = [AUTO, LINEAR, LOG]

# Tinggi chart bisa disetel karena tinggi layar tiap orang berbeda.
HEIGHTS = [600, 720, 860, 1000]

# Cara harga BTC ditampilkan. Overlay didahulukan karena jadi default.
OVERLAY = "Overlay"         # harga digabung ke chart metrik, sumbu kanan
PANE = "Separate pane"      # harga di chart sendiri di atas chart metrik
HIDDEN = "Hidden"           # harga tidak ditampilkan
BTC_MODES = [OVERLAY, PANE, HIDDEN]

# Pane tambahan paling bawah (Z-Score). Pane dibangun dari sisi Python, jadi saklarnya
# tidak bisa ikut legend yang hidup di dalam chart.
Z_HIDDEN, Z_BOTTOM = "Hidden", "Bottom pane"
Z_MODES = [Z_HIDDEN, Z_BOTTOM]

# Posisi kotak angka saat kursor di chart (lihat posisikanTooltip di lw_chart).
# Cursor jadi bawaan (keputusan user 14 Sep 2026): mata tidak bolak-balik ke pojok chart.
# Satu pilihan untuk semua halaman (selera baca, bukan soal metrik), jadi key-nya tanpa
# awalan family.key. Pindah halaman lewat st.navigation membuat Streamlit membuang nilai
# widget (terukur 14 Sep: Fixed di SOPR jadi Cursor lagi di MVRV), jadi pilihannya disimpan
# di gudang biasa TIP_STORE; widget TIP_KEY hanya cerminan yang disemai ulang tiap halaman.
TIP_MODES = ["Fixed", "Cursor", "Off"]
TIP_DEFAULT = "Cursor"
TIP_KEY = "tooltip_mode"
TIP_STORE = "tooltip_pref"


def _on_tooltip():
    _keep(TIP_KEY, st.session_state[TIP_STORE])
    st.session_state[TIP_STORE] = st.session_state[TIP_KEY]

# Metrik memakai sumbu kiri, harga BTC memakai sumbu kanan.
METRIC_AXIS_DEFAULT = "left"
BTC_AXIS = "right"

BTC_COLOR = "#F7931A"
BTC_DIM = 0.28      # opasitas BTC saat seri lain disorot (kontras 1.70:1, sama dengan metrik)
LINE_WIDTH = 2.0    # semua garis utama, termasuk BTC (uji 13 Sep: 1,5 px tampak tipis di
                    # layar rasio 1 karena library tidak membulatkan tebal garis data)
BTC_PRECISION = 0   # harga BTC tanpa desimal

# Bentuk garis yang bisa dipilih untuk tiap garis smoothing.
LINE_STYLES = {
    "Solid": dict(),
    "Dotted": dict(style=1),
    "Dashed": dict(style=2),
    "Step": dict(steps=True),
    "Band": dict(alpha=0.60),
}
STYLE_NAMES = list(LINE_STYLES)
# Nama saja tidak memberi tahu bentuk garisnya, jadi pilihan ditampilkan sebagai lambang
# bentuknya. Nama tetap tersedia lewat keterangan kecil di sudut kontrol.
# Solid, Dotted, dan Dashed ditulis sebagai kode (huruf monospace, tepat empat karakter)
# supaya semua selebar sama. Step dan Band digambar sebagai gambar garis sungguhan:
# huruf tidak bisa membuat tangga yang rapi, dan tidak bisa tembus pandang seperti pita
# di chart. Ukuran gambarnya 31 x 12 px, selebar empat karakter monospace.
STYLE_GLYPHS = {
    "Solid": "────",   # ────
    "Dotted": "····",  # ····
    "Dashed": "╌╌╌╌",  # ╌╌╌╌
}


def _svg_ikon(isi):
    svg = ('<svg xmlns="http://www.w3.org/2000/svg" width="31" height="12" '
           f'viewBox="0 0 31 12">{isi}</svg>')
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


STYLE_ICONS = {
    # satu anak tangga naik, garis saja tanpa isi
    "Step": _svg_ikon('<path d="M1 9.5 H14 V2.5 H30" fill="none" stroke="#c9d1d9" '
                      'stroke-width="1.2"/>'),
    # balok tebal dengan transparansi yang sama dengan pita di chart (alpha 0.60)
    "Band": _svg_ikon('<line x1="1" y1="6" x2="30" y2="6" stroke="#c9d1d9" '
                      f'stroke-width="4.5" stroke-opacity="{LINE_STYLES["Band"]["alpha"]}"/>'),
}


def _style_label(name):
    if name in STYLE_ICONS:
        return f"![{name}]({STYLE_ICONS[name]})"
    return f"`{STYLE_GLYPHS[name]}`"
WIDTH_MIN, WIDTH_MAX, WIDTH_STEP = 0.5, 5.0, 0.25

# Urutan pemberian gaya saat sebuah periode dinyalakan: titik-titik, tangga, lalu pita.
# Gaya menempel pada periodenya, jadi mematikan periode lain tidak menggeser gaya
# periode yang masih menyala.
STYLE_ORDER = ["Dotted", "Step", "Band"]
STYLE_WIDTH = {"Solid": 1.5, "Dotted": 2.0, "Dashed": 1.25, "Step": 1.5, "Band": 3.0}


def _styles(family):
    """Gudang gaya garis smoothing: dict biasa, bukan nilai widget.

    Nilai widget ikut dibuang Streamlit kalau satu putaran berhenti di tengah
    sebelum bagian Line style sempat digambar, sehingga gaya bisa bergeser sendiri
    saat periode lain dimatikan. Gudang ini tidak bergantung pada putaran itu.
    """
    return st.session_state.setdefault(f"{family.key}_lstyles", {})


def _new_entry(name):
    width = STYLE_WIDTH[name]
    return {"name": name, "width": width, "auto": (name, width)}


def _free_style(taken):
    return next((s for s in STYLE_ORDER if s not in taken),
                STYLE_ORDER[len(taken) % len(STYLE_ORDER)])


def _assign_styles(family):
    """Beri gaya pada periode yang belum punya. Gaya yang sudah ada dipertahankan,
    termasuk saat periode lain dimatikan. Yang digeser hanya gaya kembar yang
    belum pernah diubah sendiri oleh pengguna."""
    k = family.key
    store = _styles(family)
    taken = []
    for period in sorted(st.session_state[f"{k}_periods"]):
        entry = store.get(period)
        # Pilihan terbaru dari tombol disalin dulu, supaya tulisan Default/Custom di
        # kotak kontrol (dihitung sebelum isi popover digambar) sudah ikut terbaru.
        if entry:
            entry["name"] = st.session_state.get(f"{k}_lstyle_{period}") or entry["name"]
            entry["width"] = st.session_state.get(f"{k}_lwidth_{period}") or entry["width"]
        dipilih_sendiri = bool(entry) and entry["name"] != entry["auto"][0]
        if entry is None or (entry["name"] in taken and not dipilih_sendiri):
            entry = _new_entry(_free_style(taken))
            store[period] = entry
        taken.append(entry["name"])


def _smooth_style(family, period):
    """Bentuk dan tebal garis smoothing untuk satu periode."""
    entry = _styles(family).get(period) or _new_entry(STYLE_ORDER[0])
    return dict(LINE_STYLES[entry["name"]], width=entry["width"])


def _style_summary(family):
    store = _styles(family)
    periods = sorted(st.session_state[f"{family.key}_periods"])
    if not periods:
        return "Off"
    for period in periods:
        entry = store.get(period)
        if entry and (entry["name"], entry["width"]) != tuple(entry["auto"]):
            return "Custom"
    return "Default"


def _reset_line_style(family):
    """Kembalikan bentuk dan tebal semua garis smoothing ke urutan bawaan."""
    k = family.key
    store = _styles(family)
    taken = []
    for period in sorted(st.session_state[f"{k}_periods"]):
        entry = _new_entry(_free_style(taken))
        store[period] = entry
        st.session_state[f"{k}_lstyle_{period}"] = entry["name"]
        st.session_state[f"{k}_lwidth_{period}"] = entry["width"]
        taken.append(entry["name"])


def _render_line_style(family):
    """Satu blok pengaturan per garis smoothing: bentuk garis dan tebalnya."""
    k = family.key
    kind = st.session_state[f"{k}_smooth_kind"]
    periods = sorted(st.session_state[f"{k}_periods"])
    store = _styles(family)

    st.markdown(f"<div class='pop-head'><span>LINE STYLE</span>"
                f"<span class='pop-val'>{_style_summary(family)}</span></div>",
                unsafe_allow_html=True)
    if not periods:
        st.caption("Turn on smoothing first. Colours always follow the metric.")
        return

    for period in periods:
        entry = store[period]
        # Nilai widget disemai dari gudang, lalu pilihan pengguna ditulis balik ke gudang.
        st.session_state.setdefault(f"{k}_lstyle_{period}", entry["name"])
        st.session_state.setdefault(f"{k}_lwidth_{period}", entry["width"])

        st.caption(f"{kind} {period}D")
        st.segmented_control(f"Style {period}", STYLE_NAMES, key=f"{k}_lstyle_{period}",
                             on_change=_keep, args=(f"{k}_lstyle_{period}", entry["name"]),
                             format_func=_style_label,
                             help="Solid · Dotted · Dashed · Step · Band",
                             label_visibility="collapsed")
        # Angkanya ditampilkan oleh label bawaan slider, yang ikut bergerak dengan kenop.
        st.slider(f"Width {period}", min_value=WIDTH_MIN, max_value=WIDTH_MAX,
                  step=WIDTH_STEP, key=f"{k}_lwidth_{period}",
                  label_visibility="collapsed")

        entry["name"] = st.session_state[f"{k}_lstyle_{period}"] or entry["name"]
        entry["width"] = st.session_state[f"{k}_lwidth_{period}"] or entry["width"]

    st.button("Reset to default", key=f"{k}_style_reset", use_container_width=True,
              on_click=_reset_line_style, args=(family,))


def _render_header(family, latest):
    """Judul halaman plus tanggal data terakhir, untuk mendeteksi update harian yang macet."""
    # Nama metrik jadi judul besar supaya jelas halaman apa ini; kategori (nama menu
    # sidebar) jadi lencana kecil di atasnya. Lencana memakai latar teal gelap, warna
    # utama dashboard, dengan teks putih: teal gelap sebagai warna huruf terlalu redup.
    # Judul 1.15rem tebal 600, sama dengan menu sidebar, seperti teks tebal lainnya.
    # Kotak lencana dan huruf pertama judul lurus dengan kotak tombol dan tepi chart.
    # Dibuat dari div, bukan h3, supaya Streamlit tidak menambah ikon tautan judul.
    # margin-bottom 16 px membatalkan margin -16 px bawaan wadah teks Streamlit. Tanpa
    # itu baris tombol menimpa judul 1.4 px; dengan itu jaraknya 14.6 px, sama dengan
    # judul lama (terukur: jarak naik 1:1 mengikuti margin ini).
    # Kelas page-title dipakai aturan :fullscreen di app_v2.py untuk menyembunyikan judul.
    st.markdown(
        f"<div class='page-title' style='margin:0 0 16px;line-height:1.2;'>"
        f"<span style='display:inline-block;background:#006d77;color:#ffffff;"
        f"font-size:11px;font-weight:600;letter-spacing:0.12em;text-transform:uppercase;"
        f"line-height:1.4;padding:2px 7px;border-radius:4px;'>{family.group or family.title}</span>"
        f"<div style='display:flex;align-items:baseline;gap:10px;margin-top:4px;'>"
        f"<span style='font-size:1.15rem;font-weight:600;color:#ffffff;'>{family.subtitle}</span>"
        f"<span style='font-size:0.72rem;color:#8b90a0;font-weight:400;'>"
        f"Latest data: {latest:%d %b %Y}</span></div></div>",
        unsafe_allow_html=True)


# ------------------------------------------------------------------ kontrol

def _keep(key, fallback):
    """segmented_control boleh dikosongkan; kembalikan ke nilai terakhir yang sah."""
    if st.session_state.get(key) is None:
        st.session_state[key] = fallback


def _on_btc_mode(family):
    """Saat harga BTC pindah ke pane sendiri, sumbu kanan chart metrik jadi kosong.
    Garis yang punya separate_axis (misalnya LTH MVRV) otomatis pindah ke sana,
    dan kembali ke sumbu bawaannya saat harga BTC tidak lagi di pane terpisah."""
    k = family.key
    _keep(f"{k}_btc", OVERLAY)
    separate = st.session_state[f"{k}_btc"] == PANE
    for s in family.series:
        if s.separate_axis and s.pane != "extra":
            st.session_state[f"{k}_axis_{s.col}"] = s.separate_axis if separate else s.axis


def _init_state(family, dmin, dmax):
    k = family.key
    lo, hi = data.preset_range(DEFAULT_PRESET, dmin, dmax)
    defaults = {
        f"{k}_preset": DEFAULT_PRESET,
        f"{k}_from": lo,
        f"{k}_to": hi,
        f"{k}_smooth_kind": "SMA",
        f"{k}_periods": [],
        f"{k}_extra_periods": [],
        f"{k}_scale_price": family.price_scale_default,
        f"{k}_scale_metric": family.metric_scale_default,
        f"{k}_btc": family.btc_mode_default,
        f"{k}_axis_btc": BTC_AXIS,
        f"{k}_extra": Z_HIDDEN,
        TIP_STORE: TIP_DEFAULT,
        f"{k}_height": 720,
    }
    for key, val in defaults.items():
        st.session_state.setdefault(key, val)
    st.session_state.setdefault(TIP_KEY, st.session_state[TIP_STORE])
    # Halaman yang sejak awal memisahkan harga BTC (SOPR) langsung memakai separate_axis,
    # sama seperti kalau pengguna sendiri memilih Separate pane (_on_btc_mode).
    separate = st.session_state[f"{k}_btc"] == PANE
    for s in family.series:
        if s.pane != "extra":
            axis = s.separate_axis if separate and s.separate_axis else s.axis
            st.session_state.setdefault(f"{k}_axis_{s.col}", axis)


def _smooth_summary(family, short=False):
    """Teks ringkas smoothing. Lebar tombol mengikuti panjang teks ini."""
    k = family.key
    kind = st.session_state[f"{k}_smooth_kind"]
    periods = sorted(st.session_state[f"{k}_periods"])
    if not periods:
        return "Off"
    if len(periods) == 1:
        return f"{kind} {periods[0]}d" if short else f"{kind} {periods[0]} Days"
    return f"{kind} {periods[0]}d and {len(periods) - 1} more"


def _range_summary(family):
    k = family.key
    preset = st.session_state[f"{k}_preset"]
    if preset:
        return _preset_label(preset)
    return (f"{st.session_state[f'{k}_from']:%d %b %y}"
            f" - {st.session_state[f'{k}_to']:%d %b %y}")


def _axis_control(label, key, fallback, disabled=False):
    """Satu baris pilihan sumbu: nama di kiri, tombol Left/Right di kanan.

    Kata "Left"/"Right" sengaja tidak disingkat — tombolnya hanya 88 px dan popover
    240 px, jadi nama terpanjang pun masih muat tanpa perlu ditebak artinya.
    """
    nama, tombol = st.columns([1.2, 1], gap="small", vertical_alignment="center")
    with nama:
        # Tinggi disamakan dengan wadah tombol (32 px) lalu isinya ditengahkan sendiri.
        # margin-bottom 16 px membatalkan margin -16 px bawaan wadah teks Streamlit:
        # tanpa itu tinggi tata letaknya 16 px lebih pendek daripada kotak yang terlihat,
        # dan namanya jatuh 8 px di bawah garis tengah tombol.
        warna = "#6E7681" if disabled else "#d1d4dc"
        st.markdown(
            f"<div style='display:flex;align-items:center;height:32px;margin:0 0 16px;"
            f"font-size:0.8rem;color:{warna};'>{label}</div>",
            unsafe_allow_html=True)
    with tombol:
        st.segmented_control(label, ["left", "right"], key=key,
                             on_change=_keep, args=(key, fallback),
                             format_func=lambda x: "Left" if x == "left" else "Right",
                             label_visibility="collapsed", disabled=disabled)


def _axis_summary(family):
    """Nilai di kotak Display: sisi sumbu yang dipakai garis metrik, atau Mixed."""
    k = family.key
    sides = {st.session_state[f"{k}_axis_{s.col}"]
             for s in family.series if s.pane != "extra"}
    if len(sides) == 1:
        return "Left" if sides.pop() == "left" else "Right"
    return "Mixed"


def _period_button(family, value, key_suffix):
    """Satu kotak pada kisi periode. 'Off' mengosongkan seluruh pilihan."""
    k = family.key
    periods = st.session_state[f"{k}_periods"]

    if value == "Off":
        label, selected = "Off", not periods
    else:
        label, selected = f"{value}d", value in periods

    # Pilihan diubah lewat on_click, bukan di badan tombol yang disusul st.rerun().
    # st.rerun() menghentikan putaran di tengah popover, jadi kontrol yang digambar
    # sesudahnya (Screen paling ujung) tidak sempat muncul dan nilainya dibuang
    # Streamlit — kotak Screen lalu balik sendiri ke "Normal" padahal masih layar penuh.
    # Callback berjalan sebelum halaman digambar ulang, jadi seluruh halaman tetap
    # melihat periode yang baru tanpa ada putaran yang dipotong.
    def alihkan():
        aktif = st.session_state[f"{k}_periods"]
        if value == "Off":
            st.session_state[f"{k}_periods"] = []
        elif value in aktif:
            aktif.remove(value)
        else:
            aktif.append(value)

    st.button(label, key=f"{k}_p_{key_suffix}", use_container_width=True,
              type="primary" if selected else "secondary", on_click=alihkan)


def _render_smoothing(family):
    k = family.key

    st.markdown(f"<div class='pop-head'><span>SMOOTHING</span>"
                f"<span class='pop-val'>{_smooth_summary(family, short=True)}</span></div>",
                unsafe_allow_html=True)

    st.segmented_control("Type", SMOOTH_KINDS, key=f"{k}_smooth_kind",
                         on_change=_keep, args=(f"{k}_smooth_kind", "SMA"),
                         label_visibility="collapsed")

    for r, row in enumerate(PERIOD_GRID):
        cells = st.columns(3, gap="small")
        for c, value in enumerate(row):
            with cells[c]:
                _period_button(family, value, f"{r}{c}")

    # Baris terakhir: input sempit di kiri, tombol Add di tengah,
    # lalu periode tambahan muncul di kanan dengan gaya kotak yang sama.
    extra = st.session_state[f"{k}_extra_periods"]
    add_cols = st.columns(3, gap="small", vertical_alignment="center")

    with add_cols[0]:
        st.number_input("Period", min_value=2, max_value=5000, value=None,
                        placeholder="88", key=f"{k}_new_period",
                        label_visibility="collapsed")
    with add_cols[1]:
        # Sama seperti tombol periode: lewat on_click, tanpa st.rerun() yang memotong
        # putaran dan membuat nilai kontrol sesudahnya dibuang.
        def tambah():
            val = st.session_state[f"{k}_new_period"]
            if not val:
                return
            val = int(val)
            if val not in extra:
                extra.append(val)
            # Periode yang baru ditambahkan langsung aktif di chart.
            if val not in st.session_state[f"{k}_periods"]:
                st.session_state[f"{k}_periods"].append(val)

        st.button("Add", key=f"{k}_add", use_container_width=True, on_click=tambah)
    with add_cols[2]:
        for value in sorted(extra):
            _period_button(family, value, f"x{value}")


def _render_controls(family, dmin, dmax):
    k = family.key

    def on_preset():
        preset = st.session_state[f"{k}_preset"]
        if preset:
            lo, hi = data.preset_range(preset, dmin, dmax)
            st.session_state[f"{k}_from"] = lo
            st.session_state[f"{k}_to"] = hi

    def on_date():
        st.session_state[f"{k}_preset"] = None

    price_s = st.session_state[f"{k}_scale_price"]
    metric_s = st.session_state[f"{k}_scale_metric"]
    scale_txt = price_s if price_s == metric_s else "Mixed"

    # Satu kolom per kotak kontrol; CSS membuat tiap kolom menyusut ke lebar isinya.
    cols = st.columns(8, vertical_alignment="bottom", gap="small")

    with cols[0]:
        with st.popover(f"Range\n\n**{_range_summary(family)}**"):
            # Judul kecil memakai st.caption seperti popover lain ("MVRV OSCILLATORS",
            # "AXIS"); label bawaan widget bentuknya berbeda sendiri.
            st.caption("PRESET")
            st.segmented_control("Preset", PRESETS, key=f"{k}_preset", on_change=on_preset,
                                 format_func=_preset_label, label_visibility="collapsed")
            # From dan To disejajarkan supaya popover tidak memanjang ke bawah.
            date_cols = st.columns(2, gap="small")
            with date_cols[0]:
                st.caption("FROM")
                st.date_input("From", min_value=dmin, max_value=dmax,
                              key=f"{k}_from", on_change=on_date,
                              label_visibility="collapsed")
            with date_cols[1]:
                st.caption("TO")
                st.date_input("To", min_value=dmin, max_value=dmax,
                              key=f"{k}_to", on_change=on_date,
                              label_visibility="collapsed")

    with cols[1]:
        with st.popover(f"Smoothing\n\n**{_smooth_summary(family)}**"):
            _render_smoothing(family)

    with cols[2]:
        with st.popover(f"Scale\n\n**{scale_txt}**"):
            st.caption(family.subtitle.upper())
            st.segmented_control("Metric scale", SCALE_MODES, key=f"{k}_scale_metric",
                                 on_change=_keep, args=(f"{k}_scale_metric", AUTO),
                                 label_visibility="collapsed")
            st.caption("BTC PRICE")
            st.segmented_control("BTC price scale", SCALE_MODES, key=f"{k}_scale_price",
                                 on_change=_keep, args=(f"{k}_scale_price", AUTO),
                                 label_visibility="collapsed")

    with cols[3]:
        with st.popover(f"BTC price\n\n**{st.session_state[f'{k}_btc']}**"):
            st.segmented_control("Display mode", BTC_MODES, key=f"{k}_btc",
                                 on_change=_on_btc_mode, args=(family,),
                                 label_visibility="collapsed")

    with cols[4]:
        # Kotak ini hanya muncul kalau keluarga metriknya memang punya seri pane tambahan.
        # Pane dibangun dari sisi Python, jadi saklarnya tidak bisa ikut legend yang
        # hidup di dalam chart.
        # Nama kotak diambil dari registry (extra_label), karena isi pane ini beda per halaman.
        if any(sr.pane == "extra" for sr in family.series):
            with st.popover(f"{family.extra_label}\n\n**{st.session_state[f'{k}_extra']}**"):
                st.caption("EXTRA PANE")
                st.segmented_control(f"{family.extra_label} pane", Z_MODES, key=f"{k}_extra",
                                     on_change=_keep, args=(f"{k}_extra", Z_HIDDEN),
                                     label_visibility="collapsed")
                st.caption("Own pane below the chart, always linear.")

    with cols[5]:
        with st.popover(f"Display\n\n**{_axis_summary(family)}**"):
            st.caption("CHART HEIGHT")
            st.segmented_control("Height", HEIGHTS, key=f"{k}_height",
                                 on_change=_keep, args=(f"{k}_height", 720),
                                 format_func=lambda h: f"{h}px",
                                 label_visibility="collapsed")
            st.caption("AXIS")
            # Nama di kiri, tombolnya di kanan pada baris yang sama. Bertumpuk ke bawah
            # membuat bagian ini tiga kali lebih tinggi daripada isinya, dan popover jadi
            # lebih tinggi daripada chart saat halaman punya banyak garis.
            for s in family.series:
                if s.pane == "extra":
                    continue   # pane tambahan punya sumbunya sendiri
                # segmented_control, bukan st.radio, supaya bentuknya sama dengan kontrol lain.
                _axis_control(s.label, f"{k}_axis_{s.col}", s.axis)
            # Harga BTC juga bisa dipindah sumbu. Berguna untuk halaman yang metriknya
            # sendiri berupa harga (Price Levels, AVIV): satu sumbu untuk semuanya.
            # Hanya berlaku saat harga digabung ke chart metrik; di Separate pane harga
            # punya pane sendiri, dan saat Hidden tidak ada yang diatur.
            overlay = st.session_state[f"{k}_btc"] == OVERLAY
            _axis_control("BTC Price", f"{k}_axis_btc", BTC_AXIS, disabled=not overlay)
            if not overlay:
                st.caption("Only for BTC price = Overlay.")

    with cols[6]:
        with st.popover(f"Line style\n\n**{_style_summary(family)}**"):
            _render_line_style(family)

    with cols[7]:
        with st.popover(f"Tooltip\n\n**{st.session_state[TIP_STORE]}**"):
            st.caption("TOOLTIP")
            st.segmented_control("Tooltip position", TIP_MODES, key=TIP_KEY,
                                 on_change=_on_tooltip,
                                 help="Fixed: top-left corner · Cursor: next to the cursor · "
                                      "Off: no box",
                                 label_visibility="collapsed")


def render_metric_page(family: MetricFamily):
    df_raw = family.loader()
    if df_raw.empty:
        st.error(f"Could not load data for {family.title}.")
        return

    dmin, dmax = data.date_bounds(df_raw)
    _init_state(family, dmin, dmax)
    # Gaya garis diberikan sebelum kontrol digambar, supaya nilai widget boleh ditulis.
    _assign_styles(family)
    k = family.key

    # Tanggal terakhir yang benar-benar punya nilai metrik, bukan sekadar baris tanggal.
    latest = df_raw.dropna(subset=[s.col for s in family.series if s.pane != "extra"],
                           how="all")['Date'].max()
    _render_header(family, latest)
    _render_controls(family, dmin, dmax)

    kind = st.session_state[f"{k}_smooth_kind"]
    periods = sorted(st.session_state[f"{k}_periods"])

    # Chart selalu menerima seluruh sejarah; kotak Range hanya menentukan rentang yang tampil
    # (pilihan B, 14 Sep 2026), supaya slider rentang di bawah chart berisi semua data dan
    # tombol Range cukup memindahkan jendelanya.
    date_from, date_to = st.session_state[f"{k}_from"], st.session_state[f"{k}_to"]
    df = data.apply_filters(
        df_raw, kind, periods, dmin, dmax,
        [s.col for s in family.series if s.smoothing],
    )
    view = df["Date_str"].between(f"{date_from:%Y-%m-%d}", f"{date_to:%Y-%m-%d}")
    if df.empty or not view.any():
        st.warning("No data in this date range.")
        return

    btc_mode = st.session_state[f"{k}_btc"]
    total_h = st.session_state[f"{k}_height"]
    price_mode = st.session_state[f"{k}_scale_price"]
    metric_mode = st.session_state[f"{k}_scale_metric"]

    # Semua garis dikirim ke chart; menyalakan dan mematikannya diurus legend di browser.
    plan = []
    extra = []
    pane_extra = st.session_state[f"{k}_extra"] == Z_BOTTOM
    for sr in family.series:
        if sr.pane == "extra":
            # Pane tambahan mati: serinya tidak dikirim sama sekali, bukan sekadar
            # disembunyikan — supaya sumbu pane metrik tidak ikut menghitungnya.
            if not pane_extra:
                continue
            extra.append(Line(sr.label, sr.col, sr.color, "left", width=LINE_WIDTH,
                              group=sr.group or sr.label, dim=sr.dim, kind=sr.kind,
                              short=sr.short, alpha=sr.alpha,
                              hidden_default=sr.hidden_default, precision=sr.precision,
                              whole_from=sr.whole_from))
            continue
        axis = st.session_state[f"{k}_axis_{sr.col}"]
        plan.append(Line(sr.label, sr.col, sr.color, axis, width=LINE_WIDTH,
                         group=sr.group or sr.label, dim=sr.dim, kind=sr.kind,
                         short=sr.short, alpha=sr.alpha, precision=sr.precision,
                         hidden_default=sr.hidden_default, whole_from=sr.whole_from,
                         complement_color=sr.complement_color))
        if not sr.smoothing:
            continue
        for p in periods:
            col = f"{sr.col}__{kind}{p}"
            if col in df.columns:
                # Nama "<metrik> <SMA|EMA>(<periode>)" dibaca tooltip untuk kolom periodenya.
                plan.append(Line(f"{sr.label} {kind}({p})", col, sr.color, axis,
                                 group=sr.label, dim=sr.dim, precision=sr.precision,
                                 whole_from=sr.whole_from, complement_color=sr.complement_color,
                                 **_smooth_style(family, p)))

    # Garis acuan mengikuti sumbu yang dipakai metrik, bukan dipaku ke satu sisi.
    used_axes = {ln.axis for ln in plan}
    ref_axis = METRIC_AXIS_DEFAULT if METRIC_AXIS_DEFAULT in used_axes or not used_axes         else next(iter(used_axes))
    for ref in family.reference_lines:
        ref_col = f"_ref_{ref.value}"
        df[ref_col] = ref.value
        # all_axes: satu garis di setiap sumbu yang memuat metrik (SOPR: LTH-SOPR di kanan).
        # Kiri didahulukan supaya urutannya tetap sama tiap render.
        axes = sorted(used_axes) if ref.all_axes and used_axes else [ref_axis]
        for axis in axes:
            # Garis acuan jadi seri pertama di sumbunya, dan lightweight-charts mengambil
            # format angka sumbu dari seri pertama itu. Precision-nya disamakan dengan metrik
            # di sumbu yang sama; kalau tidak, sumbu SOPR menulis 2 desimal (1.25, bukan 1.250).
            # Aturan tanpa-desimal (whole_from, LTH-SOPR) ikut juga, supaya sumbu kanan
            # menulis "1,200" dan bukan "1,200.000".
            metrik = [ln for ln in plan if ln.axis == axis and ln.group]
            presisi = max((ln.precision for ln in metrik), default=2)
            bulat = min((ln.whole_from for ln in metrik if ln.whole_from is not None),
                        default=None)
            plan.insert(0, Line(ref.label, ref_col, "rgba(255,255,255,0.35)",
                                axis, width=1, style=2, precision=presisi, whole_from=bulat))

    # Harga BTC tanpa desimal (78,905), di sumbu, label nilai terakhir, dan tooltip.
    price_line = None
    if btc_mode == PANE:
        price_line = Line("BTC Price", "BTC Price", BTC_COLOR, "right", width=LINE_WIDTH,
                          group="BTC Price", dim=BTC_DIM, precision=BTC_PRECISION)
    elif btc_mode == OVERLAY:
        # Sumbu harga bisa dipilih (bawaan: kanan). Sumbu yang hanya berisi harga memakai
        # skala harga; kalau harga berbagi sumbu dengan metrik, skala metrik yang dipakai.
        plan.append(Line("BTC Price", "BTC Price", BTC_COLOR,
                         st.session_state[f"{k}_axis_btc"], width=LINE_WIDTH,
                         group="BTC Price", dim=BTC_DIM, precision=BTC_PRECISION))

    charts.render(df, plan, price_line, extra, total_h, metric_mode, price_mode,
                  f"dash_v2_{k}", tooltip=st.session_state[TIP_STORE],
                  metric_range=family.metric_range, complement=family.complement,
                  view=(f"{date_from:%Y-%m-%d}", f"{date_to:%Y-%m-%d}"))
