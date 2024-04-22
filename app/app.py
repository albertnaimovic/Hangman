import os
from sqlalchemy.exc import IntegrityError
from flask import Flask, render_template, redirect, url_for, flash, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import (
    LoginManager,
    current_user,
    logout_user,
    login_user,
    UserMixin,
    login_required,
)
import forms
from game_backend import Hangman
from mongo_database import mongodb_connection, statistics_collection
from datetime import datetime
import logging
import logging.config


logging.config.fileConfig("logging.conf")
logger = logging.getLogger("Log")


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


class Users(sql_db.Model, UserMixin):
    __tablename__ = "users"
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    username = sql_db.Column(sql_db.String(20), unique=True, nullable=False)
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(60), unique=True, nullable=False)


@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


@app.route("/register", methods=["GET", "POST"])
def register():
    sql_db.create_all()
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = Users(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password,
        )
        try:
            sql_db.session.add(user)
            sql_db.session.commit()
            logging.info(f"User {user.username} has been created.")
            flash("You've registered successfully !", "success")
            return redirect(url_for("index"))
        except IntegrityError as err:
            sql_db.session.rollback()
            logging.error(err)
            if "users.username" in str(err):
                flash("Username already exists.", "danger")
            elif "users.email" in str(err):
                flash("Email already exists.", "danger")
            else:
                logging.error("An error occured on register")
                flash("An error occurred. Please try again.", "danger")
    return render_template("register.html", title="Register", form=form)


@app.route("/log_in", methods=["GET", "POST"])
def log_in():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = Users.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember_me.data)
            next_page = request.args.get("next")
            logging.info(f"User {user.username} logged in.")
            return redirect(next_page) if next_page else redirect(url_for("index"))
        else:
            logging.info(f"User {user.username} entered wrong password.")
            flash("Login failed. Check your email/password.", "danger")
    return render_template("log_in.html", title="Log in", form=form)


@app.route("/disconnect")
@login_required
def disconnect():
    logout_user()
    return redirect(url_for("index"))


@app.route("/account")
@login_required
def account():
    return render_template("account.html", title="Account")


@app.route("/statistics")
@login_required
def statistics():
    query = {"user_id": current_user.id}
    statistics = mongodb_connection.find_documents(statistics_collection, query)
    return render_template("statistics.html", title="Statistics", statistics=statistics)


@app.route("/")
def index():
    if current_user.is_authenticated:
        welcome_message = f"Hi, {current_user.username} !"
        query = {"user_id": current_user.id}
        statistics = mongodb_connection.find_documents(statistics_collection, query)
        games_today = [
            i for i in statistics if i["created_at"].date() == datetime.today().date()
        ]
        return render_template(
            "index.html", welcome_message=welcome_message, statistics=games_today
        )
    else:
        welcome_message = f"Hi, stranger ! "
        return render_template("index.html", welcome_message=welcome_message)


def create_new_game() -> Hangman:
    return Hangman()


@app.route("/play", methods=["GET", "POST"])
@login_required
def play():

    if request.method == "POST":
        hangman_game_json = session.get("hangman_game")
        hangman_game = Hangman.from_json(hangman_game_json)

        letter = request.form["letter"]
        if len(letter) > 1:
            game_result = hangman_game.try_full_word(letter)
        else:
            game_result = hangman_game.take_turn(letter)

        session["hangman_game"] = hangman_game.to_json()

        if game_result:
            hangman_pic = hangman_game.wrong_attempts
            if game_result.startswith("You've lost"):
                hangman_pic = 0
                game_status = "LOSS"
            else:
                game_status = "WIN"
            logging.info(
                f"user {current_user.username} ended game with status {game_status}"
            )
            document = {
                "game_status": game_status,
                "attempts_made": 10 - hangman_game.all_attempts,
                "wrong_attempts_made": 6 - hangman_game.wrong_attempts,
                "secret_word": hangman_game.secret_word,
                "user_id": current_user.id,
                "created_at": datetime.now(),
            }
            mongodb_connection.insert_document(statistics_collection, document)
            return render_template(
                "play.html",
                result=game_result,
                attempts_left=hangman_game.all_attempts,
                wrong_attempts_left=hangman_game.wrong_attempts,
                used_letters=hangman_game.used_letters,
                hangman_pic=url_for("static", filename=f"hangman/{hangman_pic}.png"),
            )

        return render_template(
            "play.html",
            user_word=hangman_game.display_word(),
            attempts_left=hangman_game.all_attempts,
            wrong_attempts_left=hangman_game.wrong_attempts,
            used_letters=hangman_game.used_letters,
            hangman_pic=url_for(
                "static", filename=f"hangman/{hangman_game.wrong_attempts}.png"
            ),
        )
    elif request.method == "GET":
        hangman_game = create_new_game()
        session["hangman_game"] = hangman_game.to_json()
        logging.info(f"user {current_user.username} started a new game.")
        return render_template(
            "play.html",
            user_word=hangman_game.display_word(),
            attempts_left=hangman_game.all_attempts,
            wrong_attempts_left=hangman_game.wrong_attempts,
            hangman_pic=url_for("static", filename="hangman/6.png"),
        )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
    sql_db.create_all()
