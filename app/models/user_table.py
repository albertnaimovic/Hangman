from flask_login import UserMixin
from flask_login import UserMixin
from entities import sql_db


class Users(sql_db.Model, UserMixin):
    __tablename__ = "users"
    id = sql_db.Column(sql_db.Integer, primary_key=True)
    username = sql_db.Column(sql_db.String(20), unique=True, nullable=False)
    email = sql_db.Column(sql_db.String(120), unique=True, nullable=False)
    password = sql_db.Column(sql_db.String(60), unique=True, nullable=False)
