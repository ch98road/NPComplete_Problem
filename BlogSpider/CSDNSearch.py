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

def getContent(word, proxy, page, content):
    print("当前第{}页".format(page))
    try:
        url = "https://so.csdn.net/so/search/s.do?p={}&q={}&t=blog&viparticle=&domain=&o=&s=&u=&l=&f=&rbg=0".format(
            page,word)
        re = requests.get(url=url, headers=headers, proxies=proxy)
        html = etree.HTML(re.text)
        tit_list = html.xpath("//dl[@class='search-list J_search']")
        # print(len(tit_list))
        for each in tit_list:
            temp_url = each.xpath(".//div[@class='limit_width']/a[1]/@href")[0]
            temp_title = each.xpath(
                ".//div[@class='limit_width']/a[1]")[0].xpath("string(.)").replace("\"","").replace("\n","").replace(")"," ").replace("("," ").replace("\\","")
            temp_content = each.xpath(
                ".//dd[@class='search-detail']")[0].xpath("string(.)").replace("\"","").replace("\n","").replace(")"," ").replace("("," ").replace("\\","")
            # print("temp_url={}\ntitle={}\ncontent={}\n\n".format(temp_url, temp_title,temp_content))
            content.append([temp_url,temp_title, temp_content])

        if int(html.xpath("//span[@class='page-nav']/a/@page_num")[-1]) > page:
            time.sleep(random.uniform(0, 2))
            return getContent(word=word, proxy=proxy, page=page+1, content=content)
    except:
        print("访问出错")
    return content

def do(word):
    proxy = {"http": random.choice(proxy_list)}

    content = getContent(word=word, proxy=proxy, page=1, content=[])
    # for each in content:
    #     print("url={}\ntitle={}\ncontent={}\n\n".format(
    #         each[0], each[1], each[2]))
    print(len(content))
    sq.insert_into_inital_data(content, "CSDN")
if __name__ == '__main__':
    word = "3sat"
    do(word)