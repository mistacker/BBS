#coding:utf-8

from cms_exts import bp
import flask


@bp.route('/login/')
def index():
    return flask.render_template('cms/login.html')