"""Loader dan filter data untuk dashboard v2.

Sengaja berdiri sendiri (tidak mengimpor app.py) supaya dashboard lama
tidak ikut terpengaruh saat file ini berubah.
"""
from datetime import timedelta

import numpy as np
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
    return df.merge(_median_mvrv()[['Date', 'Median MVRV']], on='Date', how='left')



@st.cache_data(ttl=3600)
def load_mvrv_momentum():
    """Tiga osilator momentum MVRV Ratio (data_mvrv.csv) + rata-rata sepanjang sejarah.

    - Momentum = SMA30(MVRV) - SMA30 dari SMA30 itu: cross nol = MVRV Momentum bullish/bearish
      cross di framework v2 (K2).
    - MVRV / SMA180: < 1 = MVRV di bawah SMA180-nya (penghenti pembelian K2 bila >= 7 hari).
    - MVRV / SMA365: versi Glassnode "MVRV over its 365-day mean", pembanding jangka panjang.
    Rata-rata MVRV seluruh sejarah = 1,80 (22 Sep 2026; sama dengan angka Glassnode 1,8).
    Ambang framework (>= 7 hari dsb.) tidak digambar.
    """
    df = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price', 'mvrv_ratio'])
                  .rename(columns={'date': 'Date', 'btc_price': 'BTC Price', 'mvrv_ratio': 'MVRV'}))
    v = df['MVRV']
    cepat = v.rolling(30).mean()
    df['MVRV Momentum'] = cepat - cepat.rolling(30).mean()
    df['MVRV / SMA180'] = v / v.rolling(180).mean()
    df['MVRV / SMA365'] = v / v.rolling(365).mean()
    df['MVRV Mean'] = v.mean()
    return df


@st.cache_data(ttl=3600)
def _median_mvrv():
    """Median MVRV dan Median Realized Price dari data_median_mvrv.csv.

    Median = harga beli koin di tengah sebaran, bukan rata-rata: puncak siklusnya
    lebih tinggi dari MVRV biasa (2013: 11,3 vs 4,95) karena rata-rata tertarik oleh
    koin lama berharga sangat rendah.

    Dua catatan data (18 Sep 2026): baris resmi berhenti 18 Agt 2026 lalu melompat ke
    18 Sep 2026 (30 hari kosong, garis putus di chart), dan baris terakhir itu berkolom
    source = 'urpd_formula' — dihitung sendiri dari URPD, bukan angka resmi ChartInspect.
    Keduanya ditampilkan apa adanya (keputusan user 18 Sep 2026): tidak diisi, tidak dibuang.
    """
    df = pd.read_csv("data_median_mvrv.csv")
    df.rename(columns={
        'date': 'Date',
        'median_mvrv': 'Median MVRV',
        'median_realized_price': 'Median RP',
    }, inplace=True)
    return _prepare(df)[['Date', 'Median MVRV', 'Median RP']]


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
        'true_market_mean_price': 'True Market Mean',
    }, inplace=True)
    df = _prepare(df)

    aviv = _prepare(pd.read_csv("data_aviv.csv").rename(columns={'date': 'Date'}))
    aviv = aviv[['Date', 'btc_price', 'aviv_ratio', 'aviv_mean', 'aviv_upper_1sd']]
    dasar = aviv['btc_price'] / aviv['aviv_ratio']
    aviv['AVIV Mean'] = dasar * aviv['aviv_mean']
    aviv['AVIV Upper'] = dasar * (aviv['aviv_mean'] + 0.5 * (aviv['aviv_upper_1sd'] - aviv['aviv_mean']))
    aviv.loc[aviv['Date'] < _aviv_awal(aviv), ['AVIV Mean', 'AVIV Upper']] = float('nan')
    # Rasio untuk pane bawah. CVDD bernilai 0 sampai 16 Jul 2010: rasionya dikosongkan.
    df['Price / CVDD'] = df['BTC Price'] / df['CVDD'].where(df['CVDD'] > 0)
    df['Price / RP'] = df['BTC Price'] / df['RP'].where(df['RP'] > 0)
    df = df.merge(aviv[['Date', 'AVIV Mean', 'AVIV Upper']], on='Date', how='left')
    return df.merge(_median_mvrv()[['Date', 'Median RP']], on='Date', how='left')


def _aviv_awal(aviv):
    """Tanggal pertama AVIV layak ditampilkan.

    Rata-rata historis AVIV baru terbentuk dari segelintir hari di awal data: 84 hari
    pertama (17 Jul–9 Okt 2010) AVIV Mean jatuh sampai ±300x di bawah harga dan menarik
    sumbu Log ke 0.0002. Hari-hari sebelum rasio AVIV Mean/harga pertama kali wajar
    (0,2–5) disembunyikan; nilai sesudahnya tidak berubah.
    """
    mean_harga = aviv['btc_price'] / aviv['aviv_ratio'] * aviv['aviv_mean']
    wajar = (mean_harga / aviv['btc_price']).between(0.2, 5)
    return aviv.loc[wajar, 'Date'].iloc[0] if wajar.any() else aviv['Date'].min()


# Band umur HODL Waves: (akhiran kolom CSV, nama di legend), dari paling muda ke paling tua.
HODL_BANDS = [("0-1d", "24h"), ("1d-1w", "1d–1w"), ("1w-1m", "1w–1m"), ("1m-3m", "1m–3m"),
              ("3m-6m", "3m–6m"), ("6m-12m", "6m–12m"), ("1y-2y", "1y–2y"), ("2y-3y", "2y–3y"),
              ("3y-5y", "3y–5y"), ("5y-7y", "5y–7y"), ("7y-10y", "7y–10y"), ("10y+", "10y+")]


@st.cache_data(ttl=3600)
def load_hodl_waves():
    """RHODL Waves (porsi realized cap) dan HODL Waves (porsi supply) per band umur, dalam %.

    Kolom "RC <band>" dan "Supply <band>"; 12 band selalu berjumlah 100 (dicek 17 Sep 2026).
    Baris sebelum harga BTC pertama (2009 – 16 Jul 2010) dibuang, seperti halaman lain.
    """
    df = pd.read_csv("data_hodl_waves.csv").rename(columns={'date': 'Date', 'btc_price': 'BTC Price'})
    df = _prepare(df)
    df = df[df['Date'] >= df.loc[df['BTC Price'].notna(), 'Date'].min()]
    for akhiran, nama in HODL_BANDS:
        df[f"RC {nama}"] = df[f"realized_cap_{akhiran}"]
        df[f"Supply {nama}"] = df[f"supply_{akhiran}"]
    return df[['Date', 'BTC Price'] + [f"{u} {nama}" for _, nama in HODL_BANDS for u in ("RC", "Supply")]]


@st.cache_data(ttl=3600)
def load_rhodl_ratio():
    """RHODL Ratio versi analisa Cohort State Plane (research/analyze_cohort_state_plane.py).

    Realized cap (6m-12m + 1y-2y) / (1d-1w + 1w-1m + 1m-3m). BUKAN rhodl_ratio di data_rhodl.csv
    (1d-1w / 1y-2y). Cocok persis dengan research/findings/_cohort_state_plane.csv (dicek
    17 Sep 2026). 86% variansnya dari penyebut: angka tinggi bisa berarti modal segar hilang ATAU
    kohort lama menahan (memori rhodl-didominasi-penyebut) — jangan dibaca sendirian.
    """
    df = _prepare(pd.read_csv("data_hodl_waves.csv").rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    df = df[df['Date'] >= df.loc[df['BTC Price'].notna(), 'Date'].min()]
    rc = lambda band: df[f"realized_cap_{band}"]
    df['RHODL Ratio'] = (rc('6m-12m') + rc('1y-2y')) / (rc('1d-1w') + rc('1w-1m') + rc('1m-3m'))
    return df[['Date', 'BTC Price', 'RHODL Ratio']]


@st.cache_data(ttl=3600)
def load_aviv():
    """AVIV Ratio dan band simpangan bakunya dari data_aviv.csv (satuan rasio, bukan harga).

    Band dihitung dari mean dan +1σ, bukan dibaca dari kolom band lain: isinya identik
    (selisih < 1e-14) dan AVIV Upper framework v2 (+0,5σ) memang tidak ada di CSV.
    Rasio ≥ Upper persis sama dengan harga ≥ AVIV Upper di halaman Price Levels.
    """
    df = _prepare(pd.read_csv("data_aviv.csv").rename(columns={'date': 'Date'}))
    sd = df['aviv_upper_1sd'] - df['aviv_mean']
    df['BTC Price'] = df['btc_price']
    df['AVIV Ratio'] = df['aviv_ratio']
    df['AVIV Mean'] = df['aviv_mean']
    df['AVIV Upper'] = df['aviv_mean'] + 0.5 * sd
    df['AVIV +1σ'] = df['aviv_mean'] + sd
    df['AVIV +2σ'] = df['aviv_mean'] + 2 * sd
    # Band bawah negatif sampai Jun/Okt 2014 (σ awal sangat lebar): rasio tidak pernah
    # negatif, dan sumbu Log tidak bisa menggambarnya, jadi dikosongkan.
    df['AVIV −1σ'] = (df['aviv_mean'] - sd).where(lambda s: s > 0)
    df['AVIV −2σ'] = (df['aviv_mean'] - 2 * sd).where(lambda s: s > 0)
    # Jarak rasio dari mean dalam satuan σ: 0 = Mean, +0,5 = Upper.
    df['AVIV Deviation'] = (df['aviv_ratio'] - df['aviv_mean']) / sd
    kolom = ['AVIV Ratio', 'AVIV Mean', 'AVIV Upper', 'AVIV +1σ', 'AVIV +2σ',
             'AVIV −1σ', 'AVIV −2σ', 'AVIV Deviation']
    df.loc[df['Date'] < _aviv_awal(df), kolom] = float('nan')
    return df[['Date', 'BTC Price'] + kolom]


@st.cache_data(ttl=3600)
def load_sopr():
    """aSOPR, STH-SOPR, LTH-SOPR dari data_momentum.csv, plus gap STH-SOPR.

    Gap memakai rumus KB SOPR v1.4 §12: SMA90 STH-SOPR dikurangi SMA60 dari SMA90 itu
    (double-smoothed). Rumus ini yang mereproduksi angka KB persis (+0.02447 10 Jan 2021,
    cross turun 28 Mar 2021 dan 30 Nov 2021). Catatan: alerts/alert_check.py menghitung
    SMA60 − SMA90, hasilnya berbeda — dilaporkan ke user 13 Sep 2026, belum diputuskan.
    NUPL di file yang sama dimuat terpisah oleh load_nupl (halaman sendiri).
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
def load_nupl():
    """NUPL, STH-NUPL, LTH-NUPL dari data_momentum.csv, plus gap LTH − STH.

    Gap = LTH-NUPL − STH-NUPL (KB NUPL v1.4 §8.1), tanpa smoothing. Ratio LTH/STH (§8.2)
    sengaja tidak dimuat: melompat tanpa makna saat STH mendekati nol (+73 ke −561 sehari).
    """
    df = pd.read_csv("data_momentum.csv")
    df.rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'nupl': 'NUPL', 'sth_nupl': 'STH-NUPL', 'lth_nupl': 'LTH-NUPL',
    }, inplace=True)
    df = _prepare(df)
    df['NUPL Gap'] = df['LTH-NUPL'] - df['STH-NUPL']
    return df


@st.cache_data(ttl=3600)
def load_derivatives():
    """Funding rate dan open interest futures (data_derivatives.csv), plus perubahan OI harian.

    Satuan funding rate tidak disebut ChartInspect (median 0.0062, kemungkinan % per 8 jam),
    jadi ditampilkan tanpa satuan. Open interest = total_oi API futures-open-interest, persis
    jumlah kolom 13 bursa (dicek 16 Sep 2026, selisih 0). Satuannya tidak ditulis API; dari
    besarnya BTC (CME 107.248 x harga = 8,2 miliar USD). Cakupan bursa bertambah: CME mulai
    5 Jun 2020, Bitget 13 Agt 2021, Coinbase 2 Des 2023, Hyperliquid 25 Des 2024, MEXC
    21 Mar 2025 — di hari itu total OI melompat karena bursa baru masuk.
    OI tersedia sejak 28 Feb 2020, harga dan funding baru sejak 31 Mar 2020: baris sebelum
    harga pertama dibuang supaya chart dan slider mulai di tanggal yang sama.
    OI Change (disetujui user 16 Sep 2026) = jumlah perubahan OI per bursa, hanya bursa yang
    OI-nya > 0 di baris ini dan baris sebelumnya: hari bursa masuk cakupan (atau sehari
    bernilai 0 lalu kembali) tidak ikut dihitung. Kolom oi_* ditambahkan ke CSV oleh
    auto_update.py 16 Sep 2026; kalau belum ada, dipakai selisih total_oi biasa.
    Di 7 tanggal bolong selisihnya mencakup lebih dari satu hari.
    """
    df = pd.read_csv("data_derivatives.csv")
    df.rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'funding_rate': 'Funding Rate', 'total_oi': 'Open Interest',
    }, inplace=True)
    df = _prepare(df)
    bursa = [c for c in df.columns if c.startswith('oi_')]
    if bursa:
        oi = df[bursa]
        aktif = (oi > 0) & (oi.shift(1) > 0)
        df['OI Change'] = oi.diff().where(aktif).sum(axis=1, min_count=1)
        df.loc[df.index[0], 'OI Change'] = float('nan')
    else:
        df['OI Change'] = df['Open Interest'].diff()
    # Versi USD (16 Sep 2026): BTC x harga BTC hari itu (API OI tidak mengirim USD).
    df['Open Interest USD'] = df['Open Interest'] * df['BTC Price']
    df['OI Change USD'] = df['OI Change'] * df['BTC Price']
    awal = df.loc[df['BTC Price'].notna(), 'Date']
    if not awal.empty:
        df = df[df['Date'] >= awal.iloc[0]]
    return df


@st.cache_data(ttl=3600)
def load_exchange():
    """Saldo BTC di bursa dan arus masuk/keluar harian (data_exchange.csv).

    net_flow positif = BTC masuk bursa (data_dictionary). Selisih saldo harian sama dengan
    net_flow (dicek 17 Sep 2026). Disetujui user 17 Sep 2026 dari pratinjau:
    - Harga BTC dari data_mvrv.csv: btc_price di file ini beda sumber di 2026 (sampai 16 %).
    - Semua nilai sebelum 1 Jan 2012 dikosongkan: 2011 berisi pemindahan dompet bursa
      (+442k, −410k, +600k, −405k BTC sehari, saldo bolak-balik ke 0) yang menggepengkan sumbu.
    - Hari inflow = outflow = 0 sejak 2012 adalah data kosong yang diisi nol (8 hari, semuanya
      2026), jadi arusnya dikosongkan (celah di chart); saldo hari itu tetap.
    """
    df = _prepare(pd.read_csv("data_exchange.csv").rename(columns={
        'date': 'Date', 'total_balance': 'Exchange Balance',
        'net_flow': 'Net Flow', 'inflow': 'Inflow', 'outflow': 'Outflow'}))
    kolom = ['Exchange Balance', 'Net Flow', 'Inflow', 'Outflow']
    df.loc[df['Date'] < pd.Timestamp('2012-01-01'), kolom] = float('nan')
    kosong = (df['Inflow'] == 0) & (df['Outflow'] == 0)
    df.loc[kosong, ['Net Flow', 'Inflow', 'Outflow']] = float('nan')
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    df = df[['Date'] + kolom].merge(harga, on='Date', how='left')
    return df[df['Date'] >= df.loc[df['BTC Price'].notna(), 'Date'].min()]


@st.cache_data(ttl=3600)
def load_cdd():
    """Coin Days Destroyed dan rasio VDD 30d / 365d (data_cdd.csv).

    Dicek 24 Sep 2026: vdd_30d_ma dan vdd_365d_ma = rata-rata VDD harian persis, VDD harian
    ~ CDD x harga, vdd_multiple = VDD harian / vdd_365d_ma (tidak dipakai: terlalu ramai).
    Sesudah 2011 tanpa hari bolong, nol, atau nilai macet. Nol (2009-2010) dikosongkan
    supaya sumbu Log tidak rusak. Harga BTC dari data_mvrv.csv (file ini tanpa harga).
    """
    df = _prepare(pd.read_csv("data_cdd.csv").rename(columns={'date': 'Date', 'cdd': 'CDD'}))
    df['VDD Ratio'] = df['vdd_30d_ma'] / df['vdd_365d_ma']
    df = df[['Date', 'VDD Ratio', 'CDD']].replace(0, float('nan'))
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    df = df.merge(harga, on='Date', how='left')
    return df[df['Date'] >= df.loc[df['BTC Price'].notna(), 'Date'].min()]


@st.cache_data(ttl=3600)
def load_etf():
    """Total BTC yang dipegang ETF (data_etf.csv, Pipeline 29) dan net flow 1/7/14/30 hari.

    Flow dari kolom net_flow (sejak 2025 = flow harian ETF spot AS versi Farside, dicek ke berita
    24 Sep 2026), bukan dari selisih saldo: saldo levelnya kira-kira benar, tapi perubahan hariannya
    sering telat 1 hari dan meloncat. Halaman mulai 11 Jan 2024 (ETF spot AS; pilihan user 24 Sep
    2026): sebelumnya flow = turunan saldo, termasuk +241 ribu BTC Agu 2019, dan isi saldonya belum
    jelas. CSV tetap menyimpan sejak Nov 2018. 7/14/30 hari = jumlah flow per hari kalender.
    """
    df = _prepare(pd.read_csv("data_etf.csv", usecols=['date', 'total_balance', 'net_flow'])
                  .rename(columns={'date': 'Date', 'total_balance': 'ETF Holdings'}))
    flow = df.set_index('Date')['net_flow'].asfreq('D').fillna(0).loc['2024-01-11':]
    for n in (1, 7, 14, 30):
        df[f'ETF {n}d Flow'] = df['Date'].map(flow.rolling(n).sum())
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    df = df.drop(columns='net_flow').merge(harga, on='Date', how='left')
    return df[df['Date'] >= '2024-01-11']


@st.cache_data(ttl=3600)
def load_fear_greed():
    """Crypto Fear & Greed Index (data_fg.csv; sumber Alternative.me lewat ChartInspect).

    CSV tidak menyimpan harga BTC; harga diambil dari data_mvrv.csv (identik dengan
    bitcoinPrice di API F&G, dicek 16 Sep 2026). Data mulai 1 Feb 2018, 2 tanggal bolong.
    """
    df = pd.read_csv("data_fg.csv").rename(columns={'date': 'Date'})
    df = _prepare(df)
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    return df.merge(harga, on='Date', how='left')


@st.cache_data(ttl=3600)
def load_btc_tradfi(window=365):
    """Z-Score log(BTC / pembanding) untuk S&P 500 dan emas, jendela `window` hari.

    Jendela dipilih di kotak Window halaman (bawaan 365 hari). Sama dengan
    research/analyze_btc_spx_zscore.py: Z = (log rasio - SMA jendela) / SD jendela,
    jendela dalam hari kalender BTC. data_tradfi.csv hanya berisi hari bursa;
    akhir pekan dan libur diisi harga penutupan terakhir (ffill) sebelum rasio dihitung.
    Hasil riset (21 Sep 2026): Z rendah bukan sinyal beli yang berdiri sendiri — jendela
    1 tahun tanpa divergence diikuti penurunan median -39 %. Bukan bagian framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    tradfi = _prepare(pd.read_csv("data_tradfi.csv", usecols=['date', 'spx', 'xau'])
                      .rename(columns={'date': 'Date'}))
    df = harga.merge(tradfi, on='Date', how='left')
    df = df[df['Date'] >= tradfi['Date'].min()].copy()
    for kolom, nama in (("spx", "S&P 500"), ("xau", "Gold")):
        pembanding = df[kolom].ffill()
        rasio = np.log(df['BTC Price'] / pembanding)
        jendela = rasio.rolling(int(window))
        df[f'{nama} Z'] = (rasio - jendela.mean()) / jendela.std()
    return df.drop(columns=["spx", "xau"])


@st.cache_data(ttl=3600)
def load_vix():
    """VIX (data_vix.csv, Pipeline 24 dari file resmi Cboe) + harga BTC dari data_mvrv.csv.

    Hanya hari hitung Cboe; akhir pekan kosong (tidak di-ffill), garis menyambung
    Jumat ke Senin. Sejak Mei 2022 Cboe juga memuat sebagian hari libur bursa AS; dibiarkan.
    Cek data 21 Sep 2026: tanpa 0/macet/celah > 5 hari; lonjakan > 40 % semuanya kejadian
    pasar asli (maks 82,69 pada 16 Mar 2020). Bukan bagian framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    vix = _prepare(pd.read_csv("data_vix.csv").rename(columns={'date': 'Date', 'vix': 'VIX'}))
    return harga.merge(vix, on='Date', how='left')


@st.cache_data(ttl=3600)
def load_dxy():
    """US Dollar Index (kolom dxy di data_tradfi.csv, Pipeline 23 dari Yahoo DX-Y.NYB) + harga BTC.

    Hanya hari bursa ICE; akhir pekan dan libur kosong (tidak di-ffill). Cek data 22 Sep 2026:
    tanpa 0/macet, celah terpanjang 5 hari (badai Sandy, Okt 2012). Dibandingkan dengan DXY yang
    dihitung dari rumus resmi ICE + kurs FRED H.10 (jam 12 siang NY): median selisih 0,08 %,
    tanpa bias, korelasi perubahan mingguan 0,98. Bukan bagian framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    dxy = _prepare(pd.read_csv("data_tradfi.csv", usecols=['date', 'dxy'])
                   .rename(columns={'date': 'Date', 'dxy': 'DXY'}).dropna())
    return harga.merge(dxy, on='Date', how='left')


@st.cache_data(ttl=3600)
def load_ssr():
    """Stablecoin Supply Ratio = market cap BTC / total supply stablecoin (USD), sejak 2018.

    Market cap = harga (data_mvrv.csv) x supply BTC (LTH + STH, data_supply.csv). Supply stablecoin
    dari data_stablecoin_supply.csv (Pipeline 27): s/d 15 Feb 2021 dari blockchain (USDT = supply
    on-chain dikurangi kas Tether, lihat research/stablecoin_ratios/build_stablecoin_history.py), sesudahnya DefiLlama.
    Cek 23 Sep 2026: USDT versi blockchain vs CMC median 2-4 %/tahun (CMC telat update); ~62 juta
    (2-3 %) di 2018-2019 belum terjelaskan -> SSR 2018-2019 bisa terlalu rendah sampai ~3 %.
    Keranjang stablecoin beda dengan Glassnode: baca pakai persentil sendiri. Bukan framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    sup = _prepare(pd.read_csv("data_supply.csv", usecols=['date', 'lth_supply_btc', 'sth_supply_btc'])
                   .rename(columns={'date': 'Date'}))
    stable = _prepare(pd.read_csv("data_stablecoin_supply.csv", usecols=['date', 'stablecoin_supply_usd'])
                      .rename(columns={'date': 'Date'}))
    df = harga.merge(sup, on='Date', how='left').merge(stable, on='Date', how='left')
    df['SSR'] = (df['BTC Price'] * (df['lth_supply_btc'] + df['sth_supply_btc'])
                 / df['stablecoin_supply_usd'])
    return df.loc[df['Date'] >= '2018-01-01', ['Date', 'BTC Price', 'SSR']]


@st.cache_data(ttl=3600)
def load_exchange_ratio():
    """Exchange Stablecoin Ratio = cadangan BTC di bursa (USD) / cadangan stablecoin di bursa (USD).

    Pipeline 28 (data_exchange_reserves.csv): DefiLlama CEX Transparency, 19 bursa tetap, sejak 2023,
    stablecoin Binance dikurangi dompet jaminan Binance-Peg. Dicek terhadap PoR Binance 1 Sep 2026: BTC
    asli +0,1 %; stablecoin cocok sesudah koreksi kecuali USDT/USDC Binance di BNB Chain (±2,4 miliar)
    yang tidak ada di DefiLlama. TIDAK mencakup Coinbase/Upbit/Bithumb dkk. (±1/3 BTC di bursa saja),
    jadi level tidak sebanding dengan CryptoQuant; dipakai untuk membedah bentuk. Bukan framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    r = _prepare(pd.read_csv("data_exchange_reserves.csv",
                             usecols=['date', 'btc_reserve_usd', 'stable_reserve_usd'])
                 .rename(columns={'date': 'Date', 'btc_reserve_usd': 'BTC Reserve',
                                  'stable_reserve_usd': 'Stablecoin Reserve'}))
    r['Exchange Ratio'] = r['BTC Reserve'] / r['Stablecoin Reserve']
    df = harga.merge(r, on='Date', how='left')
    return df[df['Date'] >= r['Date'].min()]


@st.cache_data(ttl=3600)
def load_yields():
    """US Treasury yield 2Y & 10Y (data_yields.csv, Pipeline 25 dari FRED) + spread 10Y - 2Y.

    Hanya hari pasar obligasi AS; akhir pekan dan libur kosong (tidak di-ffill). Harga BTC dari
    data_mvrv.csv. Cek data 21 Sep 2026: tanpa nilai <= 0; nilai sama >= 5 hari (28 kali) hanya
    di masa suku bunga ~0 % (2011-2013, 2020-2021) = pasar diam, bukan data macet.
    Bukan bagian framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    y = _prepare(pd.read_csv("data_yields.csv").rename(
        columns={'date': 'Date', 'us2y': 'US 2Y', 'us10y': 'US 10Y'}))
    y['10Y-2Y'] = y['US 10Y'] - y['US 2Y']
    return harga.merge(y, on='Date', how='left')


@st.cache_data(ttl=3600)
def load_futures_basis():
    """BTC 3M annualized futures basis vs US 2Y yield (+ selisihnya) dan harga BTC.

    Basis dari data_futures_basis_3m.csv (Pipeline 26: Binance COIN-M + Deribit, tenor tetap
    90 hari, mulai Jun 2020). 2Y dari data_yields.csv; akhir pekan/libur diisi nilai terakhir
    (ffill) supaya selisih harian ada. Cek data 22 Sep 2026: tanpa tanggal bolong; lonjakan
    besar (2021, 11 Mar 2023 -4,7 %) dikonfirmasi kedua bursa; 3 Sep 2020 kedua bursa
    berlawanan tanda (penyebab belum dicek). Bukan bagian framework v2.
    """
    harga = _prepare(pd.read_csv("data_mvrv.csv", usecols=['date', 'btc_price'])
                     .rename(columns={'date': 'Date', 'btc_price': 'BTC Price'}))
    basis = _prepare(pd.read_csv("data_futures_basis_3m.csv", usecols=['date', 'basis_3m'])
                     .rename(columns={'date': 'Date', 'basis_3m': 'Basis 3M'}))
    y2 = _prepare(pd.read_csv("data_yields.csv", usecols=['date', 'us2y'])
                  .rename(columns={'date': 'Date', 'us2y': 'US 2Y'}))
    df = harga.merge(basis, on='Date', how='left').merge(y2, on='Date', how='left')
    df = df[df['Date'] >= basis['Date'].min()].copy()
    df['US 2Y'] = df['US 2Y'].ffill()
    df['Basis - 2Y'] = df['Basis 3M'] - df['US 2Y']
    return df


# Band umur yang dihitung sebagai LTH (batas kohort 155 hari jatuh di dalam band 3m-6m;
# band itu dimasukkan ke STH supaya tidak dipotong sembarangan).
LTH_BANDS = ("6m-12m", "1y-2y", "2y-3y", "3y-5y", "5y-7y", "7y-10y", "10y+")


@st.cache_data(ttl=3600)
def load_unrealized_pl():
    """Unrealized profit dan loss per kohort, dihitung sendiri dari band umur.

    Tiap band HODL Waves punya nilai pasar (porsi supply x market cap) dan nilai beli
    (porsi realized cap x realized cap). Selisihnya masuk sisi untung atau sisi rugi, lalu
    dijumlahkan per kohort dan dibagi market cap — satuannya sama dengan "relative unrealized
    profit/loss" ChartInspect.

    Kenapa dihitung sendiri (keputusan user 18 Sep 2026): endpoint
    relative-unrealized-pl-by-cohort (data_relative_unrealized_pl_by_cohort.csv, pipeline 20
    auto_update.py) tidak bisa direkonsiliasi dengan realized cap ChartInspect sendiri — sisi
    ruginya jauh lebih besar (LTH 0,501 vs 0,156 pada 18 Agt 2026) sementara sisi untungnya sama,
    sehingga NUPL-nya berlawanan tanda dengan halaman NUPL. Versi ini selalu konsisten: untung −
    rugi = NUPL dari MVRV persis (dicek seluruh 5.900 hari), dan datanya tidak tertinggal 30 hari.

    Batas metode: rincian hanya sampai 12 band, jadi koin rugi di dalam band yang rata-rata untung
    tidak terhitung. Kedua sisi mengecil dalam jumlah yang sama; nilai bersihnya tetap tepat.
    """
    h = _prepare(pd.read_csv("data_hodl_waves.csv").rename(columns={'date': 'Date'}))
    rc = _prepare(pd.read_csv("data_realized_cap.csv").rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price', 'realized_cap_usd': 'Realized Cap'}))
    sp = _prepare(pd.read_csv("data_supply.csv").rename(columns={'date': 'Date'}))
    df = (h.merge(rc[['Date', 'BTC Price', 'Realized Cap']], on='Date')
           .merge(sp[['Date', 'lth_supply_btc', 'sth_supply_btc']], on='Date'))
    market = (df['lth_supply_btc'] + df['sth_supply_btc']) * df['BTC Price']
    nol = market * 0
    hasil = {(kohort, sisi): nol.copy() for kohort in ('LTH', 'STH')
             for sisi in ('Unrealized Profit', 'Unrealized Loss')}
    for akhiran, _ in HODL_BANDS:
        selisih = (df[f"supply_{akhiran}"] / 100 * market
                   - df[f"realized_cap_{akhiran}"] / 100 * df['Realized Cap'])
        kohort = 'LTH' if akhiran in LTH_BANDS else 'STH'
        hasil[(kohort, 'Unrealized Profit')] += selisih.clip(lower=0)
        hasil[(kohort, 'Unrealized Loss')] += (-selisih).clip(lower=0)
    for (kohort, sisi), nilai in hasil.items():
        df[f"{kohort} {sisi}"] = nilai / market
    kolom = [f"{k} {s}" for k in ('LTH', 'STH')
             for s in ('Unrealized Profit', 'Unrealized Loss')]
    return df[['Date', 'BTC Price'] + kolom]


@st.cache_data(ttl=3600)
def load_realized_cap():
    """Realized cap total, LTH, STH (data_realized_cap.csv, USD), persen per kohort, dan
    perubahan realized cap total 30 hari kalender (%).

    LTH + STH = total (selisih <= 0,01 %, dicek 17 Sep 2026). Harga BTC di file ini identik
    dengan data_mvrv.csv. Lonjakan LTH +7,2 % 26 Apr 2026 wajar (koin 22 Nov 2025 genap 155 hari).
    Perubahan 30 hari 2011-2013 sangat besar (sampai +413 %) karena modal masih kecil; sengaja
    tidak dikosongkan (keputusan user 17 Sep 2026: cukup di-zoom).
    """
    df = _prepare(pd.read_csv("data_realized_cap.csv").rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price', 'realized_cap_usd': 'Realized Cap',
        'lth_realized_cap_usd': 'LTH Realized Cap', 'sth_realized_cap_usd': 'STH Realized Cap'}))
    total = df['Realized Cap'].where(df['Realized Cap'] > 0)
    df['LTH Realized Cap %'] = df['LTH Realized Cap'] / total * 100
    df['STH Realized Cap %'] = df['STH Realized Cap'] / total * 100
    rc = df.set_index('Date')['Realized Cap']
    df['Realized Cap 30d Change'] = ((rc / rc.shift(freq='30D').reindex(rc.index) - 1) * 100).to_numpy()
    return df[['Date', 'BTC Price', 'Realized Cap', 'LTH Realized Cap', 'STH Realized Cap',
               'LTH Realized Cap %', 'STH Realized Cap %', 'Realized Cap 30d Change']]


@st.cache_data(ttl=3600)
def load_holder_supply():
    """Jumlah supply LTH dan STH (data_supply.csv), dalam BTC dan persen supply beredar.

    LTH + STH = seluruh supply beredar (20,09 juta BTC 17 Sep 2026, cocok jadwal halving).
    Tidak entity-adjusted: koin lama yang pindah dompet (bursa/kustodian) pindah ke STH lalu
    kembali ke LTH 155 hari kemudian — mis. −536k BTC 22 Nov 2025 dan +598k 26 Apr 2026.
    Persen dihitung di sini karena CSV hanya menyimpan BTC.
    """
    df = _prepare(pd.read_csv("data_supply.csv").rename(columns={
        'date': 'Date', 'btc_price': 'BTC Price',
        'lth_supply_btc': 'LTH Supply', 'sth_supply_btc': 'STH Supply'}))
    total = (df['LTH Supply'] + df['STH Supply']).where(lambda s: s > 0)
    df['LTH Supply %'] = df['LTH Supply'] / total * 100
    df['STH Supply %'] = df['STH Supply'] / total * 100
    # Perubahan saldo LTH 30 hari kalender (bukan 30 baris), dalam BTC.
    lth = df.set_index('Date')['LTH Supply']
    df['LTH 30d Change'] = (lth - lth.shift(freq='30D').reindex(lth.index)).to_numpy()
    return df[['Date', 'BTC Price', 'LTH Supply', 'STH Supply', 'LTH Supply %', 'STH Supply %',
               'LTH 30d Change']]


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
