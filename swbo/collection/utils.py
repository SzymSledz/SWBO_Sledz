from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from swbo import app
from swbo import db
from swbo.models import users, groups, cards
from swbo.main import *

def delete_groups(group_id):
    user = session['login']
    user_id = users.query.filter_by(login=user).first().id          #user in session
    onwer = groups.query.filter_by(id=group_id).first().user_id     #group owner

    if(onwer != user_id or not user_id):                     # if user tries to delete not his group
        return "error"
    group = groups.query.filter_by(id=group_id).first()

    if not group:
        return "error"

    cards_in_group = cards.query.filter_by(group_id=group.id).all()  # finding and deleting every card in group
    for card in cards_in_group:
        db.session.delete(card)
        db.session.commit()

    db.session.delete(group)
    db.session.commit()
    return 'succes'


def delete_cards(card_id, group_id):
    user = session['login']
    user_id = users.query.filter_by(login=user).first().id          #user in session
    owner = groups.query.filter_by(id=group_id).first().user_id     #group owner.id

    if(owner != user_id or not user_id):                     # if user tries to edit not his group
        return "error"
    card = cards.query.filter_by(id=card_id).first()

    if not card:
        return "error"

    db.session.delete(card)
    db.session.commit()
    return 'succes'