#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
from warnings import filterwarnings

# 忽略mysql警告信息
filterwarnings("ignore", category=pymysql.Warning)


class DoMySQL:

    def __init__(self):
        # 连接数据库
        self.conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="root", db="spider_data", charset="utf8")

        # 使用 cursor() 方法操作游标，得到一个可以执行的sql语句，并且操作结果作为字典返回的游标
        self.cur = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def __del__(self):
        # 关闭游标
        self.cur.close()
        # 关闭连接
        self.conn.close()

    # 查询
    def query(self, sql):

        self.cur.execute(sql)
        data = self.cur.fetchall()

        return data

    # 更新、删除
    def update(self, sql):
        # 使用execute() 方法执行sql
        self.cur.execute(sql)

        # 提交事务
        self.conn.commit()


if __name__ == '__main__':
    mydb = DoMySQL()

    sql = '''INSERT INTO spider_data.`51_job_info` (job_id, titile, company_name, city, experience, certificate, numbers,release_date, tags, job_info, detail_url)
    VALUES ('2', '2', '2', '2', '2', '2', '2', '2', '2', '2', '2');'''
    # sql = "select * from `51_job_info`;"
    mydb.update(sql)

