from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app.models import Workers, Worker
from app import db


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(login, password):
	workers = db.session.query(Workers).filter(Workers.login == login).first()
	if workers and Worker.check_password(workers, password):
		return workers


@basic_auth.error_handler
def basic_auth_error(status):
	return error_response(status)



@token_auth.verify_token
def verify_token(token):
	return Worker.check_token(token) if token else None




@token_auth.error_handler
def token_auth_error(status):
	return error_response(status)






