#coding:utf-8

from exts import db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from models import cms_models,front_models,public_models
from demo19_1 import app
import time

manager = Manager(app)
migrate = Migrate(app,db)
manager.add_command('db',MigrateCommand)

# 添加cms用户
@manager.option('-n',dest='username')
@manager.option('-p',dest='password')
@manager.option('-e',dest='email')
def create_cms_user(username,password,email):
    cms_user = cms_models.CMSUser(username=username,password=password,email=email)
    db.session.add(cms_user)
    db.session.commit()
    return 'success'

# 添加权限分组
@manager.option('-n',dest='name')
@manager.option('-desc',dest='desc')
@manager.option('-p',dest='power')
def add_power_group(name,desc,power):
    cms_role = cms_models.CMSRole(name=name.decode('gbk').encode('utf8'),desc=desc.decode('gbk').encode('utf8'),power=power)
    db.session.add(cms_role)
    db.session.commit()
    print 'success add power_group'


# 分组内添加cms用户
@manager.option('-n',dest='name')
@manager.option('-p',dest='pwd')
@manager.option('-e',dest='email')
@manager.option('-r','--role_name',dest='role')
def add_cms_user(name,pwd,email,role):
    cms_role = cms_models.CMSRole.query.filter_by(name=role.decode('gbk').encode('utf8')).first()
    if not cms_role:
        print '没有指定分组'
        return
    cms_user = cms_models.CMSUser(username=name,password=pwd,email=email)
    cms_role.cms_users.append(cms_user)
    db.session.commit()
    print 'add this cms_user to group success!'

# 把当前已创建好的cms用户添加到分组中
@manager.option('-e',dest='email')
@manager.option('-r',dest='role_name')
def add_group_user(email,role_name):
    cms_user = cms_models.CMSUser.query.filter_by(email=email).first()
    if not cms_user:
        print 'cms_user is not find'
        return
    cms_role = cms_models.CMSRole.query.filter_by(name=role_name.decode('gbk').encode('utf8')).first()
    if not cms_role:
        print 'cms_role is not find'
        return
    cms_role.cms_users.append(cms_user)
    db.session.commit()
    print 'add user to group success'

# 检查用户是否拥有某个权限
@manager.option('-e',dest='email')
@manager.option('-n',dest='n')
def check_power(email,n):
    cms_user = cms_models.CMSUser.query.filter_by(email=email).first()
    if not cms_user:
        print 'sorry not find this cms_user'
        return
    if cms_user.has_power(int(n)):
        print 'this cms_user has this power'
    else:
        print 'this cms_user not has this power'
    return

# 检查用户所有的权限和信息
@manager.option('-e',dest='email')
def get_all_power_infos(email):
    cms_user = cms_models.CMSUser.query.filter_by(email=email).first()
    if not cms_user:
        print 'sorry not find this cms_user'
        return
    print cms_user.get_all_power_info()
    return

# 添加很多帖子用来测试
@manager.command
def create_posts():
    board = public_models.BoardModel.query.filter_by(name='PHP',is_live=True).first()
    front_user = front_models.FrontUser.query.filter_by(username='python',is_live=True).first()
    for i in range(1,101):
        post = public_models.Post(title=('这是标题%d'%i),content=('这是内容%d'%i))
        post.front_user = front_user
        post.board = board
        db.session.add(post)
        db.session.commit()
        print '%d finish'%i
        time.sleep(2)
    print 'success'
    return

if __name__ == '__main__':
    manager.run()