#coding:utf-8

from exts import db
from flask_migrate import Migrate,MigrateCommand
from flask_script import Manager
from models import cms_models,font_models,public_models
from demo19_1 import app

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
    return 'seccess'

# 添加权限分组
@manager.option('-n',dest='name')
@manager.option('-desc',dest='desc')
@manager.option('-p',dest='power')
def add_power_group(name,desc,power):
    cms_role = cms_models.CMSRole(name=name.decode('gbk').encode('utf8'),desc=desc.decode('gbk').encode('utf8'),power=power)
    db.session.add(cms_role)
    db.session.commit()
    print 'seccess add power_group'


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
    print 'add this cms_user to group access!'

# 把当前已创建好的cms用户添加到分组中
@manager.option('-e',dest='email')
@manager.option('-r',dest='role_name')
def add_group_user(email,role_name):
    cms_user = cms_models.CMSUser.query.filter_by(email=email).first()
    if not cms_user:
        print 'cms_user is not font'
        return
    cms_role = cms_models.CMSRole.query.filter_by(name=role_name.decode('gbk').encode('utf8')).first()
    if not cms_role:
        print 'cms_role is not font'
        return
    cms_role.cms_users.append(cms_user)
    db.session.commit()
    print 'add user to group seccess'

if __name__ == '__main__':
    manager.run()