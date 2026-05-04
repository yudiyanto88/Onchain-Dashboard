import requests
import pandas as pd
from datetime import datetime

# ==============================================================================
# SCRIPT AUTOMASI PENARIKAN DATA ON-CHAIN
# Script ini bertugas mengambil data dari API, merapikannya menjadi tabel,
# dan menyimpannya ke dalam file CSV agar bisa dibaca oleh Dashboard.
# ==============================================================================

def update_data():
    print(f"[{datetime.now()}] Memulai proses penarikan data...")

    # 1. TENTUKAN SUMBER DATA (API URL)
    # Saat ini difokuskan untuk menarik metrik STH Cost Basis & Deviation
    url_sth_cost = "https://chartinspect.com/api/onchain/chain-caps?timeframe=all&forChart=cost-basis-convergence&isProUser=false"

    try:
        # 2. MENGAMBIL DATA DARI INTERNET
        print("Mengunduh data dari API ChartInspect...")
        response = requests.get(url_sth_cost)
        response.raise_for_status() # Akan memunculkan error jika website mati/gagal
        
        json_utama = response.json()

        # 3. MENCARI LOKASI DATA UTAMA
        # Mengecek apakah data berada di dalam folder "data" atau langsung berupa array
        if "data" in json_utama:
            data_array = json_utama["data"]
        else:
            data_array = json_utama

        # Pastikan data tidak kosong
        if not data_array or len(data_array) == 0:
            print("Peringatan: Data berhasil ditarik, tetapi isinya kosong.")
            return

        # 4. MENGUBAH JSON MENJADI TABEL (DATAFRAME)
        # Pandas akan otomatis membaca header dan baris data tanpa perlu looping manual
        print("Merapikan format data menjadi tabel...")
        df = pd.DataFrame(data_array)

        # (Opsional) Memastikan kolom waktu bernama 'Date' agar seragam untuk dashboard
        # Jika API mengeluarkan nama kolom 'time' atau 't', kita ubah namanya:
        if 'time' in df.columns:
            df.rename(columns={'time': 'Date'}, inplace=True)
        elif 't' in df.columns:
            df.rename(columns={'t': 'Date'}, inplace=True)

        # 5. MENYIMPAN DATA KE FILE CSV
        nama_file_output = "Master_Onchain_Data.csv"
        df.to_csv(nama_file_output, index=False)
        print(f"Sukses! Data berhasil diperbarui dan disimpan di: {nama_file_output}")

    except Exception as e:
        print(f"Terjadi kesalahan saat memproses data: {e}")

# Baris ini memastikan script langsung berjalan saat file ini dieksekusi
if __name__ == "__main__":
    update_data()
