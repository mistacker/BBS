#coding:utf-8

from flask import session,url_for,redirect
import constants
from functools import wraps

def login_required(func):

    @wraps(func)
    def wapper(*args,**kwargs):
        if session.get(constants.USER_SESSION_ID):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('cms.login'))
    return wapper