import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

class Auth:
    """ Google project credentials """
    GOOGLE_CLIENT_ID = ('718070373176-6756k222lun7ndteijpsrdbdkpkhkfb6.apps.googleusercontent.com')
    GOOGLE_CLIENT_SECRET = 'MkiTpfVruEZ2utP_SDDV67MT'
    GOOGLE_REDIRECT_URI = 'https://localhost:5000/google-callback'
    GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    GOOGLE_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    GOOGLE_SCOPE = ['profile', 'email']

    """ Box auth credentials """
    BOX_CLIENT_ID = 'olp9zuppf1o4mw4brfruldyd2jn7yh7g'
    BOX_CLIENT_SECRET = 'lL7MQUmxkW1JBCeUFftx5RPbAoC1K7J6'
    BOX_REDIRECT_URI = 'http://0.0.0.0'
    BOX_AUTH_URI = 'https://account.box.com/api/oauth2/authorize'

    """ Lifelog credentials """
    LIFELOG_CLIENT_ID = "7eee8b7b-79ff-4ec5-a936-e20a6bd2d1e7"
    LIFELOG_SECRET = "d6F71lfPQhAeeYdt4Q1nZca8eW8"
    LIFELOG_AUTH_URI = "https://platform.lifelog.sonymobile.com/oauth/2/authorize"
    LIFELOG_TOKEN_URI = "https://platform.lifelog.sonymobile.com/oauth/2/token"
    LIFELOG_REFRESH_TOKEN = "https://platform.lifelog.sonymobile.com/oauth/2/refresh_token"
    LIFELOG_REDIRECT_URI = 'https://localhost:5000/lifelog-callback'
    LIFELOG_USER_INFO = "https://platform.lifelog.sonymobile.com/v1/users/me"
    LIFELOG_SCOPE = ['lifelog.profile.read', 'lifelog.activities.read', 'lifelog.locations.read']

    LIFELOG_GET_DATA = LIFELOG_USER_INFO + "/activities?start_time=" + datetime.datetime.now().strftime('%Y-%m-%d') + "T00:00:00.000Z"
    LIFELOG_GET_LOCATION = LIFELOG_USER_INFO + "/locations"

    """ https://platform.lifelog.sonymobile.com/oauth/2/authorize?client_id=7eee8b7b-79ff-4ec5-a936-e20a6bd2d1e7&scope=lifelog.profile.read+lifelog.activities.read """


class Config:
    """ Base config """
    APP_NAME = "HID TV"
    SECRET_KEY = "Oh WOOW Morty 33 Soo sEEekret 234"
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')

class DevConfig:
    """ Dev config """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:8KGnb43SR554uJU@localhost/hid-tv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')

class ProdConfig:
    """ Dev config """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql://root:8KGnb43SR554uJU@localhost/hid-tv'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
