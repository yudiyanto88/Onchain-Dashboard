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

if 'tr_p' not in st.session_state: st.session_state.tr_p = "All Time"
if 'cd_p' not in st.session_state: st.session_state.cd_p = 120
if 'tf_p' not in st.session_state: st.session_state.tf_p = "Daily"
if 'sma_p' not in st.session_state: st.session_state.sma_p = "0d"
if 'cs_p' not in st.session_state: st.session_state.cs_p = 50

if 'tr_m' not in st.session_state: st.session_state.tr_m = "All Time"
if 'cd_m' not in st.session_state: st.session_state.cd_m = 120
if 'tf_m' not in st.session_state: st.session_state.tf_m = "Daily"
if 'sma_m' not in st.session_state: st.session_state.sma_m = "0d"
if 'cs_m' not in st.session_state: st.session_state.cs_m = 50

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

# ==============================================================================
# 3. TABS NAVIGATION
# ==============================================================================
tab1, tab2, tab3 = st.tabs(["Price Levels", "Profit & Loss", "Oscillators (Soon)"])

# ------------------------------------------------------------------------------
# TAB 1: ON-CHAIN PRICE LEVELS
# ------------------------------------------------------------------------------
with tab1:
    if not df_price_raw.empty:
        header_p = st.container()
        controls_p = st.container()
        chart_p = st.container()

        with header_p:
            st.title("On-Chain Price Levels")
            st.markdown("---")
            # Filter Data untuk KPI
            df_p, w_p = apply_filters(df_price_raw, st.session_state.tf_p, st.session_state.sma_p, st.session_state.cs_p, st.session_state.tr_p, st.session_state.cd_p, ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'])
            
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

        with controls_p:
            col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
            with col_fs: focus_p = st.toggle("Full Screen", key="tg_p")
            with col_tf: st.session_state.tf_p = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_p), key="tfs_p", label_visibility="collapsed")
            with col_sma: st.session_state.sma_p = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_p), key="smas_p", label_visibility="collapsed")
            with col_sma_cst:
                if st.session_state.sma_p == "Custom": st.session_state.cs_p = st.number_input("Days", min_value=1, value=st.session_state.cs_p, label_visibility="collapsed", key="cst_p")
            with col_radio:
                t_opts = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]
                c_idx = t_opts.index(st.session_state.tr_p) if st.session_state.tr_p in t_opts else 5
                st.session_state.tr_p = st.radio("Range:", t_opts, index=c_idx, horizontal=True, label_visibility="collapsed", key="rg_p")
            with col_custom:
                if st.session_state.tr_p == "Custom": st.session_state.cd_p = st.number_input("Days back", min_value=7, value=st.session_state.cd_p, label_visibility="collapsed", key="cdin_p")
            
            metric_opts_p = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD']
            try: active_metrics_p = st.pills("Metrics", metric_opts_p, default=metric_opts_p, selection_mode="multi", label_visibility="collapsed")
            except: active_metrics_p = st.multiselect("Metrics", metric_opts_p, default=metric_opts_p, label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)

        if focus_p:
            st.markdown("""<style>.block-container{padding-top:1rem; padding-bottom:1rem; max-width:100%;} header, footer{visibility:hidden;}</style>""", unsafe_allow_html=True)

        with chart_p:
            chart_p_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_p else 650}
            series_p = [{"type": 'Line', "data": get_s(df_p, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}}]
            
            colors_p = {'🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis'), '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis'), '⚪ Realized Price': ('#ffffff', 'Realized Price'), '🟣 True Market Mean': ('#cc33ff', 'True Market Mean'), '🟢 CVDD': ('#00cc66', 'CVDD')}
            for m in active_metrics_p:
                if m in colors_p:
                    met_color, met_name = colors_p[m]
                    series_p.append({"type": 'Line', "data": get_s(df_p, met_name), "options": {"color": met_color, "lineWidth": 2, "title": met_name}})
                    if w_p > 1:
                        series_p.append({"type": 'Line', "data": get_s(df_p, f"{met_name}_SMA"), "options": {"color": met_color, "lineWidth": 1, "lineStyle": 2, "title": f"{met_name} SMA({w_p})"}})
            
            renderLightweightCharts([{"chart": chart_p_opts, "series": series_p}], 'chart_price')

# ------------------------------------------------------------------------------
# TAB 2: PROFIT & LOSS 
# ------------------------------------------------------------------------------
with tab2:
    if not df_mom_raw.empty:
        header_m = st.container()
        controls_m = st.container()
        chart_m = st.container()

        with header_m:
            st.title("Profit & Loss")
            st.markdown("---")
            
            df_m, w_m = apply_filters(df_mom_raw, st.session_state.tf_m, st.session_state.sma_m, st.session_state.cs_m, st.session_state.tr_m, st.session_state.cd_m, ['aSOPR', 'LTH SOPR', 'STH SOPR', 'STH P/L Ratio', 'LTH P/L Ratio', 'Net Realized PL'])
            
            last_m = df_m.iloc[-1]
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

        with controls_m:
            col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
            with col_fs: focus_m = st.toggle("Full Screen", key="tg_m")
            with col_tf: st.session_state.tf_m = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_m), key="tfs_m", label_visibility="collapsed")
            with col_sma: st.session_state.sma_m = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_m), key="smas_m", label_visibility="collapsed")
            with col_sma_cst:
                if st.session_state.sma_m == "Custom": st.session_state.cs_m = st.number_input("Days", min_value=1, value=st.session_state.cs_m, label_visibility="collapsed", key="cst_m")
            with col_radio:
                c_idx_m = t_opts.index(st.session_state.tr_m) if st.session_state.tr_m in t_opts else 5
                st.session_state.tr_m = st.radio("Range:", t_opts, index=c_idx_m, horizontal=True, label_visibility="collapsed", key="rg_m")
            with col_custom:
                if st.session_state.tr_m == "Custom": st.session_state.cd_m = st.number_input("Days back", min_value=7, value=st.session_state.cd_m, label_visibility="collapsed", key="cdin_m")
            
            m_opts_all = ['🔵 aSOPR', '🔴 STH SOPR', '🟢 LTH SOPR', '⚪ Net Realized PL', '🟣 STH P/L Ratio', '🟤 LTH P/L Ratio']
            
            try: sel_m = st.pills("Metrics", m_opts_all, default=['🔵 aSOPR', '⚪ Net Realized PL'], selection_mode="multi", label_visibility="collapsed")
            except: sel_m = st.multiselect("Metrics", m_opts_all, default=['🔵 aSOPR', '⚪ Net Realized PL'], label_visibility="collapsed")
                
            st.markdown("<br>", unsafe_allow_html=True)

        if focus_m:
            st.markdown("""<style>.block-container{padding-top:1rem; padding-bottom:1rem; max-width:100%;} header, footer{visibility:hidden;}</style>""", unsafe_allow_html=True)

        with chart_m:
            chart_m_opts = {
                "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
                "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
                "crosshair": {"mode": 0}, "height": 850 if focus_m else 650,
                "rightPriceScale": {"visible": True}, 
                "leftPriceScale": {"visible": True},
                "priceScale": {
                    "net_pl_scale": {
                        "visible": False, 
                        "scaleMargins": {"top": 0.8, "bottom": 0}
                    }
                }
            }
            
            series_m = [{"type": 'Line', "data": get_s(df_m, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
            
            df_m['Neutral_Line'] = 1.0
            series_m.append({"type": 'Line', "data": get_s(df_m, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})

            colors_m = {
                '🔵 aSOPR': ('#00e6e6', 'aSOPR'), 
                '🔴 STH SOPR': ('#ff4d4d', 'STH SOPR'), 
                '🟢 LTH SOPR': ('#00cc66', 'LTH SOPR'),
                '🟣 STH P/L Ratio': ('#cc33ff', 'STH P/L Ratio'), 
                '🟤 LTH P/L Ratio': ('#cc9966', 'LTH P/L Ratio')
            }
            
            for m in sel_m:
                if m in colors_m:
                    met_color, met_name = colors_m[m]
                    series_m.append({"type": 'Line', "data": get_s(df_m, met_name), "options": {"color": met_color, "lineWidth": 2, "priceScaleId": 'left', "title": met_name}})
                    if w_m > 1:
                        series_m.append({"type": 'Line', "data": get_s(df_m, f"{met_name}_SMA"), "options": {"color": met_color, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{met_name} SMA({w_m})"}})
                
                elif m == '⚪ Net Realized PL':
                    net_pl_raw = get_s(df_m, 'Net Realized PL')
                    for d in net_pl_raw: d['color'] = '#00cc66' if d['value'] >= 0 else '#ff4d4d'
                    series_m.append({"type": 'Histogram', "data": net_pl_raw, "options": {"priceScaleId": 'net_pl_scale', "title": 'Net PL'}})
                    if w_m > 1:
                        series_m.append({"type": 'Line', "data": get_s(df_m, 'Net Realized PL_SMA'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'net_pl_scale', "title": f"Net PL SMA({w_m})"}})

            renderLightweightCharts([{"chart": chart_m_opts, "series": series_m}], 'chart_momentum')
    else:
        st.info("Menunggu data Profit & Loss. Pastikan GitHub Actions sudah jalan!")

with tab3:
    st.info("Oscillators chart is under construction. Coming soon!")
