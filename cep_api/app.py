# -*- coding:utf-8 -*-

from flask import Flask
from flask_restful import Api
from mongoengine import connect

app = Flask(__name__)
app.config.from_object('config')

connection = connect(
    db=app.config['MONGO_DBNAME'],
    host=app.config['MONGODB_HOST'],
    port=app.config['MONGODB_PORT'],
)

api = Api(app)


# This import must be here to avoid circular import
from cep_api.resources.cep import CepAPI, CepListAPI

api.add_resource(CepAPI, '/zipcode/<string:zipcode>')
api.add_resource(CepListAPI, '/zipcode/', endpoint='ceplist')