from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from swbo import app
from swbo import db
from swbo.models import users, groups, cards
from swbo.main import *
from swbo.collection.utils import delete_groups, delete_cards

collection = Blueprint('collection', __name__)

@collection.route("/cards_collection", methods=["GET", "POST"])
def cards_collection_page():
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))
    if request.method == "POST":
        group_name = request.form["name"]
        group_lang = request.form["lang"]
        user_id = users.query.filter_by(login=session['login']).first().id # only one exists, user is unique

        new_group = groups(name=group_name, lang=group_lang, user_id=user_id)
        db.session.add(new_group)
        db.session.commit()

        return redirect(url_for("collection.cards_collection_page"))

    else: #method == get
        login_in_session = session["login"]
        user_id = users.query.filter_by(login=login_in_session).first().id
        users_groups = groups.query.filter_by(user_id=user_id).all()

        languages = ['Angielski', 'Niemiecki', 'Hiszpański', 'Francuski', 'Włoski', 'Duński',   'Turecki',
                     'Chiński', 'Japoński', 'Holenderski', 'Portugalski', 'Czeski', 'Słowacki', 'Węgierski']
        languages.sort()

        return render_template("cards_collection.html", languages=languages, groups=users_groups)

@collection.route("/group/<group>", methods=["GET", "POST"])
def group_page(group):
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))
    if request.method == "POST":
        word = request.form["word"]
        translation = request.form["translation"]
        if word == "" or translation == "":
            if word == '':
                session['form_error'] = "word"
            else:
                session['form_error'] = "translation"
        else:
            new_card = cards(word=word, translation=translation, group_id=group)
            db.session.add(new_card)
            db.session.commit()
        return redirect(url_for("collection.group_page", group=group))
    else:
        group_cards = cards.query.filter_by(group_id=group).all()

        if 'form_error' in session:
            error = session['form_error']
            flash("To pole nie może być puste")
            session.pop('form_error')
        else:
            error = ''
        group_name = groups.query.filter_by(id=group).first().name
        return render_template("group.html", group=group, error=error, cards=group_cards, group_name=group_name)

@collection.route("/delete_group/<group_index>")
def delete_group(group_index):
    if (group_index):  # group index - group to be deleted
        if "logged_in" not in session:
            return redirect(url_for("user.login_page"))

        # if session["delete_confirmed"] and session["group_delete"]:
        delete_groups(group_index)  # delete group function -> util.py
        #     session["delete_confirmed"] = False
        #     session.pop("group_delete")
        # else:
        #     session["group_delete"] = group_index
        #     return redirect(url_for("collection.cards_collection_page"))
    return redirect(url_for("collection.cards_collection_page"))

@collection.route("/delete_card/<card_index>")
def delete_card(card_index):

    if (card_index):  # card index - card to be deleted
        if "logged_in" not in session:
            return redirect(url_for("user.login_page"))

        group_id = cards.query.filter_by(id=card_index).first().group.id
        delete_cards(card_index, group_id)  # delete card function -> util.py

    return redirect(url_for("collection.group_page", group=group_id))