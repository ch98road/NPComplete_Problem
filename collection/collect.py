import BlogSpider.bokeyuanSearch as bk
import BlogSpider.JianshuSearch as js
import BlogSpider.CSDNSearch as csdn
import  mysql.mysqlUtils as sq
import baiduSpider.baiduSearch_hyk as bd

if __name__ == '__main__':
    words=sq.select_problem_name()
    for word in words:
        print("当前的word={}".format(word))
        bk.do(word+" 规约")
        js.do(word+" 规约")
        csdn.do(word+" 规约")
