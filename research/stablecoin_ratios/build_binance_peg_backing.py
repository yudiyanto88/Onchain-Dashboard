"""
Riwayat harian stablecoin di dompet jaminan token Binance-Peg (Ethereum), sejak 1 Jan 2023.

Kenapa: DefiLlama (CEX Transparency, adapter binance) ikut menghitung dompet yang menyimpan jaminan
token Binance-Peg (mis. USDT versi BNB Chain). Isinya milik pemegang token di luar Binance, bukan
cadangan bursa, dan tidak ada di Proof of Reserves Binance. Dicek 23 Sep 2026 terhadap PoR 1 Sep 2026
(blok 25878704): selisih USDT Ethereum DefiLlama - PoR = 9,18 miliar = saldo 0x47ac...d503 (9,185 miliar);
selisih USDC = 1,58 miliar = saldo 0xffa6...5a5e (1,583 miliar). BTC asli DefiLlama = PoR (+0,1 %).

Dompet dari https://www.binance.com/bapi/tokencanal/v2/tokencanal/lockinfo (sumber yang sama dengan
DefiLlama). Saldo awal = eth_call balanceOf di blok awal, lalu ditambah event Transfer (Tenderly publik).
Menulis kolom binance_peg_backing_usd ke data_exchange_reserves.csv; Pipeline 28 auto_update.py
melengkapi kolom lain dan menambah nilai harian berikutnya.
Jalankan dari akar repo: python research/stablecoin_ratios/build_binance_peg_backing.py (±5-10 menit).
"""
import time
import numpy as np
import pandas as pd
import requests

RPC = 'https://gateway.tenderly.co/public/mainnet'
DOMPET = ['0x47ac0fb4f2d84898e4d9e7b4dab3c24507a6d503', '0xffa69c0080582098af595156240214b742735a5e']
TOKEN = {  # stablecoin yang pernah ada di dompet jaminan (desimal)
    'USDT': ('0xdac17f958d2ee523a2206206994597c13d831ec7', 6),
    'USDC': ('0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48', 6),
    'BUSD': ('0x4fabb145d64652a948d72533023f6e7a623c7c53', 18),
    'DAI': ('0x6b175474e89094c44da98b954eedeac495271d0f', 18),
    'TUSD': ('0x0000000000085d4780b73119b644ae5ecd22b376', 18),
    'USDP': ('0x8e870d67f660d95d5be530380d0ec0bd388289e1', 18),
}
TR = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
MULAI, LANGKAH = 16_308_190, 100_000  # blok 1 Jan 2023


def rpc(method, params):
    for _ in range(10):
        try:
            r = requests.post(RPC, json={'jsonrpc': '2.0', 'id': 1, 'method': method, 'params': params}, timeout=90).json()
            if 'result' in r:
                return r['result']
        except Exception:
            pass
        time.sleep(5)
    raise RuntimeError(r)


akhir = int(rpc('eth_blockNumber', []), 16)
jangkar = {b: int(rpc('eth_getBlockByNumber', [hex(b), False])['timestamp'], 16)
           for b in list(range(MULAI, akhir, LANGKAH)) + [akhir]}
kb = sorted(jangkar)
hari = pd.date_range('2023-01-01', pd.to_datetime(jangkar[akhir], unit='s').normalize(), freq='D')

total = pd.Series(0.0, index=hari)
for sim, (tok, dec) in TOKEN.items():
    for d in DOMPET:
        awal = int(rpc('eth_call', [{'to': tok, 'data': '0x70a08231' + d[2:].rjust(64, '0')}, hex(MULAI)]), 16) / 10**dec
        k = '0x' + d[2:].rjust(64, '0')
        rows = []
        for a in range(MULAI + 1, akhir + 1, LANGKAH):
            b = min(a + LANGKAH - 1, akhir)
            for topik, tanda in (([TR, None, k], 1), ([TR, k], -1)):
                for l in rpc('eth_getLogs', [{'address': tok, 'fromBlock': hex(a), 'toBlock': hex(b), 'topics': topik}]):
                    rows.append((int(l['blockNumber'], 16), l['transactionHash'], int(l['logIndex'], 16),
                                 tanda * int(l['data'], 16) / 10**dec))
        e = pd.DataFrame(rows, columns=['blok', 'hash', 'log', 'delta']).drop_duplicates()
        s = pd.Series(awal, index=hari)
        if len(e):
            e['t'] = pd.to_datetime(np.interp(e.blok, kb, [jangkar[x] for x in kb]), unit='s').normalize()
            s = s + e.groupby('t').delta.sum().reindex(hari).fillna(0).cumsum()
        # cek: saldo hitungan hari ini = balanceOf sekarang
        kini = int(rpc('eth_call', [{'to': tok, 'data': '0x70a08231' + d[2:].rjust(64, '0')}, 'latest']), 16) / 10**dec
        print(f"{sim:5s} {d[:6]} awal {awal/1e6:9.1f} juta | hitung akhir {s.iloc[-1]/1e6:9.1f} | sebenarnya {kini/1e6:9.1f} "
              f"| transfer {len(e)}", flush=True)
        total += s

out = pd.DataFrame({'date': hari.strftime('%Y-%m-%d'), 'binance_peg_backing_usd': total.round().astype('int64')})
out.to_csv('data_exchange_reserves.csv', index=False)
print(out.iloc[[0, len(out) // 2, -1]].to_string(index=False))
