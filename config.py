import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # secret key protects against CSRF-attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-kvarjo'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
