"""Versi exchange (gaya CryptoQuant): cadangan BTC di bursa (USD) / cadangan stablecoin di bursa (USD).
Sumber: DefiLlama CEX Transparency (alamat dompet yang dipublikasikan bursa), sejak Nov 2022."""
import requests, json, time, pandas as pd

STABLE = {'USDT', 'USDC', 'FDUSD', 'TUSD', 'BUSD', 'DAI', 'USDE', 'USD1', 'USDP', 'PYUSD', 'FDUSD', 'USDS', 'RLUSD', 'GUSD'}
BTC = {'BTC', 'BTCB', 'WBTC', 'CBBTC'}
cexs = requests.get("https://api.llama.fi/cexs", timeout=60).json()['cexs']
print("jumlah CEX:", len(cexs), flush=True)
st, bt, ringkas = {}, {}, []
for c in cexs:
    if not c.get('slug'):
        print('  tanpa slug:', c.get('name'), flush=True); continue
    slug = c['slug'].lower()
    try:
        r = requests.get(f"https://api.llama.fi/protocol/{slug}", timeout=300)
        j = json.loads(r.content.decode('utf-8'))
    except Exception as e:
        print("  gagal", slug, e, flush=True); continue
    t = j.get('tokensInUsd') or []
    if not t:
        continue
    s = pd.Series({pd.to_datetime(x['date'], unit='s').normalize(): sum(v for k, v in x['tokens'].items() if k.upper() in STABLE) for x in t})
    b = pd.Series({pd.to_datetime(x['date'], unit='s').normalize(): sum(v for k, v in x['tokens'].items() if k.upper() in BTC) for x in t})
    st[slug], bt[slug] = s.groupby(level=0).last(), b.groupby(level=0).last()
    ringkas.append((slug, s.index.min().date(), round(s.iloc[-1] / 1e9, 2), round(b.iloc[-1] / 1e9, 2)))
    time.sleep(0.5)
st, bt = pd.DataFrame(st).sort_index(), pd.DataFrame(bt).sort_index()
st.to_csv('cex_stable.csv'); bt.to_csv('cex_btc.csv')
print(pd.DataFrame(ringkas, columns=['cex', 'mulai', 'stable_B', 'btc_B']).sort_values('stable_B', ascending=False).head(15).to_string(index=False))
