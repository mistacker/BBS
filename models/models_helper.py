# coding:utf-8
from models import public_models
from utils import xt_fy
from exts import db

class Model_Tool(object):

    class Post_sort_type(object):
        POST_NEW = 1
        POST_PICK = 2
        POST_COMMENT = 3
        POST_LAUD = 4

    @classmethod
    def front_tool(cls,page,sort,board):
        boards = public_models.BoardModel.query.filter_by(is_live=True).all()
        temp_board = 0
        posts = ''
        end_page = ''
        web_page = ''
        all_posts_count = ''
        if sort == cls.Post_sort_type.POST_NEW:  # 最新帖子
            if board == temp_board:
                all_posts_count = public_models.Post.query.filter_by(is_live=True).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = public_models.Post.query.filter_by(is_live=True).order_by(
                    public_models.Post.create_time.desc()).slice(start_post, end_post)
            else:
                all_posts_count = public_models.Post.query.filter_by(is_live=True, board_id=board).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = public_models.Post.query.filter_by(is_live=True, board_id=board).order_by(
                    public_models.Post.create_time.desc()).slice(start_post, end_post)
        elif sort == cls.Post_sort_type.POST_PICK:  # 精华帖子
            if board == temp_board:
                all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(
                    public_models.Pick).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(
                    public_models.Pick).order_by(public_models.Pick.create_time.desc(),
                                                 public_models.Post.create_time.desc()).slice(start_post, end_post)
            else:
                all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True,
                                                                                 board_id=board).outerjoin(
                    public_models.Pick).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(is_live=True, board_id=board).outerjoin(
                    public_models.Pick).order_by(public_models.Pick.create_time.desc(),
                                                 public_models.Post.create_time.desc()).slice(start_post, end_post)
        elif sort == cls.Post_sort_type.POST_LAUD:  # 点赞最多
            if board == temp_board:
                all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.lauds).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
            else:
                all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True,
                                                                                 board_id=board).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(is_live=True, board_id=board).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.lauds).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
        elif sort == cls.Post_sort_type.POST_COMMENT:  # 评论最多
            if board == temp_board:
                all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(is_live=True).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.comments).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
            else:
                all_posts_count = db.session.query(public_models.Post).filter_by(is_live=True,
                                                                                 board_id=board).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(is_live=True, board_id=board).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.comments).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
        # 所有的帖子数
        web_posts_count = public_models.Post.query.filter_by(is_live=True).count()
        content = {
            'boards': boards,
            'posts': posts,
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'front_post.page_list',
            'sort': sort,
            'board': board,
            'all_posts_count': all_posts_count,
            'web_posts_count': web_posts_count
        }
        return content

    @classmethod
    def cms_tool(cls, page, sort, board):
        boards = public_models.BoardModel.query.filter_by().all()
        temp_board = 0
        posts = ''
        end_page = ''
        web_page = ''
        all_posts_count = ''
        sort = int(sort)
        page = int(page)
        board = int(board)
        if sort == cls.Post_sort_type.POST_NEW:  # 最新帖子
            if board == temp_board:
                all_posts_count = public_models.Post.query.count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = public_models.Post.query.order_by(
                    public_models.Post.create_time.desc()).slice(start_post, end_post)
            else:
                all_posts_count = public_models.Post.query.filter_by( board_id=board).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = public_models.Post.query.filter_by( board_id=board).order_by(
                    public_models.Post.create_time.desc()).slice(start_post, end_post)
        elif sort == cls.Post_sort_type.POST_PICK:  # 精华帖子
            if board == temp_board:
                all_posts_count = db.session.query(public_models.Post).outerjoin(
                    public_models.Pick).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).outerjoin(
                    public_models.Pick).order_by(public_models.Pick.create_time.desc(),
                                                 public_models.Post.create_time.desc()).slice(start_post, end_post)
            else:
                all_posts_count = db.session.query(public_models.Post).filter_by(board_id=board).outerjoin(
                    public_models.Pick).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(board_id=board).outerjoin(
                    public_models.Pick).order_by(public_models.Pick.create_time.desc(),
                                                 public_models.Post.create_time.desc()).slice(start_post, end_post)
        elif sort == cls.Post_sort_type.POST_LAUD:  # 点赞最多
            if board == temp_board:
                all_posts_count = db.session.query(public_models.Post).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.lauds).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
            else:
                all_posts_count = db.session.query(public_models.Post).filter_by(board_id=board).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(board_id=board).outerjoin(
                    public_models.Laud).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.lauds).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
        elif sort == cls.Post_sort_type.POST_COMMENT:  # 评论最多
            if board == temp_board:
                all_posts_count = db.session.query(public_models.Post).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.comments).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
            else:
                all_posts_count = db.session.query(public_models.Post).filter_by(board_id=board).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).count()
                start_post, end_post, end_page, web_page = xt_fy.paging(10, all_posts_count, None, page)
                posts = db.session.query(public_models.Post).filter_by(board_id=board).outerjoin(
                    public_models.Comment).group_by(public_models.Post.id).order_by(
                    db.func.count(public_models.Post.comments).desc(), public_models.Post.create_time.desc()).slice(
                    start_post, end_post)
        # 所有的帖子数
        web_posts_count = public_models.Post.query.count()
        content = {
            'boards': boards,
            'posts': posts,
            'end_page': end_page,
            'web_pages': web_page,
            'page': page,
            'url': 'cms.cms_posts_page',
            'sort': sort,
            'board': board,
            'all_posts_count': all_posts_count,
            'web_posts_count': web_posts_count
        }
        return content