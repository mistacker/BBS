#coding:utf-8
from flask import Flask
import flask
from exts import db,mail
from views.front_views import post_views,account_views
from views.cms_views import cms_exts
from flask_wtf import CSRFProtect
from datetime import datetime

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)
mail.init_app(app)
CSRFProtect(app)

app.register_blueprint(post_views.bp)
app.register_blueprint(account_views.bp)
app.register_blueprint(cms_exts.bp)

# 定义404错误
@app.errorhandler(404)
def cms_errorHanderler(error):
    return flask.render_template('cms/404.html'),404

# 定义401错误
@app.errorhandler(401)
def cms_errorHanderler(error):
    return flask.render_template('cms/401.html'),401

# 自定义过滤器获取板块帖子数
@app.template_filter('get_count')
def get_count(posts):
    count = 0
    for post in posts:
        if post.is_live:
            count+=1
    return count

# 自定义过滤器判断未定义
@app.template_filter('undefine')
def undefine(value):
    if not value:
        return u'未定义'
    else:
        return value

# 自定义过滤器判断性别
@app.template_filter('gender')
def gender(value):
    value = int(value)
    if value == 1:
        return u'男'
    elif value == 2:
        return u'女'
    elif value == 3:
        return u'保密'
    else:
        return u'未知'

# 自定义过滤器判断时间
@app.template_filter('format_time')
def format_time(value):
    # 获取当前时间
    time = datetime.now()
    # 时间差
    rs_time = (time-value).total_seconds()
    # 定义变量
    temp = ''
    if rs_time<60:
        temp = u'刚刚'
    elif rs_time<60*60:
        temp = u'%s分钟前'%int(rs_time/60)
    elif rs_time<60*60*24:
        temp = u'%s小时前'%int(rs_time/(60*60))
    elif rs_time<60*60*24*30:
        temp = u'%s天前'%int(rs_time/(60*60*24))
    elif rs_time<60*60*24*30*12:
        temp = u'%s月前' % int(rs_time / (60 * 60 * 24*30))
    elif rs_time>60*60*24*30*12:
        temp = u'%s年前' % int(rs_time / (60 * 60 * 24 * 30*12))
    return temp

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
