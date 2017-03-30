#coding:utf-8

from exts import db
import shortuuid
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash



Base = db.Model

# 性别
class GenderType(object):
    MAN = 1
    WOMAN = 2
    SECRET = 3

class FrontUser(Base):
    __tablename__ = 'front_user'
    id = db.Column(db.String(100),primary_key=True,default=shortuuid.uuid())
    username = db.Column(db.String(100),nullable=False,unique=True)
    _password = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(11),nullable=False)
    email = db.Column(db.String(100))
    create_time = db.Column(db.DateTime,default=datetime.now())
    is_live = db.Column(db.Boolean,default=True)
    lask_login_time = db.Column(db.DateTime)
    qq = db.Column(db.String(15))
    relname = db.Column(db.String(20))
    gender = db.Column(db.Integer,default=GenderType.SECRET)
    signature = db.Column(db.String(100))
    bbs_points = db.Column(db.Integer,default=0)

    def __init__(self,username,password,telephone):
        self.username = username
        self.password = password
        self.telephone = telephone

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,rawpwd):
        self._password = generate_password_hash(rawpwd)

    def check_pwd(self,rawpwd):
        return check_password_hash(self.password,rawpwd)
