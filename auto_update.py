import requests
import pandas as pd
from datetime import datetime
import numpy as np

print(f"[{datetime.now()}] Memulai proses automasi On-Chain Data...")

def fetch_data(url, columns_to_keep=None):
    try:
        res = requests.get(url)
        data = res.json().get('data', [])
        df = pd.DataFrame(data)
        if columns_to_keep and not df.empty:
            df = df[[col for col in columns_to_keep if col in df.columns]]
        return df
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return pd.DataFrame()

# ==========================================
# 1. PIPELINE: PRICE LEVELS
# ==========================================
print("Menarik data Price Levels...")
df_price = fetch_data("https://chartinspect.com/api/onchain/onchain-price-levels?timeframe=all&isProUser=false", ['date', 'btc_price', 'sth_cost_basis', 'lth_cost_basis', 'realized_price', 'cvdd'])
df_tmm = fetch_data("https://chartinspect.com/api/onchain/true-market-mean?timeframe=all&isProUser=false", ['date', 'true_market_mean_price'])

if not df_price.empty and not df_tmm.empty:
    df_master_price = pd.merge(df_price, df_tmm, on='date', how='outer')
    df_master_price['date'] = pd.to_datetime(df_master_price['date'])
    df_master_price.sort_values('date').to_csv("data_price_level.csv", index=False)
    print("✅ data_price_level.csv berhasil diperbarui.")

# ==========================================
# 2. PIPELINE: MOMENTUM
# ==========================================
print("Menarik data Momentum...")
df_sopr = fetch_data("https://chartinspect.com/api/onchain/sopr?timeframe=all&isProUser=false", ['date', 'btc_price', 'asopr'])
df_lth_sopr = fetch_data("https://chartinspect.com/api/onchain/lth-sopr?timeframe=all&isProUser=false", ['date', 'lth_sopr'])
df_sth_sopr = fetch_data("https://chartinspect.com/api/onchain/sth-sopr?timeframe=all&isProUser=false", ['date', 'sth_sopr'])
df_net_pl = fetch_data("https://chartinspect.com/api/onchain/net-realized-pl?timeframe=all&isProUser=false", ['date', 'net_realized_pl_usd'])
df_age = fetch_data("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")

if not df_age.empty:
    sth_prof = df_age[[f'band_{i}_profit_usd' for i in range(5)]].sum(axis=1)
    sth_loss = df_age[[f'band_{i}_loss_usd' for i in range(5)]].sum(axis=1)
    df_age['sth_pl_ratio'] = np.where(sth_loss == 0, np.nan, sth_prof / sth_loss)

    lth_prof = df_age[[f'band_{i}_profit_usd' for i in range(5, 12)]].sum(axis=1)
    lth_loss = df_age[[f'band_{i}_loss_usd' for i in range(5, 12)]].sum(axis=1)
    df_age['lth_pl_ratio'] = np.where(lth_loss == 0, np.nan, lth_prof / lth_loss)
    
    df_age_clean = df_age[['date', 'sth_pl_ratio', 'lth_pl_ratio']]
else:
    df_age_clean = pd.DataFrame(columns=['date', 'sth_pl_ratio', 'lth_pl_ratio'])

dfs = [df_sopr, df_lth_sopr, df_sth_sopr, df_net_pl, df_age_clean]
df_master_mom = dfs[0]
for d in dfs[1:]:
    if not d.empty:
        df_master_mom = pd.merge(df_master_mom, d, on='date', how='outer')

if not df_master_mom.empty:
    df_master_mom['date'] = pd.to_datetime(df_master_mom['date'])
    df_master_mom.sort_values('date').to_csv("data_momentum.csv", index=False)
    print("✅ data_momentum.csv berhasil diperbarui.")

# ==========================================
# 3. PIPELINE: DERIVATIVES
# ==========================================
print("Menarik data Derivatives...")
df_funding = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-funding-rates?timeframe=all", ['date', 'btc_price', 'funding_rate'])
df_oi = fetch_data("https://chartinspect.com/api/charts/derivatives/futures-open-interest?timeframe=all", ['date', 'total_oi'])

if not df_funding.empty and not df_oi.empty:
    # Memisahkan btc_price agar tidak berbenturan saat merge
    df_oi_clean = df_oi[['date', 'total_oi']]
    df_master_deriv = pd.merge(df_funding, df_oi_clean, on='date', how='outer')
    df_master_deriv['date'] = pd.to_datetime(df_master_deriv['date'])
    df_master_deriv.sort_values('date').to_csv("data_derivatives.csv", index=False)
    print("✅ data_derivatives.csv berhasil diperbarui.")

# ==========================================
# 4. PIPELINE: SOCIAL SENTIMENT
# ==========================================
print("Menarik data Social Sentiment...")
df_gtrend = fetch_data("https://chartinspect.com/api/charts/onchain/google-trends?timeframe=all&isProUser=false", ['date', 'btc_price', 'trend_bitcoin', 'trend_crypto'])
df_wiki = fetch_data("https://chartinspect.com/api/charts/onchain/wikipedia-pageviews?timeframe=all&isProUser=false", ['date', 'wiki_bitcoin', 'wiki_cryptocurrency'])

if not df_gtrend.empty and not df_wiki.empty:
    df_wiki_clean = df_wiki[['date', 'wiki_bitcoin', 'wiki_cryptocurrency']]
    df_master_sentiment = pd.merge(df_gtrend, df_wiki_clean, on='date', how='outer')
    df_master_sentiment['date'] = pd.to_datetime(df_master_sentiment['date'])
    df_master_sentiment.sort_values('date').to_csv("data_sentiment.csv", index=False)
    print("✅ data_sentiment.csv berhasil diperbarui.")

print("Semua proses selesai!")
