import pytest
from backend.utils.encryption_scheme import is_password_valid, encrypt_password

def test_is_password_valid_WhenLengthIsNotSuitable():
    # Test if password is too short
    password = "abcde"
    assert is_password_valid(password) == False

    # Test if password is too long
    password = "abcdefghijkmnopqrstuvwxyz1234567890"
    assert is_password_valid(password) == False

def test_is_password_valid_WhenInputHaveNoUpperCase():
    # Test if password has no uppercase alphabet
    password = "password123"
    assert is_password_valid(password) == False

def test_is_password_valid_WhenInputHaveNoLowerCase():
    # Test if password has no lowercase alphabet
    password = "PASSWORD123"
    assert is_password_valid(password) == False

def test_is_password_valid_WhenInputHaveNoDigits():
    # Test if password has no digit
    password = "Password"
    assert is_password_valid(password) == False

def test_is_password_valid_WhenInputIsValid():
    # Test if a valid password is accepted
    password = "Password123"
    assert is_password_valid(password) == True

def test_is_password_valid_raises_exception_on_non_string_input():
    password = 123
    with pytest.raises(Exception, match="PasswordValidationFailed!"):
        is_password_valid(password)

def test_encrypt_password_WhenInputIsValid():
    # Test if a valid password is encrypted
    password = "MyPassword123"
    assert encrypt_password(password) != password       # Password is encrypted
    
def test_encrypt_password_raises_exception_on_non_string_input():
    password = "abc"
    with pytest.raises(Exception, match="PasswordEncryptionFailed!"):
        encrypt_password(password)
