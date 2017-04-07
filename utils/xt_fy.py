#coding:utf-8
import flask

def paging(every_page,posts,board_id,page):
    # 每页的帖子数
    every_page = every_page
    # 开始的帖子
    start_post = 0
    # 结束的帖子
    end_post = 0
    if page:
        start_post = (page-1)*every_page
        end_post = page*every_page
    if start_post < 0 | end_post == 0:
        return flask.abort(404)
    # 计算尾页
    all_posts = 0
    try:
        all_posts = int(posts)
    except:
        if not board_id or board_id=='0':
            all_posts = posts.query.filter_by(is_live=True).count()
        else:
            all_posts = posts.query.filter_by(is_live=True,board_id=board_id).count()
    tmp = 0
    tmp = all_posts / every_page
    if all_posts%every_page!=0:
        tmp += 1
    end_page = tmp
    # 页面上显示的页数
    web_page = {}
    if end_page < 5:
        for n in range(0,end_page):
            web_page[n] = n+1
    else:
        if page-2>=1 and page+2<=end_page:
            web_page[0] = page-2
            web_page[1] = page-1
            web_page[2] = page
            web_page[3] = page+1
            web_page[4] = page+2
        if page==1 or page==2:
            web_page[0] = 1
            web_page[1] = 2
            web_page[2] = 3
            web_page[3] = 4
            web_page[4] = 5
        if page==end_page or page==end_page-1:
            web_page[0] = end_page-4
            web_page[1] = end_page-3
            web_page[2] = end_page-2
            web_page[3] = end_page-1
            web_page[4] = end_page
    return start_post,end_post,end_page,web_page