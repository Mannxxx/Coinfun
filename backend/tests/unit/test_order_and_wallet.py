import pytest
from backend.utils.order_and_wallet import get_order_history, change_wallet, add_order

def test_add_order_WhenInputIsInvalid():
    email_id = "example@example.com"
    crypto = "BTC"
    last_price = 30000
    crypto_amount = 0.01
    order_type = "BUY"
    with pytest.raises(Exception, match= "Could not add order details to user's order history"):
        add_order(email_id, crypto, last_price, crypto_amount, order_type)

def test_add_order_WhenInputIsValid():
    email_id = "coinfunnoreply3@gmail.com"
    crypto = "BTC"
    last_price = 30000
    crypto_amount = 0.01
    order_type = "BUY"
    add_order(email_id, crypto, last_price, crypto_amount, order_type)== "Order Successful!"

def test_get_order_history_WhenInputIsValid_And_HistoryIsEmpty():
    email_id = "coinfunnoreply2@gmail.com"
    with pytest.raises(Exception, match= "You do not have any orders till now. Enter the market to place your orders!"):
        get_order_history(email_id)

def test_get_order_history_WhenInputIsValid_And_HistoryIsNonEmpty():
    email_id = "coinfunnoreply3@gmail.com"
    assert type(get_order_history(email_id)) == list

def test_change_wallet_WhenUSDTisNotEnough():
    email_id = "coinfunnoreply2@gmail.com"
    crypto = "BTC"
    order_type = "BUY"
    usdt_qty = 1000000000000000
    with pytest.raises(Exception, match= "You do not have sufficient USDT balance"):
        change_wallet(email_id, order_type, crypto, usdt_qty)

def test_change_wallet_WhenCryptoisNotEnough():
    email_id = "coinfunnoreply2@gmail.com"
    crypto = "BTC"
    order_type = "SELL"
    usdt_qty = 1000000000000000
    with pytest.raises(Exception, match= "You do not have sufficient crypto coins!"):
        change_wallet(email_id, order_type, crypto, usdt_qty)

def test_change_wallet_WhenInputIsValid():
    email_id = "coinfunnoreply3@gmail.com"
    crypto = "BTC"
    usdt_qty = 100
    assert change_wallet(email_id, "BUY", crypto, usdt_qty) == "Wallet Updated Successfully!"
    assert change_wallet(email_id, "SELL", crypto, usdt_qty) == "Wallet Updated Successfully!"