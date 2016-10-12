import os
import datetime
basedir = os.path.abspath(os.path.dirname(__file__))

class Auth:
    """ Google project credentials """
    GOOGLE_CLIENT_ID = ('')
    GOOGLE_CLIENT_SECRET = ''
    GOOGLE_REDIRECT_URI = 'https://localhost:5000/google-callback'
    GOOGLE_AUTH_URI = 'https://accounts.google.com/o/oauth2/auth'
    GOOGLE_TOKEN_URI = 'https://accounts.google.com/o/oauth2/token'
    GOOGLE_USER_INFO = 'https://www.googleapis.com/userinfo/v2/me'
    GOOGLE_SCOPE = ['profile', 'email']

    """ Lifelog credentials """
    LIFELOG_CLIENT_ID = ""
    LIFELOG_SECRET = ""
    LIFELOG_AUTH_URI = "https://platform.lifelog.sonymobile.com/oauth/2/authorize"
    LIFELOG_TOKEN_URI = "https://platform.lifelog.sonymobile.com/oauth/2/token"
    LIFELOG_REFRESH_TOKEN = "https://platform.lifelog.sonymobile.com/oauth/2/refresh_token"
    LIFELOG_REDIRECT_URI = 'https://localhost:5000/lifelog-callback'
    LIFELOG_USER_INFO = "https://platform.lifelog.sonymobile.com/v1/users/me"
    LIFELOG_SCOPE = ['lifelog.profile.read', 'lifelog.activities.read', 'lifelog.locations.read']

    LIFELOG_GET_DATA = LIFELOG_USER_INFO + "/activities?start_time=" + datetime.datetime.now().strftime('%Y-%m-%d') + "T00:00:00.000Z"
    LIFELOG_GET_LOCATION = LIFELOG_USER_INFO + "/locations"


class Config:
    """ Base config """
    APP_NAME = "HID TV"
    SECRET_KEY = ""
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')

class DevConfig:
    """ Dev config """
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # uploads
    UPLOAD_FOLDER = os.path.join(basedir, 'static/uploads')

class ProdConfig:
    """ Dev config """
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    "dev": DevConfig,
    "prod": ProdConfig,
    "default": DevConfig
}
