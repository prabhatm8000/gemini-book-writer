import mysql.connector
from mysql.connector import errorcode
import dotenv
import os

dotenv.load_dotenv()

config = {
    "user": os.getenv("AIVEN_MYSQL_USER"),
    "password": os.getenv("AIVEN_MYSQL_PASSWORD"),
    "host": os.getenv("AIVEN_MYSQL_HOST"),
    "port": os.getenv("AIVEN_MYSQL_PORT"),
    "database": os.getenv("AIVEN_MYSQL_DB_NAME")
}

mydb = None
try:
    mydb = mysql.connector.connect(
        **config
    )
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

