import functools
import psycopg2.extras

from flask import Blueprint, current_app
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

#from flaskr.db import get_db

bp=Blueprint('store',__name__)



@bp.route('/')
def index():

    return render_template('index.html')