import pytest 
from backend.utils.image import convert_to_writable
from backend.utils.kyc_api import is_single_face, approve_kyc_status, get_kyc_status
import os

def test_get_kyc_status_WhenInputIsValid():
    assert get_kyc_status("coinfunnoreply@gmail.com") == True

def test_get_kyc_status_WhenInputIsInvalid():
    with pytest.raises(Exception, match= "Couldn't fetch KYC status"):
        get_kyc_status("coinfunnoreply@example.com")
        
def test_approve_kyc_status_WhenInputIsValid():
    assert approve_kyc_status("coinfunnoreply@gmail.com") == True

def test_approve_kyc_status_WhenInputIsInvalid():
    with pytest.raises(Exception, match= "Email ID not found in userinfo table"):
        approve_kyc_status("coinfunnoreply@example.com")

def test_is_single_face_when_image_is_blank():
    script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
    file_path = script_directory + '/' + 'blank.jpg'
    assert is_single_face(convert_to_writable(file_path).decode("utf-8") ) == False
    
def test_is_single_face_when_image_is_NotBlank():
    script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
    file_path = script_directory + '/' + 'trump.jpeg'
    assert is_single_face(convert_to_writable(file_path).decode("utf-8")) == True
    
def test_is_single_face_when_image_is_None():
    with pytest.raises(Exception):
        is_single_face(None)
    