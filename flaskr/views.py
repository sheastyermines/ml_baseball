import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('bp', __name__, url_prefix='/app')

@bp.route('/home')
def home_page():
    return render_template('home.html')

@bp.route('/one_year')
def one_year_page():
    return render_template('one_year.html')

@bp.route('/five_year')
def five_year_page():
    return render_template('five_year.html')
