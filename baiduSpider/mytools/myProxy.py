#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__: kainhuck

# 提供代理
# 从数据库中获取，事先存进去，有专门爬虫获取代理

import requests

__all__ = ["getProxy", "proxies_num"]

from redis import Redis
from .security_data import redis
import json

# 链接数据库
r = Redis(**redis)

# 这里影响了速度
# myIp = requests.get("http://checkip.amazonaws.com").text
# print("我的真实IP是", myIp)
myIp = '127.0.0.1'

def getProxy(dataBase="proxies:v1"):
    '''
    返回一个代理
    :return:
    '''
    pro = r.rpop(dataBase).lower()
    if pro:
        return json.loads(pro)
    return None


def proxies_num(dataBase="proxies:v1"):
    '''
    返回数据库中剩余的代理数
    :param dataBase:
    :return:
    '''
    return r.llen(dataBase)


def checkProxy(proxies):
    '''
    检查代理是否可用
    :param proxies: 代理
    :return: True 可用,否则 False
    '''
    try:
        r = requests.get("http://checkip.amazonaws.com", headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
            'Connection': 'keep-alive'
        }, proxies=proxies, timeout=5)
        if r.text != myIp:
            return r.text
        else:
            return False
    except:
        return False


if __name__ == '__main__':
    # ----------------------测试------------------------- #

    # proxy = getProxy()
    # print(proxies_num())
    # print(a)
    # print(checkProxy({'HTTP': 'HTTP://58.253.152.16:9999'}))
    proxy = {
        # 'http': 'http://123.207.247.86:9999',
        'https': 'https://117.91.232.200:9999'
        # 'http': 'http://120.83.98.54:9999'
    }
    # proxy = {'https': 'https://113.124.85.154:9999'}

    # proxy = getProxy()

    a = checkProxy(proxy)
    if a:
        print("现在的IP是:", a)
    else:
        print("这个代理已经过期", proxy)
