from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "@$FA@Tzw$t@^BBsehwy23626g"
app.permanent_session_lifetime = timedelta(hours = 2)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)

# Importuj modele
from pjf.models import articles

# Tworzenie wszystkich tabel
with app.app_context():
    db.create_all()

from pjf.main.routes import main
from pjf.user.routes import user
from pjf.collection.routes import collection
from pjf.practice.routes import practice
from pjf.article.routes import article

app.register_blueprint(user)
app.register_blueprint(main)
app.register_blueprint(collection)
app.register_blueprint(practice)
app.register_blueprint(article)
