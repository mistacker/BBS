#coding:utf-8

from flask import Blueprint

bp = Blueprint('cms',__name__,subdomain='cms')

# @bp.route('/')
# def index():
#     return 'this is cms_index page'
#
# @bp.route('/account/')
# def account():
#     return 'this is account page'