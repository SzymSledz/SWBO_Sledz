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