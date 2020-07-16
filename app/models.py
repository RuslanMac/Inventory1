import base64
import json
from app import db
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

class Worker():
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

