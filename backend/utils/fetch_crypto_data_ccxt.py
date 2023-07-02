import ccxt
from datetime import datetime, timedelta
import pandas as pd
import json, time
import os

symbols = ['BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'DOGE/USDT', 'XRP/USDT', 'MATIC/USDT', 'ADA/USDT', 'SOL/USDT']
time_frames = ["1m" , "15m" , "1h" , "1d" ]
exchange = getattr (ccxt, "bybit") ()

# Get the absolute path of the directory where this script is located
script_directory = os.path.dirname(os.path.abspath(__file__))

# Define the path to the data directory relative to the script directory
data_directory = os.path.join(script_directory, 'data')

def fetch_specific_currency_data(symbol, timeframe): # Input Example: symbol = "BTC/USDT" and timeframe = "1m"
    try:
        data = exchange.fetch_ohlcv(symbol, timeframe)
        header = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
        df = pd.DataFrame(data, columns=header).set_index('Timestamp')
        df.index = pd.to_datetime(df.index, unit='ms') + timedelta(hours=5, minutes=30) # convert timestamp to IST format
        symbol_out = symbol.replace("/", "")
        filename = '{}-{}-{}.json'.format(exchange, symbol_out,timeframe)
        filename = os.path.join(data_directory, filename)
        df.reset_index().to_json(filename, orient='records', date_format='iso') # save as json file with date format
        return None
    except:
        raise Exception("Couldn't Fetch Data for given symbol and timeframe!" )

def fetch_all_currency_data(symbols= symbols, time_frames=time_frames):
    #start_time = time.time()  # start measuring time  (Takes about 8 seconds)
    try:
        for symbol in symbols:
            for timeframe in time_frames:
                fetch_specific_currency_data(symbol, timeframe)
        return None
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
        filename = 'market_data.json'
        filename = os.path.join(data_directory, filename)
        with open(filename, 'w') as f:
            json.dump(output_data, f, indent=2)
        return None
    except:
        raise Exception("Couldn't Fetch Market Page Data!" )

#fetch_all_currency_data()
#fetch_market_page_data()
