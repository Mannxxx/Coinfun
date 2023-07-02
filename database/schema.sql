CREATE DATABASE Coinfun_database;
USE Coinfun_database;

CREATE TABLE userinfo (
 email_id VARCHAR(50) NOT NULL PRIMARY KEY,
 username VARCHAR(50) NOT NULL,
 password VARCHAR(255) NOT NULL,
 wallet JSON NOT NULL,
 favourites TEXT,
 profile_pic MEDIUMBLOB,
 kyc BOOLEAN NOT NULL DEFAULT 0,
 contact VARCHAR(20) NULL
);

CREATE TABLE chat (
 email_id1 VARCHAR(50),
 email_id2 VARCHAR(50),
 chat_messages JSON,
 PRIMARY KEY (email_id1, email_id2),
 FOREIGN KEY (email_id1) REFERENCES userinfo(email_id),
 FOREIGN KEY (email_id2) REFERENCES userinfo(email_id)
);

CREATE TABLE P2PTradeHistoryData (
 order_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
 buyer_email_id VARCHAR(50) NOT NULL,
 seller_email_id VARCHAR(50) NOT NULL,
 transaction_usdt DOUBLE NOT NULL,
 price DOUBLE NOT NULL,
 time_stamp DATETIME NOT NULL,
 FOREIGN KEY  (buyer_email_id) REFERENCES userinfo(email_id),
 FOREIGN KEY (seller_email_id) REFERENCES userinfo(email_id)
);

CREATE TABLE P2PBiddingData (
 email_id VARCHAR(50) NOT NULL,
 buy_type BOOLEAN NOT NULL,
 transaction_usdt DOUBLE NOT NULL DEFAULT 0,
 price DOUBLE NOT NULL DEFAULT 0,
 payment_method VARCHAR(50) NOT NULL,
 lower_limit DOUBLE NOT NULL,
 upper_limit DOUBLE NOT NULL,
 FOREIGN KEY (email_id) REFERENCES userinfo(email_id)
);

CREATE TABLE CryptoTradingHistoryData (
    email_id VARCHAR(50) NOT NULL,
    crypto_name VARCHAR(50) NOT NULL,
    crypto_price DECIMAL(10,4) NOT NULL,
    order_type VARCHAR(4) NOT NULL,
    crypto_amount DECIMAL(18,4) NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    FOREIGN KEY (email_id) REFERENCES userinfo(email_id)
);
