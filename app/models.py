'''import base64
import json
from app import db, login
from sqlalchemy.ext.automap import automap_base
import os
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta








Base = automap_base()
Base.prepare(db.engine, reflect=True)

Objects = Base.classes.Objects
Workers = Base.classes.Workers
Operations = Base.classes.Operation
Divisions = Base.classes.Division
Movements = Base.classes.Movement
Placements = Base.classes.Placement

class Worker():

	@staticmethod
	def set_password_hash(password):
		return generate_password_hash(password)

	
	@staticmethod
	def check_password(workers, password):
		return check_password_hash(workers.password_hash, password)

	@staticmethod
	def check_token(token):
		workers = db.session.query(Workers).filter(Workers.token == token).first()
		if workers is None or workers.token_expiration < datetime.utcnow():
			return None
		return workers

	@staticmethod
	def get_token(workers, expires_in=3600):
		now = datetime.utcnow()
		if workers.token and workers.token_expiration > now + timedelta(seconds=60):
			return workers.token
		workers.token = base64.b64encode(os.urandom(24)).decode('utf-8')
		workers.token_expiration = now + timedelta(seconds=expires_in)
		db.session.commit()
		return workers.token

	@staticmethod
	def revoke_token(workers):
		workers.token_expiration = datetime.utcnow() -  tinedelta(seconds=1)

'''
from app import db, login
from flask_login import UserMixin


import base64
import json
from sqlalchemy.ext.automap import automap_base
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta







class Object(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128), index=True, unique=True)
	barcode = db.Column(db.Integer, index=True, unique=True)
	inv_number = db.Column(db.Integer, index=True, unique=True)
	description = db.Column(db.String(128))
	asstatus = db.Column(db.String(128))
	movements = db.relationship('Movement', backref='object_id', lazy='dynamic')

class Movement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	operation_time = db.Column(db.DateTime)
	operation_id = db.Column(db.Integer, db.ForeignKey('operation.id'))
	description = db.Column(db.String(128))
	asinfo = db.Column(db.String(128))
	placement_id = db.Column(db.Integer, db.ForeignKey('placement.id'))
	from_placement_id = db.Column(db.Integer, db.ForeignKey('placement.id'))
	oid = db.Column(db.Integer, db.ForeignKey('object.id'))



class Operation(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(128))

class Division(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	division_name = db.Column(db.String(128))
	placements = db.relationship('Placement', backref='division', lazy='dynamic')

class Placement(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	placement_name = db.Column(db.String(128))
	division_id = db.Column(db.Integer, db.ForeignKey('division.id'))



class Worker(UserMixin, db.Model):
	id = db.Column(db.Integer, primary_key = True)
	login = db.Column(db.String(128), unique=True)
	password_hash = db.Column(db.String(128))
	token = db.Column(db.String(32), index=True, unique=True)
	token_expiration = db.Column(db.DateTime)

	def __repr__(self):
		return '<User {}>'.format(self.login)

	def set_password(self, password):
		self.password_hash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.password_hash, password)

	def get_token(self, expires_in=3600):
		now = datetime.utcnow()
		if self.token and self.token_expiration > now + timedelta(seconds=60):
			return self.token 
		self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
		self.token_expiration = now + timedelta(seconds=expires_in)
		db.session.add(self)
		return self.token

	def revoke_token(self):
		self.token_expiration = datetime.utcnow() - timedelta(seconds=1)





	@staticmethod
	def check_token(token):
		worker = Worker.query.filter_by(token=token).first()
		if worker is None or worker.token_expiration < datetime.utcnow():
			return None
		return worker



