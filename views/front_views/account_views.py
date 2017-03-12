#coding:utf-8

from flask import Blueprint

bp = Blueprint('front_accent',__name__,url_prefix='/accent')

@bp.route('/front/')
def front():
    return 'user f'