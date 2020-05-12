import pymongo
from flask import g

MONGO_DB_CONNECT = "mongodb+srv://py_openData:RaGEwX7Y6W9mckZD@firstcluster-v01yi.mongodb.net/test?retryWrites=true&w=majority"



def get_db():
    if 'db' not in g:
        g.db = connect_to_database()
    return g.db


def connect_to_database():
    client = pymongo.MongoClient(MONGO_DB_CONNECT)
    db = client.openData
    return db

