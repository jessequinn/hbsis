from flask import Flask, request
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps
from flask_jsonpify import jsonify


db_connect = create_engine('sqlite:///city.list.db')
app = Flask(__name__)
api = Api(app)


class Cities(Resource):
    def get(self):
        conn = db_connect.connect()
        query = conn.execute("select id, name, country from cities;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        return jsonify(result)


api.add_resource(Cities, '/cities')

if __name__ == '__main__':
    app.run(port='5002')
