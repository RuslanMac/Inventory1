import os
import urllib
basedir = os.path.abspath(os.path.dirname(__file__))



class Config(object):
	SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
	SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
		'sqlite:///' + os.path.join(basedir, 'app2.db')
	'''params = urllib.parse.quote_plus('DRIVER={SQL Server};SERVER=DESKTOP-19PT7TH;DATABASE=Test1DB;Trusted_Connection=yes;')
	SQLALCHEMY_DATABASE_URI = 'mssql+pyodbc:///?odbc_connect=%s' % params'''
	SQLALCHEMY_TRACK_MODIFICATIONS = False

	