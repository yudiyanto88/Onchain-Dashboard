import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PENGATURAN HALAMAN UTAMA
# ==============================================================================
st.set_page_config(
    page_title="MoneyBag Journal | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Bitcoin On-Chain: STH Cost Basis 📊")
st.markdown("Dasbor interaktif untuk memantau momentum dan basis biaya pemegang jangka pendek (STH).")

# ==============================================================================
# 2. FUNGSI MEMBACA DATA (DARI CSV HASIL AUTOMASI)
# ==============================================================================
@st.cache_data(ttl=3600) # Data di-cache selama 1 jam agar web sangat cepat
def load_data():
    try:
        df = pd.read_csv("Master_Onchain_Data.csv")
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        return df
    except Exception as e:
        st.error("Data belum tersedia. Menunggu proses automasi GitHub Actions.")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # ==============================================================================
    # 3. FITUR: FILTER RENTANG WAKTU
    # ==============================================================================
    st.markdown("---")
    col_filter1, col_filter2 = st.columns([3, 1])
    
    with col_filter1:
        opsi_waktu = st.radio(
            "Pilih Rentang Waktu:",
            ["1 Bulan", "3 Bulan", "6 Bulan", "1 Tahun", "4 Tahun (Siklus)", "All Time", "Custom"],
            horizontal=True
        )
    
    with col_filter2:
        hari_kustom = 0
        if opsi_waktu == "Custom":
            hari_kustom = st.number_input("Masukkan jumlah hari ke belakang:", min_value=7, value=120)

    # Logika pemotongan data berdasarkan waktu
    tanggal_terakhir = df['Date'].max()
    
    if opsi_waktu == "1 Bulan":
        tanggal_mulai = tanggal_terakhir - timedelta(days=30)
    elif opsi_waktu == "3 Bulan":
        tanggal_mulai = tanggal_terakhir - timedelta(days=90)
    elif opsi_waktu == "6 Bulan":
        tanggal_mulai = tanggal_terakhir - timedelta(days=180)
    elif opsi_waktu == "1 Tahun":
        tanggal_mulai = tanggal_terakhir - timedelta(days=365)
    elif opsi_waktu == "4 Tahun (Siklus)":
        tanggal_mulai = tanggal_terakhir - timedelta(days=365 * 4)
    elif opsi_waktu == "Custom":
        tanggal_mulai = tanggal_terakhir - timedelta(days=hari_kustom)
    else:
        tanggal_mulai = df['Date'].min() # All Time

    # Data yang sudah difilter siap digunakan
    df_filter = df[df['Date'] >= tanggal_mulai].copy()
    df_filter['Date_str'] = df_filter['Date'].dt.strftime('%Y-%m-%d')

    # ==============================================================================
    # 4. FITUR: PAPAN SKOR (KPI SCORECARDS)
    # ==============================================================================
    baris_terakhir = df_filter.iloc[-1]
    
    # Membaca nilai metrik (Gunakan .get() agar tidak error jika nama kolom sedikit berbeda)
    harga_sekarang = baris_terakhir.get('BTC Price', 0)
    harga_sth = baris_terakhir.get('STH Cost Basis', 0)
    
    # Hitung selisih/margin persentase
    if harga_sth > 0:
        margin_persen = ((harga_sekarang - harga_sth) / harga_sth) * 100
    else:
        margin_persen = 0

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Current BTC Price", f"${harga_sekarang:,.2f}")
    col_kpi2.metric("STH Cost Basis", f"${harga_sth:,.2f}")
    
    # Warna hijau jika harga di atas STH, merah jika di bawah (otomatis dari Streamlit)
    col_kpi3.metric("Margin (Profit/Loss vs STH)", f"{margin_persen:,.2f}%", delta=f"{margin_persen:,.2f}%")
    st.markdown("---")

    # ==============================================================================
    # 5. PENGATURAN GRAFIK (LIGHTWEIGHT CHARTS)
    # ==============================================================================
    # Toggle Fullscreen
    mode_penuh = st.toggle("🔲 Mode Layar Penuh (Tekan F11 setelah aktif)")
    if mode_penuh:
        st.markdown("""<style>header {visibility: hidden;} footer {visibility: hidden;} .block-container {padding: 1rem 0rem; max-width: 100%;}</style>""", unsafe_allow_html=True)
        tinggi_chart = 650
    else:
        tinggi_chart = 450

    pengaturan_dasar = {
        "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}},
        "grid": {"vertLines": {"color": "rgba(42, 46, 57, 0.3)"}, "horzLines": {"color": "rgba(42, 46, 57, 0.3)"}},
        "crosshair": {"mode": 0},
        "timeScale": {"rightOffset": 5},
        "height": tinggi_chart
    }

    # Fungsi pembantu untuk ekstrak kolom ke format chart
    def ambil_data_series(nama_kolom):
        if nama_kolom in df_filter.columns:
            temp = df_filter[['Date_str', nama_kolom]].rename(columns={'Date_str': 'time', nama_kolom: 'value'})
            return temp.dropna().to_dict('records')
        return []

    # Fitur Pinned Legend diaktifkan dengan memasukkan parameter "title" di setiap opsi
    panel_utama = [
        {"type": 'Line', "data": ambil_data_series('BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}},
        {"type": 'Line', "data": ambil_data_series('STH Cost Basis'), "options": {"color": '#ffffff', "lineWidth": 2, "title": 'STH Cost Basis'}}
    ]

    # Tambahkan pita deviasi (jika datanya ada di CSV)
    pita_tambahan = [
        ('Overheated Band (Red)', '#ef5350'), 
        ('Heated Band', '#ff7043'), 
        ('Cooled Band (Blue)', '#2962ff')
    ]
    
    for nama_pita, warna in pita_tambahan:
        data_pita = ambil_data_series(nama_pita)
        if data_pita:
            panel_utama.append({
                "type": 'Line', 
                "data": data_pita, 
                "options": {"color": warna, "lineWidth": 1, "lineStyle": 2, "title": nama_pita.split(' ')[0]} # Ambil kata pertama saja untuk legend
            })

    # Render grafik
    renderLightweightCharts([{"chart": pengaturan_dasar, "series": panel_utama}], 'onchain_chart')
