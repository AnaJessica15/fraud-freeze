from geopy.geocoders import Nominatim
from datetime import datetime
from email_validator import validate_email,EmailNotValidError
from math import sin, cos, sqrt, atan2, radians
# from pyspark.sql import SparkSession
import csv
import pandas as pd
# from pyspark.sql.functions import filter
# from pyspark.sql.functions import col
import pickle


classifier= pickle.load(open('cc.pkl', 'rb'))

# spark = SparkSession.builder.getOrCreate() 
df = pd.read_csv('records.csv')


# calling the Nominatim tool
loc = Nominatim(user_agent="GetLoc")
date = datetime.now()

 
# entering the location name
name="Ana"
getLoc = loc.geocode("Nagercoil")
email = "anajess@gmail.com"
country = "SG"
ip_lat = 43.1411
ip_long = -74.2444	
ip_country= "SG"
ip_cust="105.182.69.43"

#email verific
try:
    emailObject = validate_email(email)
    email_verific = 1
except EmailNotValidError as e:
    email_verific = 3

print(email_verific)

# co-ords verific

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

# df_result1 = pd.DataFrame()
# df_result2 = pd.DataFrame()

# df_result1 = df[(ip_cust in df["ip_address"].values)  & (df["is_fraud"] == "1")]
# df_result2 = df[(name in df["name"])  & (ip_cust not in df["ip_address"])]

# print(df_result1)
# print(df_result2)

df1 = df.set_index(['name', 'ip_address', 'is_fraud'])

# print('t4' in df1.index.levels[0])
# print('t4' in df1.index.levels[1])
# print('t4' in df1.index.levels[2])

if ((ip_cust in df1.index.levels[1])  and (1 in df1.index.levels[2])) == True:
    ip_verific=3

elif ((name in df1.index.levels[0])  and (ip_cust not in  df1.index.levels[1])) == True:
    ip_verific=2

else:
    ip_verific=1

print(ip_verific)

# print((ip_cust in df1.index.levels[1])  and (1 in df1.index.levels[2]))

# if(add_verific+ip_verific+email_verific = )

prediction = classifier.predict([[add_verific, ip_verific, email_verific]])

print(prediction)




# output = df_result.toPandas()
# df_result.toPandas().to_csv('output.csv', index=False)

# data = pd.read_csv("output.csv")


