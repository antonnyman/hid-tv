from flask import Flask, url_for, redirect, render_template, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required, login_user, logout_user, current_user, UserMixin
from flask_turbolinks import turbolinks
from requests_oauthlib import OAuth2Session
from requests.exceptions import HTTPError

from project.config import config


## Create the app
app = Flask(__name__)
app.config.from_object(config['dev'])
app.secret_key = ""

## DB inits
db = SQLAlchemy(app)
db.init_app(app)

## Login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.session_protection = 'strong'

## Blueprints
from project.user.views import user_blueprint
from project.upload.views import upload_blueprint
from project.slideshow.views import slideshow_blueprint
app.register_blueprint(user_blueprint)
app.register_blueprint(upload_blueprint)
app.register_blueprint(slideshow_blueprint)

#turbolinks
turbolinks(app)

## Default route
@app.route('/')
@login_required
def index():
    return render_template('index.html')
