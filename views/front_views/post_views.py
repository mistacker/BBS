#coding:utf-8

from flask import Blueprint
import flask
from my_decorator import front_login_required
from constants import FRONT_USER_TEL,LOGIN_TEMP
from models import front_models,public_models
from constants import AccessKey,SecretKey
from qiniu import Auth
from forms.front_forms import Front_add_post_form,Front_comment_form,Front_second_comment_form,Front_laud_form,Front_setting_form
from exts import db
from utils import xt_json,xt_fy
from datetime import datetime
from models.models_helper import Model_Tool

bp = Blueprint('front_post',__name__)

# 首页
@bp.route('/')
def index():
    return page_list(1,1,0)

# 分页
@bp.route('/page_list/<int:page>/<int:sort>/<int:board>')
def page_list(page,sort,board):
    content = Model_Tool.front_tool(page,sort,board)
    return flask.render_template('front/front_index.html',**content)


# 测试
@bp.route('/test/')
def test():
    posts = db.session.query(public_models.Post).outerjoin(public_models.Comment).group_by(public_models.Post.id).order_by(db.func.count(public_models.Post.comments),public_models.Post.create_time.desc()).all()
    print posts
    return 'success'

# 发表新帖子
@bp.route('/add_post/',methods=['GET','POST'])
@front_login_required
def add_post():
    if flask.request.method == 'GET':
        boards = public_models.BoardModel.query.filter_by(is_live=True).all()
        return flask.render_template('front/add_post.html',boards=boards)
    else:
        form = Front_add_post_form(flask.request.form)
        if form.validate():
            title = form.title.data
            post = public_models.Post.query.filter_by(title=title,is_live=True).first()
            if post:
                return xt_json.json_params_error('对不起 该帖子标题已存在!')
            board_id = form.board_id.data
            content = form.content.data
            board = public_models.BoardModel.query.get(board_id)
            front_user = flask.g.front_user
            post = public_models.Post(title=title,content=content,create_time=datetime.now())
            board.posts.append(post)
            front_user.posts.append(post)
            db.session.commit()
            return xt_json.json_result_ok('恭喜 帖子发表成功!')
        else:
            return xt_json.json_params_error(form.get_error())

# 帖子详情界面
@bp.route('/post_detail/<int:id>')
def post_detail(id):
    if not id:
        return flask.abort(404)
    post = public_models.Post.query.get(id)
    post.read_count+=1
    db.session.commit()
    laud_front_user_ids = [laud.front_user.id for laud in post.lauds]
    content = {
        'post':post,
        'laud_front_user_ids':laud_front_user_ids
    }
    return flask.render_template('front/post_detail.html',**content)

# 评论
@bp.route('/comment/<int:id>')
@front_login_required
def comment(id):
    if not id:
        return flask.abort(404)
    post = public_models.Post.query.get(id)
    return flask.render_template('front/comment.html',post=post)

# 测试二级评论
# @bp.route('/test/')
# def test():
#     comment = public_models.Comment(comtent='这是评论')
#     comment.front_user = front_models.FrontUser.query.first()
#     comment.post = public_models.Post.query.first()
#     comment.origin_comment = public_models.Comment.query.first()
#     db.session.add(comment)
#     db.session.commit()
#     return 'success'

# 添加评论
@bp.route('/add_comment/',methods=['POST'])
def add_comment():
    form = Front_comment_form(flask.request.form)
    if form.validate():
        post_id = form.id.data
        content = form.content.data
        post = public_models.Post.query.get(post_id)
        front_user = flask.g.front_user
        comment = public_models.Comment(comtent=content,create_time=datetime.now())
        post.comments.append(comment)
        front_user.comments.append(comment)
        db.session.commit()
        return xt_json.json_result_ok('评论成功!')
    else:
        return xt_json.json_params_error(form.get_error())

# 二级评论
@bp.route('/add_comment/<int:post_id>/<int:comment_id>')
@front_login_required
def add_second_comment(post_id,comment_id):
    post = public_models.Post.query.filter_by(is_live=True,id=post_id).first()
    comment = public_models.Comment.query.filter_by(is_live=True,id=comment_id).first()
    content = {
        'post':post,
        'comment':comment
    }
    return flask.render_template('front/comment.html',**content)

# 添加二级评论
@bp.route('/add_second_comment/',methods=['POST'])
def add_second_comment_func():
    form = Front_second_comment_form(flask.request.form)
    if form.validate():
        post_id = form.id.data
        content = form.content.data
        comment_id = form.comment_id.data
        post = public_models.Post.query.filter_by(is_live=True, id=post_id).first()
        comment = public_models.Comment.query.filter_by(is_live=True, id=comment_id).first()
        child_comment = public_models.Comment(comtent=content,create_time=datetime.now())
        child_comment.origin_comment = comment
        child_comment.post = post
        child_comment.front_user = flask.g.front_user
        db.session.add(child_comment)
        db.session.commit()
        return xt_json.json_result_ok('评论成功!')
    else:
        return xt_json.json_params_error(form.get_error())

# 点赞方法
@bp.route('/laud/',methods=['POST'])
def laud():
    form = Front_laud_form(flask.request.form)
    if not hasattr(flask.g,'front_user'):
        return xt_json.json_params_error('请登录!')
    if form.validate():
        post_id = form.post_id.data
        post = public_models.Post.query.get(post_id)
        front_user = flask.g.front_user
        same_laud = public_models.Laud.query.filter_by(post_id = post_id,front_user_id=front_user.id).first()
        if same_laud:
            db.session.delete(same_laud)
            db.session.commit()
            return xt_json.json_result_ok('success')
        else:
            laud = public_models.Laud(create_time=datetime.now())
            laud.post = post
            laud.front_user = front_user
            db.session.add(laud)
            db.session.commit()
            return xt_json.json_result_ok('success')
    else:
        return xt_json.json_params_error(form.get_error())

# 设置界面
@bp.route('/setting/')
@front_login_required
def setting():
    return flask.render_template('front/front_user_setting.html')

# 保存设置界面
@bp.route('/save_setting/',methods=['POST'])
def save_setting():
    form = Front_setting_form(flask.request.form)
    if form.validate():
        front_user = flask.g.front_user
        if not front_user:
            return xt_json.json_server_error('数据错误!')
        relname = form.relname.data
        gender = form.gender.data
        qq = form.qq.data
        avatar = form.avatar.data
        signature = form.signature.data
        front_user.relname = relname
        front_user.gender = gender
        front_user.qq = qq
        front_user.avatar = avatar
        front_user.signature = signature
        db.session.commit()
        return xt_json.json_result_ok('设置成功!')
    else:
        return xt_json.json_params_error(form.get_error())

# 个人中心页面

# 抽取目标用户
def get_current_user(id):
    if not id:
        flask.abort(404)
    current_user = front_models.FrontUser.query.filter_by(id=id).first()
    if not current_user:
        flask.abort(404)
    content = {
        'current_user': current_user
    }
    return content

# 个人资料
@bp.route('/profile/<string:id>')
def profile(id):
    content = get_current_user(id)
    content['temp'] = 1
    return flask.render_template('front/front_profile.html',**content)

# 个人帖子
@bp.route('/profile_posts/<string:id>')
def profile_posts(id):
    content = get_current_user(id)
    content['temp'] = 2
    return flask.render_template('front/front_profile_posts.html',**content)

# 获取七牛token
@bp.route('/get_token/')
def get_token():
    # 构建鉴权对象
    q = Auth(AccessKey,SecretKey)
    # 要上传的七牛空间
    bucket_name = 'blog'
    # 生成上传Token
    token = q.upload_token(bucket_name)
    # 返回
    return flask.jsonify({'uptoken': token})

# 定义钩子函数用来保存当前登录的用户
@bp.before_request
def my_front_before_request():
    telephone = flask.session.get(FRONT_USER_TEL)
    if telephone:
        front_user = front_models.FrontUser.query.filter_by(telephone=telephone,is_live=True).first()
        if front_user:
            flask.g.front_user = front_user
    else:
        telephone = LOGIN_TEMP['font_login_tel']
        last_login_time = LOGIN_TEMP['last_login_time']
        if telephone and last_login_time:
            front_user = front_models.FrontUser.query.filter_by(telephone=telephone,is_live=True).first()
            front_user.lask_login_time = last_login_time
            db.session.commit()

# 向模板中传递登录用户
@bp.context_processor
def front_context_processor():
    front_tel = flask.session.get(FRONT_USER_TEL)
    if front_tel:
        front_user = flask.g.front_user
        return {'front_user':front_user}
    else:
        return {}