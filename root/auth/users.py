from pymongo import MongoClient

from root.config import Config

client = MongoClient(Config.MONGO_URI)
db = client["my_db"]
users_collection = db["users"]

def add_user(data):
    users_collection.insert_one(data)

def get_user(email):
    return users_collection.find_one({"email": email})

def update_user(data):
    users_collection.update_one({"email": data.email}, {"$set": data})
