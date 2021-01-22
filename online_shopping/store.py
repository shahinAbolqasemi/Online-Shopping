import json
import pymongo
from bson import ObjectId
from online_shopping.db import get_db
from datetime import datetime
from flask import render_template, Blueprint, session, request, jsonify, current_app
from bson.decimal128 import Decimal128, create_decimal128_context
import decimal

bp = Blueprint('store', __name__)


def get_categories():
    with open('instance/categories.json', encoding='utf-8') as f:
        json_categories = json.load(f)

    categories = []

    for group in json_categories:
        if group['subcategories']:
            for item in group['subcategories']:
                categories.append(item['name'])
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
        pro = list(get_products_by_category(cat))
        full_category.append({'single_category': cat,
                              'products': pro})

    if "order_products" not in session:
        session["order_products"] = []
    num = len(session["order_products"])

    return render_template('blog/home.html', categories=full_category, badge_num=num)


def get_single_category():
    with open('instance/categories.json', encoding='utf-8') as f:
        json_categories = json.load(f)

    db = get_db()
    products = list(db.products.find())

    categories_of_single = {}
    for group in json_categories:
        if group['subcategories']:
            for item in group['subcategories']:
                categories_of_single[item['name']] = []

    for thing in products:
        thing_category = thing['category'].split('/')[-1]
        if categories_of_single[thing_category]:
            pro_details = {"id": thing["_id"], "name": thing["name"], "product_category": thing_category}
            categories_of_single[thing_category].append(pro_details)
        else:
            categories_of_single[thing_category] = []
            pro_details = {"id": thing["_id"], "name": thing["name"], "product_category": thing_category}
            categories_of_single[thing_category].append(pro_details)

    return categories_of_single


@bp.route("/category/<category_name>/")
def category(category_name):
    side_cat_pro_name = get_single_category()
    page_products = list(get_products_by_category(category_name))

    if "order_products" not in session:
        session["order_products"] = []
    num = len(session["order_products"])

    return render_template('blog/category.html', side_categories=side_cat_pro_name,
                           page_products=page_products,
                           category_single=category_name, badge_num=num)


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


@bp.route("/product/<product_id>/", methods=["GET", "POST"])
def product(product_id):
    pro = get_product(product_id)
    pro = [i for i in pro][0]
    cat = pro["category"].split('/')[-1]

    if "order_products" not in session:
        session["order_products"] = []
    num = len(session["order_products"])

    return render_template('blog/product.html', product=pro, pro_category=cat, badge_num=num)


@bp.route("/order/add/", methods=['POST'])
def add_order():
    data = request.form

    if "order_products" not in session:
        session["order_products"] = []
    product_info = {"number": data.get('numbers'), "id": data.get('id')}
    session["order_products"].append(product_info)
    session.modified = True

    num = len(session["order_products"])

    return jsonify(result=num)


@bp.route("/cart/", methods=["GET", "POST"])
def cart():
    orders = []
    if 'order_products' not in session:
        session['order_products'] = []
    else:
        for item in session['order_products']:
            orders.append({"product": list(get_product(item["id"]))[0], "number": item["number"]})

    D128_CTX = create_decimal128_context()
    with decimal.localcontext(D128_CTX):
        total_price = sum(
            [order["product"]['price'].to_decimal() * Decimal128(order['number']).to_decimal() for order in orders])

    if "order_products" not in session:
        session["order_products"] = []
    num = len(session["order_products"])

    return render_template('blog/cart.html', orders=orders, total_price=total_price, badge_num=num)


@bp.route("/delete_order_product/", methods=['POST'])
def delete_order_product():
    data = request.form
    for item in session["order_products"]:
        if item["id"] == data.get('id'):
            session["order_products"].remove(item)
            session.modified = True
            break

    num = len(session["order_products"])

    return jsonify(result=num)


@bp.route("/cart/approve/")
def cart_approve():
    if "order_products" not in session:
        session["order_products"] = []
    num = len(session["order_products"])

    return render_template('blog/cart_approve.html', badge_num=num)


@bp.route("/order_final/", methods=['POST'])
def order_final():
    if session["order_products"]:
        data = request.form

        purchasedProductsId = []
        for item in session["order_products"]:
            pro = get_product(item['id'])
            purchasedProductsId.append(
                {"productId": ObjectId(pro["_id"]), "name": pro['name'], "warehouseName": pro['warehouse_name'],
                 "count": item['number'], "price": {"$numberDecimal": pro['price']}})

        total_price = sum([get_product(order['id'])['price'] * order['number'] for order in session["order_products"]])

        product_document = {"customerFirstName": data.get['first_name'], "customerLastName": data.get['last_name'],
                            "customerCellPhoneNum": data.get['telephone'], "address": data.get['address'],
                            "deliveryDate": {"$date": data.get['date']}, "amount": {"$numberDecimal": total_price},
                            "date": current_app.config['TEHRAN_TZ'].localize(datetime.now()),
                            'purchasedProductsId': purchasedProductsId}
        try:
            get_db('orders').insert_one(product_document)
        except Exception as ex:
            return jsonify({'status': "fail", 'exception': ex})
        else:
            session.pop('order_products', None)
            return jsonify({'status': "success"})
