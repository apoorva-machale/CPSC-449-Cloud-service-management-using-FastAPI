from fastapi import FastAPI
from routes.route import router
from routes.userRoutes import router as user_router

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

app.include_router(router)
app.include_router(user_router)