import os
from app import app, db
from app.models.forms import LoginForm, RegisterForm, PostForm, FoundForm
from app.models.tables import User, Post, Found
from flask import render_template, url_for, request, redirect, flash    
from flask_login import login_user,login_manager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename


# Página inicial
@app.route('/index')
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts = posts)


#Login e logout
@app.route('/login/', methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and User.query.filter_by(username=form.username.data).first().password == form.password.data:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('master'))
    return render_template('login.html', form=form)


@app.route('/master/')
@login_required
def master():
    return render_template('master.html')


@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


#Funcionalidades para o usuário logado
@app.route('/register/', methods=["GET", "POST"])
@login_required
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
    return render_template('register.html', form=form)

@app.route('/upload/', methods=["POST", "GET"])
@login_required
def upload_file():
    form = PostForm()  
    if request.method == 'POST':
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            flash('No selected image')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            form.image_path=filename
            posted = Post(image_path=str(form.image_path), content=str(form.local.data))
            db.session.add(posted)
            db.session.commit()
            return redirect(url_for('upload_file'))                   
    return render_template('upload.html', form=form)

@app.route('/manage/')
@login_required
def manage():
    posts = Post.query.all()
    return render_template('manage.html', posts=posts)

@app.route('/delete/<id>')
@app.route('/delete/')
@login_required
def delete(id=None):
    element = Post.query.get(id)
    os.chdir(app.config['UPLOAD_FOLDER'])
    os.unlink(element.image_path)
    db.session.delete(element)
    db.session.commit()
    return redirect('/manage/')

@app.route('/find/<id>', methods=["GET", "POST"])
@app.route('/find/', methods=["GET", "POST"])
@login_required
def find(id=None):
    form = FoundForm()
    found = Found.query.all()
    if request.method=="POST":
        if form.validate_on_submit():
            element = Post.query.get(id)
            found_element = Found(element.image_path, element.content, form.name_owner.data, form.cpf_owner.data)
            db.session.add(found_element)
            db.session.delete(element)
            db.session.commit()
            return redirect('/manage/')
    return render_template('find.html', found=found, form=form)

@app.route('/found/')
@login_required
def found():
    found = Found.query.all()
    return render_template('found.html', found = found)