from app import app
from app.models.forms import LoginForm
from app.models.tables import User
from flask import render_template, url_for, request, redirect
from flask_login import login_user,login_manager, login_required, logout_user, current_user



@app.route('/index')
@app.route('/')
def index():
    return "Olá, mundo"

@app.route('/login/', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.query.filter_by(username=form.username.data).first().password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

