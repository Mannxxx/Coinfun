import pytest
from backend.utils.fetch_crypto_data_ccxt import fetch_specific_currency_data, fetch_all_currency_data, fetch_market_page_data

def test_fetch_specific_currency_data_WhenInputIsValid():
    symbol = "BTC/USDT"
    timeframe = "1m"
    assert fetch_specific_currency_data(symbol, timeframe) == None 
     
def test_fetch_specific_currency_data_WhenInputIsInvalid():
    symbol = "Bitcoin/USDT"
    timeframe = "1minute"
    with pytest.raises(Exception, match="Couldn't Fetch Data for given symbol and timeframe!"):
        fetch_specific_currency_data(symbol, timeframe)

def test_fetch_all_currency_data_WhenInputIsValid():
    assert fetch_all_currency_data() == None

def test_fetch_all_currency_data_WhenInputIsInvalid():
    symbol = ["Bitcoin/USDT"]
    time_frame =["1minute"]
    with pytest.raises(Exception, match="Failed to fetch data for all currencies!"):
        fetch_all_currency_data(symbol, time_frame)

def test_fetch_market_page_data_WhenInputIsValid():
    assert fetch_market_page_data() == None

def test_fetch_market_page_data_WhenInputIsInvalid():
    symbol = ["Bitcoin/USDT"]
    with pytest.raises(Exception, match="Couldn't Fetch Market Page Data!"):
        fetch_market_page_data(symbol)