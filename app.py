import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts_ntf import renderLightweightCharts
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ==============================================================================
# 1. PAGE CONFIGURATION, SESSION STATE & CSS
# ==============================================================================
st.set_page_config(
    page_title="Yudiyanto | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
/* Sidebar Tabs */
section[data-testid="stSidebar"] { background-color: #151924; }
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] { gap: 10px; }
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label {
    background-color: #1a1d24; padding: 12px 16px !important; border-radius: 8px !important;
    border-left: 4px solid transparent; margin: 0 !important; cursor: pointer; transition: all 0.2s ease-in-out;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label:hover { background-color: #262a35; }
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label[data-checked="true"] {
    border-left: 4px solid #a855f7 !important; background-color: #2a203b !important;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] p {
    font-size: 1.15rem !important; font-weight: 600 !important; margin: 0 !important; color: #ffffff !important;
}
section[data-testid="stSidebar"] div.stRadio > div[role="radiogroup"] > label > div:first-child { display: none !important; }

/* Control Panel Inputs */
div[data-testid="stSelectbox"] *, div[data-testid="stRadio"] *, div[data-testid="stToggle"] *, div[data-testid="stNumberInput"] * {
    font-size: 0.85rem !important;
}

div[data-testid="stRadio"] label p { font-size: 0.85rem !important; margin-top: 3px !important; }
div[data-testid="stToggle"] label p { font-size: 0.85rem !important; margin-top: 3px !important; }
div[data-testid="stSelectbox"] label, div[data-testid="stNumberInput"] label { padding-bottom: 2px !important; min-height: 0px !important; }
div[data-baseweb="select"] > div { min-height: 32px !important; height: 32px !important; border-radius: 6px !important; padding-top: 4px !important; padding-bottom: 0px !important; }
div[data-baseweb="select"] > div > div { padding-top: 0px !important; padding-bottom: 0px !important; }
div[data-baseweb="select"] span { display: inline-block; }

/* Spasi & Pills */
.block-container { padding-top: 3rem !important; padding-bottom: 1.5rem !important; max-width: 100%; }
div[data-testid="stPill"] button { font-size: 0.85rem !important; padding: 2px 12px !important; min-height: 28px !important; }
</style>
""", unsafe_allow_html=True)

# State initialization (Termasuk ex untuk Exchange Flow)
for key in ['tr_p', 'tr_mv', 'tr_ms', 'tr_mpl', 'tr_nupl', 'tr_d', 'tr_ex', 'tr_gt', 'tr_wk', 'tr_sd', 'tr_fg', 'tr_msig', 'tr_bt', 'tr_sl', 'tr_pl']:
    if key not in st.session_state: st.session_state[key] = "All Time"
for key in ['cd_p', 'cd_mv', 'cd_ms', 'cd_mpl', 'cd_nupl', 'cd_d', 'cd_ex', 'cd_gt', 'cd_wk', 'cd_sd', 'cd_fg', 'cd_msig', 'cd_bt', 'cd_sl', 'cd_pl']:
    if key not in st.session_state: st.session_state[key] = 120
for key in ['tf_p', 'tf_mv', 'tf_ms', 'tf_mpl', 'tf_nupl', 'tf_d', 'tf_ex', 'tf_gt', 'tf_wk', 'tf_sd', 'tf_fg', 'tf_msig', 'tf_bt', 'tf_sl', 'tf_pl']:
    if key not in st.session_state: st.session_state[key] = "Daily"
for key, val in [('sl_sma_a', 14), ('sl_sma_b', 30), ('sl_sma_c', 60), ('sl_b5_thresh', 1.10)]:
    if key not in st.session_state: st.session_state[key] = val
for key in ['sma_p', 'sma_mv', 'sma_ms', 'sma_mpl', 'sma_nupl', 'sma_d', 'sma_ex', 'sma_sd', 'sma_fg', 'sma_msig', 'sma_pl']:
    if key not in st.session_state: st.session_state[key] = "0d"
for key in ['sma_gt', 'sma_wk']:
    if key not in st.session_state: st.session_state[key] = "30d"  
for key in ['cs_p', 'cs_mv', 'cs_ms', 'cs_mpl', 'cs_nupl', 'cs_d', 'cs_ex', 'cs_gt', 'cs_wk', 'cs_sd', 'cs_fg', 'cs_msig']:
    if key not in st.session_state: st.session_state[key] = 50
if 'cs_pl' not in st.session_state: st.session_state['cs_pl'] = 0
for key in ['cs_pl1', 'cs_pl2', 'cs_pl3']:
    if key not in st.session_state: st.session_state[key] = 0
for key in ['smooth_type_pl1', 'smooth_type_pl2', 'smooth_type_pl3']:
    if key not in st.session_state: st.session_state[key] = "SMA"
for key in ['tr_pl1', 'tr_pl2', 'tr_pl3']:
    if key not in st.session_state: st.session_state[key] = "All Time"
for key in ['cd_pl1', 'cd_pl2', 'cd_pl3']:
    if key not in st.session_state: st.session_state[key] = 120
for key in ['tf_pl1', 'tf_pl2', 'tf_pl3']:
    if key not in st.session_state: st.session_state[key] = "Daily"
for key in ['mode_gt', 'mode_wk']:
    if key not in st.session_state: st.session_state[key] = "Line"

# Backtesting Engine state
DEFAULT_BT_CODE = '''# Kolom tersedia: Date, BTC Price, MVRV, STH MVRV, LTH MVRV,
# aSOPR, LTH SOPR, STH SOPR, NUPL, STH NUPL, LTH NUPL,
# Net Realized PL, STH P/L Ratio, LTH P/L Ratio,
# Open Interest, Funding Rate, Net Flow, Total Balance,
# LTH Supply, STH Supply, LTH % Profit, STH % Profit, Total % Profit,
# STH Cost Basis, LTH Cost Basis, Realized Price, CVDD, True Market Mean
#
# Wajib: assign boolean Series ke variabel "buy" dan "sell"
# Contoh: aSOPR cross below BB lower band

import pandas_ta as ta

bb = ta.bbands(df["aSOPR"].ffill(), length=50, std=2.5)
if bb is not None:
    bb_lower = bb.iloc[:, 0]
    bb_upper = bb.iloc[:, 2]
    buy  = (df["aSOPR"] < bb_lower) & (df["aSOPR"].shift(1) >= bb_lower.shift(1))
    sell = (df["aSOPR"] > bb_upper) & (df["aSOPR"].shift(1) <= bb_upper.shift(1))
else:
    buy  = pd.Series(False, index=df.index)
    sell = pd.Series(False, index=df.index)
'''
if 'bt_code' not in st.session_state: st.session_state['bt_code'] = DEFAULT_BT_CODE
if 'bt_capital' not in st.session_state: st.session_state['bt_capital'] = 10000.0
if 'bt_result' not in st.session_state: st.session_state['bt_result'] = None

# ==============================================================================
# 2. DATA LOADING & FILTERING ENGINE
# ==============================================================================
@st.cache_data(ttl=3600)
def load_data_price():
    try:
        df = pd.read_csv("data_price_level.csv")
        df.rename(columns={
            'date': 'Date', 'btc_price': 'BTC Price', 'sth_cost_basis': 'STH Cost Basis', 
            'lth_cost_basis': 'LTH Cost Basis', 'realized_price': 'Realized Price', 
            'cvdd': 'CVDD', 'true_market_mean_price': 'True Market Mean',
            'active_realized_price': 'Active Realized Price', 'MVRV 0σ': 'MVRV 0σ',
            'cum_pl_price': 'Cum P/L Price', 'pl_price_ratio': 'P/L Price Ratio',
            '200_dma': '200 DMA', '50_wma': '50 WMA', '200_wma': '200 WMA'
        }, inplace=True)
        # ... (sisa kodenya biarkan sama)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
        
        delta = df['BTC Price'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.ewm(alpha=1/14, adjust=False).mean()
        avg_loss = loss.ewm(alpha=1/14, adjust=False).mean()
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_mvrv():
    try:
        df = pd.read_csv("data_mvrv.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'mvrv': 'MVRV', 'mvrv_ratio': 'MVRV', 'sth_mvrv': 'STH MVRV', 'lth_mvrv': 'LTH MVRV'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_momentum():
    try:
        df = pd.read_csv("data_momentum.csv")
        df.rename(columns={
            'date': 'Date', 'btc_price': 'BTC Price', 'asopr': 'aSOPR', 'lth_sopr': 'LTH SOPR', 'sth_sopr': 'STH SOPR',
            'net_realized_pl_usd': 'Net Realized PL',
            'nupl': 'NUPL', 'sth_nupl': 'STH NUPL', 'lth_nupl': 'LTH NUPL'
        }, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
        # STH/LTH P/L Ratio sudah dipindahkan ke data_pl.csv — load dan merge di sini
        try:
            df_pl = pd.read_csv("data_pl.csv")[['date', 'sth_pl_ratio', 'lth_pl_ratio']]
            df_pl.rename(columns={'date': 'Date', 'sth_pl_ratio': 'STH P/L Ratio', 'lth_pl_ratio': 'LTH P/L Ratio'}, inplace=True)
            df_pl['Date'] = pd.to_datetime(df_pl['Date'], errors='coerce')
            df = pd.merge(df, df_pl, on='Date', how='left')
        except Exception:
            df['STH P/L Ratio'] = 1.0
            df['LTH P/L Ratio'] = 1.0
        df['LTH P/L Ratio'] = df['LTH P/L Ratio'].ffill().fillna(1.0)
        df['STH P/L Ratio'] = df['STH P/L Ratio'].ffill().fillna(1.0)
        return df
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_derivatives():
    try:
        df = pd.read_csv("data_derivatives.csv")
        df.rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'total_oi': 'Open Interest', 'funding_rate': 'Funding Rate'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_exchange():
    try:
        df = pd.read_csv("data_exchange.csv")
        df.rename(columns={
            'date': 'Date', 'btc_price': 'BTC Price', 'total_balance': 'Total Balance', 
            'net_flow': 'Net Flow', 'inflow': 'Inflow', 'outflow': 'Outflow'
        }, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_sentiment():
    try:
        df = pd.read_csv("data_sentiment.csv")
        df.rename(columns={
            'date': 'Date', 'btc_price': 'BTC Price',
            'trend_bitcoin': 'GTrend BTC', 'trend_crypto': 'GTrend Crypto', 'trend_ethereum': 'GTrend ETH',
            'trend_nft': 'GTrend NFT', 'trend_binance': 'GTrend Binance', 'trend_solana': 'GTrend SOL', 'trend_dogecoin': 'GTrend DOGE',
            'wiki_bitcoin': 'Wiki BTC', 'wiki_cryptocurrency': 'Wiki Crypto', 'wiki_ethereum': 'Wiki ETH',
            'wiki_satoshi_nakamoto': 'Wiki Satoshi', 'wiki_blockchain': 'Wiki Blockchain', 'wiki_nft': 'Wiki NFT', 'wiki_dogecoin': 'Wiki DOGE'
        }, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_supply():
    try:
        df = pd.read_csv("data_supply.csv")
        df.rename(columns={
            'date': 'Date', 'btc_price': 'BTC Price',
            'lth_supply_btc': 'LTH Supply', 'sth_supply_btc': 'STH Supply', 
            'pct_lth_in_profit': 'LTH % Profit', 'pct_sth_in_profit': 'STH % Profit',
            'pct_lth_in_loss': 'LTH % Loss', 'pct_sth_in_loss': 'STH % Loss',
            'percent_btc_in_profit': 'Total % Profit', 'percent_btc_in_loss': 'Total % Loss'
        }, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_fg():
    try:
        df = pd.read_csv("data_fg.csv")
        df['Date'] = pd.to_datetime(df['date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_cum():
    try:
        df = pd.read_csv("data_cum_pl.csv")
        df.rename(columns={'date': 'Date', 'cum_pl_price': 'Cum P/L Price', 'pl_price_ratio': 'P/L Price Ratio'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_pl():
    try:
        df = pd.read_csv("data_pl.csv")
        df.rename(columns={
            'date': 'Date', 'btc_price': 'BTC Price',
            'daily_realized_profit_btc': 'Daily Profit BTC',
            'daily_realized_loss_btc': 'Daily Loss BTC',
            'rpl_ratio': 'RPL Ratio',
            'sth_pl_ratio': 'STH P/L Ratio',
            'lth_pl_ratio': 'LTH P/L Ratio',
            'rrp': 'RRP', 'rrl': 'RRL',
            'relative_realized_pl': 'Relative Realized PL'
        }, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
        df['Daily Loss BTC'] = -df['Daily Loss BTC'].abs()
        return df
    except: return pd.DataFrame()

@st.cache_data(ttl=3600)
def load_data_aviv():
    try:
        df = pd.read_csv("data_aviv.csv")
        df.rename(columns={
            'date': 'Date',
            'price_at_aviv_mean': 'AVIV Mean Price',
            'price_at_aviv_upper_0.5sd': 'AVIV +0.5σ Price',
        }, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

# 🟢 METRIK BARU: LTH P/L Flow Loader
@st.cache_data(ttl=3600)
def load_data_lth_flow():
    try:
        df = pd.read_csv("data_lth_flow.csv")
        df.rename(columns={'date': 'Date', 'lth_pl_price': 'LTH Cum P/L Price', 'lth_pl_flow_btc': 'LTH P/L Flow'}, inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        return df.dropna(subset=['Date']).sort_values('Date').drop_duplicates(subset=['Date'], keep='last')
    except: return pd.DataFrame()

# ⚡ EKSEKUSI DEKLARASI VARIABEL (URUTAN WAJIB KONSISTEN)
df_price_raw = load_data_price()
df_mvrv_raw = load_data_mvrv()
df_mom_raw = load_data_momentum()
df_deriv_raw = load_data_derivatives()
df_ex_raw = load_data_exchange()
df_sentiment_raw = load_data_sentiment()
df_supply_raw = load_data_supply()
df_cum_raw = load_data_cum()
df_lth_flow_raw = load_data_lth_flow()
df_pl_raw = load_data_pl()
df_aviv_raw = load_data_aviv()

# ⚡ PROSES MERGE AMAN (Mengecek keberadaan variabel hulu terlebih dahulu)
if not df_cum_raw.empty:
    # HANYA merge ke df_mom_raw (Price_raw sudah punya datanya dari CSV)
    if df_mom_raw is not None and not df_mom_raw.empty:
        df_mom_raw = pd.merge(df_mom_raw, df_cum_raw[['Date', 'P/L Price Ratio']], on='Date', how='left')

if df_lth_flow_raw is not None and not df_lth_flow_raw.empty:
    if df_price_raw is not None and not df_price_raw.empty:
        df_price_raw = pd.merge(df_price_raw, df_lth_flow_raw[['Date', 'LTH Cum P/L Price']], on='Date', how='left')

if df_aviv_raw is not None and not df_aviv_raw.empty:
    if df_price_raw is not None and not df_price_raw.empty:
        df_price_raw = pd.merge(df_price_raw, df_aviv_raw[['Date', 'AVIV Mean Price', 'AVIV +0.5σ Price']], on='Date', how='left')
    if df_mom_raw is not None and not df_mom_raw.empty:
        df_mom_raw = pd.merge(df_mom_raw, df_lth_flow_raw[['Date', 'LTH P/L Flow']], on='Date', how='left')

df_fg_base = load_data_fg()
if not df_fg_base.empty and df_price_raw is not None and not df_price_raw.empty:
    df_fg_raw = pd.merge(df_price_raw[['Date', 'BTC Price']], df_fg_base, on='Date', how='inner')
else:
    df_fg_raw = pd.DataFrame()

# (duplicate merge block dihapus - merge sudah dilakukan di blok atas)

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
    
    # Menambahkan "Exchange Flow" ke dalam urutan menu
    selected_menu = st.radio(
        "Menu Navigasi",
        ["Price Levels", "Market Valuation", "Profit & Loss", "Realized P/L", "Supply Dynamics", "Exchange Flow", "Derivatives", "Social Sentiment", "Market Signals", "Backtesting", "MVRV Signal Lab"],
        label_visibility="collapsed"
    )
    st.markdown("---")

# ==============================================================================
# 4. MAIN DASHBOARD RENDER
# ==============================================================================

# ------------------------------------------------------------------------------
# TAB 1: PRICE LEVELS
# ------------------------------------------------------------------------------
# 1. Terapkan filter (HAPUS 'Cum P/L Price', TAMBAH 'Active Realized Price', 'MVRV 0σ', 'LTH P/L Price')
if selected_menu == "Price Levels":
    if not df_price_raw.empty:
        metrics_to_filter = ['STH Cost Basis', 'LTH Cost Basis', 'Realized Price', 'True Market Mean', 'CVDD', 'LTH Cum P/L Price', 'Active Realized Price', 'MVRV 0σ', 'AVIV Mean Price', 'AVIV +0.5σ Price']
        df_p, w_p = apply_filters(df_price_raw, st.session_state.tf_p, st.session_state.sma_p, st.session_state.cs_p, st.session_state.tr_p, st.session_state.cd_p, metrics_to_filter)
    

        last_p = df_p.iloc[-1]
        prev_p = df_p.iloc[-2] if len(df_p) > 1 else last_p
        
        btc_p = last_p.get('BTC Price', 0)
        btc_prev = prev_p.get('BTC Price', 0)
        
        def render_kpi_p(title, value, is_btc=False):
            if is_btc: 
                c, tc = "#f7931a", "#f7931a"
                dp = ((btc_p - btc_prev) / btc_prev * 100) if btc_prev else 0
                ip = dp >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {abs(dp):.2f}%</span></div>"
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
        with col_title: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>On-Chain Price Levels<br><span style='font-size: 1rem; color: transparent;'>.</span></h3></div>", unsafe_allow_html=True)
            
        with k1: render_kpi_p("Current BTC Price", btc_p, True)
        with k2: render_kpi_p("STH Cost Basis", last_p.get('STH Cost Basis', 0))
        with k3: render_kpi_p("LTH Cost Basis", last_p.get('LTH Cost Basis', 0))
        with k4: render_kpi_p("Realized Price", last_p.get('Realized Price', 0))
        with k5: render_kpi_p("True Market Mean", last_p.get('True Market Mean', 0))

        col_k2a, col_k2b, col_k2c = st.columns([1.5, 1, 1])
        with col_k2b: render_kpi_p("AVIV Mean Price", last_p.get('AVIV Mean Price', 0))
        with col_k2c: render_kpi_p("AVIV +0.5σ Price", last_p.get('AVIV +0.5σ Price', 0))
        
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
        
        # 2. Injeksi Opsi (Buang Cum P/L Price warna coklat, masukkan metrik baru)
        opts_p_base = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD', '🔵 LTH Cum P/L Price', '🔴 Active Realized Price', '🟢 MVRV 0σ', '🟨 200 DMA', '🟦 50 WMA', '🟪 200 WMA', '🟠 AVIV Mean Price', '🟡 AVIV +0.5σ Price']
        all_opts_p = opts_p_base.copy()
        if w_p > 1: all_opts_p.extend([f"{m} (SMA {w_p})" for m in opts_p_base])
            
        try: active_metrics_p = st.pills("Metrics", all_opts_p, default=['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price'], selection_mode="multi", label_visibility="collapsed")
        except: active_metrics_p = st.multiselect("Metrics", all_opts_p, default=['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price'], label_visibility="collapsed")

        # SKALA DISATUKAN (Semua di Kanan)
        chart_p_opts = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_p else 650, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": False}}
        series_p = [{"type": 'Line', "data": get_s(df_p, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        
        # 3. Mapping Warna
        colors_p = {
            '🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis', 0), 
            '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis', 0), 
            '⚪ Realized Price': ('#ffffff', 'Realized Price', 0), 
            '🟣 True Market Mean': ('#00ffff', 'True Market Mean', 0), 
            '🟢 CVDD': ('#00cc66', 'CVDD', 0),
            '🔵 LTH Cum P/L Price': ('#00ffff', 'LTH Cum P/L Price', 0),
            '🔴 Active Realized Price': ('#ff6666', 'Active Realized Price', 0),
            '🟢 MVRV 0σ': ('#059669', 'MVRV 0σ', 0),
            '🟨 200 DMA': ('#ffe119', '200 DMA', 2),
            '🟦 50 WMA': ('#4363d8', '50 WMA', 2),
            '🟪 200 WMA': ('#f032e6', '200 WMA', 2),
            '🟠 AVIV Mean Price': ('#ff9900', 'AVIV Mean Price', 0),
            '🟡 AVIV +0.5σ Price': ('#ffdd00', 'AVIV +0.5σ Price', 0)
        }
        
        for m in active_metrics_p:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            if base_m in colors_p:
                c_col, c_name, c_style = colors_p[base_m]
                actual_style = 2 if is_sma or c_style == 2 else 0
                if is_sma: series_p.append({"type": 'Line', "data": get_s(df_p, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": actual_style, "priceScaleId": 'right', "title": f"{c_name} SMA"}})
                else: series_p.append({"type": 'Line', "data": get_s(df_p, c_name), "options": {"color": c_col, "lineWidth": 1, "lineStyle": actual_style, "priceScaleId": 'right', "title": c_name}})
                    
        renderLightweightCharts([{"chart": chart_p_opts, "series": series_p}], 'chart_price')

# ------------------------------------------------------------------------------
# TAB 2: MARKET VALUATION
# ------------------------------------------------------------------------------
elif selected_menu == "Market Valuation":
    if not df_mvrv_raw.empty:
        last_mv = df_mvrv_raw.iloc[-1]
        prev_mv = df_mvrv_raw.iloc[-2] if len(df_mvrv_raw) > 1 else last_mv
        
        btc_mv = last_mv.get('BTC Price', 0)
        btc_prev_mv = prev_mv.get('BTC Price', 0)
        
        def render_kpi_mv(title, value, prev_val, threshold=1.0):
            if pd.isna(value) or value == 0: 
                color = "#a3a8b8"
                d = ""
            else: 
                color = "#00cc66" if value >= threshold else "#ff4d4d"
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                diff_str = f"{abs(diff):.4f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"
                
            val_str = f"{value:.4f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_mv = ((btc_mv - btc_prev_mv) / btc_prev_mv * 100) if btc_prev_mv else 0
        ip_btc_mv = dp_btc_mv >= 0
        dc_btc_mv = "#00cc66" if ip_btc_mv else "#ff4d4d"
        ar_btc_mv = "↑" if ip_btc_mv else "↓"
        d_btc_mv = f"<div style='margin-top:4px;'><span style='color:{dc_btc_mv}; font-size:0.85rem; background-color:{dc_btc_mv}20; padding:2px 6px; border-radius:4px;'>{ar_btc_mv} {abs(dp_btc_mv):.2f}%</span></div>"
        btc_html_mv = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_mv:,.2f}</span>{d_btc_mv}</div>"

        col_title_mv, k1_mv, k2_mv, k3_mv, k4_mv, k5_mv = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_mv: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Market Valuation<br><span style='font-size: 1rem; color: #d1d4dc;'>MVRV Oscillators</span></h3></div>", unsafe_allow_html=True)
        with k1_mv: st.markdown(btc_html_mv, unsafe_allow_html=True)
        with k2_mv: render_kpi_mv("MVRV", last_mv.get('MVRV', 0), prev_mv.get('MVRV', 0), 1.0)
        with k3_mv: render_kpi_mv("LTH MVRV", last_mv.get('LTH MVRV', 0), prev_mv.get('LTH MVRV', 0), 1.0)
        with k4_mv: render_kpi_mv("STH MVRV", last_mv.get('STH MVRV', 0), prev_mv.get('STH MVRV', 0), 1.0)
        
        st.markdown("---")
        df_mv, w_mv = apply_filters(df_mvrv_raw, st.session_state.tf_mv, st.session_state.sma_mv, st.session_state.cs_mv, st.session_state.tr_mv, st.session_state.cd_mv, ['MVRV', 'LTH MVRV', 'STH MVRV'])

        col_fs_mv, col_tf_mv, col_sma_mv, col_sma_cst_mv, col_radio_mv, col_custom_mv = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_mv: focus_mv = st.toggle("Full Screen", key="tg_mv")
        with col_tf_mv: st.session_state.tf_mv = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_mv), key="tfs_mv")
        with col_sma_mv: st.session_state.sma_mv = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_mv), key="smas_mv")
        with col_sma_cst_mv:
            if st.session_state.sma_mv == "Custom": st.session_state.cs_mv = st.number_input("Days", min_value=1, value=st.session_state.cs_mv, label_visibility="collapsed", key="cst_mv")
        with col_radio_mv:
            c_idx_mv = t_opts.index(st.session_state.tr_mv) if st.session_state.tr_mv in t_opts else 5
            st.session_state.tr_mv = st.radio("Range:", t_opts, index=c_idx_mv, horizontal=True, label_visibility="collapsed", key="rg_mv")
        with col_custom_mv:
            if st.session_state.tr_mv == "Custom": st.session_state.cd_mv = st.number_input("Days back", min_value=7, value=st.session_state.cd_mv, label_visibility="collapsed", key="cdin_mv")
        
        opts_mv_base = ['🔵 MVRV', '🔴 STH MVRV', '🟢 LTH MVRV']
        all_opts_mv = opts_mv_base.copy()
        if w_mv > 1: all_opts_mv.extend([f"{m} (SMA {w_mv})" for m in opts_mv_base])
            
        try: sel_mv = st.pills("MVRV Metrics", all_opts_mv, default=['🔵 MVRV', '🔴 STH MVRV', '🟢 LTH MVRV'], selection_mode="multi", label_visibility="collapsed", key="pills_mv")
        except: sel_mv = st.multiselect("MVRV Metrics", all_opts_mv, default=['🔵 MVRV', '🔴 STH MVRV', '🟢 LTH MVRV'], label_visibility="collapsed", key="ms_mv")

        # ── Dual pane: MVRV / STH → right scale, LTH → left scale (keduanya draggable) ──
        h_total_mv = 850 if focus_mv else 650
        h_top_mv   = int(h_total_mv * 0.45)
        h_bot_mv   = h_total_mv - h_top_mv

        # Chart atas — BTC Price saja, timeScale disembunyikan agar menyatu
        chart_top_mv = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}},
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}},
            "crosshair": {"mode": 0},
            "height": h_top_mv,
            "rightPriceScale": {"visible": True},
            "leftPriceScale": {"visible": False},
            "timeScale": {"borderVisible": False, "ticksVisible": False, "visible": True},
        }
        series_top_mv = [{"type": 'Line', "data": get_s(df_mv, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        # Chart bawah — LTH MVRV → left (draggable), MVRV + STH MVRV → right (draggable)
        chart_bot_mv = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}},
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}},
            "crosshair": {"mode": 0},
            "height": h_bot_mv,
            "rightPriceScale": {"visible": True},
            "leftPriceScale": {"visible": False},
        }
        # Garis netral 1.0 di right scale sebagai referensi
        df_mv['Neutral_Line'] = 1.0
        series_bot_mv = [{"type": 'Line', "data": get_s(df_mv, 'Neutral_Line'), "options": {"color": 'rgba(255,255,255,0.3)', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'right', "title": 'Neutral (1.0)'}}]

        for m in sel_mv:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            # 🟢 FIX: Semua metrik MVRV sekarang diarahkan ke 'right' tscale
            if base_m == '🔵 MVRV':     c_col, c_col_raw, c_name, tscale = '#4da6ff', 'rgba(77,166,255,0.85)',   'MVRV',     'right'
            elif base_m == '🔴 STH MVRV': c_col, c_col_raw, c_name, tscale = '#ff4d4d', 'rgba(255,77,77,0.85)',    'STH MVRV', 'right'
            elif base_m == '🟢 LTH MVRV': c_col, c_col_raw, c_name, tscale = '#00cc66', 'rgba(0,204,102,0.85)',    'LTH MVRV', 'right'
            else: continue
            
            if is_sma: series_bot_mv.append({"type": 'Line', "data": get_s(df_mv, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": tscale, "title": f"{c_name} SMA"}})
            else:      series_bot_mv.append({"type": 'Line', "data": get_s(df_mv, c_name),            "options": {"color": c_col_raw, "lineWidth": 1.5, "priceScaleId": tscale, "title": c_name}})
        renderLightweightCharts([
            {"chart": chart_top_mv, "series": series_top_mv},
            {"chart": chart_bot_mv, "series": series_bot_mv},
        ], 'chart_mvrv_dual')

# ------------------------------------------------------------------------------
# TAB 3: PROFIT & LOSS 
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
                diff_str = f"${abs(diff):,.2f}" if is_money else f"{abs(diff):.4f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"
                
            val_str = f"${value:,.2f}" if is_money else f"{value:.4f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_m = ((btc_m - btc_prev_m) / btc_prev_m * 100) if btc_prev_m else 0
        ip_btc_m = dp_btc_m >= 0
        dc_btc_m = "#00cc66" if ip_btc_m else "#ff4d4d"
        ar_btc_m = "↑" if ip_btc_m else "↓"
        d_btc_m = f"<div style='margin-top:4px;'><span style='color:{dc_btc_m}; font-size:0.85rem; background-color:{dc_btc_m}20; padding:2px 6px; border-radius:4px;'>{ar_btc_m} {abs(dp_btc_m):.2f}%</span></div>"
        btc_html_m = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_m:,.2f}</span>{d_btc_m}</div>"

        # CHART 1: SOPR
        col_title_1, k1_1, k2_1, k3_1, k4_1, k5_1 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_1: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Profit & Loss<br><span style='font-size: 1rem; color: #d1d4dc;'>SOPR Metric</span></h3></div>", unsafe_allow_html=True)
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

       # ==========================================
        # SETUP DUAL-PANE CHART (SYNCED)
        # ==========================================
        
        tinggi_total = 850 if focus_ms else 650
        tinggi_atas = int(tinggi_total * 0.6) # 60% porsi untuk Harga BTC
        tinggi_bawah = int(tinggi_total * 0.4) # 40% porsi untuk Metrik (SOPR)

        # 1. CHART ATAS: BTC PRICE
        chart_opts_top = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": tinggi_atas, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": False},
            "timeScale": {"borderVisible": False, "ticksVisible": False, "visible": True}
        }
        series_top = [{"type": 'Line', "data": get_s(df_ms, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        # 2. CHART BAWAH: SOPR METRICS
        chart_opts_bottom = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": tinggi_bawah, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": False} 
        }
        
        # Garis Netral dimasukkan ke Chart Bawah
        df_ms['Neutral_Line'] = 1.0
        series_bottom = [{"type": 'Line', "data": get_s(df_ms, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'right', "title": 'Neutral (1.0)'}}]

        # Looping Metrik Pilihan User (Masuk ke Chart Bawah)
        for m in sel_sopr:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🔵 aSOPR': c_col, c_col_raw, c_name = '#00e6e6', 'rgba(0, 230, 230, 0.7)', 'aSOPR'
            elif base_m == '🔴 STH SOPR': c_col, c_col_raw, c_name = '#ff4d4d', 'rgba(255, 77, 77, 0.7)', 'STH SOPR'
            elif base_m == '🟢 LTH SOPR': c_col, c_col_raw, c_name = '#00cc66', 'rgba(0, 204, 102, 0.7)', 'LTH SOPR'
            else: continue
            
            if is_sma: 
                series_bottom.append({"type": 'Line', "data": get_s(df_ms, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'right', "title": f"{c_name} SMA"}})
            else: 
                series_bottom.append({"type": 'Line', "data": get_s(df_ms, c_name), "options": {"color": c_col_raw, "lineWidth": 1, "priceScaleId": 'right', "title": c_name}})

        # 3. RENDER BERSAMAAN DALAM SATU ARRAY (AUTO-SYNC ZOMM/PAN)
        renderLightweightCharts([
            {"chart": chart_opts_top, "series": series_top},
            {"chart": chart_opts_bottom, "series": series_bottom}
        ], 'chart_sopr_dual')
        
        #chart_opts_sopr = {
         #   "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
          #  "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
           # "crosshair": {"mode": 0}, "height": 850 if focus_ms else 650, 
            #"rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}, "scale3": {"visible": False} 
        #}
        #series_sopr = [{"type": 'Line', "data": get_s(df_ms, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        #df_ms['Neutral_Line'] = 1.0
        #series_sopr.append({"type": 'Line', "data": get_s(df_ms, 'Neutral_Line'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}})

        #for m in sel_sopr:
          #  is_sma = "(SMA" in m
           # base_m = m.split(" (SMA")[0]
            #target_scale = "scale3" if base_m == '🟢 LTH SOPR' else "left"
            #if base_m == '🔵 aSOPR': c_col, c_col_raw, c_name = '#00e6e6', 'rgba(0, 230, 230, 0.7)', 'aSOPR'
            #elif base_m == '🔴 STH SOPR': c_col, c_col_raw, c_name = '#ff4d4d', 'rgba(255, 77, 77, 0.7)', 'STH SOPR'
            #elif base_m == '🟢 LTH SOPR': c_col, c_col_raw, c_name = '#00cc66', 'rgba(0, 204, 102, 0.7)', 'LTH SOPR'
            #else: continue
            
            #if is_sma: series_sopr.append({"type": 'Line', "data": get_s(df_ms, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": target_scale, "title": f"{c_name} SMA"}})
            #else: series_sopr.append({"type": 'Line', "data": get_s(df_ms, c_name), "options": {"color": c_col_raw, "lineWidth": 1, "priceScaleId": target_scale, "title": c_name}})
        #renderLightweightCharts([{"chart": chart_opts_sopr, "series": series_sopr}], 'chart_sopr')
        #st.markdown("<br><br>", unsafe_allow_html=True)

        # CHART 2: REALIZED P/L
        col_title_2, k1_2, k2_2, k3_2, k4_2, k5_2 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_2: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Profit & Loss<br><span style='font-size: 1rem; color: #d1d4dc;'>Realized P&L Metric</span></h3></div>", unsafe_allow_html=True)
        with k1_2: st.markdown(btc_html_m, unsafe_allow_html=True)
        with k2_2: render_kpi_m("Net Realized PL", last_m.get('Net Realized PL', 0), prev_m.get('Net Realized PL', 0), 0.0, True)
        with k3_2: render_kpi_m("STH P/L Ratio", last_m.get('STH P/L Ratio', 0), prev_m.get('STH P/L Ratio', 0), 1.0)
        with k4_2: render_kpi_m("LTH P/L Ratio", last_m.get('LTH P/L Ratio', 0), prev_m.get('LTH P/L Ratio', 0), 1.0)
        with k5_2: render_kpi_m("P/L Price Ratio", last_m.get('P/L Price Ratio', 0), prev_m.get('P/L Price Ratio', 0), 1.0)
        st.markdown("---")
        
        df_mpl, w_mpl = apply_filters(df_mom_raw, st.session_state.tf_mpl, st.session_state.sma_mpl, st.session_state.cs_mpl, st.session_state.tr_mpl, st.session_state.cd_mpl, ['STH P/L Ratio', 'LTH P/L Ratio', 'Net Realized PL', 'P/L Price Ratio'])
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
            
        opts_pl_base = ['⚪ Net Realized PL', '🟣 STH P/L Ratio', '🟤 LTH P/L Ratio', '🟠 P/L Price Ratio']
        all_opts_pl = opts_pl_base.copy()
        if w_mpl > 1: all_opts_pl.extend([f"{m} (SMA {w_mpl})" for m in opts_pl_base])

        try: sel_pl = st.pills("P/L Metrics", all_opts_pl, default=['⚪ Net Realized PL'], selection_mode="multi", label_visibility="collapsed")
        except: sel_pl = st.multiselect("P/L Metrics", all_opts_pl, default=['⚪ Net Realized PL'], label_visibility="collapsed")

       # Konfigurasi Chart dengan Skala Logaritma untuk Rasio Ekstrem
        chart_opts_pl = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, 
            "height": 850 if focus_mpl else 650, 
            "rightPriceScale": {"visible": True}, 
            "leftPriceScale": {"visible": True}, 
            "ratio_scale": {
                "visible": True, 
                "mode": 1,  # 🟢 INDIKATOR KUNCI: 1 mengubah skala Y-axis menjadi Logarithmic
                "autoScale": True
            }  
        }
        series_pl = [{"type": 'Line', "data": get_s(df_mpl, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        for m in sel_pl:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🟣 STH P/L Ratio':
                c_col_rgba = 'rgba(204, 51, 255, 0.7)'
                c_name = 'STH P/L Ratio'
                series_pl.append({"type": 'Line', "data": get_s(df_mpl, f"{c_name}_SMA" if is_sma else c_name), "options": {"color": c_col_rgba, "lineWidth": 1, "lineStyle": 2 if is_sma else 0, "priceScaleId": 'ratio_scale', "title": f"{c_name} SMA" if is_sma else c_name}})
            elif base_m == '🟤 LTH P/L Ratio':
                c_col_rgba = 'rgba(204, 153, 102, 0.7)'
                c_name = 'LTH P/L Ratio'
                series_pl.append({"type": 'Line', "data": get_s(df_mpl, f"{c_name}_SMA" if is_sma else c_name), "options": {"color": c_col_rgba, "lineWidth": 1, "lineStyle": 2 if is_sma else 0, "priceScaleId": 'ratio_scale', "title": f"{c_name} SMA" if is_sma else c_name}})
            elif base_m == '🟠 P/L Price Ratio':
                c_col_rgba = 'rgba(255, 153, 51, 0.9)'
                c_name = 'P/L Price Ratio'
                series_pl.append({"type": 'Line', "data": get_s(df_mpl, f"{c_name}_SMA" if is_sma else c_name), "options": {"color": c_col_rgba, "lineWidth": 1.5, "lineStyle": 2 if is_sma else 0, "priceScaleId": 'ratio_scale', "title": f"{c_name} SMA" if is_sma else c_name}})
            elif base_m == '⚪ Net Realized PL':
                if is_sma:
                    series_pl.append({"type": 'Histogram', "data": get_s(df_mpl, 'Net Realized PL_SMA'), "options": {"color": 'rgba(255, 255, 255, 0.4)', "priceScaleId": 'left', "title": "Net PL SMA"}})
                else:
                    net_pl_raw = get_s(df_mpl, 'Net Realized PL')
                    for d in net_pl_raw: d['color'] = 'rgba(0, 204, 102, 0.7)' if d['value'] >= 0 else 'rgba(255, 77, 77, 0.7)'
                    series_pl.append({"type": 'Histogram', "data": net_pl_raw, "options": {"priceScaleId": 'left', "title": 'Net PL Raw'}})

        renderLightweightCharts([{"chart": chart_opts_pl, "series": series_pl}], 'chart_netpl')
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # CHART 3: NUPL 
        col_title_3, k1_3, k2_3, k3_3, k4_3, k5_3 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_3: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Profit & Loss<br><span style='font-size: 1rem; color: #d1d4dc;'>NUPL Metric</span></h3></div>", unsafe_allow_html=True)
        with k1_3: st.markdown(btc_html_m, unsafe_allow_html=True)
        with k2_3: render_kpi_m("NUPL", last_m.get('NUPL', 0), prev_m.get('NUPL', 0), 0.0)
        with k3_3: render_kpi_m("STH NUPL", last_m.get('STH NUPL', 0), prev_m.get('STH NUPL', 0), 0.0)
        with k4_3: render_kpi_m("LTH NUPL", last_m.get('LTH NUPL', 0), prev_m.get('LTH NUPL', 0), 0.0)
        st.markdown("---")
        
        df_nupl, w_nupl = apply_filters(df_mom_raw, st.session_state.tf_nupl, st.session_state.sma_nupl, st.session_state.cs_nupl, st.session_state.tr_nupl, st.session_state.cd_nupl, ['NUPL', 'STH NUPL', 'LTH NUPL'])
        col_fs_nupl, col_tf_nupl, col_sma_nupl, col_sma_cst_nupl, col_radio_nupl, col_custom_nupl = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_nupl: focus_nupl = st.toggle("Full Screen", key="tg_nupl")
        with col_tf_nupl: st.session_state.tf_nupl = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_nupl), key="tfs_nupl")
        with col_sma_nupl: st.session_state.sma_nupl = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_nupl), key="smas_nupl")
        with col_sma_cst_nupl:
            if st.session_state.sma_nupl == "Custom": st.session_state.cs_nupl = st.number_input("Days", min_value=1, value=st.session_state.cs_nupl, label_visibility="collapsed", key="cst_nupl")
        with col_radio_nupl:
            c_idx_nupl = t_opts.index(st.session_state.tr_nupl) if st.session_state.tr_nupl in t_opts else 5
            st.session_state.tr_nupl = st.radio("Range:", t_opts, index=c_idx_nupl, horizontal=True, label_visibility="collapsed", key="rg_nupl")
        with col_custom_nupl:
            if st.session_state.tr_nupl == "Custom": st.session_state.cd_nupl = st.number_input("Days back", min_value=7, value=st.session_state.cd_nupl, label_visibility="collapsed", key="cdin_nupl")
            
        opts_nupl_base = ['🔵 NUPL', '🔴 STH NUPL', '🟢 LTH NUPL']
        all_opts_nupl = opts_nupl_base.copy()
        if w_nupl > 1: all_opts_nupl.extend([f"{m} (SMA {w_nupl})" for m in opts_nupl_base])

        try: sel_nupl = st.pills("NUPL Metrics", all_opts_nupl, default=['🔵 NUPL', '🟢 LTH NUPL'], selection_mode="multi", label_visibility="collapsed")
        except: sel_nupl = st.multiselect("NUPL Metrics", all_opts_nupl, default=['🔵 NUPL', '🟢 LTH NUPL'], label_visibility="collapsed")

        chart_opts_nupl = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, "height": 850 if focus_nupl else 650, 
            "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True} 
        }
        series_nupl = [{"type": 'Line', "data": get_s(df_nupl, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        df_nupl['NUPL_Zero'] = 0.0
        series_nupl.append({"type": 'Line', "data": get_s(df_nupl, 'NUPL_Zero'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (0.0)'}})

        for m in sel_nupl:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🔵 NUPL': c_col, c_name = '#4da6ff', 'NUPL'
            elif base_m == '🔴 STH NUPL': c_col, c_name = '#ff4d4d', 'STH NUPL'
            elif base_m == '🟢 LTH NUPL': c_col, c_name = '#00cc66', 'LTH NUPL'
            else: continue
            
            if is_sma: series_nupl.append({"type": 'Line', "data": get_s(df_nupl, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{c_name} SMA"}})
            else: series_nupl.append({"type": 'Line', "data": get_s(df_nupl, c_name), "options": {"color": c_col, "lineWidth": 1, "priceScaleId": 'left', "title": c_name}})

        renderLightweightCharts([{"chart": chart_opts_nupl, "series": series_nupl}], 'chart_nupl')

# ------------------------------------------------------------------------------
# TAB: REALIZED P/L
# ------------------------------------------------------------------------------
elif selected_menu == "Realized P/L":
    if not df_pl_raw.empty:
        last_pl = df_pl_raw.iloc[-1]
        prev_pl = df_pl_raw.iloc[-2] if len(df_pl_raw) > 1 else last_pl
        btc_pl = last_pl.get('BTC Price', 0)
        btc_prev_pl = prev_pl.get('BTC Price', 1)

        def render_kpi_pl(title, value, prev_val, threshold=1.0, is_btc=False):
            if pd.isna(value) or value == 0:
                color = "#a3a8b8"; d = ""
            else:
                color = "#00cc66" if value >= threshold else "#ff4d4d"
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                diff_str = f"₿{abs(diff):,.2f}" if is_btc else f"{abs(diff):.4f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"
            val_str = f"₿{value:,.2f}" if is_btc else f"{value:.4f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_pl = ((btc_pl - btc_prev_pl) / btc_prev_pl * 100) if btc_prev_pl else 0
        dc_btc_pl = "#00cc66" if dp_btc_pl >= 0 else "#ff4d4d"
        ar_btc_pl = "↑" if dp_btc_pl >= 0 else "↓"
        d_btc_pl = f"<div style='margin-top:4px;'><span style='color:{dc_btc_pl}; font-size:0.85rem; background-color:{dc_btc_pl}20; padding:2px 6px; border-radius:4px;'>{ar_btc_pl} {abs(dp_btc_pl):.2f}%</span></div>"
        btc_html_pl = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_pl:,.2f}</span>{d_btc_pl}</div>"

        # ── FULL SCREEN toggle (shared, affects chart heights) ──
        focus_pl = st.toggle("Full Screen", key="tg_pl")

        def apply_smooth_pl(df, cols, period, stype):
            df = df.copy()
            if period > 1:
                for col in cols:
                    if col in df.columns:
                        if stype == "EMA":
                            df[f"{col}_smooth"] = df[col].ewm(span=period, adjust=False).mean()
                        else:
                            df[f"{col}_smooth"] = df[col].rolling(period, min_periods=1).mean()
            return df

        def chart_ctrl_pl(n):
            k_tf = f"tf_pl{n}"; k_tr = f"tr_pl{n}"; k_cd = f"cd_pl{n}"
            k_cs = f"cs_pl{n}"; k_st = f"smooth_type_pl{n}"
            tf_list = ["Daily", "3 Days", "Weekly", "Monthly"]
            col_tf, col_smooth, col_stype, col_radio, col_custom = st.columns([1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
            with col_tf: st.session_state[k_tf] = st.selectbox("Timeframe", tf_list, index=tf_list.index(st.session_state[k_tf]), key=f"tfs_pl{n}")
            with col_smooth: st.session_state[k_cs] = st.number_input("Period (0=off)", min_value=0, value=st.session_state[k_cs], step=1, key=f"inp_cs_pl{n}")
            with col_stype: st.session_state[k_st] = st.selectbox("", ["SMA", "EMA"], index=["SMA","EMA"].index(st.session_state[k_st]), key=f"sel_st_pl{n}", label_visibility="collapsed")
            with col_radio:
                c_idx = t_opts.index(st.session_state[k_tr]) if st.session_state[k_tr] in t_opts else 5
                st.session_state[k_tr] = st.radio("Range:", t_opts, index=c_idx, horizontal=True, label_visibility="collapsed", key=f"rg_pl{n}")
            with col_custom:
                if st.session_state[k_tr] == "Custom": st.session_state[k_cd] = st.number_input("Days back", min_value=7, value=st.session_state[k_cd], label_visibility="collapsed", key=f"cdin_pl{n}")

        # ── CHART 1: RPL Ratio + STH/LTH P/L Ratio ──
        col_t1, k1, k2, k3, k4, k5 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_t1: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Realized P/L<br><span style='font-size: 1rem; color: #d1d4dc;'>Market P/L Ratios</span></h3></div>", unsafe_allow_html=True)
        with k1: st.markdown(btc_html_pl, unsafe_allow_html=True)
        with k2: render_kpi_pl("RPL Ratio", last_pl.get('RPL Ratio', 0), prev_pl.get('RPL Ratio', 0), 1.0)
        with k3: render_kpi_pl("STH P/L Ratio", last_pl.get('STH P/L Ratio', 0), prev_pl.get('STH P/L Ratio', 0), 1.0)
        with k4: render_kpi_pl("LTH P/L Ratio", last_pl.get('LTH P/L Ratio', 0), prev_pl.get('LTH P/L Ratio', 0), 1.0)
        with k5: render_kpi_pl("Daily Profit BTC", last_pl.get('Daily Profit BTC', 0), prev_pl.get('Daily Profit BTC', 0), 0.0, True)
        st.markdown("---")
        chart_ctrl_pl(1)

        p1, t1 = st.session_state.cs_pl1, st.session_state.smooth_type_pl1
        df_c1_raw, _ = apply_filters(df_pl_raw, st.session_state.tf_pl1, "0d", 0, st.session_state.tr_pl1, st.session_state.cd_pl1, [])
        df_c1 = apply_smooth_pl(df_c1_raw, ['RPL Ratio', 'STH P/L Ratio', 'LTH P/L Ratio'], p1, t1)
        sl1 = f"{t1} {p1}" if p1 > 1 else ""
        opts_ratio_base = ['🟡 RPL Ratio', '🟣 STH P/L Ratio', '🟤 LTH P/L Ratio']
        all_opts_ratio = opts_ratio_base + ([f"{m} ({sl1})" for m in opts_ratio_base] if p1 > 1 else [])
        try: sel_ratio = st.pills("Ratio Metrics", all_opts_ratio, default=opts_ratio_base, selection_mode="multi", label_visibility="collapsed", key="pills_ratio")
        except: sel_ratio = st.multiselect("Ratio Metrics", all_opts_ratio, default=opts_ratio_base, label_visibility="collapsed", key="ms_ratio")

        chart_top_pl = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 250, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": False}}
        chart_bot_ratio = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 550 if focus_pl else 400, "rightPriceScale": {"visible": False}, "leftPriceScale": {"visible": True, "mode": 1}}

        series_price_pl = [{"type": 'Line', "data": get_s(df_c1, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        df_c1['Neutral'] = 1.0
        series_ratio = [{"type": 'Line', "data": get_s(df_c1, 'Neutral'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Neutral (1.0)'}}]
        color_map_ratio = {'🟡 RPL Ratio': ('#f5c518', 'rgba(245,197,24,0.8)', 'RPL Ratio'), '🟣 STH P/L Ratio': ('#cc33ff', 'rgba(204,51,255,0.7)', 'STH P/L Ratio'), '🟤 LTH P/L Ratio': ('#cc9966', 'rgba(204,153,102,0.7)', 'LTH P/L Ratio')}
        for m in sel_ratio:
            is_smooth = f"({sl1})" in m and p1 > 1
            base_m = m.split(" (")[0]
            if base_m not in color_map_ratio: continue
            c_col, c_col_raw, c_name = color_map_ratio[base_m]
            col_key = f"{c_name}_smooth" if is_smooth else c_name
            series_ratio.append({"type": 'Line', "data": get_s(df_c1, col_key), "options": {"color": c_col if is_smooth else c_col_raw, "lineWidth": 1, "lineStyle": 2 if is_smooth else 0, "priceScaleId": 'left', "title": f"{c_name} {sl1}" if is_smooth else c_name}})
        renderLightweightCharts([{"chart": chart_top_pl, "series": series_price_pl}, {"chart": chart_bot_ratio, "series": series_ratio}], 'chart_pl_ratio')

        st.markdown("<br>", unsafe_allow_html=True)

        # ── CHART 2: Daily Realized Profit vs Loss (BTC) ──
        col_t2, k2_1, k2_2, _ = st.columns([1.5, 1, 1, 3], vertical_alignment="center")
        with col_t2: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Realized P/L<br><span style='font-size: 1rem; color: #d1d4dc;'>Daily Profit & Loss (BTC)</span></h3></div>", unsafe_allow_html=True)
        with k2_1: render_kpi_pl("Daily Profit BTC", last_pl.get('Daily Profit BTC', 0), prev_pl.get('Daily Profit BTC', 0), 0.0, True)
        with k2_2:
            loss_val = abs(last_pl.get('Daily Loss BTC', 0))
            loss_prev = abs(prev_pl.get('Daily Loss BTC', 0))
            diff_loss = loss_val - loss_prev
            dc_l = "#00cc66" if diff_loss <= 0 else "#ff4d4d"
            ar_l = "↓" if diff_loss <= 0 else "↑"
            d_l = f"<div style='margin-top:4px;'><span style='color:{dc_l}; font-size:0.85rem; background-color:{dc_l}20; padding:2px 6px; border-radius:4px;'>{ar_l} ₿{abs(diff_loss):,.2f}</span></div>"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#ff4d4d; font-size:0.95rem; font-weight:600;'>Daily Loss BTC</span><br><span style='color:#ff4d4d; font-size:1.4rem; font-weight:700;'>₿{loss_val:,.2f}</span>{d_l}</div>", unsafe_allow_html=True)
        st.markdown("---")
        chart_ctrl_pl(2)

        p2, t2 = st.session_state.cs_pl2, st.session_state.smooth_type_pl2
        df_c2_raw, _ = apply_filters(df_pl_raw, st.session_state.tf_pl2, "0d", 0, st.session_state.tr_pl2, st.session_state.cd_pl2, [])
        df_c2 = apply_smooth_pl(df_c2_raw, ['Daily Profit BTC', 'Daily Loss BTC'], p2, t2)
        chart_top_pl2 = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 250, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": False}}
        chart_bot_flow = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 550 if focus_pl else 400, "rightPriceScale": {"visible": False}, "leftPriceScale": {"visible": True}}
        series_price_pl2 = [{"type": 'Line', "data": get_s(df_c2, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        profit_key2 = 'Daily Profit BTC_smooth' if p2 > 1 else 'Daily Profit BTC'
        loss_key2   = 'Daily Loss BTC_smooth'   if p2 > 1 else 'Daily Loss BTC'
        chart_type2 = 'Line' if p2 > 1 else 'Histogram'
        series_flow = [
            {"type": chart_type2, "data": get_s(df_c2, profit_key2), "options": {"color": 'rgba(0, 204, 102, 0.7)', "priceScaleId": 'left', "title": f'Daily Profit BTC ({t2} {p2})' if p2 > 1 else 'Daily Profit BTC'}},
            {"type": chart_type2, "data": get_s(df_c2, loss_key2),   "options": {"color": 'rgba(255, 77, 77, 0.7)', "priceScaleId": 'left', "title": f'Daily Loss BTC ({t2} {p2})' if p2 > 1 else 'Daily Loss BTC'}},
        ]
        renderLightweightCharts([{"chart": chart_top_pl2, "series": series_price_pl2}, {"chart": chart_bot_flow, "series": series_flow}], 'chart_pl_flow')

        # ── CHART 3: Relative Realized P/L (rrp, rrl, net) ──
        if 'RRP' in df_pl_raw.columns:
            st.markdown("<br>", unsafe_allow_html=True)
            col_t3, k3_1, k3_2, k3_3, k3_4 = st.columns([1.5, 1, 1, 1, 2], vertical_alignment="center")
            with col_t3: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Realized P/L<br><span style='font-size: 1rem; color: #d1d4dc;'>Relative Realized P/L</span></h3></div>", unsafe_allow_html=True)
            with k3_1: st.markdown(btc_html_pl, unsafe_allow_html=True)
            with k3_2: render_kpi_pl("RRP", last_pl.get('RRP', 0), prev_pl.get('RRP', 0), 0.0)
            with k3_3: render_kpi_pl("RRL", last_pl.get('RRL', 0), prev_pl.get('RRL', 0), 0.0)
            with k3_4: render_kpi_pl("Relative PL", last_pl.get('Relative Realized PL', 0), prev_pl.get('Relative Realized PL', 0), 0.0)
            st.markdown("---")
            chart_ctrl_pl(3)

            p3, t3 = st.session_state.cs_pl3, st.session_state.smooth_type_pl3
            df_c3_raw, _ = apply_filters(df_pl_raw, st.session_state.tf_pl3, "0d", 0, st.session_state.tr_pl3, st.session_state.cd_pl3, [])
            df_c3 = apply_smooth_pl(df_c3_raw, ['RRP', 'RRL', 'Relative Realized PL'], p3, t3)
            sl3 = f"{t3} {p3}" if p3 > 1 else ""
            opts_rrl_base = ['🟢 RRP', '🔴 RRL', '⚪ Relative PL']
            all_opts_rrl = opts_rrl_base + ([f"{m} ({sl3})" for m in opts_rrl_base] if p3 > 1 else [])
            try: sel_rrl = st.pills("Relative Metrics", all_opts_rrl, default=opts_rrl_base, selection_mode="multi", label_visibility="collapsed", key="pills_rrl")
            except: sel_rrl = st.multiselect("Relative Metrics", all_opts_rrl, default=opts_rrl_base, label_visibility="collapsed", key="ms_rrl")

            chart_top_pl3 = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 250, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": False}}
            chart_bot_rrl = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 550 if focus_pl else 400, "rightPriceScale": {"visible": False}, "leftPriceScale": {"visible": True}}
            series_price_pl3 = [{"type": 'Line', "data": get_s(df_c3, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
            df_c3['Zero'] = 0.0
            series_rrl = [{"type": 'Line', "data": get_s(df_c3, 'Zero'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Zero'}}]
            color_map_rrl = {'🟢 RRP': ('#00cc66', 'rgba(0,204,102,0.7)', 'RRP'), '🔴 RRL': ('#ff4d4d', 'rgba(255,77,77,0.7)', 'RRL'), '⚪ Relative PL': ('#d1d4dc', 'rgba(209,212,220,0.9)', 'Relative Realized PL')}
            for m in sel_rrl:
                is_smooth = f"({sl3})" in m and p3 > 1
                base_m = m.split(" (")[0]
                if base_m not in color_map_rrl: continue
                c_col, c_col_raw, c_name = color_map_rrl[base_m]
                col_key = f"{c_name}_smooth" if is_smooth else c_name
                is_hist = base_m in ('🟢 RRP', '🔴 RRL') and not is_smooth
                series_rrl.append({"type": 'Histogram' if is_hist else 'Line', "data": get_s(df_c3, col_key), "options": {"color": c_col if is_smooth else c_col_raw, "lineWidth": 1, "lineStyle": 2 if is_smooth else 0, "priceScaleId": 'left', "title": f"{c_name} {sl3}" if is_smooth else c_name}})
            renderLightweightCharts([{"chart": chart_top_pl3, "series": series_price_pl3}, {"chart": chart_bot_rrl, "series": series_rrl}], 'chart_pl_rrl')

    else:
        st.warning("Data Realized P/L belum tersedia. Jalankan auto_update.py terlebih dahulu.")

# ------------------------------------------------------------------------------
# TAB 4: SUPPLY DYNAMICS
# ------------------------------------------------------------------------------
elif selected_menu == "Supply Dynamics":
    if not df_supply_raw.empty:
        last_sd = df_supply_raw.iloc[-1]
        prev_sd = df_supply_raw.iloc[-2] if len(df_supply_raw) > 1 else last_sd
        
        btc_sd = last_sd.get('BTC Price', 0)
        btc_prev_sd = prev_sd.get('BTC Price', 0)
        
        def render_kpi_sd(title, value, prev_val, is_percent=False):
            if pd.isna(value) or value == 0: 
                color = "#a3a8b8"
                d = ""
            else: 
                if "Total % Profit" in title: color = "#ffffff"
                elif "Total % Loss" in title: color = "#a3a8b8"
                elif "LTH" in title: color = "#4da6ff"
                else: color = "#ff4d4d"
                
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                diff_str = f"{abs(diff):.2f}%" if is_percent else f"{abs(diff):,.0f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"

            val_str = f"{value:.2f}%" if is_percent else f"{value:,.0f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_sd = ((btc_sd - btc_prev_sd) / btc_prev_sd * 100) if btc_prev_sd else 0
        ip_btc_sd = dp_btc_sd >= 0
        dc_btc_sd = "#00cc66" if ip_btc_sd else "#ff4d4d"
        ar_btc_sd = "↑" if ip_btc_sd else "↓"
        d_btc_sd = f"<div style='margin-top:4px;'><span style='color:{dc_btc_sd}; font-size:0.85rem; background-color:{dc_btc_sd}20; padding:2px 6px; border-radius:4px;'>{ar_btc_sd} {abs(dp_btc_sd):.2f}%</span></div>"
        btc_html_sd = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_sd:,.2f}</span>{d_btc_sd}</div>"

        # CHART 1: STH & LTH SUPPLY
        col_title_sd, k1_sd, k2_sd, k3_sd, k4_sd, k5_sd = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_sd: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Supply Dynamics<br><span style='font-size: 1rem; color: #d1d4dc;'>STH & LTH Supply</span></h3></div>", unsafe_allow_html=True)
        with k1_sd: st.markdown(btc_html_sd, unsafe_allow_html=True)
        with k2_sd: render_kpi_sd("LTH Supply", last_sd.get('LTH Supply', 0), prev_sd.get('LTH Supply', 0), False)
        with k3_sd: render_kpi_sd("STH Supply", last_sd.get('STH Supply', 0), prev_sd.get('STH Supply', 0), False)
        st.markdown("---")

        df_sd, w_sd = apply_filters(df_supply_raw, st.session_state.tf_sd, st.session_state.sma_sd, st.session_state.cs_sd, st.session_state.tr_sd, st.session_state.cd_sd, ['LTH Supply', 'STH Supply'])

        col_fs_sd, col_tf_sd, col_sma_sd, col_sma_cst_sd, col_radio_sd, col_custom_sd = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_sd: focus_sd = st.toggle("Full Screen", key="tg_sd")
        with col_tf_sd: st.session_state.tf_sd = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_sd), key="tfs_sd")
        with col_sma_sd: st.session_state.sma_sd = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_sd), key="smas_sd")
        with col_sma_cst_sd:
            if st.session_state.sma_sd == "Custom": st.session_state.cs_sd = st.number_input("Days", min_value=1, value=st.session_state.cs_sd, label_visibility="collapsed", key="cst_sd")
        with col_radio_sd:
            c_idx_sd = t_opts.index(st.session_state.tr_sd) if st.session_state.tr_sd in t_opts else 5
            st.session_state.tr_sd = st.radio("Range:", t_opts, index=c_idx_sd, horizontal=True, label_visibility="collapsed", key="rg_sd")
        with col_custom_sd:
            if st.session_state.tr_sd == "Custom": st.session_state.cd_sd = st.number_input("Days back", min_value=7, value=st.session_state.cd_sd, label_visibility="collapsed", key="cdin_sd")
        
        opts_sd_sup = ['🔵 LTH Supply', '🔴 STH Supply']
        all_opts_sd_sup = opts_sd_sup.copy()
        if w_sd > 1: all_opts_sd_sup.extend([f"{m} (SMA {w_sd})" for m in opts_sd_sup])
            
        try: sel_sd_sup = st.pills("Supply Metrics", all_opts_sd_sup, default=opts_sd_sup, selection_mode="multi", label_visibility="collapsed", key="pills_sup")
        except: sel_sd_sup = st.multiselect("Supply Metrics", all_opts_sd_sup, default=opts_sd_sup, label_visibility="collapsed", key="ms_sup")

        chart_opts_sd = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_sd else 650, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
        series_sd = [{"type": 'Line', "data": get_s(df_sd, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        for m in sel_sd_sup:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            if base_m == '🔵 LTH Supply': c_col, c_name = '#4da6ff', 'LTH Supply'
            elif base_m == '🔴 STH Supply': c_col, c_name = '#ff4d4d', 'STH Supply'
            else: continue
            
            if is_sma: series_sd.append({"type": 'Line', "data": get_s(df_sd, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{c_name} SMA"}})
            else: series_sd.append({"type": 'Line', "data": get_s(df_sd, c_name), "options": {"color": c_col, "lineWidth": 1, "priceScaleId": 'left', "title": c_name}})

        renderLightweightCharts([{"chart": chart_opts_sd, "series": series_sd}], 'chart_supply')
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # CHART 2: STH & LTH % IN PROFIT & LOSS
        col_title_sd2, k1_sd2, k2_sd2, k3_sd2, k4_sd2, k5_sd2 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_sd2: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Supply Dynamics<br><span style='font-size: 1rem; color: #d1d4dc;'>% Supply in Profit/Loss</span></h3></div>", unsafe_allow_html=True)
        with k1_sd2: st.markdown(btc_html_sd, unsafe_allow_html=True)
        with k2_sd2: render_kpi_sd("Total % Profit", last_sd.get('Total % Profit', 0), prev_sd.get('Total % Profit', 0), True)
        with k3_sd2: render_kpi_sd("Total % Loss", last_sd.get('Total % Loss', 0), prev_sd.get('Total % Loss', 0), True)
        with k4_sd2: render_kpi_sd("LTH % Profit", last_sd.get('LTH % Profit', 0), prev_sd.get('LTH % Profit', 0), True)
        with k5_sd2: render_kpi_sd("STH % Profit", last_sd.get('STH % Profit', 0), prev_sd.get('STH % Profit', 0), True)
        st.markdown("---")

        col_fs_sd2, col_tf_sd2, col_sma_sd2, col_sma_cst_sd2, col_radio_sd2, col_custom_sd2 = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_sd2: focus_sd2 = st.toggle("Full Screen", key="tg_sd2")
        with col_tf_sd2: st.session_state.tf_sd = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_sd), key="tfs_sd2")
        with col_sma_sd2: st.session_state.sma_sd = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_sd), key="smas_sd2")
        with col_sma_cst_sd2:
            if st.session_state.sma_sd == "Custom": st.session_state.cs_sd = st.number_input("Days", min_value=1, value=st.session_state.cs_sd, label_visibility="collapsed", key="cst_sd2")
        with col_radio_sd2:
            c_idx_sd = t_opts.index(st.session_state.tr_sd) if st.session_state.tr_sd in t_opts else 5
            st.session_state.tr_sd = st.radio("Range:", t_opts, index=c_idx_sd, horizontal=True, label_visibility="collapsed", key="rg_sd2")
        with col_custom_sd2:
            if st.session_state.tr_sd == "Custom": st.session_state.cd_sd = st.number_input("Days back", min_value=7, value=st.session_state.cd_sd, label_visibility="collapsed", key="cdin_sd2")

        df_sd2, w_sd2 = apply_filters(df_supply_raw, st.session_state.tf_sd, st.session_state.sma_sd, st.session_state.cs_sd, st.session_state.tr_sd, st.session_state.cd_sd, ['LTH % Profit', 'STH % Profit', 'LTH % Loss', 'STH % Loss', 'Total % Profit', 'Total % Loss'])

        opts_sd_pct = ['⚪ Total % Profit', '⚫ Total % Loss', '🔵 LTH % Profit', '🟣 LTH % Loss', '🔴 STH % Profit', '🟠 STH % Loss']
        all_opts_sd_pct = opts_sd_pct.copy()
        if w_sd2 > 1: all_opts_sd_pct.extend([f"{m} (SMA {w_sd2})" for m in opts_sd_pct])
            
        try: sel_sd_pct = st.pills("Profit Metrics", all_opts_sd_pct, default=['⚪ Total % Profit', '🔵 LTH % Profit', '🔴 STH % Profit'], selection_mode="multi", label_visibility="collapsed", key="pills_pct")
        except: sel_sd_pct = st.multiselect("Profit Metrics", all_opts_sd_pct, default=['⚪ Total % Profit', '🔵 LTH % Profit', '🔴 STH % Profit'], label_visibility="collapsed", key="ms_pct")

        chart_opts_sd2 = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_sd2 else 650, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
        series_sd2 = [{"type": 'Line', "data": get_s(df_sd2, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        colors_sd2 = {
            '⚪ Total % Profit': ('#ffffff', 'Total % Profit'), '⚫ Total % Loss': ('#a3a8b8', 'Total % Loss'),
            '🔵 LTH % Profit': ('#4da6ff', 'LTH % Profit'), '🟣 LTH % Loss': ('#cc33ff', 'LTH % Loss'),
            '🔴 STH % Profit': ('#ff4d4d', 'STH % Profit'), '🟠 STH % Loss': ('#ff9933', 'STH % Loss')
        }

        for m in sel_sd_pct:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            if base_m in colors_sd2:
                c_col, c_name = colors_sd2[base_m]
                if is_sma: series_sd2.append({"type": 'Line', "data": get_s(df_sd2, f"{c_name}_SMA"), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": f"{c_name} SMA"}})
                else: series_sd2.append({"type": 'Line', "data": get_s(df_sd2, c_name), "options": {"color": c_col, "lineWidth": 1, "priceScaleId": 'left', "title": c_name}})

        renderLightweightCharts([{"chart": chart_opts_sd2, "series": series_sd2}], 'chart_profitpct')

# ------------------------------------------------------------------------------
# TAB 5: EXCHANGE FLOW (NEW)
# ------------------------------------------------------------------------------
elif selected_menu == "Exchange Flow":
    if not df_ex_raw.empty:
        last_ex = df_ex_raw.iloc[-1]
        prev_ex = df_ex_raw.iloc[-2] if len(df_ex_raw) > 1 else last_ex
        
        btc_ex = last_ex.get('BTC Price', 0)
        btc_prev_ex = prev_ex.get('BTC Price', 0)
        
        def render_kpi_ex(title, value, prev_val, is_flow=False):
            if pd.isna(value): 
                color = "#a3a8b8"
                d = ""
            else: 
                # Jika flow positif = Inflow = biasanya diartikan bearish (merah), outflow = bullish (hijau)
                # Tapi untuk net flow standard: Hijau jika positif, merah jika negatif (secara angka).
                color = "#00cc66" if value >= 0 else "#ff4d4d"
                if "Inflow" in title: color = "#ff4d4d" # Merah karena masuk bursa = potensi jual
                if "Outflow" in title: color = "#00cc66" # Hijau karena keluar bursa = akumulasi
                if "Total Balance" in title: color = "#4da6ff"
                
                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                diff_str = f"{abs(diff):,.0f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"

            val_str = f"{value:,.0f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_ex = ((btc_ex - btc_prev_ex) / btc_prev_ex * 100) if btc_prev_ex else 0
        ip_btc_ex = dp_btc_ex >= 0
        dc_btc_ex = "#00cc66" if ip_btc_ex else "#ff4d4d"
        ar_btc_ex = "↑" if ip_btc_ex else "↓"
        d_btc_ex = f"<div style='margin-top:4px;'><span style='color:{dc_btc_ex}; font-size:0.85rem; background-color:{dc_btc_ex}20; padding:2px 6px; border-radius:4px;'>{ar_btc_ex} {abs(dp_btc_ex):.2f}%</span></div>"
        btc_html_ex = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_ex:,.2f}</span>{d_btc_ex}</div>"

        col_title_ex, k1_ex, k2_ex, k3_ex, k4_ex, k5_ex = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_ex: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Exchange Flow<br><span style='font-size: 1rem; color: #d1d4dc;'>Liquidity & Balance</span></h3></div>", unsafe_allow_html=True)
        with k1_ex: st.markdown(btc_html_ex, unsafe_allow_html=True)
        with k2_ex: render_kpi_ex("Total Balance", last_ex.get('Total Balance', 0), prev_ex.get('Total Balance', 0))
        with k3_ex: render_kpi_ex("Net Flow", last_ex.get('Net Flow', 0), prev_ex.get('Net Flow', 0), True)
        with k4_ex: render_kpi_ex("Inflow", last_ex.get('Inflow', 0), prev_ex.get('Inflow', 0), True)
        with k5_ex: render_kpi_ex("Outflow", last_ex.get('Outflow', 0), prev_ex.get('Outflow', 0), True)
        st.markdown("---")

        df_ex, w_ex = apply_filters(df_ex_raw, st.session_state.tf_ex, st.session_state.sma_ex, st.session_state.cs_ex, st.session_state.tr_ex, st.session_state.cd_ex, ['Total Balance', 'Net Flow', 'Inflow', 'Outflow'])

        col_fs_ex, col_tf_ex, col_sma_ex, col_sma_cst_ex, col_radio_ex, col_custom_ex = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_ex: focus_ex = st.toggle("Full Screen", key="tg_ex")
        with col_tf_ex: st.session_state.tf_ex = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_ex), key="tfs_ex")
        with col_sma_ex: st.session_state.sma_ex = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_ex), key="smas_ex")
        with col_sma_cst_ex:
            if st.session_state.sma_ex == "Custom": st.session_state.cs_ex = st.number_input("Days", min_value=1, value=st.session_state.cs_ex, label_visibility="collapsed", key="cst_ex")
        with col_radio_ex:
            c_idx_ex = t_opts.index(st.session_state.tr_ex) if st.session_state.tr_ex in t_opts else 5
            st.session_state.tr_ex = st.radio("Range:", t_opts, index=c_idx_ex, horizontal=True, label_visibility="collapsed", key="rg_ex")
        with col_custom_ex:
            if st.session_state.tr_ex == "Custom": st.session_state.cd_ex = st.number_input("Days back", min_value=7, value=st.session_state.cd_ex, label_visibility="collapsed", key="cdin_ex")
        
        opts_ex_base = ['🔵 Total Balance', '⚪ Net Flow', '🔴 Inflow', '🟢 Outflow']
        all_opts_ex = opts_ex_base.copy()
        if w_ex > 1: all_opts_ex.extend([f"{m} (SMA {w_ex})" for m in opts_ex_base])
            
        try: sel_ex = st.pills("Metrics", all_opts_ex, default=['🔵 Total Balance', '⚪ Net Flow'], selection_mode="multi", label_visibility="collapsed", key="pills_ex")
        except: sel_ex = st.multiselect("Metrics", all_opts_ex, default=['🔵 Total Balance', '⚪ Net Flow'], label_visibility="collapsed", key="ms_ex")

        # Mengatur flow_scale tersembunyi agar Histogram Net Flow tidak merusak skala Balance
        chart_opts_ex = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, "height": 850 if focus_ex else 650, 
            "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}, "flow_scale": {"visible": False}
        }
        series_ex = [{"type": 'Line', "data": get_s(df_ex, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        for m in sel_ex:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🔵 Total Balance':
                if is_sma: series_ex.append({"type": 'Line', "data": get_s(df_ex, 'Total Balance_SMA'), "options": {"color": '#4da6ff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": "Balance SMA"}})
                else: series_ex.append({"type": 'Line', "data": get_s(df_ex, 'Total Balance'), "options": {"color": '#4da6ff', "lineWidth": 1, "priceScaleId": 'left', "title": 'Total Balance'}})
            
            elif base_m == '⚪ Net Flow':
                if is_sma:
                    series_ex.append({"type": 'Histogram', "data": get_s(df_ex, 'Net Flow_SMA'), "options": {"color": 'rgba(255, 255, 255, 0.4)', "priceScaleId": 'flow_scale', "title": "Net Flow SMA"}})
                else:
                    flow_raw = get_s(df_ex, 'Net Flow')
                    for d_val in flow_raw: d_val['color'] = 'rgba(0, 204, 102, 0.7)' if d_val['value'] >= 0 else 'rgba(255, 77, 77, 0.7)'
                    series_ex.append({"type": 'Histogram', "data": flow_raw, "options": {"priceScaleId": 'flow_scale', "title": 'Net Flow'}})
            
            elif base_m == '🔴 Inflow':
                if is_sma: series_ex.append({"type": 'Line', "data": get_s(df_ex, 'Inflow_SMA'), "options": {"color": '#ff4d4d', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'flow_scale', "title": "Inflow SMA"}})
                else: series_ex.append({"type": 'Line', "data": get_s(df_ex, 'Inflow'), "options": {"color": 'rgba(255, 77, 77, 0.7)', "lineWidth": 1, "priceScaleId": 'flow_scale', "title": 'Inflow'}})
                
            elif base_m == '🟢 Outflow':
                if is_sma: series_ex.append({"type": 'Line', "data": get_s(df_ex, 'Outflow_SMA'), "options": {"color": '#00cc66', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'flow_scale', "title": "Outflow SMA"}})
                else: series_ex.append({"type": 'Line', "data": get_s(df_ex, 'Outflow'), "options": {"color": 'rgba(0, 204, 102, 0.7)', "lineWidth": 1, "priceScaleId": 'flow_scale', "title": 'Outflow'}})

        renderLightweightCharts([{"chart": chart_opts_ex, "series": series_ex}], 'chart_exchange')
    else:
        st.info("Menunggu data Exchange Flow. Pastikan script auto_update.py sudah menarik data terbaru!")

# ------------------------------------------------------------------------------
# TAB 6: DERIVATIVES 
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
                diff_str = f"${abs(diff):,.2f}" if is_money else (f"{abs(diff):.4f}%" if is_percent else f"{abs(diff):,.0f}")
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"

            val_str = f"${value:,.2f}" if is_money else (f"{value:.4f}%" if is_percent else f"{value:,.0f}")
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_d = ((btc_d - btc_prev_d) / btc_prev_d * 100) if btc_prev_d else 0
        ip_btc_d = dp_btc_d >= 0
        dc_btc_d = "#00cc66" if ip_btc_d else "#ff4d4d"
        ar_btc_d = "↑" if ip_btc_d else "↓"
        d_btc_d = f"<div style='margin-top:4px;'><span style='color:{dc_btc_d}; font-size:0.85rem; background-color:{dc_btc_d}20; padding:2px 6px; border-radius:4px;'>{ar_btc_d} {abs(dp_btc_d):.2f}%</span></div>"
        btc_html_d = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_d:,.2f}</span>{d_btc_d}</div>"

        col_title, k1, k2, k3, k4, k5 = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Derivatives<br><span style='font-size: 1rem; color: #d1d4dc;'>Open Interest & Funding Rates</span></h3></div>", unsafe_allow_html=True)
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
            "crosshair": {"mode": 0}, "height": 850 if focus_d else 650, 
            "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}, "funding_scale": {"visible": False} 
        }
        series_d = [{"type": 'Line', "data": get_s(df_d, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        for m in active_metrics_d:
            is_sma = "(SMA" in m
            base_m = m.split(" (SMA")[0]
            
            if base_m == '🔵 Open Interest':
                if is_sma: series_d.append({"type": 'Line', "data": get_s(df_d, 'Open Interest_SMA'), "options": {"color": '#4da6ff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": "OI SMA"}})
                else: series_d.append({"type": 'Line', "data": get_s(df_d, 'Open Interest'), "options": {"color": '#4da6ff', "lineWidth": 1, "priceScaleId": 'left', "title": 'Open Interest'}})
            
            elif base_m == '📊 Funding Rate':
                if is_sma: series_d.append({"type": 'Line', "data": get_s(df_d, 'Funding Rate_SMA'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'funding_scale', "title": "Funding SMA"}})
                else:
                    funding_raw = get_s(df_d, 'Funding Rate')
                    for d_val in funding_raw: d_val['color'] = 'rgba(0, 204, 102, 0.7)' if d_val['value'] >= 0 else 'rgba(255, 77, 77, 0.7)'
                    series_d.append({"type": 'Histogram', "data": funding_raw, "options": {"priceScaleId": 'funding_scale', "title": 'Funding Rate'}})

        renderLightweightCharts([{"chart": chart_opts_d, "series": series_d}], 'chart_deriv')

# ------------------------------------------------------------------------------
# TAB 7: SOCIAL SENTIMENT
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
                color = "#4da6ff" 
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

        # ==========================================
        # CHART 1: FEAR & GREED INDEX
        # ==========================================
        if not df_fg_raw.empty:
            last_fg = df_fg_raw.iloc[-1]
            prev_fg = df_fg_raw.iloc[-2] if len(df_fg_raw) > 1 else last_fg
            
            fg_val = last_fg.get('Fear & Greed', 0)
            if fg_val < 25: fg_color, fg_status = "#ff4d4d", "Extreme Fear"
            elif fg_val < 45: fg_color, fg_status = "#ff9933", "Fear"
            elif fg_val <= 55: fg_color, fg_status = "#eab308", "Neutral"
            elif fg_val <= 75: fg_color, fg_status = "#00cc66", "Greed"
            else: fg_color, fg_status = "#006600", "Extreme Greed"

            col_title_fg, k1_fg, k2_fg, k3_fg, k4_fg, k5_fg = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
            with col_title_fg: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Social Sentiment<br><span style='font-size: 1rem; color: #d1d4dc;'>Fear & Greed Index</span></h3></div>", unsafe_allow_html=True)
            with k1_fg: st.markdown(btc_html_ss, unsafe_allow_html=True)
            with k2_fg: st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{fg_color}; font-size:0.95rem; font-weight:600;'>Index Value</span><br><span style='color:{fg_color}; font-size:1.4rem; font-weight:700;'>{fg_val:,.0f}</span><div style='margin-top:4px;'><span style='color:{fg_color}; font-size:0.85rem; background-color:{fg_color}20; padding:2px 6px; border-radius:4px;'>{fg_status}</span></div></div>", unsafe_allow_html=True)
            st.markdown("---")

            # 🟢 FIX: Sekarang mendukung filter Timeframe dan SMA secara dinamis
            df_fg, w_fg = apply_filters(df_fg_raw, st.session_state.tf_fg, st.session_state.sma_fg, st.session_state.cs_fg, st.session_state.tr_fg, st.session_state.cd_fg, ['Fear & Greed'])

            col_fs_fg, col_tf_fg, col_sma_fg, col_sma_cst_fg, col_radio_fg, col_custom_fg = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
            with col_fs_fg: focus_fg = st.toggle("Full Screen", key="tg_fg")
            with col_tf_fg: st.session_state.tf_fg = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_fg), key="tfs_fg")
            with col_sma_fg: st.session_state.sma_fg = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_fg), key="smas_fg")
            with col_sma_cst_fg:
                if st.session_state.sma_fg == "Custom": st.session_state.cs_fg = st.number_input("Days", min_value=1, value=st.session_state.cs_fg, label_visibility="collapsed", key="cst_fg")
            with col_radio_fg:
                c_idx_fg = t_opts.index(st.session_state.tr_fg) if st.session_state.tr_fg in t_opts else 5
                st.session_state.tr_fg = st.radio("Range:", t_opts, index=c_idx_fg, horizontal=True, label_visibility="collapsed", key="rg_fg")
            with col_custom_fg:
                if st.session_state.tr_fg == "Custom": st.session_state.cd_fg = st.number_input("Days back", min_value=7, value=st.session_state.cd_fg, label_visibility="collapsed", key="cdin_fg")
            
            opts_fg_base = ['📊 Fear & Greed']
            all_opts_fg = opts_fg_base.copy()
            if w_fg > 1: all_opts_fg.extend([f"{m} (SMA {w_fg})" for m in opts_fg_base])
                
            try: sel_fg = st.pills("F&G Metrics", all_opts_fg, default=['📊 Fear & Greed'], selection_mode="multi", label_visibility="collapsed", key="pills_fg")
            except: sel_fg = st.multiselect("F&G Metrics", all_opts_fg, default=['📊 Fear & Greed'], label_visibility="collapsed", key="ms_fg")

            # 🟢 FIX: Mengaktifkan skala kiri (leftPriceScale) agar grafik garis dapat dirender sejajar dengan BTC
            chart_opts_fg = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_fg else 650, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
            
            series_fg = [{"type": 'Line', "data": get_s(df_fg, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

            # Garis Referensi Statis (75 & 25)
            df_fg['Greed_Line'] = 75.0
            df_fg['Fear_Line'] = 25.0
            series_fg.append({"type": 'Line', "data": get_s(df_fg, 'Greed_Line'), "options": {"color": 'rgba(0, 204, 102, 0.4)', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Greed Area (75)'}})
            series_fg.append({"type": 'Line', "data": get_s(df_fg, 'Fear_Line'), "options": {"color": 'rgba(255, 77, 77, 0.4)', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Fear Area (25)'}})

            # Render Garis Fear & Greed
            for m in sel_fg:
                is_sma = "(SMA" in m
                if is_sma: 
                    series_fg.append({"type": 'Line', "data": get_s(df_fg, 'Fear & Greed_SMA'), "options": {"color": '#4da6ff', "lineWidth": 1.5, "lineStyle": 2, "priceScaleId": 'left', "title": "F&G SMA"}})
                else: 
                    series_fg.append({"type": 'Line', "data": get_s(df_fg, 'Fear & Greed'), "options": {"color": '#ffffff', "lineWidth": 1.5, "priceScaleId": 'left', "title": 'Fear & Greed'}})
                
            renderLightweightCharts([{"chart": chart_opts_fg, "series": series_fg}], 'chart_fg')
            st.markdown("<br><br>", unsafe_allow_html=True)

        # ==========================================
        # CHART 2: GOOGLE TRENDS
        # ==========================================
        col_title_gt, k1_gt, k2_gt, k3_gt, k4_gt, k5_gt = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_gt: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Social Sentiment<br><span style='font-size: 1rem; color: #d1d4dc;'>Google Trends (Global)</span></h3></div>", unsafe_allow_html=True)
        with k1_gt: st.markdown(btc_html_ss, unsafe_allow_html=True)
        with k2_gt: render_kpi_ss("BTC", last_ss.get('GTrend BTC', 0), prev_ss.get('GTrend BTC', 0))
        with k3_gt: render_kpi_ss("Crypto", last_ss.get('GTrend Crypto', 0), prev_ss.get('GTrend Crypto', 0))
        with k4_gt: render_kpi_ss("Binance", last_ss.get('GTrend Binance', 0), prev_ss.get('GTrend Binance', 0))
        st.markdown("---")

        df_gt, w_gt = apply_filters(df_sentiment_raw, st.session_state.tf_gt, st.session_state.sma_gt, st.session_state.cs_gt, st.session_state.tr_gt, st.session_state.cd_gt, ['GTrend BTC', 'GTrend Crypto', 'GTrend ETH', 'GTrend NFT', 'GTrend Binance', 'GTrend SOL', 'GTrend DOGE'])

        col_fs_gt, col_tf_gt, col_sma_gt, col_mode_gt, col_radio_gt, col_custom_gt = st.columns([1, 1.2, 1.2, 1.2, 5.5, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_gt: focus_gt = st.toggle("Full Screen", key="tg_gt")
        with col_tf_gt: st.session_state.tf_gt = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_gt), key="tfs_gt")
        with col_sma_gt: st.session_state.sma_gt = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_gt), key="smas_gt")
        with col_mode_gt: st.session_state.mode_gt = st.selectbox("Chart Type", ["Line", "Stacked Area"], index=["Line", "Stacked Area"].index(st.session_state.mode_gt), key="md_gt")
        with col_radio_gt:
            c_idx_gt = t_opts.index(st.session_state.tr_gt) if st.session_state.tr_gt in t_opts else 5
            st.session_state.tr_gt = st.radio("Range:", t_opts, index=c_idx_gt, horizontal=True, label_visibility="collapsed", key="rg_gt")
        with col_custom_gt:
            if st.session_state.tr_gt == "Custom": st.session_state.cd_gt = st.number_input("Days back", min_value=7, value=st.session_state.cd_gt, label_visibility="collapsed", key="cdin_gt")
        
        opts_gt_base = ['🔵 BTC', '🟢 ETH', '🟣 Crypto', '🟡 NFT', '🟠 Binance', '🔴 SOL', '🟤 DOGE']
        colors_gt = {'🔵 BTC': ('#4da6ff', 'GTrend BTC'), '🟢 ETH': ('#00cc66', 'GTrend ETH'), '🟣 Crypto': ('#cc33ff', 'GTrend Crypto'), '🟡 NFT': ('#eab308', 'GTrend NFT'), '🟠 Binance': ('#ff9933', 'GTrend Binance'), '🔴 SOL': ('#ff4d4d', 'GTrend SOL'), '🟤 DOGE': ('#cc9966', 'GTrend DOGE')}
        
        all_opts_gt = opts_gt_base.copy()
        if w_gt > 1: all_opts_gt.extend([f"{m} (SMA {w_gt})" for m in opts_gt_base])
            
        try: sel_gt = st.pills("GTrend Metrics", all_opts_gt, default=['🔵 BTC', '🟣 Crypto'], selection_mode="multi", label_visibility="collapsed", key="pills_gtrend")
        except: sel_gt = st.multiselect("GTrend Metrics", all_opts_gt, default=['🔵 BTC', '🟣 Crypto'], label_visibility="collapsed", key="ms_gtrend")

        chart_opts_gt = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_gt else 650, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
        series_gt = [{"type": 'Line', "data": get_s(df_gt, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        active_cols_gt = []
        for m in sel_gt:
            base_m = m.split(" (SMA")[0]
            if base_m in colors_gt:
                c_name = colors_gt[base_m][1]
                actual_col = f"{c_name}_SMA" if "(SMA" in m else c_name
                active_cols_gt.append((base_m, actual_col))

        if st.session_state.mode_gt == "Stacked Area":
            current_sum = pd.Series(0.0, index=df_gt.index)
            for base_m, actual_col in active_cols_gt:
                current_sum = current_sum + df_gt[actual_col].fillna(0)
                df_gt[actual_col + "_stacked"] = current_sum
            for base_m, actual_col in reversed(active_cols_gt):
                c_col = colors_gt[base_m][0]
                series_gt.append({"type": 'Area', "data": get_s(df_gt, actual_col + "_stacked"), "options": {"lineColor": c_col, "topColor": c_col + "66", "bottomColor": c_col + "0D", "lineWidth": 1, "priceScaleId": 'left', "title": actual_col}})
        else:
            for base_m, actual_col in active_cols_gt:
                c_col = colors_gt[base_m][0]
                series_gt.append({"type": 'Line', "data": get_s(df_gt, actual_col), "options": {"color": c_col, "lineWidth": 1, "priceScaleId": 'left', "title": actual_col}})

        renderLightweightCharts([{"chart": chart_opts_gt, "series": series_gt}], 'chart_gtrend')
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        # ==========================================
        # CHART 3: WIKIPEDIA PAGEVIEWS
        # ==========================================
        col_title_wk, k1_wk, k2_wk, k3_wk, k4_wk, k5_wk = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_wk: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Social Sentiment<br><span style='font-size: 1rem; color: #d1d4dc;'>Wikipedia Pageviews</span></h3></div>", unsafe_allow_html=True)
        with k1_wk: st.markdown(btc_html_ss, unsafe_allow_html=True)
        with k2_wk: render_kpi_ss("BTC", last_ss.get('Wiki BTC', 0), prev_ss.get('Wiki BTC', 0))
        with k3_wk: render_kpi_ss("Crypto", last_ss.get('Wiki Crypto', 0), prev_ss.get('Wiki Crypto', 0))
        with k4_wk: render_kpi_ss("Satoshi", last_ss.get('Wiki Satoshi', 0), prev_ss.get('Wiki Satoshi', 0))
        with k5_wk: render_kpi_ss("Blockchain", last_ss.get('Wiki Blockchain', 0), prev_ss.get('Wiki Blockchain', 0))
        st.markdown("---")

        df_wk, w_wk = apply_filters(df_sentiment_raw, st.session_state.tf_wk, st.session_state.sma_wk, st.session_state.cs_wk, st.session_state.tr_wk, st.session_state.cd_wk, ['Wiki BTC', 'Wiki Crypto', 'Wiki ETH', 'Wiki Satoshi', 'Wiki Blockchain', 'Wiki NFT', 'Wiki DOGE'])

        col_fs_wk, col_tf_wk, col_sma_wk, col_mode_wk, col_radio_wk, col_custom_wk = st.columns([1, 1.2, 1.2, 1.2, 5.5, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_wk: focus_wk = st.toggle("Full Screen", key="tg_wk")
        with col_tf_wk: st.session_state.tf_wk = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_wk), key="tfs_wk")
        with col_sma_wk: st.session_state.sma_wk = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_wk), key="smas_wk")
        with col_mode_wk: st.session_state.mode_wk = st.selectbox("Chart Type", ["Line", "Stacked Area"], index=["Line", "Stacked Area"].index(st.session_state.mode_wk), key="md_wk")
        with col_radio_wk:
            c_idx_wk = t_opts.index(st.session_state.tr_wk) if st.session_state.tr_wk in t_opts else 5
            st.session_state.tr_wk = st.radio("Range:", t_opts, index=c_idx_wk, horizontal=True, label_visibility="collapsed", key="rg_wk")
        with col_custom_wk:
            if st.session_state.tr_wk == "Custom": st.session_state.cd_wk = st.number_input("Days back", min_value=7, value=st.session_state.cd_wk, label_visibility="collapsed", key="cdin_wk")
        
        opts_wk_base = ['⚪ BTC', '🟢 Crypto', '🔵 ETH', '🟣 Satoshi', '🟡 Blockchain', '🔴 NFT', '🟤 DOGE']
        colors_wk = {'⚪ BTC': ('#ffffff', 'Wiki BTC'), '🟢 Crypto': ('#00cc66', 'Wiki Crypto'), '🔵 ETH': ('#4da6ff', 'Wiki ETH'), '🟣 Satoshi': ('#cc33ff', 'Wiki Satoshi'), '🟡 Blockchain': ('#eab308', 'Wiki Blockchain'), '🔴 NFT': ('#ff4d4d', 'Wiki NFT'), '🟤 DOGE': ('#cc9966', 'Wiki DOGE')}
        
        all_opts_wk = opts_wk_base.copy()
        if w_wk > 1: all_opts_wk.extend([f"{m} (SMA {w_wk})" for m in opts_wk_base])
            
        try: sel_wk = st.pills("Wiki Metrics", all_opts_wk, default=['⚪ BTC', '🟢 Crypto'], selection_mode="multi", label_visibility="collapsed", key="pills_wiki")
        except: sel_wk = st.multiselect("Wiki Metrics", all_opts_wk, default=['⚪ BTC', '🟢 Crypto'], label_visibility="collapsed", key="ms_wiki")

        chart_opts_wk = {"layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, "crosshair": {"mode": 0}, "height": 850 if focus_wk else 650, "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}}
        series_wk = [{"type": 'Line', "data": get_s(df_wk, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]

        active_cols_wk = []
        for m in sel_wk:
            base_m = m.split(" (SMA")[0]
            if base_m in colors_wk:
                c_name = colors_wk[base_m][1]
                actual_col = f"{c_name}_SMA" if "(SMA" in m else c_name
                active_cols_wk.append((base_m, actual_col))

        if st.session_state.mode_wk == "Stacked Area":
            current_sum_wk = pd.Series(0.0, index=df_wk.index)
            for base_m, actual_col in active_cols_wk:
                current_sum_wk = current_sum_wk + df_wk[actual_col].fillna(0)
                df_wk[actual_col + "_stacked"] = current_sum_wk
            for base_m, actual_col in reversed(active_cols_wk):
                c_col = colors_wk[base_m][0]
                series_wk.append({"type": 'Area', "data": get_s(df_wk, actual_col + "_stacked"), "options": {"lineColor": c_col, "topColor": c_col + "66", "bottomColor": c_col + "0D", "lineWidth": 1, "priceScaleId": 'left', "title": actual_col}})
        else:
            for base_m, actual_col in active_cols_wk:
                c_col = colors_wk[base_m][0]
                series_wk.append({"type": 'Line', "data": get_s(df_wk, actual_col), "options": {"color": c_col, "lineWidth": 1, "priceScaleId": 'left', "title": actual_col}})

        renderLightweightCharts([{"chart": chart_opts_wk, "series": series_wk}], 'chart_wiki')

# ------------------------------------------------------------------------------
# TAB 8: MARKET SIGNALS (RSI IMPLEMENTED NATIVELY)
# ------------------------------------------------------------------------------
elif selected_menu == "Market Signals":
    if not df_price_raw.empty:
        last_msig = df_price_raw.iloc[-1]
        prev_msig = df_price_raw.iloc[-2] if len(df_price_raw) > 1 else last_msig
        
        btc_msig = last_msig.get('BTC Price', 0)
        btc_prev_msig = prev_msig.get('BTC Price', 0)
        
        def render_kpi_msig(title, value, prev_val):
            if pd.isna(value) or value == 0: 
                color = "#a3a8b8"
                d = ""
            else: 
                color = "#ffffff"
                if value > 70: color = "#ff4d4d"
                elif value < 30: color = "#00cc66"

                diff = value - prev_val
                ip = diff >= 0
                dc = "#00cc66" if ip else "#ff4d4d"
                ar = "↑" if ip else "↓"
                diff_str = f"{abs(diff):.2f}"
                d = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {diff_str}</span></div>"

            val_str = f"{value:.2f}"
            st.markdown(f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:{color}; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{color}; font-size:1.4rem; font-weight:700;'>{val_str}</span>{d}</div>", unsafe_allow_html=True)

        dp_btc_msig = ((btc_msig - btc_prev_msig) / btc_prev_msig * 100) if btc_prev_msig else 0
        ip_btc_msig = dp_btc_msig >= 0
        dc_btc_msig = "#00cc66" if ip_btc_msig else "#ff4d4d"
        ar_btc_msig = "↑" if ip_btc_msig else "↓"
        d_btc_msig = f"<div style='margin-top:4px;'><span style='color:{dc_btc_msig}; font-size:0.85rem; background-color:{dc_btc_msig}20; padding:2px 6px; border-radius:4px;'>{ar_btc_msig} {abs(dp_btc_msig):.2f}%</span></div>"
        btc_html_msig = f"<div style='line-height: 1.4; padding: 5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_msig:,.2f}</span>{d_btc_msig}</div>"

        # CHART 1: TECHNICAL MOMENTUM (RSI)
        col_title_msig, k1_msig, k2_msig, k3_msig, k4_msig, k5_msig = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_title_msig: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Market Signals<br><span style='font-size: 1rem; color: #d1d4dc;'>Technical Momentum</span></h3></div>", unsafe_allow_html=True)
        with k1_msig: st.markdown(btc_html_msig, unsafe_allow_html=True)
        with k2_msig: render_kpi_msig("14-Day RSI", last_msig.get('RSI', 0), prev_msig.get('RSI', 0))
        st.markdown("---")

        df_msig, w_msig = apply_filters(df_price_raw, st.session_state.tf_msig, st.session_state.sma_msig, st.session_state.cs_msig, st.session_state.tr_msig, st.session_state.cd_msig, ['RSI'])

        col_fs_msig, col_tf_msig, col_sma_msig, col_sma_cst_msig, col_radio_msig, col_custom_msig = st.columns([1, 1.2, 1.2, 1, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_msig: focus_msig = st.toggle("Full Screen", key="tg_msig")
        with col_tf_msig: st.session_state.tf_msig = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_msig), key="tfs_msig")
        with col_sma_msig: st.session_state.sma_msig = st.selectbox("SMA", ["0d", "7d", "14d", "30d", "Custom"], index=["0d", "7d", "14d", "30d", "Custom"].index(st.session_state.sma_msig), key="smas_msig")
        with col_sma_cst_msig:
            if st.session_state.sma_msig == "Custom": st.session_state.cs_msig = st.number_input("Days", min_value=1, value=st.session_state.cs_msig, label_visibility="collapsed", key="cst_msig")
        with col_radio_msig:
            c_idx_msig = t_opts.index(st.session_state.tr_msig) if st.session_state.tr_msig in t_opts else 5
            st.session_state.tr_msig = st.radio("Range:", t_opts, index=c_idx_msig, horizontal=True, label_visibility="collapsed", key="rg_msig")
        with col_custom_msig:
            if st.session_state.tr_msig == "Custom": st.session_state.cd_msig = st.number_input("Days back", min_value=7, value=st.session_state.cd_msig, label_visibility="collapsed", key="cdin_msig")
        
        opts_msig_base = ['📊 14D RSI']
        all_opts_msig = opts_msig_base.copy()
        if w_msig > 1: all_opts_msig.extend([f"{m} (SMA {w_msig})" for m in opts_msig_base])
            
        try: sel_msig = st.pills("Signals", all_opts_msig, default=['📊 14D RSI'], selection_mode="multi", label_visibility="collapsed", key="pills_msig")
        except: sel_msig = st.multiselect("Signals", all_opts_msig, default=['📊 14D RSI'], label_visibility="collapsed", key="ms_msig")

        chart_opts_msig = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}}, 
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}}, 
            "crosshair": {"mode": 0}, "height": 850 if focus_msig else 650, 
            "rightPriceScale": {"visible": True}, "leftPriceScale": {"visible": True}
        }
        
        series_msig = [{"type": 'Line', "data": get_s(df_msig, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        
        df_msig['OB'] = 70.0
        df_msig['OS'] = 30.0
        series_msig.append({"type": 'Line', "data": get_s(df_msig, 'OB'), "options": {"color": '#ff4d4d', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Overbought (70)'}})
        series_msig.append({"type": 'Line', "data": get_s(df_msig, 'OS'), "options": {"color": '#00cc66', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": 'Oversold (30)'}})

        for m in sel_msig:
            is_sma = "(SMA" in m
            if is_sma: series_msig.append({"type": 'Line', "data": get_s(df_msig, 'RSI_SMA'), "options": {"color": '#ffffff', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'left', "title": "RSI SMA"}})
            else: series_msig.append({"type": 'Line', "data": get_s(df_msig, 'RSI'), "options": {"color": '#4da6ff', "lineWidth": 1, "priceScaleId": 'left', "title": '14D RSI'}})

        renderLightweightCharts([{"chart": chart_opts_msig, "series": series_msig}], 'chart_msig')

# ------------------------------------------------------------------------------
# TAB 9: BACKTESTING VIEW
# ------------------------------------------------------------------------------
elif selected_menu == "Backtesting":
    # Merge semua data yang dibutuhkan ke satu dataframe
    df_bt_base = df_mvrv_raw.copy() if not df_mvrv_raw.empty else pd.DataFrame()
    if not df_mom_raw.empty and not df_bt_base.empty:
        df_bt_base = pd.merge(df_bt_base, df_mom_raw[['Date','aSOPR','LTH SOPR','STH SOPR','NUPL','STH NUPL','LTH NUPL','Net Realized PL','STH P/L Ratio','LTH P/L Ratio']], on='Date', how='left')
    if not df_supply_raw.empty and not df_bt_base.empty:
        df_bt_base = pd.merge(df_bt_base, df_supply_raw[['Date','LTH Supply','STH Supply','LTH % Profit','STH % Profit','Total % Profit']], on='Date', how='left')
    if not df_ex_raw.empty and not df_bt_base.empty:
        df_bt_base = pd.merge(df_bt_base, df_ex_raw[['Date','Net Flow','Total Balance']], on='Date', how='left')
    if not df_deriv_raw.empty and not df_bt_base.empty:
        df_bt_base = pd.merge(df_bt_base, df_deriv_raw[['Date','Open Interest','Funding Rate']], on='Date', how='left')
    if not df_price_raw.empty and not df_bt_base.empty:
        df_bt_base = pd.merge(df_bt_base, df_price_raw[['Date','STH Cost Basis','LTH Cost Basis','Realized Price','CVDD','True Market Mean']], on='Date', how='left')

    if df_bt_base.empty:
        st.warning("Data tidak tersedia untuk Backtesting View.")
    else:
        # KPI row
        last_bt = df_bt_base.iloc[-1]
        prev_bt = df_bt_base.iloc[-2] if len(df_bt_base) > 1 else last_bt
        btc_bt = last_bt.get('BTC Price', 0)
        btc_prev_bt = prev_bt.get('BTC Price', 0)
        dp_bt = ((btc_bt - btc_prev_bt) / btc_prev_bt * 100) if btc_prev_bt else 0
        dc_bt = "#00cc66" if dp_bt >= 0 else "#ff4d4d"
        ar_bt = "↑" if dp_bt >= 0 else "↓"
        d_bt  = f"<div style='margin-top:4px;'><span style='color:{dc_bt}; font-size:0.85rem; background-color:{dc_bt}20; padding:2px 6px; border-radius:4px;'>{ar_bt} {abs(dp_bt):.2f}%</span></div>"
        col_title_bt, k1_bt = st.columns([1.5, 2], vertical_alignment="center")
        with col_title_bt: st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>Backtesting View<br><span style='font-size: 1rem; color: #d1d4dc;'>Multi-Indicator</span></h3></div>", unsafe_allow_html=True)
        with k1_bt: st.markdown(f"<div style='line-height:1.4; padding:5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>Current BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_bt:,.2f}</span>{d_bt}</div>", unsafe_allow_html=True)
        st.markdown("---")

        # Controls
        col_fs_bt, col_tf_bt, col_radio_bt, col_custom_bt = st.columns([1, 1.2, 6, 1.2], vertical_alignment="bottom", gap="small")
        with col_fs_bt: focus_bt = st.toggle("Full Screen", key="tg_bt")
        with col_tf_bt: st.session_state.tf_bt = st.selectbox("Timeframe", ["Daily", "3 Days", "Weekly", "Monthly"], index=["Daily", "3 Days", "Weekly", "Monthly"].index(st.session_state.tf_bt), key="tfs_bt")
        with col_radio_bt:
            c_idx_bt = t_opts.index(st.session_state.tr_bt) if st.session_state.tr_bt in t_opts else 5
            st.session_state.tr_bt = st.radio("Range:", t_opts, index=c_idx_bt, horizontal=True, label_visibility="collapsed", key="rg_bt")
        with col_custom_bt:
            if st.session_state.tr_bt == "Custom": st.session_state.cd_bt = st.number_input("Days back", min_value=7, value=st.session_state.cd_bt, label_visibility="collapsed", key="cdin_bt")

        # Apply filters
        all_bt_cols = ['MVRV','STH MVRV','LTH MVRV','aSOPR','LTH SOPR','STH SOPR','NUPL','STH NUPL','LTH NUPL',
                       'Net Realized PL','STH P/L Ratio','LTH P/L Ratio','LTH Supply','STH Supply',
                       'LTH % Profit','STH % Profit','Total % Profit','Net Flow','Total Balance',
                       'Open Interest','Funding Rate','STH Cost Basis','LTH Cost Basis','Realized Price','CVDD','True Market Mean']
        df_bt_base['Date_str'] = df_bt_base['Date'].dt.strftime('%Y-%m-%d') if 'Date_str' not in df_bt_base.columns else df_bt_base['Date_str']
        df_bt, _ = apply_filters(df_bt_base, st.session_state.tf_bt, "0d", 50, st.session_state.tr_bt, st.session_state.cd_bt, [])

        # ── Pill selectors ──
        # Chart atas: Price Levels overlay di BTC
        price_level_opts = ['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price', '🟣 True Market Mean', '🟢 CVDD']
        st.markdown("<span style='font-size:0.8rem; color:#a3a8b8;'>CHART ATAS — BTC + Price Levels</span>", unsafe_allow_html=True)
        try: sel_bt_pl = st.pills("Price Levels", price_level_opts, default=['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price'], selection_mode="multi", label_visibility="collapsed", key="pills_bt_pl")
        except: sel_bt_pl = st.multiselect("Price Levels", price_level_opts, default=['🔴 STH Cost Basis', '🔵 LTH Cost Basis', '⚪ Realized Price'], label_visibility="collapsed", key="ms_bt_pl")

        # Chart tengah: indikator pilihan (right scale)
        mid_ind_opts = ['🔵 MVRV', '🔴 STH MVRV', '🟢 LTH MVRV', '🩵 aSOPR', '🟠 STH SOPR', '🟤 LTH SOPR', '🟣 NUPL', '🩶 STH NUPL', '🫐 LTH NUPL', '⚪ STH P/L Ratio', '🟨 LTH P/L Ratio']
        st.markdown("<span style='font-size:0.8rem; color:#a3a8b8;'>CHART TENGAH — Indikator (drag scale kiri/kanan untuk adjust)</span>", unsafe_allow_html=True)
        try: sel_bt_mid = st.pills("Mid Indicators", mid_ind_opts, default=['🔵 MVRV', '🩵 aSOPR'], selection_mode="multi", label_visibility="collapsed", key="pills_bt_mid")
        except: sel_bt_mid = st.multiselect("Mid Indicators", mid_ind_opts, default=['🔵 MVRV', '🩵 aSOPR'], label_visibility="collapsed", key="ms_bt_mid")

        # Chart bawah: indikator pilihan (left scale)
        bot_ind_opts = ['📊 Net Flow', '💰 Total Balance', '📈 Open Interest', '💸 Funding Rate', '🔵 LTH Supply', '🔴 STH Supply', '⚪ Total % Profit', '🟦 LTH % Profit', '🟥 STH % Profit']
        st.markdown("<span style='font-size:0.8rem; color:#a3a8b8;'>CHART BAWAH — Indikator (drag scale kiri/kanan untuk adjust)</span>", unsafe_allow_html=True)
        try: sel_bt_bot = st.pills("Bot Indicators", bot_ind_opts, default=['📊 Net Flow', '📈 Open Interest'], selection_mode="multi", label_visibility="collapsed", key="pills_bt_bot")
        except: sel_bt_bot = st.multiselect("Bot Indicators", bot_ind_opts, default=['📊 Net Flow', '📈 Open Interest'], label_visibility="collapsed", key="ms_bt_bot")

        # ── Height split ──
        h_total_bt = 1100 if focus_bt else 900
        h_top_bt = int(h_total_bt * 0.38)
        h_mid_bt = int(h_total_bt * 0.32)
        h_bot_bt = h_total_bt - h_top_bt - h_mid_bt

        BASE_CHART = {
            "layout": {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}},
            "grid": {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}},
            "crosshair": {"mode": 0},
            "rightPriceScale": {"visible": True},
            "leftPriceScale": {"visible": True},
        }

        # ── CHART ATAS: BTC + Price Levels ──
        # timeScale harus tetap ada (visible) agar crosshair sync antar pane bekerja di ntf
        # Kita sembunyikan visual-nya saja via borderVisible+ticksVisible false, bukan visible:false
        chart_bt_top = {**BASE_CHART, "height": h_top_bt, "timeScale": {"borderVisible": False, "ticksVisible": False, "visible": True}}
        series_bt_top = [{"type": 'Line', "data": get_s(df_bt, 'BTC Price'), "options": {"color": '#f7931a', "lineWidth": 2, "priceScaleId": 'right', "title": 'BTC Price'}}]
        pl_colors = {
            '🔴 STH Cost Basis': ('#ff4d4d', 'STH Cost Basis'),
            '🔵 LTH Cost Basis': ('#4da6ff', 'LTH Cost Basis'),
            '⚪ Realized Price':  ('#ffffff', 'Realized Price'),
            '🟣 True Market Mean':('#00ffff', 'True Market Mean'),
            '🟢 CVDD':           ('#00cc66', 'CVDD'),
        }
        for m in sel_bt_pl:
            if m in pl_colors:
                c_col, c_name = pl_colors[m]
                series_bt_top.append({"type": 'Line', "data": get_s(df_bt, c_name), "options": {"color": c_col, "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'right', "title": c_name}})

        # ── CHART TENGAH: Indikator ──
        # Indikator dengan range mirip (0–5) → right; yang berbeda → left
        # LTH MVRV → left, sisanya → right; NUPL group → left
        chart_bt_mid = {**BASE_CHART, "height": h_mid_bt, "timeScale": {"borderVisible": False, "ticksVisible": False, "visible": True}}
        df_bt['Neutral_mid'] = 1.0
        series_bt_mid = [{"type": 'Line', "data": get_s(df_bt, 'Neutral_mid'), "options": {"color": 'rgba(255,255,255,0.2)', "lineWidth": 1, "lineStyle": 2, "priceScaleId": 'right', "title": 'Neutral 1.0'}}]
        mid_map = {
            '🔵 MVRV':         ('#4da6ff', 'MVRV',         'right'),
            '🔴 STH MVRV':     ('#ff4d4d', 'STH MVRV',     'right'),
            '🟢 LTH MVRV':     ('#00cc66', 'LTH MVRV',     'left'),
            '🩵 aSOPR':        ('#00e6e6', 'aSOPR',        'right'),
            '🟠 STH SOPR':     ('#ff9933', 'STH SOPR',     'right'),
            '🟤 LTH SOPR':     ('#cc9966', 'LTH SOPR',     'left'),
            '🟣 NUPL':         ('#cc33ff', 'NUPL',         'left'),
            '🩶 STH NUPL':     ('#a3a8b8', 'STH NUPL',     'left'),
            '🫐 LTH NUPL':     ('#6666ff', 'LTH NUPL',     'left'),
            '⚪ STH P/L Ratio':('#ffffff', 'STH P/L Ratio','right'),
            '🟨 LTH P/L Ratio':('#ffe119', 'LTH P/L Ratio','left'),
        }
        for m in sel_bt_mid:
            if m in mid_map:
                c_col, c_name, tscale = mid_map[m]
                series_bt_mid.append({"type": 'Line', "data": get_s(df_bt, c_name), "options": {"color": c_col, "lineWidth": 1.5, "priceScaleId": tscale, "title": c_name}})

        # ── CHART BAWAH: Indikator supply/flow/derivatives ──
        chart_bt_bot = {**BASE_CHART, "height": h_bot_bt}
        series_bt_bot = []
        bot_map = {
            '📊 Net Flow':       ('#ff6666', 'Net Flow',       'left'),
            '💰 Total Balance':  ('#4da6ff', 'Total Balance',  'right'),
            '📈 Open Interest':  ('#00cc66', 'Open Interest',  'right'),
            '💸 Funding Rate':   ('#ffe119', 'Funding Rate',   'left'),
            '🔵 LTH Supply':     ('#4da6ff', 'LTH Supply',     'right'),
            '🔴 STH Supply':     ('#ff4d4d', 'STH Supply',     'right'),
            '⚪ Total % Profit': ('#ffffff', 'Total % Profit', 'left'),
            '🟦 LTH % Profit':   ('#4da6ff', 'LTH % Profit',  'left'),
            '🟥 STH % Profit':   ('#ff4d4d', 'STH % Profit',  'left'),
        }
        for m in sel_bt_bot:
            if m in bot_map:
                c_col, c_name, tscale = bot_map[m]
                series_bt_bot.append({"type": 'Line', "data": get_s(df_bt, c_name), "options": {"color": c_col, "lineWidth": 1.5, "priceScaleId": tscale, "title": c_name}})

        # Kalau chart bawah kosong (tidak ada yang dipilih), tetap render placeholder
        if not series_bt_bot:
            df_bt['_empty'] = float('nan')
            series_bt_bot = [{"type": 'Line', "data": [], "options": {"color": '#131722', "priceScaleId": 'right'}}]

        renderLightweightCharts([
            {"chart": chart_bt_top, "series": series_bt_top},
            {"chart": chart_bt_mid, "series": series_bt_mid},
            {"chart": chart_bt_bot, "series": series_bt_bot},
        ], 'chart_backtesting')

# ------------------------------------------------------------------------------
# TAB: MVRV SIGNAL LAB
# ------------------------------------------------------------------------------
elif selected_menu == "MVRV Signal Lab":
    if df_mvrv_raw.empty:
        st.warning("Data MVRV tidak tersedia.")
    else:
        # Full dataset (no time filter) — needed for B5 scan + forward return computation
        df_sl_full = df_mvrv_raw.copy().sort_values('Date').reset_index(drop=True)

        last_sl  = df_sl_full.iloc[-1]
        prev_sl  = df_sl_full.iloc[-2] if len(df_sl_full) > 1 else last_sl
        btc_sl   = last_sl.get('BTC Price', 0)
        btc_prev_sl = prev_sl.get('BTC Price', 0)

        sth_now  = last_sl.get('STH MVRV', 0)
        lth_now  = last_sl.get('LTH MVRV', 0)
        sth_prev = prev_sl.get('STH MVRV', 0)
        lth_prev = prev_sl.get('LTH MVRV', 0)
        ratio_now  = lth_now / sth_now  if sth_now  > 0 else 0
        ratio_prev = lth_prev / sth_prev if sth_prev > 0 else 0

        _sma30_s  = df_sl_full['MVRV'].rolling(30, min_periods=1).mean()
        sma30_now  = _sma30_s.iloc[-1]
        sma30_prev = _sma30_s.iloc[-2]
        gap_now    = sth_now  - sma30_now
        gap_prev   = sth_prev - sma30_prev

        # KPI row
        dp_sl = ((btc_sl - btc_prev_sl) / btc_prev_sl * 100) if btc_prev_sl else 0
        dc_sl = "#00cc66" if dp_sl >= 0 else "#ff4d4d"
        ar_sl = "↑" if dp_sl >= 0 else "↓"
        d_sl_btc = f"<div style='margin-top:4px;'><span style='color:{dc_sl}; font-size:0.85rem; background-color:{dc_sl}20; padding:2px 6px; border-radius:4px;'>{ar_sl} {abs(dp_sl):.2f}%</span></div>"

        def _kpi_sl(col, title, val, prev, thresh=None):
            diff = val - prev
            dc = "#00cc66" if diff >= 0 else "#ff4d4d"
            ar = "↑" if diff >= 0 else "↓"
            c  = ("#00cc66" if val >= thresh else "#ff4d4d") if thresh is not None else "#ffffff"
            d  = f"<div style='margin-top:4px;'><span style='color:{dc}; font-size:0.85rem; background-color:{dc}20; padding:2px 6px; border-radius:4px;'>{ar} {abs(diff):.4f}</span></div>"
            col.markdown(f"<div style='line-height:1.4; padding:5px 0;'><span style='color:#a3a8b8; font-size:0.95rem; font-weight:600;'>{title}</span><br><span style='color:{c}; font-size:1.4rem; font-weight:700;'>{val:.4f}</span>{d}</div>", unsafe_allow_html=True)

        col_t_sl, k1_sl, k2_sl, k3_sl, k4_sl, k5_sl = st.columns([1.5, 1, 1, 1, 1, 1], vertical_alignment="center")
        with col_t_sl:
            st.markdown("<div style='border-right: 2px solid #333; padding-right: 15px;'><h3 style='color: #a855f7; margin: 0; font-weight: 700; font-size: 1.4rem;'>MVRV Signal Lab<br><span style='font-size: 1rem; color: #d1d4dc;'>B5 Cross + LTH/STH Ratio</span></h3></div>", unsafe_allow_html=True)
        with k1_sl:
            st.markdown(f"<div style='line-height:1.4; padding:5px 0;'><span style='color:#f7931a; font-size:0.95rem; font-weight:600;'>BTC Price</span><br><span style='color:#f7931a; font-size:1.4rem; font-weight:700;'>${btc_sl:,.2f}</span>{d_sl_btc}</div>", unsafe_allow_html=True)
        _kpi_sl(k2_sl, "STH MVRV",     sth_now,    sth_prev,    1.0)
        _kpi_sl(k3_sl, "LTH MVRV",     lth_now,    lth_prev,    1.0)
        _kpi_sl(k4_sl, "LTH/STH Ratio",ratio_now,  ratio_prev,  1.0)
        _kpi_sl(k5_sl, "STH vs SMA30", gap_now,    gap_prev,    0.0)

        st.markdown("---")

        # Controls row
        col_fs_sl, col_sa, col_sb, col_sc, col_b5f, col_rg_sl, col_cd_sl = st.columns(
            [1, 0.7, 0.7, 0.7, 0.9, 5, 1], vertical_alignment="bottom", gap="small"
        )
        with col_fs_sl: focus_sl = st.toggle("Full Screen", key="tg_sl")
        with col_sa:    sma_a = st.number_input("SMA A", min_value=2, max_value=200, value=st.session_state.sl_sma_a, key="sl_in_a")
        with col_sb:    sma_b = st.number_input("SMA B", min_value=2, max_value=200, value=st.session_state.sl_sma_b, key="sl_in_b")
        with col_sc:    sma_c = st.number_input("SMA C", min_value=2, max_value=200, value=st.session_state.sl_sma_c, key="sl_in_c")
        with col_b5f:   b5_thr = st.number_input("B5 STH<", min_value=0.5, max_value=2.0, value=float(st.session_state.sl_b5_thresh), step=0.05, format="%.2f", key="sl_in_b5")
        with col_rg_sl:
            c_idx_sl = t_opts.index(st.session_state.tr_sl) if st.session_state.tr_sl in t_opts else 5
            st.session_state.tr_sl = st.radio("Range:", t_opts, index=c_idx_sl, horizontal=True, label_visibility="collapsed", key="rg_sl")
        with col_cd_sl:
            if st.session_state.tr_sl == "Custom":
                st.session_state.cd_sl = st.number_input("Days back", min_value=7, value=st.session_state.cd_sl, label_visibility="collapsed", key="cdin_sl")

        st.session_state.sl_sma_a = sma_a
        st.session_state.sl_sma_b = sma_b
        st.session_state.sl_sma_c = sma_c
        st.session_state.sl_b5_thresh = b5_thr

        # Compute all derived columns on full dataset
        df_sl_full['LTH/STH Ratio'] = df_sl_full['LTH MVRV'] / df_sl_full['STH MVRV'].replace(0, float('nan'))
        sma_col_a = f'MVRV SMA{sma_a}'
        sma_col_b = f'MVRV SMA{sma_b}'
        sma_col_c = f'MVRV SMA{sma_c}'
        df_sl_full[sma_col_a] = df_sl_full['MVRV'].rolling(sma_a, min_periods=1).mean()
        df_sl_full[sma_col_b] = df_sl_full['MVRV'].rolling(sma_b, min_periods=1).mean()
        df_sl_full[sma_col_c] = df_sl_full['MVRV'].rolling(sma_c, min_periods=1).mean()
        df_sl_full['Date_str'] = df_sl_full['Date'].dt.strftime('%Y-%m-%d')

        # Apply time filter for chart display only
        t_max_sl = df_sl_full['Date'].max()
        if   st.session_state.tr_sl == "1 Month":         t_min_sl = t_max_sl - timedelta(days=30)
        elif st.session_state.tr_sl == "3 Months":        t_min_sl = t_max_sl - timedelta(days=90)
        elif st.session_state.tr_sl == "6 Months":        t_min_sl = t_max_sl - timedelta(days=180)
        elif st.session_state.tr_sl == "1 Year":          t_min_sl = t_max_sl - timedelta(days=365)
        elif st.session_state.tr_sl == "4 Years (Cycle)": t_min_sl = t_max_sl - timedelta(days=365*4)
        elif st.session_state.tr_sl == "Custom":          t_min_sl = t_max_sl - timedelta(days=st.session_state.cd_sl)
        else:                                              t_min_sl = df_sl_full['Date'].min()
        df_sl = df_sl_full[df_sl_full['Date'] >= t_min_sl].copy()

        # Historical event markers from KB (only shown if date is within chart range)
        _EVENTS = [
            ("2018-12-14", "Bear Bot '18",  "belowBar", "arrowUp",   "#00cc66"),
            ("2019-01-30", "BB Window",     "belowBar", "arrowUp",   "#00cc66"),
            ("2019-03-21", "Pre-Det '19",   "belowBar", "arrowUp",   "#4da6ff"),
            ("2019-04-25", "SoB '19",       "belowBar", "circle",    "#00ff88"),
            ("2021-11-09", "Peak '21",      "aboveBar", "arrowDown", "#ff4d4d"),
            ("2021-11-30", "LH '21",        "aboveBar", "arrowDown", "#ff9933"),
            ("2022-11-08", "FTX Bot",       "belowBar", "arrowUp",   "#00cc66"),
            ("2022-11-21", "Bear Bot '22",  "belowBar", "arrowUp",   "#00cc66"),
            ("2023-01-10", "Pre-Det '23",   "belowBar", "arrowUp",   "#4da6ff"),
            ("2023-02-10", "SoB '23",       "belowBar", "circle",    "#00ff88"),
            ("2025-10-05", "Peak '25",      "aboveBar", "arrowDown", "#ff4d4d"),
            ("2025-10-26", "LH '25",        "aboveBar", "arrowDown", "#ff9933"),
        ]
        _date_set = set(df_sl['Date_str'].tolist())
        _markers  = sorted(
            [{"time": d, "position": pos, "color": col, "shape": shp, "text": lbl, "size": 1}
             for d, lbl, pos, shp, col in _EVENTS if d in _date_set],
            key=lambda x: x["time"]
        )

        # Helper constant columns for chart reference lines
        df_sl['_1.0']  = 1.0
        df_sl['_3.0']  = 3.0
        df_sl['_1.0b'] = 1.0
        df_sl['_b5']   = b5_thr

        h_total_sl = 1000 if focus_sl else 800
        h_top_sl   = int(h_total_sl * 0.33)
        h_bot_sl   = h_total_sl - h_top_sl

        _BASE_SL = {
            "layout":    {"textColor": '#d1d4dc', "background": {"type": 'solid', "color": '#131722'}},
            "grid":      {"vertLines": {"color": "rgba(42,46,57,0.3)"}, "horzLines": {"color": "rgba(42,46,57,0.3)"}},
            "crosshair": {"mode": 0},
            "rightPriceScale": {"visible": True},
            "leftPriceScale":  {"visible": False},
        }

        # ── PLOTLY CHART: BTC Price + Rule B5 (top) / LTH/STH Ratio histogram (bottom) ──
        _date_price = df_sl.set_index('Date_str')['BTC Price']
        _ev_buy  = [(d, lbl) for d, lbl, pos, shp, col in _EVENTS if pos == "belowBar"  and d in _date_set]
        _ev_sell = [(d, lbl) for d, lbl, pos, shp, col in _EVENTS if pos == "aboveBar" and d in _date_set]

        def _ratio_color_plotly(v):
            if v < 1.0:  return 'rgba(0,204,102,0.40)'
            if v >= 3.0: return 'rgba(255,77,77,0.40)'
            return 'rgba(168,85,247,0.40)'

        _ratio_df  = df_sl[['Date_str', 'LTH/STH Ratio']].dropna()
        _x0, _x1   = df_sl['Date_str'].iloc[0], df_sl['Date_str'].iloc[-1]

        fig_sl = make_subplots(
            rows=2, cols=1,
            shared_xaxes=True,
            specs=[[{"secondary_y": True}], [{"secondary_y": False}]],
            row_heights=[0.62, 0.38],
            vertical_spacing=0.02,
        )

        # Row 1 — BTC Price (left axis)
        fig_sl.add_trace(go.Scatter(
            x=df_sl['Date_str'], y=df_sl['BTC Price'],
            name='BTC Price', line=dict(color='#f7931a', width=2),
            hovertemplate='$%{y:,.0f}<extra>BTC</extra>',
        ), row=1, col=1, secondary_y=False)

        # Event markers on BTC Price
        if _ev_buy:
            fig_sl.add_trace(go.Scatter(
                x=[d for d, _ in _ev_buy], y=[_date_price.get(d) for d, _ in _ev_buy],
                text=[lbl for _, lbl in _ev_buy], mode='markers+text',
                textposition='bottom center', textfont=dict(size=8, color='#00cc66'),
                marker=dict(symbol='triangle-up', size=9, color='#00cc66'),
                showlegend=False, hovertemplate='%{text}<extra></extra>',
            ), row=1, col=1, secondary_y=False)
        if _ev_sell:
            fig_sl.add_trace(go.Scatter(
                x=[d for d, _ in _ev_sell], y=[_date_price.get(d) for d, _ in _ev_sell],
                text=[lbl for _, lbl in _ev_sell], mode='markers+text',
                textposition='top center', textfont=dict(size=8, color='#ff9933'),
                marker=dict(symbol='triangle-down', size=9, color='#ff9933'),
                showlegend=False, hovertemplate='%{text}<extra></extra>',
            ), row=1, col=1, secondary_y=False)

        # Row 1 — STH MVRV + SMAs + reference lines (right axis)
        fig_sl.add_trace(go.Scatter(
            x=df_sl['Date_str'], y=df_sl['STH MVRV'],
            name='STH MVRV', line=dict(color='#ff4d4d', width=2),
            hovertemplate='%{y:.4f}<extra>STH MVRV</extra>',
        ), row=1, col=1, secondary_y=True)
        for col_name, color, label in [
            (sma_col_a, '#4da6ff', f'SMA{sma_a}'),
            (sma_col_b, '#00cc66', f'SMA{sma_b}'),
            (sma_col_c, '#ffe119', f'SMA{sma_c}'),
        ]:
            fig_sl.add_trace(go.Scatter(
                x=df_sl['Date_str'], y=df_sl[col_name],
                name=label, line=dict(color=color, width=1, dash='dot'),
                hovertemplate='%{y:.4f}<extra>' + label + '</extra>',
            ), row=1, col=1, secondary_y=True)
        for ref_y, ref_c in [(1.0, 'rgba(255,255,255,0.18)'), (b5_thr, 'rgba(255,170,0,0.28)')]:
            fig_sl.add_trace(go.Scatter(
                x=[_x0, _x1], y=[ref_y, ref_y],
                line=dict(color=ref_c, width=1, dash='dash'),
                showlegend=False, hoverinfo='skip', mode='lines',
            ), row=1, col=1, secondary_y=True)

        # Row 2 — LTH/STH Ratio histogram
        fig_sl.add_trace(go.Bar(
            x=_ratio_df['Date_str'], y=_ratio_df['LTH/STH Ratio'],
            marker_color=[_ratio_color_plotly(v) for v in _ratio_df['LTH/STH Ratio']],
            marker_line_width=0, name='LTH/STH Ratio',
            hovertemplate='%{y:.3f}<extra>LTH/STH</extra>',
        ), row=2, col=1)
        for ref_y, ref_c in [(1.0, 'rgba(255,255,255,0.18)'), (3.0, 'rgba(255,77,77,0.18)')]:
            fig_sl.add_trace(go.Scatter(
                x=[_x0, _x1], y=[ref_y, ref_y],
                line=dict(color=ref_c, width=1, dash='dash'),
                showlegend=False, hoverinfo='skip', mode='lines',
            ), row=2, col=1)

        _h_plotly = 1000 if focus_sl else 750
        fig_sl.update_layout(
            height=_h_plotly,
            paper_bgcolor='#131722', plot_bgcolor='#131722',
            font=dict(color='#d1d4dc', size=11),
            legend=dict(orientation='h', yanchor='bottom', y=1.01, xanchor='left', x=0,
                        bgcolor='rgba(0,0,0,0)', bordercolor='rgba(0,0,0,0)', font=dict(size=10)),
            margin=dict(l=10, r=10, t=30, b=10),
            hovermode='x unified', barmode='overlay',
        )
        fig_sl.update_xaxes(showgrid=True, gridcolor='rgba(42,46,57,0.4)', zeroline=False)
        fig_sl.update_yaxes(showgrid=True, gridcolor='rgba(42,46,57,0.4)', zeroline=False)
        fig_sl.update_yaxes(title_text='BTC Price ($)', secondary_y=False, row=1, col=1, tickformat='$,.0f')
        fig_sl.update_yaxes(title_text='MVRV', secondary_y=True, row=1, col=1, showgrid=False)
        fig_sl.update_yaxes(title_text='LTH/STH Ratio', row=2, col=1)

        st.plotly_chart(fig_sl, use_container_width=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # ── B5 SIGNAL SCAN TABLE ─────────────────────────────────────────────────
        st.markdown(f"**B5 Signal Log** — STH MVRV cross above MVRV SMA{sma_b}  |  filter: STH < {b5_thr:.2f}")

        # Scan on full (unfiltered) dataset so forward returns can be computed
        _sth  = df_sl_full['STH MVRV']
        _sref = df_sl_full[sma_col_b]
        _cross_up = (_sth > _sref) & (_sth.shift(1) <= _sref.shift(1)) & (_sth < b5_thr)
        cross_rows = df_sl_full[_cross_up].copy()

        if cross_rows.empty:
            st.info(f"Tidak ada B5 crossing ditemukan pada SMA{sma_b} dengan filter STH < {b5_thr:.2f}.")
        else:
            cross_list = cross_rows.reset_index()  # original df_sl_full index preserved in 'index' col

            # Classify ALERT / CONFIRM (pairs within 90 days = same bear recovery event)
            types = []
            prev_d_c  = None
            pair_num  = 0
            in_pair   = False
            for _, r in cross_list.iterrows():
                d = r['Date']
                if prev_d_c is None or (d - prev_d_c).days > 90:
                    pair_num += 1
                    types.append(f"#{pair_num} ALERT")
                    in_pair = True
                elif in_pair:
                    types.append(f"#{pair_num} CONFIRM")
                    in_pair = False
                else:
                    pair_num += 1
                    types.append(f"#{pair_num} ALERT")
                    in_pair = True
                prev_d_c = d
            cross_list['Type'] = types

            # Forward returns (index-based lookup on df_sl_full)
            rows_out = []
            for _, r in cross_list.iterrows():
                orig_idx = r['index']
                ep = r['BTC Price']

                def fwd(n, _idx=orig_idx, _ep=ep):
                    fi = _idx + n
                    if fi >= len(df_sl_full) or _ep <= 0: return None
                    return (df_sl_full.loc[fi, 'BTC Price'] - _ep) / _ep * 100

                r7, r30, r90 = fwd(7), fwd(30), fwd(90)
                rows_out.append({
                    'Tanggal':       r['Date'].strftime('%Y-%m-%d'),
                    'BTC Price':     f"${ep:,.0f}",
                    'STH MVRV':      f"{r['STH MVRV']:.4f}",
                    f'SMA{sma_b}':   f"{r[sma_col_b]:.4f}",
                    'Type':          r['Type'],
                    '7d %':          f"{r7:+.1f}%" if r7 is not None else "—",
                    '30d %':         f"{r30:+.1f}%" if r30 is not None else "—",
                    '90d %':         f"{r90:+.1f}%" if r90 is not None else "—",
                })

            st.dataframe(pd.DataFrame(rows_out), use_container_width=True, hide_index=True)

            def _pos_rate(col):
                vals = [r[col] for r in rows_out if r[col] != "—"]
                if not vals: return "—"
                pos = sum(1 for v in vals if float(v.replace('%','').replace('+','')) > 0)
                return f"{pos}/{len(vals)}"

            sc1, sc2, sc3, sc4 = st.columns(4)
            sc1.metric("Total Crossings",   len(cross_list))
            sc2.metric("7d Positive",        _pos_rate('7d %'))
            sc3.metric("30d Positive",       _pos_rate('30d %'))
            sc4.metric("90d Positive",       _pos_rate('90d %'))

