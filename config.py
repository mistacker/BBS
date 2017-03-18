#coding:utf-8

import os

USERNAME = 'root'
PASSWORD = '123456'
HOSTNAME = 'localhost'
POSR = '3306'
DATABASE = 'demo19_1'
charset = 'utf8'

DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s'%(USERNAME,PASSWORD,HOSTNAME,POSR,DATABASE,charset)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = 'tz.com'

SECRET_KEY = os.urandom(24)

# 邮箱mail的参数
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL=True
MAIL_USERNAME = '2596279105@qq.com'
MAIL_PASSWORD = 'whsnqbuvrdymeacc'
MAIL_DEFAULT_SENDER = '2596279105@qq.com'