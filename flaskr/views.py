import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from model import run_model

bp = Blueprint('bp', __name__, url_prefix='/app')

@bp.route('/home')
def home_page():
    return render_template('home.html')

@bp.route('/one_year', methods=('GET', 'POST'))
def one_year_page():
    if request.method == 'POST':
        flash("POSTED")
        # team_name: String
        # year: Int
        ## wins = FUNC CALL HERE 
        return render_template('one_year.html')
    else:
        return render_template('one_year.html')

@bp.route('/five_year', methods=('GET', 'POST'))
def five_year_page():
    if request.method == 'POST':
        flash("POSTED")
        # team_name: String
        # year: Int
        # num_years: Int
        ## FUNC CALL HERE
        return render_template('five_year.html')
    else:
        return render_template('five_year.html')
