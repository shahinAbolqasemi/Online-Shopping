import pymongo
from flask import g, current_app


def get_db():
    if 'db' not in g:
        g.db = pymongo.MongoClient(current_app.config["CONNECTION_STRING_MDB"]).online_shopping
    return g.db


def close_db(e=None):
    db = g.pop('db', None)


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
