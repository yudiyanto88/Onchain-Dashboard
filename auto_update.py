import requests
import pandas as pd
from datetime import datetime

print(f"[{datetime.now()}] Memulai proses penarikan data On-Chain Price Levels...")

# Gunakan timeframe=all agar filter di dasbor bekerja maksimal
url_price_levels = "https://chartinspect.com/api/onchain/onchain-price-levels?timeframe=all&isProUser=false"
url_tmm = "https://chartinspect.com/api/onchain/true-market-mean?timeframe=all&isProUser=false"

try:
    # 1. Tarik Data Base Price Levels
    print("Mengunduh data Price Levels...")
    res1 = requests.get(url_price_levels)
    data1 = res1.json().get('data', [])
    df1 = pd.DataFrame(data1)
    # Ambil kolom yang diperlukan saja
    df1 = df1[['date', 'btc_price', 'sth_cost_basis', 'lth_cost_basis', 'realized_price', 'cvdd']]
    
    # 2. Tarik Data True Market Mean
    print("Mengunduh data True Market Mean...")
    res2 = requests.get(url_tmm)
    data2 = res2.json().get('data', [])
    df2 = pd.DataFrame(data2)
    # Ambil tanggal dan nilai TMM saja (hindari duplikasi btc_price)
    df2 = df2[['date', 'true_market_mean_price']]
    
    # 3. Jahit Data (Merge) berdasarkan Tanggal
    print("Merapikan dan menggabungkan data...")
    df_master = pd.merge(df1, df2, on='date', how='outer')
    
    # Urutkan berdasarkan tanggal dan simpan ke CSV
    df_master['date'] = pd.to_datetime(df_master['date'])
    df_master = df_master.sort_values('date')
    df_master.to_csv("data_price_level.csv", index=False)
    
    print("Sukses! Data berhasil diperbarui dan disimpan di: data_price_level.csv")

except Exception as e:
    print(f"Terjadi kesalahan saat menjalankan automasi: {e}")
