from flask import g
import os
import pymongo
import dns

MONGO_DB_CONNECT = os.environ["MONGO_DB_CONNECT"]

def get_db():
    if "db" not in g:
        try:
            g.db = connect_to_database()
            return g.db
        except dns.exception.Timeout:
            raise ValueError("Cannot connect to db")
        except pymongo.errors.ConfigurationError :
            raise ValueError("Cannot connect to db")
    


def connect_to_database():
    client = pymongo.MongoClient(MONGO_DB_CONNECT)
    return client
