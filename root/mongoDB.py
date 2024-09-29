from pymongo import MongoClient

cluster = MongoClient("mongodb+srv://skhomyn12:Skhomyn123@cluster0.1tpyf.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

mongoDB = cluster["my_db"]
collection = mongoDB["my_collection"]
