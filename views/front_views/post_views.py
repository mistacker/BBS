#coding:utf-8

from flask import Blueprint
import flask
from my_decorator import front_login_required
from constants import FRONT_USER_TEL
from models import front_models,public_models
from constants import AccessKey,SecretKey
from qiniu import Auth
from forms.front_forms import Front_add_post_form
from exts import db
from utils import xt_json,xt_fy

bp = Blueprint('front_post',__name__)

# 首页
@bp.route('/')
def index():
    return list(1)

# 分页
@bp.route('/list/<int:page>')
def list(page):
    tablename = public_models.Post
    start_post,end_post,end_page,web_page = xt_fy.paging(10,tablename,page)
    boards = public_models.BoardModel.query.filter_by(is_live=True).all()
    posts = public_models.Post.query.filter_by(is_live=True).order_by(public_models.Post.create_time.desc())[start_post:end_post]
    content = {
        'boards':boards,
        'posts':posts,
        'end_page':end_page,
        'web_pages':web_page,
        'page':page,
        'url':'front_post.list'
    }
    return flask.render_template('front/front_index.html',**content)

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
            post = public_models.Post(title=title,content=content)
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
    return flask.render_template('front/post_detail.html',post=post)

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

# 向模板中传递登录用户
@bp.context_processor
def front_context_processor():
    front_tel = flask.session.get(FRONT_USER_TEL)
    if front_tel:
        front_user = flask.g.front_user
        return {'front_user':front_user}
    else:
        return {}