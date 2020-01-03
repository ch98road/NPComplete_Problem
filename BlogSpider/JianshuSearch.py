import requests
import time
from lxml import etree
import random
import os
import json
import mysql.mysqlUtils as sq

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
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
    url = "https://www.jianshu.com/search?q={}&page=1&type=note".format(word)
    re = requests.get(url=url, headers=head, timeout=30, proxies=proxy)
    html = etree.HTML(re.text)
    head["x-csrf-token"] = str(html.xpath("//*[@name='csrf-token']/@content")[0])
    strCookie = "_m7e_session_core={};".format(
        re.cookies.get("_m7e_session_core"))
    head["cookie"] = strCookie
    # print(head)
    return head


def getContent(word, head, proxy, page, content, total_pages):
    print("当前第{}页".format(page))
    try:
        # 用post请求访问真正数据
        url = "https://www.jianshu.com/search/do?q={}&type=note&page={}&order_by=default".format(
            word, page)
        re = requests.post(url=url, headers=head, timeout=30, proxies=proxy)

        # Json分析
        js = json.loads(re.text)
        # 从JSON中获取总页数
        try:
            if total_pages == 0:
                total_pages = js["total_pages"]
            data = js["entries"]
        except:
            print("total_pages or error")

        if data:
            for each in data:
                temp_title = each["title"].replace("\"", "").replace("\n", "").replace(")", " ").replace("(",
                                                                                                         " ").replace(
                    "\\", "")
                temp_content = each["content"].replace("\"", "").replace("\n", "").replace(")", " ").replace("(",
                                                                                                             " ").replace(
                    "\\", "")
                temp_url = "https://www.jianshu.com/p/{}".format(each["slug"])
                # print("{}\n{}\n{}\n\n".format(temp_title, temp_content, temp_url))
                content.append([temp_url, temp_title, temp_content])
        # 递归访问下一页
        if total_pages != 0 and total_pages > page and page < 15:
            time.sleep(1)
            return getContent(word=word, head=head, proxy=proxy, page=page + 1, content=content,
                              total_pages=total_pages)
    except NameError as  e:
        print(e, "访问出错")
    return content


def do(word):
    # 随机获取代理ip
    proxy = {"http": random.choice(proxy_list)}
    # print(proxy)
    head = getCookie(word=word, head=headers.copy(), proxy=proxy)
    content = getContent(word=word, head=head, proxy=proxy, page=1, content=[], total_pages=0)
    print(len(content))
    # for each in content:
    #     print("title={}\ncontent={}\nurl={}\n\n".format(each[0],each[1],each[2]))
    sq.insert_into_inital_data(content, "简书")


if __name__ == '__main__':
    word = "电路SAT"
    do(word)
