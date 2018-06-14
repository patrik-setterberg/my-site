import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # secret key protects against CSRF-attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-kvarjo'

    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # settings for pagination of blog posts
    POSTS_PER_PAGE = 3

    # e-mail server details
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['admin-email@example.com']
