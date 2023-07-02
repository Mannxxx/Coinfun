import os
import random
import smtplib

def is_valid_domain(email):
    try:
        ## Takes a string as input a checks whether the email has valid domain or not
        valid_domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'hotmail.com' , 'iitd.ac.in']
        domain = email.split('@')[-1]
        if domain in valid_domains:
            return True
        else:
            return False
    except Exception as e:
        raise Exception("Couldn't validate email domain")

def send_otp(receiver_email):
    # Try to log in to server and send email
    try:
        if(is_valid_domain(receiver_email)== False ):
            raise("Invalid Email Domain")
        # Get the absolute path of the directory where this script is located
        script_directory = os.path.dirname(os.path.abspath(__file__))
        
        # Read the sender's email address and password from the text file
        with open(os.path.join(script_directory, 'gmail_info.txt'), 'r') as f:
            sender_email, sender_password = f.read().strip().split('\n')
        
        # Generate a random 6-digit OTP
        otp = random.randint(100000, 999999)
        
        message = [
            'Subject: Your Coinfun Verification OTP\n\n',
            f'Hello,\n\nYour OTP is {otp}.\n\n',
            'If you did not request an OTP, please ignore this email.',
            'Also, please do not share this OTP with anyone, as it can be used to access your Coinfun account.',
            'Please be aware that trading involves risk, and you could lose money. Before making any trades, please read our risk disclaimer.\n\n',
            'Thank you,\nCoinfun Team\n\n\n' ,
            'Risk Warning: Digital asset prices are subject to high market risk and price volatility. ' ,
            'The value of your investment can go down or up, and you may not get back the amount invested. ' ,
            'You are solely responsible for your investment decisions and Coinfun is not liable for any losses you may incur. ' ,
            'Past performance is not a reliable predictor of future performance. You should only invest in products ' ,
            'you are familiar with and where you understand the risks. You should carefully consider your investment ' ,
            'experience, financial situation, investment objectives and risk tolerance and consult an independent ' ,
            'financial adviser prior to making any investment. This material should not be construed as financial advice.\n' ,
            'This is an automated email. Please do not reply to this email.' 
        ]
        
        # Connect to the SMTP server and send the message
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email.lower() , "".join(message))
            server.quit()
        return otp  # Return the OTP to the caller
    except Exception as e:
        raise Exception("Couldn't Send OTP to given email")

#send_otp("abcdefgh@gmail.com")
