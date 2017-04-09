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
    cms_user = db.relationship('CMSUser',backref='boards')         ###########

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

    board = db.relationship('BoardModel',backref='posts')          ##########
    # board = db.relationship('BoardModel',backref=db.backref('posts',lazy='dynamic'))          ##########
    # lazy 默认等于select 这样返回的是一个list对象，现改成dynamic 这回就返回一个query对象
    front_user = db.relationship('FrontUser',backref='posts')
    pick = db.relationship('Pick',backref='post',uselist=False)

# 精品表
class Pick(Base):
    __tablename__ = 'pick'
    id = db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime,default=datetime.now)

# 评论
class Comment(Base):
    __tablename__ = 'comment'
    id = db.Column(db.Integer,primary_key=True)
    comtent = db.Column(db.Text,nullable=False)
    create_time = db.Column(db.DateTime,default=datetime.now)
    is_live = db.Column(db.Boolean,default=True)

    front_user_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))
    origin_comment_id = db.Column(db.Integer,db.ForeignKey('comment.id'))

    front_user = db.relationship('FrontUser',backref='comments')
    post = db.relationship('Post',backref='comments')
    origin_comment = db.relationship('Comment',backref='comments',remote_side=[id])        ########

# 点赞
class Laud(Base):
    __tablename__ = 'laud'
    id = db.Column(db.Integer,primary_key=True)
    create_time = db.Column(db.DateTime,default=datetime.now)
    front_user_id = db.Column(db.String(100),db.ForeignKey('front_user.id'))
    post_id = db.Column(db.Integer,db.ForeignKey('post.id'))

    front_user = db.relationship('FrontUser',backref='lauds')
    post = db.relationship('Post',backref='lauds')          #########