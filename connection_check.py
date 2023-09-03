from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://jinyoonok:jinyoon981023@cmpsc487-jinyoon.vuymlgv.mongodb.net/?retryWrites=true&w=majority"

# Create a new client and connect to the server
client = MongoClient(uri)

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")

    # Let's also print the names of all the databases
    print("Databases:", client.list_database_names())

except Exception as e:
    print(e)
