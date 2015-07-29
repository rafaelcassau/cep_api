# -*- coding:utf-8 -*-


class ZipCodeValidator(object):

    def __init__(self, zipcode):
        self.zipcode = zipcode
        self.ZIPCODE_MAX_LENGTH = 8
        self.cleaned_data = {}
        self.invalid_data = {}

    def is_valid(self):

        zipcode = self.zipcode.strip().replace('-', '')

        if len(zipcode) != self.ZIPCODE_MAX_LENGTH or zipcode.isalpha():
            self.invalid_data['zipcode'] = zipcode
            return False

        self.cleaned_data['zipcode'] = zipcode
        return True


class LimitValidator(object):

    def __init__(self, limit):
        self.limit = limit
        self.cleaned_data = {}
        self.invalid_data = {}

    def is_valid(self):

        limit = self.limit

        if limit and limit.isalpha() or limit and int(limit) < 0:
            self.invalid_data['limit'] = limit
            return False

        self.cleaned_data['limit'] = int(limit) if limit else None
        return True
