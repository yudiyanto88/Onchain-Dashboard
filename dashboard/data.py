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


@st.cache_data(ttl=3600)
def load_price_levels():
    """Level harga on-chain dan teknikal, plus AVIV Mean/Upper dari data_aviv.csv.

    AVIV dihitung ulang dari kolom mentah seperti app.py dan alerts/alert_check.py:
    kolom price_at_aviv_* bawaan ChartInspect salah basis harga (±9–10% terlalu tinggi,
    lihat README). AVIV Upper framework v2 = mean + 0,5 simpangan baku.
    """
    df = pd.read_csv("data_price_level.csv")
    df.rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'sth_cost_basis': 'STH RP', 'realized_price': 'RP', 'lth_cost_basis': 'LTH RP',
        'cvdd': 'CVDD', 'MVRV 0σ': 'MVRV 0σ',
        '200_dma': '200 DMA', '50_wma': '50 WMA', '200_wma': '200 WMA',
    }, inplace=True)
    df = _prepare(df)

    aviv = _prepare(pd.read_csv("data_aviv.csv").rename(columns={'date': 'Date'}))
    aviv = aviv[['Date', 'btc_price', 'aviv_ratio', 'aviv_mean', 'aviv_upper_1sd']]
    dasar = aviv['btc_price'] / aviv['aviv_ratio']
    aviv['AVIV Mean'] = dasar * aviv['aviv_mean']
    aviv['AVIV Upper'] = dasar * (aviv['aviv_mean'] + 0.5 * (aviv['aviv_upper_1sd'] - aviv['aviv_mean']))
    # Rata-rata historis AVIV baru terbentuk dari segelintir hari di awal data: 84 hari
    # pertama (17 Jul–9 Okt 2010) AVIV Mean jatuh sampai ±300x di bawah harga dan menarik
    # sumbu Log ke 0.0002. Hari-hari sebelum rasio AVIV Mean/harga pertama kali wajar
    # (0,2–5) disembunyikan; level sesudahnya tidak berubah.
    wajar = (aviv['AVIV Mean'] / aviv['btc_price']).between(0.2, 5)
    if wajar.any():
        awal = aviv.loc[wajar, 'Date'].iloc[0]
        aviv.loc[aviv['Date'] < awal, ['AVIV Mean', 'AVIV Upper']] = float('nan')
    return df.merge(aviv[['Date', 'AVIV Mean', 'AVIV Upper']], on='Date', how='left')


@st.cache_data(ttl=3600)
def load_sopr():
    """aSOPR, STH-SOPR, LTH-SOPR dari data_momentum.csv, plus gap STH-SOPR.

    Gap memakai rumus KB SOPR v1.4 §12: SMA90 STH-SOPR dikurangi SMA60 dari SMA90 itu
    (double-smoothed). Rumus ini yang mereproduksi angka KB persis (+0.02447 10 Jan 2021,
    cross turun 28 Mar 2021 dan 30 Nov 2021). Catatan: alerts/alert_check.py menghitung
    SMA60 − SMA90, hasilnya berbeda — dilaporkan ke user 13 Sep 2026, belum diputuskan.
    NUPL di file yang sama sengaja tidak dimuat: halaman sendiri.
    """
    df = pd.read_csv("data_momentum.csv")
    df.rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'asopr': 'aSOPR', 'sth_sopr': 'STH-SOPR', 'lth_sopr': 'LTH-SOPR',
    }, inplace=True)
    df = _prepare(df)
    ma90 = df['STH-SOPR'].rolling(90).mean()
    df['STH-SOPR Gap'] = ma90 - ma90.rolling(60).mean()
    return df


@st.cache_data(ttl=3600)
def load_supply():
    """Persen supply dalam untung: semua holder, STH, LTH (data_supply.csv).

    Kolom *_in_loss tidak dimuat: di data selalu 100 − in_profit, dan tooltip menghitungnya
    sendiri. Jumlah supply LTH/STH (BTC) belum dipakai halaman ini.
    """
    df = pd.read_csv("data_supply.csv")
    df.rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'percent_btc_in_profit': 'Total Supply in Profit',
        'pct_sth_in_profit': 'STH Supply in Profit',
        'pct_lth_in_profit': 'LTH Supply in Profit',
    }, inplace=True)
    return _prepare(df)


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
