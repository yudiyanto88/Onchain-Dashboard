"""Loader dan filter data untuk dashboard v2.

Sengaja berdiri sendiri (tidak mengimpor app.py) supaya dashboard lama
tidak ikut terpengaruh saat file ini berubah.
"""
from datetime import timedelta

import pandas as pd
import streamlit as st


def _prepare(df):
    """Normalisasi kolom Date: parse, buang yang gagal, urutkan, buang duplikat."""
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    return (df.dropna(subset=['Date'])
              .sort_values('Date')
              .drop_duplicates(subset=['Date'], keep='last'))


# Jendela rolling untuk Z-Score, dalam hari kalender.
ROLLING_WINDOWS = {"1Y": 365, "2Y": 730, "4Y": 1460}


@st.cache_data(ttl=3600)
def load_mvrv():
    df = pd.read_csv("data_mvrv.csv")
    df.rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'mvrv_ratio': 'MVRV', 'sth_mvrv': 'STH MVRV', 'lth_mvrv': 'LTH MVRV',
        'mvrv_zscore': 'MVRV Z-Score',
    }, inplace=True)
    df = _prepare(df)
    # Z-Score rolling tidak ada di CSV: dihitung dari MVRV Ratio terhadap rata-rata dan
    # simpangan sekian hari terakhir. Menurut KB MVRV v1.4 (Catatan Tambahan) angka ini
    # alat bantu visual, bukan sinyal yang berdiri sendiri — jendela mana pun yang dipakai.
    for tahun, hari in ROLLING_WINDOWS.items():
        jendela = df['MVRV'].rolling(hari)
        df[f'MVRV Z-Score {tahun}'] = (df['MVRV'] - jendela.mean()) / jendela.std()
    return df


def date_bounds(df):
    """Tanggal paling awal dan paling akhir yang tersedia di data."""
    return df['Date'].min().date(), df['Date'].max().date()


def preset_range(preset, dmin, dmax):
    """Terjemahkan preset rentang jadi sepasang tanggal."""
    days = {
        "1M": 30, "3M": 90, "6M": 180,
        "1Y": 365, "4Y": 365 * 4,
    }.get(preset)
    if days is None:
        return dmin, dmax
    lo = dmax - timedelta(days=days)
    return max(lo, dmin), dmax


def smooth_column(series, kind, period):
    """Hitung satu garis penghalus. SMA merata-rata, EMA memberi bobot lebih ke data baru."""
    if kind == "EMA":
        return series.ewm(span=period, adjust=False).mean()
    return series.rolling(period, min_periods=1).mean()


def apply_filters(df, smooth_kind, periods, date_from, date_to, cols):
    """Tambahkan garis penghalus, lalu potong menurut rentang tanggal.

    Tidak ada resampling: metrik on-chain harian dipertahankan apa adanya supaya
    tanggal perpotongan (cross) tidak bergeser.

    Kolom hasil diberi nama "<kolom>__SMA50", "<kolom>__EMA14", dan seterusnya.
    """
    if df.empty:
        return df

    dff = df.copy()

    if smooth_kind in ("SMA", "EMA"):
        for c in cols:
            if c not in dff.columns:
                continue
            for p in periods:
                dff[f"{c}__{smooth_kind}{p}"] = smooth_column(dff[c], smooth_kind, p)

    lo = pd.Timestamp(date_from)
    hi = pd.Timestamp(date_to)
    dff = dff[(dff['Date'] >= lo) & (dff['Date'] <= hi)].copy()
    dff['Date_str'] = dff['Date'].dt.strftime('%Y-%m-%d')
    return dff


def series_points(df, col):
    """Ubah satu kolom jadi format {time, value} yang dipakai lightweight-charts."""
    if col not in df.columns:
        return []
    clean = df[['Date_str', col]].dropna()
    return clean.rename(columns={'Date_str': 'time', col: 'value'}).to_dict('records')
