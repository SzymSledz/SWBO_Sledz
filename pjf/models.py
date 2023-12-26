from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import db
class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    login = db.Column(db.String(60))
    password = db.Column(db.String(60))

    def __init__(self, login, password):
        self.login = login
        self.password = password