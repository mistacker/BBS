#coding:utf-8
from flask import Flask
import flask
from exts import db
from views.front_views import post_views,account_views
from views.cms_views import cms_views,account_views

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

app.register_blueprint(post_views.bp)
app.register_blueprint(account_views.bp)
app.register_blueprint(cms_views.bp)
app.register_blueprint(account_views.bp)


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=80, debug=True)