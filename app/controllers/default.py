import os
from app import app, db
from app.models.forms import LoginForm, PostForm
from app.models.tables import User, Post
from flask import render_template, url_for, request, redirect, flash    
from flask_login import login_user,login_manager, login_required, logout_user, current_user
from werkzeug.utils import secure_filename



@app.route('/index')
@app.route('/')
def index():
    posts = Post.query.all()
    return render_template('index.html', posts = posts)


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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/upload/', methods=["POST", "GET"])
@login_required
def upload_file():
    form = PostForm()  

    if request.method == 'POST':
        # check if the post request has the file part
        if 'image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['image']
        # if user does not select file, browser also
        # submit an empty part without filename
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

@app.route('/delete/')
@login_required
def delete():
    posts = Post.query.all()
    return render_template('delete.html', posts=posts)

@app.route('/deleted/<id>')
@app.route('/deleted/')
@login_required
def deleted(id=None):
    element = Post.query.get(id)
    db.session.delete(element)
    db.session.commit()
    return redirect('/')