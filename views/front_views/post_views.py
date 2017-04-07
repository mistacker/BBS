#coding:utf-8

from flask import Blueprint
import flask
from my_decorator import front_login_required
from constants import FRONT_USER_TEL
from models import front_models,public_models
from constants import AccessKey,SecretKey
from qiniu import Auth
from forms.front_forms import Front_add_post_form,Front_comment_form,Front_second_comment_form,Front_laud_form
from exts import db
from utils import xt_json,xt_fy
from datetime import datetime

bp = Blueprint('front_post',__name__)

# 首页
@bp.route('/')
def index():
    return page_list(1,1,0)

# 分页
@bp.route('/page_list/<int:page>/<int:sort>/<int:board>')
def page_list(page,sort,board):
    tablename = public_models.Post
    boards = public_models.BoardModel.query.filter_by(is_live=True).all()
    temp_board = 0
    posts = ''
    end_page = ''
    web_page = ''
    if sort == 1:  # 最新帖子
        if board == temp_board:
            all_posts_count = public_models.Post.query.filter_by(is_live=True).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = public_models.Post.query.filter_by(is_live=True).order_by(public_models.Post.create_time.desc()).slice(start_post,end_post)
        else:
            all_posts_count = public_models.Post.query.filter_by(is_live=True,board_id=board).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = public_models.Post.query.filter_by(is_live=True,board_id=board).order_by(public_models.Post.create_time.desc()).slice(start_post,end_post)
    elif sort == 2: # 精华帖子
        if board == temp_board:
            all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(public_models.Pick).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(public_models.Pick).order_by(public_models.Pick.create_time.desc(),public_models.Post.create_time.desc()).slice(start_post,end_post)
        else:
            all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True,board_id=board).outerjoin(public_models.Pick).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = db.session.query(public_models.Post).filter_by(is_live=True,board_id=board).outerjoin(public_models.Pick).order_by(public_models.Pick.create_time.desc(),public_models.Post.create_time.desc()).slice(start_post,end_post)
    elif sort == 3:  # 点赞最多
        if board == temp_board:
            all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(public_models.Laud).group_by(public_models.Post.id).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(public_models.Laud).group_by(public_models.Post.id).order_by(db.func.count(public_models.Post.lauds).desc(),public_models.Post.create_time.desc()).slice(start_post,end_post)
        else:
            all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True,board_id=board).outerjoin(public_models.Laud).group_by(public_models.Post.id).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = db.session.query(public_models.Post).filter_by(is_live=True,board_id=board).outerjoin(public_models.Laud).group_by(public_models.Post.id).order_by(db.func.count(public_models.Post.lauds).desc(),public_models.Post.create_time.desc()).slice(start_post, end_post)
    elif sort == 4:   # 评论最多
        if board == temp_board:
            all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(public_models.Comment).group_by(public_models.Post.id).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(public_models.Comment).group_by(public_models.Post.id).order_by(db.func.count(public_models.Post.comments).desc(), public_models.Post.create_time.desc()).slice(start_post,end_post)
        else:
            all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True,board_id=board).outerjoin(public_models.Comment).group_by(public_models.Post.id).count()
            start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
            posts = db.session.query(public_models.Post).filter_by(is_live=True,board_id=board).outerjoin(public_models.Comment).group_by(public_models.Post.id).order_by(db.func.count(public_models.Post.comments).desc(), public_models.Post.create_time.desc()).slice(start_post,end_post)
    # 所有的帖子数
    web_posts_count = public_models.Post.query.filter_by(is_live=True).count()
    content = {
        'boards':boards,
        'posts':posts,
        'end_page':end_page,
        'web_pages':web_page,
        'page':page,
        'url':'front_post.page_list',
        'sort':sort,
        'board':board,
        'all_posts_count':all_posts_count,
        'web_posts_count':web_posts_count
    }
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