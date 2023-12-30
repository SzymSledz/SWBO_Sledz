from random import random
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards, lessons
from pjf.main import *
from pjf.practice.utils import shuffle_list, check_answers

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

    group = groups.query.filter_by(id=group_id).first()

    if not group:
        return redirect(url_for("practice.practice_page"))

    login_in_session = session["login"]
    user_id = users.query.filter_by(login=login_in_session).first().id
    owner = group.user_id

    if user_id != owner:
        return redirect(url_for("practice.practice_page"))

    cards_list = cards.query.filter_by(group_id=group_id).all()

    if request.method == "POST":
        answers = []
        for card in cards_list:
            answer = request.form["answer" + str(card.id)] # get answer for each card
            answers.append(answer)
        results = check_answers(cards_list, answers)    # chekcs each answers and returns one of three results (correct/nearly/wrong)

        translations = [] # for debug purposes only
        for card in cards_list:
            translation = card.translation
            translations.append(translation)

        session["results"] = results
        session["answers"] = answers
        print(answers)
        print(results)
        print(translations)
        return redirect(url_for("practice.lesson_page", group_id=group_id))

    if("results" not in session):
        results = ''
        cards_list = shuffle_list(cards_list)
        answers = ''
    else:
        results = session["results"]
        answers = session["answers"]
        session.pop("results")
    return render_template("lesson.html", cards=cards_list, results=results, answers=answers)