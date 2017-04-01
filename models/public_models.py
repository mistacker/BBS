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

# 帖子表
class Post(Base):
    __tablename__ = 'post'
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),unique=True,nullable=False)
    content = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now())
    update_time = db.Column(db.DateTime,default=datetime.now(),onupdate=datetime.now())
    read_count = db.Column(db.Integer,default=0)
    is_live = db.Column(db.Boolean,default=True)

    board_id = db.Column(db.Integer,db.ForeignKey('board.id'))
    front_user_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    pick_id = db.Column(db.Integer,db.ForeignKey('pick.id'))

    board = db.relationship('BoardModel',backref='posts')
    front_user = db.relationship('FrontUser',backref='posts')
    pick = db.relationship('Pick',backref='post',uselist=False)

# 精品表
class Pick(Base):
    __tablename__ = 'pick'
    id = db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime,default=datetime.now())