import streamlit as st
import pandas as pd
from datetime import timedelta
from streamlit_lightweight_charts import renderLightweightCharts

# ==============================================================================
# 1. PENGATURAN HALAMAN UTAMA
# ==============================================================================
st.set_page_config(
    page_title="MoneyBag Journal | On-Chain Dashboard",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.title("Bitcoin On-Chain: STH Cost Basis 📊")
st.markdown("Dasbor interaktif untuk memantau momentum dan basis biaya pemegang jangka pendek (STH).")

# ==============================================================================
# 2. FUNGSI MEMBACA DATA (DARI CSV HASIL AUTOMASI)
# ==============================================================================
@st.cache_data(ttl=3600) # Data di-cache selama 1 jam agar web sangat cepat
def load_data():
    try:
        df = pd.read_csv("Master_Onchain_Data.csv")
        
        # --- PERBAIKAN: Menyamakan / Menerjemahkan nama kolom dari API ---
        df.rename(columns={
            'date': 'Date',
            'btc_price': 'BTC Price',
            'active_realized_price': 'STH Cost Basis' # Kita pakai ini sebagai proxy garis cost basis
        }, inplace=True)
        # ------------------------------------------------------------------

        df['Date'] = pd.to_datetime(df['Date'])
        df = df.sort_values('Date')
        return df
    except Exception as e:
        st.error(f"Error membaca data: {e}")
        return pd.DataFrame()
