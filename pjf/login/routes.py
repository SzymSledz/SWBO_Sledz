from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards
from pjf.main import *

login = Blueprint('login', __name__)

@login.route("/login", methods=["GET", "POST"])
def login_page():
    if "logged_in" in session:
        return redirect(url_for("user_page"))
    if "login_failed" not in session:
        session["login_failed"] = False
    if request.method == "POST":
        session.permanent = True
        user_login = request.form["login"]
        user_password = request.form["password"]
        session["login"] = user_login
        session["password"] = user_password

        user_in_db = users.query.filter_by(login=user_login).first()

        if user_in_db:
            user_in_db_password = users.query.filter_by(login=user_login).first().password

            if user_password == user_in_db_password:
                session["logged_in"] = True  # if login is succesfull
                return redirect(url_for("user_page"))
            else:
                #failed to login
                session["login_failed"] = True
                return redirect(url_for("login_page", login_failed=session["login_failed"]))
        else:
            # failed to login user not found
            session["login_failed"] = True
            return redirect(url_for("login_page", login_failed=session["login_failed"]))
    else:
        if("login" in session):
            login = session["login"]
        else:
            login = ''

        if session["login_failed"] == True: # set login_failed = False in order to display error only once
            session["login_failed"] = False
            return render_template("login.html", login=login, login_failed=True)
        return render_template("login.html", login=login, login_failed=False)
