from flask import  g, jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import Worker
from flask_cors import CORS, cross_origin


@bp.route('/login', methods=['POST'])
@cross_origin()
@basic_auth.login_required
def get_token():
	token = g.current_user.get_token()
	db.session.commit()
	return jsonify({'token': token })


@bp.route('/login', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
	g.current_user.revoke_token()
	db.session.commit()
	return '', 204