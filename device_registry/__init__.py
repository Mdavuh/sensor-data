import markdown
import os
import shelve

# Import the framework
from flask import Flask, g
from flask_restful import Resource, Api, reqparse

# Create an instance of Flask
app = Flask(__name__)

# Create the API
api = Api(app)

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = shelve.open("sensors.db")
    return db

@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/")
def index():
    """Present some documentation"""

    # Open the README file
    with open(os.path.dirname(app.root_path) + '/README.md', 'r') as markdown_file:

        # Read the content of the file
        content = markdown_file.read()

        # Convert to HTML
        return markdown.markdown(content)


class SensorsList(Resource):
    def get(self):
        shelf = get_db()
        keys = list(shelf.keys())

        sensors = [
                    {
                    "gyroscope_id": 1,
                    "trip_id": 3,
                    "x_value": 1.11304,
                    "y_value": 1.66957,
                    "z_value": -0.83478,
                    "timestamp": "2017-01-19 16:19:03.051205"
                    },
                    {
                    "gyroscope_id": 2,
                    "trip_id": 3,
                    "x_value": 1.46087,
                    "y_value": 1.94783,
                    "z_value": -0.69565,
                    "timestamp": "2017-01-19 16:19:03.093157"
                    },
                    {
                    "gyroscope_id": 3,
                    "trip_id": 3,
                    "x_value": 1.32174,
                    "y_value": 1.8087,
                    "z_value": -1.11304,
                    "timestamp": "2017-01-19 16:19:03.134884"
                    },
                    {
                    "gyroscope_id": 4,
                    "trip_id": 3,
                    "x_value": 1.11304,
                    "y_value": 1.87826,
                    "z_value": -0.90435,
                    "timestamp": "2017-01-19 16:19:03.176626"
                    },
                    {
                    "gyroscope_id": 5,
                    "trip_id": 3,
                    "x_value": 1.18261,
                    "y_value": 1.94783,
                    "z_value": -0.69565,
                    "timestamp": "2017-01-19 16:19:03.218367"
                    },
                    {
                    "gyroscope_id": 6,
                    "trip_id": 3,
                    "x_value": 1.11304,
                    "y_value": 1.94783,
                    "z_value": -0.69565,
                    "timestamp": "2017-01-19 16:19:03.260101"
                    },
                    {
                    "gyroscope_id": 7,
                    "trip_id": 3,
                    "x_value": 1.18261,
                    "y_value": 1.87826,
                    "z_value": -0.76522,
                    "timestamp": "2017-01-19 16:19:03.301868"
                    },
                    {
                    "gyroscope_id": 8,
                    "trip_id": 3,
                    "x_value": 1.25217,
                    "y_value": 1.87826,
                    "z_value": -1.04348,
                    "timestamp": "2017-01-19 16:19:03.343608"
                    },
                    {
                    "gyroscope_id": 9,
                    "trip_id": 3,
                    "x_value": 0.97391,
                    "y_value": 1.8087,
                    "z_value": -0.76522,
                    "timestamp": "2017-01-19 16:19:03.385370"
                    },
                    {
                    "gyroscope_id": 10,
                    "trip_id": 3,
                    "x_value": 1.46087,
                    "y_value": 1.66957,
                    "z_value": -0.69565,
                    "timestamp": "2017-01-19 16:19:03.427319"
                    }
                    ]

        for key in keys:
            sensors.append(shelf[key])

        return {'message': 'Success', 'data': sensors}, 200

    def post(self):
        parser = reqparse.RequestParser()

        parser.add_argument('gyroscope_id', required=True)
        parser.add_argument('trip_id', required=True)
        parser.add_argument('x_value', required=True)
        parser.add_argument('y_value', required=True)
        parser.add_argument('z_value', required=True)
        parser.add_argument('timestamp', required=True)

        # Parse the arguments into an object
        args = parser.parse_args()

        shelf = get_db()
        shelf[args['gyroscope_id']] = args

        return {'message': 'Sensor registered', 'data': args}, 201


class Sensor(Resource):
    def get(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Sensor data not found', 'data': {}}, 404

        return {'message': 'Sensor data found', 'data': shelf[identifier]}, 200

    def delete(self, identifier):
        shelf = get_db()

        # If the key does not exist in the data store, return a 404 error.
        if not (identifier in shelf):
            return {'message': 'Sensor data not found', 'data': {}}, 404

        del shelf[identifier]
        return '', 204


api.add_resource(SensorsList, '/sensordata')
api.add_resource(Sensor, '/sensor/<string:identifier>')