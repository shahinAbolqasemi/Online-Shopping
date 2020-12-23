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
        if "admin" in session:
            return redirect(url_for("admin.login"))

        return view(*args, **kwargs)

    return wrapped_view


with open('Online_Shopping/admins.json') as f:
    main = json.load(f)

with open('Online_Shopping/key.txt') as f:
    key = f.read()

cipher_suite = Fernet(key.encode())
admins = {}
for admin in main[1:]:
    username = admin[0]
    password = admin[1]
    admins[username] = cipher_suite.decrypt(password.encode()).decode()


def valid_admin(username, password):
    if username in admins.keys():
        return password == admins[username]
    else:
        return 'invalid username'


@bp.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if valid_admin(username, password):
            session.clear()
            session['admin'] = request.form['username']
            return redirect(url_for('admin.panel'))

        elif valid_admin(username, password) == 'invalid username':
            error = 'Username not registered! :('

        else:
            error = 'Invalid Password'

        flash(error)

    return render_template('admin/login.html')


@bp.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('admin.login'))


@bp.route('/panel')
def panel():
    return render_template('admin/orders.html')


@bp.route('/commodity')
def commodity():
    pass


@bp.route('/inventory')
def inventory():
    pass


@bp.route('/price')
def price():
    pass


@bp.route('/orders')
@login_required
def orders():
    """get somethings from database """
    return render_template("admin/orders.html")
