from fastapi import FastAPI
from routes.subscriptionPlans import router as subscription_router
from routes.userRoutes import router as user_router
from routes.authentication import router as authentication_router
from routes.userSubscription import router as user_subscription_router

app = FastAPI()

#from pymongo.mongo_client import MongoClient
#from pymongo.server_api import ServerApi
#uri = "mongodb+srv://sundrifafu:CPSC449@cluster0.co8msb3.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
#client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
#try:
 #   client.admin.command('ping')
  #  print("Pinged your deployment. You successfully connected to MongoDB!")
#except Exception as e:
 #   print(e)

#@app.get('/')
#async def index():
 #   return{'hello': 'world'}

app.include_router(subscription_router)
app.include_router(user_router)
app.include_router(authentication_router)
app.include_router(user_subscription_router)