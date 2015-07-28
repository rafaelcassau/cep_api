from mongoengine.document import Document
from mongoengine.fields import StringField


class ZipCode(Document):

    zip_code = StringField(max_length=50)
    adress = StringField(max_length=100)
    neighborhood = StringField(max_length=100)
    state = StringField(max_length=50)
    city = StringField(max_length=50)

    @classmethod
    def save_zipcode(cls, zip_code_dict):

        zip_code = ZipCode(
            adress=zip_code_dict.get('logradouro'),
            neighborhood=zip_code_dict.get('bairro'),
            city=zip_code_dict.get('cidade'),
            state=zip_code_dict.get('estado'),
            zip_code=zip_code_dict.get('cep'),
        )
        zip_code.save()

    def __repr__(self):
        return '<ZipCode {}>'.format(self.zip_code)