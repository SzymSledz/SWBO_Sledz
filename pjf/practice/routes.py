from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards
from pjf.main import *

practice = Blueprint('practice', __name__)

@practice.route("/practice", methods=["GET", "POST"])
def practice_page():
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    login_in_session = session["login"]
    user_id = users.query.filter_by(login=login_in_session).first().id
    users_groups = groups.query.filter_by(user_id=user_id).all()

    return render_template("practice.html", groups=users_groups)