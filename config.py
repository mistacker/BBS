#coding:utf-8

import os
import top.api
from utils.xt_cache import create_num_captcha

USERNAME = 'root'
PASSWORD = '123456'
HOSTNAME = 'localhost'
POSR = '3306'
DATABASE = 'demo19_1'
charset = 'utf8'

DB_URI = 'mysql+mysqldb://%s:%s@%s:%s/%s?charset=%s'%(USERNAME,PASSWORD,HOSTNAME,POSR,DATABASE,charset)
SQLALCHEMY_DATABASE_URI = DB_URI

SQLALCHEMY_TRACK_MODIFICATIONS = False

SERVER_NAME = 'tz.com'

SECRET_KEY = os.urandom(24)

# 邮箱mail的参数
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL=True
MAIL_USERNAME = '2596279105@qq.com'
MAIL_PASSWORD = 'whsnqbuvrdymeacc'
MAIL_DEFAULT_SENDER = '2596279105@qq.com'

# 阿里大于参数 及方法封装
appkey = '23584025'
secret = 'de6149e7409f9085b5bb486656d1d5af'

# 获取手机验证码
def get_tel_captcha(tel):
    req = top.api.AlibabaAliqinFcSmsNumSendRequest()
    req.set_app_info(top.appinfo(appkey,secret))
    captcha = create_num_captcha(6,tel,5*60)
    req.extend = ""
    req.sms_type = "normal"
    req.sms_free_sign_name = "票务查询"
    req.sms_param = "{'code':'%s'}"%captcha
    print captcha,tel
    req.rec_num = tel.decode('utf-8').encode('ascii')
    req.sms_template_code = "SMS_57320071"
    try :
         resp = req.getResponse()
         print ('this is resp:',resp)
         return True
    except Exception,e:
         print ('this is error:',e)
         return False