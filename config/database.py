from pymongo import MongoClient
client = MongoClient("mongodb+srv://devashri:7AYjQVww7HocV6aq@cluster0.vq8huyc.mongodb.net/?retryWrites=true&w=majority")

db = client.cloud_service_db

subscription_collection = db["subscription_collection"]
user_collection = db["user_collection"]
collection_user_statistics = db["user_statistics"]

