#coding:utf-8

from flask import Blueprint
import flask
from my_decorator import front_login_required

bp = Blueprint('front_post',__name__)

# 首页
@bp.route('/')
@front_login_required
def index():
    return flask.render_template('front/front_index.html')