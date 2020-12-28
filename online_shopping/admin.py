from flask import *
import functools
from werkzeug.security import *
import json
from cryptography.fernet import Fernet

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
            print(url_for('admin.orders'))
            return redirect(url_for('admin.orders'))

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


@bp.route('/products/')
def prods():
    prods = {'لوبیا قرمز گلستان 900 گرمی': 'مواد غذایی / کالاهای اساسی و خوار و بار',
             'روغن سرخ کردنی سمن 1.35 کیلویی': 'مواد غذایی / کالاهای اساسی و خوار و بار',
             'روغن مایع آفتابگردان حاوی ویتامین دی و ای': 'مواد غذایی / کاهای اساسی و خوار و بار',
             'کره سنتی شکلی 100 گرمی': 'مواد غذایی / لبنیات',
             'قهوه اسپرسو بن مانو مدل آرتیمان 250 گرمی': 'مواد غذایی / نوشیدنی'
             }

    return render_template('product.html', products=prods)


@bp.route('/inventory/')
def inventory():
    invens = ['انبار شماره 1',
              'انبار شماره 2',
              'انبار شماره 3'
              ]

    return render_template('inventory.html', inventories=invens)


@bp.route('/price/')
def price():
    pass


@bp.route('/orders/')
@login_required
def orders():
    """get somethings from database """
    return render_template("admin/orders.html")
