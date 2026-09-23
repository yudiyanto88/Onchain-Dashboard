"""
Sejarah total supply stablecoin (USD) 1 Des 2017 - 15 Feb 2021 untuk halaman SSR, dari blockchain.

Kenapa tidak DefiLlama saja: sebelum 2021 DefiLlama belum melacak USDT di Omni (awal 2019 tercatat
0,03 miliar, seharusnya ~2 miliar). Kenapa tidak CoinMetrics mentah: SplyCur ikut menghitung USDT
yang masih disimpan kas Tether (belum beredar), kebesaran sampai 40 % (Okt 2018). CMC telat
memperbarui (datar berminggu-minggu, selisih sampai 19,8 %).

Rumus: USDT beredar = supply on-chain CoinMetrics (Omni + Ethereum + Tron) - saldo kas Tether.
Kas Tether (dicek 23 Sep 2026 terhadap app.tether.to/transparency.json):
  Omni    1NTMakcg... (= reserve_balance_omni resmi, persis), 3MbYQMMm... (penerbit s/d Apr 2019),
          32TLn1WL... (penerbit sesudahnya)          -> disusun dari semua transaksi Omni Explorer
  Tron    TKHuVq1o... (= reserve_balance_tron resmi, persis), THPvaUho... (kas awal 2019-2020)
          -> disusun dari transfer TRC20 TronGrid (cetak USDT Tron = transfer dari alamat nol)
  Ethereum 0x5754284f... -> event Transfer lewat eth_getLogs (Tenderly publik); cocok dengan saldo
          archive RPC di 36 akhir bulan (selisih 0). Saldo owner kontrak (0xc6cd..., ~0,1 juta,
          <0,01 % total) diabaikan.
Non-USDT: CoinMetrics USDC+TUSD+PAX+BUSD+DAI sampai hari pertama (>= Mar 2019) DefiLlama
(total - USDT) menyamai/melebihinya, lalu DefiLlama (ikut menghitung koin kecil). Lompatan 0,28 %.
Sesudah 15 Feb 2021 Pipeline 27 auto_update.py memakai DefiLlama total (lompatan sambung -1,2 %).

Ketidakpastian yang tersisa: versi blockchain konsisten ~62 juta (2-3 %) di atas CMC pada
2018-2019; dugaan token dibekukan Tether (transaksi Freeze di Omni), belum dipastikan.

Jalankan dari akar repo: python research/stablecoin_ratios/build_stablecoin_history.py (±20-40 menit, API publik
dengan batas permintaan). Menulis data_stablecoin_supply.csv (baris < 2021-02-16) dan
research/stablecoin_ratios/data/stablecoin_treasury_check.csv (bandingan bulanan dengan CMC).
"""
import time, json
import numpy as np
import pandas as pd
import requests

SAMBUNG = pd.Timestamp('2021-02-16')
HARI = pd.date_range('2017-12-01', SAMBUNG - pd.Timedelta(days=1), freq='D')


def minta(fn, cek, coba=10, jeda=10):
    for _ in range(coba):
        try:
            r = fn()
            if cek(r):
                return r
        except Exception:
            pass
        time.sleep(jeda)
    raise RuntimeError("permintaan gagal terus")


def saldo_harian(df):
    """df kolom t, delta -> saldo akhir hari, diisi ke HARI."""
    s = df.sort_values('t').set_index('t').delta.cumsum()
    s = s.groupby(s.index.normalize()).last()
    return s.reindex(s.index.union(HARI)).ffill().reindex(HARI).fillna(0)


# ---------- CoinMetrics: supply on-chain ----------
def coinmetrics(aset):
    rows, url = [], "https://community-api.coinmetrics.io/v4/timeseries/asset-metrics"
    p = {'assets': aset, 'metrics': 'SplyCur', 'frequency': '1d', 'page_size': 10000,
         'start_time': '2017-11-01', 'end_time': '2021-03-01'}
    while url:
        j = minta(lambda: requests.get(url, params=p, timeout=90).json(), lambda j: 'data' in j)
        rows += j['data']; url = j.get('next_page_url'); p = None
    d = pd.DataFrame(rows)
    s = pd.Series(d.SplyCur.astype(float).values, index=pd.to_datetime(d.time).dt.tz_localize(None).dt.normalize())
    return s.reindex(s.index.union(HARI)).ffill().reindex(HARI).fillna(0)

cm = {a: coinmetrics(a) for a in ['usdt_omni', 'usdt_eth', 'usdt_trx', 'usdc', 'tusd', 'pax', 'busd', 'dai']}
print("CoinMetrics selesai", flush=True)


# ---------- Kas Tether di Omni ----------
def omni(addr):
    tx, pg = {}, 0
    while True:
        d = minta(lambda: requests.post('https://api.omniexplorer.info/v1/transaction/address',
                                        data={'addr': addr, 'page': pg}, timeout=60).json(),
                  lambda d: 'transactions' in d, jeda=15)
        for x in d['transactions']:
            tx[x['txid']] = x  # halaman bisa bergeser saat transaksi baru masuk -> buang dobel
        pg += 1
        if pg >= d['pages']:
            break
        time.sleep(2)
    rows = []
    for x in tx.values():
        if not x.get('valid') or str(x.get('propertyid')) != '31' or 'amount' not in x:
            continue  # Freeze/Change Issuer tanpa jumlah
        a = float(x['amount'])
        if x['type'] == 'Grant Property Tokens':
            dd = a if x.get('referenceaddress') in (None, '', addr) else 0
        elif x['type'] == 'Revoke Property Tokens':
            dd = -a
        else:
            dd = (a if x.get('referenceaddress') == addr else 0) - (a if x.get('sendingaddress') == addr else 0)
        rows.append((pd.to_datetime(x['blocktime'], unit='s'), dd))
    return saldo_harian(pd.DataFrame(rows, columns=['t', 'delta']))

kas = {f'omni_{a[:6]}': omni(a) for a in ['1NTMakcgVwQpMdGxRQnFKyb3G1FAJysSfz',
                                          '3MbYQMMmSkC3AgWkj9FMo5LsPTW1zBTwXL',
                                          '32TLn1WLcu8LtfvweLzYUYU6ubc2YV9eZs']}
print("Omni selesai", flush=True)


# ---------- Kas Tether di Tron ----------
def tron(addr):
    url = f'https://api.trongrid.io/v1/accounts/{addr}/transactions/trc20'
    p = {'contract_address': 'TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t', 'limit': 200, 'order_by': 'block_timestamp,asc',
         'max_timestamp': int(SAMBUNG.timestamp() * 1000)}
    rows = {}
    while url:
        d = minta(lambda: requests.get(url, params=p, timeout=60).json(), lambda d: 'data' in d)
        p = None
        for t in d['data']:
            v = int(t['value']) / 1e6
            rows[t['transaction_id']] = (pd.to_datetime(t['block_timestamp'], unit='ms'),
                                         (v if t['to'] == addr else 0) - (v if t['from'] == addr else 0))
        url = d.get('meta', {}).get('links', {}).get('next')
        time.sleep(0.4)
    return saldo_harian(pd.DataFrame(list(rows.values()), columns=['t', 'delta']))

kas.update({f'tron_{a[:6]}': tron(a) for a in ['TKHuVq1oKVruCGLvqVexFs6dawKv6fQgFs', 'THPvaUhoh2Qn2y9THCZML3H815hhFhn5YC']})
print("Tron selesai", flush=True)


# ---------- Kas Tether di Ethereum ----------
RPC = 'https://gateway.tenderly.co/public/mainnet'
USDT = '0xdac17f958d2ee523a2206206994597c13d831ec7'
TR = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
K = '0x' + '5754284f345afc66a98fbb0a0afe71e0f007b949'.rjust(64, '0')

def rpc(method, params):
    return minta(lambda: requests.post(RPC, json={'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params},
                                       timeout=90).json(), lambda r: 'result' in r, jeda=5)['result']

MULAI, AKHIR, LANGKAH = 5_900_000, 11_900_000, 100_000  # Jul 2018 (kas masih kosong) .. Feb 2021
rows, jangkar = [], {}
for a in range(MULAI, AKHIR + 1, LANGKAH):
    b = min(a + LANGKAH - 1, AKHIR)
    jangkar[a] = int(rpc('eth_getBlockByNumber', [hex(a), False])['timestamp'], 16)
    for topik, tanda in (([TR, None, K], 1), ([TR, K], -1)):
        for l in rpc('eth_getLogs', [{'address': USDT, 'fromBlock': hex(a), 'toBlock': hex(b), 'topics': topik}]):
            rows.append((int(l['blockNumber'], 16), l['transactionHash'], int(l['logIndex'], 16), tanda * int(l['data'], 16) / 1e6))
jangkar[AKHIR] = int(rpc('eth_getBlockByNumber', [hex(AKHIR), False])['timestamp'], 16)
e = pd.DataFrame(rows, columns=['blok', 'hash', 'log', 'delta']).drop_duplicates(['hash', 'log', 'delta'])
# waktu blok diinterpolasi antar jangkar tiap 100k blok (meleset paling beberapa menit)
kb = sorted(jangkar)
e['t'] = pd.to_datetime(np.interp(e.blok, kb, [jangkar[k] for k in kb]), unit='s')
kas['eth_0x5754'] = saldo_harian(e[['t', 'delta']])
print("Ethereum selesai", flush=True)


# ---------- Rakit ----------
usdt = cm['usdt_omni'] + cm['usdt_eth'] + cm['usdt_trx'] - sum(kas.values())
def dl(q=''):
    j = minta(lambda: requests.get(f"https://stablecoins.llama.fi/stablecoincharts/all{q}", timeout=90).json(),
              lambda j: isinstance(j, list))
    s = pd.Series({pd.to_datetime(int(x['date']), unit='s').normalize(): x.get('totalCirculatingUSD', {}).get('peggedUSD')
                   for x in j}, dtype=float)
    return s.reindex(HARI)
cm5 = cm['usdc'] + cm['tusd'] + cm['pax'] + cm['busd'] + cm['dai']
dl_non = dl() - dl('?stablecoin=1')
ganti = dl_non[(dl_non >= cm5) & (HARI >= '2019-03-01')].index[0]
non = cm5.where(HARI < ganti, dl_non)
total = (usdt + non).round()
print("non-USDT pindah ke DefiLlama:", ganti.date())

out = pd.DataFrame({'date': HARI.strftime('%Y-%m-%d'), 'stablecoin_supply_usd': total.astype('int64'), 'sumber': 'onchain'})
out.to_csv("data_stablecoin_supply.csv", index=False)
print("data_stablecoin_supply.csv:", len(out), "baris,", out.date.iloc[0], "->", out.date.iloc[-1])

# Bandingan bulanan dengan CMC (circulating supply USDT; API situs CMC tanpa key, tidak resmi)
def cmc(t0, t1):
    j = minta(lambda: requests.get("https://api.coinmarketcap.com/data-api/v3/cryptocurrency/historical",
                                   params={'id': 825, 'convertId': 2781, 'timeStart': t0, 'timeEnd': t1, 'interval': '1d'},
                                   headers={'User-Agent': 'Mozilla/5.0'}, timeout=60).json(), lambda j: 'data' in j)
    return pd.Series({pd.Timestamp(q['timeClose'][:10]): q['quote'].get('circulatingSupply') for q in j['data']['quotes']})
awal = int(HARI[0].timestamp())
c = pd.concat([cmc(t, t + 360 * 86400) for t in range(awal, int(SAMBUNG.timestamp()), 360 * 86400)])
c = c[~c.index.duplicated()].replace(0, np.nan).reindex(HARI)
m = pd.DataFrame({'usdt_onchain': usdt, 'usdt_cmc': c, 'kas_tether': sum(kas.values()),
                  'usdt_coinmetrics_mentah': cm['usdt_omni'] + cm['usdt_eth'] + cm['usdt_trx']}).resample('ME').last()
m['cmc_vs_onchain_pct'] = (m.usdt_cmc / m.usdt_onchain - 1) * 100
m['coinmetrics_kebesaran_pct'] = (m.usdt_coinmetrics_mentah / m.usdt_onchain - 1) * 100
m.round(2).to_csv("research/stablecoin_ratios/data/stablecoin_treasury_check.csv")
print(m[['cmc_vs_onchain_pct', 'coinmetrics_kebesaran_pct']].abs().describe().round(2).to_string())
