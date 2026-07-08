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

# ==========================================
# 1. PIPELINE: PRICE LEVELS & MOVING AVERAGES
# ==========================================
print("\n[1/15] Menarik data Price Levels...")
# 🟢 FIX: Tambahkan 'active_realized_price' dan 'mvrv_avg_price' ke dalam whitelist kolom hulu (akan di-rename ke 'MVRV 0σ' sebelum disimpan)
df_price = fetch_data("https://chartinspect.com/api/onchain/onchain-price-levels?timeframe=all&isProUser=false", 
                      ['date', 'btc_price', 'sth_cost_basis', 'lth_cost_basis', 'realized_price', 'cvdd', 'active_realized_price', 'mvrv_avg_price'])
df_tmm = fetch_data("https://chartinspect.com/api/onchain/true-market-mean?timeframe=all&isProUser=false", ['date', 'true_market_mean_price'])

if not df_price.empty and not df_tmm.empty:
    df_master_price = pd.merge(df_price, df_tmm, on='date', how='outer')
    df_master_price['date'] = pd.to_datetime(df_master_price['date']).dt.strftime('%Y-%m-%d')
    df_master_price = df_master_price.sort_values('date').reset_index(drop=True)
    
    # Kalkulasi Moving Averages
    df_master_price['200_dma'] = df_master_price['btc_price'].rolling(window=200, min_periods=1).mean()
    df_master_price['50_wma'] = df_master_price['btc_price'].rolling(window=350, min_periods=1).mean()
    df_master_price['200_wma'] = df_master_price['btc_price'].rolling(window=1400, min_periods=1).mean()

    # Rename kolom API ke nama display sebelum disimpan ke CSV
    df_master_price.rename(columns={'mvrv_avg_price': 'MVRV 0σ'}, inplace=True)

    df_master_price.to_csv("data_price_level.csv", index=False)
    print("✅ data_price_level.csv berhasil diperbarui.")
    print(df_master_price.tail(3).to_string(index=False))

# ==========================================
# 2. PIPELINE: MOMENTUM & P/L
# ==========================================
print("\n[2/15] Menarik data Momentum & P/L...")
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
    
    df_age_clean = df_age[['date', 'sth_pl_ratio', 'lth_pl_ratio']]
else:
    df_age_clean = pd.DataFrame(columns=['date', 'sth_pl_ratio', 'lth_pl_ratio'])

dfs = [df_sopr, df_lth_sopr, df_sth_sopr, df_net_pl, df_age_clean, df_nupl]
df_master_mom = dfs[0]
for d in dfs[1:]:
    if not d.empty:
        df_master_mom = pd.merge(df_master_mom, d, on='date', how='outer')

if not df_master_mom.empty:
    df_master_mom['date'] = pd.to_datetime(df_master_mom['date']).dt.strftime('%Y-%m-%d')
    df_master_mom = df_master_mom.sort_values('date').reset_index(drop=True)
    df_master_mom.to_csv("data_momentum.csv", index=False)
    print("✅ data_momentum.csv berhasil diperbarui.")
    print(df_master_mom[['date', 'btc_price', 'sth_pl_ratio', 'lth_pl_ratio']].tail(3).to_string(index=False))

# ==========================================
# 3. PIPELINE: DERIVATIVES
# ==========================================
print("\n[3/15] Menarik data Derivatives...")
df_funding = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-funding-rates?timeframe=all", ['date', 'btc_price', 'funding_rate'])
df_oi = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-open-interest?timeframe=all", ['date', 'total_oi'])

if not df_funding.empty and not df_oi.empty:
    df_oi_clean = df_oi[['date', 'total_oi']]
    df_master_deriv = pd.merge(df_funding, df_oi_clean, on='date', how='outer')
    df_master_deriv['date'] = pd.to_datetime(df_master_deriv['date']).dt.strftime('%Y-%m-%d')
    df_master_deriv = df_master_deriv.sort_values('date').reset_index(drop=True)
    df_master_deriv.to_csv("data_derivatives.csv", index=False)
    print("✅ data_derivatives.csv berhasil diperbarui.")
    print(df_master_deriv.tail(3).to_string(index=False))

# ==========================================
# 4. PIPELINE: SOCIAL SENTIMENT
# ==========================================
print("\n[4/15] Menarik data Social Sentiment...")
df_gtrend = fetch_data("https://chartinspect.com/api/charts/onchain/google-trends?timeframe=all&isProUser=false", 
                       ['date', 'btc_price', 'trend_bitcoin', 'trend_crypto', 'trend_ethereum', 'trend_nft'])
df_wiki = fetch_data("https://chartinspect.com/api/charts/onchain/wikipedia-pageviews?timeframe=all&isProUser=false", 
                     ['date', 'wiki_bitcoin', 'wiki_cryptocurrency', 'wiki_ethereum', 'wiki_blockchain'])

if not df_gtrend.empty and not df_wiki.empty:
    df_wiki_clean = df_wiki.drop(columns=['btc_price'], errors='ignore')
    df_master_sentiment = pd.merge(df_gtrend, df_wiki_clean, on='date', how='outer')
    df_master_sentiment['date'] = pd.to_datetime(df_master_sentiment['date']).dt.strftime('%Y-%m-%d')
    df_master_sentiment = df_master_sentiment.sort_values('date').reset_index(drop=True)
    df_master_sentiment.to_csv("data_sentiment.csv", index=False)
    print("✅ data_sentiment.csv berhasil diperbarui.")
    print(df_master_sentiment[['date', 'trend_bitcoin', 'wiki_bitcoin']].tail(3).to_string(index=False))

# ==========================================
# 5. PIPELINE: SUPPLY DYNAMICS
# ==========================================
print("\n[5/15] Menarik data Supply Dynamics...")
df_sth_lth = fetch_data("https://chartinspect.com/api/onchain/sth-lth?timeframe=all&isProUser=false", 
                       ['date', 'btc_price', 'lth_supply_btc', 'sth_supply_btc', 'pct_lth_in_profit', 'pct_sth_in_profit', 'pct_lth_in_loss', 'pct_sth_in_loss'])
df_profit_loss = fetch_data("https://chartinspect.com/api/onchain/profit-loss?timeframe=all&isProUser=false", 
                            ['date', 'percent_btc_in_profit', 'percent_btc_in_loss'])

if not df_sth_lth.empty and not df_profit_loss.empty:
    df_profit_loss_clean = df_profit_loss[['date', 'percent_btc_in_profit', 'percent_btc_in_loss']]
    df_supply = pd.merge(df_sth_lth, df_profit_loss_clean, on='date', how='outer')
    df_supply['date'] = pd.to_datetime(df_supply['date']).dt.strftime('%Y-%m-%d')
    df_supply = df_supply.sort_values('date').reset_index(drop=True)
    df_supply.to_csv("data_supply.csv", index=False)
    print("✅ data_supply.csv berhasil diperbarui.")
    print(df_supply[['date', 'lth_supply_btc', 'sth_supply_btc']].tail(3).to_string(index=False))

# ==========================================
# 6. PIPELINE: MARKET VALUATION
# ==========================================
print("\n[6/15] Menarik data Market Valuation...")
df_mvrv = fetch_data("https://chartinspect.com/api/onchain/mvrv?timeframe=all&isProUser=false",
                     ['date', 'btc_price', 'mvrv', 'sth_mvrv', 'lth_mvrv'])
df_mvrv_z = fetch_data("https://chartinspect.com/api/onchain/mvrv-z-score?timeframe=all&isProUser=false",
                       ['date', 'mvrv_zscore'])

if not df_mvrv.empty:
    df_mvrv.rename(columns={'mvrv': 'mvrv_ratio'}, inplace=True)
    df_mvrv['date'] = pd.to_datetime(df_mvrv['date']).dt.strftime('%Y-%m-%d')
    df_mvrv = df_mvrv.sort_values('date').reset_index(drop=True)

    if not df_mvrv_z.empty:
        df_mvrv_z['date'] = pd.to_datetime(df_mvrv_z['date']).dt.strftime('%Y-%m-%d')
        df_mvrv = pd.merge(df_mvrv, df_mvrv_z, on='date', how='left')

    df_mvrv.to_csv("data_mvrv.csv", index=False)
    print("✅ data_mvrv.csv berhasil diperbarui.")
    print(df_mvrv.tail(3).to_string(index=False))
    
# ==========================================
# 7. PIPELINE: FEAR & GREED
# ==========================================
print("\n[7/15] Menarik data Fear & Greed...")
df_fg = fetch_data("https://chartinspect.com/api/charts/crypto/fear-greed-index?timeframe=all&isProUser=false")
if not df_fg.empty:
    df_fg['date'] = pd.to_datetime(df_fg['timestamp'], unit='s').dt.strftime('%Y-%m-%d')
    df_fg.rename(columns={'value': 'Fear & Greed'}, inplace=True)
    df_fg_clean = df_fg[['date', 'Fear & Greed']].sort_values('date').reset_index(drop=True)
    df_fg_clean.to_csv("data_fg.csv", index=False)
    print("✅ data_fg.csv berhasil diperbarui.")
    print(df_fg_clean.tail(3).to_string(index=False))

# ==========================================
# 8. PIPELINE: EXCHANGE FLOWS
# ==========================================
print("\n[8/15] Menarik data Exchange Flow...")
df_ex = fetch_data("https://chartinspect.com/api/charts/exchange-etf/exchange-flows?timeframe=all", 
                   ['date', 'btc_price', 'total_balance', 'net_flow', 'inflow', 'outflow'])
if not df_ex.empty:
    df_ex['date'] = pd.to_datetime(df_ex['date'], format='mixed', errors='coerce').dt.strftime('%Y-%m-%d')
    df_ex = df_ex.sort_values('date').reset_index(drop=True)
    df_ex.to_csv("data_exchange.csv", index=False)
    print("✅ data_exchange.csv berhasil diperbarui.")
    print(df_ex[['date', 'total_balance', 'net_flow']].tail(3).to_string(index=False))

# ==========================================
# 9. PIPELINE: CUMULATIVE P/L PRICE & RATIO
# ==========================================
print("\n[9/15] Mengkalkulasi Cumulative P/L Price...")
try:
    df_age_raw = fetch_data("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
    
    if not df_age_raw.empty:
        df_age_raw['date'] = pd.to_datetime(df_age_raw['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
        df_age_raw = df_age_raw.sort_values('date').reset_index(drop=True)
        
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
            df_p_rekap = pd.read_csv("data_price_level.csv")
            df_p_rekap['date'] = pd.to_datetime(df_p_rekap['date'], errors='coerce').dt.strftime('%Y-%m-%d')
            
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
print("\n[10/15] Menarik data RHODL Ratio...")
df_rhodl = fetch_data("https://chartinspect.com/api/onchain/rhodl?historical=true&timeframe=all&isProUser=false")
if not df_rhodl.empty:
    cols_rhodl = ['date', 'btc_price', 'rhodl_ratio', 'realized_cap_1w', 'realized_cap_1_2y']
    available_cols = [c for c in cols_rhodl if c in df_rhodl.columns]
    
    df_rhodl_clean = df_rhodl[available_cols].copy()
    df_rhodl_clean['date'] = pd.to_datetime(df_rhodl_clean['date']).dt.strftime('%Y-%m-%d')
    df_rhodl_clean = df_rhodl_clean.sort_values('date').reset_index(drop=True)
    df_rhodl_clean.to_csv("data_rhodl.csv", index=False)
    
    print("✅ data_rhodl.csv berhasil diperbarui.")
    print(df_rhodl_clean[['date', 'rhodl_ratio']].tail(3).to_string(index=False))

# ==========================================
# 11. PIPELINE: HODL WAVES (SPECIAL PARSING)
# ==========================================
print("\n[11/15] Menarik data HODL Waves...")
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
        df_hw['date'] = pd.to_datetime(df_hw['date']).dt.strftime('%Y-%m-%d')
        df_hw = df_hw.sort_values('date').reset_index(drop=True)
        
        df_hw.to_csv("data_hodl_waves.csv", index=False)
        print("✅ data_hodl_waves.csv berhasil diperbarui.")
        print(df_hw[['date', 'supply_1y-2y', 'realized_cap_1y-2y']].tail(3).to_string(index=False))
    else:
        print("❌ GAGAL: Endpoint HODL Waves mengembalikan array kosong.")
except Exception as e:
    print(f"❌ Error fetching HODL Waves: {e}")

# ==========================================
# 12. PIPELINE: REALIZED CAP
# ==========================================
print("\n[12/15] Menarik data Realized Cap...")
try:
    url_rcap = "https://chartinspect.com/api/onchain/realized-cap?timeframe=all&isProUser=false"
    cols_rcap = ['date', 'btc_price', 'realized_cap_usd', 'lth_realized_cap_usd', 'sth_realized_cap_usd']
    df_rcap = fetch_data(url_rcap, cols_rcap)
    
    if not df_rcap.empty:
        df_rcap['date'] = pd.to_datetime(df_rcap['date']).dt.strftime('%Y-%m-%d')
        df_rcap = df_rcap.sort_values('date').reset_index(drop=True)
        df_rcap.to_csv("data_realized_cap.csv", index=False)
        print("✅ data_realized_cap.csv berhasil diperbarui.")
        print(df_rcap[['date', 'realized_cap_usd']].tail(3).to_string(index=False))
    else:
        print("❌ GAGAL: Data Realized Cap kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error fetching Realized Cap: {e}")

# ==========================================
# 13. PIPELINE: COIN DAYS DESTROYED (CDD)
# ==========================================
print("\n[13/15] Menarik data Coin Days Destroyed (CDD)...")
try:
    url_cdd = "https://chartinspect.com/api/onchain/cdd?timeframe=all&isProUser=false"
    cols_cdd = ['date', 'cdd', 'vdd_30d_ma', 'vdd_365d_ma', 'vdd_multiple']
    df_cdd = fetch_data(url_cdd, cols_cdd)
    
    if not df_cdd.empty:
        df_cdd['date'] = pd.to_datetime(df_cdd['date']).dt.strftime('%Y-%m-%d')
        df_cdd = df_cdd.sort_values('date').reset_index(drop=True)
        df_cdd.to_csv("data_cdd.csv", index=False)
        print("✅ data_cdd.csv berhasil diperbarui.")
        print(df_cdd[['date', 'cdd', 'vdd_multiple']].tail(3).to_string(index=False))
    else:
        print("❌ GAGAL: Data CDD kosong atau gagal ditarik.")
except Exception as e:
    print(f"❌ Error fetching CDD: {e}")

# ==========================================
# 14. PIPELINE: LTH P/L PRICE FLOW
# ==========================================
print("\n[14/15] Mengkalkulasi LTH P/L Price Flow...")
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
# 15. MASTER PIPELINE: ALL METRICS AGGREGATOR (NEW)
# ==========================================
print("\n[15/15] 🌌 Mengkompilasi Semua File CSV ke dalam 1 Master Dataset...")
try:
    # Daftar semua file CSV target hulu hasil rekapitulasi individu
    csv_files = [
        "data_price_level.csv", "data_momentum.csv", "data_derivatives.csv",
        "data_sentiment.csv", "data_supply.csv", "data_mvrv.csv", "data_fg.csv",
        "data_exchange.csv", "data_rhodl.csv", "data_hodl_waves.csv",
        "data_realized_cap.csv", "data_cdd.csv", "data_lth_flow.csv"
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
