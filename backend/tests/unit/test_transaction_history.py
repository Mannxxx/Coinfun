import pytest
from backend.utils.transaction_history import get_transaction_history_data

def test_get_transaction_history_data_WhenInvalidEmailIsGiven():
    # Test if a valid email is accepted
    email_id = "example@exaple.com"
    with pytest.raises(Exception, match="No Transaction History Available"):
        get_transaction_history_data(email_id)

def test_get_transaction_history_data_WhenValidEmailIsGiven():
    # Test if a valid email is accepted
    email_id = "coinfunnoreply@gmail.com" # This email is in the database with empty history
    with pytest.raises(Exception, match="No Transaction History Available"):
        get_transaction_history_data(email_id)

def test_get_transaction_history_data_WhenValidEmailIsGiven():
    # Test if a valid email is accepted
    email_id = "person1@gmail.com" # This email is in the database with non-empty history
    data = get_transaction_history_data(email_id)
    assert type(data) == list