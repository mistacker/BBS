#coding:utf-8

from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash


Base = db.Model

# 定义权限
class User_power(object):
    common = 1
    admin = 255

# 中间表
user_role_table = db.Table('cms_user_role',Base.metadata,
            db.Column('cms_role_id',db.Integer,db.ForeignKey('cms_role.id'),primary_key=True),
            db.Column('cms_user_id',db.Integer,db.ForeignKey('cms_user.id'),primary_key=True),
            )

# CMS用户权限组
class CMSRole(Base):
    __tablename__ = 'cms_role'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    desc = db.Column(db.String(100))
    power = db.Column(db.Integer,default=User_power.common)
    create_time = db.Column(db.DateTime,default=datetime.now())
    cms_users = db.relationship('CMSUser',secondary=user_role_table)

# CMS用户表
class CMSUser(Base):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now())
    cms_roles = db.relationship('CMSRole',secondary=user_role_table)

    def __init__(self,username,password,email):
        self.username = username
        self.password = password
        self.email = email

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_pwd(self,rawpwd):
        rs = check_password_hash(self.password,rawpwd)
        return rs

    def __repr__(self):
        return '<User(id:%s,name:%s,pwd:%s,email:%s)>'%(self.id,self.username,self.password,self.email)