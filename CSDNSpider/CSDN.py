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
    "cookie":  "acw_sc__v2=5e0c5e185cc6a68ba12fcce39cefcbcbbe87a608"
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
                    content.append("![].({})".format(eImg))
        return title,content
    except:
        return "",""

def save(title,content):
    with open("{}.txt".format(title[0]),'w',encoding='utf-8') as f:
        f.write(str(title[0])+'\n\n')
        for each in content:
            f.write(each+'\n')


if __name__ == '__main__':
    url = "https://blog.csdn.net/LI_AINY/article/details/89456412"
    url = "https://blog.csdn.net/qian123shuai/article/details/85866286"
    # url = "https://blog.csdn.net/m0_37696990/article/details/101704767"
    title,content = getContent(url)
    save(title,content)
    # 使用说明：由于CSDN中的加密机制，因此就算是静态页面，没有acw加密的码也拿不到真实数据
    # 故此使用时需预先获取acw_sc__v2码，它存在一定的时效性，具体获取方法见README
    