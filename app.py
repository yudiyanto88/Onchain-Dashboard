import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

st.set_page_config(page_title="MoneyBag Journal | On-Chain Dashboard", layout="wide")

st.title("Bitcoin On-Chain: STH Cost Basis 📊")
st.markdown("Dasbor interaktif untuk memantau momentum dan basis biaya pemegang jangka pendek (STH).")

# SISTEM CACHE DIMATIKAN AGAR MEMBACA DATA FRESH
def load_data():
    try:
        df = pd.read_csv("Master_Onchain_Data.csv")
        
        # 1. TAMPILKAN TABEL MENTAH KE LAYAR UNTUK TESTING
        st.markdown("### 🔍 Mengintip Isi File CSV:")
        st.dataframe(df.tail()) # Menampilkan 5 baris data paling bawah
        
        # 2. PROSES UBAH NAMA KOLOM
        df.rename(columns={
            'date': 'Date',
            'btc_price': 'BTC Price',
            'active_realized_price': 'STH Cost Basis'
        }, inplace=True)
        
        # 3. PASTIKAN FORMAT TANGGAL BENAR
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']) 
        df = df.sort_values('Date')
        return df
        
    except Exception as e:
        st.error(f"Terjadi masalah saat membaca CSV: {e}")
        return pd.DataFrame()

df = load_data()

# ==============================================================================
# JIKA DATA ADA, TAMPILKAN GRAFIK. JIKA KOSONG, TAMPILKAN PERINGATAN.
# ==============================================================================
if not df.empty:
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
        tanggal_mulai = df['Date'].min()

    df_filter = df[df['Date'] >= tanggal_mulai].copy()
    df_filter['Date_str'] = df_filter['Date'].dt.strftime('%Y-%m-%d')

    baris_terakhir = df_filter.iloc[-1]
    harga_sekarang = baris_terakhir.get('BTC Price', 0)
    harga_sth = baris_terakhir.get('STH Cost Basis', 0)
    
    if pd.isna(harga_sth) or harga_sth == 0:
        margin_persen = 0
    else:
        margin_persen = ((harga_sekarang - harga_sth) / harga_sth) * 100

    col_kpi1, col_kpi2, col_kpi3 = st.columns(3)
    col_kpi1.metric("Current BTC Price", f"${harga_sekarang:,.2f}")
    col_kpi2.metric("STH Cost Basis", f"${harga_sth:,.2f}")
    col_kpi3.metric("Margin (Profit/Loss vs STH)", f"{margin_persen:,.2f}%", delta=f"{margin_persen:,.2f}%")
    st.markdown("---")

    mode_penuh = st.toggle("🔲 Mode Layar Penuh (Tekan F11)")
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

    def ambil_data_series(nama_kolom):
        if nama_kolom in df_filter.columns:
            temp = df_filter[['Date_str', nama_kolom]].rename(columns={'Date_str': 'time', nama_kolom: 'value'})
            return temp.dropna().to_dict('records')
        return []

    panel_utama = [
        {"type": 'Line', "data": ambil_data_series('BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}},
        {"type": 'Line', "data": ambil_data_series('STH Cost Basis'), "options": {"color": '#ffffff', "lineWidth": 2, "title": 'STH Cost Basis'}}
    ]

    renderLightweightCharts([{"chart": pengaturan_dasar, "series": panel_utama}], 'onchain_chart')

else:
    st.error("⚠️ Proses terhenti: Tabel CSV terbaca, tapi tidak ada baris datanya (kosong).")
