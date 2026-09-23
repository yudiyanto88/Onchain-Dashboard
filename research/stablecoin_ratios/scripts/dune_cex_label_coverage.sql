select cex_name, blockchain, count(*) as n_alamat
from cex.addresses
where lower(cex_name) in ('coinbase','binance','upbit','bithumb','bitflyer','coincheck','coinone','okx','kraken','bitfinex','bybit','gemini','robinhood')
  and blockchain in ('bitcoin','ethereum','tron')
group by 1,2 order by 1,2
