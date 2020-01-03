#!/usr/bin/python3
# -*- coding: utf-8 -*-

# 这个是用于将数据存进MySQL，将其稍微封装了一下，方便使用

import pymysql
from .security_data import mysql

class Mysql(object):
    def __init__(self, host, username, passwd, database):
        self.host = host
        self.username = username
        self.passwd = passwd
        self.database = database
        self.cursor = None

    def __enter__(self):
        self.db = pymysql.connect(self.host, self.username, self.passwd, self.database)
        self.cursor = self.db.cursor()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_val:
            # 如果出现异常
            print("An Exception: %s." % exc_val)

        self.db.close()
        return True

    def executeSql(self, sql):
        try:
            # 执行SQL语句
            self.cursor.execute(sql)
            # 提交到数据库执行，为了及时跟进数据库这句最好加上
            self.db.commit()
        except:
            # 如果发生错误则回滚
            self.db.rollback()


if __name__ == '__main__':

    # 使用方法
    with Mysql(**mysql) as m:
        results = m.executeSql("SELECT * FROM users;")

        for each in results:
            print(each)
