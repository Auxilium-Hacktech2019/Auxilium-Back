from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from geopy import distance
import sys
from flask_restplus import reqparse
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/goldrushdb'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://goldrush:goldrush@127.0.0.1/goldrushdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
api = Api(app)
db = SQLAlchemy(app)


patient_position_args = reqparse.RequestParser()
patient_position_args.add_argument('longitude', type=str, required=True, location='args', help='')
patient_position_args.add_argument('latitude', type=str, required=True, location='args', help='')

aider_info = api.model('Aider', {
    'id': fields.Integer,
    'name': fields.String,
    'longitude': fields.String,
    'latitude': fields.String,
    'patient_position': fields.String
})

aider_create_params = api.model('Aider Create Params', {
    'name': fields.String(required=True, description='Aider Name'),
    'longitude': fields.String,
    'latitude': fields.String
})

aider_aid_over_params = api.model('Aider Aids Over Params',{
    'name': fields.String
})


@api.route('/schedule')
class ScheduleAider(Resource):
    @api.doc(description='Shceduel an aider')
    @api.expect(patient_position_args)
    @api.marshal_with(aider_info)
    def post(self):
        args = request.args
        longitude = args.get('longitude')
        latitude = args.get('latitude')
        return AiderModuleOp.schedule(longitude, latitude)


@api.route('/', strict_slashes=False)
class AiderCreate(Resource):
    @api.doc(description='Create a aider')
    @api.expect(aider_create_params)
    def post(self):
        params = request.json
        name = params.get('name')
        longitude = params.get('longitude', '')
        latitude = params.get('latitude', '')
        AiderModuleOp.create(name, longitude, latitude)


@api.route('/<aider_name>')
class Aider(Resource):
    @api.doc(description='Get an aider by name')
    @api.marshal_with(aider_info)
    def get(self, aider_name):
        aider = AiderModuleOp.get_aider(aider_name)
        if aider is None:
            raise Exception("No Found")
        return aider


@api.route('/update_patient', strict_slashes=False)
class AiderAidOver(Resource):
    @api.doc(description='Aid Over')
    @api.expect(aider_aid_over_params)
    @api.marshal_with(aider_info)
    def post(self):
        params = request.json
        name = params.get('name')
        aider = AiderModuleOp.get_aider(name)
        AiderDAO.update_patient_position(aider)
        return aider


class Aider(db.Model):
    __tablename__ = 'aider'
    type = 'table'

    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=True)
    longitude = Column(String(200), default='')
    latitude = Column(String(200), default='')
    patient_position = Column(String(200), default='')

    def __str__(self):
        return "Aider[{}]".format(self.name)


class AiderModuleOp(object):
    @classmethod
    def schedule(cls, longitude, latitude):
        aiders = AiderDAO.get()
        target_airder, min_distance = None, sys.float_info.max
        for aider in aiders:
            tmp_dis = distance.great_circle((aider.latitude, aider.longitude), (latitude, longitude)).miles
            if tmp_dis < min_distance:
                target_airder = aider
                min_distance = tmp_dis

        from aider import operators
        fh = operators.FindHospital(latitude + "," + longitude)  # find hospital
        hos_latitude, hos_longitude = fh.find_hospital()
        fare_id = operators.get_fare_id(longitude, latitude, hos_longitude, hos_latitude)
        operators.request_ride(fare_id)  # schedule uber
        return AiderDAO.update_patient_position(target_airder, (longitude, latitude))

    @classmethod
    def create(cls, name, longitude, latitude):
        aider = Aider(name=name, longitude=longitude, latitude=latitude)
        db.session.add(aider)
        db.session.commit()

    @classmethod
    def get_aider(cls, name):
        return AiderDAO.get(name)


class AiderDAO:
    @classmethod
    def get(cls, name=None):
        if name is None:
            return db.session.query(Aider).all()
        return Aider.query.filter_by(name=name).first()

    @classmethod
    def update_patient_position(cls, aider, patient_position=None):
        if aider is None:
            raise Exception("Not Found")
        aider = db.session.query(Aider).filter_by(id=aider.id).first()
        if patient_position is None or len(patient_position) == 0:
            aider.patient_position = None
        else:
            aider.patient_position = patient_position[0] + ',' + patient_position[1]
        db.session.commit()
        return aider


if __name__ == '__main__':
    # app.run(debug=False, host='127.0.0.1')
    app.run(debug=False, host='0.0.0.0')
