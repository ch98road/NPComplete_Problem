import requests
import time
from lxml import etree
import random
import os
import json



headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "accept-language":"zh-CN,zh;q=0.9,en;q=0.8",
    # "cookie":"acw_sc__v2=5e0c4608eda0369b627288eebf26ea9b0d11bcbb"
    "cookie":  "acw_sc__v2=5e0c90c2e2e885ed5748dbfaf6b26a12f0aad2e0"
    }


def getContent(url):
    try:
        req = requests.get(url,headers = headers)
        req.encoding = req.apparent_encoding
        # print(req.text)
        html = etree.HTML(req.text)
        title = html.xpath("//*[@id='mainBox']/main/div[1]/div/div/div[1]/h1/text()")
        content = []
        for each in html.xpath("//*[@id='content_views']/*"):
            con_temp = each.xpath("string(.)")
            if  con_temp:
                content.append(str(con_temp))
            con_temp = each.xpath("img/@src")
            if con_temp:
                for eImg in con_temp:
                    content.append("![]({})".format(eImg))
        return title,content
    except:
        return "",""

def save(title,content,name):
    with open("{}.md".format(name),'w',encoding='utf-8') as f:
        f.write(str(title[0])+'\n\n')
        for each in content:
            f.write(each+'\n')


if __name__ == '__main__':
    url = "https://blog.csdn.net/w746805370/article/details/51312248"

    # 3SAT规约到独立集
    url = "https://blog.csdn.net/xiazdong/article/details/8258092"
    # 【NPC】3、3SAT规约到顶点覆盖
    url = "https://blog.csdn.net/xiazdong/article/details/8258086"
    # 证明题NP难问题:3SAT-------》独立集
    name = "3SAT-独立集"
    url = "https://blog.csdn.net/u010499172/article/details/73920646"

    # 几个NP-完全问题的证明
    name = "几个NP-完全问题的证明"
    url = "https://blog.csdn.net/kufaaa/article/details/54630460"
    title,content = getContent(url)
    if title is not "":
        save(title,content,name)
    else:
        print("访问出错，请更换acw码或者确认url试试")
    # 使用说明：由于CSDN中的加密机制，因此就算是静态页面，没有acw加密的码也拿不到真实数据
    # 故此使用时需预先获取acw_sc__v2码，它存在一定的时效性，具体获取方法见README
    