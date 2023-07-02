import ccxt
from datetime import datetime, timedelta, timezone
import math
import pandas as pd
import time
import json

exchange = getattr (ccxt, "bybit") ()
with open('symbols.json', 'r') as f:
    symbols = json.load(f)
# symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'DOGE/USDT', 'XRP/USDT', 'MATIC/USDT', 'ADA/USDT', 'SOL/USDT', 'SHIB/USDT', 'LTC/USDT']

time_frames = ["1m" , "15m" , "1h" , "1d" ]

# start_time = time.time()  # start measuring time  (Takes about 8 seconds)
for symbol in symbols:
    for timeframe in time_frames:
        data = exchange.fetch_ohlcv(symbol, timeframe)
        header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(data, columns=header).set_index('Timestamp')
        df.index = pd.to_datetime(df.index, unit='ms') # convert timestamp to datetime format
        symbol_out = symbol.replace("/", "")
        filename = 'data/{}-{}-{}.json'.format(exchange, symbol_out,timeframe)
        df.reset_index().to_json(filename, orient='records', date_format='iso') # save as json file with date format
# end_time = time.time()  # end measuring time
# print("Total time taken:", end_time - start_time, "seconds")