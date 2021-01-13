# import functools
import json
import pymongo
from bson import ObjectId
from online_shopping.db import get_db

# import psycopg2.extras
# from flask import flash
# from flask import redirect
from flask import render_template, Blueprint, session, request, jsonify

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


def get_products_by_category(cat):
    db = get_db()
    return db.products.aggregate([
        {
            '$unwind': {
                'path': '$warehouses',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$match': {
                'warehouses.quantity': {
                    '$gt': 0
                },
                'category': {
                    '$regex': cat
                }
            }
        }, {
            '$group': {
                '_id': '$_id',
                'name': {
                    '$first': '$name'
                },
                'price': {
                    '$min': '$warehouses.price'
                },
                'category': {
                    '$first': '$category'
                },
                'description': {
                    '$first': '$description'
                },
                'image': {
                    '$first': '$image'
                },
                'date': {
                    '$first': '$date'
                }
            }
        }, {
            '$sort': {
                'date': pymongo.DESCENDING
            }
        }
    ])


@bp.route('/', methods=["GET", "POST"])
def home():
    categories = get_categories()
    full_category = []
    for cat in categories:
        pro = list(get_products_by_category(cat).limit(4))
        full_category.append({'single_category': cat.split('/')[-1],
                              'category': cat,
                              'products': pro})

    return render_template('blog/home.html', categories=full_category)


def get_single_category(cat):
    with open('instance/categories.json', encoding='utf-8') as f:
        json_categories = json.load(f)
    single_cat = cat.split('/')[0]
    products = list(get_products_by_category(single_cat))

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
    side_cat_pro_name = get_single_category(category_name)
    page_products = list(get_products_by_category(category_name))
    page_category_name = category_name.split('/')[-1]
    return render_template('blog/category.html', side_categories=side_cat_pro_name,
                           page_products=page_products,
                           category_single=page_category_name)


def get_product(product_id):
    db = get_db()
    return db.products.aggregate([
        {
            '$match': {
                '_id': ObjectId(product_id)
            }
        }, {
            '$unwind': {
                'path': '$warehouses',
                'preserveNullAndEmptyArrays': True
            }
        }, {
            '$match': {
                'warehouses.quantity': {
                    '$gt': 0
                }
            }
        }, {
            '$sort': {
                'warehouses.price': pymongo.ASCENDING
            }
        }, {
            '$limit': 1
        }, {
            '$group': {
                '_id': '$_id',
                'name': {
                    '$first': '$name'
                },
                'description': {
                    '$first': '$description'
                },
                'category': {
                    '$first': '$category'
                },
                'image': {
                    '$first': '$image'
                },
                'warehouse_name': {
                    '$first': '$warehouses.name'
                },
                'price': {
                    '$first': '$warehouses.price'
                },
                'quantity': {
                    '$first': '$warehouses.quantity'
                }
            }
        }
    ])


@bp.route("/product/<product_id>", methods=["GET", "POST"])
def product(product_id):
    pro = get_product(product_id)
    return render_template('blog/product.html', product=pro)


@bp.route("/add_order", methods=['POST'])
def add_order():
    data = request.get_json()
    if "order_products" not in session:
        session["order_products"] = {}
    session["order_products"].append(data)
    session.modified = True
    num = len(session["order_products"])
    return jsonify({'badge_number': num})


@bp.route("/cart")
def cart():
    orders = []
    if 'order_products' not in session:
        session['order_products'] = {}
    else:
        for item in session['order_products']:
            orders.append({"product": get_product(item["id"]), "numbers": item["numbers"]})
    total_price = sum(order["product"]['price'] * order['number'] for order in orders)
    return render_template('blog/cart.html', orders=orders, total_price=total_price)


@bp.route("/delete_order_product", methods=['POST'])
def add_order():
    data = request.get_json()
    for item in session["order_products"]:
        if data['id'] in item:
            del session["order_products"][item]
            session.modified = True
            num = len(session["order_products"])
            return jsonify({'badge_number': num, 'status': 'success'})
    return jsonify({'status': 'success'})


@bp.route("/cart/approve")
def cart_approve():
    return render_template('blog/cart_approve.html', prosucts=orders)
