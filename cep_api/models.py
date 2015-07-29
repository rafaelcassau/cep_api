from mongoengine.document import Document
from mongoengine.fields import StringField
from .app import app


class ZipCode(Document):

    zip_code = StringField(max_length=50)
    address = StringField(max_length=100)
    neighborhood = StringField(max_length=100)
    state = StringField(max_length=50)
    city = StringField(max_length=50)

    @classmethod
    def save_zipcode(cls, zipcode_dict):
        zip_code = ZipCode(
            address=zipcode_dict.get('logradouro'),
            neighborhood=zipcode_dict.get('bairro'),
            city=zipcode_dict.get('cidade'),
            state=zipcode_dict.get('estado'),
            zip_code=zipcode_dict.get('cep'),
        )
        zip_code.save()

        app.logger.info('Add zipcode {} on database'.format(zip_code))

    @classmethod
    def update_zipcode(cls, zipcode_dict):

        # Object always exists on database
        zipcode_obj = cls.get_by_zipcode(zipcode_dict.get('cep'))

        zipcode_obj.address = zipcode_dict.get('logradouro')
        zipcode_obj.neighborhood = zipcode_dict.get('bairro')
        zipcode_obj.city = zipcode_dict.get('cidade')
        zipcode_obj.state = zipcode_dict.get('estado')
        zipcode_obj.zip_code = zipcode_dict.get('cep')

        zipcode_obj.save()

        app.logger.info('Update zipcode {} on database'.format(zipcode_obj))

    @classmethod
    def get_by_zipcode(cls, zipcode):
        zip_code_obj = cls.objects.get(zip_code=zipcode)

        app.logger.info('Get zipcode {}'.format(zip_code_obj))

        return zip_code_obj

    @classmethod
    def zipcode_exists(cls, zipcode):
        zip_code_obj = cls.objects.filter(zip_code=zipcode).first()
        exist = True if zip_code_obj else False
        return exist

    @classmethod
    def remove_by_zipcode(cls, zipcode):
        zip_code_obj = cls.objects.get(zip_code=zipcode)
        zip_code_obj.delete()

        app.logger.info('Remove zipcode {}'.format(zip_code_obj))

    @classmethod
    def list(cls, limit=None):

        if not limit:
            zip_code_list = cls.objects.order_by('-id')
            return zip_code_list

        limit = int(limit)
        zip_code_list = cls.objects.order_by('-id')

        if zip_code_list.count() > limit:
            zip_code_list = zip_code_list[:limit]

        app.logger.info('List zipcodes {}'.format(zip_code_list))

        return zip_code_list

    def __repr__(self):
        return '<ZipCode {}>'.format(self.zip_code)

    def __unicode__(self):
        return '<ZipCode {}>'.format(self.zip_code)