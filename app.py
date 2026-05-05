import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PAGE CONFIGURATION & SESSION STATE
# ==============================================================================
st.set_page_config(
    page_title="Yudiyanto | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

if 'time_range' not in st.session_state:
    st.session_state.time_range = "All Time"
if 'custom_days' not in st.session_state:
    st.session_state.custom_days = 120
if 'smooth_period' not in st.session_state:
    st.session_state.smooth_period = "0d"
if 'custom_smooth' not in st.session_state:
    st.session_state.custom_smooth = 50

# ==============================================================================
# 2. DATA LOADING (DARI CSV)
# ==============================================================================
@st.cache_data(ttl=3600)
def load_data():
    try:
        df = pd.read_csv("data_price_level.csv")
        df.rename(columns={
            'date': 'Date',
            'btc_price': 'BTC Price',
            'sth_cost_basis': 'STH Cost Basis',
            'lth_cost_basis': 'LTH Cost Basis',
            'realized_price': 'Realized Price',
            'cvdd': 'CVDD',
            'true_market_mean_price': 'True Market Mean'
        }, inplace=True)
        
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']) 
        df = df.sort_values('Date')
        return df
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return pd.DataFrame()

df_raw = load_data()

# ==============================================================================
# 3. TOP TABS NAVIGATION
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["Price Levels", "Momentum (Soon)", "Oscillators (Soon)"])

# ------------------------------------------------------------------------------
# TAB 1: ON-CHAIN PRICE LEVELS
# ------------------------------------------------------------------------------
with tab1:
    if not df_raw.empty:
        df = df_raw.copy()
        
        header_container = st.container()
        controls_container = st.container()
        chart_container = st.container()

        # --- A. KONTROL (FULL SCREEN, SMOOTHING, METRIC TOGGLE, TIME RANGE) ---
        with controls_container:
            # Mengatur proporsi lebar kolom kontrol
            col_toggle, col_smooth, col_metrics, col_space, col_radio, col_custom = st.columns([1.5, 1.5, 3.5, 0.5, 5, 1.5], vertical_alignment="bottom")
            
            with col_toggle:
                focus_mode = st.toggle("Full Screen")
                
            with col_smooth:
                with st.popover("Smoothing (SMA)"):
                    st.markdown("**Select Smoothing Period:**")
                    st.session_state.smooth_period = st.radio(
                        "Period", 
                        ["0d", "7d", "14d", "30d", "Custom"], 
                        index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.smooth_period),
                        horizontal=True,
                        label_visibility="collapsed"
                    )
                    if st.session_state.smooth_period == "Custom":
                        st.session_state.custom_smooth = st.number_input("Days", min_value=1, value=st.session_state.custom_smooth)
            
            with col_metrics:
                # Multiselect untuk mematikan/menyalakan metrik di chart
                active_metrics = st.multiselect(
                    "Show Metrics:",
                    ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'],
                    default=['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'],
                    label_visibility="collapsed",
                    placeholder="Pilih metrik yang ditampilkan..."
                )

            with col_radio:
                time_options = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]
                current_idx = time_options.index(st.session_state.time_range) if st.session_state.time_range in time_options else 5
                
                st.session_state.time_range = st.radio("Time Range:", time_options, index=current_idx, horizontal=True, label_visibility="collapsed")
            
            with col_custom:
                if st.session_state.time_range == "Custom":
                    st.session_state.custom_days = st.number_input("Days back", min_value=7, value=st.session_state.custom_days, label_visibility="collapsed")
                    
            st.markdown("<br>", unsafe_allow_html=True)
        
        # --- B. KALKULASI SMA SMOOTHING ---
        window = 1
        if st.session_state.smooth_period == "7d": window = 7
        elif st.session_state.smooth_period == "14d": window = 14
        elif st.session_state.smooth_period == "30d": window = 30
        elif st.session_state.smooth_period == "Custom": window = st.session_state.custom_smooth
        
        if window > 1:
            metrics_to_smooth = ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD']
            for col in metrics_to_smooth:
                if col in df.columns:
                    df[col] = df[col].rolling(window=window, min_periods=1).mean()

        # --- C. FILTER WAKTU ---
        tanggal_terakhir = df['Date'].max()
        opsi_waktu = st.session_state.time_range
        
        if opsi_waktu == "1 Month": tanggal_mulai = tanggal_terakhir - timedelta(days=30)
        elif opsi_waktu == "3 Months": tanggal_mulai = tanggal_terakhir - timedelta(days=90)
        elif opsi_waktu == "6 Months": tanggal_mulai = tanggal_terakhir - timedelta(days=180)
        elif opsi_waktu == "1 Year": tanggal_mulai = tanggal_terakhir - timedelta(days=365)
        elif opsi_waktu == "4 Years (Cycle)": tanggal_mulai = tanggal_terakhir - timedelta(days=365 * 4)
        elif opsi_waktu == "Custom": tanggal_mulai = tanggal_terakhir - timedelta(days=st.session_state.custom_days)
        else: tanggal_mulai = df['Date'].min()

        df_filter = df[df['Date'] >= tanggal_mulai].copy()
        df_filter['Date_str'] = df_filter['Date'].dt.strftime('%Y-%m-%d')

        # --- D. HEADERS & KPI ---
        with header_container:
            if not focus_mode:
                st.title("On-Chain Price Levels")
                st.markdown("Bitcoin's current market price alongside fundamental price levels derived from on-chain metrics.")
                st.markdown("---")

                baris_terakhir = df_filter.iloc[-1]
                btc_price = baris_terakhir.get('BTC Price', 0)
                sth_cb = baris_terakhir.get('STH Cost Basis', 0)
                lth_cb = baris_terakhir.get('LTH Cost Basis', 0)
                realized = baris_terakhir.get('Realized Price', 0)
                tmm = baris_terakhir.get('True Market Mean', 0)
                
                # Fungsi penghitung selisih persentase vs BTC Price
                def hitung_delta(nilai_metrik):
                    if pd.isna(nilai_metrik) or nilai_metrik == 0 or btc_price == 0:
                        return 0
                    return ((nilai_metrik - btc_price) / btc_price) * 100
                
                col_kpi1, col_kpi2, col_kpi3, col_kpi4, col_kpi5 = st.columns(5)
                col_kpi1.metric("Current BTC Price", f"${btc_price:,.2f}")
                col_kpi2.metric("STH Cost Basis", f"${sth_cb:,.2f}", f"{hitung_delta(sth_cb):,.2f}%")
                col_kpi3.metric("LTH Cost Basis", f"${lth_cb:,.2f}", f"{hitung_delta(lth_cb):,.2f}%")
                col_kpi4.metric("Realized Price", f"${realized:,.2f}", f"{hitung_delta(realized):,.2f}%")
                col_kpi5.metric("True Market Mean", f"${tmm:,.2f}", f"{hitung_delta(tmm):,.2f}%")
                st.markdown("---")
            else:
                st.markdown("""<style>.block-container {padding-top: 1rem; padding-bottom: 1rem; max-width: 100%;} header {visibility: hidden;} footer {visibility: hidden;}</style>""", unsafe_allow_html=True)

        # --- E. LIGHTWEIGHT CHARTS (MULTI-LINE) ---
        with chart_container:
            # Tinggi ditambah signifikan agar lebih nyaman untuk visualisasi data berlapis
            tinggi_chart = 850 if focus_mode else 650 

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

            # Harga BTC selalu ditampilkan sebagai dasar
            panel_utama = [
                {"type": 'Line', "data": ambil_data_series('BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}}
            ]
            
            # Memetakan warna unik untuk masing-masing metrik
            warna_metrik = {
                'STH Cost Basis': '#ff4d4d',
                'LTH Cost Basis': '#4da6ff',
                'Realized Price': '#ffffff',
                'True Market Mean': '#cc33ff',
                'CVDD': '#00cc66'
            }
            
            # Hanya memasukkan garis ke dalam chart jika metrik dipilih pada filter dropdown
            for metrik in active_metrics:
                if metrik in warna_metrik:
                    panel_utama.append({
                        "type": 'Line', 
                        "data": ambil_data_series(metrik), 
                        "options": {"color": warna_metrik[metrik], "lineWidth": 2, "title": metrik}
                    })

            renderLightweightCharts([{"chart": pengaturan_dasar, "series": panel_utama}], 'onchain_price_levels')

    else:
        st.error("Menunggu data automasi. Pastikan GitHub Actions sudah berhasil membuat data_price_level.csv!")

# ------------------------------------------------------------------------------
# TAB 2 & 3: TEMPAT UNTUK METRIK BERIKUTNYA
# ------------------------------------------------------------------------------
with tab2:
    st.info("Momentum chart is under construction. Coming soon!")
    
with tab3:
    st.info("Oscillators chart is under construction. Coming soon!")
