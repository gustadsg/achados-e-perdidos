from app import db, login_manager
from flask_login import login_user
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = generate_password_hash(password)
    
    def verify_password(self, pwd):
        return check_password_hash(self.password, pwd)

    def __repr__(self):
        return "<User %r>" % self.username

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    image_path = db.Column(db.String, unique=True)
    content = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, image_path, content, user_id):
        self.image_path = image_path
        self.content = content
        self.user_id = user_id
    
    def __repr__(self):
        return "<User %r>" % self.post