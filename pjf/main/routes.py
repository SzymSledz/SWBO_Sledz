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

@app.route("/cards_collection", methods=["GET", "POST"])
def cards_collection_page():
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))
    if request.method == "POST":
        group_name = request.form["name"]
        group_lang = request.form["lang"]
        user_id = users.query.filter_by(login=session['login']).first().id # only one exists, user is unique

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
            return redirect(url_for("user.login_page"))
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
