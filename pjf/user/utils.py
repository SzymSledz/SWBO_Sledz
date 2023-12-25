import random as rand
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards, lessons
from pjf.main import *
import math


def get_user_id(user_login):
    return users.query.filter_by(login=user_login).first().id
def count_completion(user_login):
    user_id = get_user_id(user_login)
    user_groups = groups.query.filter_by(user_id=user_id).all()
    result = 0

    for group in user_groups:
        result += group.completion

    return result/len(user_groups)

def count_words(user_login):
    user_id = get_user_id(user_login)
    user_groups = groups.query.filter_by(user_id=user_id).all()
    result = 0

    for group in user_groups:
        words_in_group = cards.query.filter_by(group_id=group.id).all()
        known_words = int(group.completion)/100 * len(words_in_group)
        result += math.floor(known_words)

    return result

def count_lessons(user_login):
    user_id = get_user_id(user_login)
    user_groups = groups.query.filter_by(user_id=user_id).all()
    result = 0

    for group in user_groups:
        lessons_in_group = lessons.query.filter_by(group_id=group.id).all()
        result += len(lessons_in_group)

    return result




def get_favorite_lang(user_login):
    user_id = get_user_id(user_login)
    user_groups = groups.query.filter_by(user_id=user_id).all()
    user_lessons = []

    for group in user_groups:
        lessons_in_group = lessons.query.filter_by(group_id=group.id)
        for lesson in lessons_in_group:
            user_lessons.append(lesson.group.lang)

    counter = 0
    result = user_lessons[0]

    for i in user_lessons:
        curr_frequency = user_lessons.count(i)
        if (curr_frequency > counter):
            counter = curr_frequency
            result = i

    return result

def count_days(user_login):
    user_id = get_user_id(user_login)
    user_groups = groups.query.filter_by(user_id=user_id).all()
    user_lessons_dates = []

    for group in user_groups:
        lessons_in_group = lessons.query.filter_by(group_id=group.id)
        for lesson in lessons_in_group:
            user_lessons_dates.append(lesson.date)

    days_list = []

    for day in user_lessons_dates:
        if day not in days_list:
            days_list.append(day)

    return len(days_list)
