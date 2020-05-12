import pymongo
import os

MONGO_DB_CONNECT = "mongodb+srv://py_openData:RaGEwX7Y6W9mckZD@firstcluster-v01yi.mongodb.net/test?retryWrites=true&w=majority"

client = pymongo.MongoClient(MONGO_DB_CONNECT)
db = client.openData

