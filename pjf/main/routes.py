from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards


main = Blueprint('main', __name__)
@app.route("/")
def main_page():
    return render_template("index.html")

# @app.route("/login", methods=["GET", "POST"])
# def login_page():
#     if "logged_in" in session:
#         return redirect(url_for("user_page"))
#     if "login_failed" not in session:
#         session["login_failed"] = False
#     if request.method == "POST":
#         session.permanent = True
#         user_login = request.form["login"]
#         user_password = request.form["password"]
#         session["login"] = user_login
#         session["password"] = user_password
#
#         user_in_db = users.query.filter_by(login=user_login).first()
#
#         if user_in_db:
#             user_in_db_password = users.query.filter_by(login=user_login).first().password
#
#             if user_password == user_in_db_password:
#                 session["logged_in"] = True  # if login is succesfull
#                 return redirect(url_for("user_page"))
#             else:
#                 #failed to login
#                 session["login_failed"] = True
#                 return redirect(url_for("login_page", login_failed=session["login_failed"]))
#         else:
#             # failed to login user not found
#             session["login_failed"] = True
#             return redirect(url_for("login_page", login_failed=session["login_failed"]))
#     else:
#         if("login" in session):
#             login = session["login"]
#         else:
#             login = ''
#
#         if session["login_failed"] == True: # set login_failed = False in order to display error only once
#             session["login_failed"] = False
#             return render_template("login.html", login=login, login_failed=True)
#         return render_template("login.html", login=login, login_failed=False)


@app.route("/user", methods=["GET", "POST"])
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
        return redirect(url_for("login.login_page"))



@app.route("/sign_up", methods=["GET", "POST"])
def sign_up_page():
    if "logged_in" in session:
        return redirect(url_for("user_page"))
    if request.method == "POST":
        session.permanent = True
        user_login = request.form["login"]
        user_password = request.form["password"]
        user_password_repeat = request.form["passwordRepeat"]

        session["login"] = user_login
        session["password"] = user_password

        user_in_db = users.query.filter_by(login=user_login).first()

        if user_in_db: #user login allready taken
            flash("Ta nazwa użytkownika jest już zajęta", "warning")
            session["sign_up_error"] = "user exists"
            return redirect(url_for("sign_up_page", login=session["login"]))
        else:
            if user_password != user_password_repeat:
                flash("Hasło i jego powtrzórzenie nie są identyczne", "error")
                session["sign_up_error"] = "different passwords"
                return redirect(url_for("sign_up_page"))
            if user_password == '':
                flash("Hasło nie może być puste", "warning")
                session["sign_up_error"] = "empty password"
                return redirect(url_for("sign_up_page"))
            new_user = users(user_login, user_password) # sign up successful
            db.session.add(new_user)
            db.session.commit()
            session["logged_in"] = True  # if login is succesfull
            flash("Zostałeś poprawnie zarejestrowany!", "info")
            return redirect(url_for("user_page"))
    else:
        if "logged_in" in session: # already logged in - redirect
            return redirect(url_for("user_page"))
        else:
            if "sign_up_error" in session:
                error = session["sign_up_error"]
                session.pop("sign_up_error", None)
            else:
                error = ""
            if "login" in session:  # fill login input if login is in session
                return render_template("sign_up.html", login=session["login"], error=error)
            return render_template("sign_up.html", login="", error=error)

@app.route("/cards_collection", methods=["GET", "POST"])
def cards_collection_page():
    if "logged_in" not in session:
        return redirect(url_for("login.login_page"))
    if request.method == "POST":
        group_name = request.form["name"]
        group_lang = request.form["lang"]
        user_id = users.query.filter_by(login=session['login']).first().id # only one exists, login is unique

        # new_card = cards(word='malete', translation='walizka', group_id=7)
        # db.session.add(new_card)
        # db.session.commit()

        new_group = groups(name=group_name, lang=group_lang, user_id=user_id)
        db.session.add(new_group)
        db.session.commit()

        return redirect(url_for("cards_collection_page"))

    else: #method == get
        login_in_session = session["login"]
        user_id = users.query.filter_by(login=login_in_session).first().id
        users_groups = groups.query.filter_by(user_id=user_id).all()

        languages = ['Angielski', 'Niemiecki', 'Hiszpański', 'Francuski', 'Włoski', 'Duński',   'Turecki',
                     'Chiński', 'Japoński', 'Holenderski', 'Portugalski', 'Czeski', 'Słowacki', 'Węgierski']
        languages.sort()

        return render_template("cards_collection.html", languages=languages, groups=users_groups)

@app.route("/delete_group/<group_index>")
def delete_group(group_index):
    if(group_index):    # group index - group to be deleted
        if "logged_in" not in session:
            return redirect(url_for("login.login_page"))
        group = groups.query.filter_by(id=group_index).first()
        session_user_id = users.query.filter_by(login=session["login"]).first().id

        if(session_user_id != group.user_id):   # if user tries to delete not his group
            return redirect(url_for("cards_collection_page"))
        #
        # cards_in_group = cards.query.filter_by(group_id=group.id).all()
        # for card in cards_in_group:
        #     db.session.delete(card)
        #     db.session.commit()

        db.session.delete(group)
        db.session.commit()
        return redirect(url_for("cards_collection_page"))
    else:
        return redirect(url_for("cards_collection_page"))

@app.route("/logout")
def logout_page():
    session.pop("login", None)
    session.pop("password", None)
    session.pop("logged_in", None)
    session.pop("login_failed", None)
    session.pop("sign_up_error", None)
    flash("Zostałeś poprawnie wylogowany!", "info")
    return redirect(url_for("login.login_page"))