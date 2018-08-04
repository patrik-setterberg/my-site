import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # DEBUG = True

    UPLOADED_IMAGES_DEST = os.path.join(basedir, 'app/static/img/')
    UPLOADED_IMAGES_URL = 'http://localhost:5000/static/img/'

    # secret key protects against CSRF-attacks
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-kvarjo'

    # check for existing database or setup new database file in root dir
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # settings for pagination of blog posts
    POSTS_PER_PAGE = 10
    TITLES_PER_PAGE = 20
    COMMENTS_PER_PAGE = 10

    # KEYS FOR LOCALHOST ONLY. MUST FIX SOMEHOW LATER.
    RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
    RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'

    # e-mail server details
    # MAIL_SERVER = os.environ.get('MAIL_SERVER')
    # MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    # MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    # MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    # MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    # ADMINS = ['admin-email@example.com']
