import pytest
from backend.utils.chat import update_chat_txt
from backend.utils.chat import get_chat_list
from backend.utils.userprofile import add_new_user, drop_user_having_data_only_in_userinfo , validate_user_while_login
from backend.utils.encryption_scheme import encrypt_password

def test_create_new_user_and_get_empty_chat_list():
    email_id = "coinfunnoreply15_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply15"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    assert get_chat_list(email_id) == []
    drop_user_having_data_only_in_userinfo(email_id)
    assert validate_user_while_login(email_id, "password") == False     # check if user exists


def test_use_old_user_and_get_Nonempty_chat_list():
    email_id1 = "coinfunnoreply2@gmail.com"
    email_id2 = "coinfunnoreply3@gmail.com"
    assert update_chat_txt(email_id1, email_id1, email_id2, "Hello")== "Chat messages updated successfully!" # sender is email_id1
    assert update_chat_txt(email_id1, email_id2, email_id1, "Hello")== "Chat messages updated successfully!" # sender is email_id1
    assert get_chat_list(email_id1) != []

def take_new_user_and_try_sending_mesg_to_self():
    email_id = "coinfunnoreply15_test_user@gmail.com"      # create a new user email
    assert validate_user_while_login(email_id, "password") == False     # check if user exists
    
    password = "CoinfunNoreply15"
    assert add_new_user(email_id, "CoinfunNoreply9", encrypt_password( password ), "1234567890")==True
    assert validate_user_while_login(email_id, password) == True
    
    with pytest.raises(Exception, match= "You cannot send message to yourself"):
        update_chat_txt(email_id, email_id, email_id, "Hello") # sender is email_id1
    assert get_chat_list(email_id) == []
    drop_user_having_data_only_in_userinfo(email_id)
    
    
    
    