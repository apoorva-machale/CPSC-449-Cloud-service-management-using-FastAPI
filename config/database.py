from pymongo import MongoClient
client = MongoClient("mongodb+srv://sundrifafu:CPSC449@cluster0.co8msb3.mongodb.net/?retryWrites=true&w=majority")

db = client.cloud_service_db

subscription_collection = db["subscription_collection"]
user_collection = db["user_collection"]
permission_collection = db["permission_collection"]
