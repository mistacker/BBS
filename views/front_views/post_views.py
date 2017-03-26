#coding:utf-8

from flask import Blueprint
import flask
from my_decorator import front_login_required
from constants import FRONT_USER_TEL
from models import front_models,public_models

bp = Blueprint('front_post',__name__)

# 首页
@bp.route('/')
def index():
    boards = public_models.BoardModel.query.filter_by(is_live=True).all()
    return flask.render_template('front/front_index.html',boards=boards)

# 发表新帖子
@bp.route('/add_post/',methods=['GET','POST'])
@front_login_required
def add_post():
    if flask.request.method == 'GET':
        boards = public_models.BoardModel.query.filter_by(is_live=True).all()
        return flask.render_template('front/add_post.html',boards=boards)

# 定义钩子函数用来保存当前登录的用户
@bp.before_request
def my_front_before_request():
    telephone = flask.session.get(FRONT_USER_TEL)
    if telephone:
        front_user = front_models.FrontUser.query.filter_by(telephone=telephone,is_live=True).first()
        if front_user:
            flask.g.front_user = front_user

# 向模板中传递登录用户
@bp.context_processor
def front_context_processor():
    front_tel = flask.session.get(FRONT_USER_TEL)
    if front_tel:
        front_user = flask.g.front_user
        return {'front_user':front_user}
    else:
        return {}