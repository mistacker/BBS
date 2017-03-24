#coding:utf-8

from flask import Blueprint
from flask import views
import flask
from utils.xt_img_captcha import Captcha
from constants import CAPTCHA
from utils import xt_cache,xt_json
from config import get_tel_captcha
from forms import front_forms
from models import front_models
from exts import db
try:
    from StringIO import StringIO
except:
    from io import BytesIO as StringIO

bp = Blueprint('front_accent',__name__,url_prefix='/accent')

@bp.route('/index/')
def index():
    return flask.render_template('front/front_index.html')

# 注册
class RegisteUser(views.MethodView):

    def get(self):
        return flask.render_template('front/front_regist.html')

    def post(self):
        form = front_forms.Front_user_regist_form(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            tel_captcha = form.tel_captcha.data
            username = form.username.data
            password = form.password.data
            captcha = form.captcha.data
            front_user = front_models.FrontUser.query.filter_by(username=username).first()
            if front_user:
                temp = {
                    'result' : u'对不起 该用户名已存在!',
                    'content' : u'<a href={{url_for("account.regist")}}>重新注册</a>'
                }
                return flask.render_template('front/result.html',**temp)
            if not xt_cache.get(telephone) or xt_cache.get(telephone) != tel_captcha:
                temp = {
                    'result' : u'对不起 手机验证码不正确!',
                    'content' : u'<a href={{url_for("account.regist")}}>重新注册</a>'
                }
                return flask.render_template('front/result.html',**temp)
            if not xt_cache.get(CAPTCHA) or not xt_cache.check_captcha(CAPTCHA,captcha):
                temp = {
                    'result' : u'对不起 网页验证码不正确!',
                    'content' : u'<a href={{url_for("account.regist")}}>重新注册</a>'
                }
                return flask.render_template('front/result.html',**temp)
            front_user = front_models.FrontUser(username=username,password=password,telephone=telephone)
            db.session.add(front_user)
            db.session.commit()
            temp = {
                'result' : u'恭喜 注册成功！',
                'content' : u'<a href={{url_for("account.login")}}>前去登录</a>'
            }
            return flask.render_template('front/result.html',**temp)
        else:
            temp = {
                'result' : form.get_error(),
                'content' : u'<a href={{url_for("account.regist")}}>重新注册</a>'
            }
            return flask.render_template('front/result.html',**temp)

bp.add_url_rule('/regist/',view_func=RegisteUser.as_view('regist'))

# 登录
class LoginUser(views.MethodView):

    def get(self):
        return flask.render_template('front/front_login.html')

    def post(self):
        form = front_forms.Front_login_form(flask.request.form)
        if form.validate():
            telephone = form.telephone.data
            password = form.password.data
            captcha = form.captcha.data
            remember = form.remember.data
            if not xt_cache.get(CAPTCHA) or not xt_cache.check_captcha(CAPTCHA,captcha):
                temp = {
                    'result': u'验证码不正确重新登陆',
                    'content': u'<a href={{url_for("account.login")}}>重新登录</a>'
                }
                return flask.render_template('front/result.html',**temp)
            front_user = front_models.FrontUser.query.filter_by(telephone=telephone).first()
            if front_user and front_user.check_pwd(password):
                if remember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('front_accent.index'))
            else:
                temp = {
                    'result': u'当前用户不存在',
                    'content': u'<a href={{url_for("account.login")}}>重新登录</a>'
                }
                return flask.render_template('front/result.html', **temp)
        else:
            temp = {
                'result': form.get_error(),
                'content': u'<a href={{url_for("account.login")}}>重新登录</a>'
            }
            return flask.render_template('front/result.html', **temp)

bp.add_url_rule('/login/',view_func=LoginUser.as_view('login'))


@bp.route('/get_yzm/')
def get_yzm():
    captcha = Captcha()
    text,img = captcha.gene_code()
    xt_cache.set(CAPTCHA,text,3*60)
    # StringIO相当于是一个管道
    out = StringIO()
    # 把image塞到StringIO这个管道中
    img.save(out,'png')
    # 将StringIO的指针只想开始的地方
    out.seek(0)

    # 生成一个响应对象，out.read是把图片流给读出来
    response = flask.make_response(out.read())
    # 指定相应的类型
    response.content_type = 'image/png'
    return response

@bp.route('/tel/',methods=['POST'])
def tel():
    form = front_forms.Front_check_telephone(flask.request.form)
    if form.validate():
        try:
            tel = form.telephone.data
            front_user = front_models.FrontUser.query.filter_by(telephone=tel).first()
            if front_user:
                return xt_json.json_params_error('对不起 该号码已存在!')
            if get_tel_captcha(tel):
                return xt_json.json_result_ok('发送验证码成功!')
            else:
                return xt_json.json_params_error('服务器忙，请稍后注册!')
        except:
            return xt_json.json_params_error('内部错误!')
    else:
        return xt_json.json_params_error(form.get_error())