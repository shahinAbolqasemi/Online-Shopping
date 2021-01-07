# import functools
import json

import pymongo
from bson import ObjectId
from pymongo import MongoClient

from online_shopping.db import get_db

# import psycopg2.extras


# from flask import flash
# from flask import g
# from flask import redirect
from flask import render_template, Blueprint, session

# from flask import request
# from flask import session
# from flask import url_for
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash
# from flaskr.db import get_db

bp = Blueprint('store', __name__)


def get_categories():
    with open('instance/categories.json', encoding='utf-8') as f:
        json_categories = json.load(f)

    categories = []

    for group in json_categories:
        if group['subcategories']:
            for item in group['subcategories']:
                categories.append(group['name'] + '/' + item['name'])
        else:
            categories.append(group['name'])

    return categories


@bp.route('/', methods=["GET", "POST"])
def home():
    categories = get_categories()
    # client = MongoClient('localhost', 27017)
    db = get_db()
    full_category = []
    for cat in categories:
        pro = list(db.products.find({'category': {'$regex': cat}}).sort("date", pymongo.DESCENDING).limit(4))
        full_category.append({'single_category': cat.split('/')[-1],
                              'category': cat,
                              'products': pro})

    return render_template('blog/index.html', categories=full_category)


def get_single_category(cat):

    with open('instance/categories.json', encoding='utf-8') as f:
        json_categories = json.load(f)
    client = MongoClient('localhost', 27017)
    db = client.online_shopping
    single_cat = cat.split('/')[0]
    products = list(db.products.find({'category': {'$regex': cat}}))

    categories_of_single = {}
    for group in json_categories:
        if group['subcategories'] and group['name'] == single_cat:
            for item in group['subcategories']:
                categories_of_single[item['name']] = []

    for thing in products:
        thing_category = thing['category'].split('/')[-1]
        categories_of_single[thing_category].append(thing)

    return categories_of_single


@bp.route("/category/<category_name>")
def category(category_name):
    client = MongoClient('localhost', 27017)
    db = client.online_shopping
    side_cat_pro_name = get_single_category(category_name)
    page_products = list(db.products.find({{'category': {'$regex': category_name}}}).sort("date", pymongo.DESCENDING))
    page_category_name = category_name.split('/')[0]
    return render_template('blog/products.html', side_categories=side_cat_pro_name,
                           page_category=page_products,
                           cat=page_category_name,
                           cat_category=category_name)


@bp.route("/product/<product_id>", methods=["GET", "POST"])
def product(product_id):
    client = MongoClient('localhost', 27017)
    db = client.online_shopping
    pro = db.products.find({'_id': ObjectId(product_id)})
    return render_template('blog/product.html', product=pro)


@bp.route("/cart/<product_id")
def cart(product_id):
    if product_id is None:
        return render_template('blog/cart.html', product=session["product_list"])
    else:
        for item in session['product_list']:
            if session['product_list'][item][product_id] == product_id:
                session['product_list'].remove(item)
