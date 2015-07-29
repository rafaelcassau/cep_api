# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import request as http_request
from mongoengine.errors import DoesNotExist
import requests
import json
from werkzeug.exceptions import NotFound, BadRequest, Conflict
from ..app import app
from cep_api.models import ZipCode
from cep_api.resources.validators import ZipCodeValidator, LimitValidator
from commons.http_status_code import Http
from commons.utils import model_to_dict, convert_query_set_to_list_dict


class CepAPI(Resource):

    def post(self):
        zipcode = http_request.form.get('zip_code')
        try:
            zip_code_validator = ZipCodeValidator(zipcode)
            if not zip_code_validator.is_valid():
                raise BadRequest()

            zipcode = zip_code_validator.cleaned_data['zipcode']

            if ZipCode.zipcode_exists(zipcode):
                raise Conflict()

            uri = '{}{}'.format(app.config['POSTMON_BASE_URL'], zipcode)
            response = requests.get(uri)

            if response.status_code == Http.NOT_FOUND:
                raise NotFound()

            response_to_dict = json.loads(response.content)
            ZipCode.save_zipcode(response_to_dict)

            return {'status_code': Http.CREATED}, Http.CREATED

        except BadRequest as exception:
            app.logger.error('Invalid value to parameter zipcode {}, Exception: {} '.format(zipcode, exception))
            return {'message': 'Invalid parameter', 'status_code': Http.BAD_REQUEST}, Http.BAD_REQUEST

        except Conflict:
            app.logger.error('Zipcode {} already exists on database'.format(zipcode))
            return {'message': 'Zipcode already exists', 'status_code': Http.CONFLICT}, Http.CONFLICT

        except NotFound as exception:
            app.logger.error('Error to add a zipcode {}, this zipcode not found on postmon api, Exception: {}'.format(zipcode, exception))
            return {'message': 'Zipcode not found', 'status_code': Http.NOT_FOUND}, Http.NOT_FOUND

        except Exception as exception:
            app.logger.error('Internal server error: {} '.format(exception))
            return {'message': 'Internal server error, contact the administrator', 'status_code': Http.INTERNAL_SERVER_ERROR}, Http.INTERNAL_SERVER_ERROR

    def put(self):
        zipcode = http_request.form.get('zip_code')
        try:
            zip_code_validator = ZipCodeValidator(zipcode)

            if not zip_code_validator.is_valid():
                raise BadRequest()

            zipcode = zip_code_validator.cleaned_data['zipcode']
            uri = '{}{}'.format(app.config['POSTMON_BASE_URL'], zipcode)
            response = requests.get(uri)
            response_to_dict = json.loads(response.content)

            if ZipCode.zipcode_exists(zipcode):
                ZipCode.update_zipcode(response_to_dict)
                return {'message': 'Zipcode updated', 'status_code': Http.OK}, Http.OK

            ZipCode.save_zipcode(response_to_dict)
            return {'message': 'Zipcode added', 'status_code': Http.CREATED}, Http.CREATED

        except BadRequest as exception:
            app.logger.error('Invalid value to parameter zipcode {}, Exception: {} '.format(zipcode, exception))
            return {'message': 'Invalid parameter', 'status_code': Http.BAD_REQUEST}, Http.BAD_REQUEST

        except NotFound as exception:
            app.logger.error('Error to add a zipcode {}, this zipcode not found on postmon api, Exception: {}'.format(zipcode, exception))
            return {'message': 'Zipcode not found', 'status_code': Http.NOT_FOUND}, Http.NOT_FOUND

        except Exception as exception:
            app.logger.error('Internal server error: {} '.format(exception))
            return {'message': 'Internal server error, contact the administrator', 'status_code': Http.INTERNAL_SERVER_ERROR}, Http.INTERNAL_SERVER_ERROR

    def delete(self, zipcode):
        try:
            zip_code_validator = ZipCodeValidator(zipcode)

            if not zip_code_validator.is_valid():
                raise BadRequest()

            zipcode = zip_code_validator.cleaned_data['zipcode']
            ZipCode.remove_by_zipcode(zipcode)

            return {'status_code': Http.NOT_CONTENT}, Http.NOT_CONTENT

        except BadRequest as exception:
            app.logger.error('Invalid value to parameter zipcode {}, Exception: {} '.format(zipcode, exception))
            return {'message': 'Invalid parameter', 'status_code': Http.BAD_REQUEST}, Http.BAD_REQUEST

        except DoesNotExist, exception:
            app.logger.error('Error to get a zipcode {} on database, Exception: {}'.format(zipcode, exception))
            return {'message': 'Zipcode not found', 'status_code': Http.NOT_FOUND}, Http.NOT_FOUND

        except Exception as exception:
            app.logger.error('Internal server error: {} '.format(exception))
            return {'message': 'Internal server error, contact the administrator', 'status_code': Http.INTERNAL_SERVER_ERROR}, Http.INTERNAL_SERVER_ERROR

    def get_by_zipcode(self, zipcode):
        try:
            zip_code_validator = ZipCodeValidator(zipcode)

            if not zip_code_validator.is_valid():
                raise BadRequest()

            zipcode = zip_code_validator.cleaned_data['zipcode']
            zipcode_obj = ZipCode.get_by_zipcode(zipcode)
            zipcode_dict = model_to_dict(zipcode_obj, exclude=['id'])

            return zipcode_dict

        except BadRequest as exception:
            app.logger.error('Invalid value to parameter zipcode {}, Exception: {} '.format(zipcode, exception))
            return {'message': 'Invalid parameter', 'status_code': Http.BAD_REQUEST}, Http.BAD_REQUEST

        except DoesNotExist, exception:
            app.logger.error('Error to get a zipcode {} on database, Exception: {}'.format(zipcode, exception))
            return {'message': 'Zipcode not found', 'status_code': Http.NOT_FOUND}, Http.NOT_FOUND

        except Exception as exception:
            app.logger.error('Internal server error: {} '.format(exception))
            return {'message': 'Internal server error, contact the administrator', 'status_code': Http.INTERNAL_SERVER_ERROR}, Http.INTERNAL_SERVER_ERROR

    def get(self, zipcode=None):
        if zipcode:
            return self.get_by_zipcode(zipcode)

        return self.get_list()

    def get_list(self):
        limit = ''
        try:
            limit = http_request.args.get('limit')
            limit_validator = LimitValidator(limit)

            if not limit_validator.is_valid():
                raise BadRequest()

            limit = limit_validator.cleaned_data['limit']
            zipcode_list = ZipCode.list(limit)
            zipcode_list = convert_query_set_to_list_dict(zipcode_list, exclude=['id'])

            return zipcode_list

        except BadRequest as exception:
            app.logger.error('Invalid value to parameter zipcode {}, Exception: {} '.format(limit, exception))
            return {'message': 'Invalid parameter', 'status_code': Http.BAD_REQUEST}, Http.BAD_REQUEST

        except Exception as exception:
            app.logger.error('Internal server error: {} '.format(exception))
            return {'message': 'Internal server error, contact the administrator', 'status_code': Http.INTERNAL_SERVER_ERROR}, Http.INTERNAL_SERVER_ERROR