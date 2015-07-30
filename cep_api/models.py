from mongoengine.document import Document
from mongoengine.fields import StringField


class ZipCode(Document):

    zip_code = StringField(max_length=50)
    address = StringField(max_length=100)
    neighborhood = StringField(max_length=100)
    state = StringField(max_length=50)
    city = StringField(max_length=50)

    @classmethod
    def save_zipcode(cls, zipcode_dict):
        zipcode = ZipCode(
            address=zipcode_dict.get('logradouro'),
            neighborhood=zipcode_dict.get('bairro'),
            city=zipcode_dict.get('cidade'),
            state=zipcode_dict.get('estado'),
            zip_code=zipcode_dict.get('cep'),
        ).save()

        return zipcode

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

        return zipcode_obj

    @classmethod
    def get_by_zipcode(cls, zipcode):
        zip_code_obj = cls.objects.get(zip_code=zipcode)
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
        return zip_code_obj

    @classmethod
    def list(cls, limit=None):

        if not limit:
            zip_code_list = cls.objects.order_by('-id')
            return zip_code_list

        limit = int(limit)
        zip_code_list = cls.objects.order_by('-id')

        if zip_code_list.count() > limit:
            zip_code_list = zip_code_list[:limit]

        return zip_code_list

    def __repr__(self):
        return '<ZipCode {}>'.format(self.zip_code)

    def __unicode__(self):
        return '<ZipCode {}>'.format(self.zip_code)