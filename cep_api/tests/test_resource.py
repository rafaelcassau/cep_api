# # -*- coding:utf-8 -*-

import unittest
import requests

from cep_api.models import ZipCode
from commons.http_status_code import Http
import json
from ..app import app


class ZipCodePostResourceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.CEP_API_BASE_URL = 'http://localhost:5000/zipcode/'

    @classmethod
    def tearDownClass(cls):
        ZipCode.objects.all().delete()

    def test_post_cleaned_zipcode(self):
        response = requests.post(self.CEP_API_BASE_URL, data={'zip_code': '14810000'})
        assert response.status_code == Http.CREATED

    def test_post_mask_zipcode(self):
        response = requests.post(self.CEP_API_BASE_URL, data={'zip_code': '14815-000'})
        assert response.status_code == Http.CREATED

    def test_post_zipcode_not_exists(self):
        response = requests.post(self.CEP_API_BASE_URL, data={'zip_code': '14810-001'})
        assert response.status_code == Http.NOT_FOUND

    def test_post_zipcode_already_exists(self):
        requests.post(self.CEP_API_BASE_URL, data={'zip_code': '14830-000'})
        response = requests.post(self.CEP_API_BASE_URL, data={'zip_code': '14830-000'})
        assert response.status_code == Http.CONFLICT

    def test_post_alpha_zipcode(self):
        response = requests.post(self.CEP_API_BASE_URL, data={'zip_code': 'aaaaaaaaa'})
        assert response.status_code == Http.BAD_REQUEST

    def test_post_different_len_zipcode(self):
        response = requests.post(self.CEP_API_BASE_URL, data={'zip_code': '1402-260'})
        assert response.status_code == Http.BAD_REQUEST


class ZipCodePutResourceTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.CEP_API_BASE_URL = 'http://localhost:5000/zipcode/'

    @classmethod
    def tearDownClass(cls):
        ZipCode.objects.all().delete()

    def test_put_cleaned_zipcode(self):
        response = requests.put(self.CEP_API_BASE_URL, data={'zip_code': '14810000'})
        assert response.status_code == Http.CREATED

    def test_put_mask_zipcode(self):
        response = requests.put(self.CEP_API_BASE_URL, data={'zip_code': '14815-000'})
        assert response.status_code == Http.CREATED

    def test_put_zipcode_not_exists(self):
        response = requests.put(self.CEP_API_BASE_URL, data={'zip_code': '14810-001'})
        assert response.status_code == Http.NOT_FOUND

    def test_put_zipcode_already_exists(self):
        requests.post(self.CEP_API_BASE_URL, data={'zip_code': '14830-000'})
        response = requests.put(self.CEP_API_BASE_URL, data={'zip_code': '14830-000'})
        assert response.status_code == Http.OK

    def test_put_alpha_zipcode(self):
        response = requests.put(self.CEP_API_BASE_URL, data={'zip_code': 'aaaaaaaaa'})
        assert response.status_code == Http.BAD_REQUEST

    def test_put_different_len_zipcode(self):
        response = requests.put(self.CEP_API_BASE_URL, data={'zip_code': '1402-260'})
        assert response.status_code == Http.BAD_REQUEST


class TestDeleteResource(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.CEP_API_BASE_URL = 'http://localhost:5000/zipcode/'
        for zipcode in [14810000, 14820000]:
            requests.post(cls.CEP_API_BASE_URL, data={'zip_code': zipcode})

    @classmethod
    def tearDownClass(cls):
        ZipCode.objects.all().delete()

    def test_delete_cleaned_zip_code(self):
        response = requests.delete('{}{}/'.format(self.CEP_API_BASE_URL, '14810000'))
        assert response.status_code == Http.NOT_CONTENT

    def test_delete_mask_zipcode(self):
        response = requests.delete('{}{}/'.format(self.CEP_API_BASE_URL, '14820-000'))
        assert response.status_code == Http.NOT_CONTENT

    def test_delete_zipcode_not_exists(self):
        response = requests.delete('{}{}/'.format(self.CEP_API_BASE_URL, '14820-001'))
        assert response.status_code == Http.NOT_FOUND

    def test_delete_alpha_zipcode(self):
        response = requests.delete('{}{}/'.format(self.CEP_API_BASE_URL, 'aaaaaaaaa'))
        assert response.status_code == Http.BAD_REQUEST

    def test_delete_different_len_zipcode(self):
        response = requests.delete('{}{}/'.format(self.CEP_API_BASE_URL, '1402-260'))
        assert response.status_code == Http.BAD_REQUEST


class TestGetResource(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.CEP_API_BASE_URL = 'http://localhost:5000/zipcode/'
        requests.post(cls.CEP_API_BASE_URL, data={'zip_code': '14810000'})

    @classmethod
    def tearDownClass(cls):
        ZipCode.objects.all().delete()

    def test_get_cleaned_zip_code(self):
        response = requests.get('{}{}/'.format(self.CEP_API_BASE_URL, '14810000'))
        assert response.status_code == Http.OK

    def test_get_mask_zipcode(self):
        response = requests.get('{}{}/'.format(self.CEP_API_BASE_URL, '14810-000'))
        assert response.status_code == Http.OK

    def test_get_zipcode_not_exists(self):
        response = requests.get('{}{}/'.format(self.CEP_API_BASE_URL, '14810001'))
        assert response.status_code == Http.NOT_FOUND

    def test_get_alpha_zipcode(self):
        response = requests.get('{}{}/'.format(self.CEP_API_BASE_URL, 'aaaaaaaaa'))
        assert response.status_code == Http.BAD_REQUEST

    def test_get_different_len_zipcode(self):
        response = requests.get('{}{}/'.format(self.CEP_API_BASE_URL, '1402-260'))
        assert response.status_code == Http.BAD_REQUEST


class TestGetListResource(object):

    @classmethod
    def setUp(cls):
        cls.CEP_API_BASE_URL = 'http://localhost:5000/zipcode/'
        for zipcode in [14810000, 14815000, 14820000]:
            requests.post(cls.CEP_API_BASE_URL, data={'zip_code': zipcode})

    @classmethod
    def tearDownClass(cls):
        ZipCode.objects.all().delete()

    def test_get_list_without_limit(self):
        response = requests.get(self.CEP_API_BASE_URL)
        zipcode_list = json.loads(response.content)
        assert response.status_code == Http.OK
        assert len(zipcode_list) == 3

    def test_get_list_exact_limit(self):
        response = requests.get('{}?limit={}'.format(self.CEP_API_BASE_URL, '3'))
        zipcode_list = json.loads(response.content)
        assert response.status_code == Http.OK
        assert len(zipcode_list) == 3

    def test_get_list_lower_limit(self):
        response = requests.get('{}?limit={}'.format(self.CEP_API_BASE_URL, '2'))
        zipcode_list = json.loads(response.content)
        assert response.status_code == Http.OK
        assert len(zipcode_list) == 2

    def test_get_list_ignore_higher_limit(self):
        response = requests.get('{}?limit={}'.format(self.CEP_API_BASE_URL, '5'))
        zipcode_list = json.loads(response.content)
        assert response.status_code == Http.OK
        assert len(zipcode_list) == 3

    def test_get_list_ignore_zero_limit(self):
        response = requests.get('{}?limit={}'.format(self.CEP_API_BASE_URL, '0'))
        zipcode_list = json.loads(response.content)
        assert response.status_code == Http.OK
        assert len(zipcode_list) == 3

    def test_get_list_negative_limit(self):
        response = requests.get('{}?limit={}'.format(self.CEP_API_BASE_URL, '-1'))
        assert response.status_code == Http.BAD_REQUEST

    def test_get_list_alpha_limit(self):
        response = requests.get('{}?limit={}'.format(self.CEP_API_BASE_URL, 'aaaaaaaaa'))
        assert response.status_code == Http.BAD_REQUEST