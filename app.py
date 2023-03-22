from flask import Flask,render_template,request
import json
from geopy.geocoders import Nominatim
from datetime import datetime
from email_validator import validate_email,EmailNotValidError
from math import sin, cos, sqrt, atan2, radians
import pickle
from csv import writer
import pandas as pd
from csv import DictReader
import requests


app = Flask(__name__)

@app.route("/")
def main_pg():
	return render_template('main.html')

@app.route("/cc")
def cc_form():
	return render_template('index.html')

@app.route("/admin")
def dashboard():

    with open("records.csv", 'r') as f:
        dict_reader = DictReader(f)
        records_list = list(dict_reader)

    return render_template('admin.html',records_list = records_list )

@app.route('/submit',methods=['POST'])

def form_post(): 
    name 	= request.form.get("user_name")
    email 	= request.form.get("user_email")
    country = request.form.get("user_country")
    address = request.form.get("address2")

    # Python Program to Get IP Address
    # import socket
    # hostname = socket.gethostname()
    # IPAddr = socket.gethostbyname(hostname)

    # print("Your Computer Name is:" + hostname)
    # print("Your Computer IP Address is:" + IPAddr)



    response = requests.get('https://api64.ipify.org?format=json').json()
    # response_json = json.loads(response.read())
    ip_address = response["ip"]

    cust_response = requests.get(f'https://ipapi.co/{ip_address}/json/').json()
    # cust_response_json = json.loads(cust_response.read())

    ip_long = cust_response.get("longitude")
    ip_lat=cust_response.get("latitude")
    ip_country=cust_response.get("country")

    loc = Nominatim(user_agent="GetLoc")
    date = datetime.now()

    #email verific
    try:
        emailObject = validate_email(email)
        email_verific = 1
    except EmailNotValidError as e:
        email_verific = 3

    print(email_verific)

    # co-ords verific
    getLoc = loc.geocode(address)
    lat= getLoc.latitude
    long=getLoc.longitude

    R = 6373.0

    lat1 = radians(lat)
    lon1 = radians(long)
    lat2 = radians(ip_lat)
    lon2 = radians(ip_long)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c

    if ((ip_country == country) and (distance > 1000.0)):
        add_verific = 2
    elif ((ip_country != country) and (distance > 11000.0)):
        add_verific = 3
    else:
        add_verific = 1

    print(add_verific)

    #credit limit and no. of transactions per day checked my bank
    # prev data verific

    df = pd.read_csv('records.csv')

    df1 = df.set_index(['name', 'ip_address', 'prediction'])

    if ((ip_address in df1.index.levels[1])  and (1 in df1.index.levels[2])) == True:
        ip_verific=3

    elif ((name in df1.index.levels[0])  and (ip_address not in  df1.index.levels[1])) == True:
        ip_verific=2

    else:
        ip_verific=1

    print(ip_verific)

     #calculate risk-score
    risk_score = add_verific + ip_verific + email_verific
    if (risk_score == 9) or (risk_score == 8) or (risk_score == 7):
        risk_label="High risk"
        risk_verific = 3
    elif (risk_score == 6) or (risk_score == 5) or (risk_score == 4):
        risk_label="Low risk"
        risk_verific = 2
    else:
        risk_label="Legit"
        risk_verific = 1
         
    #prediction
    classifier= pickle.load(open('cc.pkl', 'rb'))

    prediction = classifier.predict([[add_verific, ip_verific, email_verific,risk_verific]])

    print(int(prediction))

    # db
    db_list = [name,ip_address,email,date,int(prediction),risk_label]
    with open('records.csv', 'a') as f_object:
    
        writer_object = writer(f_object)
        writer_object.writerow(db_list)
        f_object.close()

    if (int(prediction) == 0 and risk_verific == 1):
        pred_text = "Transaction Successful"

    else:
        pred_text = "Transaction Failed - Contact Admin"
        

    return render_template("index.html",pred_text = pred_text)  

  

  

if __name__ == '__main__':
	app.run()
