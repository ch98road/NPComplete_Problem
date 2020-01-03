import requests
import time
from lxml import etree
import random
import os
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
    # , "x-csrf-token": "2JZ7qkLmHS28y8dc/quZoc7L1O6APSZna2KYPkScHdquQdrjnBAjpCRxovXpU5zskagwcij+nZy0T8Uf3jDSSQ=="
    # ,"cookie":"_m7e_session_core=0abf36dbb800c71e074260fdf55e85b6;"
}

proxy_list = [
    '117.90.131.247:8118',
    '171.11.32.77:9999',
    '223.199.31.112:9999',
    '27.191.234.69:9999',
    '223.199.31.5:9999',
    '60.167.135.179:9999'
]

# 获取必要的两个访问头x-csrf-token和_m7e_session_core
def getCookie(word, head, proxy):
    # 先通过必要的一次访问获取x-csrf-token值和cookie中_m7e_session_core的值，二次构造header
    url = r"https://www.jianshu.com/search?q={}&page=1&type=note".format(word)
    re = requests.get(url=url, headers=head, timeout=30, proxies=proxy)
    html = etree.HTML(re.text)
    head["x-csrf-token"] = str(html.xpath("//*[@name='csrf-token']/@content")[0])
    strCookie = "_m7e_session_core={};".format(
        re.cookies.get("_m7e_session_core"))
    head["cookie"] = strCookie
    # print(head)
    return head


def getContent(word, head, proxy,page,content):
    try:
        # 用post请求访问真正数据
        url = "https://www.jianshu.com/search/do?q={}&type=note&page={}&order_by=default".format(
            word,page)
        re = requests.post(url=url, headers=head, timeout=30, proxies=proxy)

        # Json分析
        js = json.loads(re.text)
        # 从JSON中获取总页数
        total_pages = js["total_pages"]
        data = js["entries"]

        for each in data:
            temp_title = each["title"]
            temp_content = each["content"]
            temp_url = "https://www.jianshu.com/p/{}".format(each["slug"])
            # print("{},{},{}".format(temp_title, temp_content, temp_url))
            content.append([temp_title,temp_content,temp_url])
        # 递归访问下一页
        if total_pages>page:
            return getContent(word=word, head=head, proxy=proxy,page=page+1,content=content)
    except:
        print("访问出错")
    return content

if __name__ == '__main__':

    # 随机获取代理ip
    proxy = {"http": random.choice(proxy_list)}
    # print(proxy)

    word = "3sat"
    head = getCookie(word=word,head=headers.copy(),proxy= proxy)
    content = getContent(word=word, head=head, proxy=proxy,page=1,content = [])
    print(len(content))
    # for each in content:
    #     print("title={}\ncontent={}\nurl={}\n\n".format(each[0],each[1],each[2]))