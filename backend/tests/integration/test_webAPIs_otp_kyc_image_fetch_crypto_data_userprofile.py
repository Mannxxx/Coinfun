import pytest
from backend.utils.userprofile import validate_user_while_login, add_new_user, drop_user_having_data_only_in_userinfo , get_user_profile, change_pass_help
from backend.utils.encryption_scheme import encrypt_password
from backend.utils.otp import send_otp
from backend.utils.fetch_crypto_data_ccxt import fetch_specific_currency_data, fetch_all_currency_data, fetch_market_page_data
from backend.utils.image import convert_to_writable
from backend.utils.kyc_api import is_single_face, approve_kyc_status, get_kyc_status
import os

def test_old_users_to_send_otp_at():
    email = "CoinfunNoReply@example.com"
    with pytest.raises(Exception, match="Couldn't Send OTP to given email"):
        otp = send_otp(email)
    
    email = "CoinfunNoReply@gmail.com"
    otp = send_otp(email)
    assert isinstance(otp, int)
    assert otp >= 100000 and otp <= 999999

def test_create_new_user_and_fetch_crypto_data():
    email_id = "coinfunnoreply25_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply25"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    fetch_specific_currency_data("BTC/USDT","1m")
    fetch_all_currency_data()
    fetch_market_page_data()
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists

def test_create_new_user_and_test_kyc_api():
    email_id = "coinfunnoreply25_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply25"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert get_kyc_status(email_id) == False
    
    script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
    file_path = script_directory + '/' + 'blank.jpg'
    assert is_single_face(convert_to_writable(file_path).decode("utf-8") ) == False
    
    with pytest.raises(Exception):
        is_single_face(None)

    script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
    file_path = script_directory + '/' + 'trump.jpeg'
    assert is_single_face(convert_to_writable(file_path).decode("utf-8")) == True
    
    with pytest.raises(Exception):
        approve_kyc_status("exmaple@example.com")
    
    assert approve_kyc_status(email_id) == True
    assert get_kyc_status(email_id) == True
    
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists anymore