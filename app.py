from sqlalchemy import create_engine
from pymongo import MongoClient
client = MongoClient("mongodb://<hostname>:<port>")   #### please replace the db connection url as per your mongo db installed ('mongodb://localhost:27017')
database = "youtubescrp1"  #### keep this db name as it is dont change this
user=    #### replace it with your username for example user="root"
pw=   #### replace it with your password for example pw="root123"
engine1 = create_engine("mysql+pymysql://{user}:{pw}@<hostname>".format(user="xxxxx", pw="xxxxx123"))   #### replace hostname and username as per your installation 
engine = create_engine("mysql+pymysql://{user}:{pw}@<hostname>/{db}".format(user="xxxxx", pw="xxxxx123", db = database)) #### replace hostname and username as per your installation 
