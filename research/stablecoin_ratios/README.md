# Stablecoin Ratios — SSR & Exchange Ratio (catatan kerja 22–23 Sep 2026)

Semua riset, data, dan keputusan untuk dua halaman kelompok **Liquidity**. Tujuannya: kalau nanti
mau di-upgrade, bisa langsung lanjut dari sini tanpa mengulang.

## Isi folder

| File | Isi |
|---|---|
| `build_stablecoin_history.py` | Membangun sejarah supply stablecoin 1 Des 2017 – 15 Feb 2021 dari blockchain → baris `sumber=onchain` di `data_stablecoin_supply.csv` |
| `build_binance_peg_backing.py` | Riwayat harian dompet jaminan Binance-Peg sejak 2023 → kolom `binance_peg_backing_usd` di `data_exchange_reserves.csv` |
| `scripts/fetch_defillama_cex.py` | Tarik riwayat token semua bursa di DefiLlama CEX (dipakai untuk memilih 19 bursa) |
| `scripts/dune_query.py` + `dune_cex_label_coverage.sql` | Jalankan query Dune (key di `.env`, `DUNE_API_KEY`) — cek kelengkapan label bursa |
| `data/stablecoin_treasury_check.csv` | USDT versi blockchain vs CMC vs CoinMetrics mentah, per bulan 2017–2021 |
| `data/usdt_onchain_vs_cmc_monthly.csv` | Tabel uji yang sama dari tahap riset (kas ETH dari saldo archive akhir bulan) |
| `data/coinmetrics_splycur.csv` | CoinMetrics SplyCur (usdt per chain, usdc, dai, busd, tusd, pax) sejak 2014 |
| `data/cmc_circulating_supply.csv` | CMC circulating supply harian 2017– (USDT, USDC, DAI, BUSD, TUSD, USDP, GUSD, HUSD, sUSD) |
| `data/defillama_cex_stable_per_exchange.csv`, `..._btc_per_exchange.csv` | Stablecoin & BTC (USD) per bursa, semua bursa DefiLlama, Nov 2022 – 23 Sep 2026 |
| `data/binance_por_2026-09-01_btc_usdt_usdc_usd1.csv` | Dompet hot/cold PoR Binance 1 Sep 2026 (4 koin), dari "Download All Address" |
| `data/binance_lockinfo_2026-09-23.json` | Daftar dompet jaminan token Binance-Peg (`bapi/tokencanal/v2/tokencanal/lockinfo`) |

Data harian dashboard: `data_stablecoin_supply.csv` (Pipeline 27), `data_exchange_reserves.csv` (Pipeline 28).

---

## 1. SSR (halaman `/ssr`) — SELESAI

**Rumus (standar, bukan proksi):** market cap BTC ÷ total supply stablecoin (USD).
Market cap = harga (`data_mvrv.csv`) × supply BTC (LTH + STH, `data_supply.csv`). Tampil mulai 2018.

**Sumber supply stablecoin:**
- **1 Des 2017 – 15 Feb 2021 (dibekukan):** USDT = supply on-chain CoinMetrics (Omni + Ethereum + Tron)
  − saldo kas Tether. Non-USDT: CoinMetrics (USDC, TUSD, PAX, BUSD, DAI) s/d 3 Mar 2019, lalu DefiLlama
  (total − USDT; ikut koin kecil). Lompatan ganti non-USDT 0,28 %.
- **Sejak 16 Feb 2021:** DefiLlama total (`stablecoins.llama.fi/stablecoincharts/all`). Lompatan sambung −0,36 %.

**Kenapa bukan sumber lain:**
- DefiLlama sebelum 2021: USDT Omni hilang (awal 2019 tercatat 0,03 miliar, seharusnya ±2 miliar).
- CoinMetrics mentah: ikut menghitung USDT di kas Tether (belum beredar) — kebesaran sampai 40 % (Okt 2018).
- CMC: telat update (datar berminggu-minggu), selisih sampai 18–20 %. Endpoint situs tidak resmi.
- CoinGecko gratis: hanya 365 hari. CoinPaprika gratis: hanya 1 tahun. Wayback (arsip transparansi Tether): 429.

**Kas Tether (dicek terhadap `app.tether.to/transparency.json`, 23 Sep 2026):**

| Chain | Alamat | Cek |
|---|---|---|
| Omni | `1NTMakcgVwQpMdGxRQnFKyb3G1FAJysSfz` | saldo hitungan = `reserve_balance_omni` resmi, persis (775.616.130,15) |
| Omni | `3MbYQMMmSkC3AgWkj9FMo5LsPTW1zBTwXL` (penerbit s/d Apr 2019), `32TLn1WLcu8LtfvweLzYUYU6ubc2YV9eZs` | saldo hitungan = saldo sebenarnya |
| Tron | `TKHuVq1oKVruCGLvqVexFs6dawKv6fQgFs` | = `reserve_balance_tron` resmi, persis (1.844,9 juta) |
| Tron | `THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC` (kas awal 2019–2020, maks ±2,3 juta) | transfer palsu bernilai triliunan sejak 2022 — dibatasi s/d Feb 2021 |
| Ethereum | `0x5754284f345afc66a98fbb0a0afe71e0f007b949` | cocok dengan saldo archive di 36 akhir bulan (selisih 0) |
| Ethereum | owner kontrak `0xc6cde7c39eb2f0f0095f41570af89efc2c1ea828` | ±0,1 juta, diabaikan |

Ethereum: selisih 30 juta dengan angka `reserve_balance_eth` resmi hari itu (penyebab belum tahu, 0,02 % total).

**Hasil uji USDT versi blockchain vs CMC:** median 2,3 %, rata-rata 3,3 %, maks 18,3 % (CMC telat).
Per tahun (median / maks): 2018 2,7 / 5,0 · 2019 3,9 / 13,6 · 2020 1,9 / 19,8 · 2021 1,0 / 2,6.

**Belum terjelaskan / terbuka:**
- **±62 juta USDT (2–3 %) di 2018–2019:** versi blockchain konsisten di atas CMC. Dugaan: token dibekukan
  Tether (ada transaksi "Freeze Property Tokens" di Omni 2017–2019). Belum dipastikan → SSR 2018–2019 bisa
  terlalu rendah sampai ±3 %. Cara cek: jumlahkan saldo alamat yang di-freeze pada tanggal itu.
- Koin kecil sebelum Mar 2019 (SAI, GUSD) tidak ikut; DefiLlama mencatat non-USDT hampir 0 di masa itu.
- Keranjang beda dengan Glassnode/CryptoQuant → level absolut tidak sama; baca pakai persentil sendiri.

---

## 2. Exchange Ratio (halaman `/exchange-ratio`) — VERSI AWAL, BISA DI-UPGRADE

**Rumus (gaya CryptoQuant "Stablecoins Ratio"):** cadangan BTC di bursa (USD) ÷ cadangan stablecoin di bursa (USD).
Mulai **1 Jan 2023** (opsi A, pilihan user 23 Sep 2026).

**Sumber:** DefiLlama CEX Transparency (`api.llama.fi/protocol/<slug>`, field `tokensInUsd`), 19 bursa dikunci
(ada sejak 2022): binance-cex, okx, bitfinex, bybit, crypto-com, htx, kucoin, deribit, gate, bitget, bitmex,
swissborg, korbit, phemex, woo-x, bake.io, coinsquare, nbx, voyager. BTC = BTC/WBTC/CBBTC/BTCB. Stablecoin =
simbol peggedUSD DefiLlama + awalan USDT/USDC (USDT0, AVALANCHEUSDC, USDT.E, …).

**Koreksi Binance-Peg (terbukti):** adapter DefiLlama Binance juga menghitung dompet jaminan token Binance-Peg
(milik pemegang token di luar Binance, tidak ada di PoR). Pada PoR 1 Sep 2026 (blok 25878704):
selisih USDT Ethereum 9,18 miliar = saldo `0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503` (9,185 miliar);
selisih USDC 1,58 miliar = saldo `0xffa69c0080582098af595156240214b742735a5e` (1,583 miliar).
Jan 2023 dompet itu berisi BUSD 5,33 + USDT 1,25 + USDC 0,88 miliar. Dikurangkan harian (kolom
`stable_reserve_raw_usd` − `binance_peg_backing_usd` = `stable_reserve_usd`).

**Verifikasi Binance vs PoR resmi 1 Sep 2026:**

| Aset | DefiLlama | PoR | Catatan |
|---|---|---|---|
| BTC asli | 641.226 | 640.617 | +0,1 % — cocok. PoR juga menghitung BTCB di BSC 40.657 + BTC di ETH 2.174 (DefiLlama tidak, supaya tidak dobel) |
| USDT | 41,10 miliar | 33,25 miliar | sesudah koreksi Peg cocok, kecuali USDT di BNB Chain 1,19 miliar (PoR ada, DefiLlama tidak) |
| USDC | 8,55 miliar | 7,99 miliar | idem; USDC di BNB Chain 0,77 miliar |
| USDT/USDC Tron & Solana | = PoR | | cocok persis |

**Keterbatasan (masih salah / belum bagus):**
1. **Coinbase, Upbit, Bithumb, bitFlyer, Coincheck, Coinone, BTCC, Deepcoin tidak ada** (tanpa data dompet di
   DefiLlama). 19 bursa ±1,16 juta BTC vs ChartInspect `total_balance` 3,41 juta BTC → ±2/3 tidak tercakup.
   Level TIDAK sebanding dengan CryptoQuant; halaman untuk membedah bentuk.
2. Stablecoin Binance di BNB Chain (±2,4 miliar, ±7 % stablecoin Binance) tidak ikut.
3. 18 bursa selain Binance belum diverifikasi terhadap PoR masing-masing.
4. **7 lompatan harian rasio > 10 % bukan dari harga** (koreksi Peg tidak berubah di hari itu), penyebab belum
   tahu (dugaan: dompet ditambah/dicabut di DefiLlama, atau beda jam harga):
   16 Feb 2023 (BTC cadangan +11,9 %), 18 Mar 2023 (BTC +11,4 %), 15 Apr 2023 (stablecoin −10,7 %),
   24 Okt 2023 (BTC +11,8 %), 12 Nov 2024 (BTC +9,5 %), 1 Des 2025 (stablecoin +13,3 %), 6 Feb 2026
   (BTC −13,4 % padahal harga +12,3 %). Cara cek: bandingkan per bursa di `data/defillama_cex_*_per_exchange.csv`.

**Pilihan tanggal mulai (dibahas 23 Sep 2026; dipilih A):**

| | A. 1 Jan 2023 (dipakai) | B. 16 Nov 2022, bursa masuk bertahap | C. 16 Nov 2022, hanya 7 bursa awal |
|---|---|---|---|
| Bottom FTX Nov–Des 2022 | tidak terlihat | terlihat | terlihat |
| Lompatan palsu | tidak ada | 12 lompatan 18 Nov–23 Des 2022: stablecoin +7,6 %, BTC +14 % (HTX BTC +5,2 %, BitMEX +3,2 %, KuCoin stable +3,0 %) | tidak ada |
| Porsi bursa hilang | 0 % | 0 % sesudah 23 Des 2022 | stable 8,1 % / BTC 12,2 % (Jan 2023) → 4,7 % / 7,8 % (Sep 2026); bergeser sepanjang grafik |

7 bursa awal (C): binance-cex, okx, bitfinex, bybit, crypto-com, deribit, voyager.
Sebelum Nov 2022: tidak ada daftar dompet resmi (PoR baru muncul sesudah FTX) → tidak bisa dengan data gratis.

**Jalur upgrade yang sudah dicek:**
- **Dune (akun gratis, key di `.env`):** label `cex.addresses` terlalu tipis untuk sisi BTC — Coinbase 13
  alamat BTC, Upbit 1, Bithumb 0; Tron tanpa label Coinbase/Upbit/Bithumb. Hasil lengkap: jalankan
  `scripts/dune_query.py scripts/dune_cex_label_coverage.sql`. Kesimpulan 23 Sep 2026: tidak bisa melengkapi.
- **ChartInspect `exchange-flows`:** hanya BTC gabungan (tanpa rincian bursa, tanpa stablecoin) → tidak bisa
  dipasangkan dengan stablecoin dari daftar bursa yang sama.
- **CryptoQuant API:** punya metrik ini per bursa sejak 2017 termasuk Coinbase; kemungkinan berbayar, harga
  belum dicek. Kandidat utama kalau mau level yang sebanding.
- **Binance BNB Chain:** riwayat saldo stablecoin dompet PoR di BSC — belum dicari sumbernya.
- **PoR bursa lain** (OKX, Bybit, dll. menerbitkan laporan bulanan) — bisa dipakai verifikasi seperti Binance.

---

## Jebakan teknis (API gratis)

- Wayback Machine CDX cepat memblokir (429) dan lama pulih.
- Blockscout `eth.blockscout.com/api` sering "Too many requests".
- `eth.drpc.org`: `eth_call` archive jalan, `eth_getLogs` ditolak ("ranges over 10000 blocks…" walau rentang kecil).
  **Tenderly publik `gateway.tenderly.co/public/mainnet`**: `eth_getLogs` rentang 100k blok & `eth_call` historis jalan.
  publicnode / ankr / 1rpc / blastapi / flashbots: archive atau log dibatasi.
- Omni Explorer (`api.omniexplorer.info`): pagination bergeser saat transaksi baru masuk → buang `txid` dobel; transaksi
  Freeze/Change Issuer tidak punya `amount`; endpoint kadang tidak mengirim `transactions` (ulangi).
- TronGrid: kadang tidak mengirim `data` (ulangi); ada transfer palsu bernilai ±1e22–1e71 sejak 2022; cetak USDT Tron
  tercatat sebagai transfer dari `T9yD14Nj9j7xAB4dbGeiX9h8unkKHxuWwb` (alamat nol).
- DefiLlama `api.llama.fi/protocol/binance-cex` ±42 MB; beberapa entri `/cexs` tanpa `slug` (Coinbase dkk.).
  Membaca JSON besar di Windows: buka dengan `encoding='utf-8'`.
- CMC `api.coinmarketcap.com/data-api/v3/cryptocurrency/historical`: rentang panjang otomatis disampel (±731 titik) →
  tarik per 360 hari.
- Halaman PoR Binance diblokir untuk curl & panel browser Claude; user membuka sendiri dan mengunduh "Download All Address".
- Membuka situs luar di tab panel browser yang sama dengan localhost diduga mematikan server `dashboard-v2-uji`
  (23 Sep 2026) — buka situs luar di tab terpisah.

## Menjalankan ulang

```bash
python research/stablecoin_ratios/build_stablecoin_history.py
python research/stablecoin_ratios/build_binance_peg_backing.py
```
Keduanya menulis ulang file data dari awal; sesudahnya jalankan Pipeline 27/28 (`auto_update.py`) untuk bagian harian.
