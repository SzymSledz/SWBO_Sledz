from flask import Flask, redirect, url_for, render_template, request, session
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "@$FA@Tzw$t"
app.permanent_session_lifetime = timedelta(hours = 2)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    login = db.Column(db.String(60))
    password = db.Column(db.String(60))

    def __init__(self, login, password):
        self.login = login
        self.password = password

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        session.permanent = True
        user_login = request.form["login"]
        user_password = request.form["password"]
        session["login"] = user_login
        session["password"] = user_password

        session["logged_in"] = True # if login is succesfull

        user_in_db = users.query.filter_by(login=user_login).first()
        if user_in_db:
            session["login"] = user_in_db.login
        else:
            usr = users(user_login, user_password)
            db.session.add(usr)
            db.session.commit()

        return redirect(url_for("user_page"))
    else:
        if "logged_in" in session:
            return redirect(url_for("user_page"))
        else:
            login = ''
            password = ''
        return render_template("login.html", login=login, password=password)

@app.route("/user", methods=["GET", "POST"])
def user_page():
    if "logged_in" in session:
        login_in_session = session["login"]

        if request.method == "POST":
            login = request.form["login"]
            session["login"] = login
            user_in_db = users.query.filter_by(login=login).first()
            user_in_db.login = login
            db.session.commit()
        else:
            if "login" in session:
                login_in_session = session["login"]
        return render_template("user.html", login=login_in_session)
    else:
        return redirect(url_for("login_page"))

@app.route("/logout")
def logout_page():
    session.pop("login", None)
    session.pop("password", None)
    session.pop("logged_in", None)
    return redirect(url_for("login_page"))

@app.route("/sign_up", methods=["GET", "POST"])
def sign_up_page():
    if "logged_in" in session:
        return redirect(url_for("login_page"))
    return render_template("sign_up.html")

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)
