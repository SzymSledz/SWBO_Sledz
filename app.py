from flask import Flask, redirect, url_for, render_template, request

app = Flask(__name__)

@app.route("/")
def main_page():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        user = request.form["login"]
        return redirect(url_for("user_page", usr=user))
    else:
        return render_template("login.html")

@app.route("/<usr>")
def user_page(usr):
    return f"<h1>Wellcome {usr}</h1>"

if __name__ == '__main__':
    app.run(debug = True)
