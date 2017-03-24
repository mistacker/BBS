#coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,BooleanField
from wtforms.validators import Length,Regexp,InputRequired,EqualTo

class Form_error(FlaskForm):
    def get_error(self):
        k,v = self.errors.popitem()
        return v[0]

class Front_user_regist_form(Form_error):
    telephone = StringField(validators=[Regexp('^[1][358][0-9]{9}$',message=u'手机号码不符合规矩')])
    tel_captcha = StringField(validators=[Length(6,6,message=u'验证码位数不准确')])
    username = StringField(validators=[Length(min=6,message=u'用户名最短为6位')])
    password = StringField(validators=[Length(min=3,message=u'密码最短长度为3位')])
    password_re = StringField(validators=[EqualTo('password',message=u'确认密码必须和密码相等')])
    captcha = StringField(validators=[InputRequired(message=u'验证码不能为空')])

class Front_check_telephone(Form_error):
    telephone = StringField(validators=[Regexp('^[1][358][0-9]{9}$',message=u'手机号码不符合规矩')])

class Front_login_form(Form_error):
    telephone = StringField(validators=[Regexp('^[1][358][0-9]{9}$',message=u'手机号码不符合规矩')])
    password = StringField(validators=[InputRequired(message=u'密码不能为空')])
    captcha = StringField(validators=[InputRequired(message=u'验证码不能为空')])
    remember = BooleanField()