import pytest
from backend.utils.userprofile import get_user_profile, change_pass_help, validate_user_while_login, add_new_user, drop_user_having_data_only_in_userinfo
from backend.utils.encryption_scheme import encrypt_password

def test_validate_user_while_login_WhenInputIsValid():
    assert validate_user_while_login("Coinfunnoreply@gmail.com" , "Testaccount1Testaccount1") == True

def test_validate_user_while_login_WhenInputIsInValid():
    assert validate_user_while_login("Coinfunnoreply@example.com" , "Testaccount1Testaccount1") == False

def test_add_and_drop_a_new_valid_user():
    assert add_new_user("Coinfunnoreply4@gmail.com","Testaccount4", encrypt_password("Testaccount4Testaccount4"), "999999999999") ==True
    assert drop_user_having_data_only_in_userinfo("Coinfunnoreply4@gmail.com") == True
    
def test_get_user_profile_WhenInputIsValid():
    # Test if a valid email is accepted
    email = "coinfunnoreply@gmail.com"
    data = get_user_profile(email)
    assert data['email_id'] == email
    assert data['username'] == 'Testaccount1'
    assert type(data)==dict

def test_get_user_profile_When_input_is_invalid():
    # Test if a invalid email is accepted
    email = "example@example.com"
    with pytest.raises(Exception, match="Couldn't fetch user profile data"):
        get_user_profile(email)
        



def test_change_pass_help_WhenNewPassIsNotEqualNewPassConfirm():
    # Test if a valid email is accepted
    with pytest.raises(Exception, match="The new password does not matches the confirm new password !"):
        change_pass_help("coinfunnoreply@gmail.com","Testaccount1Testaccount1","Testaccount1Testaccount1","Testaccount1Testaccount")

def test_change_pass_help_WhenNewPassIsNotValid():
    # Test if a valid email is accepted
    with pytest.raises(Exception, match="Please enter a valid password, it should contain atleast 1 capital and 1 small alphabets and atleast 1 digit with length between 8-25"):
        change_pass_help("coinfunnoreply@gmail.com","Testaccount1Testaccount1","Test1","Test1")

def test_change_pass_help_WhenCurrentPassIsNotValid1():
    # Test if a valid email is accepted
    with pytest.raises(Exception, match="The current entered password does not matches the exisiting password"):
        change_pass_help("coinfunnoreply@gmail.com","Old","Testaccount1Testaccount1","Testaccount1Testaccount1")
        
def test_change_pass_help_WhenCurrentPassIsNotValid2():
    # Test if a valid email is accepted
    with pytest.raises(Exception, match="The current entered password does not matches the exisiting password"):
        change_pass_help("coinfunnoreply@gmail.com","OldPassword1","Testaccount1Testaccount1","Testaccount1Testaccount1")

def test_change_pass_help_WhenInputIsValid():
    assert change_pass_help("coinfunnoreply@gmail.com","Testaccount1Testaccount1","Testaccount1Testaccount1","Testaccount1Testaccount1")=='PASSWORD UPDATED SUCCESSFULLY'  
