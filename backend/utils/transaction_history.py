from backend.utils.userprofile import get_user_profile
import mysql.connector
import datetime

def time_convertor_to_str(datetime_obj):
    return datetime_obj.strftime("%Y-%m-%d %H:%M:%S")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teamwork123",
    database="Coinfun_database",
    autocommit=True
)

def get_transaction_history_data(email_id): # returns a list of dictionaries containing transaction history data of P2P trades
    try:
        cursor = db.cursor()
        # query the P2PTradeHistoryData table for transactions involving the given email_id
        query = "SELECT * FROM P2PTradeHistoryData WHERE buyer_email_id = %s OR seller_email_id = %s"
        cursor.execute(query, (email_id, email_id))
        result = cursor.fetchall()
        
        # check if the result is empty and raise an exception if so
        if not result:
            cursor.close()
            raise Exception("No Transaction History Available")
        
        #convert the result to a list of dictionaries
        #keys = ['order_id', 'buyer_email_id', 'seller_email_id', 'transaction_usdt', 'price', 'time_stamp'] ## Order of keys
        transaction_history = []
        
        for row in result:
            temp = {}
            temp['time_stamp'] = time_convertor_to_str(row[5])
            temp['order_id'] = row[0]
            
            temp['client'] = ["username","email_id"]
            if(row[1]==email_id):
                # means the user is the buyer
                temp['order_type'] = "Buy"
                temp['client'][1] = row[2]
            else:
                # means the user is the seller
                temp['order_type'] = "Sell"
                temp['client'][1] = row[1]
            temp['client'][0] = get_user_profile(temp['client'][1])['username']
            ## temp['client'] = [username, email_id]
            temp['transaction_usdt'] = round(row[3],3)
            temp['price'] = round(row[4],3)
            temp['net_usdt'] = temp['transaction_usdt'] * temp['price']
            transaction_history.append(temp)
        cursor.close()
        return transaction_history
    except mysql.connector.Error as e:
        db.rollback()
        raise e
    except Exception as e:
        raise e

#print(get_transaction_history_data("person1@gmail.com"))