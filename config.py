
import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'OxycoolThunderbird'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
            'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER='smtp.gmail.com'
    MAIL_PORT=587
    MAIL_USE_TLS=1
    MAIL_USERNAME="ketanrockstar007@gmail.com"
    MAIL_PASSWORD="wannahackmyaccountfuckyouasshole"
    ADMINS = ['ketanrockstar007@gmail.com']
