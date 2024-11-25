from flask import Flask
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "@$FA@Tzw$t@^BBsehwy23626g"
app.permanent_session_lifetime = timedelta(hours = 2)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Importuj modele
from swbo.models import calendarEvent

# Tworzenie wszystkich tabel
with app.app_context():
    db.create_all()

from swbo.main.routes import main
from swbo.user.routes import user
from swbo.collection.routes import collection
from swbo.practice.routes import practice

app.register_blueprint(user)
app.register_blueprint(main)
app.register_blueprint(collection)
app.register_blueprint(practice)
