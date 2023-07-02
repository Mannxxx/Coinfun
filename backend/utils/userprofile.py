import mysql.connector
from backend.utils.encryption_scheme import is_password_valid, encrypt_password
import base64
from PIL import Image
import io

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teamwork123",
    database="Coinfun_database",
    autocommit=True
)

def check_email_exists(email_id):
    try:
        cursor = db.cursor()
        email_id = email_id.lower()
        cursor.execute("SELECT email_id FROM userinfo WHERE email_id = %s", (email_id,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except:
        cursor.close()
        return False

def validate_user_while_login(email_id, password):
    try:
        if(check_email_exists(email_id)== False):
            return False
        cursor = db.cursor()
        cursor.execute("SELECT password FROM userinfo WHERE email_id = %s", (email_id,))
        result = cursor.fetchone()
        cursor.close()
        return (result!=None and result[0] == encrypt_password(password))
    except:
        return False

def add_new_user(email_id, username, encrypted_password, phone_number):
    try:
        cursor = db.cursor()
        email_id = email_id.lower()
        sql = "INSERT INTO userinfo (email_id, username, password, wallet, favourites, profile_pic, kyc, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (email_id, username, encrypted_password , '{"ADA": 0.0, "BNB": 0.0, "BTC": 0.0, "ETH": 0.0, "SOL":  0.0, "XRP": 0.0, "DOGE": 0.0, "USDT": 10000.0, "MATIC": 0.0, "USDT_in_bid": 0.0}', "", "" , False, phone_number)
        cursor.execute(sql, values)
        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as e:
        db.rollback()
        raise Exception("Couldn't create new user")
    except:
        raise Exception("Couldn't create new user")

def drop_user_having_data_only_in_userinfo(email_id):
    try:
        cursor = db.cursor()
        email_id = email_id.lower()
        cursor.execute("DELETE FROM userinfo WHERE email_id = %s", (email_id,) )
        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as e:
        db.rollback()
        raise Exception("Couldn't drop user having data only in userinfo")
    except:
        raise Exception("Couldn't drop user having data only in userinfo")

def get_user_profile(email):
    cursor = db.cursor()
    try:
        data = {}
        data['email_id'] = email 
        cursor.execute("SELECT * FROM userinfo where email_id=%s", (email,))
        details = cursor.fetchone()
        
        data['username'] = details[1]
        try:
            data['profile_pic'] = base64.b64decode(details[5])
            data['profile_pic'] = details[5].decode('UTF-8')
        except:
            data['profile_pic'] = ""
        data['kyc'] = details[6]
        data['contact_number'] = details[7]
        cursor.close()
        return data
    except mysql.connector.Error as e:
        db.rollback()
        raise Exception("Couldn't fetch user profile data")
    except:
        raise Exception("Couldn't fetch user profile data")


def change_pass_help(email, current_pass, new_pass, new_pass_confirm):
    try:
        if(new_pass!=new_pass_confirm):
            raise Exception("The new password does not matches the confirm new password !")
        if(is_password_valid(new_pass)==False):
            raise Exception("Please enter a valid password, it should contain atleast 1 capital and 1 small alphabets and atleast 1 digit with length between 8-25")
        
        try:
            password_encrypt_for_validation = encrypt_password(current_pass)
        except:
            raise Exception('The current entered password does not matches the exisiting password')
        cursor = db.cursor()
        cursor.execute('SELECT password from userinfo where email_id=%s',(email,))
        current_encrypted_pass = cursor.fetchone()[0]
        
        if(current_encrypted_pass!= password_encrypt_for_validation):
            cursor.close()
            raise Exception('The current entered password does not matches the exisiting password')
        else:
            new_encrypted_pass = encrypt_password(new_pass)
            cursor.execute('UPDATE userinfo SET password =%s WHERE email_id =%s',(new_encrypted_pass,email,))
            cursor.close()
            return 'PASSWORD UPDATED SUCCESSFULLY'
    except mysql.connector.Error as e:
        db.rollback()
        raise e
    except Exception as e:
        raise e

