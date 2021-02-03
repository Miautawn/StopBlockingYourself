from flask import Flask, render_template, request, redirect
import json
from utils import DBconnection, DBoperations
from utils import credentials
import datetime

#Database connection
DB = DBconnection.connect()
DBoperations.DBconnection = DB

app = Flask(__name__)

def post_time(entered_seconds):
    current_time = datetime.datetime.now()
    expiration_time = current_time + datetime.timedelta(seconds = int(entered_seconds))

    values = {
    "ip": request.remote_addr,
    "start_time": current_time.strftime("%Y-%m-%d %H:%M:%S"),
    "end_time": expiration_time.strftime("%Y-%m-%d %H:%M:%S")}
    DBoperations.insert_ip(values)



@app.route("/", methods=["POST", "GET"])
def index():
    if(request.method == "POST"):
        post_time(request.form["entered_time"])
        return redirect("/")
    else:
        ip_status = DBoperations.is_ip_blacklisted(request.remote_addr)
        if(ip_status["isBlacklisted"] == True):
            return render_template("blocked.html", seconds = ip_status["remaining_time"])
        else: return render_template("home.html")
        
#Starting up the website
if(__name__ == "__main__"):
    app.run(host = credentials.WEB_HOST_IP, port =credentials.WEB_HOST_PORT, debug = True)





