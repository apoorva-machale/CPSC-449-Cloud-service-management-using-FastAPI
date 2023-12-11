from pymongo import MongoClient
client = MongoClient("mongodb+srv://devashri:7AYjQVww7HocV6aq@cluster0.vq8huyc.mongodb.net/?retryWrites=true&w=majority")

db = client.cloud_service_db

subscription_collection = db["subscription_collection"]
user_collection = db["user_collection"]
collection_user_statistics = db["user_statistics"]


permission_collection = db["permission_collection"]

usage_collection = db["usage_collection"]

# Akshay - Usage Tracking Dummy Database

# Function to push dummy data into MongoDB for testing
def push_dummy_data():
    try:
        # Dummy subscription data
        dummy_subscription = {
            "name": "dummy_plan",
            "description": "Dummy subscription plan",
            "price": 10.0,
            "validityPeriod": "30 days",
            "apiPermissions": [
                {
                    "apiName": "weather_api",
                    "endpoint": "weather",
                    "maxUsageLimit": 5,
                }
            ]
        }

        # Insert dummy subscription data
        subscription_result = subscription_collection.insert_one(dummy_subscription)

        # Dummy user data with subscriptionPlanID
        dummy_user = {
            "username": "dummy_user",
            "email": "dummy@example.com",
            "role": "customer",
            "hashed_password": "dummy_hashed_password",
            "subscriptionPlanId": str(subscription_result.inserted_id)  # Get the ID of the inserted subscription
        }

        # Insert dummy user data
        user_collection.insert_one(dummy_user)

        # Dummy usage data
        dummy_usage = {
            "user_id": "dummy_user",
            "api_name": "dummy_api",
            "usage_count": 3,
        }
        usage_collection.insert_one(dummy_usage)

        print("Dummy data inserted successfully.")
    except Exception as e:
        print(f"Error inserting dummy data: {e}")

# Uncomment the line below to push dummy data into MongoDB
push_dummy_data()


