import pymongo
from flask import g, current_app


# db = client.online_shopping

def get_db():
    if 'db' not in g:
        g.db = pymongo.MongoClient(current_app.config["CONNECTION_STRING_MDB"]).online_shopping
    return g.db


def close_db():
    db = g.pop('db', None)
