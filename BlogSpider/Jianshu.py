import requests
import time
from lxml import etree
import random
import os
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    }

def getContent(url):
    try:
        re = requests.get(url,headers = headers)
        re.encoding = re.apparent_encoding
        # print(re.text)
        html = etree.HTML(re.text)
        title = html.xpath("//*[@id='__next']/div[1]/div/div/section[1]/h1/text()")
        content = []
        for each in html.xpath("//*[@id='__next']/div[1]/div/div/section[1]/article/*"):
            con_temp = each.xpath("string(.)")
            if  con_temp:
                content.append(str(con_temp))
            con_temp = each.xpath(".//@data-original-src")

            if con_temp:
                for ImgIndex in range(len(con_temp)):
                    if ImgIndex>0 and con_temp[ImgIndex] is not con_temp[ImgIndex-1]:
                        content.append("![]({})".format(con_temp[ImgIndex]))
                    elif ImgIndex==0:
                        content.append("![]({})".format(con_temp[ImgIndex]))
                    # print(ImgIndex,con_temp[ImgIndex])
        return title,content
    except:
        return "",""
def save(title,content):
    with open("{}.md".format(title[0]),'w',encoding='utf-8') as f:
        f.write(str(title[0])+'\n\n')
        for each in content:
            f.write(each+'\n')


if __name__ == '__main__':
    url = "https://www.jianshu.com/p/280c6a6f2594"
    url = "https://www.jianshu.com/p/d75211cec9df"
    title,content = getContent(url)
    if title is not "":
            save(title,content)
            pass
    else:
        print("访问出错，请确认下url试试")