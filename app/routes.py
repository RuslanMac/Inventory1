from app import app, db
from flask import jsonify
from app.models import Object

@app.route('/')
@app.route('/index')
def index():
	return 'Hello, World'

@app.route('/objects')
def get_objects():
	#object1 = Objects(Name='принтер Canon', barcode='112342467', inv_number='123412')
	#db.session.add(object1)
	#db.session.commit()
	objects= db.session.query(Objects).filter(Objects.barcode == 12345).first()
	return jsonify({'objects_count': objects.Name})
