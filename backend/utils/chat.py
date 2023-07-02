import json
import mysql.connector
from backend.utils.userprofile import get_user_profile

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teamwork123",
    database="Coinfun_database",
    autocommit=True
)


def update_chat_txt(sender_email, emailID1, emailID2, message):        #emailID1-> looking to buy and emailID2-> looking to sell
    try:
        cursor = db.cursor()
        #if (emailID1 > emailID2):
        #    emailID1,emailID2 = emailID2,emailID1
        if(emailID1==emailID2):
            raise Exception("You cannot send message to yourself!")
        cursor.execute('SELECT chat_messages FROM chat WHERE email_id1 = %s AND email_id2 = %s', (emailID1, emailID2,))
        t = cursor.fetchone()
        if (t == None):
            chat = json.dumps([])
            cursor.execute('INSERT INTO chat (email_id1, email_id2, chat_messages) VALUES (%s, %s, %s)', (emailID1, emailID2, chat,))
            db.commit()
            cursor.close()
            update_chat_txt(sender_email,emailID1,emailID2,message)
            return "Chat messages updated successfully!"
        t = json.loads(t[0])
        data = {}
        data["sender"] = sender_email
        data["message"] = message
        data['image'] = {}
        data['image']['name'] = None
        data['image']['type'] = None
        data['image']['data'] = None
        # data['image'] = json.loads("{'name':Null,'type':Null,'data':NULL}")
        t.append(data)
        t = json.dumps(t)
        cursor.execute("UPDATE chat SET chat_messages = %s WHERE email_id1 = %s AND email_id2 = %s", (t, emailID1,emailID2))
        db.commit()
        cursor.close()
        return "Chat messages updated successfully!"
    except mysql.connector.Error as e:
        db.rollback()
        cursor.close()
        raise Exception("Chat Messages Coudn't be updated!")
    except:
        cursor.close()
        raise Exception("Chat Messages Coudn't be updated!")


# def update_chat_image(sender_email,emailID1,emailID2,photo):
#     try:
#         cursor = db.cursor()
#         #if (emailID1 > emailID2):
#         #    emailID1,emailID2 = emailID2,emailID1
#         if(emailID1==emailID2):
#             raise Exception("You cannot send message to yourself!")
#         cursor.execute('SELECT chat_messages FROM chat WHERE email_id1 = %s AND email_id2 = %s', (emailID1, emailID2,))
#         t = cursor.fetchone()
#         if (t == None):
#             chat = json.dumps([])
#             cursor.execute('INSERT INTO chat (email_id1, email_id2, chat_messages) VALUES (%s, %s, %s)', (emailID1, emailID2, chat,))
#             db.commit()
#             cursor.close()
#             update_chat_image(sender_email,emailID1,emailID2,photo)
#             return "Chat messages updated successfully!"
#         t = json.loads(t[0])
        
#         data = {}
#         data["sender"] = sender_email
#         data["message"] = ''
#         # data['image'] = json.loads("{'name':Null,'type':Null,'data':NULL}")
#         data['image'] = {}
#         data['image']['name'] = None
#         data['image']['type'] = None
#         data['image']['data'] = photo # Encoded base64 string
#         t.append(data)
        
#         t = json.dumps(t)
#         cursor.execute("UPDATE chat SET chat_messages = %s WHERE email_id1 = %s AND email_id2 = %s", (t, emailID1,emailID2))
#         db.commit()
#         cursor.close()
#         return "Chat messages updated successfully!"
#     except mysql.connector.Error as e:
#         db.rollback()
#         cursor.close()
#         raise Exception("Chat Messages Coudn't be updated!")
#     except:
#         cursor.close()
#         raise Exception("Chat Messages Coudn't be updated!")

def get_chat_list(email_id):
    try:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM chat WHERE email_id1 = %s OR email_id2 = %s", (email_id, email_id))
        chat_list = []
        for result in cursor:
            email_id1 = result[0]
            email_id2 = result[1]
            if email_id1 == email_id:
                client_email_id = email_id2
                order_type = "BUY"
            else:
                client_email_id = email_id1
                order_type = "SELL"
            chat_dict = { "client_email_id": client_email_id, "username": get_user_profile(client_email_id)['username'], "order_type": order_type }
            chat_list.append(chat_dict)
        cursor.close()
        return chat_list
    except mysql.connector.Error as e:
        db.rollback()
        cursor.close()
        return []
    except:
        cursor.close()
        return []

#print(get_chat_list("person4@gmail.com"))