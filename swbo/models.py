from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from swbo import db
from datetime import datetime
class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    login = db.Column(db.String(60))
    password = db.Column(db.String(60))
    group = db.relationship("groups", backref="owner", lazy=True)
    def __init__(self, login, password):
        self.login = login
        self.password = password


class groups(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    lang = db.Column(db.String(60))
    completion = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    card = db.relationship("cards", backref="group", lazy=True)
    lesson = db.relationship("lessons", backref="group", lazy=True)


class cards(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    word = db.Column(db.String(60))
    translation = db.Column(db.String(60))
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

class lessons(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    completion = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    group_id = db.Column(db.Integer, db.ForeignKey("groups.id"))

class articles(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date = db.Column(db.DateTime)
    text = db.Column(db.String(2000))

class calendarEvent(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    description = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)



