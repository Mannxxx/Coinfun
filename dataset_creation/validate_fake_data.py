import mysql.connector
import io
import base64
from PIL import Image
import json

# Establish a connection to the MySQL server
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Teamwork123",
    database="Coinfun_database"
)

# Create a cursor object
cursor = db.cursor()

##### To see a profile pic in userinfo table


# Fetch the image data for person1 from the user_info table
email_id = "person1@gmail.com"
cursor.execute("SELECT profile_pic FROM userinfo WHERE email_id=%s", (email_id,))
image_data = cursor.fetchone()[0]
# print(image_data)
# Decode the base64 encoded image
decoded_image = base64.b64decode(image_data)

# Open the image using PIL
image = Image.open(io.BytesIO(decoded_image))
    
# Show the image
image.show()

# Close the cursor and database connections
cursor.close()
db.close()



##### To see a pic in chat between two

# Fetch the chat messages for two users
# email_id1 = "person16@gmail.com"
# email_id2 = "person7@gmail.com"
# cursor.execute("SELECT chat_messages FROM chat WHERE email_id1=%s AND email_id2=%s", (email_id1, email_id2))
# chat_messages = cursor.fetchall()[0][0]

# # Load the chat messages as a JSON object
# chat = json.loads(chat_messages)

# # Get the second message from the messages list
# second_message = chat["messages"][1]

# # Check if the second message has an image
# if second_message["image"]:
#     # Decode the base64 encoded image
#     image_data = io.BytesIO(base64.b64decode(second_message["image"]["data"]))
#     # Open the image using PIL
#     image = Image.open(image_data)
    
#     # Show the image
#     image.show()
# else:
#     print("The second message does not have an image.")

# # Close the cursor and database connections
# cursor.close()
# db.close()
