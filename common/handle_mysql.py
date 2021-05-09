"""
======================================
Author:包天宇
Time:2021-04-24 22:57
E-mail:uattb991492@icccuat.com
======================================
"""
import pymysql


class HandleSql:

    def __init__(self, host='api.lemonban.com', port=3306, user='future', password='123456', *args, **kwargs):
        # 连接数据库
        self.con = pymysql.connect(host=host,
                                   port=port,
                                   user=user,
                                   password=password,
                                   charset='utf8',
                                   # cursorclass=pymysql.cursors.DictCursor (设置游标对象返回的数据类型（字典） # 默认是元组)
                                   )

    def find_all(self, sql: str):
        """
        查询查询到的所有数据
        :param sql: 输入的sql
        :return: 返回所有的数据,返回的结果为 ((字段1，字段2....),(字段1，字段2....),(字段1，字段2....))
        """
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchall()
        cur.close()
        return res

    def find_one(self, sql: str):
        """
        获取查询集中的第一条数据
        :param sql: 输入的sql
        :return: 返回一条数据，返回的结果为（字段1，字段2....）
        """
        with self.con as cur:
            cur.execute(sql)
        res = cur.fetchone()
        cur.close()
        return res

    def find_count(self, sql: str):
        """
        sql执行完之后，返回的数据条数
        :param sql: 输入的sql
        :return:  返回数据的条数
        """
        with self.con as cur:
            res = cur.execute(sql)
        cur.close()
        return res


if __name__ == '__main__':
    mysql = HandleSql()
    res = mysql.find_count(sql='select * from futureloan.financelog limit 10;')
    print(res)
