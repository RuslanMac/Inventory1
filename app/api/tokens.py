from flask import jsonify
from app import db
from app.api import bp
from app.api.auth import basic_auth, token_auth
from app.models import Worker


@bp.route('/tokens', methods=['POST'])
@basic_auth.login_required
def get_token():
	token =  Worker.get_token(basic_auth.current_user())
	db.session.commit()
	return jsonify({'token': token })


@bp.route('/tokens', methods=['DELETE'])
@token_auth.login_required
def revoke_token():
	token_auth.current_user().revoke_token()
	db.session.commit()
	return '', 204