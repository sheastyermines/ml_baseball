import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from flaskr.model import predict
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
        team_acronym = teams[request.form["team"]]
        year = int(request.form["year"])
        try:
            wins, real_wins = predict(team_acronym, year, 0)
        except Exception as c:
            print(c)
            flash("Data is unavailable for chosen year. Choose a different year.", "error")
            return render_template(
                'five_year.html',
                teams=teams,
                team_selected=request.form["team"],
                year_selected=year,
            )
        if wins > 0:
            flash("Estimated Wins: " + str(wins) + "<br> Actual Wins: " + str(real_wins), "success")
        else:
            flash("Error: Invalid Combination of Attributes", "error")

        return render_template(
            'one_year.html',
            teams=teams,
            team_selected=request.form["team"],
            year_selected=year,
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
        num_years = int(request.form["num_years"])
        try:
            wins, real_wins = predict(team_acronym, year, num_years)
        except Exception as c:
            print(c)
            flash("Data is unavailable for chosen year. Choose a different year.", "error")
            return render_template(
                'five_year.html',
                teams=teams,
                team_selected=request.form["team"],
                year_selected=year,
                num_years_selected=num_years,
            )
        if wins > 0:
            flash("Estimated Wins: " + str(wins) + "<br> Actual Wins: " + str(real_wins), "success")
        else:
            flash("Error: Invalid Combination of Attributes", "error")

        return render_template(
            'five_year.html',
            teams=teams,
            team_selected=request.form["team"],
            year_selected=year,
            num_years_selected=num_years,
        )
    return render_template(
        'five_year.html',
        teams=teams
    )
