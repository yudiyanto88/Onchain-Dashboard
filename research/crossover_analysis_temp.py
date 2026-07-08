import pandas as pd

df = pd.read_csv('data_price_level.csv')
df['date'] = pd.to_datetime(df['date'])

mvrv_col = [c for c in df.columns if 'MVRV' in c][0]
df = df.rename(columns={mvrv_col: 'mvrv_0std'})
df = df.dropna(subset=['cum_pl_price', 'mvrv_0std'])
df = df[df['date'] >= '2015-01-01'].copy()  # skip genesis noise

df['pl_above_mvrv'] = df['cum_pl_price'] > df['mvrv_0std']
df['cross_up'] = df['pl_above_mvrv'] & ~df['pl_above_mvrv'].shift(1, fill_value=False)
df['cross_down'] = ~df['pl_above_mvrv'] & df['pl_above_mvrv'].shift(1, fill_value=False)

crossups = df[df['cross_up']][['date', 'btc_price', 'cum_pl_price', 'mvrv_0std']]
crossdowns = df[df['cross_down']][['date', 'btc_price', 'cum_pl_price', 'mvrv_0std']]

print('=== CROSS UP (cum_pl naik di atas mvrv_0std) ===')
for _, r in crossups.iterrows():
    gap = r['cum_pl_price'] - r['mvrv_0std']
    print(str(r['date'].date()) + '  BTC=' + str(round(r['btc_price'])) + '  cum_pl=' + str(round(r['cum_pl_price'])) + '  mvrv0=' + str(round(r['mvrv_0std'])) + '  gap=' + str(round(gap)))

print()
print('=== CROSS DOWN (cum_pl turun di bawah mvrv_0std) ===')
for _, r in crossdowns.iterrows():
    gap = r['cum_pl_price'] - r['mvrv_0std']
    print(str(r['date'].date()) + '  BTC=' + str(round(r['btc_price'])) + '  cum_pl=' + str(round(r['cum_pl_price'])) + '  mvrv0=' + str(round(r['mvrv_0std'])) + '  gap=' + str(round(gap)))

# Cek berapa hari setelah cross up ada cross down, dan BTC setelahnya
print()
print('=== SESI ABOVE (durasi & BTC max selama above) ===')
cup_dates = list(crossups['date'])
cdn_dates = list(crossdowns['date'])

for cu in cup_dates:
    next_down = [d for d in cdn_dates if d > cu]
    if next_down:
        cd = next_down[0]
        duration = (cd - cu).days
        mask = (df['date'] >= cu) & (df['date'] <= cd)
        btc_max = df[mask]['btc_price'].max()
        btc_at_cd = df[df['date'] == cd]['btc_price'].values[0]
        print('Cross UP: ' + str(cu.date()) + ' -> Cross DOWN: ' + str(cd.date()) + '  (' + str(duration) + 'd)  BTC max during: ' + str(round(btc_max)) + '  BTC at down: ' + str(round(btc_at_cd)))
    else:
        last_date = df['date'].iloc[-1]
        duration = (last_date - cu).days
        mask = (df['date'] >= cu)
        btc_max = df[mask]['btc_price'].max()
        btc_now = df['btc_price'].iloc[-1]
        print('Cross UP: ' + str(cu.date()) + ' -> STILL ABOVE (' + str(duration) + 'd since cross)  BTC max: ' + str(round(btc_max)) + '  BTC now: ' + str(round(btc_now)))

# Sekarang
print()
latest = df.iloc[-1]
print('Kondisi sekarang ' + str(latest['date'].date()) + ':')
print('  BTC price:    ' + str(round(float(latest['btc_price']))))
print('  cum_pl_price: ' + str(round(float(latest['cum_pl_price']))))
print('  mvrv_0std:    ' + str(round(float(latest['mvrv_0std']))))
print('  gap:          ' + str(round(float(latest['cum_pl_price']) - float(latest['mvrv_0std']))))
print('  status:       ' + ('cum_pl ABOVE mvrv0' if latest['pl_above_mvrv'] else 'cum_pl BELOW mvrv0'))
