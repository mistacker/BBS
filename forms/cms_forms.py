#coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,BooleanField
from wtforms.validators import InputRequired,Email,ValidationError,Length,EqualTo
from models.cms_models import CMSUser

class FormError(FlaskForm):
    def get_error(self):
        key,value = self.errors.popitem()
        return value[0]

# CMS用户登录
class CMS_user_login_form(FormError):
    email = StringField(validators=[Email(message=u'邮箱格式不正确!')])
    password = StringField(validators=[Length(min=6,message=u'密码最短为6个字符!')])
    rember = BooleanField()

# 修改密码
class Set_pwd_form(FormError):
    oldpwd = StringField(validators=[Length(min=6,message=u'原密码不得少于6位!')])
    newpwd = StringField(validators=[Length(min=6,message=u'新密码不得少于6位!')])
    re_newpwd = StringField(validators=[EqualTo('newpwd',message=u'确认密码必须和新密码相等!')])

# 修改邮箱
class Set_email_form(FormError):
    newemail = StringField(validators=[Email(message=u'邮箱地址不符合规则!')])
    captcha = StringField(validators=[InputRequired(message=u'验证码不能为空!')])

# 检查邮箱
class check_email_form(FormError):
    newemail = StringField(validators=[Email(message=u'邮箱地址不符合规则!')])