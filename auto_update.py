import requests
import pandas as pd
from datetime import datetime
import numpy as np
import os

print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 🚀 Memulai proses automasi On-Chain Data...")
print("="*60)

def fetch_data(url, columns_to_keep=None):
    try:
        res = requests.get(url)
        data = res.json().get('data', [])
        df = pd.DataFrame(data)
        
        if not df.empty:
            # 🟢 ROOT CAUSE FIX: Sanitasi format tanggal secara mutlak di hulu
            if 'date' in df.columns:
                # Paksa standarisasi timezone ke UTC, lalu potong murni menjadi string YYYY-MM-DD
                df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
            
            if columns_to_keep:
                df = df[[col for col in columns_to_keep if col in df.columns]]
                
            # Bersihkan anomali duplikasi internal sejak dari sumbernya
            if 'date' in df.columns:
                df = df.dropna(subset=['date']).drop_duplicates(subset=['date'], keep='last')
                
        return df
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return pd.DataFrame()


def simpan(df, file, kolom_log=None):
    """Urutkan menurut tanggal, tulis CSV, cetak 3 baris terakhir. Mengembalikan df terurut."""
    df = df.sort_values('date').reset_index(drop=True)
    df.to_csv(file, index=False)
    print(f"✅ {file} berhasil diperbarui.")
    print((df[kolom_log] if kolom_log else df).tail(3).to_string(index=False))
    return df

# ==========================================
# 1. PIPELINE: PRICE LEVELS & MOVING AVERAGES
# ==========================================
print("\n[1] Menarik data Price Levels...")
# 🟢 FIX: Tambahkan 'active_realized_price' dan 'mvrv_avg_price' ke dalam whitelist kolom hulu (akan di-rename ke 'MVRV 0σ' sebelum disimpan)
df_price = fetch_data("https://chartinspect.com/api/onchain/onchain-price-levels?timeframe=all&isProUser=false", 
                      ['date', 'btc_price', 'sth_cost_basis', 'lth_cost_basis', 'realized_price', 'cvdd', 'active_realized_price', 'mvrv_avg_price'])
df_tmm = fetch_data("https://chartinspect.com/api/onchain/true-market-mean?timeframe=all&isProUser=false", ['date', 'true_market_mean_price'])

if not df_price.empty and not df_tmm.empty:
    df_master_price = pd.merge(df_price, df_tmm, on='date', how='outer')
    df_master_price = df_master_price.sort_values('date').reset_index(drop=True)
    
    # Kalkulasi Moving Averages
    df_master_price['200_dma'] = df_master_price['btc_price'].rolling(window=200, min_periods=1).mean()
    df_master_price['50_wma'] = df_master_price['btc_price'].rolling(window=350, min_periods=1).mean()
    df_master_price['200_wma'] = df_master_price['btc_price'].rolling(window=1400, min_periods=1).mean()

    # Rename kolom API ke nama display sebelum disimpan ke CSV
    df_master_price.rename(columns={'mvrv_avg_price': 'MVRV 0σ'}, inplace=True)

    simpan(df_master_price, "data_price_level.csv")

# ==========================================
# 2. PIPELINE: MOMENTUM & P/L
# ==========================================
print("\n[2] Menarik data Momentum & P/L...")
df_sopr = fetch_data("https://chartinspect.com/api/onchain/sopr?timeframe=all&isProUser=false", ['date', 'btc_price', 'asopr'])
df_lth_sopr = fetch_data("https://chartinspect.com/api/onchain/lth-sopr?timeframe=all&isProUser=false", ['date', 'lth_sopr'])
df_sth_sopr = fetch_data("https://chartinspect.com/api/onchain/sth-sopr?timeframe=all&isProUser=false", ['date', 'sth_sopr'])
df_net_pl = fetch_data("https://chartinspect.com/api/onchain/net-realized-pl?timeframe=all&isProUser=false", ['date', 'net_realized_pl_usd'])
df_age = fetch_data("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
df_nupl = fetch_data("https://chartinspect.com/api/onchain/nupl?timeframe=all&isProUser=false", ['date', 'nupl', 'sth_nupl', 'lth_nupl'])

if not df_age.empty:
    # STH: Age bands 0-2 (range(3) = 0, 1, 2)
    sth_prof = df_age[[f'band_{i}_profit_usd' for i in range(3)]].sum(axis=1)
    sth_loss = df_age[[f'band_{i}_loss_usd' for i in range(3)]].sum(axis=1)
    df_age['sth_pl_ratio'] = (sth_prof / sth_loss).replace([np.inf, -np.inf], np.nan).ffill().fillna(1.0)

    # LTH: Age bands 3-10 sesuai standar dokumentasi (range(3, 11))
    lth_prof = df_age[[f'band_{i}_profit_usd' for i in range(3, 11)]].sum(axis=1)
    lth_loss = df_age[[f'band_{i}_loss_usd' for i in range(3, 11)]].sum(axis=1)
    df_age['lth_pl_ratio'] = (lth_prof / lth_loss).replace([np.inf, -np.inf], np.nan).ffill().fillna(1.0)
    
    df_age_pl = df_age[['date', 'sth_pl_ratio', 'lth_pl_ratio']]
else:
    df_age_pl = pd.DataFrame(columns=['date', 'sth_pl_ratio', 'lth_pl_ratio'])

dfs = [df_sopr, df_lth_sopr, df_sth_sopr, df_net_pl, df_nupl]
df_master_mom = dfs[0]
for d in dfs[1:]:
    if not d.empty:
        df_master_mom = pd.merge(df_master_mom, d, on='date', how='outer')

if not df_master_mom.empty:
    simpan(df_master_mom, "data_momentum.csv", ['date', 'btc_price', 'asopr', 'net_realized_pl_usd'])

# ==========================================
# 3. PIPELINE: DERIVATIVES
# ==========================================
print("\n[3] Menarik data Derivatives...")
# Kolom OI per bursa dari API futures-open-interest (satuan BTC). Disimpan supaya
# perubahan OI bisa dihitung tanpa lompatan saat bursa baru masuk cakupan.
OI_EXCHANGES = ['cme', 'binance', 'bybit', 'hyperliquid', 'bitget', 'okx', 'deribit',
                'coinbase', 'bitmex', 'kraken', 'bitfinex', 'mexc', 'huobi']

df_funding = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-funding-rates?timeframe=all", ['date', 'btc_price', 'funding_rate'])
df_oi = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-open-interest?timeframe=all", ['date', 'total_oi'] + OI_EXCHANGES)

if not df_funding.empty and not df_oi.empty:
    df_oi_clean = df_oi.rename(columns={ex: f'oi_{ex}' for ex in OI_EXCHANGES})
    simpan(pd.merge(df_funding, df_oi_clean, on='date', how='outer'), "data_derivatives.csv")

# ==========================================
# 4. PIPELINE: SOCIAL SENTIMENT
# ==========================================
print("\n[4] Menarik data Social Sentiment...")
df_gtrend = fetch_data("https://chartinspect.com/api/charts/onchain/google-trends?timeframe=all&isProUser=false", 
                       ['date', 'btc_price', 'trend_bitcoin', 'trend_crypto', 'trend_ethereum', 'trend_nft'])
df_wiki = fetch_data("https://chartinspect.com/api/charts/onchain/wikipedia-pageviews?timeframe=all&isProUser=false", 
                     ['date', 'wiki_bitcoin', 'wiki_cryptocurrency', 'wiki_ethereum', 'wiki_blockchain'])

if not df_gtrend.empty and not df_wiki.empty:
    simpan(pd.merge(df_gtrend, df_wiki, on='date', how='outer'), "data_sentiment.csv",
           ['date', 'trend_bitcoin', 'wiki_bitcoin'])

# ==========================================
# 5. PIPELINE: SUPPLY DYNAMICS
# ==========================================
print("\n[5] Menarik data Supply Dynamics...")
df_sth_lth = fetch_data("https://chartinspect.com/api/onchain/sth-lth?timeframe=all&isProUser=false", 
                       ['date', 'btc_price', 'lth_supply_btc', 'sth_supply_btc', 'pct_lth_in_profit', 'pct_sth_in_profit', 'pct_lth_in_loss', 'pct_sth_in_loss'])
df_profit_loss = fetch_data("https://chartinspect.com/api/onchain/profit-loss?timeframe=all&isProUser=false", 
                            ['date', 'percent_btc_in_profit', 'percent_btc_in_loss'])

if not df_sth_lth.empty and not df_profit_loss.empty:
    simpan(pd.merge(df_sth_lth, df_profit_loss, on='date', how='outer'), "data_supply.csv",
           ['date', 'lth_supply_btc', 'sth_supply_btc'])

# ==========================================
# 6. PIPELINE: MARKET VALUATION
# ==========================================
print("\n[6] Menarik data Market Valuation...")
df_mvrv = fetch_data("https://chartinspect.com/api/onchain/mvrv?timeframe=all&isProUser=false",
                     ['date', 'btc_price', 'mvrv', 'sth_mvrv', 'lth_mvrv'])
df_mvrv_z = fetch_data("https://chartinspect.com/api/onchain/mvrv-z-score?timeframe=all&isProUser=false",
                       ['date', 'mvrv_zscore'])

if not df_mvrv.empty:
    df_mvrv.rename(columns={'mvrv': 'mvrv_ratio'}, inplace=True)
    if not df_mvrv_z.empty:
        df_mvrv = pd.merge(df_mvrv, df_mvrv_z, on='date', how='left')
    simpan(df_mvrv, "data_mvrv.csv")
    
# ==========================================
# 7. PIPELINE: FEAR & GREED
# ==========================================
print("\n[7] Menarik data Fear & Greed...")
df_fg = fetch_data("https://chartinspect.com/api/charts/crypto/fear-greed-index?timeframe=all&isProUser=false")
if not df_fg.empty:
    df_fg['date'] = pd.to_datetime(df_fg['timestamp'], unit='s').dt.strftime('%Y-%m-%d')
    df_fg.rename(columns={'value': 'Fear & Greed'}, inplace=True)
    simpan(df_fg[['date', 'Fear & Greed']], "data_fg.csv")

# ==========================================
# 8. PIPELINE: EXCHANGE FLOWS
# ==========================================
print("\n[8] Menarik data Exchange Flow...")
df_ex = fetch_data("https://chartinspect.com/api/charts/exchange-etf/exchange-flows?timeframe=all", 
                   ['date', 'btc_price', 'total_balance', 'net_flow', 'inflow', 'outflow'])
if not df_ex.empty:
    simpan(df_ex, "data_exchange.csv", ['date', 'total_balance', 'net_flow'])

# ==========================================
# 9. PIPELINE: CUMULATIVE P/L PRICE & RATIO
# ==========================================
print("\n[9] Mengkalkulasi Cumulative P/L Price...")
try:
    # Endpoint yang sama sudah ditarik di Pipeline 2 (df_age); cumsum butuh urutan tanggal.
    if not df_age.empty:
        df_age_raw = df_age.sort_values('date').reset_index(drop=True)
        
        # 🟢 FIX MUTLAK: LTH murni adalah 155+ Hari (Bands 5 sampai 11)
        lth_prof_raw = df_age_raw[[f'band_{i}_profit_usd' for i in range(5, 12)]].sum(axis=1)
        lth_loss_raw = df_age_raw[[f'band_{i}_loss_usd' for i in range(5, 12)]].sum(axis=1)
        
        df_cum = pd.DataFrame({'date': df_age_raw['date'], 'lth_net_pl_usd': lth_prof_raw - lth_loss_raw})
        
        # 🟢 FIX MUTLAK 2: CumSum HARUS dieksekusi SEBELUM merge agar data historis 2010 utuh
        df_cum['cum_net_pl'] = df_cum['lth_net_pl_usd'].cumsum()

        df_p = pd.read_csv("data_price_level.csv")
        df_s = pd.read_csv("data_supply.csv")
        df_p['date'] = pd.to_datetime(df_p['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        df_s['date'] = pd.to_datetime(df_s['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        df_cum = pd.merge(df_cum, df_p[['date', 'btc_price', 'realized_price', 'lth_cost_basis']], on='date', how='inner')
        df_cum = pd.merge(df_cum, df_s[['date', 'lth_supply_btc']], on='date', how='inner')
        df_cum = df_cum.sort_values('date').dropna(subset=['realized_price']).reset_index(drop=True)
        
        if not df_cum.empty:
            safe_supply = df_cum['lth_supply_btc'].replace(0, np.nan)

            df_cum['cum_pl_price'] = df_cum['realized_price'] + (df_cum['cum_net_pl'] / safe_supply)
            df_cum['pl_price_ratio'] = df_cum['btc_price'] / df_cum['cum_pl_price']
            
            df_cum_final = df_cum[['date', 'cum_pl_price', 'pl_price_ratio']]

            # 🟢 REKAP DATA MUTLAK: Amankan struktur file data_price_level.csv
            df_p_rekap = df_p

            cols_to_drop = [c for c in ['cum_pl_price', 'pl_price_ratio'] if c in df_p_rekap.columns]
            if cols_to_drop:
                df_p_rekap.drop(columns=cols_to_drop, inplace=True)
            
            df_p_rekap = pd.merge(df_p_rekap, df_cum_final, on='date', how='left')
            df_p_rekap.to_csv("data_price_level.csv", index=False)
            print("✅ cum_pl_price & pl_price_ratio berhasil dimerge ke data_price_level.csv.")
        else:
            print("❌ GAGAL: Data kosong setelah digabungkan (merge error).")
    else:
        print("❌ GAGAL: Endpoint API realized-profit-by-age tidak merespons.")
except Exception as e:
    print(f"❌ Error Sistem Pipeline 9: {e}")

# ==========================================
# 10. PIPELINE: RHODL RATIO
# ==========================================
print("\n[10] Menarik data RHODL Ratio...")
df_rhodl = fetch_data("https://chartinspect.com/api/onchain/rhodl?historical=true&timeframe=all&isProUser=false",
                      ['date', 'btc_price', 'rhodl_ratio', 'realized_cap_1w', 'realized_cap_1_2y'])
if not df_rhodl.empty:
    simpan(df_rhodl, "data_rhodl.csv", ['date', 'rhodl_ratio'])

# ==========================================
# 11. PIPELINE: HODL WAVES (SPECIAL PARSING)
# ==========================================
print("\n[11] Menarik data HODL Waves...")
try:
    url_hw = "https://chartinspect.com/api/onchain/hodl-waves?timeframe=all&waveType=standard&historical=true&resolution=auto&maxPoints=2000&isProUser=false"
    res_hw = requests.get(url_hw)
    raw_hw = res_hw.json().get('historical', []) 
    
    if raw_hw:
        rows_hw = []
        for item in raw_hw:
            dt_obj = pd.to_datetime(item['timestamp'], unit='ms')
            date_str = dt_obj.strftime('%Y-%m-%d')
            
            row = {'date': date_str, 'btc_price': item.get('btc_price')}
            for w in item.get('waves', []):
                bucket_name = w['age_bucket'] 
                row[f"supply_{bucket_name}"] = w['percentage_of_supply']
                row[f"realized_cap_{bucket_name}"] = w['percentage_of_realized_cap']
                
            rows_hw.append(row)
        
        df_hw = pd.DataFrame(rows_hw)
        df_hw = df_hw.dropna(subset=['date']).drop_duplicates(subset=['date'], keep='last')
        simpan(df_hw, "data_hodl_waves.csv", ['date', 'supply_1y-2y', 'realized_cap_1y-2y'])
    else:
        print("❌ GAGAL: Endpoint HODL Waves mengembalikan array kosong.")
except Exception as e:
    print(f"❌ Error fetching HODL Waves: {e}")

# ==========================================
# 12. PIPELINE: REALIZED CAP
# ==========================================
print("\n[12] Menarik data Realized Cap...")
try:
    url_rcap = "https://chartinspect.com/api/onchain/realized-cap?timeframe=all&isProUser=false"
    cols_rcap = ['date', 'btc_price', 'realized_cap_usd', 'lth_realized_cap_usd', 'sth_realized_cap_usd']
    df_rcap = fetch_data(url_rcap, cols_rcap)
    
    if not df_rcap.empty:
        simpan(df_rcap, "data_realized_cap.csv", ['date', 'realized_cap_usd'])
    else:
        print("❌ GAGAL: Data Realized Cap kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error fetching Realized Cap: {e}")

# ==========================================
# 13. PIPELINE: COIN DAYS DESTROYED (CDD)
# ==========================================
print("\n[13] Menarik data Coin Days Destroyed (CDD)...")
try:
    url_cdd = "https://chartinspect.com/api/onchain/cdd?timeframe=all&isProUser=false"
    cols_cdd = ['date', 'cdd', 'vdd_30d_ma', 'vdd_365d_ma', 'vdd_multiple']
    df_cdd = fetch_data(url_cdd, cols_cdd)
    
    if not df_cdd.empty:
        simpan(df_cdd, "data_cdd.csv", ['date', 'cdd', 'vdd_multiple'])
    else:
        print("❌ GAGAL: Data CDD kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error fetching CDD: {e}")

# ==========================================
# 14. PIPELINE: LTH P/L PRICE FLOW
# ==========================================
print("\n[14] Mengkalkulasi LTH P/L Price Flow...")
try:
    df_p = pd.read_csv("data_price_level.csv")
    df_p['date'] = pd.to_datetime(df_p['date'], errors='coerce').dt.strftime('%Y-%m-%d')
    
    df_flow = df_p[['date', 'cum_pl_price', 'btc_price']].dropna(subset=['cum_pl_price']).copy()
    df_flow = df_flow.sort_values('date').reset_index(drop=True)

    if not df_flow.empty:
        df_flow['lth_pl_price'] = df_flow['cum_pl_price']
        df_flow['delta_pl_price'] = df_flow['lth_pl_price'].diff().fillna(0)
        df_flow['lth_pl_flow_btc'] = df_flow['delta_pl_price'] / df_flow['btc_price']

        df_flow = df_flow.round(4)
        df_flow_clean = df_flow[['date', 'lth_pl_price', 'lth_pl_flow_btc']]
        df_flow_clean.to_csv("data_lth_flow.csv", index=False)
        print("✅ data_lth_flow.csv berhasil dibuat dan tersinkronisasi.")
except Exception as e:
    print(f"❌ Error kalkulasi LTH Flow: {e}")


# ==========================================
# 15. PIPELINE: REALIZED PROFIT/LOSS IN BTC + P/L RATIOS
# ==========================================
print("\n[15] Menarik data Realized Profit/Loss (BTC) + P/L Ratios...")
try:
    df_rpl = fetch_data(
        "https://chartinspect.com/api/onchain/realized-profit-loss?timeframe=all&isProUser=false",
        ['date', 'btc_price', 'daily_realized_profit_btc', 'daily_realized_loss_btc']
    )

    if not df_rpl.empty:
        df_rpl['rpl_ratio'] = (df_rpl['daily_realized_profit_btc'] / df_rpl['daily_realized_loss_btc']).replace([np.inf, -np.inf], np.nan)

        if not df_age_pl.empty:
            df_rpl = pd.merge(df_rpl, df_age_pl, on='date', how='outer')

        # Kalkulasi rrp, rrl, relative_realized_pl via realized cap
        if os.path.exists("data_realized_cap.csv"):
            df_rcap = pd.read_csv("data_realized_cap.csv")[['date', 'realized_cap_usd']]
            df_rcap['date'] = pd.to_datetime(df_rcap['date'], errors='coerce').dt.strftime('%Y-%m-%d')
            df_rpl = pd.merge(df_rpl, df_rcap, on='date', how='left')
            safe_rcap = df_rpl['realized_cap_usd'].replace(0, np.nan)
            df_rpl['rrp'] = (df_rpl['daily_realized_profit_btc'] * df_rpl['btc_price']) / safe_rcap
            df_rpl['rrl'] = (df_rpl['daily_realized_loss_btc']   * df_rpl['btc_price']) / safe_rcap
            df_rpl['relative_realized_pl'] = df_rpl['rrp'] - df_rpl['rrl']
            df_rpl.drop(columns=['realized_cap_usd'], inplace=True)

        df_rpl['date'] = pd.to_datetime(df_rpl['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        df_rpl = df_rpl.dropna(subset=['date']).drop_duplicates(subset=['date'], keep='last')
        df_rpl = df_rpl.sort_values('date').reset_index(drop=True)
        df_rpl.to_csv("data_pl.csv", index=False)
        print("✅ data_pl.csv berhasil diperbarui.")

        # Update data_pl_events.csv — preserve existing event annotations, append new rows only
        events_file = "data_pl_events.csv"
        if not os.path.exists(events_file):
            df_pl_events = df_rpl.copy()
            df_pl_events.insert(1, 'event', '')
            df_pl_events.to_csv(events_file, index=False)
            print("✅ data_pl_events.csv berhasil dibuat (baru).")
        else:
            df_existing_events = pd.read_csv(events_file)
            df_existing_events['date'] = pd.to_datetime(df_existing_events['date'], errors='coerce').dt.strftime('%Y-%m-%d')
            latest_date = df_existing_events['date'].max()
            df_new_rows = df_rpl[df_rpl['date'] > latest_date].copy()
            if not df_new_rows.empty:
                df_new_rows.insert(1, 'event', '')
                df_existing_events = pd.concat([df_existing_events, df_new_rows], ignore_index=True)
                df_existing_events = df_existing_events.sort_values('date').reset_index(drop=True)
                df_existing_events.to_csv(events_file, index=False)
                print(f"✅ data_pl_events.csv diperbarui (+{len(df_new_rows)} baris baru).")
            else:
                print("ℹ️ data_pl_events.csv: sudah up-to-date.")

        print(df_rpl[['date', 'btc_price', 'rpl_ratio', 'rrp', 'rrl', 'relative_realized_pl']].tail(3).to_string(index=False))
    else:
        print("❌ GAGAL: Data Realized P/L BTC kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 15 Realized P/L BTC: {e}")

# ==========================================
# 16. PIPELINE: AVIV RATIO & BANDS
# ==========================================
print("\n[16] Menarik data AVIV Ratio & Bands...")
try:
    df_aviv = fetch_data(
        "https://chartinspect.com/api/onchain/aviv-bands?timeframe=all&isProUser=false",
        ['date', 'btc_price', 'aviv_ratio', 'aviv_mean', 'aviv_upper_1sd', 'aviv_upper_2sd',
         'aviv_lower_1sd', 'aviv_lower_2sd', 'price_at_aviv_mean', 'price_at_aviv_plus_1_sigma',
         'price_at_aviv_plus_2_sigma', 'price_at_aviv_minus_1_sigma', 'investor_cap',
         'active_realized_price', 'liveliness']
    )

    if not df_aviv.empty:
        simpan(df_aviv, "data_aviv.csv", ['date', 'btc_price', 'aviv_ratio', 'aviv_mean'])
    else:
        print("❌ GAGAL: Data AVIV Bands kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 16 AVIV Bands: {e}")

# NOTE: kolom price_at_aviv_mean / price_at_aviv_plus_1_sigma dari API ChartInspect pakai
# active_realized_price sebagai basis, yang salah (basis benar = btc_price / aviv_ratio,
# match persis ke field true_market_mean_price mereka sendiri). app.py load_data_aviv() dan
# alerts/alert_check.py load_data() SUDAH menghitung ulang sendiri dari kolom mentah
# (btc_price, aviv_ratio, aviv_mean, aviv_upper_1sd) — kolom price_at_aviv_* di CSV ini
# cuma dipertahankan untuk kompatibilitas script lama di research/, jangan dipakai langsung
# di script baru.

# ==========================================
# 17. PIPELINE: APPARENT DEMAND
# ==========================================
print("\n[17] Menarik data Apparent Demand...")
try:
    df_demand = fetch_data(
        "https://chartinspect.com/api/onchain/apparent-demand?timeframe=all&isProUser=false",
        ['date', 'btc_price', 'apparent_demand']
    )

    if not df_demand.empty:
        simpan(df_demand, "data_apparent_demand.csv", ['date', 'apparent_demand'])
    else:
        print("❌ GAGAL: Data Apparent Demand kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 17 Apparent Demand: {e}")

# ==========================================
# 19. PIPELINE: US 2-YEAR TREASURY YIELD (MACRO)
# ==========================================
print("\n[19] Menarik data US 2-Year Treasury Yield...")
try:
    df_t2y = fetch_data("https://chartinspect.com/api/charts/economic/indicators?indicator=2y-treasury&timeframe=all")

    if not df_t2y.empty:
        # 'time' adalah Unix timestamp (detik); 'value' adalah yield dalam persen
        df_t2y['date'] = pd.to_datetime(df_t2y['time'], unit='s', utc=True).dt.strftime('%Y-%m-%d')
        df_t2y = df_t2y.rename(columns={'value': 'treasury_2y_yield'})[['date', 'treasury_2y_yield']]
        df_t2y = df_t2y.dropna(subset=['date']).drop_duplicates(subset=['date'], keep='last')
        simpan(df_t2y, "data_treasury_2y.csv")
    else:
        print("❌ GAGAL: Data Treasury 2Y kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 19 Treasury 2Y: {e}")

# ==========================================
# 20. PIPELINE: RELATIVE UNREALIZED P/L BY COHORT
# ==========================================
print("\n[20] Menarik data Relative Unrealized P/L by Cohort...")
try:
    df_rupl_cohort = fetch_data(
        "https://chartinspect.com/api/onchain/relative-unrealized-pl-by-cohort?timeframe=all&isProUser=false",
        ['date', 'btc_price', 'sth_rup', 'sth_rul', 'sth_nupl', 'lth_rup', 'lth_rul', 'lth_nupl']
    )

    if not df_rupl_cohort.empty:
        simpan(df_rupl_cohort, "data_relative_unrealized_pl_by_cohort.csv",
               ['date', 'sth_rup', 'sth_rul', 'lth_rup', 'lth_rul'])
    else:
        print("❌ GAGAL: Data Relative Unrealized P/L by Cohort kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 20 Relative Unrealized P/L by Cohort: {e}")

# ==========================================
# 21. PIPELINE: MEDIAN MVRV
# ==========================================
# Sumber ganda: histori (>=30 hari lalu, batasan tier free ChartInspect) pakai
# endpoint resmi (source='official'). Hari ini & gap yang belum ke-cover endpoint
# resmi dihitung dari URPD di Pipeline 22 (source='urpd_formula'). Begitu endpoint
# resmi akhirnya nyampe ke tanggal yang tadinya urpd_formula, baris itu DIVERIFIKASI
# (dibandingkan) dulu sebelum ditimpa angka resmi.
def baca_median_mvrv():
    """data_median_mvrv.csv yang ada (atau tabel kosong), tanggal sebagai teks."""
    if os.path.exists("data_median_mvrv.csv"):
        df = pd.read_csv("data_median_mvrv.csv")
    else:
        df = pd.DataFrame(columns=['date', 'btc_price', 'median_realized_price', 'median_mvrv', 'source'])
    if 'source' not in df.columns:
        df['source'] = 'official'  # file lama sebelum kolom source ada
    df['date'] = df['date'].astype(str)
    return df


print("\n[21] Menarik data Median MVRV...")
try:
    df_median_official = fetch_data(
        "https://chartinspect.com/api/onchain/median-mvrv?timeframe=all&isProUser=false",
        ['date', 'btc_price', 'median_realized_price', 'median_mvrv']
    )

    if not df_median_official.empty:
        df_median_official = df_median_official.sort_values('date').reset_index(drop=True)
        df_median_official['source'] = 'official'
        official_dates = set(df_median_official['date'])

        df_mm_prev = baca_median_mvrv()

        df_prev_urpd_rows = df_mm_prev[df_mm_prev['source'] == 'urpd_formula']

        # --- VERIFIKASI: tanggal yang tadinya urpd_formula, sekarang official-nya udah ada ---
        overlap = df_prev_urpd_rows[df_prev_urpd_rows['date'].isin(official_dates)]
        if not overlap.empty:
            print(f"🔍 Verifikasi {len(overlap)} baris urpd_formula vs official (baru tersedia):")
            for _, r in overlap.iterrows():
                official_row = df_median_official[df_median_official['date'] == r['date']].iloc[0]
                diff_pct = abs(r['median_mvrv'] - official_row['median_mvrv']) / official_row['median_mvrv'] * 100
                print(f"   {r['date']}: urpd_formula={r['median_mvrv']:.4f} vs official={official_row['median_mvrv']:.4f} "
                      f"(selisih {diff_pct:.2f}%)")

        # Baris urpd_formula yang tanggalnya BELUM ada di official tetap dipertahankan (gap)
        df_gap_rows = df_prev_urpd_rows[~df_prev_urpd_rows['date'].isin(official_dates)]

        df_median_mvrv = pd.concat([df_median_official, df_gap_rows], ignore_index=True)
        df_median_mvrv = df_median_mvrv.sort_values('date').reset_index(drop=True)
        df_median_mvrv.to_csv("data_median_mvrv.csv", index=False)
        print("✅ data_median_mvrv.csv berhasil diperbarui.")
        print(df_median_mvrv[['date', 'btc_price', 'median_realized_price', 'median_mvrv', 'source']].tail(5).to_string(index=False))
    else:
        print("❌ GAGAL: Data Median MVRV kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 21 Median MVRV: {e}")

# ==========================================
# 22. PIPELINE: URPD SNAPSHOT (UTXO REALIZED PRICE DISTRIBUTION)
# ==========================================
# CATATAN: endpoint /api/onchain/urpd TIDAK punya historis — selalu balikin snapshot
# hari-ini persis (parameter date/timestamp/isProUser diabaikan). Beda dari endpoint
# lain di file ini, jadi histori data_urpd.csv cuma numpuk maju dari titik pertama
# script ini dijalankan, TIDAK bisa backfill ke masa lalu.
print("\n[22] Menarik snapshot URPD (UTXO Realized Price Distribution)...")
try:
    res_urpd = requests.get("https://chartinspect.com/api/onchain/urpd?timeframe=all&isProUser=false")
    raw_urpd = res_urpd.json().get('data', [])

    if raw_urpd:
        today_str = datetime.now().strftime('%Y-%m-%d')
        df_urpd_today = pd.DataFrame(raw_urpd)[
            ['bucket_min', 'bucket_max', 'price_bucket', 'btc_amount',
             'percentage', 'cumulative_pct', 'in_profit', 'avg_age_days', 'utxo_count']
        ]
        df_urpd_today.insert(0, 'date', today_str)

        if os.path.exists("data_urpd.csv"):
            df_urpd_existing = pd.read_csv("data_urpd.csv")
            df_urpd_existing = df_urpd_existing[df_urpd_existing['date'] != today_str]
            df_urpd_all = pd.concat([df_urpd_existing, df_urpd_today], ignore_index=True)
        else:
            df_urpd_all = df_urpd_today

        df_urpd_all = df_urpd_all.sort_values(['date', 'bucket_min']).reset_index(drop=True)
        df_urpd_all.to_csv("data_urpd.csv", index=False)
        print(f"✅ data_urpd.csv berhasil diperbarui (snapshot {today_str}, {len(df_urpd_today)} bucket). Total baris: {len(df_urpd_all)}")

        # --- Gap-fill Median MVRV real-time dari URPD hari ini ---
        # Endpoint resmi median-mvrv (Pipeline 21) lag ~30 hari. Tapi URPD adalah data
        # MENTAH sumber Median MVRV — jadi bisa dihitung EXACT (bukan proxy) langsung dari
        # snapshot hari ini: cari titik cumulative_pct = 50% (interpolasi linear di dalam
        # bucket), itu Median Realized Price. Median MVRV = btc_price / Median Realized Price.
        try:
            def _median_realized_price_from_urpd(buckets):
                prev_cum = 0.0
                for b in buckets:
                    cum = b['cumulative_pct']
                    if cum >= 50:
                        span = cum - prev_cum
                        frac = (50 - prev_cum) / span if span > 0 else 0
                        return b['bucket_min'] + frac * (b['bucket_max'] - b['bucket_min'])
                    prev_cum = cum
                return buckets[-1]['bucket_max']

            df_price_latest = pd.read_csv("data_price_level.csv")
            df_price_latest['date'] = pd.to_datetime(df_price_latest['date'], errors='coerce').dt.strftime('%Y-%m-%d')
            today_price_row = df_price_latest[df_price_latest['date'] == today_str]

            if not today_price_row.empty:
                today_btc_price = float(today_price_row.iloc[-1]['btc_price'])
                median_rp_today = _median_realized_price_from_urpd(raw_urpd)
                median_mvrv_today = today_btc_price / median_rp_today

                df_mm = baca_median_mvrv()

                if today_str not in df_mm['date'].values:
                    df_new_row = pd.DataFrame([{
                        'date': today_str,
                        'btc_price': today_btc_price,
                        'median_realized_price': round(median_rp_today, 2),
                        'median_mvrv': round(median_mvrv_today, 4),
                        'source': 'urpd_formula',
                    }])
                    df_mm = pd.concat([df_mm, df_new_row], ignore_index=True)
                    df_mm = df_mm.sort_values('date').reset_index(drop=True)
                    df_mm.to_csv("data_median_mvrv.csv", index=False)
                    print(f"✅ Median MVRV {today_str} dihitung real-time dari URPD (gap-fill): "
                          f"{round(median_mvrv_today, 4)} (median RP ${median_rp_today:,.2f})")
                else:
                    print(f"ℹ️ data_median_mvrv.csv sudah punya baris {today_str}, skip gap-fill.")
            else:
                print("⚠️ btc_price hari ini belum ada di data_price_level.csv, skip gap-fill Median MVRV.")
        except Exception as e:
            print(f"❌ Error gap-fill Median MVRV dari URPD: {e}")
    else:
        print("❌ GAGAL: Data URPD kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error Pipeline 22 URPD Snapshot: {e}")

# ==========================================
# 23. PIPELINE: PASAR TRADISIONAL (YAHOO FINANCE)
# ==========================================
# Harga penutupan harian aset non-kripto untuk halaman pembanding di dashboard.
# Semua ticker masuk SATU file, satu kolom per aset: menambah VIX / DXY / yield nanti
# cukup satu baris di TRADFI_TICKERS.
# - Hanya hari bursa (akhir pekan & libur tidak ada baris); isi kekosongan dilakukan
#   di loader dashboard/research, bukan di sini, supaya data mentah tetap jujur.
# - Tanggal = timestamp + gmtoffset bursa, jadi tanggalnya tanggal lokal bursa.
# - Seluruh sejarah ditarik ulang tiap jalan, sehingga bar hari ini yang belum final
#   (mis. GC=F yang diperdagangkan hampir 24 jam) otomatis terkoreksi besoknya.
# - Kalau satu ticker gagal, kolom lamanya di file dipertahankan (tidak dikosongkan).
TRADFI_TICKERS = {
    'spx': '^GSPC',   # S&P 500
    'xau': 'GC=F',    # Emas, futures bulan terdekat (pendekatan harga spot)
}
print("\n[23] Menarik harga pasar tradisional dari Yahoo Finance...")
try:
    tradfi_file = "data_tradfi.csv"
    if os.path.exists(tradfi_file):
        df_tradfi = pd.read_csv(tradfi_file, dtype={'date': str}).set_index('date')
    else:
        df_tradfi = pd.DataFrame(index=pd.Index([], name='date', dtype=str))

    berhasil = 0
    for kolom, simbol in TRADFI_TICKERS.items():
        try:
            res_yf = requests.get(
                f"https://query1.finance.yahoo.com/v8/finance/chart/{simbol}",
                params={'period1': 1262304000,  # 1 Jan 2010
                        'period2': int(datetime.now().timestamp()),
                        'interval': '1d'},
                headers={'User-Agent': 'Mozilla/5.0'},
                timeout=30,
            )
            hasil = res_yf.json()['chart']['result'][0]
            offset = hasil['meta'].get('gmtoffset', 0)
            tanggal = pd.to_datetime(pd.Series(hasil['timestamp']) + offset, unit='s').dt.strftime('%Y-%m-%d')
            seri = pd.Series(hasil['indicators']['quote'][0]['close'], index=tanggal.values, dtype=float).dropna()
            seri = seri[~seri.index.duplicated(keep='last')]
            if seri.empty:
                raise ValueError("data kosong")
            df_tradfi = df_tradfi.drop(columns=[kolom], errors='ignore').join(seri.rename(kolom), how='outer')
            berhasil += 1
            print(f"   {kolom} ({simbol}): {len(seri)} hari, terakhir {seri.index[-1]} = {seri.iloc[-1]:,.2f}")
        except Exception as e:
            print(f"   ⚠️ {kolom} ({simbol}) gagal: {e} — kolom lama dipertahankan")

    if berhasil:
        df_tradfi.index.name = 'date'
        df_tradfi = df_tradfi.sort_index()
        df_tradfi = df_tradfi[[k for k in TRADFI_TICKERS if k in df_tradfi.columns]]
        df_tradfi.reset_index().to_csv(tradfi_file, index=False)
        print(f"✅ {tradfi_file} berhasil diperbarui ({berhasil}/{len(TRADFI_TICKERS)} ticker).")
    else:
        print(f"❌ GAGAL: semua ticker Yahoo gagal, {tradfi_file} tidak diubah.")
except Exception as e:
    print(f"❌ Error Pipeline 23 Pasar Tradisional: {e}")

# ==========================================
# 24. PIPELINE: VIX (CBOE RESMI)
# ==========================================
# VIX dari file resmi Cboe (pembuat indeks), bukan Yahoo: Yahoo kehilangan 31 dari 33 hari
# libur bursa AS yang dihitung Cboe sejak Mei 2022 dan 9 penutupannya beda (terbesar 6 Feb
# 2026: 20,37 vs 17,76). FRED VIXCLS = salinan persis Cboe (dicek 21 Sep 2026).
# Nilai di hari libur bursa AS itu resmi dari Cboe, dibiarkan apa adanya.
# Seluruh sejarah ditarik ulang tiap jalan; gagal = file lama tidak diubah.
print("\n[24] Menarik VIX dari Cboe...")
try:
    df_vix = pd.read_csv(
        "https://cdn.cboe.com/api/global/us_indices/daily_prices/VIX_History.csv",
        storage_options={'User-Agent': 'Mozilla/5.0'},
    )
    df_vix = pd.DataFrame({
        'date': pd.to_datetime(df_vix['DATE'], format='%m/%d/%Y').dt.strftime('%Y-%m-%d'),
        'vix': df_vix['CLOSE'],
    }).dropna()
    if df_vix.empty:
        raise ValueError("data kosong")
    simpan(df_vix, "data_vix.csv")
except Exception as e:
    print(f"❌ Error Pipeline 24 VIX: {e} — data_vix.csv tidak diubah")

# ==========================================
# 25. PIPELINE: US TREASURY YIELD 2Y & 10Y (FRED)
# ==========================================
# FRED DGS2/DGS10 harian (persen), tanpa API key. Kalender pasar obligasi AS: Columbus Day dan
# Veterans Day kosong, Good Friday ada nilainya; dibiarkan apa adanya. data_treasury_2y.csv
# (Pipeline 19) = DGS2 versi bulanan (cek 21 Sep 2026: rata-rata bulanan beda maks 0,005).
# Seluruh sejarah ditarik ulang tiap jalan; gagal = file lama tidak diubah.
print("\n[25] Menarik US Treasury Yield 2Y & 10Y dari FRED...")
try:
    df_yields = None
    for kolom, seri in {'us2y': 'DGS2', 'us10y': 'DGS10'}.items():
        # Tanpa User-Agent 'Mozilla/5.0': FRED membiarkannya timeout (dicek 22 Sep 2026);
        # User-Agent bawaan Python diterima.
        df_y = pd.read_csv(f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={seri}")
        df_y = pd.DataFrame({'date': df_y.iloc[:, 0],
                             kolom: pd.to_numeric(df_y[seri], errors='coerce')}).dropna()
        if df_y.empty:
            raise ValueError(f"{seri} kosong")
        df_yields = df_y if df_yields is None else df_yields.merge(df_y, on='date', how='outer')
    simpan(df_yields, "data_yields.csv")
except Exception as e:
    print(f"❌ Error Pipeline 25 Treasury Yield: {e} — data_yields.csv tidak diubah")

# ==========================================
# 26. PIPELINE: BTC 3M ANNUALIZED FUTURES BASIS (BINANCE COIN-M + DERIBIT)
# ==========================================
# Dipindah dari research/fetch_futures_basis_history.py (22 Sep 2026). Per hari, per bursa:
# dua kontrak quarterly yang mengapit tenor 90 hari, basis tahunan = (F/S - 1) * 365 / hari ke
# expiry, diinterpolasi linear ke tepat 90 hari; hasil = rata-rata bursa yang ada. Mulai Jun 2020.
# Seluruh sejarah dihitung ulang tiap jalan. Satu bursa gagal = bursa lain tetap dipakai; semua
# gagal = file lama tidak diubah.
# Spot = Bitstamp BTC/USD, close 00:00 UTC (sejak 22 Sep 2026). Sebelumnya index Binance BTCUSD
# (dapi), tapi di GitHub Actions dapi tidak memberi data ("index Binance kosong", run 22 Sep) dan
# seluruh pipeline gagal. Beda Bitstamp vs index Binance: median 0,001 %, p95 0,05 % = efek ke
# basis 3M median 0,005 poin, p95 0,2 poin.
print("\n[26] Menarik futures basis 3 bulan (Binance COIN-M + Deribit)...")
try:
    import calendar
    from datetime import timedelta, timezone

    BASIS_START = datetime(2020, 6, 1, tzinfo=timezone.utc)
    BASIS_END = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    BULAN = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]

    def _ms(dt):
        return int(dt.timestamp() * 1000)

    def _jumat_terakhir(y, m):
        dt = datetime(y, m, calendar.monthrange(y, m)[1], 8, tzinfo=timezone.utc)
        while dt.weekday() != 4:
            dt -= timedelta(days=1)
        return dt

    # Expiry quarterly Deribit & Binance: Jumat terakhir Mar/Jun/Sep/Des 08:00 UTC
    EXPIRY = [_jumat_terakhir(y, m) for y in range(2020, BASIS_END.year + 2) for m in (3, 6, 9, 12)]

    def _binance(path, params):
        rows, start = [], _ms(BASIS_START)
        while True:
            r = requests.get(f"https://dapi.binance.com/dapi/v1/{path}", timeout=30, params={
                **params, "interval": "1d", "startTime": start, "limit": 1500}).json()
            if not isinstance(r, list):
                print(f"   ⚠️ Binance {path}: {str(r)[:150]}")   # jawaban mentah untuk diagnosis
                break
            if not r:
                break
            rows += r
            start = r[-1][0] + 86_400_000
            if len(r) < 1500:
                break
        s = pd.Series({pd.Timestamp(k[0], unit="ms"): float(k[4]) for k in rows}, dtype=float)
        return s[~s.index.duplicated()]

    def _deribit(nama, start, end):
        r = requests.get("https://www.deribit.com/api/v2/public/get_tradingview_chart_data", timeout=30,
                         params={"instrument_name": nama, "resolution": "60",
                                 "start_timestamp": _ms(start), "end_timestamp": _ms(end)}).json()
        res = r.get("result") or {}
        if res.get("status") != "ok":
            if "error" in r:
                print(f"   ⚠️ Deribit {nama}: {str(r['error'])[:150]}")
            return pd.Series(dtype=float)
        # Bar 1 jam yang mulai 23:00 -> close 00:00 UTC, sama dengan index
        s = pd.Series(res["close"], index=pd.to_datetime(res["ticks"], unit="ms"))
        s = s[s.index.hour == 23]
        s.index = s.index.normalize()
        return s

    def _ke_90_hari(titik):
        titik = sorted(p for p in titik if p[0] >= 7)  # kontrak < 7 hari ke expiry terlalu berisik
        bawah = [p for p in titik if p[0] <= 90]
        atas = [p for p in titik if p[0] > 90]
        if bawah and atas:
            (t1, b1), (t2, b2) = bawah[-1], atas[0]
            return b1 + (b2 - b1) * (90 - t1) / (t2 - t1)
        dekat = [p for p in titik if 60 <= p[0] <= 120]
        return min(dekat, key=lambda p: abs(p[0] - 90))[1] if dekat else None

    def _aman(f, *a):
        try:
            return f(*a)
        except Exception as e:
            print(f"   ⚠️ {f.__name__}{a[:1]} gagal: {e}")
            return pd.Series(dtype=float)

    def _bitstamp():
        rows, start = [], int(BASIS_START.timestamp())
        while True:
            o = requests.get("https://www.bitstamp.net/api/v2/ohlc/btcusd/", timeout=30, params={
                "step": 86400, "limit": 1000, "start": start}).json()["data"]["ohlc"]
            rows += o
            if len(o) < 1000:
                break
            start = int(o[-1]["timestamp"]) + 86400
        s = pd.Series({pd.Timestamp(int(x["timestamp"]), unit="s"): float(x["close"]) for x in rows},
                      dtype=float)
        s = s[~s.index.duplicated()]
        return s[s.index < pd.Timestamp(BASIS_END.date())]   # bar hari ini belum tutup

    idx = _bitstamp()
    if idx.empty:
        raise ValueError("spot Bitstamp kosong")
    cq = _aman(_binance, "continuousKlines", {"pair": "BTCUSD", "contractType": "CURRENT_QUARTER"})
    nq = _aman(_binance, "continuousKlines", {"pair": "BTCUSD", "contractType": "NEXT_QUARTER"})
    deribit = {}
    for e in EXPIRY:
        if e - timedelta(days=200) > BASIS_END:
            continue
        s = _aman(_deribit, f"BTC-{e.day}{BULAN[e.month - 1]}{e.year % 100:02d}",
                  max(BASIS_START, e - timedelta(days=200)), min(e, BASIS_END + timedelta(days=1)))
        if len(s):
            deribit[e] = s
    print(f"   spot Bitstamp {len(idx)} hari, Binance CQ {len(cq)} / NQ {len(nq)}, Deribit {len(deribit)} kontrak")

    baris = []
    for hari, spot in idx.items():
        tutup = hari.tz_localize("UTC") + timedelta(days=1)
        depan = [e for e in EXPIRY if e > tutup]
        tenor = lambda e: (e - tutup).total_seconds() / 86400
        tahunan = lambda f, e: (f / spot - 1) * 365 / tenor(e) * 100
        bn = []
        if hari in cq.index:
            bn.append((tenor(depan[0]), tahunan(cq[hari], depan[0])))
        if hari in nq.index:
            bn.append((tenor(depan[1]), tahunan(nq[hari], depan[1])))
        dr = [(tenor(e), tahunan(s[hari], e)) for e, s in deribit.items() if e > tutup and hari in s.index]
        b, d = _ke_90_hari(bn), _ke_90_hari(dr)
        ada = [v for v in (b, d) if v is not None]
        baris.append({'date': hari.strftime('%Y-%m-%d'), 'basis_binance': b, 'basis_deribit': d,
                      'basis_3m': sum(ada) / len(ada) if ada else None})
    df_basis = pd.DataFrame(baris).dropna(subset=['basis_3m']).round(4)
    if df_basis.empty:
        raise ValueError("basis kosong (semua bursa gagal)")
    simpan(df_basis, "data_futures_basis_3m.csv")
except Exception as e:
    print(f"❌ Error Pipeline 26 Futures Basis: {e} — data_futures_basis_3m.csv tidak diubah")

# ==========================================
# 18. MASTER PIPELINE: ALL METRICS AGGREGATOR (NEW)
# ==========================================
print("\n[Master] 🌌 Mengkompilasi Semua File CSV ke dalam 1 Master Dataset...")
try:
    # Daftar semua file CSV target hulu hasil rekapitulasi individu
    csv_files = [
        "data_price_level.csv", "data_momentum.csv", "data_pl.csv",
        "data_derivatives.csv", "data_sentiment.csv", "data_supply.csv",
        "data_mvrv.csv", "data_fg.csv", "data_exchange.csv", "data_rhodl.csv",
        "data_hodl_waves.csv", "data_realized_cap.csv", "data_cdd.csv", "data_lth_flow.csv",
        "data_aviv.csv", "data_apparent_demand.csv", "data_treasury_2y.csv",
        "data_relative_unrealized_pl_by_cohort.csv", "data_median_mvrv.csv",
        "data_tradfi.csv", "data_vix.csv", "data_yields.csv",
        "data_futures_basis_3m.csv"
    ]
    
    df_master = None
    
    for file in csv_files:
        if os.path.exists(file):
            df_temp = pd.read_csv(file)
            if not df_temp.empty:
                # Standardisasi string format tanggal secara ketat
                df_temp['date'] = pd.to_datetime(df_temp['date'], errors='coerce').dt.strftime('%Y-%m-%d')
                df_temp = df_temp.dropna(subset=['date']).drop_duplicates(subset=['date'], keep='last')
                
                # Jika ada kolom btc_price di file pecahan, hapus agar tidak melahirkan duplikat btc_price_x / btc_price_y
                if df_master is not None and 'btc_price' in df_temp.columns:
                    df_temp = df_temp.drop(columns=['btc_price'], errors='ignore')
                
                # Eksekusi Outer Merge Gabungan Makro
                if df_master is None:
                    df_master = df_temp
                else:
                    df_master = pd.merge(df_master, df_temp, on='date', how='outer')
                    
    if df_master is not None and not df_master.empty:
        # Sortir kronologis dari tanggal terlama ke terbaru
        df_master = df_master.sort_values('date').reset_index(drop=True)
        
        # Susun tata letak urutan kolom: 'date' selalu berada di paling kiri
        cols = ['date'] + [col for col in df_master.columns if col != 'date']
        df_master = df_master[cols]
        
        # Simpan ke dalam satu file master final
        df_master.to_csv("data_master_all_metrics.csv", index=False)
        print("📊 --------------------------------------------------------")
        print("✅ DETECTED SUCCESS: 'data_master_all_metrics.csv' BERHASIL DISUNTIK!")
        print(f"   Total Baris Data : {df_master.shape[0]} Hari")
        print(f"   Total Kolom Metrik: {df_master.shape[1]} Indikator")
        print("📊 --------------------------------------------------------")
    else:
        print("❌ GAGAL MASTER AGGREGATOR: Tidak ada file CSV pecahan yang ditemukan untuk digabungkan.")
except Exception as e:
    print(f"❌ Error Fatal pada Master Aggregator Pipeline 15: {e}")

print("\n🎉 Semua proses selesai! CSV tersimpan rapi.")
