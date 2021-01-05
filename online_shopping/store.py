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
        pro = list(db.products.find({'category': {'$regex': cat}}).sort({'$date': -1}))
        full_category.append({'single_category': category.split('/')[0],
                              'category': category,
                              'products': pro})
    return render_template('blog/index.html', categories=full_category)


@bp.route("/category/<category_name>")
def category():
    return render_template('blog/products.html')


@bp.route("/product/<id>")
def product():
    return render_template('blog/product.html')
