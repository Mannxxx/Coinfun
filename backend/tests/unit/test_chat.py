import pytest
from backend.utils.chat import update_chat_txt, get_chat_list
from backend.utils.image import convert_to_writable
import os 

def test_update_chat_txt_whenInputIsInvalid():
    email_id1 = "coinfunnoreply2@gmail.com"
    email_id2 = email_id1
    with pytest.raises(Exception, match="Chat Messages Coudn't be updated!"):
        update_chat_txt(email_id1, email_id1, email_id2, "Hello")

def test_update_chat_txt_whenInputIsValid():
    email_id1 = "coinfunnoreply2@gmail.com"
    email_id2 = "coinfunnoreply3@gmail.com"
    assert update_chat_txt(email_id1, email_id1, email_id2, "Hello") == "Chat messages updated successfully!"

# def test_update_chat_image_whenInputIsInvalid():
#     email_id1 = "coinfunnoreply2@gmail.com"
#     email_id2 = "coinfunnoreply2@gmail.com"
#     script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
#     file_path = os.path.join(script_directory, 'blank.jpg') # Define the path to the image file relative to the data directory
#     with pytest.raises(Exception, match="Chat Messages Coudn't be updated!"):
#         update_chat_image(email_id1, email_id1, email_id2, convert_to_writable(file_path).decode("UTF-8"))

# def test_update_chat_image_whenInputIsValid():
#     email_id1 = "coinfunnoreply3@gmail.com"
#     email_id2 = "coinfunnoreply2@gmail.com"
#     script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
#     file_path = os.path.join(script_directory, 'blank.jpg') # Define the path to the image file relative to the data directory
#     assert update_chat_image(email_id1, email_id1, email_id2, convert_to_writable(file_path).decode("UTF-8") )=="Chat messages updated successfully!"

def test_get_chat_list_whenInputIsValid():
    email_id1 = "coinfunnoreply3@gmail.com"
    assert type(get_chat_list(email_id1)) == list

