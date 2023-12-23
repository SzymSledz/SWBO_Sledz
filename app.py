from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from sqlalchemy import *

app = Flask(__name__)
app.secret_key = "@$FA@Tzw$t"
app.permanent_session_lifetime = timedelta(hours = 2)
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

@app.route("/user")
def user_page():
    if "user" in session:
        usr = session["user"]
        return render_template("user.html")
    else:
        return redirect(url_for("login_page"))

@app.route("/logout")
def logout_page():
    session.pop("user", None)
    return redirect(url_for("login_page"))

if __name__ == '__main__':
    app.run(debug = True)
