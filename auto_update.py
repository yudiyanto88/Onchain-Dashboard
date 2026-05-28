import requests
import pandas as pd
from datetime import datetime
import numpy as np

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
print("\n[1/9] Menarik data Price Levels...")
df_price = fetch_data("https://chartinspect.com/api/onchain/onchain-price-levels?timeframe=all&isProUser=false", ['date', 'btc_price', 'sth_cost_basis', 'lth_cost_basis', 'realized_price', 'cvdd'])
df_tmm = fetch_data("https://chartinspect.com/api/onchain/true-market-mean?timeframe=all&isProUser=false", ['date', 'true_market_mean_price'])

if not df_price.empty and not df_tmm.empty:
    df_master_price = pd.merge(df_price, df_tmm, on='date', how='outer')
    df_master_price['date'] = pd.to_datetime(df_master_price['date'])
    df_master_price = df_master_price.sort_values('date').reset_index(drop=True)
    
    # Kalkulasi Moving Averages
    df_master_price['200_dma'] = df_master_price['btc_price'].rolling(window=200, min_periods=1).mean()
    df_master_price['50_wma'] = df_master_price['btc_price'].rolling(window=350, min_periods=1).mean()
    df_master_price['200_wma'] = df_master_price['btc_price'].rolling(window=1400, min_periods=1).mean()

    df_master_price.to_csv("data_price_level.csv", index=False)
    print("✅ data_price_level.csv berhasil diperbarui.")
    print(df_master_price.tail(3).to_string(index=False))

# ==========================================
# 2. PIPELINE: MOMENTUM & P/L
# ==========================================
print("\n[2/9] Menarik data Momentum & P/L...")
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
    df_master_mom['date'] = pd.to_datetime(df_master_mom['date'])
    df_master_mom = df_master_mom.sort_values('date').reset_index(drop=True)
    df_master_mom.to_csv("data_momentum.csv", index=False)
    print("✅ data_momentum.csv berhasil diperbarui.")
    print(df_master_mom[['date', 'btc_price', 'sth_pl_ratio', 'lth_pl_ratio']].tail(3).to_string(index=False))

# ==========================================
# 3. PIPELINE: DERIVATIVES
# ==========================================
print("\n[3/9] Menarik data Derivatives...")
df_funding = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-funding-rates?timeframe=all", ['date', 'btc_price', 'funding_rate'])
df_oi = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-open-interest?timeframe=all", ['date', 'total_oi'])

if not df_funding.empty and not df_oi.empty:
    df_oi_clean = df_oi[['date', 'total_oi']]
    df_master_deriv = pd.merge(df_funding, df_oi_clean, on='date', how='outer')
    df_master_deriv['date'] = pd.to_datetime(df_master_deriv['date'])
    df_master_deriv = df_master_deriv.sort_values('date').reset_index(drop=True)
    df_master_deriv.to_csv("data_derivatives.csv", index=False)
    print("✅ data_derivatives.csv berhasil diperbarui.")
    print(df_master_deriv.tail(3).to_string(index=False))

# ==========================================
# 4. PIPELINE: SOCIAL SENTIMENT
# ==========================================
print("\n[4/9] Menarik data Social Sentiment...")
df_gtrend = fetch_data("https://chartinspect.com/api/charts/onchain/google-trends?timeframe=all&isProUser=false", 
                       ['date', 'btc_price', 'trend_bitcoin', 'trend_crypto', 'trend_ethereum', 'trend_nft'])
df_wiki = fetch_data("https://chartinspect.com/api/charts/onchain/wikipedia-pageviews?timeframe=all&isProUser=false", 
                     ['date', 'wiki_bitcoin', 'wiki_cryptocurrency', 'wiki_ethereum', 'wiki_blockchain'])

if not df_gtrend.empty and not df_wiki.empty:
    df_wiki_clean = df_wiki.drop(columns=['btc_price'], errors='ignore')
    df_master_sentiment = pd.merge(df_gtrend, df_wiki_clean, on='date', how='outer')
    df_master_sentiment['date'] = pd.to_datetime(df_master_sentiment['date'])
    df_master_sentiment = df_master_sentiment.sort_values('date').reset_index(drop=True)
    df_master_sentiment.to_csv("data_sentiment.csv", index=False)
    print("✅ data_sentiment.csv berhasil diperbarui.")
    print(df_master_sentiment[['date', 'trend_bitcoin', 'wiki_bitcoin']].tail(3).to_string(index=False))

# ==========================================
# 5. PIPELINE: SUPPLY DYNAMICS
# ==========================================
print("\n[5/9] Menarik data Supply Dynamics...")
df_sth_lth = fetch_data("https://chartinspect.com/api/onchain/sth-lth?timeframe=all&isProUser=false", 
                       ['date', 'btc_price', 'lth_supply_btc', 'sth_supply_btc', 'pct_lth_in_profit', 'pct_sth_in_profit', 'pct_lth_in_loss', 'pct_sth_in_loss'])
df_profit_loss = fetch_data("https://chartinspect.com/api/onchain/profit-loss?timeframe=all&isProUser=false", 
                            ['date', 'percent_btc_in_profit', 'percent_btc_in_loss'])

if not df_sth_lth.empty and not df_profit_loss.empty:
    df_profit_loss_clean = df_profit_loss[['date', 'percent_btc_in_profit', 'percent_btc_in_loss']]
    df_supply = pd.merge(df_sth_lth, df_profit_loss_clean, on='date', how='outer')
    df_supply['date'] = pd.to_datetime(df_supply['date'])
    df_supply = df_supply.sort_values('date').reset_index(drop=True)
    df_supply.to_csv("data_supply.csv", index=False)
    print("✅ data_supply.csv berhasil diperbarui.")
    print(df_supply[['date', 'lth_supply_btc', 'sth_supply_btc']].tail(3).to_string(index=False))

# ==========================================
# 6. PIPELINE: MARKET VALUATION
# ==========================================
print("\n[6/9] Menarik data Market Valuation...")
df_mvrv = fetch_data("https://chartinspect.com/api/onchain/mvrv?timeframe=all&isProUser=false", 
                     ['date', 'btc_price', 'mvrv', 'sth_mvrv', 'lth_mvrv'])

if not df_mvrv.empty:
    df_mvrv['date'] = pd.to_datetime(df_mvrv['date'])
    df_mvrv = df_mvrv.sort_values('date').reset_index(drop=True)
    df_mvrv.to_csv("data_mvrv.csv", index=False)
    print("✅ data_mvrv.csv berhasil diperbarui.")
    print(df_mvrv.tail(3).to_string(index=False))
    
# ==========================================
# 7. PIPELINE: FEAR & GREED
# ==========================================
print("\n[7/9] Menarik data Fear & Greed...")
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
print("\n[8/9] Menarik data Exchange Flow...")
df_ex = fetch_data("https://chartinspect.com/api/charts/exchange-etf/exchange-flows?timeframe=all", 
                   ['date', 'btc_price', 'total_balance', 'net_flow', 'inflow', 'outflow'])
if not df_ex.empty:
    df_ex['date'] = pd.to_datetime(df_ex['date'], format='mixed', errors='coerce').dt.tz_localize(None)
    df_ex = df_ex.sort_values('date').reset_index(drop=True)
    df_ex.to_csv("data_exchange.csv", index=False)
    print("✅ data_exchange.csv berhasil diperbarui.")
    print(df_ex[['date', 'total_balance', 'net_flow']].tail(3).to_string(index=False))

# ==========================================
# 9. PIPELINE: CUMULATIVE P/L PRICE & RATIO (INDEPENDENT)
# ==========================================
print("\n[9/9] Mengkalkulasi Cumulative P/L Price...")
try:
    df_age_raw = fetch_data("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
    
    if not df_age_raw.empty:
        # Band 3-10
        lth_prof_raw = df_age_raw[[f'band_{i}_profit_usd' for i in range(3, 11)]].sum(axis=1)
        lth_loss_raw = df_age_raw[[f'band_{i}_loss_usd' for i in range(3, 11)]].sum(axis=1)
        
        df_cum = pd.DataFrame({'date': df_age_raw['date'], 'lth_net_pl_usd': lth_prof_raw - lth_loss_raw})
        df_p = pd.read_csv("data_price_level.csv")
        df_s = pd.read_csv("data_supply.csv")
        
        df_cum['date'] = pd.to_datetime(df_cum['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
        df_p['date'] = pd.to_datetime(df_p['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        df_s['date'] = pd.to_datetime(df_s['date'], errors='coerce').dt.strftime('%Y-%m-%d')
        
        df_cum = pd.merge(df_cum, df_p[['date', 'btc_price', 'lth_cost_basis']], on='date', how='inner')
        df_cum = pd.merge(df_cum, df_s[['date', 'lth_supply_btc']], on='date', how='inner')
        df_cum = df_cum.sort_values('date').dropna(subset=['lth_cost_basis']).reset_index(drop=True)
        
        if not df_cum.empty:
            initial_lth_price = df_cum['lth_cost_basis'].iloc[0]
            df_cum['cum_net_pl'] = df_cum['lth_net_pl_usd'].cumsum()
            safe_supply = df_cum['lth_supply_btc'].replace(0, np.nan)
            
            df_cum['cum_pl_price'] = initial_lth_price + (df_cum['cum_net_pl'] / safe_supply)
            df_cum['pl_price_ratio'] = df_cum['btc_price'] / df_cum['cum_pl_price']
            
            df_cum_final = df_cum[['date', 'cum_pl_price', 'pl_price_ratio']]
            df_cum_final.to_csv("data_cum_pl.csv", index=False)
            print("✅ data_cum_pl.csv berhasil diperbarui.")
            print(df_cum_final.tail(3).to_string(index=False))
        else:
            print("❌ GAGAL: Data kosong setelah digabungkan (merge error).")
    else:
        print("❌ GAGAL: Endpoint API realized-profit-by-age tidak merespons.")
except Exception as e:
    print(f"❌ Error Sistem: {e}")

# ==========================================
# 10. PIPELINE: RHODL RATIO (NEW)
# ==========================================
print("\n[10/10] Menarik data RHODL Ratio...")
try:
    df_rhodl = fetch_data("https://chartinspect.com/api/onchain/rhodl?historical=true&timeframe=all&isProUser=false", 
                          ['date', 'btc_price', 'rhodl_ratio'])
    
    if not df_rhodl.empty:
        # Format tanggal sudah ditangani oleh fungsi fetch_data yang kita perbaiki sebelumnya
        df_rhodl = df_rhodl.sort_values('date').reset_index(drop=True)
        
        # Simpan ke file terpisah sesuai instruksi
        df_rhodl.to_csv("data_rhodl.csv", index=False)
        print("✅ data_rhodl.csv berhasil diperbarui.")
        print(df_rhodl[['date', 'btc_price', 'rhodl_ratio']].tail(3).to_string(index=False))
    else:
        print("❌ GAGAL: Endpoint API RHODL tidak merespons atau kosong.")
except Exception as e:
    print(f"❌ Error Sistem (RHODL): {e}")

print("\n🎉 Semua proses selesai! CSV tersimpan rapi.")

