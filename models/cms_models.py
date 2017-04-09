#coding:utf-8

from exts import db
from datetime import datetime
from werkzeug.security import check_password_hash,generate_password_hash


Base = db.Model

# 定义权限
class User_power(object):
    common = 1
    admin = 255
    desc_temp = {
        common:(u'普通管理员',u'拥有管理前台用户和帖子等权限'),
        admin:(u'超级管理员',u'拥有所有权限，可进行任何操作'),
    }

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
    create_time = db.Column(db.DateTime,default=datetime.now)
    cms_users = db.relationship('CMSUser',secondary=user_role_table)

# CMS用户表
class CMSUser(Base):
    __tablename__ = 'cms_user'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    username = db.Column(db.String(100),nullable=False)
    _password = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),nullable=False,unique=True)
    join_time = db.Column(db.DateTime,default=datetime.now)
    is_live = db.Column(db.Boolean,default=True)
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

    # 获取用户的所有权限
    def get_all_powers(self):
        if not self.cms_roles:
            return False
        all_powers = 0
        for role in self.cms_roles:
            all_powers = all_powers | role.power
        return all_powers

    # 判断用户是否有某个权限
    def has_power(self,is_power):
        all_powers = self.get_all_powers()
        # return all_power & is_power == is_power
        if (all_powers & is_power) == is_power:
            return True
        else:
            return False

    # 判断用户是否是super_admin
    @property
    def is_super_admin(self):
        rs = self.has_power(User_power.admin)
        return rs

    # 获取用户的所有权限和描述信息
    @property
    def get_all_power_info(self):
        all_powers = self.get_all_powers()
        power_dicts = {}
        if all_powers & User_power.admin == User_power.admin:
            power_dicts[User_power.admin] = User_power.desc_temp[User_power.admin]
            return power_dicts
        # for power,info in User_power.desc_temp.iteritems():
        #     if all_powers & power == power:
        #         power_dicts[power] = info
        for info in self.cms_roles:
            temp = []
            temp.append(info.name)
            temp.append(info.desc)
            power_dicts[info.power] = temp
        return power_dicts


    def __repr__(self):
        return '<User(id:%s,name:%s,pwd:%s,email:%s)>'%(self.id,self.username,self.password,self.email)