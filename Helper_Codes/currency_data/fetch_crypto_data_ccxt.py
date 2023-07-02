import ccxt
from datetime import datetime, timedelta
import pandas as pd
import json, time

symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'DOGE/USDT', 'XRP/USDT', 'MATIC/USDT', 'ADA/USDT', 'SOL/USDT', 'SHIB/USDT', 'LTC/USDT']
time_frames = ["1m" , "15m" , "1h" , "1d" ]
exchange = getattr (ccxt, "bybit") ()    

def fetch_specific_currency_data(symbol, timeframe): # Input Example: symbol = "BTC/USDT" and timeframe = "1m"
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe)
        header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(data, columns=header).set_index('Timestamp')
        df.index = pd.to_datetime(df.index, unit='ms') + timedelta(hours=5, minutes=30) # convert timestamp to IST format
        symbol_out = symbol.replace("/", "")
        filename = 'data/{}-{}-{}.json'.format(exchange, symbol_out,timeframe)
        df.reset_index().to_json(filename, orient='records', date_format='iso') # save as json file with date format
    except:
        raise Exception("Couldn't Fetch Data for given symbol and timeframe!" )

def fetch_all_currency_data(symbols= symbols, time_frames=time_frames):
    #start_time = time.time()  # start measuring time  (Takes about 8 seconds)
    try:
        for symbol in symbols:
            for timeframe in time_frames:
                fetch_specific_currency_data(symbol, timeframe)
    except:
        raise Exception("Failed to fetch data for all currencies!" )
    #end_time = time.time()  # end measuring time
    #print("Total time taken:", end_time - start_time, "seconds")

def fetch_market_page_data(symbols= symbols):
    try:
        #exchange = ccxt.bybit()
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
    except:
        raise Exception("Couldn't Fetch Market Page Data!" )

fetch_all_currency_data()
fetch_market_page_data()
