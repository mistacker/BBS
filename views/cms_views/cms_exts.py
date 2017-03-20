#coding:utf-8

from flask import Blueprint
import flask
from flask.views import MethodView
from forms.cms_forms import CMS_user_login_form,Set_pwd_form,check_email_form,Set_email_form,Add_manager_form,Add_group_form
from models.cms_models import db,CMSUser,CMSRole
from constants import USER_SESSION_ID
from my_decorator import login_required
from utils import xt_json
from utils.xt_mail import send_mail
from utils import xt_cache


bp = Blueprint('cms',__name__,subdomain='cms')


# CMS用户登录
class Login(MethodView):

    def get(self,message=''):
        return flask.render_template('cms/login.html',message=message)

    def post(self):
        form = CMS_user_login_form(flask.request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            rember = form.rember.data
            # print email
            user = CMSUser.query.filter_by(email=email).first()
            if user and user.check_pwd(password):
                flask.session[USER_SESSION_ID] = email
                if rember:
                    flask.session.permanent = True
                else:
                    flask.session.permanent = False
                return flask.redirect(flask.url_for('cms.index'))
            else:
                return self.get(message=u'用户名或密码不正确!')
        else:
            return self.get(message=form.get_error())


bp.add_url_rule('/login/',view_func=Login.as_view('login'))

# CMS用户首页
@bp.route('/')
@login_required
def index():
    return flask.render_template('cms/cms_index.html')


@bp.route('/account/')
def account():
    return 'this is account page'

# CMS用户推出登录
@bp.route('/logout/')
def logout():
    email = flask.session.pop(USER_SESSION_ID)
    return flask.redirect(flask.url_for('cms.login'))

# 个人中心

# 个人信息
@bp.route('/profile/')
@login_required
def profile():
    return flask.render_template('cms/profile.html')

# 修改密码
@bp.route('/resetpwd/',methods=['POST','GET'])
@login_required
def resetpwd():
    if flask.request.method == 'GET':
        return flask.render_template('cms/resetpwd.html',message='')
    else:
        form = Set_pwd_form(flask.request.form)
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            if flask.g.cms_user.check_pwd(oldpwd):
                flask.g.cms_user.password = newpwd
                db.session.commit()
                return xt_json.json_result(message='success')
            else:
                return xt_json.json_params_error(message=u'原始密码不正确!')
        else:
            return xt_json.json_params_error(message=u'数据填写有误!')

# 修改邮箱
@bp.route('/resetemail/',methods=['GET','POST'])
@login_required
def resetemail():
    if flask.request.method == 'GET':
        return flask.render_template('cms/resetemail.html')
    else:
        form = Set_email_form(flask.request.form)
        if form.validate():
            newemail = form.newemail.data
            captcha = form.captcha.data
            server_captcha = xt_cache.get(newemail)
            if server_captcha and xt_cache.check_captcha(newemail,captcha):
                flask.g.cms_user.email = newemail
                db.session.commit()
                return xt_json.json_result_ok('恭喜，修改成功!')
            else:
                return xt_json.json_params_error('对不起，验证码不正确!')
        else:
            return xt_json.json_params_error('对不起，格式有误!')

# 发送邮箱验证码
@bp.route('/send_captcha/',methods=['POST'])
def send_email_captcha():
    form = check_email_form(flask.request.form)
    if flask.request.is_xhr and form.validate():
        newemail = form.newemail.data
        email = flask.session.get(USER_SESSION_ID)
        if newemail == email:
            return xt_json.json_params_error('新邮箱和原始邮箱一致!')
        if xt_cache.get(newemail):
            return xt_json.json_params_error('已经发送验证码，3分钟内不能重复提交!')
        user = CMSUser.query.filter_by(email=newemail).first()
        if user:
            return xt_json.json_params_error('对不起该邮箱已存在!')
        captcha = xt_cache.set_captcha(6,newemail,3*60)
        if captcha:
            send_mail('潭州论坛-邮箱验证码',newemail,body='您正在修改潭州论坛CMS用户的邮箱，您的验证码是：'+captcha)
            return xt_json.json_result_ok('发送验证码成功!')
        else:
            return xt_json.json_server_error('服务器错误!')
    else:
        return xt_json.json_params_error(form.get_error())

# CMS用户管理界面
@bp.route('/cms_user_manager/')
@login_required
def cms_user_manager():
    cms_users = CMSUser.query.all()
    return flask.render_template('cms/cms_user_manager.html',cms_users=cms_users)

# 添加管理员界面
@bp.route('/add_manager/',methods=['POST','GET'])
@login_required
def add_manager():
    if flask.request.method == 'GET':
        cms_roles = CMSRole.query.all()
        return flask.render_template('cms/add_manager.html',cms_roles=cms_roles)
    else:
        form = Add_manager_form(flask.request.form)
        if form.validate():
            username = form.username.data
            password = form.password.data
            email = form.email.data
            web_check = flask.request.form.getlist('web_check[]')
            cms_user = CMSUser.query.filter_by(username=username).first()
            if cms_user:
                return xt_json.json_params_error('对不起 该用户名已存在!')
            cms_user = CMSUser.query.filter_by(email=email).first()
            if cms_user:
                return xt_json.json_params_error('对不起 该邮箱已存在!')
            cms_user = CMSUser(username=username,password=password,email=email)
            if web_check:
                cms_roles = []
                for check in web_check:
                    cms_role = CMSRole.query.get(check)
                    cms_roles.append(cms_role)
                cms_user.cms_roles = cms_roles
                db.session.add(cms_user)
                db.session.commit()
            else:
                return xt_json.json_params_error('对不起 必须指定所属分组!')
            return xt_json.json_result_ok('恭喜 添加CMS用户成功!')
        else:
            return xt_json.json_params_error(form.get_error())

# cms组管理界面
@bp.route('/cms_group/')
@login_required
def cms_group():
    all_groups = CMSRole.query.all()
    return flask.render_template('cms/cms_group.html',all_groups=all_groups)

# cms添加管理组界面
@bp.route('/add_group/',methods=['GET','POST'])
@login_required
def add_group():
    if flask.request.method == 'GET':
        return flask.render_template('cms/add_group.html')
    else:
        form = Add_group_form(flask.request.form)
        if form.validate():
            name = form.name.data
            desc = form.desc.data
            all_count = CMSRole.query.count()
            power = pow(2,all_count-1)
            if power>255:
                return xt_json.json_server_error('对不起 内部错误!')
            cms_role = CMSRole.query.filter_by(name=name).first()
            if cms_role:
                return xt_json.json_params_error('对不起，该组名已存在!')
            new_cms_role = CMSRole(name=name,desc=desc,power=power)
            db.session.add(new_cms_role)
            db.session.commit()
            return xt_json.json_result_ok('恭喜，添加该组管理成功!')
        else:
            return xt_json.json_params_error(form.get_error())


@bp.context_processor
def cms_context_processor():
    email = flask.session.get(USER_SESSION_ID)
    if email:
        user = CMSUser.query.filter_by(email=email).first()
        return {'user':user}
    else:
        return {}

# 定义钩子函数，在requeset之前执行 获取当前登录的cms_user,并绑定给flask.g 然后方便在视图函数进行调用获取其中绑定的cms_user
@bp.before_request
def cms_befor_request():
    email = flask.session.get(USER_SESSION_ID)
    if email:
        user = CMSUser.query.filter_by(email=email).first()
        flask.g.cms_user = user