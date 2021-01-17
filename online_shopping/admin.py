import functools

from flask import (
    Blueprint, session, url_for, current_app, request, flash, render_template, g
)
from werkzeug.utils import redirect
from werkzeug.security import *
import json
from cryptography.fernet import Fernet
from online_shopping.db import get_db

# CONST for validation of admin
SUCCESS_AUTH = 0
INVALID_PASSWORD = 2
INVALID_USERNAME = 1

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
    if username in admins:
        if password == admins[username]:
            return SUCCESS_AUTH
        else:
            return INVALID_PASSWORD
    else:
        return INVALID_USERNAME


@bp.route('/login/', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_admin(username, password) == SUCCESS_AUTH:
            session.clear()
            session['admin'] = request.form['username']
            return redirect(url_for('admin.admin_orders'))
        elif valid_admin(username, password) == INVALID_USERNAME:
            flash('Username not registered! :(')
        else:
            flash('Invalid Password')
    elif "admin" in session:
        return redirect(url_for('admin.admin_orders'))

    return render_template('admin/login.html')

def get_categories():
    with open('instance/categories.json', encoding='utf-8') as f:
        categories = json.load(f)

    categories_list = []

    for category in categories:
        if category['subcategories']:
            for sub in category['subcategories']:
                categories_list.append(category['name'] + ' / ' + sub['name'])
        else:
            categories_list.append(category['name'])

    return categories_list

@bp.route('/logout/')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@bp.route('/products/')
@login_required
def admin_product():
    db = get_db()
    prods = list(db.products.find())
    categories = get_categories()
    return render_template('admin/products.html', products=prods, categories=categories)


@bp.route('/warehouses/')
@login_required
def admin_warehouse():
    db = get_db()
    warehouses = db.warehouses.find()
    return render_template('admin/warehouses.html', warehouses=warehouses)


@bp.route('/quantities/')
@login_required
def admin_quantity():
    db = get_db()
    prods = list(db.products.find())
    warehouses = db.warehouses.find()
    return render_template('admin/quantities.html', products=prods, warehouses=warehouses)


@bp.route('/orders/')
@login_required
def admin_orders():
    """get somethings from database """
    orders = get_db().orders.find()
    return render_template("admin/orders.html", orders=orders)
