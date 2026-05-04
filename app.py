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

# Initialize Session State for memory (so chart doesn't reset in Focus Mode)
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
# 3. MAIN DASHBOARD INTERFACE
# ==============================================================================
if not df.empty:
    # FOCUS MODE TOGGLE (Always visible)
    focus_mode = st.toggle("🔲 Focus Mode (Chart Only)")

    # If NOT in focus mode, render the full UI (Title, Filters, KPIs)
    if not focus_mode:
        st.title("Bitcoin On-Chain: STH Cost Basis 📊")
        st.markdown("Interactive dashboard to monitor short-term holder (STH) momentum and cost basis.")
        st.markdown("---")
        
        # FILTERS
        col_filter1, col_filter2 = st.columns([6, 1])
        time_options = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]
        
        with col_filter1:
            # Match current session state to keep selection active
            current_idx = time_options.index(st.session_state.time_range) if st.session_state.time_range in time_options else 5
            
            st.session_state.time_range = st.radio(
                "Time Range:",
                time_options,
                index=current_idx,
                horizontal=True
            )
        
        with col_filter2:
            # Show input box neatly right next to 'Custom'
            if st.session_state.time_range == "Custom":
                st.session_state.custom_days = st.number_input(
                    "Days back", 
                    min_value=7, 
                    value=st.session_state.custom_days,
                    label_visibility="collapsed" # This hides the text label above the box
                )

    # --------------------------------------------------------------------------
    # DATA FILTERING LOGIC (Runs invisibly even in Focus Mode)
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
    # KPI SCORECARDS (Only visible if NOT in Focus Mode)
    # --------------------------------------------------------------------------
    if not focus_mode:
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
        # Inject CSS to remove whitespace when in Focus Mode
        st.markdown("""<style>header {visibility: hidden;} footer {visibility: hidden;} .block-container {padding: 1rem 0rem; max-width: 100%;}</style>""", unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # LIGHTWEIGHT CHARTS RENDERING
    # --------------------------------------------------------------------------
    tinggi_chart = 700 if focus_mode else 450 # Chart expands automatically in Focus Mode

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
