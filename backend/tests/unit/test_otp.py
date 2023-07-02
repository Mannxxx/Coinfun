import pytest
from backend.utils.otp import is_valid_domain, send_otp

def test_is_valid_domain_WhenInputDomainIsValid():
    # Test if a valid email is accepted
    email = "CoinfunNoReply@gmail.com"
    assert is_valid_domain(email) == True

def test_is_valid_domain_WhenInputDomainIsInvalid():
    # Test if an invalid email is rejected
    email = "CoinfunNoReply@abc.com"
    assert is_valid_domain(email) == False

def test_is_valid_domain_WhenInputIsInvalid():
    # Test if an invalid email is rejected
    email = 123
    with pytest.raises(Exception, match="Couldn't validate email domain"):
        is_valid_domain(email)



def test_send_otp_WhenInputEmailDomainIsInvalid():
    # Test if a valid email is valid
    email = "CoinfunNoReply@example.com"
    with pytest.raises(Exception, match="Couldn't Send OTP to given email"):
        otp = send_otp(email)
        
def test_send_otp_WhenInputEmailIsInvalid():
    # Test if a valid email is valid
    email = "CoinfunNoReplyCoinfunNoReplyCoinfunNoReplyCoinfunNoReply@example.com"
    with pytest.raises(Exception, match="Couldn't Send OTP to given email"):
        otp = send_otp(email)
        
def test_send_otp_WhenInputEmailIsValid():
    # Test if a valid email is valid
    email = "CoinfunNoReply@gmail.com"
    otp = send_otp(email)
    assert isinstance(otp, int)
    assert otp >= 100000 and otp <= 999999