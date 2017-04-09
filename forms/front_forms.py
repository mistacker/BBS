#coding:utf-8

from flask_wtf import FlaskForm
from wtforms import StringField,IntegerField,BooleanField
from wtforms.validators import Length,Regexp,InputRequired,EqualTo,ValidationError
from utils.xt_cache import check_captcha
from constants import CAPTCHA

class Form_error(FlaskForm):
    def get_error(self):
        k,v = self.errors.popitem()
        return v[0]

class Form_img_captcha(Form_error):
    captcha = StringField(validators=[InputRequired(message=u'验证码不能为空')])

    def validate_captcha(self, field):
        captcha = field.data
        captcha = str(captcha)
        if check_captcha(CAPTCHA, captcha):
            return True
        else:
            raise ValidationError(message=u'验证码过期或者输入不正确!')

class Front_user_regist_form(Form_img_captcha):
    telephone = StringField(validators=[Regexp('^[1][358][0-9]{9}$',message=u'手机号码不符合规矩')])
    tel_captcha = StringField(validators=[Length(6,6,message=u'验证码位数不准确')])
    username = StringField(validators=[Length(min=6,message=u'用户名最短为6位')])
    password = StringField(validators=[Length(min=3,message=u'密码最短长度为3位')])
    password_re = StringField(validators=[EqualTo('password',message=u'确认密码必须和密码相等')])

class Front_check_telephone(Form_error):
    telephone = StringField(validators=[Regexp('^[1][358][0-9]{9}$',message=u'手机号码不符合规矩')])

class Front_login_form(Form_img_captcha):
    telephone = StringField(validators=[Regexp('^[1][358][0-9]{9}$',message=u'手机号码不符合规矩')])
    password = StringField(validators=[InputRequired(message=u'密码不能为空')])
    remember = BooleanField()

class Front_add_post_form(Form_img_captcha):
    title = StringField(validators=[Length(min=3,max=100,message=u'标题字数在3到100个数之间')])
    board_id = IntegerField(validators=[InputRequired()])
    content = StringField(validators=[InputRequired(u'内容不能为空')])

class Front_comment_form(Form_error):
    id = IntegerField(validators=[InputRequired(message=u'帖子id不能为空')])
    content = StringField(validators=[InputRequired(message=u'评论内容不能为空')])

class Front_second_comment_form(Front_comment_form):
    comment_id = IntegerField(validators=[InputRequired(message=u'评论的id不能为空')])

class Front_laud_form(Form_error):
    post_id = IntegerField(validators=[InputRequired(message=u'帖子id不能为空')])

class Front_setting_form(Form_error):
    username = StringField(validators=[InputRequired(message=u'用户名不能为空')])
    relname = StringField()
    # qq = StringField(validators=[Regexp('^[1-9]\\d(4,10)$',message=u'qq号格式不正确')])
    gender = IntegerField(validators=[InputRequired(message=u'性别不能为空')])
    qq = StringField()
    avatar = StringField()
    signature = StringField()