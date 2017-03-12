#coding:utf-8

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