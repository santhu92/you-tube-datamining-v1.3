from sqlalchemy import create_engine
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017")
database = "youtubescrp1"
user="root"
pw="root123"
engine1 = create_engine("mysql+pymysql://{user}:{pw}@localhost".format(user="root", pw="root123"))
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format(user="root", pw="root123", db = database))