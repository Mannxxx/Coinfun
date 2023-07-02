import pytest 
from backend.utils.userprofile import add_new_user, drop_user_having_data_only_in_userinfo , validate_user_while_login
from backend.utils.encryption_scheme import encrypt_password
from backend.utils.dashboard import get_wallet_data
from backend.utils.marketandp2p import get_market_data , get_fav_page_data , get_p2p_buy_page_data , get_p2p_sell_page_data
from backend.utils.marketandp2p import add_usdt_to_wallet_when_bought_from_p2p , form_graph
from backend.utils.order_and_wallet import get_order_history


def test_add_new_user_and_check_dashboard_data():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert type(get_wallet_data(email_id)) == dict 
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    

def test_add_new_user_and_check_market_data_page():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert type(get_wallet_data(email_id)) == dict 
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists

def test_add_new_user_and_check_fav_market_data_page():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert type(get_market_data(email_id)) == list 
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists

def test_add_new_user_and_check_fav_market_data_page():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert type(get_fav_page_data(email_id)) == list 
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
def test_add_new_user_and_check_p2p_buy_page_data():    
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert type(get_p2p_buy_page_data()) == list 
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists

def test_add_new_user_and_check_p2p_sell_page_data():    
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert type(get_p2p_sell_page_data()) == list 
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists

def test_add_new_user_and_get_paid_via_P2P():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    initial_wallet = get_wallet_data(email_id)
    initial_USDT = next((item['amount'] for item in initial_wallet['data'] if item['symbol'] == 'USDT'), 0)
    assert add_usdt_to_wallet_when_bought_from_p2p(email_id, 100) == True
    final_wallet = get_wallet_data(email_id)
    final_USDT = next((item['amount'] for item in final_wallet['data'] if item['symbol'] == 'USDT'), 0)
    assert abs(final_USDT - initial_USDT - 100) < 0.1
    assert add_usdt_to_wallet_when_bought_from_p2p(email_id, -100) == True
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
def test_add_new_user_and_get_data_for_charts():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    data = form_graph("ETH", "1m")
    assert type(data[0]) == str
    assert type(data[1]) == dict
    
    with pytest.raises(Exception):
        data = form_graph("example", "1m")
        
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists

def test_add_new_user_and_get_order_history_data():
    email_id = "coinfunnoreply35_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply35"
    assert add_new_user(email_id, "CoinfunNoreply35", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    with pytest.raises(Exception, match= 'You do not have any orders till now. Enter the market to place your orders!' ):
        get_order_history(email_id)
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    
    