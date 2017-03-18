#coding:utf-8

from flask import jsonify


# Http状态码
ok = 200
paramserror = 400
unauth = 401
methoderror = 405
servererror = 500

# 正常访问
def json_result(code,message='',data={},kwargs={}):

    json = {'code':code,'message':message,'data':data}
    if kwargs.keys():
        for k,v in kwargs.iteritems():
            json[k] = v
    return jsonify(json)

def json_result_ok(message='',data={},kwargs={}):
    return json_result(ok,message,data,kwargs)

def json_params_error(message=''):
    """
    :param message: 请求参数错误
    :return:
    """
    return json_result(code=paramserror,message=message)

def json_unauth_error(message=''):
    """
    :param message:没权限访问
    :return:
    """
    return json_result(code=unauth,message=message)

def json_method_error(message=''):
    """
    :param message: 访问方法错误
    :return:
    """
    return json_result(code=methoderror,message=message)

def json_server_error(message=''):
    """
    :param message:服务器错误
    :return:
    """
    return json_result(code=servererror,message=message)