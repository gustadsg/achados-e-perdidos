from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

from app.models import tables
from app.controllers import default

