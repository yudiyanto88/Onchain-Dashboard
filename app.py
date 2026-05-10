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
    initial_sidebar_state="expanded"
)

# --- CSS SUPER CUSTOM UNTUK SIDEBAR TABS, SELECTBOX, DAN MENCEGAH CLIPPING ---
st.markdown("""
<style>
/* ======================================================
   A. STYLING SIDEBAR MENU MENJADI BENTUK "TAB" BESAR
   ====================================================== */
section[data-testid="stSidebar"] {
    background-color: #0e1117;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] {
    gap: 10px; 
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label {
    background-color: #1a1d24;
    padding: 12px 16px !important;
    border-radius: 8px !important;
    border-left: 4px solid transparent;
    margin: 0 !important;
    cursor: pointer;
    transition: all 0.2s ease-in-out;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label:hover {
    background-color: #262a35;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label[data-checked="true"] {
    border-left: 4px solid #a855f7 !important;
    background-color: #2a203b !important;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] p {
    font-size: 1.15rem !important;
    font-weight: 600 !important;
    margin: 0 !important;
    color: #ffffff !important;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label > div:first-child {
    display: none !important;
}

/* ======================================================
   B. MENGECILKAN SELECTBOX, TOGGLE, DAN MENYAMAKAN FONT
   ====================================================== */
div[data-testid="stSelectbox"] *, 
div[data-testid="stRadio"] *, 
div[data-testid="stToggle"] *,
div[data-testid="stNumberInput"] * {
    font-size: 0.85rem !important;
}
div[data-testid="stToggle"] label p {
    font-size: 0.85rem !important;
    margin-top: 2px !important; 
}
div[data-testid="stSelectbox"] label, 
div[data-testid="stNumberInput"] label {
    padding-bottom: 2px !important;
    min-height: 0px !important;
}

/* Memotong Tinggi Selectbox & Presisi Tengah Vertikal */
div[data-baseweb="select"] > div {
    min-height: 32px !important;
    height: 32px !important;
    border-radius: 6px !important;
    padding-bottom: 2px !important;
}
div[data-baseweb="select"] > div > div {
    padding-top: 0px !important;
    padding-bottom: 0px !important;
}
div[data-baseweb="select"] span {
    display: inline-block;
}

/* ======================================================
   C. MERAPIKAN SPASI UTAMA & MENCEGAH TEKS TERPOTONG
   ====================================================== */
.block-container { 
    padding-top: 3rem !important; 
    padding-bottom: 1.5rem !important; 
    max-width: 100%; 
}
div[data-testid="stPill"] button {
    font-size: 0.85rem !important;
    padding: 2px 12px !important;
    min-height: 28px !important;
}
</style>
""", unsafe_allow_html=True)

# Inisialisasi Session State 
for key in ['tr_p', 'tr_ms', 'tr_mpl', 'tr_d', 'tr_ss']:
    if key not in st.session_state: st.session_state[key] = "All Time"
for key in ['cd_p', 'cd_ms', 'cd_mpl', 'cd_d', 'cd_ss']:
    if key not in st.session_state: st.session_state[key] = 120
for key in ['tf_p', 'tf_ms', 'tf_mpl', 'tf_d', 'tf_ss']:
    if key not in st.session_state: st.session_state[key] = "Daily"
for key in ['sma_p', 'sma_ms', 'sma_mpl', 'sma_d']:
    if key not in st.session_state: st.session_state[key] = "0d"

# Secara khusus mensetting default SMA untuk Social Sentiment adalah 30d
if 'sma_ss' not in st.session_state: st.session_state['sma_ss'] = "30d"

for key in ['cs_p', 'cs_ms', 'cs_mpl', 'cs_d', 'cs_ss']:
    if key not in st.session_state: st.session_state[key] = 50

# ==============================================================================
# 2. DATA LOADING & FILTERING ENGINE
# ==============================================================================
@st.cache_data(ttl=3600)
def load_data_price():
    try:
        df = pd.read_csv("data_price_level.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'sth_cost_basis': 'STH Cost Basis', 'lth_cost_basis': 'LTH Cost Basis', 'realized_price': 'Realized Price', 'cvdd': 'CVDD', 'true_market_mean_price': 'True Market Mean'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date')
        return df.drop_duplicates(subset=['Date'], keep='last') 
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_momentum():
    try:
        df = pd.read_csv("data_momentum.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'asopr': 'aSOPR', 'lth_sopr': 'LTH SOPR', 'sth_sopr': 'STH SOPR', 'net_realized_pl_usd': 'Net Realized PL', 'sth_pl_ratio': 'STH P/L Ratio', 'lth_pl_ratio': 'LTH P/L Ratio'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date')
        return df.drop_duplicates(subset=['Date'], keep='last') 
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_derivatives():
    try:
        df = pd.read_csv("data_derivatives.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'total_oi': 'Open Interest', 'funding_rate': 'Funding Rate'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date')
        return df.drop_duplicates(subset=['Date'], keep='last') 
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_sentiment():
    try:
        df = pd.read_csv("data_sentiment.csv")
        # Menyelaraskan nama kolom dengan API response
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'trend_bitcoin': 'Google Trend (BTC)', 'trend_crypto': 'Google Trend (Crypto)', 'wiki_bitcoin': 'Wiki (BTC)', 'wiki_cryptocurrency': 'Wiki (Crypto)'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date')
        return df.drop_duplicates(subset=['Date'], keep='last') 
    except: return pd.DataFrame()

df_price_raw = load_data_price()
df_mom_raw = load_data_momentum()
df_deriv_raw = load_data_derivatives()
df_sentiment_raw = load_data_sentiment()

def apply_filters(df, res_state, smooth_state, custom_smooth, time_state, custom_days, metrics_to_smooth):
    if df.empty: return df, 1
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
            if c in dff.columns:
                dff[f"{c}_SMA"] = dff[c].rolling(w, min_periods=1).mean()
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

def get_s(df, col): 
    if col not in df.columns: return []
    clean_df = df[['Date_str', col]].dropna()
    return clean_df.rename(columns={'Date_str':'time', col:'value'}).to_dict('records')

t_opts = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]

# ==============================================================================
# 3. SIDEBAR NAVIGATION
# ==============================================================================
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #ffffff; font-size: 2.2rem;'>Yudiyanto</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center; color: #a855f7; font-weight: 800; font-size: 1.3rem; margin-top: -15px;'>ON-CHAIN DASHBOARD</h3>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    selected_menu = st.radio(
        "Menu Navigasi",
        ["Price Levels", "Profit & Loss", "Derivatives", "Social Sentiment"],
        label_visibility="collapsed"
    )
    st.markdown("---")

# ==============================================================================
# 4. MAIN DASHBOARD RENDER
# ==============================================================================

# ------------------------------------------------------------------------------
# TAB 1: PRICE LEVELS
# ------------------------------------------------------------------------------
if selected_menu == "Price Levels":
    if not df_price_raw.empty:
        df_p, w_p = apply_filters(df_price_raw, st.session_state.tf_p, st.session_state.sma_p, st.session_state.cs_p, st.session_state.tr_p, st.session_state.cd_p, ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'])

        last_p = df_p.iloc[-1]
        prev_p = df_p.iloc[-2] if len(df_p) > 1 else last_p
        
        btc_p = last_p.get('BTC Price', 0)
        btc_prev_p = prev_p.get('BTC Price', 0)
        
        def render_kpi_p(title, value, is_btc=False):
            if is_btc: 
                c, tc = "#f7931a", "#f7931a"
                if btc_prev_p > 0:
                    dp = ((btc_p - btc_prev_p) / btc_prev_p) * 100
                    ip = dp >= 0
                    dc = "#00cc66" if ip else "#ff4d4d"
                    ar = "↑" if ip else "↓"
                    d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {abs(dp):.2f}%</span></div>"
                else: d = ""
            elif pd.isna(value) or value == 0: 
                c, tc, d = "#ffffff", "#a3a8b8", ""
            else:
                dp = ((btc_p - value) / btc_p) * 100
                ip = dp >= 0
                c = "#00cc66" if ip else "#ff4d4d"
                tc, ar = c, "↑" if ip else "↓"
                d = f"<div style='margin-top:4px;'><span style='color:{c}; font-size:0.85rem; background-color:{c}20; padding:2px 6px; border-radius:4px;'>{ar} {abs(dp):.2f}%</span></div>"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{tc}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{c}; font-size:1.4rem; font-weight:700;'>${value:,.2f}</span>{d}</div>", unsafe_allow_html=True)

        col_title, k1, k2, k3, k4, k5 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        
        with col_title:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>On-Chain Price Levels<br><span style='font-size: 1rem; color: transparent;'>.</span></h3></div>", unsafe_allow_html=True)
            
        with k1: render_kpi_p("Current BTC Price", btc_p, True)
        with k2: render_kpi_p("STH Cost Basis", last_p.get('STH Cost Basis', 0))
        with k3: render_kpi_p("LTH Cost Basis", last_p.get('LTH Cost Basis', 0))
        with k4: render_kpi_p("Realized Price", last_p.get('Realized Price', 0))
        with k5: render_kpi_p("True Market Mean", last_p.get('True Market Mean', 0))
        
        st.markdown("---")

        col_fs, col_tf, col_sma, col_sma_cst, col_radio, col_custom = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs: focus_p = st.toggle("Full Screen", key="tg_p")
        with col_tf: st.session_state.tf_p = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_p), key="tfs_p")
        with col_sma: st.session_state.sma_p = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_p), key="smas_p")
        with col_sma_cst:
            if st.session_state.sma_p == "Custom": st.session_state.cs_p = st.number_input("Days", min_value=1, value=st.session_state.cs_p, label_visibility="collapsed", key="cst_p")
        with col_radio:
            c_idx = t_opts.index(st.session_state.tr_p) if st.session_state.tr_p in t_opts else 5
            st.session_state.tr_p = st.radio("Range:", t_opts, index=c_idx, horizontal=True, label_visibility="collapsed", key="rg_p")
        with col_custom:
            if st.session_state.tr_p == "Custom": st.session_state.cd_p = st.number_input("Days back", min_value=7, value=st.session_state.cd_p, label_visibility="collapsed", key="cdin_p")
        
        opts_p_base = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD']
        all_opts_p = opts_p_base.copy()
        if w_p > 1: all_opts_p.extend([f"{m} (SMA {w_p})" for m in opts_p_base])
            
        try: active_metrics_p = st.pills("Metrics", all_opts_p, default=opts_p_base, selection_mode="multi", label_visibility="collapsed")
        except: active_metrics_p = st.multiselect("Metrics", all_opts_p, default=opts_p_base, label_visibility="collapsed")

        chart_p_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_p else 650}
        
        series_p = [{"type": 'Line', "data": get_s(df_p, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        
        colors_p = {'🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis'), '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis'), '⚪ Realized Price': ('#ffffff', 'Realized Price'), '🟣 True Market Mean': ('#cc33ff', 'True Market Mean'), '🟢 CVDD': ('#00cc66', 'CVDD')}
        
        for m in active_metrics_p:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            if base_m in colors_p:
                m_color = colors_p[base_m][0]
                m_name = colors_p[base_m][1]
                if is_sma: series_p.append({"type": 'Line', "data": get_s(df_p, f"{m_name}_SMA"), "options": {"color": m_color, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{m_name} SMA"}})
                else: series_p.append({"type": 'Line', "data": get_s(df_p, m_name), "options": {"color": m_color, "lineWidth": 1, "priceScaleId": 'left', "title": m_name}})
                    
        renderLightweightCharts([{"chart": chart_p_opts, "series": series_p}], 'chart_price')

# ------------------------------------------------------------------------------
# TAB 2: PROFIT & LOSS 
# ------------------------------------------------------------------------------
elif selected_menu == "Profit & Loss":
    if not df_mom_raw.empty:
        last_m = df_mom_raw.iloc[-1]
        prev_m = df_mom_raw.iloc[-2] if len(df_mom_raw) > 1 else last_m
        
        btc_m = last_m.get('BTC Price', 0)
        btc_prev_m = prev_m.get('BTC Price', 0)
        
        def render_kpi_m(title, value, prev_val, threshold=1.0, is_money=False):
            if pd.isna(value) or value == 0: 
                color = "#a3a8b8"
                d = ""
            else: 
                color = "#00cc66" if value >= threshold else "#ff4d4d"
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                if is_money: diff_str = f"${abs(diff):,.2f}"
                else: diff_str = f"{abs(diff):.4f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"
                
            val_str = f"${value:,.2f}" if is_money else f"{value:.4f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_m = ((btc_m - btc_prev_m) / btc_prev_m * 100) if btc_prev_m else 0
        ip_btc_m = dp_btc_m >= 0
        dc_btc_m = "#00cc66" if ip_btc_m else "#ff4d4d"
        ar_btc_m = "↑" if ip_btc_m else "↓"
        d_btc_m = f"<div style='margin-top:4px;'><span style='color:{dc_btc_m}; font-size:0.85rem; background-color:{dc_btc_m}20; padding:2px 6px; border-radius:4px;'>{ar_btc_m} {abs(dp_btc_m):.2f}%</span></div>"
        btc_html_m = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_m:,.2f}</span>{d_btc_m}</div>"

        # ===========================================
        # CHART 1: SOPR GROUP
        # ===========================================
        col_title_1, k1_1, k2_1, k3_1, k4_1, k5_1 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        
        with col_title_1:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Profit & Loss<br><span style='font-size: 1rem; color: #d1d4dc;'>SOPR Metric</span></h3></div>", unsafe_allow_html=True)
            
        with k1_1: st.markdown(btc_html_m, unsafe_allow_html=True)
        with k2_1: render_kpi_m("aSOPR", last_m.get('aSOPR', 0), prev_m.get('aSOPR', 0), 1.0)
        with k3_1: render_kpi_m("LTH SOPR", last_m.get('LTH SOPR', 0), prev_m.get('LTH SOPR', 0), 1.0)
        with k4_1: render_kpi_m("STH SOPR", last_m.get('STH SOPR', 0), prev_m.get('STH SOPR', 0), 1.0)
        
        st.markdown("---")
        
        df_ms, w_ms = apply_filters(df_mom_raw, st.session_state.tf_ms, st.session_state.sma_ms, st.session_state.cs_ms, st.session_state.tr_ms, st.session_state.cd_ms, ['aSOPR', 'LTH SOPR', 'STH SOPR'])

        col_fs_ms, col_tf_ms, col_sma_ms, col_sma_cst_ms, col_radio_ms, col_custom_ms = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_ms: focus_ms = st.toggle("Full Screen", key="tg_ms")
        with col_tf_ms: st.session_state.tf_ms = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_ms), key="tfs_ms")
        with col_sma_ms: st.session_state.sma_ms = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_ms), key="smas_ms")
        with col_sma_cst_ms:
            if st.session_state.sma_ms == "Custom": st.session_state.cs_ms = st.number_input("Days", min_value=1, value=st.session_state.cs_ms, label_visibility="collapsed", key="cst_ms")
        with col_radio_ms:
            c_idx_ms = t_opts.index(st.session_state.tr_ms) if st.session_state.tr_ms in t_opts else 5
            st.session_state.tr_ms = st.radio("Range:", t_opts, index=c_idx_ms, horizontal=True, label_visibility="collapsed", key="rg_ms")
        with col_custom_ms:
            if st.session_state.tr_ms == "Custom": st.session_state.cd_ms = st.number_input("Days back", min_value=7, value=st.session_state.cd_ms, label_visibility="collapsed", key="cdin_ms")
        
        opts_sopr_base = ['🔵 aSOPR', '🔴 STH SOPR', '🟢 LTH SOPR']
        all_opts_sopr = opts_sopr_base.copy()
        if w_ms > 1: all_opts_sopr.extend([f"{m} (SMA {w_ms})" for m in opts_sopr_base])
            
        try: sel_sopr = st.pills("SOPR Metrics", all_opts_sopr, default=['🔵 aSOPR', '🟢 LTH SOPR'], selection_mode="multi", label_visibility="collapsed")
        except: sel_sopr = st.multiselect("SOPR Metrics", all_opts_sopr, default=['🔵 aSOPR', '🟢 LTH SOPR'], label_visibility="collapsed")

        chart_opts_sopr = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_ms else 650, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": True},
            "scale3": {"visible": False} 
        }
        
        series_sopr = [{"type": 'Line', "data": get_s(df_ms, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        
        df_ms['Neutral_Line'] = 1.0
        series_sopr.append({"type": 'Line', "data": get_s(df_ms, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})

        for m in sel_sopr:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            target_scale = "scale3" if base_m == '🟢 LTH SOPR' else "left"
            
            if base_m == '🔵 aSOPR': 
                c_col = '#00e6e6'
                c_col_raw = 'rgba(0, 230, 230, 0.7)'
                c_name = 'aSOPR'
            elif base_m == '🔴 STH SOPR': 
                c_col = '#ff4d4d'
                c_col_raw = 'rgba(255, 77, 77, 0.7)'
                c_name = 'STH SOPR'
            elif base_m == '🟢 LTH SOPR': 
                c_col = '#00cc66'
                c_col_raw = 'rgba(0, 204, 102, 0.7)'
                c_name = 'LTH SOPR'
            else: continue
            
            if is_sma: 
                series_sopr.append({"type": 'Line', "data": get_s(df_ms, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": target_scale, "title": f"{c_name} SMA"}})
            else: 
                series_sopr.append({"type": 'Line', "data": get_s(df_ms, c_name), "options": {"color": c_col_raw, "lineWidth": 1, "priceScaleId": target_scale, "title": c_name}})
        
        renderLightweightCharts([{"chart": chart_opts_sopr, "series": series_sopr}], 'chart_sopr')
        
        st.markdown("<br><br>", unsafe_allow_html=True)

        # ===========================================
        # CHART 2: REALIZED P/L GROUP
        # ===========================================
        col_title_2, k1_2, k2_2, k3_2, k4_2, k5_2 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        
        with col_title_2:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Profit & Loss<br><span style='font-size: 1rem; color: #d1d4dc;'>Realized P&L Metric</span></h3></div>", unsafe_allow_html=True)
            
        with k1_2: st.markdown(btc_html_m, unsafe_allow_html=True)
        with k2_2: render_kpi_m("Net Realized PL", last_m.get('Net Realized PL', 0), prev_m.get('Net Realized PL', 0), 0.0, True)
        with k3_2: render_kpi_m("STH P/L Ratio", last_m.get('STH P/L Ratio', 0), prev_m.get('STH P/L Ratio', 0), 1.0)
        with k4_2: render_kpi_m("LTH P/L Ratio", last_m.get('LTH P/L Ratio', 0), prev_m.get('LTH P/L Ratio', 0), 1.0)
        
        st.markdown("---")
        
        df_mpl, w_mpl = apply_filters(df_mom_raw, st.session_state.tf_mpl, st.session_state.sma_mpl, st.session_state.cs_mpl, st.session_state.tr_mpl, st.session_state.cd_mpl, ['STH P/L Ratio', 'LTH P/L Ratio', 'Net Realized PL'])

        col_fs_mpl, col_tf_mpl, col_sma_mpl, col_sma_cst_mpl, col_radio_mpl, col_custom_mpl = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_mpl: focus_mpl = st.toggle("Full Screen", key="tg_mpl")
        with col_tf_mpl: st.session_state.tf_mpl = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_mpl), key="tfs_mpl")
        with col_sma_mpl: st.session_state.sma_mpl = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_mpl), key="smas_mpl")
        with col_sma_cst_mpl:
            if st.session_state.sma_mpl == "Custom": st.session_state.cs_mpl = st.number_input("Days", min_value=1, value=st.session_state.cs_mpl, label_visibility="collapsed", key="cst_mpl")
        with col_radio_mpl:
            c_idx_mpl = t_opts.index(st.session_state.tr_mpl) if st.session_state.tr_mpl in t_opts else 5
            st.session_state.tr_mpl = st.radio("Range:", t_opts, index=c_idx_mpl, horizontal=True, label_visibility="collapsed", key="rg_mpl")
        with col_custom_mpl:
            if st.session_state.tr_mpl == "Custom": st.session_state.cd_mpl = st.number_input("Days back", min_value=7, value=st.session_state.cd_mpl, label_visibility="collapsed", key="cdin_mpl")
            
        opts_pl_base = ['⚪ Net Realized PL', '🟣 STH P/L Ratio', '🟤 LTH P/L Ratio']
        all_opts_pl = opts_pl_base.copy()
        if w_mpl > 1: all_opts_pl.extend([f"{m} (SMA {w_mpl})" for m in opts_pl_base])

        try: sel_pl = st.pills("P/L Metrics", all_opts_pl, default=['⚪ Net Realized PL'], selection_mode="multi", label_visibility="collapsed")
        except: sel_pl = st.multiselect("P/L Metrics", all_opts_pl, default=['⚪ Net Realized PL'], label_visibility="collapsed")

        chart_opts_pl = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_mpl else 650, 
            "rightPriceScale": {"visible": True},            
            "leftPriceScale": {"visible": True},             
            "ratio_scale": {"visible": True, "position": "left", "autoScale": True}  
        }
        
        series_pl = [{"type": 'Line', "data": get_s(df_mpl, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        for m in sel_pl:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🟣 STH P/L Ratio':
                c_col_rgba = 'rgba(204, 51, 255, 0.7)'
                c_name = 'STH P/L Ratio'
                if is_sma: series_pl.append({"type": 'Line', "data": get_s(df_mpl, f"{c_name}_SMA"), "options": {"color": c_col_rgba, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'ratio_scale', "title": f"{c_name} SMA"}})
                else: series_pl.append({"type": 'Line', "data": get_s(df_mpl, c_name), "options": {"color": c_col_rgba, "lineWidth": 1, "priceScaleId": 'ratio_scale', "title": c_name}})
            
            elif base_m == '🟤 LTH P/L Ratio':
                c_col_rgba = 'rgba(204, 153, 102, 0.7)'
                c_name = 'LTH P/L Ratio'
                if is_sma: series_pl.append({"type": 'Line', "data": get_s(df_mpl, f"{c_name}_SMA"), "options": {"color": c_col_rgba, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'ratio_scale', "title": f"{c_name} SMA"}})
                else: series_pl.append({"type": 'Line', "data": get_s(df_mpl, c_name), "options": {"color": c_col_rgba, "lineWidth": 1, "priceScaleId": 'ratio_scale', "title": c_name}})
            
            elif base_m == '⚪ Net Realized PL':
                if is_sma:
                    series_pl.append({"type": 'Line', "data": get_s(df_mpl, 'Net Realized PL_SMA'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": "Net PL SMA"}})
                else:
                    net_pl_raw = get_s(df_mpl, 'Net Realized PL')
                    for d in net_pl_raw: d['color'] = 'rgba(0, 204, 102, 0.7)' if d['value'] >= 0 else 'rgba(255, 77, 77, 0.7)'
                    series_pl.append({"type": 'Histogram', "data": net_pl_raw, "options": {"priceScaleId": 'left', "title": 'Net PL Raw'}})

        renderLightweightCharts([{"chart": chart_opts_pl, "series": series_pl}], 'chart_netpl')

# ------------------------------------------------------------------------------
# TAB 3: DERIVATIVES (OPEN INTEREST & FUNDING RATES)
# ------------------------------------------------------------------------------
elif selected_menu == "Derivatives":
    if not df_deriv_raw.empty:
        last_d = df_deriv_raw.iloc[-1]
        prev_d = df_deriv_raw.iloc[-2] if len(df_deriv_raw) > 1 else last_d
        
        btc_d = last_d.get('BTC Price', 0)
        btc_prev_d = prev_d.get('BTC Price', 0)
        
        def render_kpi_d(title, value, prev_val, is_money=False, is_percent=False):
            if pd.isna(value) or value == 0: 
                color = "#a3a8b8"
                d = ""
            else: 
                color = "#00cc66" if value >= 0 else "#ff4d4d"
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                if is_money: diff_str = f"${abs(diff):,.2f}"
                elif is_percent: diff_str = f"{abs(diff):.4f}%"
                else: diff_str = f"{abs(diff):,.0f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"

            if is_money: val_str = f"${value:,.2f}"
            elif is_percent: val_str = f"{value:.4f}%"
            else: val_str = f"{value:,.0f}"
            
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_d = ((btc_d - btc_prev_d) / btc_prev_d * 100) if btc_prev_d else 0
        ip_btc_d = dp_btc_d >= 0
        dc_btc_d = "#00cc66" if ip_btc_d else "#ff4d4d"
        ar_btc_d = "↑" if ip_btc_d else "↓"
        d_btc_d = f"<div style='margin-top:4px;'><span style='color:{dc_btc_d}; font-size:0.85rem; background-color:{dc_btc_d}20; padding:2px 6px; border-radius:4px;'>{ar_btc_d} {abs(dp_btc_d):.2f}%</span></div>"
        btc_html_d = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_d:,.2f}</span>{d_btc_d}</div>"

        col_title, k1, k2, k3, k4, k5 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        
        with col_title:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Derivatives<br><span style='font-size: 1rem; color: #d1d4dc;'>Open Interest & Funding Rates</span></h3></div>", unsafe_allow_html=True)
            
        with k1: st.markdown(btc_html_d, unsafe_allow_html=True)
        with k2: render_kpi_d("Open Interest", last_d.get('Open Interest', 0), prev_d.get('Open Interest', 0), is_money=True)
        with k3: render_kpi_d("Funding Rate", last_d.get('Funding Rate', 0), prev_d.get('Funding Rate', 0), is_percent=True)
        
        st.markdown("---")

        df_d, w_d = apply_filters(df_deriv_raw, st.session_state.tf_d, st.session_state.sma_d, st.session_state.cs_d, st.session_state.tr_d, st.session_state.cd_d, ['Open Interest', 'Funding Rate'])

        col_fs_d, col_tf_d, col_sma_d, col_sma_cst_d, col_radio_d, col_custom_d = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_d: focus_d = st.toggle("Full Screen", key="tg_d")
        with col_tf_d: st.session_state.tf_d = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_d), key="tfs_d")
        with col_sma_d: st.session_state.sma_d = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_d), key="smas_d")
        with col_sma_cst_d:
            if st.session_state.sma_d == "Custom": st.session_state.cs_d = st.number_input("Days", min_value=1, value=st.session_state.cs_d, label_visibility="collapsed", key="cst_d")
        with col_radio_d:
            c_idx_d = t_opts.index(st.session_state.tr_d) if st.session_state.tr_d in t_opts else 5
            st.session_state.tr_d = st.radio("Range:", t_opts, index=c_idx_d, horizontal=True, label_visibility="collapsed", key="rg_d")
        with col_custom_d:
            if st.session_state.tr_d == "Custom": st.session_state.cd_d = st.number_input("Days back", min_value=7, value=st.session_state.cd_d, label_visibility="collapsed", key="cdin_d")
        
        opts_d_base = ['🔵 Open Interest', '📊 Funding Rate']
        all_opts_d = opts_d_base.copy()
        if w_d > 1: all_opts_d.extend([f"{m} (SMA {w_d})" for m in opts_d_base])
            
        try: active_metrics_d = st.pills("Metrics", all_opts_d, default=opts_d_base, selection_mode="multi", label_visibility="collapsed")
        except: active_metrics_d = st.multiselect("Metrics", all_opts_d, default=opts_d_base, label_visibility="collapsed")

        chart_opts_d = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_d else 650, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": True},
            "funding_scale": {"visible": True, "position": "left", "autoScale": True} 
        }
        
        series_d = [{"type": 'Line', "data": get_s(df_d, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        for m in active_metrics_d:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🔵 Open Interest':
                if is_sma:
                    series_d.append({"type": 'Line', "data": get_s(df_d, 'Open Interest_SMA'), "options": {"color": '#4da6ff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": "OI SMA"}})
                else:
                    series_d.append({"type": 'Line', "data": get_s(df_d, 'Open Interest'), "options": {"color": '#4da6ff', "lineWidth": 1, "priceScaleId": 'left', "title": 'Open Interest'}})
            
            elif base_m == '📊 Funding Rate':
                if is_sma:
                    series_d.append({"type": 'Line', "data": get_s(df_d, 'Funding Rate_SMA'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'funding_scale', "title": "Funding SMA"}})
                else:
                    funding_raw = get_s(df_d, 'Funding Rate')
                    for d_val in funding_raw: d_val['color'] = 'rgba(0, 204, 102, 0.7)' if d_val['value'] >= 0 else 'rgba(255, 77, 77, 0.7)'
                    series_d.append({"type": 'Histogram', "data": funding_raw, "options": {"priceScaleId": 'funding_scale', "title": 'Funding Rate'}})

        renderLightweightCharts([{"chart": chart_opts_d, "series": series_d}], 'chart_deriv')

# ------------------------------------------------------------------------------
# TAB 4: SOCIAL SENTIMENT (NEW TAB)
# ------------------------------------------------------------------------------
elif selected_menu == "Social Sentiment":
    if not df_sentiment_raw.empty:
        last_ss = df_sentiment_raw.iloc[-1]
        prev_ss = df_sentiment_raw.iloc[-2] if len(df_sentiment_raw) > 1 else last_ss
        
        btc_ss = last_ss.get('BTC Price', 0)
        btc_prev_ss = prev_ss.get('BTC Price', 0)
        
        def render_kpi_ss(title, value, prev_val):
            if pd.isna(value) or value == 0: 
                color = "#a3a8b8"
                d = ""
            else: 
                color = "#4da6ff" # Biru netral untuk metrik sosial agar tidak disalahpahami sebagai "Profit/Loss"
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                diff_str = f"{abs(diff):,.0f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"

            val_str = f"{value:,.0f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_ss = ((btc_ss - btc_prev_ss) / btc_prev_ss * 100) if btc_prev_ss else 0
        ip_btc_ss = dp_btc_ss >= 0
        dc_btc_ss = "#00cc66" if ip_btc_ss else "#ff4d4d"
        ar_btc_ss = "↑" if ip_btc_ss else "↓"
        d_btc_ss = f"<div style='margin-top:4px;'><span style='color:{dc_btc_ss}; font-size:0.85rem; background-color:{dc_btc_ss}20; padding:2px 6px; border-radius:4px;'>{ar_btc_ss} {abs(dp_btc_ss):.2f}%</span></div>"
        btc_html_ss = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_ss:,.2f}</span>{d_btc_ss}</div>"

        # ===========================================
        # CHART 1: GOOGLE TRENDS
        # ===========================================
        col_title_1, k1_1, k2_1, k3_1, k4_1, k5_1 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        
        with col_title_1:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Social Sentiment<br><span style='font-size: 1rem; color: #d1d4dc;'>Google Trends</span></h3></div>", unsafe_allow_html=True)
            
        with k1_1: st.markdown(btc_html_ss, unsafe_allow_html=True)
        with k2_1: render_kpi_ss("Google Trend (BTC)", last_ss.get('Google Trend (BTC)', 0), prev_ss.get('Google Trend (BTC)', 0))
        with k3_1: render_kpi_ss("Google Trend (Crypto)", last_ss.get('Google Trend (Crypto)', 0), prev_ss.get('Google Trend (Crypto)', 0))
        
        st.markdown("---")

        df_ss, w_ss = apply_filters(df_sentiment_raw, st.session_state.tf_ss, st.session_state.sma_ss, st.session_state.cs_ss, st.session_state.tr_ss, st.session_state.cd_ss, ['Google Trend (BTC)', 'Google Trend (Crypto)', 'Wiki (BTC)', 'Wiki (Crypto)'])

        col_fs_ss, col_tf_ss, col_sma_ss, col_sma_cst_ss, col_radio_ss, col_custom_ss = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_ss: focus_ss = st.toggle("Full Screen", key="tg_ss")
        with col_tf_ss: st.session_state.tf_ss = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_ss), key="tfs_ss")
        with col_sma_ss: st.session_state.sma_ss = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_ss), key="smas_ss")
        with col_sma_cst_ss:
            if st.session_state.sma_ss == "Custom": st.session_state.cs_ss = st.number_input("Days", min_value=1, value=st.session_state.cs_ss, label_visibility="collapsed", key="cst_ss")
        with col_radio_ss:
            c_idx_ss = t_opts.index(st.session_state.tr_ss) if st.session_state.tr_ss in t_opts else 5
            st.session_state.tr_ss = st.radio("Range:", t_opts, index=c_idx_ss, horizontal=True, label_visibility="collapsed", key="rg_ss")
        with col_custom_ss:
            if st.session_state.tr_ss == "Custom": st.session_state.cd_ss = st.number_input("Days back", min_value=7, value=st.session_state.cd_ss, label_visibility="collapsed", key="cdin_ss")
        
        opts_ss_base = ['🔵 Google Trend (BTC)', '🟣 Google Trend (Crypto)']
        all_opts_ss = opts_ss_base.copy()
        if w_ss > 1: all_opts_ss.extend([f"{m} (SMA {w_ss})" for m in opts_ss_base])
            
        # Menambahkan Pilihan Chart Mode (Line vs Stacked) di samping metrik
        col_pills_ss, col_style_ss = st.columns([8, 2], vertical_alignment="center")
        with col_pills_ss:
            try: sel_ss = st.pills("Trend Metrics", all_opts_ss, default=['🔵 Google Trend (BTC)', '🟣 Google Trend (Crypto)'], selection_mode="multi", label_visibility="collapsed", key="pills_gtrend")
            except: sel_ss = st.multiselect("Trend Metrics", all_opts_ss, default=['🔵 Google Trend (BTC)', '🟣 Google Trend (Crypto)'], label_visibility="collapsed", key="ms_gtrend")
        with col_style_ss:
            mode_ss = st.radio("Style", ["Line", "Stacked Area"], horizontal=True, label_visibility="collapsed", key="mode_gtrend_rad")

        chart_opts_ss = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_ss else 650, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": True}
        }
        
        series_ss = [{"type": 'Line', "data": get_s(df_ss, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        # Helper warna 
        def get_color_configs(name):
            configs = {
                'Google Trend (BTC)': {'hex': '#4da6ff', 'top': 'rgba(77, 166, 255, 0.6)', 'bot': 'rgba(77, 166, 255, 0.0)'},
                'Google Trend (Crypto)': {'hex': '#cc33ff', 'top': 'rgba(204, 51, 255, 0.6)', 'bot': 'rgba(204, 51, 255, 0.0)'},
                'Wiki (BTC)': {'hex': '#ffffff', 'top': 'rgba(255, 255, 255, 0.6)', 'bot': 'rgba(255, 255, 255, 0.0)'},
                'Wiki (Crypto)': {'hex': '#00cc66', 'top': 'rgba(0, 204, 102, 0.6)', 'bot': 'rgba(0, 204, 102, 0.0)'}
            }
            return configs.get(name, {'hex': '#888888', 'top': 'rgba(136,136,136,0.6)', 'bot': 'rgba(136,136,136,0.0)'})

        if mode_ss == "Stacked Area":
            cum_series = []
            current_sum = pd.Series(0.0, index=df_ss.index)
            for m in sel_ss:
                is_sma = "(SMA" in m
                base_m = m.split(" (SMA")[0].split(' ', 1)[1] # Ambil nama asli dari '🔵 Google Trend (BTC)'
                col_target = f"{base_m}_SMA" if is_sma else base_m
                
                if col_target in df_ss.columns:
                    current_sum = current_sum + df_ss[col_target].fillna(0)
                    temp_col = f"{col_target}_stacked"
                    df_ss[temp_col] = current_sum
                    c_conf = get_color_configs(base_m)
                    
                    area_opts = {
                        "lineColor": c_conf['hex'],
                        "topColor": c_conf['top'],
                        "bottomColor": c_conf['bot'],
                        "lineWidth": 1,
                        "priceScaleId": 'left',
                        "title": col_target
                    }
                    cum_series.append({"type": 'Area', "data": get_s(df_ss, temp_col), "options": area_opts})
            
            # Stacked series dibalik urutannya agar area yg besar di belakang, kecil di depan
            series_ss.extend(cum_series[::-1])
        else:
            for m in sel_ss:
                is_sma = "(SMA" in m
                base_m = m.split(" (SMA")[0].split(' ', 1)[1]
                col_target = f"{base_m}_SMA" if is_sma else base_m
                if col_target in df_ss.columns:
                    c_conf = get_color_configs(base_m)
                    series_ss.append({"type": 'Line', "data": get_s(df_ss, col_target), "options": {"color": c_conf['hex'], "lineWidth": 1, "lineStyle": 2 if is_sma else 1, "priceScaleId": 'left', "title": col_target}})

        renderLightweightCharts([{"chart": chart_opts_ss, "series": series_ss}], 'chart_gtrend')
        
        with st.expander("ℹ️ About Google Trends (Crypto Search Interest)"):
            st.markdown("""
            **What this shows:** This chart plots worldwide Google search interest for major crypto keywords alongside Bitcoin price. Values are relative (0 to 100), where 100 is the all-time peak for the most-searched term in the series (Bitcoin).

            **How to read it:** * Bitcoin searches tend to spike near cycle tops (late 2013, Dec 2017, Nov 2021).  
            * Altcoin-specific terms tend to lag Bitcoin and reflect retail speculation phases.
            """)

        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ===========================================
        # CHART 2: WIKIPEDIA PAGEVIEWS
        # ===========================================
        col_title_2, k1_2, k2_2, k3_2, k4_2, k5_2 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        
        with col_title_2:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Social Sentiment<br><span style='font-size: 1rem; color: #d1d4dc;'>Wikipedia Pageviews</span></h3></div>", unsafe_allow_html=True)
            
        with k1_2: st.markdown(btc_html_ss, unsafe_allow_html=True)
        with k2_2: render_kpi_ss("Wiki (BTC)", last_ss.get('Wiki (BTC)', 0), prev_ss.get('Wiki (BTC)', 0))
        with k3_2: render_kpi_ss("Wiki (Crypto)", last_ss.get('Wiki (Crypto)', 0), prev_ss.get('Wiki (Crypto)', 0))
        
        st.markdown("---")
        
        opts_ss_wiki = ['⚪ Wiki (BTC)', '🟢 Wiki (Crypto)']
        all_opts_ss_wiki = opts_ss_wiki.copy()
        if w_ss > 1: all_opts_ss_wiki.extend([f"{m} (SMA {w_ss})" for m in opts_ss_wiki])
            
        col_pills_wiki, col_style_wiki = st.columns([8, 2], vertical_alignment="center")
        with col_pills_wiki:
            try: sel_ss_wiki = st.pills("Wiki Metrics", all_opts_ss_wiki, default=['⚪ Wiki (BTC)', '🟢 Wiki (Crypto)'], selection_mode="multi", label_visibility="collapsed", key="pills_wiki")
            except: sel_ss_wiki = st.multiselect("Wiki Metrics", all_opts_ss_wiki, default=['⚪ Wiki (BTC)', '🟢 Wiki (Crypto)'], label_visibility="collapsed", key="ms_wiki")
        with col_style_wiki:
            mode_ss_wiki = st.radio("Style", ["Line", "Stacked Area"], horizontal=True, label_visibility="collapsed", key="mode_wiki_rad")

        chart_opts_ss_wiki = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_ss else 650, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": True}
        }
        
        series_ss_wiki = [{"type": 'Line', "data": get_s(df_ss, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        if mode_ss_wiki == "Stacked Area":
            cum_series_wiki = []
            current_sum_wiki = pd.Series(0.0, index=df_ss.index)
            for m in sel_ss_wiki:
                is_sma = "(SMA" in m
                base_m = m.split(" (SMA")[0].split(' ', 1)[1]
                col_target = f"{base_m}_SMA" if is_sma else base_m
                
                if col_target in df_ss.columns:
                    current_sum_wiki = current_sum_wiki + df_ss[col_target].fillna(0)
                    temp_col = f"{col_target}_stacked_wiki"
                    df_ss[temp_col] = current_sum_wiki
                    c_conf = get_color_configs(base_m)
                    
                    area_opts = {
                        "lineColor": c_conf['hex'],
                        "topColor": c_conf['top'],
                        "bottomColor": c_conf['bot'],
                        "lineWidth": 1,
                        "priceScaleId": 'left',
                        "title": col_target
                    }
                    cum_series_wiki.append({"type": 'Area', "data": get_s(df_ss, temp_col), "options": area_opts})
            
            series_ss_wiki.extend(cum_series_wiki[::-1])
        else:
            for m in sel_ss_wiki:
                is_sma = "(SMA" in m
                base_m = m.split(" (SMA")[0].split(' ', 1)[1]
                col_target = f"{base_m}_SMA" if is_sma else base_m
                if col_target in df_ss.columns:
                    c_conf = get_color_configs(base_m)
                    series_ss_wiki.append({"type": 'Line', "data": get_s(df_ss, col_target), "options": {"color": c_conf['hex'], "lineWidth": 1, "lineStyle": 2 if is_sma else 1, "priceScaleId": 'left', "title": col_target}})

        renderLightweightCharts([{"chart": chart_opts_ss_wiki, "series": series_ss_wiki}], 'chart_wiki')

        with st.expander("ℹ️ About Wikipedia Pageviews (Crypto Attention)"):
            st.markdown("""
            **What this shows:** This chart plots daily Wikipedia pageviews for major crypto-related articles alongside Bitcoin price. Values are absolute view counts from the English Wikipedia (bots excluded).

            **Why Wikipedia?** When retail interest in crypto spikes, so do visits to foundational Wikipedia articles. Unlike Google Trends, pageview counts are absolute, so you can compare attention directly across articles and eras.

            **How to read it:** * Bitcoin pageviews spike near cycle tops.  
            * Newer chain articles only appear once the chain gains mainstream attention.
            """)

    else:
        st.info("Menunggu data Social Sentiment. Pastikan script auto_update.py sudah menarik data terbaru!")
