import pymongo
import pytz
from bson import CodecOptions
from flask import g, current_app


def get_db(collection=None):
    if 'db' not in g and collection is None:
        g.db = pymongo.MongoClient(current_app.config["CONNECTION_STRING_MDB"]).online_shopping
    elif 'db' not in g:
        codec_options = CodecOptions(tz_aware=True, tzinfo=pytz.timezone("Asia/Tehran"))
        g.db = pymongo.MongoClient(current_app.config["CONNECTION_STRING_MDB"]).online_shopping.get_collection(
            collection, codec_options=codec_options)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)


def init_app(app):
    """Register database functions with the Flask app. This is called by
    the application factory.
    """
    app.teardown_appcontext(close_db)
