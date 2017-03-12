#coding:utf-8

from exts import db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from models import cms_models,font_models,public_models
from demo19_1 import app

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)


if __name__ == '__main__':
    manager.run()