from flask import render_template

from app.blueprints.main import bp


@bp.route("/")
def home():
    return render_template("main/home.html")