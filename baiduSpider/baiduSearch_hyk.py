import requests
from baiduSpider.mytools.UserAgent import makeAgent
from baiduSpider.mytools.text import to_dict
from pprint import pprint

from lxml import etree
import time

url = "https://www.baidu.com/s"


def get_each_page(pn):
    string = to_dict('''
    ie: utf-8
    mod: 1
    isbd: 1
    isid: e447cac600083db2
    wd: site:csdn.net npc问题归约   
    pn: %d
    oq: npc问题归约
    ie: utf-8
    rsv_idx: 1
    rsv_pq: e447cac600083db2
    rsv_t: aed8FtYXvUG11jkT3B30RJLH3AoDH5u3WRUj+H/ht5SJwwAHJ/rfmRmC+s4
    bs: npc问题归约
    rsv_sid: 1427_21082_30211_18560_30283_30503
    _ss: 1
    clist: 3c28ace6c7f7f97f	3d01acecc83b0ea5	3c28ace6c7f7f97f	dd81e66b94300afe
    hsug: npc问题归约关系	npc问题归约
    f4s: 1
    csor: 7
    _cr1: 37333
    ''' % pn)
    '''
    如果要从博客园查就将wd改为  site:cnblogs.com npc问题归约     
    '''

    r = requests.get(url, headers=makeAgent(), params=string)

    # print(r.status_code)
    html = r.text

    sel = etree.HTML(html)

    content = sel.xpath('//div[@class="result c-container "]')
    for index, each in enumerate(content):
        print("{} {} {:50} {} {}\n".format(
            index + 1,
            each.xpath('./h3/a/@href')[0],
            "".join("".join(each.xpath('./h3/a/text()')).split("-")[:-1]).strip(),
            "".join(each.xpath('./div[@class="c-abstract"]/text()')).strip(),
            "".join(each.xpath('./h3/a/text()')).split("-")[-1]).strip())

        # print(each.xpath('./div[@class="c-abstract"]/text()'))
        time.sleep(1)


if __name__ == "__main__":
    for i in range(1, 11):
        print("第{}页内容如下：".format(i))
        get_each_page(i * 10)
