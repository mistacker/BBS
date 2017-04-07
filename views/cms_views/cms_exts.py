#coding:utf-8

from flask import Blueprint
import flask
from flask.views import MethodView
from forms.cms_forms import CMS_user_login_form,Set_pwd_form,check_email_form,Set_email_form,Add_manager_form,Add_group_form
from models.cms_models import db,CMSUser,CMSRole
from models.front_models import FrontUser
from models.public_models import BoardModel,Post,Pick,Comment
from constants import USER_SESSION_ID
from my_decorator import login_required,prove_power_super_admin
from utils import xt_json,xt_fy
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
            if not user.is_live:
                return self.get(message=u'sorry 该用户已被禁用，请联系管理员!')
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
                return xt_json.json_result_ok(message='success')
            else:
                return xt_json.json_params_error(message=u'原始密码不正确!')
        else:
            return xt_json.json_params_error(form.get_error())

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
            return xt_json.json_params_error(form.get_error())

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

# 帖子管理
@bp.route('/cms_posts/')
@login_required
def cms_posts():
    return cms_posts_page(1)

@bp.route('/cms_posts/<int:page>')
@login_required
def cms_posts_page(page):
    # 1. 按时间
    # 2. 按精品
    # 3. 按阅读量
    tablename = Post
    board_id = flask.request.args.get('board_id')
    sort_id = flask.request.args.get('sort')
    start_post, end_post, end_page, web_page = xt_fy.paging(8, tablename,board_id, page)
    posts = ''
    if not sort_id and not board_id:
        posts = Post.query.filter_by(is_live=True).slice(start_post,end_post)
        boards = BoardModel.query.filter_by(is_live=True).all()
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.cms_posts_page',
            'posts':posts,
            'boards':boards
        }
        return flask.render_template('cms/cms_posts.html', **content)
    elif sort_id == '1':
        if board_id == '0' or not board_id:
            posts = Post.query.order_by(Post.create_time).filter_by(is_live=True).slice(start_post,end_post)
        else:
            posts = Post.query.order_by(Post.create_time).filter_by(is_live=True,board_id=board_id).slice(start_post,end_post)
    elif sort_id == '2':
        if board_id == '0' or not board_id:
            posts = db.session.query(Post).outerjoin(Pick).filter(Post.is_live==True).order_by(Pick.create_time.desc(),Post.create_time.desc()).slice(start_post,end_post)
        else:
            posts = db.session.query(Post).outerjoin(Pick).filter(Post.is_live==True,Post.board_id==board_id).order_by(Pick.create_time.desc(),Post.create_time.desc()).slice(start_post,end_post)
    elif sort_id == '3':
        if board_id == '0' or not board_id:
            posts = Post.query.order_by(Post.create_time.desc()).filter_by(is_live=True).slice(start_post,end_post)
        else:
            posts = Post.query.order_by(Post.create_time.desc()).filter_by(is_live=True, board_id=board_id).slice(start_post, end_post)
    else:
        if board_id != '0' and board_id:
            posts = Post.query.order_by(Post.create_time).filter_by(is_live=True, board_id=board_id).slice(start_post,end_post)
    boards = BoardModel.query.filter_by(is_live=True).all()
    content = {
        'end_page': end_page,
        'web_pages': web_page,
        'page': page,
        'url': 'cms.cms_posts_page',
        'posts': posts,
        'boards': boards,
        'sort':sort_id,
        'board_id':board_id
    }
    return flask.render_template('cms/cms_posts.html', **content)


# 帖子操作：加精和移除
@bp.route('/cms_post_operate/',methods=['GET','POST'])
def cms_post_operate():
    if flask.request.method == 'GET':
        post_id = flask.request.args.get('id')
        if not post_id:
            return xt_json.json_params_error('数据错误!')
        post = Post.query.get(post_id)
        post.is_live = False
        db.session.commit()
        return xt_json.json_result_ok('移除成功!')
    else:
        post_id = flask.request.form.get('id')
        if not post_id:
            return xt_json.json_params_error('数据错误!')
        post = Post.query.get(post_id)
        if post.pick:
            db.session.delete(post.pick)
            db.session.commit()
            return xt_json.json_result_ok('取消加精成功!')
        else:
            pick = Pick()
            post.pick = pick
            db.session.commit()
            return xt_json.json_result_ok('加精成功!')

# 评论管理
@bp.route('/comment_manage/')
@login_required
def comment_manage():
    return comment_manage_page(1)

@bp.route('/comment_manage/<int:page>',methods=['GET'])
@login_required
def comment_manage_page(page):
    sort = flask.request.args.get('sort')
    if not sort or sort == '1':
        start_post, end_post, end_page, web_page = xt_fy.paging(8,FrontUser,None,page)
        front_users = FrontUser.query.slice(start_post,end_post)
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.comment_manage_page',
            'front_users':front_users,
            'sort':'1',
            'temp':1
        }
        return flask.render_template('cms/comment_manage.html',**content)
    elif sort == '2':
        start_post, end_post, end_page, web_page = xt_fy.paging(8, Post, None, page)
        posts = Post.query.slice(start_post,end_post)
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.comment_manage_page',
            'posts':posts,
            'sort':'2',
            'temp':2
        }
        return flask.render_template('cms/comment_manage.html',**content)

# 评论操作管理
@bp.route('/comment_manage_opt/',methods=['GET','POST'])
def comment_manage_opt():
    if flask.request.method == 'GET':
        try:
            comment_id = flask.request.args.get('id')
            comment = Comment.query.get(comment_id)
            db.session.delete(comment)
            db.session.commit()
            return xt_json.json_result_ok('删除成功!')
        except Exception as e:
            print e
            return xt_json.json_params_error('内部错误!')
    else:
        try:
            comment_id = flask.request.form.get('id')
            comment = Comment.query.get(comment_id)
            if comment.is_live:
                comment.is_live = False
            else:
                comment.is_live = True
            db.session.commit()
            return xt_json.json_result_ok('修改成功!')
        except Exception as e:
            print e
            return xt_json.json_params_error('内部错误!')

# CMS用户管理界面
@bp.route('/cms_user_manager/')
@login_required
@prove_power_super_admin
def cms_user_manager():
    return cms_user_manager_page(1)

@bp.route('/cms_user_manager/<int:page>')
@login_required
@prove_power_super_admin
def cms_user_manager_page(page):
    cms_user = flask.g.cms_user
    tablename = CMSUser
    start_post, end_post, end_page, web_page = xt_fy.paging(5, tablename,None, page)
    cms_users = CMSUser.query[start_post:end_post]
    content = {
        'end_page': end_page,
        'web_pages': web_page,
        'page': page,
        'url': 'cms.cms_user_manager_page',
        'cms_users': cms_users,
        'cmsUser': cms_user
    }
    return flask.render_template('cms/cms_user_manager.html',**content)

# 添加管理员界面
@bp.route('/add_manager/',methods=['POST','GET'])
@login_required
@prove_power_super_admin
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
@prove_power_super_admin
@login_required
def cms_group():
    all_groups = CMSRole.query.all()
    return flask.render_template('cms/cms_group.html',all_groups=all_groups)

# cms添加管理组界面
@bp.route('/add_group/',methods=['GET','POST'])
@login_required
@prove_power_super_admin
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
            return xt_json.json_result_ok('恭喜，添加该管理组成功!')
        else:
            return xt_json.json_params_error(form.get_error())

# 编辑cms用户界面
@bp.route('/edit_cms_user/<id>')
@login_required
@prove_power_super_admin
def edit_cms_user(id):
    cms_user = CMSUser.query.get(id)
    cms_roles = CMSRole.query.all()
    roles = []
    for cms_role in cms_user.cms_roles:
        roles.append(cms_role.id)
    if cms_user:
        content = {
            'cms_user':cms_user,
            'cms_roles':cms_roles,
            'roles':roles
        }
        return flask.render_template('cms/edit_cms_user.html',**content)
    else:
        return flask.abort(404)

# 提交编辑cms用户界面
@bp.route('/add_edit_cms_user/',methods=['GET','POST'])
@login_required
@prove_power_super_admin
def add_edit_cms_user():
    if flask.request.is_xhr and flask.request.method == 'GET':
        id = flask.request.args.get('id')
        cms_user = CMSUser.query.get(id)
        if not cms_user.is_live:
            cms_user.is_live = True
            db.session.commit()
            return xt_json.json_result_ok('恭喜，解禁成功!')
        else:
            cms_user.is_live = False
            db.session.commit()
            return xt_json.json_result_ok('恭喜，禁用成功!')
    else:
        web_roles = flask.request.form.getlist('web_roles[]')
        id = flask.request.form.get('id')
        if not web_roles:
            return xt_json.json_params_error('对不起，必须指定分组!')
        cms_user = CMSUser.query.get(id)
        roles = []
        for web_role in web_roles:
            roles.append(CMSRole.query.get(web_role))
        cms_user.cms_roles = roles
        db.session.commit()
        return xt_json.json_result_ok('恭喜 修改成功!')

# 前台用户管理界面
@bp.route('/front_user_manage/')
@login_required
def front_user_manage():
    return front_user_manage_page(1)

@bp.route('/front_user_manage/<int:page>')
@login_required
def front_user_manage_page(page):
    index = flask.request.args.get('sort')
    tablename = FrontUser
    start_post, end_post, end_page, web_page = xt_fy.paging(5, tablename,None, page)
    if not index:
        front_users = FrontUser.query[start_post:end_post]
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.front_user_manage',
            'front_users':front_users
        }
        return flask.render_template('cms/front_user_manage.html', **content)
    if index == '1':
        front_users = FrontUser.query.order_by(FrontUser.create_time.desc())[start_post:end_post]
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.front_user_manage',
            'front_users':front_users,
            'sort':'1'
        }
        return flask.render_template('cms/front_user_manage.html', **content)
    if index == '2':
        front_users = FrontUser.query[start_post:end_post]
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.front_user_manage',
            'front_users':front_users,
            'sort':'2'
        }
        return flask.render_template('cms/front_user_manage.html', **content)
    if index == '3':
        front_users = FrontUser.query.order_by(FrontUser.id.desc())[start_post:end_post]
        content = {
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.front_user_manage',
            'front_users':front_users,
            'sort':'3'
        }
        return flask.render_template('cms/front_user_manage.html', **content)
    return flask.abort(404)

# 编辑前台用户管理界面
@bp.route('/edit_front_user/<id>',methods=['GET','POST'])
@login_required
def edit_front_user(id):
    if flask.request.method == 'GET':
        front_user = FrontUser.query.filter_by(id=id).first()
        return flask.render_template('cms/edit_front_user.html',front_user=front_user)

# 板块管理

@bp.route('/board/')
@login_required
def cms_board():
    return cms_board_page(1)

@bp.route('/board/<int:page>')
@login_required
def cms_board_page(page):
    tablename = BoardModel
    start_post, end_post, end_page, web_page = xt_fy.paging(5,tablename,None, page)
    boards = BoardModel.query.filter_by(is_live=True)[start_post:end_post]
    content = {
        'boards': boards,
        'end_page': end_page,
        'web_pages': web_page,
        'page': page,
        'url':'cms.cms_board_page'
    }
    return flask.render_template('cms/board.html',**content)

# 禁用前台用户
@bp.route('/disable/',methods=['POST'])
def deisable():
    id = flask.request.form.get('id')
    front_user = FrontUser.query.filter_by(id=id).first()
    if front_user.is_live:
        front_user.is_live = False
        db.session.commit()
        return xt_json.json_result_ok('禁用成功!')
    else:
        front_user.is_live = True
        db.session.commit()
        return xt_json.json_result_ok('解禁成功!')

# 添加模块管理
@bp.route('/add_board/',methods=['POST'])
def add_board():
    name = flask.request.form.get('name')
    board = BoardModel.query.filter_by(name=name,is_live=True).first()
    if board:
        return xt_json.json_params_error('对不起 该模块已存在!')
    board = BoardModel(name=name)
    flask.g.cms_user.boards.append(board)
    db.session.commit()
    return xt_json.json_result_ok('恭喜，添加成功!')

# 编辑前台模块
@bp.route('/edit_board/',methods=['POST'])
def edit_board():
    id = flask.request.form.get('id')
    name = flask.request.form.get('name')
    board = BoardModel.query.filter_by(name=name,is_live=True).first()
    if board:
        return xt_json.json_params_error('对不起 该模块已存在!')
    board = BoardModel.query.get(id)
    board.name = name
    db.session.commit()
    return xt_json.json_result_ok('修改成功!')

# 删除前台模块
@bp.route('/del_board/',methods=['POST'])
def del_board():
    id = flask.request.form.get('id')
    board = BoardModel.query.get(id)
    board.is_live = False
    db.session.commit()
    return xt_json.json_result_ok('删除成功!')

@bp.context_processor
def cms_context_processor():
    email = flask.session.get(USER_SESSION_ID)
    if email:
        user = flask.g.cms_user
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