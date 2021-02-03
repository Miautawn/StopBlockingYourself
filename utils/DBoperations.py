from utils.credentials import TABLE_NAME
import datetime

DBconnection = None

def is_ip_blacklisted(ip):
    cursor = DBconnection.cursor()
    cursor.execute("SELECT * FROM {0} WHERE ip = '{1}'".format(TABLE_NAME, ip))
    search_results = cursor.fetchall()
    cursor.close()

    if(len(search_results) == 0): return {"isBlacklisted": False, "remaining_time":0}
    else: 
        if(is_time_expired(search_results[0][2])):
            delete_ip(ip)
            return {"isBlacklisted": False, "remaining_time":0}
        #returning the remaining time
        else:
            remaining_time = int((search_results[0][2] - datetime.datetime.now()).total_seconds())
            return {"isBlacklisted": True, "remaining_time": remaining_time}
        
    
def is_time_expired(end_time):
    if(datetime.datetime.now() > end_time): return True
    else: return False

def insert_ip(values):
    try:
        cursor = DBconnection.cursor()
        cursor.execute("INSERT INTO {0} VALUES ('{1}', '{2}', '{3}');".format(TABLE_NAME, values["ip"], values["start_time"], values["end_time"]))
    except: 
        print("An error occurred while inserting data")
        DBconnection.rollback()
    else:
        print("Successfully blacklisted an ip adress") 
        DBconnection.commit()
    finally: cursor.close()

def delete_ip(ip):
    try:
        cursor = DBconnection.cursor()
        cursor.execute("DELETE FROM {0} WHERE ip = '{1}'".format(TABLE_NAME, ip))
    except:
        print("An error ocurred while trying to delete data")
        DBconnection.rollback()
    else: 
        DBconnection.commit()
        print("Successfully deleted an ip address")
    finally: cursor.close()






