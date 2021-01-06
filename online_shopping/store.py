# import functools
import json

import pymongo

from online_shopping.db import get_db

# import psycopg2.extras


# from flask import flash
# from flask import g
# from flask import redirect
from flask import render_template, Blueprint

# from flask import request
# from flask import session
# from flask import url_for
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash
# from flaskr.db import get_db

bp = Blueprint('store', __name__)


def get_categories():
    with open('instance/categories.json',encoding='utf-8') as f:
        json_categories = json.load(f)

    categories = []

    for group in json_categories:
        if group['subcategories']:
            for item in group['subcategories']:
                categories.append(group['name'] + ' / ' + item['name'])
        else:
            categories.append(group['name'])

    return categories


@bp.route('/', methods=["GET", "POST"])
def home():
    categories = get_categories()
    db = get_db()
    full_category = []
    for cat in categories:
        # pro = list(db.products.find({'category': {'$regex': cat}}, {'$orderby': {'date': -1}}).limit(5))
        pro = list(db.products.find({'category': {'$regex': cat}}).sort("date", pymongo.DESCENDING).limit(4))
        full_category.append({'single_category': cat.split('/')[-1],
                              'category': cat,
                              'products': pro})

    return render_template('blog/index.html', categories=full_category)


def get_single_category(cat):
    with open('categories.json', encoding='utf-8') as f:
        json_categories = json.load(f)

    db = get_db
    single_cat = cat.split('/')[-1].strip()
    products = list(db.products.find({'category': {'$regex': cat}}))

    categories_of_single = {}
    for group in json_categories:
        if group['subcategories'] and group['name'] == single_cat:
            for item in group['subcategories']:
                categories_of_single[item['name']] = []

    for thing in products:
        thing_category = thing['category'].split('/')[0].strip()
        categories_of_single[thing_category].append(thing)

    return categories_of_single


@bp.route("/category/<category_name>")
def category(category_name):
    db = get_db
    side_cat_pro_name = get_single_category(category_name)
    page_products = list(db.products.find({{'category': {'$regex': category_name}}, {'$orderby': {'date': -1}}}))
    page_category_name = category_name.split('/')[0]
    return render_template('blog/products.html', side_categories=side_cat_pro_name,
                           page_category=page_products,
                           cat=page_category_name,
                           cat_category=category_name)


@bp.route("/product/<id>")
def product(id):
    db = get_db
    pro = list(db.products.find({'_id': id}))
    return render_template('blog/product.html', product=pro)


@bp.route("/cart")
def cart():
    db = get_db
    pro = list(db.products.find())
    return render_template('blog/cart.html', product=pro)