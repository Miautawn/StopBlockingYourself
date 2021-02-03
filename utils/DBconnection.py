from utils import credentials as CRED
import mysql.connector
from mysql.connector import errorcode

def connect():
    try:
        DBconnection = mysql.connector.connect(**CRED.CONFIG)
    except mysql.connector.Error as err:
        if(err.errno == errorcode.ER_ACCESS_DENIED_ERROR):
             print("ACCESS DENIED")
        else: print(err)
        print("Failed to connect to the database, exiting...")
        quit(1)
    else: return DBconnection



