# --- SUNTIKAN CSS KHUSUS UNTUK TOMBOL METRIK ---
st.markdown("""
<style>
/* Kondisi Tombol OFF (Mati, Abu-abu, Tercoret) */
div[data-testid="stPill"] label[data-selected="false"] {
    background-color: transparent !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    color: #555555 !important;
    text-decoration: line-through !important;
    transition: all 0.3s ease;
}

/* Kondisi Tombol ON (Menyala, Gradasi Ungu, Garis Glowing) */
div[data-testid="stPill"] label[data-selected="true"] {
    background: linear-gradient(135deg, rgba(88, 28, 135, 0.9), rgba(46, 16, 101, 0.8)) !important;
    border: 1px solid #a855f7 !important;
    box-shadow: 0 0 12px rgba(168, 85, 247, 0.7) !important;
    color: #ffffff !important;
    text-decoration: none !important;
}

.block-container { padding-top: 1rem; padding-bottom: 1rem; max-width: 100%; }
</style>
""", unsafe_allow_html=True)
