import pytest
from backend.utils.marketandp2p import get_market_data, get_fav_crypto_list, get_fav_page_data, get_p2p_buy_page_data ,get_p2p_sell_page_data, form_graph , add_usdt_to_wallet_when_bought_from_p2p, deduct_usdt_from_wallet_when_released_in_p2p
from backend.utils.marketandp2p import update_p2p_trade_history, update_p2p_bid

def test_get_market_deta_WhenInputIsValid():
    assert type(get_market_data("coinfunnoreply3@gmail.com")) == list

def test_get_market_data_WhenInputIsNone():
    assert type(get_market_data()) == list

def test_get_market_data_WhenInvalidFilenameisGiven():
    #with pytest.raises(Exception, match="Market data could not be fetched!"):
    assert type(get_market_data("example.exmaple","example.exmaple")) == list

def test_get_fav_crypto_list_WhenFavListIsNonEmpty():
    assert type(get_fav_crypto_list("coinfunnoreply@gmail.com")) == list

def test_get_fav_crypto_list_WhenFavListIsEmpty():
    with pytest.raises(Exception, match="You do not have any favourite crypto currencies!"):
        get_fav_crypto_list("coinfunnoreply2@gmail.com")



def test_get_fav_page_data_WhenFavListIsNonEmpty():
    assert type(get_fav_page_data("coinfunnoreply@gmail.com"))== list

def test_get_fav_page_data_WhenFavListIsEmpty():
    assert type(get_fav_page_data("coinfunnoreply2@gmail.com"))== list

def test_get_fav_page_data_WhenInputEmailIsInvalid():
    assert type(get_fav_page_data("example@example.com"))== list


def test_p2p_buy_page_data_get():
    assert type(get_p2p_buy_page_data()) == list



def test_p2p_sell_page_data_get():
    assert type(get_p2p_sell_page_data()) == list



def test_form_graph_WhenInputIsValid():
    data = form_graph("BTC", "1m")
    assert type(data[0]) == str
    assert type(data[1]) == dict

def test_form_graph_WhenInputIsInValid():
    with pytest.raises(Exception):
        data = form_graph("example", "1m")

def test_add_usdt_to_wallet_when_bought_from_p2p_whenInputIsValid():
    #initial_wallet = get_wallet_data("coinfunnoreply@gmail.com")
    #initial_USDT = next((item['amount'] for item in initial_wallet['data'] if item['symbol'] == 'USDT'), 0)
    assert add_usdt_to_wallet_when_bought_from_p2p("coinfunnoreply@gmail.com", 100) == True
    #final_wallet = get_wallet_data("coinfunnoreply@gmail.com")
    #final_USDT = next((item['amount'] for item in final_wallet['data'] if item['symbol'] == 'USDT'), 0)
    #assert abs(final_USDT - initial_USDT - 100) < 0.1
    assert add_usdt_to_wallet_when_bought_from_p2p("coinfunnoreply@gmail.com", -100) == True

def test_add_usdt_to_wallet_when_bought_from_p2p_whenInputIsValid():
    assert add_usdt_to_wallet_when_bought_from_p2p("example@example.com",100) == False

def test_update_p2p_trade_history_whenInputIsInvalid():
    assert update_p2p_trade_history("example@example.com","example@example.com", 0, True) == False
    assert update_p2p_trade_history("example@example.com","example@example.com", 0, False) == False
    assert update_p2p_trade_history("coinfunnoreply@gmail.com","coinfunnoreply2@gmail.com", 0, True) == False
    assert update_p2p_trade_history("coinfunnoreply@gmail.com","coinfunnoreply2@gmail.com", 0, False) == False
    assert update_p2p_trade_history("coinfunnoreply2@gmail.com","coinfunnoreply@gmail.com", 0, True) == False
    assert update_p2p_trade_history("coinfunnoreply2@gmail.com","coinfunnoreply@gmail.com", 0, False) == False

def test_update_p2p_bid():
    assert update_p2p_bid("example@example.com", 0, True) == False

def test_deduct_usdt_from_wallet_when_released_in_p2p_whenInputIsValid():
    email_id1 = "coinfunnoreply@gmail.com"
    email_id2 = "coinfunnoreply2@gmail.com"
    assert deduct_usdt_from_wallet_when_released_in_p2p(email_id1, email_id2, 0) == True

def test_deduct_usdt_from_wallet_when_released_in_p2p_whenInputIsInValid():
    email_id1 = "example@example.com"
    email_id2 = "example@example1.com"
    assert deduct_usdt_from_wallet_when_released_in_p2p(email_id1, email_id2, 0) == False