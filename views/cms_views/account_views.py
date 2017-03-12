#coding:utf-8

from cms_exts import bp

@bp.route('/account/')
def account():
    return 'this is account page'