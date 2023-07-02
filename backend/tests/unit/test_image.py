import pytest
from backend.utils.image import is_allowed_file, convert_to_writable
import os
import base64

def test_is_allowed_file_when_it_have_allowed_extension():
    assert is_allowed_file("test.png") == True
    assert is_allowed_file("test.jpg") == True
    assert is_allowed_file("test.jpeg") == True
    
def test_is_allowed_file_when_it_doesnt_have_allowed_extension():
    assert is_allowed_file("test.txt") == False
    assert is_allowed_file("test") == False

def test_convert_to_writable_when_it_is_a_valid_file():
    # Get the absolute path of the directory where this script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_directory, 'blank.jpg')
    # This function expects the filepath of the image to be converted
    encoded_file = convert_to_writable(filepath)   
    decoded_file = base64.b64decode(encoded_file)  # We must decode the file to get the original file
    assert decoded_file == open(filepath,'rb').read()  # Open a file in binary mode

def test_convert_to_writable_when_it_is_a_Invalid_file():
    
    with pytest.raises(Exception, match= "ConversionToBase64StringFailed!"):
        convert_to_writable("Invalid_file")
