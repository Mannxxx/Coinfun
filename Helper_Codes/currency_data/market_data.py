import ccxt
import json

exchange = ccxt.bybit()
with open('symbols.json', 'r') as f:
    symbols = json.load(f)

# symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'DOGE/USDT', 'XRP/USDT', 'MATIC/USDT', 'ADA/USDT', 'SOL/USDT', 'SHIB/USDT', 'LTC/USDT']
output_data = []

for symbol in symbols:
    ticker = exchange.fetch_ticker(symbol)
    data = {
        'symbol': symbol,
        'last_price': ticker['last'],
        '24h_change': ticker['percentage'],
        '24h_high': ticker['high'],
        '24h_low': ticker['low'],
        '24h_turnover': ticker['quoteVolume'],
    }
    output_data.append(data)

with open('data/market_data.json', 'w') as f:
    json.dump(output_data, f, indent=2)