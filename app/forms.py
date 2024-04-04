from flask_wtf import FlaskForm
from wtforms import SubmitField, BooleanField, StringField, PasswordField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email
import app


class RegistrationForm(FlaskForm):
    username = StringField("Name", [DataRequired()])
    email = StringField("Email", [Email()])
    password = PasswordField("Password", [DataRequired()])
    confirm_password = PasswordField(
        "Confirm password", [EqualTo("password", "Password must match.")]
    )
    submit = SubmitField("Register")

    def check_name(self, name):
        user = app.Users.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError("Username already exists.")

    def check_email(self, email):
        user = app.Users.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already exists.")


class LoginForm(FlaskForm):
    email = StringField("Email", [DataRequired()])
    password = PasswordField("Password", [DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Log in")
