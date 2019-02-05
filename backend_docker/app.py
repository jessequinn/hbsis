from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify


db_connect = create_engine('sqlite:///city.list.db')
app = Flask(__name__)
api = Api(app)


class CityID(Resource):
    '''

    User most provide country and city.

    :return: integer

    '''
    def get(self, country, city):
        conn = db_connect.connect()
        query = conn.execute("SELECT id FROM cities WHERE country = '%s' AND name = '%s';" % (country, city))
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)

class Countries(Resource):
    ''''

    Call returns countries.

    :return: List

    '''
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("SELECT DISTINCT country FROM cities ORDER BY country ASC;")
        result = {'data': [i[0] for i in query.cursor.fetchall()]}
        return jsonify(result)

api.add_resource(CityID, '/<country>/<city>')
api.add_resource(Countries, '/countries')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='5050')
