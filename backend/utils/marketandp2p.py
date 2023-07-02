import mysql.connector
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import os
import json
import base64
from backend.utils.image import convert_to_writable
from backend.utils.userprofile import get_user_profile
import io

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teamwork123",
    database="Coinfun_database",
    autocommit=True
)

def get_fav_crypto_list(email_id):
    try: 
        cursor = db.cursor()
        cursor.execute('SELECT favourites from userinfo where email_id=%s',(email_id,))
        t = cursor.fetchone()
        if(t==None or t[0]==None or t[0]==""):
            raise Exception("You do not have any favourite crypto currencies!")
        favourite_crypto_list = t[0].split(",")
        cursor.close()
        return favourite_crypto_list    # returns a list of strings
    except mysql.connector.Error as e:
        db.rollback()
        raise e
    except Exception as e:
        raise e

def get_market_data(email_id= None, filename='market_data.json'):   # returns a list of dictionaries containing market data
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__)) # Define the path to the data directory relative to the script directory
        data_directory = os.path.join(script_directory, 'data')
        file_path = data_directory + '/' + filename
        with open(file_path) as f:  
            market_data = json.load(f) # Access contents of the dictionary
    except:
        market_data = []

    try:
        if(email_id == None):
            for item in market_data:
                item['symbol'] = (item['symbol'].split("/"))[0]
            return market_data
        else:
            fav_crypto = get_fav_crypto_list(email_id)
            for item in market_data:
                item['symbol'] = (item['symbol'].split("/"))[0]
                if (item['symbol'] in fav_crypto):
                    item['fav_crypto'] = True
                else:
                    item['fav_crypto'] = False
            return market_data
    except Exception as e:
        if(str(e)=="You do not have any favourite crypto currencies!"):
            #raise e
            for item in market_data:
                item['symbol'] = (item['symbol'].split("/"))[0]
                item['fav_crypto'] = False
            return market_data
        else:
            raise Exception('Market data could not be fetched!')

def get_fav_page_data(email_id):
    try: 
        market_data = get_market_data(email_id)
        list_ = []
        for dict_ in market_data:
            if(dict_['fav_crypto'] == True):
                list_.append(dict_)
        return list_
    except Exception as e:
        raise e

def get_p2p_buy_page_data():        # returns a list of dict
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM P2PBiddingData where buy_type = false')
        rows = cursor.fetchall()
        keys = ('email_id', 'buy_type', 'transaction_usdt', 'price', 'payment_method', 'lower_limit', 'upper_limit')
        data_ = list([dict(zip(keys, row)) for row in rows])
        for dict_ in data_:
            dict_['username'] = get_user_profile(dict_["email_id"])['username']
        data_ = [{**d, 'price': round(d['price'], 2)} for d in data_]
        data_ = [{**d, 'lower_limit': round(d['lower_limit'], 2)} for d in data_]
        data_ = [{**d, 'upper_limit': round(d['upper_limit'], 2)} for d in data_]
        cursor.close()
        return data_
    except mysql.connector.Error as e:
        db.rollback()
        raise Exception('Sorry! Bidding details for Buying page could not be fetched !')
    except:
        raise Exception('Sorry! Bidding details for Buying page could not be fetched !')

def get_p2p_sell_page_data():   # returns a list of dict
    try:
        cursor = db.cursor()
        cursor.execute('SELECT * FROM P2PBiddingData where buy_type = True')
        rows = cursor.fetchall()
        keys = ('email_id', 'buy_type', 'transaction_usdt', 'price', 'payment_method', 'lower_limit', 'upper_limit')
        data_ = list([dict(zip(keys, row)) for row in rows])
        for dict_ in data_:
            dict_['username'] = get_user_profile(dict_["email_id"])['username']
        data_ = [{**d, 'price': round(d['price'], 2)} for d in data_]
        data_ = [{**d, 'lower_limit': round(d['lower_limit'], 2)} for d in data_]
        data_ = [{**d, 'upper_limit': round(d['upper_limit'], 2)} for d in data_]
        cursor.close()
        return data_
    except mysql.connector.Error as e:
        db.rollback()
        raise Exception('Sorry! Bidding details for Selling page could not be fetched!')
    except:
        raise Exception('Sorry! Bidding details for Selling page could not be fetched!')

def form_graph(crypto, time_frame, horizontal_size=16, vertical_size=8):
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__)) # Load market data from JSON file
        data_directory = os.path.join(script_directory, 'data') # Define the path to the data directory relative to the script directory
        file1_path = data_directory + '/' + "Bybit-" + crypto + "USDT-" + time_frame + ".json"
        
        with open(file1_path) as f:  
            currency_data = json.load(f)
        df = pd.DataFrame(currency_data)
        
        market_data = get_market_data()
        # crypto_details = next((item for item in market_data if item['symbol'].startswith(crypto)), {})
        crypto_details = {}
        for item in market_data:
            temp = (item['symbol'].split('/'))[0]
            if (temp == crypto):
                crypto_details = item
                crypto_details['symbol'] = crypto
        
        # Convert timestamps to dates
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%dT%H:%M:%S.%f')
        
        # Plot candlestick chart
        fig, ax = plt.subplots()
        
        # Plot the candlesticks
        for i in range(len(df)):
            x = df['Timestamp'][i]
            y_open = df['Open'][i]
            y_high = df['High'][i]
            y_low = df['Low'][i]
            y_close = df['Close'][i]
            if y_close > y_open:
                ax.plot([x, x], [y_low, y_high], color='green')
                ax.plot([x, x], [y_open, y_close], color='green', linewidth=3)
            else:
                ax.plot([x, x], [y_low, y_high], color='red')
                ax.plot([x, x], [y_open, y_close], color='red', linewidth=3)
        
        fig.set_size_inches(horizontal_size, vertical_size)
        #plt.show()
        
        buf = io.BytesIO() # Convert image to base64 string
        fig.savefig(buf, format='png')
        #image_path = os.path.join(data_directory, crypto+'_'+time_frame+'_candlestick_plot.png')
        #fig.savefig(image_path) # Save image to a file
        
        buf.seek(0)
        base64_image = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        return ( base64_image, crypto_details) # image is a base64 string, crypto_details is a dictionary
    except Exception as e:
        raise e

def add_usdt_to_wallet_when_bought_from_p2p(email_id, balance_to_add):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT wallet FROM userinfo WHERE email_id = %s', (email_id,))
        wallet = cursor.fetchone()[0]
        wallet = json.loads(wallet)
        wallet['USDT']+=balance_to_add
        wallet = json.dumps(wallet)
        cursor.execute("UPDATE userinfo SET wallet = %s WHERE email_id= %s",(wallet,email_id,))
        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as e:
        db.rollback()
        return False
    except Exception as e:
        return False

def update_p2p_trade_history(buyer_email_id, seller_email_id, transaction_usdt, bid_type):
    try:
        cursor = db.cursor()                # bid_type = True means VIP user released, else Normal user sold
        
        # Retrieve the bid record for the specified email_id and buy_type
        query = "SELECT * FROM P2PBiddingData WHERE email_id = %s AND buy_type = %s"
        if(bid_type==True):
            cursor.execute(query, (seller_email_id, False,))
        else:
            cursor.execute(query, (buyer_email_id, True,))
            
        bid = cursor.fetchone()
        price = float(bid[3])
        
        sql = "INSERT INTO P2PTradeHistoryData (buyer_email_id, seller_email_id, transaction_usdt, price, time_stamp) VALUES (%s, %s, %s, %s, NOW())"
        val = (buyer_email_id, seller_email_id, transaction_usdt, price)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as e:
        db.rollback()
        cursor.close()
        return False
    except Exception as e:
        cursor.close()
        return False

def update_p2p_bid(email_id, usdt_qnty, buy_type):
    try:                        # buy_type is type of VIP user's bid
        cursor = db.cursor()

        query = "SELECT * FROM P2PBiddingData WHERE email_id = %s AND buy_type = %s"
        cursor.execute(query, (email_id, buy_type,))
        bid = cursor.fetchone()
        
        new_transaction_usdt = float(bid[2]) - usdt_qnty
        new_lower_limit = float(bid[5]) - (usdt_qnty * float(bid[3]))
        new_upper_limit = float(bid[6]) - (usdt_qnty * float(bid[3]))
        
        if new_transaction_usdt <=0.1:
            query = "DELETE FROM P2PBiddingData WHERE email_id = %s AND buy_type = %s"
            cursor.execute(query, (email_id, buy_type,))
        else:
            query = "UPDATE P2PBiddingData SET transaction_usdt = %s, lower_limit = %s, upper_limit = %s WHERE email_id = %s AND buy_type = %s"
            cursor.execute(query, (new_transaction_usdt, new_lower_limit, new_upper_limit, email_id, buy_type,))
        db.commit()
        cursor.close()
        return True
    except mysql.connector.Error as e:
        db.rollback()
        cursor.close()
        return False
    except:
        cursor.close()
        return False

def deduct_usdt_from_wallet_when_released_in_p2p(email_id, buyer_mailid, balance_to_deduct):
    try:
        cursor = db.cursor()
        cursor.execute('SELECT wallet FROM userinfo WHERE email_id = %s', (email_id,))
        wallet = cursor.fetchone()[0]
        wallet = json.loads(wallet)
        print(wallet)
        
        if(wallet['USDT_in_bid']>10 and  balance_to_deduct > wallet['USDT_in_bid']):    # VIP user ad ->Invalid order
            raise Exception("Your amount entered exceeds upper limit of your order amount!")
        elif(wallet['USDT_in_bid'] + 0.1 >= balance_to_deduct):   # VIP valid order is releasing i.e. buy_type=False
            wallet['USDT_in_bid']-=balance_to_deduct              # ad was on buy_page 
            wallet['USDT_in_bid'] = max(wallet['USDT_in_bid'], 0)
            wallet = json.dumps(wallet)
            update_p2p_trade_history(buyer_mailid, email_id, balance_to_deduct, True)
            update_p2p_bid(email_id, balance_to_deduct, False)
        elif(wallet['USDT']> balance_to_deduct + 0.1 ):    # Normal user is selling to VIP buyer i.e. buy_type=True
            wallet['USDT'] -= balance_to_deduct
            wallet['USDT'] = max(wallet['USDT'], 0)
            wallet = json.dumps(wallet)
            update_p2p_trade_history(buyer_mailid, email_id, balance_to_deduct, False)
            update_p2p_bid(buyer_mailid, balance_to_deduct, True)
        elif(wallet['USDT']< balance_to_deduct ):
            raise Exception("Your amount entered exceeds your wallet balance!")
        
        cursor.execute("UPDATE userinfo SET wallet = %s WHERE email_id= %s",(wallet,email_id,))
        db.commit()
        
        cursor.close()
        return True
    except mysql.connector.Error as e:
        db.rollback()
        return False
    except Exception as e:
        cursor.close()
        return False