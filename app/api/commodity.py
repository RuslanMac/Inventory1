from flask import jsonify, request
from app import db
from app.models import Objects, Workers, Operations, Divisions,  Placements, Movements,  Worker
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response
from sqlalchemy import text
from flask_cors import CORS, cross_origin


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
@cross_origin()
@token_auth.login_required
def get_operations():
	operations = db.session.query(Operations).all()
	data = {
			'operations': [operation.Name for operation in operations]
	}
	return jsonify(data)

@bp.route('/divisions', methods=['GET'])
@token_auth.login_required
@cross_origin()
def get_divisions():
	divisions = db.session.query(Divisions).all()
	data = {
			'divisions': [division.Name for division in divisions]
	}

@bp.route('/placement', methods=['POST'])
@token_auth.login_required
@cross_origin()
def add_placement():
	row = request.get_json()
	placement = Placements(Name = row['placement'], division_id = row['division'])
	db.session.add(placement)
	db.session.commit()
	return jsonify({'answer': 'ok'  })

@bp.route('/register', methods=['POST'])
def register():
	password = request.form['password']
	confirm_password = request.form['confirm_password']
	if password != confirm_password:
		return error_response(400, "The Confirm Password confirmation does not match")
	password_hash = Worker.set_password_hash(request.form['password'])


	new_worker = Workers(login = request.form['login'], password_hash = password_hash)
	db.session.add(new_worker)
	db.session.commit()
	return jsonify({'request': password})

'''@bp.route('/report/motion', methods=['POST'])
def get_report_motion():
	row = request.get_json()
	oid_report = db.session.query(Objects).join(Movements).join(Divisions, Movements.division_id == Divisions.division_id).join(Operations).filter(Objects.oid == row['oid']).filter(Movements.operation_date.between(row['begin'], row['end'])).with_entities( Movements.operation_date, Movements.asinfo, Movements.description).all()        
	data = {
		"oid": row['oid'],
		"name": row['name'],
		"material_objects": [
		{
			"operation": oidrep
			#"date_operation": oidrep.Movement_operation_date,
			#"movement": oidrep.Movement_description,
			#"movement_info": oidrep.Movement_asinfo







		}  for oidrep in oid_report]
	}
	return jsonify({'data': data})


@bp.route('/object/<oid>/latest', methods=['GET'])
def get_latest_info_object(oid):
	#objects_latest = db.session.query(Objects, Movements).join(Movements, Objects.oid == Movements.oid  ).filter(Objects.oid == oid).order_by(Movements.operation_date.desc()).first()
	objects_latest = db.engine.execute("""SELECT *
										FROM [Objects]
										JOIN [Movement] ON [Objects].oid = [Movement].oid
										JOIN [Division] ON [Division].division_id = [Movement].division_id
										WHERE [Objects].oid = ?""",('a7a7e4e0-e986-4e65-b898-26308bb76a70'))
	data = {
		"object_id": objects_latest.items()[0], 
		#"name": objects_latest[0],
		#"discription": objects_latest.description,
		#"barcode": objects_latest.barcode,
		#"operation": objects_latest[1],
		#"division": objects_latest[2],
		#"placement": objects_latest[3]
		#"movement": objects_latest.move_id,
		#"movement_info": objects_latest.movement_info,
		#"data": objects_latest.operation_data

	}
	

	return jsonify({'data': data})'''








	
		















