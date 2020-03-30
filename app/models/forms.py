from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators

class LoginForm(FlaskForm):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me')

