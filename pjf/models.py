from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import db
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
    #creation_date = db.Column(db.Datetime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    # def __init__(self, name, lang):
    #     self.name = name
    #     self.lang = lang