import hashlib
import re

def is_password_valid(password):
    try:
        if len(password) < 8 or len(password) > 25:
            return False			## Too short or Too Long
        if not re.search(r'[A-Z]', password):
            return False			## No Capital Alphabet
        if not re.search(r'[a-z]', password):
            return False			## No Small Alphabet
        if not re.search(r'\d', password):
            return False			## No digit
        return True
    except:
        raise Exception("PasswordValidationFailed!")

def encrypt_password(password):
    try:
        if(is_password_valid(password)):
            # hash the salted password using SHA-256
            salted_password = password + "my_salt" + password[::-1]
            hashed_password = hashlib.sha256(salted_password.encode()).hexdigest()
            return hashed_password
        raise Exception("Invalid Password")
    except:
        raise Exception("PasswordEncryptionFailed!")
