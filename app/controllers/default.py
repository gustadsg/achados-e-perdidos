from app import app
from flask import render_template, url_for


@app.route('/index')
@app.route('/')
def index():
    return "Olá, mundo"

@app.route('/login/')
def login():
    return render_template('login.html')