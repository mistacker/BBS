#coding:utf-8

from flask import session,url_for,redirect,abort,g,request
import constants
from functools import wraps
from models.cms_models import CMSUser,User_power
from utils import xt_json

# 登录装饰器
def login_required(func):
    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get(constants.USER_SESSION_ID):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return wapper

# 验证权限装饰器
def prove_power(is_power):
    def power_required(func):
        @wraps(func)
        def wapper(*args,**kwargs):
            if g.cms_user.has_power(is_power):
                return func(*args,**kwargs)
            elif request.is_xhr:
                return xt_json.json_unauth_error(u'你没有权限进行此项操作!')
            else:
                abort(401)
        return wapper
    return power_required

# 验证是否有超级管理员权限
def prove_power_super_admin(func):
    return prove_power(User_power.admin)(func)