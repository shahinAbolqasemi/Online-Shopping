from flask import *
import functools
from werkzeug.security import *
import json
from cryptography.fernet import Fernet
from pymongo import MongoClient
from bson.json_util import dumps
from bson import ObjectId
from online_shopping.db import get_db


# client = MongoClient('localhost', 27017)
# db = client.shop
db = get_db()
bp = Blueprint('admin', __name__, url_prefix='/admin')


def login_required(view):
    """View decorator that redirects anonymous users to the login page."""
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login"))

        return view(*args, **kwargs)

    return wrapped_view


@bp.before_app_request
def load_data():
    with open('instance/admins.json') as f:
        admins = json.load(f)
    key = current_app.config["ENCRYPT_KEY"]
    cipher_suite = Fernet(key.encode())
    admins_dict = {}
    for admin in admins:
        username = admin[0]
        password = admin[1]
        admins_dict[username] = cipher_suite.decrypt(password.encode()).decode()
    print(admins_dict)
    g.admins = admins_dict


def valid_admin(username, password):
    admins = g.admins
    if username in admins.keys():
        return password == admins[username]
    else:
        return 'invalid username'


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_admin(username, password):
            session.clear()
            session['admin'] = request.form['username']
            return redirect(url_for('admin.admin_orders'))

        elif valid_admin(username, password) == 'invalid username':
            error = 'Username not registered! :('

        else:
            error = 'Invalid Password'

        flash(error)

    return render_template('admin/login.html')


@bp.route('/logout/')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


# @bp.route('/products/')
# @login_required
# def admin_product():
#     prods = {'لوبیا قرمز گلستان 900 گرمی': 'مواد غذایی / کالاهای اساسی و خوار و بار',
#              'روغن سرخ کردنی سمن 1.35 کیلویی': 'مواد غذایی / کالاهای اساسی و خوار و بار',
#              'روغن مایع آفتابگردان حاوی ویتامین دی و ای': 'مواد غذایی / کاهای اساسی و خوار و بار',
#              'کره سنتی شکلی 100 گرمی': 'مواد غذایی / لبنیات',
#              'قهوه اسپرسو بن مانو مدل آرتیمان 250 گرمی': 'مواد غذایی / نوشیدنی'
#              }
#
# <<<<<<< HEAD
@bp.route('/products/', methods=['POST', 'GET'])
@login_required
def prods():
    # prods = {'لوبیا قرمز گلستان 900 گرمی' : 'مواد غذایی / کالاهای اساسی و خوار و بار',
    #      'روغن سرخ کردنی سمن 1.35 کیلویی' : 'مواد غذایی / کالاهای اساسی و خوار و بار',
    #      'روغن مایع آفتابگردان حاوی ویتامین دی و ای' : 'مواد غذایی / کاهای اساسی و خوار و بار',
    #      'کره سنتی شکلی 100 گرمی' : 'مواد غذایی / لبنیات',
    #      'قهوه اسپرسو بن مانو مدل آرتیمان 250 گرمی' : 'مواد غذایی / نوشیدنی'
    #      }
    #
    # return render_template('product.html', products=prods)
    if request.method == 'POST':
        prods = dumps(db.products.find(), indent=4)
        return prods


@bp.route('/inventory/', methods=['POST', 'GET'])
@login_required
def inventory():
    # invens = ['انبار شماره 1',
    #           'انبار شماره 2',
    #           'انبار شماره 3'
    #           ]
    # 
    # return render_template('inventory.html', inventories=invens)
    if request.method == 'POST':
        invens = dumps(db.inventory.find(), indent=4)
        return invens

@bp.route('/inventory/<str:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_inventory(id):
    if request.method == 'POST':
        name = request.form['name']
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            flash(error)

        else:
            db.inventory.update_one({'_id' : ObjectId(id)},
                                {'$set' : {'name' : name}},
                                    upsert=False)
        flash('Inventory edited.')

        invens = dumps(db.inventory.find(), indent=4)
        return invens

@bp.route('/inventory/<str:id>/delete', methods=['POST', 'GET'])
@login_required
def delete_inventory(id):
    if request.method == 'POST':
        db.inventory.delete_one({'_id' : ObjectId(id)})
        flash('Inventory deleted.')

        invens = dumps(db.inventory.find(), indent=4)
        return invens

@bp.route('/inventory/add', methods=['POST', 'GET'])
@login_required
def add_inventory():
    if request.method == 'POST':
        name = request.form['name']
        new_inv = {
            'name' : name
        }
        db.inventory.insert_one(new_inv)

        flash('Inventroy added.')
        invens = dumps(db.inventory.find(), indent=4)
        return invens



        

@bp.route('/price')
def price():
    pass


# =======
#     return render_template('admin/products.html', products=prods)


# @bp.route('/warehouses/')
# @login_required
# def admin_warehouse():
#     invens = ['انبار شماره 1',
#               'انبار شماره 2',
#               'انبار شماره 3'
#               ]
#
#     return render_template('admin/warehouses.html', inventories=invens)


@bp.route('/quantities/')
@login_required
def admin_quantity():
    return render_template('admin/quantities.html')

@bp.route('/orders', methods=['POST', 'GET'])
# >>>>>>> 31a37d04ca361e7a71b4556a7eec4f9b5bc33030
@login_required
def admin_orders():
    """get somethings from database """
    if request.method == 'POST':
        orders = dumps(db.orders.find(), indent=4)
        return orders


@bp.route('/orders/<str:id>/check-order', methods=['POST', 'GET'])
@login_required
def check_order(id):
    if request.method == 'POST':
        order = dumps(db.orders.find_one({'_id' : ObjectId(id)}), indent=4)
        return order

