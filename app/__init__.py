import logging
from flask import Flask, current_app
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from sqlalchemy import create_engine
from flask_login import LoginManager
from config import Config
from logging.handlers import RotatingFileHandler
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy


import os




#CORS(app)

db = SQLAlchemy()


migrate = Migrate()

login = LoginManager()

def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(config_class)

	db.init_app(app)
	migrate.init_app(app, db)
	login.init_app(app)


	from app.api import bp as api_bp
	app.register_blueprint(api_bp, url_prefix='/api')

	if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/inventory1.log',
                                               maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Inventory1 startup')


	

	return app



from app import routes, models




