import time
import pymysql
import random

user = "root"
password = "1230"
host = 'www.cmcandy.com'
db = 'np_complete'
port = 3306


def insert_into_inital_data(content=[], sourse=''):
    try:
        conn = pymysql.connect(host=host, user=user, passwd=password,
                               db=db, charset='utf8', port=port)  # 默认为127.0.0.1本地主机
        cur = conn.cursor()
        data = ""
        for each in content:
            data += "(\"{}\",\"{}\",\"{}\",\"{}\"),".format(each[0], each[1], each[2], sourse)
        data = data[:-1]

        sql = "insert into inital_data(url,title,content,source) values" + data + ";"
        print(sql)
        cur.execute(sql)
        conn.commit()

    except:
        print("插入出错")
    finally:
        cur.close()
        conn.close()


def select_problem_name():
    '''
    查询所有problem
    :return:
    '''
    words = []
    try:
        conn = pymysql.connect(host=host, user=user, passwd=password,
                               db=db, charset='utf8', port=port)  # 默认为127.0.0.1本地主机
        cur = conn.cursor()

        cur.execute("select name from problem")
        conn.commit()
        fr = cur.fetchall()
        for each in fr:
            words.append(each[0])
        return words
    except:
        print("查询错误")
    finally:
        cur.close()
        conn.close()



def get_problem_name():
    '''
    读取NPC.txt中problem数据
    :return:
    '''
    with open("../NPC.txt", "r", encoding='UTF-8') as f:
        words = []
        temp = f.readline()
        while temp:
            words.append(temp.replace("\n", ""))
            temp = f.readline()
    return words


def insert_problem():
    '''
    插入新problem
    :return:
    '''
    words1 = get_problem_name()
    words2 = select_problem_name()
    # 差集
    words = subtraction = list(set(words1).difference(set(words2)))
    if words:
        try:
            conn = pymysql.connect(host=host, user=user, passwd=password,
                                   db=db, charset='utf8', port=port)  # 默认为127.0.0.1本地主机
            cur = conn.cursor()
            data = ""
            i = 0
            for each in words:
                data += "(\"{}\"),".format(each)
                i += 1
            data = data[:-1]

            sql = "insert into problem(name) values" + data + ";"
            print("插入了{}条".format(i))
            print(sql)
            cur.execute(sql)
            conn.commit()

        except NameError as e:
            print(e, "插入出错")
        finally:
            cur.close()
            conn.close()


def select_relation():
    '''
    从数据库中拿到所有关系
    :return: [[a,b],[c,d]....]
    '''
    relation = []
    try:
        conn = pymysql.connect(host=host, user=user, passwd=password,
                               db=db, charset='utf8', port=port)  # 默认为127.0.0.1本地主机
        cur = conn.cursor()

        cur.execute(
            "SELECT p1.name AS fname,p2.name AS tname FROM relation AS r  LEFT JOIN problem AS p1 ON p1.`id`=r.`fpid`LEFT JOIN problem AS p2 ON p2.`id`=r.`tpid`")
        conn.commit()
        fr = cur.fetchall()
        for each in fr:
            relation.append([each[0], each[1]])
        return relation
    except NameError as e:
        print(e, "查询错误")
    finally:
        cur.close()
        conn.close()


def read_relation():
    '''
    从NPC_relation.txt文件中读取关系
    :return:
    '''
    try:
        with open("../NPC_relation.txt", "r", encoding='UTF-8') as f:
            relation = []
            temp = f.readline()
            while temp:
                relation.append(temp.replace("\n", "").split(" "))
                temp = f.readline()
    except NameError as e:
        print(e, "读取出错")
    return relation


def insert_relation():
    '''
    插入新关系
    :return:
    '''
    relation1 = select_relation()
    relation2 = read_relation()
    relation = get_d_set(relation1,relation2)
    if relation:
        try:
            conn = pymysql.connect(host=host, user=user, passwd=password,
                                   db=db, charset='utf8', port=port)  # 默认为127.0.0.1本地主机
            cur = conn.cursor()
            data = ""
            for re in relation:
                sql = "insert into relation(fpid,tpid) SELECT p1.`id` ,p2.`id` FROM problem AS p1 ,problem AS p2 WHERE p1.`name`  = \'{}\' AND p2.`name` = \'{}\'".format(re[0],re[1])
                cur.execute(sql)
            print(data)
            conn.commit()
        except NameError as e :
            print(e,"insert_relation error")
        finally:
            cur.close()
            conn.close()
def get_d_set(relation1,relation2):
    '''
    得到双重数组的差集
    :param relation1:
    :param relation2:
    :return: relation
    '''
    relation = []
    # 求差集 r1-r2
    for r2 in relation2:
        for r1 in relation1:
            # print(r1,r2,r1==r2)
            if (r1 == r2):
                flag = True
        # print(flag)
        if flag == False:
            relation.append(r2)
        else:
            flag = False
    return relation


if __name__ == '__main__':
    # insert_into_inital_data()
    # words1 = get_problem_name()
    # print(words1)
    # words2 = select_problem_name()
    # print(words2)
    # words = subtraction = list(set(words1).difference(set(words2)))
    # print(words)
    # insert_problem()
    relation1 = select_relation()
    relation2 = read_relation()
    flag = False

    # print(get_d_set(relation1,relation2))
    insert_relation()