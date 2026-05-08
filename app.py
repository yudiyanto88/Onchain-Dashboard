import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PAGE CONFIGURATION, SESSION STATE & CSS
# ==============================================================================
st.set_page_config(
    page_title="Yudiyanto | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- SUNTIKAN CSS KHUSUS UNTUK TOMBOL METRIK (SHINY TECH & STRIKETHROUGH) ---
st.markdown("""
<style>
/* Kondisi Tombol OFF (Mati, Abu-abu, Tercoret, Transparan) */
div[data-testid="stPill"] button {
    background-color: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #666666 !important;
    text-decoration: line-through !important;
    transition: all 0.3s ease;
}
/* Kondisi Tombol ON (Menyala, Putih, Gradasi Ungu, Garis Glowing) */
div[data-testid="stPill"] button[data-selected="true"], 
div[data-testid="stPill"] button[aria-pressed="true"] {
    background: linear-gradient(135deg, rgba(60, 20, 100, 0.8), rgba(20, 0, 50, 0.6)) !important;
    border: 1px solid #a855f7 !important;
    box-shadow: 0 0 8px rgba(168, 85, 247, 0.6) !important;
    color: #ffffff !important;
    text-decoration: none !important;
}
/* Menyembunyikan elemen header & footer saat Full Screen */
.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
</style>
""", unsafe_allow_html=True)

# Inisialisasi State Independen untuk masing-masing Tab/Chart
if 'tr_p' not in st.session_state: st.session_state.tr_p = "All Time"
if 'cd_p' not in st.session_state: st.session_state.cd_p = 120
if 'tf_p' not in st.session_state: st.session_state.tf_p = "Daily"
if 'sma_p' not in st.session_state: st.session_state.sma_p = "0d"
if 'cs_p' not in st.session_state: st.session_state.cs_p = 50

# State Khusus SOPR (Chart 1 - Tab Profit & Loss)
if 'tr_sopr' not in st.session_state: st.session_state.tr_sopr = "All Time"
if 'cd_sopr' not in st.session_state: st.session_state.cd_sopr = 120
if 'tf_sopr' not in st.session_state: st.session_state.tf_sopr = "Daily"
if 'sma_sopr' not in st.session_state: st.session_state.sma_sopr = "0d"
if 'cs_sopr' not in st.session_state: st.session_state.cs_sopr = 50

# State Khusus Realized PL (Chart 2 - Tab Profit & Loss)
if 'tr_pl' not in st.session_state: st.session_state.tr_pl = "All Time"
if 'cd_pl' not in st.session_state: st.session_state.cd_pl = 120
if 'tf_pl' not in st.session_state: st.session_state.tf_pl = "Daily"
if 'sma_pl' not in st.session_state: st.session_state.sma_pl = "0d"
if 'cs_pl' not in st.session_state: st.session_state.cs_pl = 50

# ==============================================================================
# 2. DATA LOADING & FILTERING ENGINE
# ==============================================================================
@st.cache_data(ttl=3600)
def load_data_price():
    try:
        df = pd.read_csv("data_price_level.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'sth_cost_basis': 'STH Cost Basis', 'lth_cost_basis': 'LTH Cost Basis', 'realized_price': 'Realized Price', 'cvdd': 'CVDD', 'true_market_mean_price': 'True Market Mean'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_momentum():
    try:
        df = pd.read_csv("data_momentum.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'asopr': 'aSOPR', 'lth_sopr': 'LTH SOPR', 'sth_sopr': 'STH SOPR', 'net_realized_pl_usd': 'Net Realized PL', 'sth_pl_ratio': 'STH P/L Ratio', 'lth_pl_ratio': 'LTH P/L Ratio'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date')
    except: return pd.DataFrame()

df_price_raw = load_data_price()
df_mom_raw = load_data_momentum()

# Mesin filter yang mendukung mode Dual-Line (Raw + SMA)
def apply_filters(df, res_state, smooth_state, custom_smooth, time_state, custom_days, metrics_to_smooth):
    if df.empty: return df, 1
    dff = df.copy()
    
    # 1. Resampling Timeframe
    if res_state != "Daily":
        dff.set_index('Date', inplace=True)
        if res_state == "3 Days": dff = dff.resample('3D').last()
        elif res_state == "Weekly": dff = dff.resample('W').last()
        elif res_state == "Monthly": dff = dff.resample('ME').last()
        dff.reset_index(inplace=True)
        
    # 2. Smoothing (SMA)
    w = 1
    if smooth_state == "7d": w = 7
    elif smooth_state == "14d": w = 14
    elif smooth_state == "30d": w = 30
    elif smooth_state == "Custom": w = custom_smooth
    
    if w > 1:
        for c in metrics_to_smooth:
            if c in dff.columns:
                # Membuat kolom duplikat khusus untuk garis SMA putus-putus
                dff[f"{c}_SMA"] = dff[c].rolling(w, min_periods=1).mean()
                    
    # 3. Time Range Filter
    t_max = dff['Date'].max()
    if time_state == "1 Month": t_min = t_max - timedelta(days=30)
    elif time_state == "3 Months": t_min = t_max - timedelta(days=90)
    elif time_state == "6 Months": t_min = t_max - timedelta(days=180)
    elif time_state == "1 Year": t_min = t_max - timedelta(days=365)
    elif time_state == "4 Years (Cycle)": t_min = t_max - timedelta(days=365 * 4)
    elif time_state == "Custom": t_min = t_max - timedelta(days=custom_days)
    else: t_min = dff['Date'].min()
    
    dff = dff[dff['Date'] >= t_min].copy()
    dff['Date_str'] = dff['Date'].dt.strftime('%Y-%m-%d')
    return dff, w

def get_s(df, col): return df[['Date_str', col]].dropna().rename(columns={'Date_str':'time', col:'value'}).to_dict('records') if col in df.columns else []
t_opts = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]

# ==============================================================================
# 3. TABS NAVIGATION
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["Price Levels", "Profit & Loss", "Oscillators (Soon)"])

# ------------------------------------------------------------------------------
# TAB 1: ON-CHAIN PRICE LEVELS
# ------------------------------------------------------------------------------
with tab1:
    if not df_price_raw.empty:
        df_p, w_p = apply_filters(df_price_raw, st.session_state.tf_p, st.session_state.sma_p, st.session_state.cs_p, st.session_state.tr_p, st.session_state.cd_p, ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'])

        # 1. JUDUL & KPI
        st.title("On-Chain Price Levels")
        st.markdown("---")
        last_p = df_p.iloc[-1]
        btc_p = last_p.get('BTC Price', 0)
        
        def render_kpi_p(title, value, is_btc=False):
            if is_btc or pd.isna(value) or value == 0:
                c, tc, d = "#ffffff", "#a3a8b8", ""
            else:
                dp = ((btc_p - value) / btc_p) * 100
                ip = dp >= 0
                c = "#00cc66" if ip else "#ff4d4d"
                tc, ar = c, "↑" if ip else "↓"
                d = f"<div style='margin-top:4px;'><span style='color:{c}; font-size:0.85rem; background-color:{c}20; padding:2px 6px; border-radius:4px;'>{ar} {abs(dp):.2f}%</span></div>"
            st.markdown(f"<div style='padding-bottom:10px;'><span style='color:{tc}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{c}; font-size:1.4rem; font-weight:700;'>${value:,.2f}</span>{d}</div>", unsafe_allow_html=True)

        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: render_kpi_p("Current BTC Price", btc_p, True)
        with k2: render_kpi_p("STH Cost Basis", last_p.get('STH Cost Basis', 0))
        with k3: render_kpi_p("LTH Cost Basis", last_p.get('LTH Cost Basis', 0))
        with k4: render_kpi_p("Realized Price", last_p.get('Realized Price', 0))
        with k5: render_kpi_p("True Market Mean", last_p.get('True Market Mean', 0))
        st.markdown("---")

        # 2. PANEL KONTROL
        col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
        with col_fs: focus_p = st.toggle("Full Screen", key="tg_p")
        with col_tf: st.session_state.tf_p = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_p), key="tfs_p", label_visibility="collapsed")
        with col_sma: st.session_state.sma_p = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_p), key="smas_p", label_visibility="collapsed")
        with col_sma_cst:
            if st.session_state.sma_p == "Custom": st.session_state.cs_p = st.number_input("Days", min_value=1, value=st.session_state.cs_p, label_visibility="collapsed", key="cst_p")
        with col_radio:
            c_idx = t_opts.index(st.session_state.tr_p) if st.session_state.tr_p in t_opts else 5
            st.session_state.tr_p = st.radio("Range:", t_opts, index=c_idx, horizontal=True, label_visibility="collapsed", key="rg_p")
        with col_custom:
            if st.session_state.tr_p == "Custom": st.session_state.cd_p = st.number_input("Days back", min_value=7, value=st.session_state.cd_p, label_visibility="collapsed", key="cdin_p")
        
        # 3. SELECTION METRIC (TOMBOL PILLS)
        opts_p_base = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD']
        all_opts_p = opts_p_base.copy()
        if w_p > 1:
            all_opts_p.extend([f"{m} (SMA {w_p})" for m in opts_p_base])
            
        try: active_metrics_p = st.pills("Metrics", all_opts_p, default=opts_p_base, selection_mode="multi", label_visibility="collapsed")
        except: active_metrics_p = st.multiselect("Metrics", all_opts_p, default=opts_p_base, label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        # 4. RENDER CHART
        chart_p_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_p else 650}
        series_p = [{"type": 'Line', "data": get_s(df_p, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}}]
        
        colors_p = {'🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis'), '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis'), '⚪ Realized Price': ('#ffffff', 'Realized Price'), '🟣 True Market Mean': ('#cc33ff', 'True Market Mean'), '🟢 CVDD': ('#00cc66', 'CVDD')}
        
        for m in active_metrics_p:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            if base_m in colors_p:
                m_color, m_name = colors_p[base_m]
                if is_sma:
                    series_p.append({"type": 'Line', "data": get_s(df_p, f"{m_name}_SMA"), "options": {"color": m_color, "lineWidth": 1, "lineStyle": 2, "title": f"{m_name} SMA"}})
                else:
                    series_p.append({"type": 'Line', "data": get_s(df_p, m_name), "options": {"color": m_color, "lineWidth": 2, "title": m_name}})
                    
        renderLightweightCharts([{"chart": chart_p_opts, "series": series_p}], 'chart_price')

# ------------------------------------------------------------------------------
# TAB 2: PROFIT & LOSS (DUAL CHARTS)
# ------------------------------------------------------------------------------
with tab2:
    if not df_mom_raw.empty:
        # 1. JUDUL & KPI GLOBAL (Diambil dari raw data terkini agar tidak terpengaruh filter)
        st.title("Profit & Loss")
        st.markdown("---")
        last_m = df_mom_raw.iloc[-1]
        btc_m = last_m.get('BTC Price', 0)
        
        def render_kpi_m(title, value, threshold=1.0, is_money=False):
            if pd.isna(value) or value == 0: color = "#a3a8b8"
            else: color = "#00cc66" if value >= threshold else "#ff4d4d"
            val_str = f"${value:,.2f}" if is_money else f"{value:.4f}"
            st.markdown(f"<div style='padding-bottom:10px;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span></div>", unsafe_allow_html=True)

        k1, k2, k3, k4, k5 = st.columns(5)
        with k1: st.markdown(f"<div style='padding-bottom:10px;'><span style='color:#a3a8b8; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#ffffff; font-size:1.4rem; font-weight:700;'>${btc_m:,.2f}</span></div>", unsafe_allow_html=True)
        with k2: render_kpi_m("aSOPR", last_m.get('aSOPR', 0), 1.0)
        with k3: render_kpi_m("LTH SOPR", last_m.get('LTH SOPR', 0), 1.0)
        with k4: render_kpi_m("STH SOPR", last_m.get('STH SOPR', 0), 1.0)
        with k5: render_kpi_m("Net Realized PL", last_m.get('Net Realized PL', 0), 0.0, True)
        st.markdown("---")

        # ======================================================================
        # CHART 2A: SOPR FAMILY
        # ======================================================================
        st.subheader("SOPR Oscillators")
        df_sopr, w_sopr = apply_filters(df_mom_raw, st.session_state.tf_sopr, st.session_state.sma_sopr, st.session_state.cs_sopr, st.session_state.tr_sopr, st.session_state.cd_sopr, ['aSOPR', 'LTH SOPR', 'STH SOPR'])

        # PANEL KONTROL - SOPR
        col_fs_s, col_tf_s, col_sma_s, col_sma_cst_s, col_space_s, col_radio_s, col_custom_s = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
        with col_fs_s: focus_sopr = st.toggle("Full Screen", key="tg_sopr")
        with col_tf_s: st.session_state.tf_sopr = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_sopr), key="tfs_sopr", label_visibility="collapsed")
        with col_sma_s: st.session_state.sma_sopr = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_sopr), key="smas_sopr", label_visibility="collapsed")
        with col_sma_cst_s:
            if st.session_state.sma_sopr == "Custom": st.session_state.cs_sopr = st.number_input("Days", min_value=1, value=st.session_state.cs_sopr, label_visibility="collapsed", key="cst_sopr")
        with col_radio_s:
            c_idx_s = t_opts.index(st.session_state.tr_sopr) if st.session_state.tr_sopr in t_opts else 5
            st.session_state.tr_sopr = st.radio("Range:", t_opts, index=c_idx_s, horizontal=True, label_visibility="collapsed", key="rg_sopr")
        with col_custom_s:
            if st.session_state.tr_sopr == "Custom": st.session_state.cd_sopr = st.number_input("Days back", min_value=7, value=st.session_state.cd_sopr, label_visibility="collapsed", key="cdin_sopr")

        # SELECTION METRIC - SOPR
        opts_sopr_base = ['🔵 aSOPR', '🔴 STH SOPR', '🟢 LTH SOPR']
        all_opts_sopr = opts_sopr_base.copy()
        if w_sopr > 1:
            all_opts_sopr.extend([f"{m} (SMA {w_sopr})" for m in opts_sopr_base])
            
        try: sel_sopr = st.pills("SOPR Metrics", all_opts_sopr, default=['🔵 aSOPR'], selection_mode="multi", label_visibility="collapsed")
        except: sel_sopr = st.multiselect("SOPR Metrics", all_opts_sopr, default=['🔵 aSOPR'], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        chart_sopr_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_sopr else 550, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
        series_sopr = [{"type": 'Line', "data": get_s(df_sopr, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        
        df_sopr['Neutral_Line'] = 1.0
        series_sopr.append({"type": 'Line', "data": get_s(df_sopr, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})

        colors_sopr = {'🔵 aSOPR': ('#00e6e6', 'aSOPR'), '🔴 STH SOPR': ('#ff4d4d', 'STH SOPR'), '🟢 LTH SOPR': ('#00cc66', 'LTH SOPR')}
        
        for m in sel_sopr:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            if base_m in colors_sopr:
                c_col, c_name = colors_sopr[base_m]
                if is_sma: 
                    series_sopr.append({"type": 'Line', "data": get_s(df_sopr, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{c_name} SMA"}})
                else: 
                    series_sopr.append({"type": 'Line', "data": get_s(df_sopr, c_name), "options": {"color": c_col, "lineWidth": 2, "priceScaleId": 'left', "title": c_name}})
        
        renderLightweightCharts([{"chart": chart_sopr_opts, "series": series_sopr}], 'chart_sopr')
        st.markdown("<br><br>", unsafe_allow_html=True)


        # ======================================================================
        # CHART 2B: REALIZED P/L FAMILY
        # ======================================================================
        st.markdown("---")
        st.subheader("Realized Profit & Loss")
        df_pl, w_pl = apply_filters(df_mom_raw, st.session_state.tf_pl, st.session_state.sma_pl, st.session_state.cs_pl, st.session_state.tr_pl, st.session_state.cd_pl, ['Net Realized PL', 'STH P/L Ratio', 'LTH P/L Ratio'])

        # PANEL KONTROL - REALIZED PL
        col_fs_pl, col_tf_pl, col_sma_pl, col_sma_cst_pl, col_space_pl, col_radio_pl, col_custom_pl = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
        with col_fs_pl: focus_pl = st.toggle("Full Screen", key="tg_pl")
        with col_tf_pl: st.session_state.tf_pl = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_pl), key="tfs_pl", label_visibility="collapsed")
        with col_sma_pl: st.session_state.sma_pl = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_pl), key="smas_pl", label_visibility="collapsed")
        with col_sma_cst_pl:
            if st.session_state.sma_pl == "Custom": st.session_state.cs_pl = st.number_input("Days", min_value=1, value=st.session_state.cs_pl, label_visibility="collapsed", key="cst_pl")
        with col_radio_pl:
            c_idx_pl = t_opts.index(st.session_state.tr_pl) if st.session_state.tr_pl in t_opts else 5
            st.session_state.tr_pl = st.radio("Range:", t_opts, index=c_idx_pl, horizontal=True, label_visibility="collapsed", key="rg_pl")
        with col_custom_pl:
            if st.session_state.tr_pl == "Custom": st.session_state.cd_pl = st.number_input("Days back", min_value=7, value=st.session_state.cd_pl, label_visibility="collapsed", key="cdin_pl")

        # SELECTION METRIC - REALIZED PL
        opts_pl_base = ['⚪ Net Realized PL', '🟣 STH P/L Ratio', '🟤 LTH P/L Ratio']
        all_opts_pl = opts_pl_base.copy()
        if w_pl > 1:
            all_opts_pl.extend([f"{m} (SMA {w_pl})" for m in opts_pl_base])

        try: sel_pl = st.pills("PL Metrics", all_opts_pl, default=['⚪ Net Realized PL'], selection_mode="multi", label_visibility="collapsed")
        except: sel_pl = st.multiselect("PL Metrics", all_opts_pl, default=['⚪ Net Realized PL'], label_visibility="collapsed")
        st.markdown("<br>", unsafe_allow_html=True)

        chart_pl_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_pl else 550, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
        series_pl = [{"type": 'Line', "data": get_s(df_pl, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        colors_pl = {'⚪ Net Realized PL': ('#ffffff', 'Net Realized PL'), '🟣 STH P/L Ratio': ('#cc33ff', 'STH P/L Ratio'), '🟤 LTH P/L Ratio': ('#cc9966', 'LTH P/L Ratio')}
        
        for m in sel_pl:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m in colors_pl:
                c_col, c_name = colors_pl[base_m]
                if is_sma: 
                    series_pl.append({"type": 'Line', "data": get_s(df_pl, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{c_name} SMA"}})
                else: 
                    series_pl.append({"type": 'Line', "data": get_s(df_pl, c_name), "options": {"color": c_col, "lineWidth": 2, "priceScaleId": 'left', "title": c_name}})

        renderLightweightCharts([{"chart": chart_pl_opts, "series": series_pl}], 'chart_netpl')

    else:
        st.info("Menunggu data Profit & Loss. Pastikan GitHub Actions sudah jalan!")

with tab3:
    st.info("Oscillators chart is under construction. Coming soon!")
