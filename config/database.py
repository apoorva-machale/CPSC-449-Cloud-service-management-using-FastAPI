from pymongo import MongoClient
client = MongoClient("mongodb+srv://sundrifafu:CPSC449@cluster0.co8msb3.mongodb.net/?retryWrites=true&w=majority")

db = client.cloud_service_db

collection_name = db["subscription_collection"]