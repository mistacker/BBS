#coding: utf8

#使用memcached
import memcache
cache = memcache.Client(['127.0.0.1:11211'],debug=True)

# 从缓存中获取数据的函数
def get(key=None):
    if key:
        return cache.get(key)
    return None

# 设置缓存的函数，默认过期时间是5分钟
def set(key=None,value=None,timeout=5*60):
    if key and value:
        result = cache.set(key,value,timeout)
        return result
    return False

# 删除缓存
def delete(key=None):
    if key:
        cache.delete(key)
        return True
    return False

# 添加缓存的函数，默认过期时间是5分钟
def add(key=None,value=None,timeout=5*60):
    if key and value:
        result = cache.add(key,value,timeout)
        return result
    return False