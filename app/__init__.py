import logging
from flask import Flask, current_app
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate
from sqlalchemy import create_engine
from config import Config
from logging.handlers import RotatingFileHandler
from sqlalchemy.ext.automap import automap_base
from flask_sqlalchemy import SQLAlchemy
import urllib
import pyodbc
import os



app = Flask(__name__)
app.config.from_object(Config)
#CORS(app)

db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])


migrate = Migrate(app, db)

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')


if not os.path.exists('logs'):
	os.mkdir('logs')
file_handler = RotatingFileHandler('logs/inventory1.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
	'%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)

app.logger.setLevel(logging.INFO)
app.logger.info('Inventory1 startup')



from app import routes, models




