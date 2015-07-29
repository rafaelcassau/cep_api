# -*- coding:utf-8 -*-
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api
from mongoengine import connect
import os
import logging

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

app = Flask(__name__)
app.config.from_object('config')

# log config
MAX_BYTES = 1 * 1024 * 1024
ROTATE = 10
MODE = 'a'
PATH_FILE = '{}/cep_api.log'.format(BASE_DIR)

file_handler = RotatingFileHandler(PATH_FILE, MODE, MAX_BYTES, ROTATE)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s: %(lineno)d]'))
file_handler.setLevel(logging.DEBUG)
app.logger.setLevel(logging.DEBUG)
app.logger.addHandler(file_handler)

#mongo config
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