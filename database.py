from flask import g
from secrets import MONGO_DB_CONNECT
import pymongo


def get_db():
    if "db" not in g:
        g.db = connect_to_database()
    return g.db


def connect_to_database():
    client = pymongo.MongoClient(MONGO_DB_CONNECT)
    return client
