import os
from datetime import datetime

from bson import ObjectId
from flask import Blueprint, request, jsonify, current_app, url_for, session
from werkzeug.utils import secure_filename, redirect

from online_shopping.admin import login_required
from online_shopping.db import get_db

bp = Blueprint('api', __name__, url_prefix='/api')


@bp.before_app_request
def load_():
    pass


@bp.route('/product/list/')
@login_required
def prod_list():
    products = list(get_db('products').find())
    return jsonify(data=products)


@bp.route('/product/<product_id>/')
@login_required
def prod_details(product_id):
    product = get_db('products').find_one({'_id': ObjectId(product_id)})
    return jsonify(data=product)


@bp.route('/product/add/', methods=['POST'])
@login_required
def prod_add():
    image_file = request.files.get('image')
    if image_file:
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('uploads', filename=filename)
    else:
        image_url = url_for('uploads', filename='default_product_image.jpg')

    product_document = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'category': request.form.get('category'),
        'date': current_app.config['TEHRAN_TZ'].localize(datetime.now()),
        'image': image_url
    }
    try:
        product_added = get_db('products').insert_one(product_document)
    except (Exception) as ex:
        return jsonify(status={'status': False})
    else:
        return jsonify(status={'status': True}, data={'productId': product_added['_id']})


@bp.route('/product/edit/', methods=['POST'])
@login_required
def prod_edit():
    products = get_db("products")
    product_id = request.form.get('productId')
    # if product_id := request.form.get('productId'):
    #     product = products.find_one({"_id": ObjectId(product_id)}, {"_id": 0})
    #     return jsonify(data=product)
    # else:
    product_document = {
        'name': request.form.get('name'),
        'description': request.form.get('description'),
        'category': request.form.get('category')
    }
    image_file = request.files.get('image')
    if image_file:
        filename = secure_filename(image_file.filename)
        image_file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
        image_url = url_for('uploads', filename=filename)
        product_document['image'] = image_url
    try:
        products = get_db('products').update({ObjectId(product_id)}, {"$set": product_document})
    except (Exception) as ex:
        return jsonify(status={'status': False})
    else:
        return jsonify(status={'status': True})


@bp.route('/product/delete/<productId>/')
@login_required
def prod_delete(productId):
    try:
        get_db("products").delete_one({"_id": ObjectId(productId)})
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/product/upload/', methods=['POST'])
@login_required
def prod_upload():
    products_collection = get_db('products')
    products_file = request.files.get('file')
    products_lines = products_file.read()
    product_keys = next(products_lines)
    products = []
    for i, product_line in enumerate(products_lines):
        products.append({})
        for elem, key in zip(product_line, product_keys.split(',')):
            products[i][key] = elem
    try:
        products_collection.insert_many(products)
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/warehouse/list/')
@login_required
def ware_list():
    warehouses = list(get_db('warehouses').find())
    return jsonify(data=warehouses)


@bp.route('/warehouse/add/', methods=['POST'])
@login_required
def ware_add():
    warehouse_name = request.form.get('name')
    try:
        warehouse_added = get_db("warehouses").insert_one({'name': warehouse_name})
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True}, data={'warehouseId': warehouse_added['_id']})


@bp.route('/warehouse/edit/', methods=['POST'])
@login_required
def ware_edit():
    warehouses = get_db('warehouses')
    warehouse_id = request.form.get('warehouseId')
    warehouse_name = request.form.get('name')
    # if warehouse_id := request.form.get('warehouseId'):
    #     warehouse = warehouses.find({"_id": ObjectId(warehouse_id)})
    #     return jsonify(data=warehouse)
    # else:
    try:
        warehouses.update_one({"_id": ObjectId(warehouse_id)}, {"$set": {"name": warehouse_name}})
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/warehouse/delete/<warehouseId>/')
@login_required
def ware_delete(warehouseId):
    try:
        get_db('warehouses').delete_one({"_id": ObjectId(warehouseId)})
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/quantity/list/')
@login_required
def quantity_list():
    products = get_db("products")
    quantities = products.aggregate([
        {
            '$unwind': {
                'path': '$warehouses',
                'preserveNullAndEmptyArrays': False
            }
        }, {
            '$project': {
                '_id': 0,
                'name': 1,
                'warehouses': 1
            }
        }
    ])
    return jsonify(data=list(quantities))


@bp.route('/quantity/add/', methods=['POST'])
@login_required
def quantity_add():
    products = get_db('products')
    # product_id = request.form.get('productId')
    warehouse_name = request.form.get('warehouseName')
    product_name = request.form.get('productName')
    # warehouse_id = request.form.get('warehouse-id')
    product_price = request.form.get('price')
    product_quantity = request.form.get('quantity')
    try:
        products.update_one({
            "_id": ObjectId(product_id)},
            {
                "$push": {
                    'warehouses': {'_id': ObjectId(warehouse_id), 'name': warehouse_name, 'price': product_price,
                                   'quantity': product_quantity}
                }
            })
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/quantity/edit/', methods=['POST'])
@login_required
def quantity_edit():
    products = get_db('products')
    product_id = request.form.get('productId')
    warehouse_id = request.form.get('warehouseId')
    product_name = request.form.get('product-name')
    warehouse_name = request.form.get('warehouse-name')
    product_price = request.form.get('product-price')
    product_quantity = request.form.get('product-quantity')
    try:
        products.update_one(
            {"_id": ObjectId(product_id), 'warehouses': {"$elemMatch": {"_id": ObjectId(warehouse_id)}}},
            {"$set": {
                "name": product_name,
                'warehouses.$': {
                    '_id': ObjectId(warehouse_id),
                    'name': warehouse_name,
                    'price': product_price,
                    'quantity': product_quantity
                }
            }}
        )
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/quantity/delete/')
@login_required
def quantity_delete():
    product_id = request.args.get('product')
    warehouse_id = request.args.get('warehouse')
    products = get_db("products")
    try:
        products.update_one({"_id": ObjectId(product_id)}, {"$pull": {"warehouses": {"_id": ObjectId(warehouse_id)}}})
    except (Exception) as ex:
        return jsonify(status={'success': False})
    else:
        return jsonify(status={'success': True})


@bp.route('/order/list/')
@login_required
def order_list():
    orders = list(get_db('orders').find())
    return jsonify(orders)


@bp.route('/order/<order_id>/')
@login_required
def order_details(order_id):
    order = get_db('orders').find_one({'_id': ObjectId(order_id)}, {'_id': 0})
    # aggregate(
    #     [
    #         {
    #             '$match': {'_id': ObjectId(order_id)}
    #         },
    #         {
    #             '$lookup': {
    #                 'from': 'products',
    #                 'localField': 'purchasedProductsId',
    #                 'foreignField': '_id',
    #                 'as': 'purchasedProductsId'
    #             }
    #         },
    #         {
    #             '$project': {
    #                 '_id': 0
    #             }
    #         }

    #     ]
    # )
    # data = order
    # data['']
    return jsonify(data=order)
