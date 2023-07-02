import mysql.connector
from backend.utils.encryption_scheme import encrypt_password
import os
import random
import json
from datetime import datetime, timedelta
import read_n_write_image_with_sql
from collections import defaultdict

#### It set ups all the tables with fake data ####
#### It assumes profile_pics folder to be present in the same directory as this file ####
#### It assumes that the database is already created ####
#### It assumes that the tables are already created and are empty ####
#### It assumes payment_images folder to be present in the same directory as this file ####

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Teamwork123",
  database="Coinfun_database"
)

# Define the list of available cryptocurrencies
CRYPTO_LIST = ['BTC', 'ETH', 'BNB', 'DOGE', 'XRP', 'MATIC', 'ADA', 'SOL']
CRYPTO_PRICE = {'BTC': 25000, 'ETH': 2000, 'BNB': 320, 'DOGE': 0.08, 'XRP': 0.5, 'MATIC': 0.6, 'ADA': 0.4, 'SOL': 20}


# Define the range for USDT and in_bid_usdt
USDT_RANGE = (5000, 50000)
IN_BID_USDT_RANGE = (0, 10000)

mycursor = mydb.cursor()            # Code assumes profile_pics folder to be present in the same directory as this file

KYC_users = []
      
# Insert fake data into trading history table i.e. table with table name = table_name (Helper Function)

def insert_fake_trading_history_data(email_id):
    wallet_ = {'USDT': 100000000000}
    for crypto in CRYPTO_LIST:
          wallet_[crypto] = 0

    # generate 5 to 50 transactions
    if(random.randint(0,1)==0):
      num_transactions = random.randint(2, 6)
    else:
      num_transactions = random.randint(10,40)
    
    last_transaction_time = datetime.now() - timedelta(weeks=1)

    for i in range(num_transactions):
        # randomly select a crypto for this transaction
        crypto = random.choice(list(CRYPTO_PRICE.keys()))
        
        # randomly select order type (buy or sell)
        order_type = random.choice(['BUY', 'SELL'])
        if(wallet_[crypto]<=0.0001):
          order_type = 'BUY'
        
        # determine amount of crypto to buy/sell
        if order_type == 'BUY':
            crypto_price = CRYPTO_PRICE[crypto] * random.uniform(0.95, 1.05)
            usdt_spent = random.randint(100, 10000)
            crypto_amount = usdt_spent / crypto_price
            wallet_['USDT'] -= usdt_spent
            wallet_[crypto] += crypto_amount
        else:
            crypto_price = CRYPTO_PRICE[crypto] * random.uniform(0.95, 1.05)
            crypto_amount = random.uniform(0.01, wallet_[crypto])
            usdt_earned = crypto_price * crypto_amount
            wallet_['USDT'] += usdt_earned
            wallet_[crypto] -= crypto_amount

        # determine timestamp
        if i == 0:
            timestamp = last_transaction_time
        else:
            timestamp = last_transaction_time + timedelta(minutes=random.randint(30, 60))

        # MySQL query to insert data into the CryptoTradingHistoryData table
        sql = "INSERT INTO CryptoTradingHistoryData (email_id, crypto_name, crypto_price, order_type, crypto_amount, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        val = (email_id, crypto, crypto_price, order_type, crypto_amount, timestamp)
        mycursor.execute(sql, val)
        mydb.commit()
        
        last_transaction_time = timestamp
    wallet_['USDT'] = round(random.uniform(*USDT_RANGE), 2)
    
    return wallet_


def generate_fake_userinfo_p2pbidding_crptotradinghistory_data(num_users):
    # Insert 20 fake users in userinfo table
    # having columns as email_id, username, password, wallet, favourites, profile_pic, kyc, contact
    for i in range(1, num_users+1):
        # Define user data
        username = f"Person{i}"
        email_id = f"{username.lower()}@gmail.com"
        kyc = True
        contact = "9" + str(random.randint(100000000000, 999999999999))
        favourites = random.sample(CRYPTO_LIST, random.randint(0, len(CRYPTO_LIST)-2))
        favourites = ",".join(favourites)
        password = encrypt_password(username+username)
        
        # Select profile picture for the user based on their username
        profile_pic_path = os.path.join("profile_pics",f"{username}.jpg")  # must be stable!
        #profile_pic_path = f"profile_pics/{username}.jpg"    # works fine in laptop, but may get unstable
        if os.path.exists(profile_pic_path):
            profile_pic_path = f"profile_pics/{username}.jpg"
        if not os.path.exists(profile_pic_path):
            profile_pic_path = f"profile_pics/blank.jpg"
            if(random.randint(0,100)<25):
              kyc = False
        
        # Allocate random wallet currencies and amounts for the user
        wallet = {}
        for crypto in CRYPTO_LIST:
          wallet[crypto] = 0
        
        if(kyc):
          for crypto in random.sample(CRYPTO_LIST, random.randint(2, len(CRYPTO_LIST))):
              wallet[crypto] = round(random.uniform(0.01, 10), 2)
          wallet['USDT'] = round(random.uniform(*USDT_RANGE), 2)
          if(random.randint(0,100)<30):
            wallet['USDT_in_bid'] = round(random.uniform(*IN_BID_USDT_RANGE), 2)  # Will sell in P2P (30% sellers of USDT)
          else:
            wallet['USDT_in_bid'] = 0   # Buyer in P2P (70% max buyers)
        else:
          wallet['USDT'] = 0            # No entry in P2P
          wallet['USDT_in_bid'] = 0
        
        #print(username, email_id, kyc, contact, password, favourites)
        #print("Initial random wallet",wallet)
        
        # Insert the user data into the database
        sql = "INSERT INTO userinfo (email_id, username, password, wallet, favourites, profile_pic, kyc, contact) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (email_id, username, password, json.dumps(wallet), favourites, (read_n_write_image_with_sql.convert_to_writable(profile_pic_path)).decode("UTF-8"), kyc, contact)
        mycursor.execute(sql, val)
        mydb.commit()   # userinfo table done 
        
        
        if(kyc==True and wallet['USDT_in_bid']==0 and random.randint(1,100)<50 ):
          buy_type = True                         ## Approx 30% people are buyers in P2PBiddingData
          transaction_usdt = random.uniform(1000, 10000)
          price = random.uniform(70,90)
          upper_limit = price* transaction_usdt
          lower_limit = random.uniform(0.5,0.75)*upper_limit
          payment_method = random.choice(['UPI', 'Bank Transfer', 'IMPS', 'Credit Card'])
          sql = "INSERT INTO P2PBiddingData (email_id, buy_type, transaction_usdt, price, payment_method, lower_limit, upper_limit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
          val = (email_id, buy_type, transaction_usdt, price, payment_method, lower_limit, upper_limit)
          mycursor.execute(sql, val)
          mydb.commit()
        elif(kyc==True and wallet['USDT_in_bid']!=0):
          buy_type = False                         ## Approx 30% people are sellers in P2PBiddingData
          transaction_usdt = wallet['USDT_in_bid']
          price = random.uniform(90,100)
          upper_limit = price* transaction_usdt
          lower_limit = random.uniform(0.5,0.75)*upper_limit
          payment_method = random.choice(['UPI', 'Bank Transfer', 'IMPS', 'Credit Card'])
          sql = "INSERT INTO P2PBiddingData (email_id, buy_type, transaction_usdt, price, payment_method, lower_limit, upper_limit) VALUES (%s, %s, %s, %s, %s, %s, %s)"
          val = (email_id, buy_type, transaction_usdt, price, payment_method, lower_limit, upper_limit)
          mycursor.execute(sql, val)
          mydb.commit()
        #print("P2PBiddingData table data addition done")
        # P2PBiddingData table done
        
        # Making table for history of crypto trading for each user and updating the wallet sensibly
        if(kyc==True):
          wallet_final = insert_fake_trading_history_data(email_id)
          for item in wallet_final:
              wallet[item] = wallet_final[item]
          # update userinfo table with new wallet
          query = "UPDATE userinfo SET wallet = %s WHERE email_id = %s"
          values = (json.dumps(wallet), email_id)
          mycursor.execute(query, values)
          mydb.commit()
          KYC_users.append(email_id)

        print(f"User {username} added to database")
          
def generate_chat_object(id1, id2):
    chat = {}
    messages = []
    
    # First message
    first_sender = random.choice([id1, id2])
    messages.append({"sender": first_sender, 
                     "message": random.choice(["Hi", "Hello", "How are you?"]), 
                     "image": None,
                     "timestamp": datetime.now().isoformat() })
    
    # Second message
    second_sender = id1 if first_sender == id2 else id2
    image_path = os.path.join("payment_images", random.choice(os.listdir("payment_images")))

    image_type = os.path.splitext(image_path)[1][1:]
    image_data_b64 = read_n_write_image_with_sql.convert_to_writable(image_path)
    
    next_timestamp = datetime.now() + timedelta(minutes=1)
    
    messages.append({"sender": second_sender, 
                     "message": None, 
                     "image": {"name": os.path.basename(image_path), "type": image_type, "data": image_data_b64.decode('UTF-8') },
                     "timestamp": next_timestamp.isoformat() })
    
    # Third message
    next_timestamp = datetime.now() + timedelta(minutes=2)
    
    third_sender = first_sender
    messages.append({"sender": third_sender, 
                     "message": random.choice(["Thanks, released!", "Released", "Releasing"]), 
                     "image": None,
                     "timestamp": next_timestamp.isoformat()  })
    
    # Fourth message
    next_timestamp = datetime.now() + timedelta(minutes=3)
    
    fourth_sender = second_sender
    messages.append({"sender": fourth_sender, 
                     "message": "Thanks", 
                     "image": None,
                     "timestamp": next_timestamp.isoformat() })
    
    # Add all messages to the chat object
    chat["messages"] = messages    
    return chat

def generate_fake_P2PTradeHistoryData_chat(datasize):
  chat_done = defaultdict(bool)
  for temp in range(2*data_size):
    random_emails = random.sample(KYC_users, 2)
    buyer_email_id = random_emails[0]
    seller_email_id = random_emails[1]
    
    # generate random transaction usdt and price
    transaction_usdt = round(random.uniform(500, 2000), 2)
    price = round(random.uniform(87, 92), 2)
    
    # generate a random timestamp within the last two weeks
    now = datetime.now()
    past_date = now - timedelta(days=random.randint(0, 13), hours=random.randint(0, 23), minutes=random.randint(0, 59))
    timestamp = past_date.strftime('%Y-%m-%d %H:%M:%S')
    
    # SQL query to insert data into the P2PTradeHistoryData table
    sql = f"INSERT INTO P2PTradeHistoryData (buyer_email_id, seller_email_id, transaction_usdt, price, time_stamp) VALUES ('{buyer_email_id}', '{seller_email_id}', {transaction_usdt}, {price}, '{timestamp}')"
    # execute the query
    mycursor.execute(sql)
    mydb.commit()
    
    if(buyer_email_id>seller_email_id):
      buyer_email_id, seller_email_id = seller_email_id, buyer_email_id

    if(chat_done[(buyer_email_id, seller_email_id)]==False):
      chat_done[(buyer_email_id, seller_email_id)] = True
      chat = generate_chat_object(buyer_email_id, seller_email_id)
      sql = "INSERT INTO chat (email_id1, email_id2, chat_messages) VALUES (%s, %s, %s)"
      val = (buyer_email_id, seller_email_id, json.dumps(chat))
      mycursor.execute(sql, val)
      mydb.commit()
    print("P2PTradeHistoryData and chat table data addition done for ", buyer_email_id, seller_email_id)
        
data_size = 45
generate_fake_userinfo_p2pbidding_crptotradinghistory_data(data_size)
print("3 tables done")
generate_fake_P2PTradeHistoryData_chat(data_size)
