from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards
from pjf.main import *

user = Blueprint('user', __name__)

@user.route("/login", methods=["GET", "POST"])
def login_page():
    if "logged_in" in session:
        return redirect(url_for("user.user_page"))
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
                return redirect(url_for("user.user_page"))
            else:
                #failed to login
                session["login_failed"] = True
                return redirect(url_for("user.login_page", login_failed=session["login_failed"]))
        else:
            # failed to login user not found
            session["login_failed"] = True
            return redirect(url_for("user.login_page", login_failed=session["login_failed"]))
    else:
        if("login" in session):
            login = session["login"]
        else:
            login = ''

        if session["login_failed"] == True: # set login_failed = False in order to display error only once
            session["login_failed"] = False
            return render_template("login.html", login=login, login_failed=True)
        return render_template("login.html", login=login, login_failed=False)



@user.route("/sign_up", methods=["GET", "POST"])
def sign_up_page():
    if "logged_in" in session:
        return redirect(url_for("user.user_page"))
    if request.method == "POST":
        session.permanent = True
        user_login = request.form["login"]
        user_password = request.form["password"]
        user_password_repeat = request.form["passwordRepeat"]

        if(user_login == ""):
            flash("Nazwa użytkownika jest pusta", "error")
            session["sign_up_error"] = "empty login"
            return redirect(url_for("user.sign_up_page"))

        session["login"] = user_login
        session["password"] = user_password

        user_in_db = users.query.filter_by(login=user_login).first()

        if user_in_db:  # user user allready taken
            flash("Ta nazwa użytkownika jest już zajęta", "warning")
            session["sign_up_error"] = "user exists"
            return redirect(url_for("user.sign_up_page", login=session["login"]))
        else:
            if user_password != user_password_repeat:
                flash("Hasło i jego powtrzórzenie nie są identyczne", "error")
                session["sign_up_error"] = "different passwords"
                return redirect(url_for("user.sign_up_page"))
            if user_password == '':
                flash("Hasło nie może być puste", "warning")
                session["sign_up_error"] = "empty password"
                return redirect(url_for("user.sign_up_page"))
            new_user = users(user_login, user_password)  # sign up successful
            db.session.add(new_user)
            db.session.commit()
            session["logged_in"] = True  # if user is succesfull
            flash("Zostałeś poprawnie zarejestrowany!", "info")
            return redirect(url_for("user.user_page"))
    else:
        if "logged_in" in session:  # already logged in - redirect
            return redirect(url_for("user.user_page"))
        else:
            if "sign_up_error" in session:
                error = session["sign_up_error"]
                session.pop("sign_up_error", None)
            else:
                error = ""
            if "login" in session:  # fill user input if user is in session
                return render_template("sign_up.html", login=session["login"], error=error)
            return render_template("sign_up.html", login="", error=error)

@user.route("/user", methods=["GET", "POST"])
def user_page():
    if "logged_in" in session:
        login_in_session = session["login"]

        if request.method == "POST":
            login = request.form["login"]
            session["login"] = login
            user_in_db = users.query.filter_by(login=login).first()
            user_in_db.login = login
            db.session.commit()
        else:
            if "login" in session:
                login_in_session = session["login"]

        user_id = users.query.filter_by(login=login_in_session).first().id
        users_groups = groups.query.filter_by(user_id=user_id).all()
        messages = []

        for group in users_groups:
            message = f"Nazwa: {group.name} Język: {group.lang} User: {group.user_id} Id_w_Sesji: {user_id}"
            messages.append(message)
        return render_template("user.html", login=login_in_session, groups=messages)
    else:
        return redirect(url_for("user.login_page"))


@user.route("/logout")
def logout_page():
    session.pop("login", None)
    session.pop("password", None)
    session.pop("logged_in", None)
    session.pop("login_failed", None)
    session.pop("sign_up_error", None)
    session.pop("delete_confirmed", None)
    session.pop("group_delete", None)
    session.pop("results", None)
    flash(f"Zostałeś poprawnie wylogowany!", "info")
    return redirect(url_for("user.login_page"))


@user.route("/stats")
def stats_page():
    if "logged_in" not in session:
        return redirect(url_for("login.login_page"))

    user_id = users.query.filter_by(login=session["login"]).first().id
    users_groups=groups.query.filter_by(user_id=user_id).all()

    return render_template("stats.html", groups=users_groups)