import pytest
from backend.utils.userprofile import validate_user_while_login, add_new_user, drop_user_having_data_only_in_userinfo , get_user_profile, change_pass_help
from backend.utils.encryption_scheme import encrypt_password
from backend.utils.transaction_history import get_transaction_history_data

def test_create_new_use_with_different_passwords():
    email_id = "coinfunnoreply9_test_user@gmail.com"        # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "Coin"   # try with short password
    with pytest.raises(Exception, match= "PasswordEncryptionFailed!"):
        password = encrypt_password(password)
    
    password = "coinfun123" # try with password without capital letter
    with pytest.raises(Exception, match= "PasswordEncryptionFailed!"):
        password = encrypt_password(password)
    
    password = "COINFUN123" # try with password without small letter
    with pytest.raises(Exception, match= "PasswordEncryptionFailed!"):
        password = encrypt_password(password)
    
    password = "123456789" # try with password without alphabet letter
    with pytest.raises(Exception, match= "PasswordEncryptionFailed!"):
        password = encrypt_password(password)
    
    password = "CoinfunNoreply9"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    assert drop_user_having_data_only_in_userinfo(email_id)==True   # delete the test user from database
    
    
def test_create_new_user_and_change_password():
    email_id = "coinfunnoreply9_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply9"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    assert type(get_user_profile(email_id)) == dict
    
    with pytest.raises(Exception, match= "The new password does not matches the confirm new password !"):
        change_pass_help(email_id, password, "12345", "123456789")
    
    with pytest.raises(Exception, match= "Please enter a valid password, it should contain atleast 1 capital and 1 small alphabets and atleast 1 digit with length between 8-25"):
        change_pass_help(email_id, password, "123456789", "123456789")
    
    with pytest.raises(Exception, match= "The current entered password does not matches the exisiting password"):
        change_pass_help(email_id, "Hello", password, password)
    
    with pytest.raises(Exception, match= "The current entered password does not matches the exisiting password"):
        change_pass_help(email_id, "Hello1234", password, password)
    
    assert change_pass_help(email_id, password, password, password) == 'PASSWORD UPDATED SUCCESSFULLY'
    
    assert drop_user_having_data_only_in_userinfo(email_id)==True

def test_create_new_user_and_check_transaction_history():
    email_id = "coinfunnoreply9_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply9"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    with pytest.raises(Exception, match="No Transaction History Available"):
        get_transaction_history_data(email_id)
    
    assert drop_user_having_data_only_in_userinfo(email_id)==True

    
    
    