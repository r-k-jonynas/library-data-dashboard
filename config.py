import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # This is not a real secret key :)
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'something_very_very_very_secret!5'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
