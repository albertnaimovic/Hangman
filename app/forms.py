from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email


class RegistrationForm(FlaskForm):
    username = StringField("Username", [DataRequired()])
    email = StringField("Email", [Email()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField(
        "Confirm password", [EqualTo("password", "Password must match.")]
    )
    submit = SubmitField("Register")


class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")
