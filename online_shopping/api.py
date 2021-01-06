from bson import ObjectId
from flask import Blueprint, request, jsonify

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
    return jsonify(products)


@bp.route('/product/<product_id>/')
@login_required
def prod_details(product_id):
    product = get_db('products').find_one({'_id': ObjectId(product_id)})
    return jsonify(product)


@bp.route('/product/add/', methods=['POST'])
@login_required
def prod_add():
    product_document = {
        'name': request.form.get('prod-name'),
        'description': request.form.get('prod-desc'),
        'category': request.form.get('prod-category'),
        'image': request.form.get('prod-image'),
        'warehouses': request.form.get('prod-warehouses')
    }
    try:
        get_db('products').insert_one(product_document)
    except (Exception) as ex:
        return jsonify({'status': False})
    else:
        return jsonify({'status': True})


@bp.route('/product/edit/', methods=['POST'])
@login_required
def prod_edit():
    return ...


@bp.route('/product/delete/<int:product_id>/')
@login_required
def prod_delete(product_id):
    return ...


@bp.route('/product/add/', methods=['POST'])
@login_required
def prod_upload():
    return ...


@bp.route('/warehouse/list/')
@login_required
def ware_list():
    return ...


@bp.route('/warehouse/add/', methods=['POST'])
@login_required
def ware_add():
    return ...


@bp.route('/warehouse/edit/', methods=['POST'])
@login_required
def ware_edit():
    return ...


@bp.route('/warehouse/delete/<int:warehouse_id>/')
@login_required
def ware_delete(warehouse_id):
    return ...


@bp.route('/quantity/list/')
@login_required
def quantity_list():
    return ...


@bp.route('/quantity/add/', methods=['POST'])
@login_required
def quantity_add():
    return ...


@bp.route('/quantity/edit/', methods=['POST'])
@login_required
def quantity_edit():
    return ...


@bp.route('/quantity/delete/')
@login_required
def quantity_delete():
    product_id = request.args.get('product')
    warehouse_id = request.args.get('warehouse')
    return ...


@bp.route('/order/list/')
@login_required
def order_list():
    orders = list(get_db('orders').find())
    return jsonify(orders)


@bp.route('/order/<order_id>/')
@login_required
def order_details(order_id):
    order = get_db('orders').find_one({'_id': ObjectId(order_id)})
    return jsonify(order)
