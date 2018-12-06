import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.model import run_model
from flaskr.config import teams

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
        return render_template(
            'one_year.html',
            teams=teams
        )
    else:
        return render_template(
            'one_year.html',
            teams=teams
        )

@bp.route('/five_year', methods=('GET', 'POST'))
def five_year_page():
    if request.method == 'POST':
        # team_name: String
        # year: Int
        # num_years: Int
        team_acronym = teams[request.form["team"]]
        year = int(request.form["year"])
        #num_years = str(request.form["num_years"]) + "_years"
        num_years = int(request.form["num_years"])
        wins, real_wins = run_model(team_acronym, year, num_years)
        flash("Estimated Wins: " + str(wins) + " Actual Wins: " + str(real_wins))
    return render_template(
        'five_year.html',
        teams=teams
    )
