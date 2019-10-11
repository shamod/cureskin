from flask import Flask
import os
import time

app = Flask(__name__)

# Setup the app with the config.py file
app.config.from_object('app.config')

app.config.update(
    UPLOADED_PATH=os.path.join(app.instance_path, 'photos'),
    # Flask-Dropzone config:
    DROPZONE_ALLOWED_FILE_TYPE='image',
    DROPZONE_MAX_FILE_SIZE=3,
    DROPZONE_MAX_FILES=1,
)

# Setup the logger
from app.logger_setup import logger

# Setup the database
from flask.ext.sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Setup the mail server
from flask.ext.mail import Mail
mail = Mail(app)

# Setup the debug toolbar
from flask_debugtoolbar import DebugToolbarExtension
if app.config['DEBUG']:
    toolbar = DebugToolbarExtension(app)

# Setup the password crypting
from flask.ext.bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# Setup flask dropzone
from flask_dropzone import Dropzone
dropzone = Dropzone(app)

# Import the views
from app.views import main, user, error
app.register_blueprint(user.userbp)

# Setup the user login process
from flask.ext.login import LoginManager
from app.models import User

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'userbp.signin'


@login_manager.user_loader
def load_user(email):
    return User.query.filter(User.email == email).first()

from app import admin

# Setup template date filter
def format_epoch_datetime(value, format='medium'):
    if format == 'full':
        format="%Y-%m-%d %H:%M"
    elif format == 'medium':
        format="%Y-%m-%d"
    return time.strftime(format, time.localtime(value))

app.jinja_env.filters['epoch_datetime'] = format_epoch_datetime
