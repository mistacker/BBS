#coding:utf-8

from exts import db
from datetime import datetime

Base = db.Model

# 板块模块
class BoardModel(Base):
    __tablename__ = 'board'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    is_live = db.Column(db.Boolean,default=True)
    cms_user_id = db.Column(db.Integer,db.ForeignKey('cms_user.id'))
    cms_user = db.relationship('CMSUser',backref='boards')

