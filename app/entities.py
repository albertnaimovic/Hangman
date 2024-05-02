import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config["SECRET_KEY"] = "4654f5dfadsrfasdr54e6rae"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "hangman_sqlite.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
sql_db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "log_in"
login_manager.login_message_category = "info"
