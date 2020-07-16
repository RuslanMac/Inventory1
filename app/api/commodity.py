from flask import jsonify
from app import db
from app.models import Objects, Workers, Operations, Divisions,   Worker
from app.api import bp
from app.api.auth import token_auth


@bp.route('/objects', methods = ['GET'])
def get_object():
	workers = db.session.query(Workers).filter(Workers.login == 'John').first()
	workers.token = 12345671248
	db.session.commit()
	return workers.login
	#object1 = db.session.query(Objects).filter(Objects.barcode == barcode).first()
	#return jsonify({'object_id': object1.oid,
			#		'name': object1.Name,
			#		'barcode': object1.barcode,
			#		'inv_number': object1.inv_number})

@bp.route('/operations', methods=['GET'])
@token_auth.login_required
def get_operations():
	operations = db.session.query(Operations).all()
	data = {
			'operations': [operation.Name for operation in operations]
	}
	return jsonify(data)

@bp.route('/divisions', methods=['GET'])
@token_auth.login_required
def get_divisions():
	divisions = db.session.query(Divisions).all()
	data = {
			'divisions': [division.Name for division in divisions]
	}









