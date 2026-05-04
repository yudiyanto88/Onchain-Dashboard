import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="Yudiyanto | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize Session State for memory
if 'time_range' not in st.session_state:
    st.session_state.time_range = "All Time"
if 'custom_days' not in st.session_state:
    st.session_state.custom_days = 120

# ==============================================================================
# 2. DATA LOADING (WITH CACHE)
# ==============================================================================
@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("Master_Onchain_Data.csv")
        df.rename(columns={
            'date': 'Date',
            'btc_price': 'BTC Price',
            'active_realized_price': 'STH Cost Basis'
        }, inplace=True)
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']) 
        df = df.sort_values('Date')
        return df
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

df = load_data()

# ==============================================================================
# 3. MAIN DASHBOARD INTERFACE & LAYOUT MANAGEMENT
# ==============================================================================
if not df.empty:
    header_kpi_container = st.container()
    controls_container = st.container()
    chart_container = st.container()

    # --------------------------------------------------------------------------
    # A. CONTROLS (Full Screen di kiri, Time Range di kanan)
    # --------------------------------------------------------------------------
    with controls_container:
        # Pembagian kolom: [Kiri, Kosong, Kanan (Radio), Kanan (Input Custom)]
        col_toggle, col_space, col_radio, col_custom = st.columns([2, 2, 7, 1.5], vertical_alignment="bottom")

        with col_toggle:
            focus_mode = st.toggle("🔲 Full Screen")

        with col_radio:
            time_options = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]
            current_idx = time_options.index(st.session_state.time_range) if st.session_state.time_range in time_options else 5
            
            st.session_state.time_range = st.radio(
                "Time Range:",
                time_options,
                index=current_idx,
                horizontal=True,
                label_visibility="collapsed" # Menyembunyikan teks agar sejajar
            )
        
        with col_custom:
            if st.session_state.time_range == "Custom":
                st.session_state.custom_days = st.number_input(
                    "Days back", 
                    min_value=7, 
                    value=st.session_state.custom_days,
                    label_visibility="collapsed" 
                )

        st.markdown("<br>", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # B. DATA FILTERING LOGIC
    # --------------------------------------------------------------------------
    tanggal_terakhir = df['Date'].max()
    opsi_waktu = st.session_state.time_range
    
    if opsi_waktu == "1 Month":
        tanggal_mulai = tanggal_terakhir - timedelta(days=30)
    elif opsi_waktu == "3 Months":
        tanggal_mulai = tanggal_terakhir - timedelta(days=90)
    elif opsi_waktu == "6 Months":
        tanggal_mulai = tanggal_terakhir - timedelta(days=180)
    elif opsi_waktu == "1 Year":
        tanggal_mulai = tanggal_terakhir - timedelta(days=365)
    elif opsi_waktu == "4 Years (Cycle)":
        tanggal_mulai = tanggal_terakhir - timedelta(days=365 * 4)
    elif opsi_waktu == "Custom":
        tanggal_mulai = tanggal_terakhir - timedelta(days=st.session_state.custom_days)
    else:
        tanggal_mulai = df['Date'].min()

    df_filter = df[df['Date'] >= tanggal_mulai].copy()
    df_filter['Date_str'] = df_filter['Date'].dt.strftime('%Y-%m-%d')

    # --------------------------------------------------------------------------
    # C. HEADERS & KPI SCORECARDS
    # --------------------------------------------------------------------------
    with header_kpi_container:
        if not focus_mode:
            st.title("Bitcoin On-Chain: STH Cost Basis 📊")
            st.markdown("Interactive dashboard to monitor short-term holder (STH) momentum and cost basis.")
            st.markdown("---")

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
        else:
            st.markdown("""<style>.block-container {padding-top: 1rem; padding-bottom: 1rem; max-width: 100%;} header {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # D. LIGHTWEIGHT CHARTS RENDERING
    # --------------------------------------------------------------------------
    with chart_container:
        tinggi_chart = 700 if focus_mode else 450 

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
    st.error("⚠️ Waiting for automated data...")
