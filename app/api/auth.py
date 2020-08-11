from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from app.api.errors import error_response
from app.models import Worker
from app import db


basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()


@basic_auth.verify_password
def verify_password(login, password):
	workers = Worker.query.filter_by(login=login).first()
	if workers is None:
		return False

	g.current_user = workers
	return workers.check_password(password)

@basic_auth.error_handler
def basic_auth_error(status):
	return error_response(status)



@token_auth.verify_token
def verify_token(token):
	g.current_user = Worker.check_token(token) if token else None
	return g.current_user is not None




@token_auth.error_handler
def token_auth_error(status):
	return error_response(status)






