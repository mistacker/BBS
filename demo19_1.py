#coding:utf-8
from flask import Flask
import flask
from exts import db,mail
from views.front_views import post_views,account_views
from views.cms_views import cms_exts
from flask_wtf import CSRFProtect


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

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)
