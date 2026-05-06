import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PAGE CONFIGURATION & SESSION STATE
# ==============================================================================
st.set_page_config(page_title="Yudiyanto | On-Chain Dashboard", layout="wide", initial_sidebar_state="collapsed")

# Inisialisasi State Independen untuk masing-masing Tab
for tab in ['p', 'm']:
    if f'tr_{tab}' not in st.session_state: st.session_state[f'tr_{tab}'] = "All Time"
    if f'cd_{tab}' not in st.session_state: st.session_state[f'cd_{tab}'] = 120
    if f'tf_{tab}' not in st.session_state: st.session_state[f'tf_{tab}'] = "Daily"
    if f'sma_{tab}' not in st.session_state: st.session_state[f'sma_{tab}'] = "0d"
    if f'cs_{tab}' not in st.session_state: st.session_state[f'cs_{tab}'] = 50

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

# Mesin filter dengan perhitungan Dual SMA
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
        
    # 2. Smoothing (SMA) - Menghasilkan kolom baru dengan akhiran _SMA
    w = 1
    if smooth_state == "7d": w = 7
    elif smooth_state == "14d": w = 14
    elif smooth_state == "30d": w = 30
    elif smooth_state == "Custom": w = custom_smooth
    if w > 1:
        for c in metrics_to_smooth:
            if c in dff.columns: dff[f"{c}_SMA"] = dff[c].rolling(w, min_periods=1).mean()
                    
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
        header_p, controls_p, chart_p = st.container(), st.container(), st.container()

        # 1. HEADER & KPI
        with header_p:
            st.title("On-Chain Price Levels")
            st.markdown("Bitcoin's current market price alongside fundamental price levels derived from on-chain metrics.")
            st.markdown("---")
            
            # Hitung data sementara untuk KPI (Tanpa smoothing agar KPI selalu real-time)
            df_temp_p, _ = apply_filters(df_price_raw, "Daily", "0d", 1, st.session_state.tr_p, st.session_state.cd_p, [])
            last_p = df_temp_p.iloc[-1] if not df_temp_p.empty else pd.Series()
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

        # 2. KONTROL & SELEKSI METRIK
        with controls_p:
            col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
            with col_fs: focus_p = st.toggle("Full Screen", key="tg_p")
            with col_tf: st.session_state.tf_p = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_p), key="tfs_p")
            with col_sma: st.session_state.sma_p = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_p), key="smas_p")
            with col_sma_cst:
                if st.session_state.sma_p == "Custom": st.session_state.cs_p = st.number_input("Days", min_value=1, value=st.session_state.cs_p, label_visibility="collapsed", key="cst_p")
            with col_radio:
                t_opts = ["1 Month", "3 Months", "6 Months", "1 Year", "4 Years (Cycle)", "All Time", "Custom"]
                c_idx = t_opts.index(st.session_state.tr_p) if st.session_state.tr_p in t_opts else 5
                st.session_state.tr_p = st.radio("Range:", t_opts, index=c_idx, horizontal=True, label_visibility="collapsed", key="rg_p")
            with col_custom:
                if st.session_state.tr_p == "Custom": st.session_state.cd_p = st.number_input("Days back", min_value=7, value=st.session_state.cd_p, label_visibility="collapsed", key="cdin_p")
            
            # Terapkan Filter Data
            df_p, w_p = apply_filters(df_price_raw, st.session_state.tf_p, st.session_state.sma_p, st.session_state.cs_p, st.session_state.tr_p, st.session_state.cd_p, ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD'])

            # Dinamika Tombol Metrik (Menambah tombol SMA jika aktif)
            base_metrics_p = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD']
            all_opts_p = []
            for m in base_metrics_p:
                all_opts_p.append(m)
                if w_p > 1: all_opts_p.append(f"{m} (SMA)")
            
            try: active_metrics_p = st.pills("Metrics", all_opts_p, default=base_metrics_p, selection_mode="multi", label_visibility="collapsed")
            except: active_metrics_p = st.multiselect("Metrics", all_opts_p, default=base_metrics_p, label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)

        # 3. RENDER CHART
        with chart_p:
            if focus_p: st.markdown("""<style>.block-container{padding-top:1rem; padding-bottom:1rem; max-width:100%;} header, footer{visibility:hidden;}</style>""", unsafe_allow_html=True)
            chart_p_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_p else 650}
            
            series_p = [{"type": 'Line', "data": get_s(df_p, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 3, "title": 'BTC Price'}}]
            colors_p = {'🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis'), '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis'), '⚪ Realized Price': ('#ffffff', 'Realized Price'), '🟣 True Market Mean': ('#cc33ff', 'True Market Mean'), '🟢 CVDD': ('#00cc66', 'CVDD')}
            
            for m in active_metrics_p:
                is_sma = "(SMA)" in m
                base_m = m.replace(" (SMA)", "")
                if base_m in colors_p:
                    met_color = colors_p[base_m][0]
                    col_name = f"{colors_p[base_m][1]}_SMA" if is_sma else colors_p[base_m][1]
                    lw = 1 if is_sma else 2
                    ls = 2 if is_sma else 0 # 2 is Dashed
                    series_p.append({"type": 'Line', "data": get_s(df_p, col_name), "options": {"color": met_color, "lineWidth": lw, "lineStyle": ls, "title": f"{colors_p[base_m][1]} {'SMA '+str(w_p) if is_sma else 'Raw'}"}})
            
            renderLightweightCharts([{"chart": chart_p_opts, "series": series_p}], 'chart_price')

# ------------------------------------------------------------------------------
# TAB 2: PROFIT & LOSS (DUAL CHART)
# ------------------------------------------------------------------------------
with tab2:
    if not df_mom_raw.empty:
        header_m, controls_m, chart_m_sopr, chart_m_pl = st.container(), st.container(), st.container(), st.container()

        # 1. HEADER & KPI
        with header_m:
            st.title("Profit & Loss")
            st.markdown("Track investor behavior, greed, and fear using SOPR and Realized Profit/Loss.")
            st.markdown("---")
            
            df_temp_m, _ = apply_filters(df_mom_raw, "Daily", "0d", 1, st.session_state.tr_m, st.session_state.cd_m, [])
            last_m = df_temp_m.iloc[-1] if not df_temp_m.empty else pd.Series()
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

        # 2. KONTROL & SELEKSI METRIK
        with controls_m:
            col_fs, col_tf, col_sma, col_sma_cst, col_space, col_radio, col_custom = st.columns([1.2, 1.5, 1.5, 1, 0.5, 5, 1.2], vertical_alignment="bottom")
            with col_fs: focus_m = st.toggle("Full Screen", key="tg_m")
            with col_tf: st.session_state.tf_m = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_m), key="tfs_m")
            with col_sma: st.session_state.sma_m = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_m), key="smas_m")
            with col_sma_cst:
                if st.session_state.sma_m == "Custom": st.session_state.cs_m = st.number_input("Days", min_value=1, value=st.session_state.cs_m, label_visibility="collapsed", key="cst_m")
            with col_radio:
                c_idx_m = t_opts.index(st.session_state.tr_m) if st.session_state.tr_m in t_opts else 5
                st.session_state.tr_m = st.radio("Range:", t_opts, index=c_idx_m, horizontal=True, label_visibility="collapsed", key="rg_m")
            with col_custom:
                if st.session_state.tr_m == "Custom": st.session_state.cd_m = st.number_input("Days back", min_value=7, value=st.session_state.cd_m, label_visibility="collapsed", key="cdin_m")
            
            # Terapkan Filter Data
            df_m, w_m = apply_filters(df_mom_raw, st.session_state.tf_m, st.session_state.sma_m, st.session_state.cs_m, st.session_state.tr_m, st.session_state.cd_m, ['aSOPR', 'LTH SOPR', 'STH SOPR', 'STH P/L Ratio', 'LTH P/L Ratio', 'Net Realized PL'])

            # Pisahkan menu Tombol untuk Chart 1 (SOPR) dan Chart 2 (Realized PL)
            base_sopr = ['🔵 aSOPR', '🔴 STH SOPR', '🟢 LTH SOPR']
            base_pl = ['⚪ Net Realized PL', '🟣 STH P/L Ratio', '🟤 LTH P/L Ratio']
            
            opts_sopr, opts_pl = [], []
            for m in base_sopr:
                opts_sopr.append(m)
                if w_m > 1: opts_sopr.append(f"{m} (SMA)")
            for m in base_pl:
                opts_pl.append(m)
                if w_m > 1: opts_pl.append(f"{m} (SMA)")

            st.markdown("**Chart 1: SOPR Metrics**")
            try: sel_sopr = st.pills("C1", opts_sopr, default=['🔵 aSOPR'], selection_mode="multi", label_visibility="collapsed")
            except: sel_sopr = st.multiselect("C1", opts_sopr, default=['🔵 aSOPR'], label_visibility="collapsed")
            
            st.markdown("**Chart 2: Realized Profit/Loss Metrics**")
            try: sel_pl = st.pills("C2", opts_pl, default=['⚪ Net Realized PL'], selection_mode="multi", label_visibility="collapsed")
            except: sel_pl = st.multiselect("C2", opts_pl, default=['⚪ Net Realized PL'], label_visibility="collapsed")
            st.markdown("<br>", unsafe_allow_html=True)

        if focus_m: st.markdown("""<style>.block-container{padding-top:1rem; padding-bottom:1rem; max-width:100%;} header, footer{visibility:hidden;}</style>""", unsafe_allow_html=True)

        # Base Chart Configuration
        base_chart_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 500 if focus_m else 400, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}

        df_m['Neutral_Line'] = 1.0

        # 3. RENDER CHART 1 (SOPR)
        with chart_m_sopr:
            series_c1 = [{"type": 'Line', "data": get_s(df_m, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
            series_c1.append({"type": 'Line', "data": get_s(df_m, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})
            
            c_map_sopr = {'🔵 aSOPR': ('#00e6e6', 'aSOPR'), '🔴 STH SOPR': ('#ff4d4d', 'STH SOPR'), '🟢 LTH SOPR': ('#00cc66', 'LTH SOPR')}
            for m in sel_sopr:
                is_sma = "(SMA)" in m
                base_m = m.replace(" (SMA)", "")
                if base_m in c_map_sopr:
                    met_color, met_name = c_map_sopr[base_m][0], c_map_sopr[base_m][1]
                    col_name = f"{met_name}_SMA" if is_sma else met_name
                    lw, ls = (1, 2) if is_sma else (2, 0)
                    series_c1.append({"type": 'Line', "data": get_s(df_m, col_name), "options": {"color": met_color, "lineWidth": lw, "lineStyle": ls, "priceScaleId": 'left', "title": f"{met_name} {'SMA '+str(w_m) if is_sma else 'Raw'}"}})
            renderLightweightCharts([{"chart": base_chart_opts, "series": series_c1}], 'chart_m1')

        # 4. RENDER CHART 2 (REALIZED P/L)
        with chart_m_pl:
            st.markdown("<br>", unsafe_allow_html=True) # Jarak antar chart
            
            # Modifikasi khusus Chart 2: Skala ketiga untuk Histogram Net PL agar tidak merusak harga BTC
            opts_c2 = base_chart_opts.copy()
            opts_c2["netPlScale"] = {"visible": False} # Skala khusus tidak terlihat di sumbu

            series_c2 = [{"type": 'Line', "data": get_s(df_m, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
            series_c2.append({"type": 'Line', "data": get_s(df_m, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})

            c_map_pl = {'⚪ Net Realized PL': ('#ffffff', 'Net Realized PL'), '🟣 STH P/L Ratio': ('#cc33ff', 'STH P/L Ratio'), '🟤 LTH P/L Ratio': ('#cc9966', 'LTH P/L Ratio')}
            for m in sel_pl:
                is_sma = "(SMA)" in m
                base_m = m.replace(" (SMA)", "")
                if base_m in c_map_pl:
                    met_color, met_name = c_map_pl[base_m][0], c_map_pl[base_m][1]
                    col_name = f"{met_name}_SMA" if is_sma else met_name
                    lw, ls = (1, 2) if is_sma else (2, 0)
                    
                    if met_name == 'Net Realized PL':
                        if not is_sma:
                            net_pl_raw = get_s(df_m, col_name)
                            for d in net_pl_raw: d['color'] = '#00cc66' if d['value'] >= 0 else '#ff4d4d'
                            series_c2.append({"type": 'Histogram', "data": net_pl_raw, "options": {"priceScaleId": 'netPlScale', "title": 'Net PL Raw'}})
                        else:
                            series_c2.append({"type": 'Line', "data": get_s(df_m, col_name), "options": {"color": met_color, "lineWidth": lw, "lineStyle": ls, "priceScaleId": 'netPlScale', "title": f"Net PL SMA {w_m}"}})
                    else:
                        series_c2.append({"type": 'Line', "data": get_s(df_m, col_name), "options": {"color": met_color, "lineWidth": lw, "lineStyle": ls, "priceScaleId": 'left', "title": f"{met_name} {'SMA '+str(w_m) if is_sma else 'Raw'}"}})
            renderLightweightCharts([{"chart": opts_c2, "series": series_c2}], 'chart_m2')

    else:
        st.info("Menunggu data Profit & Loss. Pastikan GitHub Actions sudah jalan!")

with tab3:
    st.info("Oscillators chart is under construction. Coming soon!")
