import mysql.connector
import json
from collections import defaultdict
from backend.utils.userprofile import get_user_profile
from backend.utils.marketandp2p import get_market_data

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teamwork123",
    database="Coinfun_database",
    autocommit=True
)

def get_wallet_data(email_id):
    # returns a dict with keys username->username, data-->list of dicts, est_balance--> total balance 
    try:
        cursor = db.cursor()
        cursor.execute('SELECT wallet FROM userinfo where email_id=%s',(email_id,))
        wallet = cursor.fetchone()[0]
        wallet = json.loads(wallet) # Typecast string to dictionary
        wallet = defaultdict(float, wallet)
        
        market_data = get_market_data()
        
        dict_ = {}
        dict_['username'] = get_user_profile(email_id)['username']

        list_ = []  # List of dictornaries
        # Each dictionary have symbol, amount, price, est_balance
        total_balance = wallet['USDT'] + wallet['USDT_in_bid']

        for item in market_data:
            temp = {}
            crypto = item['symbol'].split("/")[0]
            item['symbol'] = crypto
            temp['symbol'] = crypto
            temp['amount'] = wallet[crypto]
            temp['price'] = item['last_price']
            temp['est_balance'] = temp['price']*temp['amount']     
            total_balance += temp['est_balance']
            list_.append(temp)
        list_.append({'symbol':'USDT', 'amount': wallet['USDT'] , 'price' : '1' , 'est_balance': wallet['USDT']})
        list_.append({'symbol':'USDT(queued in P2P order)', 'amount': wallet['USDT_in_bid'] , 'price' : '1' , 'est_balance': wallet['USDT_in_bid']})
        dict_['data'] = list_ 
        dict_['estimated_balance'] = round(total_balance,3)
        cursor.close()
        return dict_
    except:
        db.rollback()
        raise Exception("Couldn't fetch wallet data")

#print(get_wallet_data("person1@gmail.com"))