#!/usr/bin/python3
# -*- coding: utf-8 -*-
# __author__: kainhuck

'''
文本处理工具
'''

__all__ = ['to_dict']

from .MyError import TextNotCorrectError

def to_dict(string):
    '''
    将String转换成字典
    :param string: 必须长得像dict
    :return:
    '''
    result = {}
    string = string.strip()
    items = string.split('\n')
    for item in items:
        item = item.strip()
        try:
            key, *value = (each.strip() for each in item.split(":"))
        except:
            raise TextNotCorrectError("待转换的文本格式错误")
        result[key] = ':'.join(value)

    return result


def _test():
    test_str = '''
    ct: 24
    qqmusic_ver: 1298
    new_json: 1
    remoteplace: txt.yqq.center
    searchid: 51976023507034189
    t: 0
    aggr: 1
    cr: 1
    catZhida: 1
    lossless: 0
    flag_qc: 0
    p: 1
    n: 10
    w: 乐队的夏天
    g_tk: 5381
    loginUin: 0
    hostUin: 0
    format: json
    inCharset: utf8
    outCharset: utf-8
    notice: 0
    platform: yqq.json
    needNewCode: 0
    '''
    print(to_dict(test_str))



if __name__ == '__main__':
    _test()
