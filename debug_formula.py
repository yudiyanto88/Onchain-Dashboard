import pandas as pd
import numpy as np
import requests

r = requests.get("https://chartinspect.com/api/onchain/realized-profit-by-age?timeframe=all&isProUser=false")
df = pd.DataFrame(r.json()['data'])
df['date'] = pd.to_datetime(df['date'], utc=True, errors='coerce').dt.strftime('%Y-%m-%d')
df = df.sort_values('date').reset_index(drop=True)

lth_net = (
    df[[f'band_{i}_profit_usd' for i in range(5, 12)]].sum(axis=1) -
    df[[f'band_{i}_loss_usd' for i in range(5, 12)]].sum(axis=1)
)
df['cum_net_pl'] = lth_net.cumsum()

# Print nilai harian di tahun 2010-2014 untuk deteksi anomali
early = df[df['date'] <= '2014-01-01'][['date', 'cum_net_pl']].copy()
early['daily_net_pl'] = lth_net[early.index]
print(early[['date', 'daily_net_pl', 'cum_net_pl']].to_string())
