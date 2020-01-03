import requests
import time
from lxml import etree
import random
import os
import json

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36",
    "cookie":"ShitNoRobotCookie=CfDJ8FKe-Oc4rmBCjdz4t-OOIu2aEYBudlB9ouQyKS59I7-mpuH4nlKbJjWLG1AlCW6KV9i7XJM75CdElvddoYV5QkcGXyda8ucnZLPJmfMMI5QChwjxFwm_FYME0m-e88z9xA; "
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
        url = "https://zzk.cnblogs.com/s/blogpost?Keywords={}&pageindex={}".format(
            word,page)
        re = requests.get(url=url, headers=headers, proxies=proxy)
        html = etree.HTML(re.text)
        tit_list = html.xpath("//div[@class='forflow']/div[@class='searchItem']")
        # print(len(tit_list))
        for each in tit_list:
            temp_url = each.xpath("./h3/a/@href")
            temp_title = each.xpath(
                "./h3/a")[0].xpath("string(.)")
            temp_content = each.xpath(
                "./span")[0].xpath("string(.)").strip()
            # print("temp_url={}\ntitle={}\ncontent={}\n\n".format(temp_url, temp_title,temp_content))
            content.append([temp_title, temp_content, temp_url])

        print()
        if "current" not in str(html.xpath("//div[@class='forflow']/div[@id='paging_block']//a/@class")[-1]):
            time.sleep(random.uniform(0, 2))
            return getContent(word=word, proxy=proxy, page=page+1, content=content)
    except:
        print("访问出错")
    return content

if __name__ == '__main__':
    proxy = {"http": random.choice(proxy_list)}
    word = "3sat"
    content = getContent(word=word, proxy=proxy, page=1, content=[])
    for each in content:
        print("url={}\ntitle={}\ncontent={}\n\n".format(
            each[0], each[1], each[2]))
