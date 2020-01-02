import requests
from lxml import etree
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36"
}

baseUrl = 'http://www.baidu.com/s'
page = 1 #第几页
word = '3sat'  #搜索关键词
data = {'wd':word,'pn':str(page-1)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}

def getContent(session):
    req = session.get(url=baseUrl, params=data,headers=headers,timeout = 30)
    req.encoding = req.apparent_encoding
    html = etree.HTML(req.text)
    print(req.url)
    # print(req.text)

    # content_box = html.xpath("//div[@class = 'content']/*")
    # for each in content_box:
    #     title = each.xpath(".//h3")
    #     # if type(title) is list and title:
    #     #     print(title[0].xpath("string(.)"))
    #     # print(each.xpath("string(.)"))
    #     content = each.xpath(".//font")
    #     if type(content) is list and content:
    #         print(str(content[0].xpath("string(.)")).replace('\n','').replace('\t','').replace(' ','')+"\n")
    return session

if __name__ == '__main__':
    # 该爬虫智能爬第一页，第二页的内容无法爬取
    session = requests.session()
    page+=1
    print(data.get('pn'))
    print(session.cookies)

    session = getContent(session)
    data["pn"]=str(page-1)+'0'
    print(data.get('pn'))
    print(session.cookies)
    getContent(session)
            
