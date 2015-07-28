# -*- coding:utf-8 -*-

from flask_restful import Resource
from flask import request as http_request
import requests
import json
from ..app import app
from cep_api.models import ZipCode
from commons.utils import model_to_dict


class CepAPI(Resource):

    def post(self, zipcode):
        response = requests.get(app.config['POSTMON_BASE_URL'].format(zipcode))
        response_to_dict = json.loads(response.content)
        ZipCode.save_zipcode(response_to_dict)
        return '', 201

    def get(self, zipcode):
        zip_code_obj = ZipCode.objects.get(zip_code=zipcode)
        zip_code_obj = model_to_dict(zip_code_obj, exclude=['id'])
        return zip_code_obj

    def delete(self, zipcode):
        zip_code_obj = ZipCode.objects.get(zip_code=zipcode)
        zip_code_obj.delete()
        return '', 204


class CepListAPI(Resource):

    def get(self):
        limit = http_request.args.get('limit')

        zip_code_list = ZipCode.objects.order_by('-id')

        if limit and limit.isdigit():

            limit = int(limit)

            if zip_code_list.count() > limit:
                zip_code_list = zip_code_list[:limit]

        zip_code_list = [model_to_dict(zip_code, exclude=['id']) for zip_code in zip_code_list[:limit]]

        return zip_code_list

