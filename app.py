"""Dashboard v2 — satu halaman per keluarga metrik (lihat dashboard/registry.py).

Menggantikan dashboard v1 sejak 13 Sep 2026; v1 diarsipkan di archive/app_v1.py.
Jalankan dengan (tema teal gelap dari .streamlit/config.toml):
    streamlit run app.py
"""
import streamlit as st

from dashboard.metric_page import render_metric_page
from dashboard.registry import FAMILIES

st.set_page_config(
    page_title="On-Chain Dashboard v2",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
section[data-testid="stSidebar"] { background-color: #151924; }
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] { gap: 10px; }
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label {
    background-color: #1a1d24; padding: 12px 16px !important; border-radius: 8px !important;
    border-left: 4px solid transparent; margin: 0 !important; cursor: pointer;
    transition: all 0.2s ease-in-out;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label:hover {
    background-color: #262a35;
}
/* Streamlit 1.63 menandai opsi terpilih dengan data-selected (dulu data-checked).
   Teal gelap #006d77 warna utama dashboard: garis tepi teal, latar teal 25% di atas sidebar. */
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label[data-selected="true"] {
    border-left: 4px solid #006d77 !important; background-color: #102e39 !important;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] p {
    font-size: 1.15rem !important; font-weight: 600 !important;
    margin: 0 !important; color: #ffffff !important;
}
/* Bulatan radio disembunyikan. Di 1.63 bulatan itu saudara teks menu, bukan anak pertama label. */
section[data-testid="stSidebar"] div.stRadio label div:has(> [data-testid="stMarkdownContainer"]) > div:not([data-testid]) {
    display: none !important;
}

div[data-testid="stSelectbox"] *, div[data-testid="stRadio"] *,
div[data-testid="stToggle"] *, div[data-testid="stNumberInput"] *,
div[data-testid="stDateInput"] * { font-size: 0.85rem !important; }

div[data-baseweb="select"] > div, div[data-testid="stDateInput"] input {
    min-height: 32px !important; height: 32px !important; border-radius: 6px !important;
}

/* Kontrol bergaya ChartInspect: judul kecil menempel di garis atas kotak,
   nilai tebal di dalam. Lebar kotak mengikuti isinya ("50d" sempit, "50d and 1 more" lebar). */
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPopover"]) {
    gap: 8px !important; flex-wrap: wrap !important; padding-top: 9px !important;
}
div[data-testid="stHorizontalBlock"]:has(div[data-testid="stPopover"]) > div[data-testid="stColumn"] {
    width: auto !important; flex: 0 0 auto !important;
    min-width: 0 !important; padding: 0 !important; overflow: visible !important;
}
div[data-testid="stPopover"], div[data-testid="stPopover"] * { overflow: visible !important; }
div[data-testid="stPopover"] { width: auto !important; }

button[data-testid="stPopoverButton"] {
    position: relative !important; width: auto !important; white-space: nowrap !important;
    padding: 8px 10px 5px 12px !important; min-height: 38px !important;
    border-radius: 8px !important; background-color: transparent !important;
    border: 1px solid #2a2e39 !important; text-align: left !important; line-height: 1.15 !important;
}
button[data-testid="stPopoverButton"]:hover { border-color: #3a4152 !important; }
button[data-testid="stPopoverButton"][aria-expanded="true"] {
    border-color: #006d77 !important; background-color: rgba(0, 109, 119, 0.40) !important;
}
button[data-testid="stPopoverButton"] p { margin: 0 !important; white-space: nowrap !important; }

/* Judul: tab kecil yang duduk di atas garis kotak, ditebalkan supaya mudah dibaca.
   Tab tetap ikut aliran layout (bukan absolute) supaya kotak minimal selebar judulnya.
   Kalau absolute, judul panjang di atas nilai pendek ("Smoothing" di atas "Off")
   menabrak judul kotak sebelahnya. top menggeser tab ke garis atas, margin bawah
   negatif menarik nilai naik ke posisi semula. */
button[data-testid="stPopoverButton"] div[data-testid="stMarkdownContainer"] p:first-child {
    position: relative !important; top: -17px; width: fit-content;
    display: block !important;   /* p di tombol 1.63 bawaannya inline: nilai ikut duduk di sebelah judul */
    margin: 0 0 -18px -4px !important;
    font-size: 10.5px !important; font-weight: 600 !important; color: #c9d1d9 !important;
    background: #0e1117; padding: 0 6px !important; line-height: 16px !important;
    border: 1px solid #2a2e39; border-radius: 5px; letter-spacing: 0.01em;
}
button[data-testid="stPopoverButton"][aria-expanded="true"] div[data-testid="stMarkdownContainer"] p:first-child {
    border-color: #006d77; color: #ffffff !important;
}
button[data-testid="stPopoverButton"] p strong {
    font-size: 13px !important; font-weight: 600 !important; color: #ffffff !important;
}

/* Judul di dalam popover smoothing: nama di kiri, ringkasan nilai di kanan. */
.pop-head {
    display: flex; justify-content: space-between; align-items: baseline; gap: 14px;
    margin-bottom: 8px; font-size: 0.72rem; letter-spacing: 0.06em;
    text-transform: uppercase; color: #8b90a0;
}
.pop-head > span:first-child { flex: 0 0 auto; }
.pop-head .pop-val {
    color: #c9d1d9; font-weight: 700; text-transform: none; letter-spacing: 0;
    flex: 0 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
}

/* Kisi periode 3x3. Isi popover dirender di portal terpisah, jadi tombolnya
   tidak bisa dijangkau lewat div[data-testid="stPopover"]. Satu-satunya
   st.button di halaman ini memang tombol-tombol kisi tersebut. */
/* Tinggi 26 px, sama dengan segmented control: Streamlit memaku tombol di 32 px, jadi
   height harus ditimpa langsung (min-height dan padding tidak mempan). */
div[data-testid="stButton"] button {
    background: transparent !important; border: 1px solid #232838 !important;
    color: #c9d1d9 !important; font-weight: 600 !important;   /* abu terang, sama dengan judul kecil tombol */
    padding: 3px 6px !important; height: 26px !important; min-height: 0 !important;
    line-height: 1.25 !important;
    white-space: nowrap !important; border-radius: 6px !important;
    display: flex !important; align-items: center !important; justify-content: center !important;
}
/* Tulisan tombol ini jatuh ~2,3 px di bawah garis tengah kotak, sementara semua
   segmented control duduk 0,5 px di atasnya — terlihat begitu kisi periode berjajar.
   Sebabnya: Streamlit memasang teksnya sebagai baris "inline" di dalam kotak baris yang
   lebih tinggi daripada hurufnya, jadi huruf duduk di garis dasar, bukan di tengah.
   Dijadikan blok dengan tinggi baris sepadan supaya ikut ditengahkan seperti yang lain. */
div[data-testid="stButton"] button p {
    margin: 0 !important; display: block !important; line-height: 1.25 !important;
    font-size: 0.82rem !important; white-space: nowrap !important;
}
div[data-testid="stButton"] button:hover {
    background: #1e2330 !important; border-color: #2a3550 !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: rgba(0, 109, 119, 0.40) !important; color: #ffffff !important;
    border-color: #006d77 !important;
}

/* Pilihan terpilih di segmented control (SMA/EMA, Auto/Linear/Log, Overlay/...):
   latar teal gelap 40% + garis tepi teal, menggantikan merah bawaan Streamlit. */
[data-testid="stButtonGroup"] button[role="radio"][aria-checked="true"] {
    background: rgba(0, 109, 119, 0.40) !important; border-color: #006d77 !important;
    color: #ffffff !important;
}
[data-testid="stButtonGroup"] button[role="radio"][aria-checked="true"] * { color: #ffffff !important; }

/* Kotak tanggal: latar abu bawaan Streamlit diganti garis tipis, senada dengan
   kontrol lain. accent-color mengatur warna kalender bawaan browser, yang sebelumnya
   memakai warna aksen sistem (merah). */
div[data-testid="stDateInputField"] {
    background: transparent !important; border: 1px solid #2a2e39 !important;
    border-radius: 6px !important;
    /* Sepadan dengan tombol 26 px di atasnya; sebelumnya 40 px dan kelihatan jauh
       lebih besar daripada kontrol lain di popover yang sama. */
    min-height: 0 !important; height: 28px !important;
}
div[data-testid="stDateInputField"]:hover { border-color: #3a4152 !important; }
div[data-testid="stDateInputField"]:focus-within { border-color: #006d77 !important; }
/* Isinya ditengahkan supaya sebaris dengan tombol-tombol di sekitarnya, yang semua
   tulisannya di tengah kotak. */
div[data-testid="stDateInput"] input { accent-color: #006d77 !important; text-align: center !important; }
div[data-testid="stDateInput"] input::selection { background: rgba(0, 109, 119, 0.40) !important; }

/* Slider tebal garis. Warna kenop dan isian track ikut warna utama tema
   (dijalankan dengan --theme.primaryColor teal); kenop tetap dipaksa teal sebagai cadangan. */
div[data-testid="stSlider"] div:has(> div > input[type="range"]) {
    background-color: #006d77 !important;
}

/* Garis fokus: Streamlit memakai bayangan merah di elemen yang sedang dipilih. */
[data-testid="stButtonGroup"] button:focus-visible,
[data-testid="stButtonGroup"] button[data-focus-visible],
div[data-testid="stButton"] button:focus-visible,
button[data-testid="stPopoverButton"]:focus-visible,
[data-testid="stRadioOption"]:focus-visible,
div[data-testid="stSlider"] div[data-focus-visible] {
    box-shadow: 0 0 0 0.2rem rgba(0, 109, 119, 0.5) !important;
}

/* Isi popover dirapatkan: padding, jarak antar-baris, judul kecil, dan tombol
   yang lebih pendek. Berlaku untuk semua popover kontrol, bukan hanya Line style. */
[data-testid="stPopoverBody"] { padding: 12px 14px !important; min-width: 0 !important; }
[data-testid="stPopoverBody"] div[data-testid="stVerticalBlock"] { gap: 0.3rem !important; }

/* Judul kecil di dalam popover ("AXIS", "BTC PRICE", nama metrik). Streamlit memberi
   margin bawah minus 16px, yang membuat wadahnya lebih pendek dari tulisannya sehingga
   tertimpa kotak tombol di bawahnya. */
[data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] { margin-bottom: 0 !important; }
[data-testid="stPopoverBody"] [data-testid="stCaptionContainer"] p {
    font-size: 11px !important; line-height: 1.35 !important;
    margin: 6px 0 2px !important; letter-spacing: 0.04em;
}
/* Streamlit memaku tinggi tombol di 32 px padahal tulisannya cuma 15 px, jadi min-height
   maupun padding tidak bisa mengecilkannya — tingginya harus ditimpa langsung.
   26 px = 15 px tulisan + 6 px jarak dalam + 2 px garis tepi, masih nyaman diklik. */
[data-testid="stButtonGroup"] button {
    height: 26px !important; min-height: 0 !important; padding: 3px 8px !important;
    line-height: 1.25 !important;
}
[data-testid="stButtonGroup"] button p { font-size: 12px !important; line-height: 1.25 !important; }
/* Lambang gaya garis ditulis sebagai kode supaya memakai huruf monospace dan semua
   lambang selebar sama. Kotak abu bawaan kode dihilangkan, warnanya ikut tombol. */
[data-testid="stButtonGroup"] button code {
    background: transparent !important; padding: 0 !important; border: 0 !important;
    color: inherit !important; font-size: 13px !important; letter-spacing: 0 !important;
}

/* Slider: angka ikut bergerak bersama kenop (label bawaan Streamlit), dengan satuan px
   ditambahkan lewat CSS. Batas bawah dan atas tetap ditampilkan kecil di bawah track. */
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] {
    font-size: 11px !important; font-weight: 600 !important; color: #ffffff !important;
    white-space: nowrap !important;
}
[data-testid="stSlider"] [data-testid="stSliderThumbValue"] p::after { content: "px"; }
[data-testid="stSlider"] [data-testid="stSliderTickBar"] { font-size: 10px !important; }
[data-testid="stSlider"] { padding: 0 6px 0 2px !important; }

/* Input periode dibuat sempit agar sebaris dengan tombol Add. */
div[data-testid="stNumberInput"] input {
    height: 30px !important; font-size: 0.82rem !important; padding: 0 8px !important;
}
div[data-testid="stNumberInput"] button { display: none !important; }

/* Saat browser benar-benar fullscreen, kerangka Streamlit disembunyikan
   supaya chart memakai seluruh layar tanpa perlu menekan F11. */
:fullscreen header[data-testid="stHeader"],
:fullscreen div[data-testid="stToolbar"],
:fullscreen div[data-testid="stDecoration"] { display: none !important; }
:fullscreen section[data-testid="stSidebar"] { display: none !important; }
/* Layar penuh: jarak kiri-kanan bawaan Streamlit (5rem = 80 px per sisi) dipangkas
   jadi 1rem, dan judul halaman disembunyikan supaya baris tombol naik ke atas dan
   chart mendapat ruang lebih. Isi dan desain chart tidak berubah. */
:fullscreen .block-container {
    padding-top: 0.6rem !important; padding-bottom: 0.3rem !important;
    padding-left: 1rem !important; padding-right: 1rem !important;
    max-width: 100% !important;
}
:fullscreen div[data-testid="stElementContainer"]:has(.page-title) { display: none !important; }

/* Header Streamlit melayang di atas konten. Dengan padding dipangkas, judul ikut
   tertutup. Header hanya berisi tombol Deploy dan menu, jadi disembunyikan. */
header[data-testid="stHeader"] { display: none !important; }

/* Ruang di atas chart dipangkas: padding, jarak antar-baris, dan garis pemisah. */
.block-container {
    padding-top: 0.6rem !important; padding-bottom: 0.3rem !important; max-width: 100%;
}
.block-container hr { margin: 6px 0 !important; }
div[data-testid="stVerticalBlock"] { gap: 0.35rem !important; }
div[data-testid="stElementContainer"]:has(> div[data-testid="stMarkdown"]) { margin-bottom: 0 !important; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("<h1 style='text-align:center;color:#ffffff;font-size:2.2rem;'>Yudiyanto</h1>",
                unsafe_allow_html=True)
    # Tulisan memakai teal terang #2aa6b0 (hue sama dengan #006d77): teal gelap sebagai
    # warna huruf cuma 2.9:1 di latar sidebar, teal terang 6.0:1.
    st.markdown("<h3 style='text-align:center;color:#2aa6b0;font-weight:800;font-size:1.3rem;"
                "margin-top:-15px;'>ON-CHAIN DASHBOARD v2</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    selected = st.radio("Menu", list(FAMILIES), label_visibility="collapsed")

render_metric_page(FAMILIES[selected])


# Tombol layar penuh hidup di dalam chart (dashboard/lw_chart.py), bukan di sini.
# Kliknya sudah merupakan gestur pengguna, jadi requestFullscreen() bisa dipanggil
# langsung dan tidak perlu skrip penyisip yang memasang pendengar ke tombol Streamlit.
# Yang tersisa di file ini cuma aturan :fullscreen di atas, yang menyembunyikan
# kerangka Streamlit saat browser benar-benar masuk layar penuh.
