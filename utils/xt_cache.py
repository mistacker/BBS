#coding: utf8

#使用memcached
import memcache
cache = memcache.Client(['127.0.0.1:11211'],debug=True)
import string,random

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

# 生成验证码
def set_captcha(num,email,time=5*60):
    if isinstance(num,int)==False:
        return False
    temp = string.letters+'0123456789'
    captcha = random.sample(temp,num)
    captcha = ''.join(captcha)
    set(email,captcha,time)
    return captcha

# 生成数字验证码
def create_num_captcha(num,key,timeout=60):
    temp = '0123456789'
    rs = random.sample(temp,num)
    rs = ''.join(rs)
    set(key=key,value=rs,timeout=timeout)
    return rs

# 判断验证码是否相等
def check_captcha(key,web_captcha):
    ser_captcha = get(key)
    if not ser_captcha:
        return False
    if ser_captcha.lower() == web_captcha.lower():
        return True
    else:
        return False