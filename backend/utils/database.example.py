import os
from pymongo import MongoClient

uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(uri)
db = client[os.getenv("DB_NAME", "mydatabase")]

def get_collection(collection: str):
    return db[collection]
