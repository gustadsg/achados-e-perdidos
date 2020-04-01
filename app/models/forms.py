from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms import validators

class LoginForm(FlaskForm):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])
    remember_me = BooleanField('remember_me')

class RegisterForm(FlaskForm):
    username = StringField('username', [validators.DataRequired()])
    password = PasswordField('password', [validators.DataRequired()])

class PostForm(FlaskForm):
    image_path = StringField('image', [validators.DataRequired()])
    local = StringField('local', [validators.DataRequired()])

class FoundForm(FlaskForm):
    name_owner = StringField('name_owner', [validators.DataRequired()])
    cpf_owner = StringField('cpf_owner', [validators.DataRequired(), validators.Length(min=11)])