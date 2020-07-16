from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from config import Config
from sqlalchemy.ext.automap import automap_base
import urllib
import pyodbc



app = Flask(__name__)
app.config.from_object(Config)

db = SQLAlchemy(app)
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

from app.api import bp as api_bp
app.register_blueprint(api_bp, url_prefix='/api')





from app import routes, models




