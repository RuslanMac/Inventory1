from flask import jsonify, request
from app import db
from app.models import Object, Worker, Movement, Division, Placement, Operation
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import error_response
from sqlalchemy import text
from flask_cors import CORS, cross_origin
import datetime


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
	operations = Operation.query.all()
	data = {
			'operations': [operation.name for operation in operations]
	}
	return jsonify(data)

@bp.route('/division', methods=['GET'])
@token_auth.login_required
@cross_origin()
def get_divisions():
	divisions = Division.query.all()
	data = [division.division_name for division in divisions]

	return jsonify(data)  

  

@bp.route('/placement', methods=['POST'])
@token_auth.login_required
@cross_origin()
def add_placement():
	row = request.get_json()
	placement = Placement(placement_name = row['placement'], division_id = Division.query.filter_by(division_name=row['division_name']).first().id)
	db.session.add(placement)
	db.session.commit()
	return jsonify({'answer': 'ok'  })


@bp.route('/placement/<division>', methods=['GET'])
@token_auth.login_required
@cross_origin()
def placements(division):
	#placements = Placement.query.filter_by(division_id =Division.query.filter_by(division_name=division).id).all()
	placement = Division.query.filter_by(division_name=division).first().placements.all()
	data = [placement.placement_name for placement in placements]

	return jsonify(data)

@bp.route('/register', methods=['POST'])
@cross_origin()
def register():
	row = request.get_json()
	password = row['password']
	confirm_password = row['confirm_password']
	if password != confirm_password:
		return error_response(400, "The Confirm Password confirmation does not match")

	worker = Worker(login=row['login'])
	worker.set_password(row['password'])
	db.session.add(worker)
	db.session.commit()



	return jsonify({'request': 'ok'})



@bp.route('/object/<oid>/latest', methods=['GET'])
@token_auth.login_required
@cross_origin()
def get_latest_info_object(oid):
	object_info = Object.query.get(oid)
	object_movement_info = Movement.query.filter_by(oid =oid).order_by(Movement.operation_time.desc()).first()

	data = {
				"object_id": object_info.id,
				"name": object_info.name,
				"description": object_info.description,
				"barcode": object_info.barcode,
				"operation": Operation.query.get(object_movement_info.operation_id).name,
				"division": Division.query.get(Placement.query.get(object_movement_info.placement_id).division_id).division_name,
				"placement": Placement.query.get(  object_movement_info.placement_id).placement_name,
				"movement": object_movement_info.description,
				"movement_info": object_movement_info.asinfo,
				"date": object_movement_info.operation_time
			}

	

	

	

	return jsonify(data)
  




'''@bp.route('/object/new', methods=['POST'])
@cross_origin()
def add_new_objects():
	row = request.get_json()
	db.engine.execute("""INSERT INTO [Objects] ([object_Name], [description], [barcode])
						VALUES (?, ?, ?)""", (row['object_Name'], row['description'] ,row['barcode'] ))
	db.engine.execute("""INSERT INTO [Movement] ([operation_id], [division_id], [oid],     [description], [asinfo], [operation_date])
						VALUES ((SELECT [Operation].operation_id
								FROM [Operation]
								WHERE [Operation].operation_Name = ?), 
								(SELECT [Division].division_id
								FROM [Division]
								WHERE [Division].[Name] = ?),
								(SELECT [Objects].[oid]
								FROM [Objects]
								WHERE [Objects].[object_Name]  = ?), ?, ?, ?)""", (row['operation'], row['division'], row['object_Name'],  row['description'], row['asinfo'], row['date']))
	return jsonify({'data': 'ok'})
'''

@bp.route('/object/find', methods=['POST'])
@cross_origin()
def get_objects():
	row = request.get_json()
	the_objects = Object.query
	if row['object_id'] is not None:
		search = "{}%".format(row['object_id'])

		the_objects = the_objects.filter(Object.id.like(search))
	if row['barcode']:
		search = "{}%".format(row['barcode'])

		the_objects = the_objects.filter(Object.barcode.like(search))

	if row['name']:
		search = "{}%".format(row['name'])

		the_objects = the_objects.filter(Object.name.like(search))

	if row['placement']:
		the_objects_movements = the_objects.all().movements

		the_objects_movements = the_objects_movements.filter_by(placement_id=row['placement'])

		
	'''if row['name']:
		search = "{}%".format(row['name'])

		the_objects = the_objects.filter_by(Objects.tags.like(search)).all()
		pass
	if row['placement']:
		the_objects = the_objects.filter_by(placement_id=Placement.query.filter_by(name=row['placement']).first()).all()
		pass
	if row['division']:
		the_objects = the_objects.join(Placement, Placement.placement_id = Object.placement_id)
		pass
	if row['movement']:
		pass
	if row['movement_info']:
		pass'''

	data = [{
				'object_id': the_object.object_id,
				'barcode': the_object.barcode,
				'name': the_object.name,
				'placement': the_object.placement,
				'division': the_object.division_name,
				'movement': the_object.description,
				'movement_info': the_object.asstatus        

			}
			 for the_object in the_objects]
	return jsonify({'data': data})






@bp.route('/report/motion', methods=['POST'])
@token_auth.login_required
@cross_origin()
def get_report_motion():
	row = request.get_json()
	object_id = row['object_id']
	begin = row['begin']
	end = row['end']
	object1 = Object.query.get(object_id)
	object_reports = Object.query.filter_by(id = object_id).first().movements

	data =  [{
				"operation": object_report.operation_id,
				"date_operation": object_report.operation_time,
				"placement": Placement.query.get(object_report.placement_id).placement_name,
				"previous_placement":   Placement.query.get(object_report.from_placement_id).placement_name,  
				"movement": object_report.description,
				"movement_info": object1.asstatus
	} for object_report in object_reports]
	return jsonify({"object_id": object1.id,  
					"name": object1.name,
					"material_objects": data})


	


@bp.route('/object/new', methods=['POST'])
@token_auth.login_required
@cross_origin()
def get_add_object():
	row = request.get_json()
	the_objectx = Object(id=row['object_id'], name=row['name'], description=row['description'], barcode=row['barcode'])
	db.session.add(the_objectx)
	db.session.commit()
	name=row['operation']
	movement = Movement(oid =row['object_id'], operation_id=Operation.query.filter_by(name=row['operation']).first().id, placement_id =Placement.query.filter_by(placement_name=row['placement']).first().id, description=row['movement'],  operation_time=datetime.datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S'), asinfo=row['movement_info'])
	db.session.add(movement)
	db.session.commit()
	return jsonify({'answer': 'ok'})  
	
		





@bp.route('/object')
@token_auth.login_required
@cross_origin()
def object_change_location():
	row = request.get_json()
	the_object = row['object_id']
	movement = Movement(oid = the_object, operation_id=Operation.query.filter_by(name=row['operation']).first().id, placement_id =Placement.query.filter_by(placement_name=row['placement']).first().id, description=row['movement'], operation_time=datetime.datetime.strptime(row['date'],  '%Y-%m-%d %H:%M:%S'), asinfo=row['movement_info'])
	db.session.add(movement)
	db.session.commit()
	return jsonify({'answer': 'ok  '})



@bp.route('/division', methods=['POST'])
@token_auth.login_required
@cross_origin()
def add_the_division():
	row = request.get_json()
	division = Division(division_name=row['division'])
	db.session.add(division)
	db.session.commit()




@bp.route('/report/balance/division/<division>/placement/<placement>', methods=['GET'])
@token_auth.login_required
@cross_origin()
def get_balance_objects():
	objects = Object.query.all()





