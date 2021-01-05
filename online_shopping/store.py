# import functools
import json
from online_shopping.db import get_db

# import psycopg2.extras

from flask import Blueprint, current_app
# from flask import flash
# from flask import g
# from flask import redirect
from flask import render_template

# from flask import request
# from flask import session
# from flask import url_for
# from werkzeug.security import check_password_hash
# from werkzeug.security import generate_password_hash
# from flaskr.db import get_db

bp = Blueprint('store', __name__)


def get_categories():
    with open('categories.json') as f:
        json_categories = json.load(f)

    categories = []

    for group in json_categories:
        if group.subcategoies:
            for item in group.subcategoies:
                categories.append(group['name'] + ' / ' + item['name'])
        else:
            categories.append(group['name'])

    return categories


def get_category(full_category):
    category_name = full_category.split('/')
    return category_name[0]


@bp.route('/', methods=["GET", "POST"])
def home():
    categories = get_categories()
    db = get_db
    full_category = []
    for cat in categories:
        pro = list(db.products.find({'category': {'$regex': cat}}, {'$orderby': {'date': -1}})).limit(5)
        full_category.append({'single_category': category.split('/')[0],
                              'category': category,
                              'products': pro})
    return render_template('blog/index.html', categories=full_category)


def get_single_category(cat):
    with open('categories.json') as f:
        json_categories = json.load(f)

    db = get_db
    single_cat = cat.split('/')[-1].strip()
    products = list(db.products.find({'category': {'$regex': cat}}))

    categories_of_single = {}
    for group in json_categories:
        if group.subcategoies and group['name'] == single_cat:
            for item in group.subcategoies:
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
                           cat=page_category_name)


@bp.route("/product/<id>")
def product():
    return render_template('blog/product.html')
