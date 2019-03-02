from flask import Flask, request
from flask_restplus import Api, Resource, fields
from flask_sqlalchemy import SQLAlchemy
from geopy import distance
import sys
from flask_restplus import reqparse
from sqlalchemy import Column, Integer, String

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@127.0.0.1/goldrushdb'
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
            tmp_dis = distance.great_circle((aider.longitude, aider.latitude), (longitude, latitude)).miles
            if tmp_dis < min_distance:
                target_airder = aider
                min_distance = tmp_dis

        return AiderDAO.update_patient_position(target_airder, (longitude, latitude))


class AiderDAO:
    @classmethod
    def get(cls):
        return db.session.query(Aider).all()

    @classmethod
    def update_patient_position(cls, aider, patient_position):
        aider = db.session.query(Aider).filter_by(id=aider.id).first()
        aider.patient_position = patient_position[0] + ',' + patient_position[1]
        db.session.commit()
        return aider


if __name__ == '__main__':
    app.run(debug=True)
