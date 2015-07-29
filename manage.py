# -*- coding:utf-8 -*-

from flask.ext.script import Manager

from cep_api.app import app
from cep_api.models import ZipCode

manager = Manager(app)

@manager.command
def clear_db():
    ZipCode.objects.all().delete()


if __name__ == "__main__":
    manager.run()