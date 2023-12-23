from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.secret_key = "@$FA@Tzw$t"
app.permanent_session_lifetime = timedelta(hours = 2)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.string(60))
    email = db.Column(db.String(60))

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        session.permanent = True
        user = request.form["login"]
        session["user"] = user
        return redirect(url_for("user_page"))
    else:
        if("user" in session):
            return redirect(url_for("user_page"))
        return render_template("login.html")

@app.route("/user", methods=["GET", "POST"])
def user_page():
    if "user" in session:
        usr = session["user"]

        if request.method == "POST":
            email = request.form["email"]
            session["email"] = email
        else:
            if "email" in session:
                email = session["email"]
        return render_template("user.html", email=email)
    else:
        return redirect(url_for("login_page"))

@app.route("/logout")
def logout_page():
    session.pop("user", None)
    session.pop("email", None)
    return redirect(url_for("login_page"))

if __name__ == '__main__':
    app.run(debug = True)
