import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- CONFIGURASI HALAMAN ---
st.set_page_config(page_title="Yudiyanto | On-Chain Dashboard", layout="wide")

# --- CUSTOM CSS (PREMIUM DARK NAVY THEME) ---
st.markdown(f"""
    <style>
    /* Global Styles */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');
    html, body, [data-testid="stSidebar"] {{
        font-family: 'Inter', sans-serif;
        background-color: #131722;
    }}
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {{
        background-color: #151924;
        border-right: 1px solid #2B2F3A;
        width: 300px !important;
    }}
    
    /* Control Panel Font Size */
    .stSelectbox label, .stSlider label, .stMultiSelect label {{
        font-size: 0.85rem !important;
        color: #848E9C;
    }}

    /* Tab Block Hack for st.radio */
    div[data-testid="stSidebarUserContent"] .stRadio > div {{
        flex-direction: column;
    }}
    div[data-testid="stSidebarUserContent"] .stRadio label {{
        background-color: #1E232F;
        border: 1px solid #2B2F3A;
        padding: 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        transition: 0.3s;
    }}
    div[data-testid="stSidebarUserContent"] .stRadio label:hover {{
        border-color: #f7931a;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- HELPER FUNCTIONS ---
def apply_premium_style(fig):
    """Menerapkan DNA Visual MoneyBag Journal ke Plotly"""
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font_color="#D1D4DC",
        margin=dict(l=0, r=0, t=30, b=0),
        hovermode="x unified",
        showlegend=False,
        xaxis=dict(
            showgrid=True, gridcolor='rgba(43, 47, 58, 0.3)', 
            linecolor='#2B2F3A', zeroline=False
        ),
        yaxis=dict(
            showgrid=True, gridcolor='rgba(43, 47, 58, 0.3)', 
            linecolor='#2B2F3A', zeroline=False, side='right'
        )
    )
    return fig

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.image("https://via.placeholder.com/150x50?text=LOGO+MONEYBAG", use_column_width=False) # Ganti link logo jika ada
    menu = st.radio(
        "NAVIGATION",
        ["Price Levels", "Market Valuation", "Profit & Loss", "Supply Dynamics", "Derivatives", "Social Sentiment", "Market Signals"],
        label_visibility="hidden"
    )

# --- DATA LOADING (MOCKUP) ---
# Di tahap ini, load 7 file CSV sesuai arsitektur backend
@st.cache_data
def load_data(file_name):
    # df = pd.read_csv(f'data/{file_name}')
    # return df
    pass

# --- MAIN LAYOUT ---
# Baris 1: Judul & KPI
col_title, kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns([1.5, 1, 1, 1, 1, 1])
with col_title:
    st.subheader(f"{menu}")
    st.markdown("---")

# Baris 2: Control Panel
c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
with c1: timeframe = st.selectbox("Timeframe", ["Daily", "Weekly"], label_visibility="collapsed")
with c2: sma_toggle = st.multiselect("Overlay Indicators", ["200 DMA", "50 WMA", "True Market Mean"], label_visibility="collapsed")

# Baris 3: Selection Metric
selected_metric = st.pills("Metrics", ["Price", "Realized Cap", "Delta Cap"])

# Baris 4: Plotly Chart Logic
def render_chart(menu_type):
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    
    # --- LOGIC PER TAB ---
    if menu_type == "Price Levels":
        # Contoh Plotting BTC Price
        fig.add_trace(go.Scatter(
            x=[1,2,3,4], y=[40000, 42000, 41000, 45000], # Ganti dengan data['Price']
            line=dict(color='#f7931a', width=2),
            name="BTC Price"
        ))
        # Indikator Dashed
        fig.add_trace(go.Scatter(
            x=[1,2,3,4], y=[38000, 38500, 39000, 39500],
            line=dict(color='#00ffff', width=1.5, dash='dash'),
            name="True Market Mean"
        ))

    elif menu_type == "Profit & Loss":
        # Realized P/L as Histogram
        fig.add_trace(go.Bar(
            x=[1,2,3,4], y=[100, -50, 200, -20],
            marker_color='rgba(0, 255, 0, 0.3)', # Contoh warna
            name="Realized P/L"
        ))
        # SOPR as Line
        fig.add_trace(go.Scatter(
            x=[1,2,3,4], y=[1.05, 0.98, 1.10, 1.01],
            line=dict(color='#ffffff', width=1.5),
            name="SOPR"
        ), secondary_y=True)

    elif menu_type == "Social Sentiment":
        # BTC Price in White for Sentiment Context
        fig.add_trace(go.Scatter(
            x=[1,2,3,4], y=[40000, 42000, 41000, 45000],
            line=dict(color='#ffffff', width=1.5),
            name="BTC Price"
        ))
        # Fear & Greed as Markers
        fig.add_trace(go.Scatter(
            x=[1,2,3,4], y=[40000, 42000, 41000, 45000],
            mode='markers',
            marker=dict(size=10, color=[20, 50, 80, 40], colorscale='RdYlGn', showscale=False),
            name="Fear & Greed Index"
        ))

    elif menu_type == "Market Signals":
        # RSI 14D dengan Banding
        fig.add_trace(go.Scatter(x=[1,2,3], y=[30, 65, 75], line=dict(color='#8884d8')))
        fig.add_hline(y=70, line_dash="dash", line_color="#ff4b4b", annotation_text="Overbought")
        fig.add_hline(y=30, line_dash="dash", line_color="#00ff41", annotation_text="Oversold")

    # Final Styling
    fig = apply_premium_style(fig)
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

render_chart(menu)
