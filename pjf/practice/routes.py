from random import random
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards
from pjf.main import *
from pjf.practice.utils import shuffle_list, check_answer

practice = Blueprint('practice', __name__)

@practice.route("/practice", methods=["GET", "POST"])
def practice_page():
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    login_in_session = session["login"]
    user_id = users.query.filter_by(login=login_in_session).first().id
    users_groups = groups.query.filter_by(user_id=user_id).all()

    return render_template("practice.html", groups=users_groups)

@practice.route("/lesson/<group_id>", methods=["GET", "POST"])
def lesson_page(group_id):
    if "logged_in" not in session:
        return redirect(url_for("user.login_page"))

    # if request.method == "POST":
    #     answer = request.form["answer"]
    #     if answer:
    #         resault = check_answer(card_id, answer)
    #         flash(resault)
    #     return redirect(url_for("lesson.lesson_page"), group_id=group_id)

    group = groups.query.filter_by(id=group_id).first()

    if not group:
        return redirect(url_for("practice.practice_page"))

    login_in_session = session["login"]
    user_id = users.query.filter_by(login=login_in_session).first().id
    owner = group.user_id

    if user_id != owner:
        return redirect(url_for("practice.practice_page"))

    cards_list = cards.query.filter_by(group_id=group_id).all()
    cards_list = shuffle_list(cards_list)
    mess = type(cards_list)

    return render_template("lesson.html", cards=cards_list, message=mess)