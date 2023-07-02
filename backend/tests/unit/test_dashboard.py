import pytest
from backend.utils.dashboard import get_wallet_data

def test_get_wallet_data_WhenInputIsValid():
    # Test if a valid email is accepted
    email = "coinfunnoreply@gmail.com"
    assert type(get_wallet_data(email)) == dict

def test_get_wallet_data_When_input_is_invalid():
    # Test if a invalid email is accepted
    email = "example@example.com"
    with pytest.raises(Exception, match="Couldn't fetch wallet data"):
        get_wallet_data(email)