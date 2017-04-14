#coding:utf-8
import cProfile

import redis
from models import models_helper

host = ''
port = ''
password = ''
name = 'port'
#
# cache = redis.StrictRedis(host=host,port=port,password=password)
#
# # 添加帖子
# # 考虑后用list数据类型更合适点，所以用rpush
# def add_port(port_model):
#     port_json = models_helper.Model_Tool.to_json(port_model)
#     cache.rpush(name,port_json)     # 保存成字典
#
# def get_ports(start,end):
#     rs =  cache.lrange(name,start,end)
#     print rs
#     return rs
#
# # 查看列表中有多少数据
# def get_len():
#     return cache.llen(name)

# # profile的使用                  ########################
# profile = cProfile.Profile()
# profile.runcall(方法,参数)       # 第一个参数为方法，第二个参数为方法中的参数，因为是args类型 所以需要多个参数中间用','隔开
# print profile.print_stats()     # 打印方法运行过程中数据，里面有时间。

class PORT_redis(object):
    def __init__(self,redis):
        self.__redis = redis

    def add_port(self,port_model):
        port_json = models_helper.Model_Tool.to_json(port_model)
        self.__redis.rpush(name,port_json)

    def get_ports(self,start,end):
        rs = self.__redis.lrange(name,start,end)
        return rs

    def get_len(self):
        return self.__redis.llen(name)

class BBS_redis(object):

    __redis = redis.StrictRedis(host=host,port=port,password=password)

    @classmethod
    def port(cls):
        port_redis = PORT_redis(cls.__redis)
        return port_redis

    @classmethod
    def get(cls,key):
        cls.__redis.get(key)

    @classmethod
    def set(cls,key,value):
        cls.__redis.set(key,value)