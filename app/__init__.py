from config import Config
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
# from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import logging
import os
from logging.handlers import RotatingFileHandler  # SMTPHandler


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'
# mail = Mail(app)
bootstrap = Bootstrap(app)


from app import errors, models, routes

# mail and file error logging
if not app.debug:

    # if app.config['MAIL_SERVER']:
    #     auth = None

    # if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
    #     auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])

    # secure = None
    #     if app.config['MAIL_USE_TLS']:
    #        secure = ()

    # mail_handler = SMTPHandler(
    #     mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
    #     fromaddr='no-reply@' + app.config['MAIL_SERVER'],
    #     toaddrs=app.config['ADMINS'], subject='my_site Failure',
    #     credentials=auth, secure=secure)
    #     mail_handler.setLevel(logging.ERROR)
    #     app.logger.addhandler(mail_handler)

    # logging to file
    if not os.path.exists('logs'):
        os.mkdir('logs')

    # rotate logs, limit 10KB, keep ten log tiles as backup
    file_handler = RotatingFileHandler('logs/my_site.log', maxBytes=10240,
                                       backupCount=10)

    # format log entry
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))

    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('my_site startup')
