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
    products_collection = get_db().products
    res = list(products_collection.find({}, {"_id": 0}))
    return jsonify(res)


@bp.route('/product/<int:product_id>/')
@login_required
def prod_details(product_id):
    return ...


@bp.route('/product/add/', methods=['POST'])
@login_required
def prod_add():
    return ...


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
    return ...


@bp.route('/order/<int:order_id>/')
@login_required
def order_details(order_id):
    return ...
