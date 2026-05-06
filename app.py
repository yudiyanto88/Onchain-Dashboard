import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PAGE CONFIGURATION & CUSTOM CSS (MENGHILANGKAN WARNA MERAH DEFAULT)
# ==============================================================================
st.set_page_config(
    page_title="Yudiyanto | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Injeksi CSS agar tombol Pills yang aktif berwarna abu-abu/putih (bukan merah)
st.markdown("""
<style>
    div[data-testid="stPills"] label[data-selected="true"] {
        background-color: #2b2b36 !important;
        color: #ffffff !important;
        border-color: #4b4b5c !important;
    }
</style>
""", unsafe_allow_html=True)

if 'time_range' not in st.session_state: st.session_state.time_range = "All Time"
if 'custom_days' not in st.session_state: st.session_state.custom_days = 120
if 'resolution' not in st.session_state: st.session_state.resolution = "Daily"
if 'smooth_period' not in st.session_state: st.session_state.smooth_period = "0d"
if 'custom_smooth' not in st.session_state: st.session_state.custom_smooth = 50

# ==============================================================================
# 2. DATA LOADING
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

# Helper Filter Waktu & Resample
def apply_filters(df, res_state, smooth_state, custom_smooth, time_state, custom_days, metrics_to_smooth):
    if df.empty: return df
    dff = df.copy()
    
    if res_state != "Daily":
        dff.set_index('Date', inplace=True)
        if res_state == "3 Days": dff = dff.resample('3D').last()
        elif res_state == "Weekly": dff = dff.resample('W').last()
        elif res_state == "Monthly": dff = dff.resample('ME').last()
        dff.reset_index(inplace=True)
        
    w = 1
    if smooth_state == "7d": w = 7
    elif smooth_state == "14d": w = 14
    elif smooth_state == "30d": w = 30
    elif smooth_state == "Custom": w = custom_smooth
    if w > 1:
        for c in metrics_to_smooth:
            if c in dff.columns: dff[c] = dff[c].rolling(w, min_periods=1).mean()
            
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
    return dff

# ==============================================================================
# 3. TABS NAVIGATION
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["Price Levels", "Profit & Loss", "Oscillators (Soon)"])

# ------------------------------------------------------------------------------
# TAB 1: ON-CHAIN PRICE LEVELS
# ------------------------------------------------------------------------------
with tab1:
    if not df_price_raw.empty:
        col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
        with col_fs: focus_mode_p = st.toggle("Full Screen", key="fs_p")
        with col_tf: st.session_state.resolution = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.resolution), key="tf_p")
        with col_sma: st.session_state.smooth_period = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.smooth_period), key="sma_p")
        with col_sma_cst:
            if st.session_state.smooth_period == "Custom": st.session_state.custom_smooth = st.number_input("Days", min_value=1, value=st.session_state.custom_smooth, label_visibility="collapsed", key="cst_p")
        with col_radio:
            t_opts = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]
            c_idx = t_opts.index(st.session_state.time_range) if st.session_state.time_range in t_opts else 5
            st.session_state.time_range = st.radio("Range:", t_opts, index=c_idx, horizontal=True, label_visibility="collapsed", key="rg_p")
        with col_custom:
            if st.session_state.time_range == "Custom": st.session_state.custom_days = st.number_input("Days back", min_value=7, value=st.session_state.custom_days, label_visibility="collapsed", key="cd_p")
        
        metric_opts_p = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD']
        try:
            active_metrics_p = st.pills("Metrics:", metric_opts_p, default=metric_opts_p, selection_mode="multi", label_visibility="collapsed")
        except:
            active_metrics_p = st.multiselect("Metrics:", metric_opts_p, default=metric_opts_p, label_visibility="collapsed")
            
        st.markdown("<br>", unsafe_allow_html=True)

        df_p = apply_filters(df_price_raw, st.session_state.resolution, st.session_state.smooth_period, st.session_state.custom_smooth, st.session_state.time_range, st.session_state.custom_days, ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'])

        if not focus_mode_p:
            st.title("On-Chain Price Levels")
            st.markdown("---")
            last_p = df_p.iloc[-1]
            btc_p = last_p.get('BTC Price', 0)
            
            def render_kpi(title, value, is_btc=False):
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
            with k1: render_kpi("Current BTC Price", btc_p, True)
            with k2: render_kpi("STH Cost Basis", last_p.get('STH Cost Basis', 0))
            with k3: render_kpi("LTH Cost Basis", last_p.get('LTH Cost Basis', 0))
            with k4: render_kpi("Realized Price", last_p.get('Realized Price', 0))
            with k5: render_kpi("True Market Mean", last_p.get('True Market Mean', 0))
            st.markdown("---")
        else:
            st.markdown("""<style>.block-container{padding-top:1rem; padding-bottom:1rem; max-width:100%;} header, footer{visibility:hidden;}</style>""", unsafe_allow_html=True)

        chart_p_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_mode_p else 650}
        
        def get_s(df, col): return df[['Date_str', col]].dropna().rename(columns={'Date_str':'time', col:'value'}).to_dict('records') if col in df.columns else []
        
        series_p = [{"type": 'Line', "data": get_s(df_p, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}}]
        
        colors_p = {'🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis'), '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis'), '⚪ Realized Price': ('#ffffff', 'Realized Price'), '🟣 True Market Mean': ('#cc33ff', 'True Market Mean'), '🟢 CVDD': ('#00cc66', 'CVDD')}
        for m in active_metrics_p:
            if m in colors_p: series_p.append({"type": 'Line', "data": get_s(df_p, colors_p[m][1]), "options": {"color": colors_p[m][0], "lineWidth": 2, "title": colors_p[m][1]}})
        
        renderLightweightCharts([{"chart": chart_p_opts, "series": series_p}], 'chart_price')

# ------------------------------------------------------------------------------
# TAB 2: PROFIT & LOSS (SEBELUMNYA MOMENTUM)
# ------------------------------------------------------------------------------
with tab2:
    if not df_mom_raw.empty:
        col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
        with col_fs: focus_mode_m = st.toggle("Full Screen", key="fs_m")
        with col_tf: st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], key="tf_m_d", disabled=True)
        with col_sma: st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], key="sma_m_d", disabled=True)
        
        m_sopr = ['🟠 aSOPR', '🔴 STH SOPR', '🔵 LTH SOPR']
        m_pl = ['🟡 Net Realized PL (Hist)', '🟣 STH P/L Ratio', '🟢 LTH P/L Ratio']
        
        try: 
            sel_sopr = st.pills("SOPR", m_sopr, default=['🟠 aSOPR'], selection_mode="multi", label_visibility="collapsed")
            sel_pl = st.pills("PL", m_pl, default=['🟡 Net Realized PL (Hist)'], selection_mode="multi", label_visibility="collapsed")
        except: 
            sel_sopr = st.multiselect("SOPR", m_sopr, default=['🟠 aSOPR'], label_visibility="collapsed")
            sel_pl = st.multiselect("PL", m_pl, default=['🟡 Net Realized PL (Hist)'], label_visibility="collapsed")

        st.markdown("<br>", unsafe_allow_html=True)
        
        df_m = apply_filters(df_mom_raw, st.session_state.resolution, st.session_state.smooth_period, st.session_state.custom_smooth, st.session_state.time_range, st.session_state.custom_days, ['aSOPR', 'LTH SOPR', 'STH SOPR', 'STH P/L Ratio', 'LTH P/L Ratio', 'Net Realized PL'])

        if not focus_mode_m:
            st.title("Profit & Loss")
            st.markdown("---")
            
            # KPI PANEL UNTUK TAB 2 (PROFIT/LOSS)
            last_m = df_m.iloc[-1]
            prev_m = df_m.iloc[-2] if len(df_m) > 1 else last_m
            btc_m = last_m.get('BTC Price', 0)
            
            def render_kpi_momentum(title, val, prev_val, format_usd=False):
                if pd.isna(val) or val == 0:
                    c, tc, d = "#ffffff", "#a3a8b8", ""
                else:
                    dp = ((val - prev_val) / abs(prev_val)) * 100 if prev_val != 0 else 0
                    
                    # Logika warna: Profit hijau jika SOPR >= 1 atau Net PL >= 0
                    if "SOPR" in title or "Ratio" in title: is_profit = val >= 1.0
                    else: is_profit = val >= 0
                    
                    c = "#00cc66" if is_profit else "#ff4d4d"
                    tc, ar = c, "↑" if dp >= 0 else "↓"
                    d = f"<div style='margin-top:4px;'><span style='color:{c}; font-size:0.85rem; background-color:{c}20; padding:2px 6px; border-radius:4px;'>{ar} {abs(dp):.2f}% (DoD)</span></div>"
                
                val_str = f"${val:,.2f}" if format_usd else f"{val:,.4f}"
                st.markdown(f"<div style='padding-bottom:10px;'><span style='color:{tc}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{c}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

            k1, k2, k3, k4 = st.columns(4)
            with k1: 
                st.markdown(f"<div style='padding-bottom:10px;'><span style='color:#a3a8b8; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#ffffff; font-size:1.4rem; font-weight:700;'>${btc_m:,.2f}</span></div>", unsafe_allow_html=True)
            with k2: render_kpi_momentum("aSOPR", last_m.get('aSOPR', 0), prev_m.get('aSOPR', 0))
            with k3: render_kpi_momentum("LTH SOPR", last_m.get('LTH SOPR', 0), prev_m.get('LTH SOPR', 0))
            with k4: render_kpi_momentum("Net Realized PL", last_m.get('Net Realized PL', 0), prev_m.get('Net Realized PL', 0), format_usd=True)
            st.markdown("---")

        chart_m_opts = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_mode_m else 650,
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": True}    
        }
        
        series_m = [{"type": 'Line', "data": get_s(df_m, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        
        df_m['Neutral_Line'] = 1.0
        series_m.append({"type": 'Line', "data": get_s(df_m, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})

        colors_m = {
            '🟠 aSOPR': ('#ff9933', 'aSOPR'), 
            '🔴 STH SOPR': ('#ff4d4d', 'STH SOPR'), 
            '🔵 LTH SOPR': ('#4da6ff', 'LTH SOPR'),
            '🟣 STH P/L Ratio': ('#cc33ff', 'STH P/L Ratio'), 
            '🟢 LTH P/L Ratio': ('#00cc66', 'LTH P/L Ratio')
        }
        
        for m in (sel_sopr if sel_sopr else []) + (sel_pl if sel_pl else []):
            if m in colors_m:
                series_m.append({"type": 'Line', "data": get_s(df_m, colors_m[m][1]), "options": {"color": colors_m[m][0], "lineWidth": 2, "priceScaleId": 'left', "title": colors_m[m][1]}})
        
        if sel_pl and '🟡 Net Realized PL (Hist)' in sel_pl:
            net_pl_data = get_s(df_m, 'Net Realized PL')
            for d in net_pl_data: d['color'] = '#00cc66' if d['value'] >= 0 else '#ff4d4d'
            series_m.append({"type": 'Histogram', "data": net_pl_data, "options": {"priceScaleId": 'right', "title": 'Net Realized P/L'}})

        renderLightweightCharts([{"chart": chart_m_opts, "series": series_m}], 'chart_momentum')
    else:
        st.info("Menunggu data Profit & Loss. Pastikan GitHub Actions sudah jalan!")

with tab3:
    st.info("Oscillators chart is under construction. Coming soon!")
