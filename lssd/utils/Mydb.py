#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Created by mark.huang on 2017/12/25.

import pymysql.cursors


class Mydb():
    def __init__(self, host, user_name, password, db_name, charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor):
        self.host = host
        self.user_name = user_name
        self.password = password
        self.db_name = db_name
        self.charset = charset
        self.cursorclass = cursorclass

    def serach_info(self, sql, count='all'):
        """
        查询数据
        :param sql: "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
        :param count: 获取一条值为one,获取所有值为all,获取一部分可以填要获取的数字如'30'.默认为all
        :return:
        """
        connection = pymysql.connect(host=self.host, user=self.user_name, password=self.password, db=self.db_name,
                                     charset=self.charset, cursorclass=self.cursorclass)
        result = []
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                if count == 'all':
                    result = cursor.fetchall()
                elif count == 'one':
                    result = cursor.fetchone()
                else:
                    result = cursor.fetchmany(size=int(count))

        finally:
            connection.close()
            return result

    def insert_data(self, sql):
        """
        新增数据
        :param sql:  "INSERT INTO `users` (`email`, `password`) VALUES (%s, %s)"
        :return:
        """
        connection = pymysql.connect(host=self.host, user=self.user_name, password=self.password, db=self.db_name,
                                     charset=self.charset, cursorclass=self.cursorclass)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()
        finally:
            connection.close()

    def delete_data(self, sql):
        """
        删除数据
        :param sql: "DELETE FROM `users` WHERE `username`=`mark.huang`"
        :return:
        """
        connection = pymysql.connect(host=self.host, user=self.user_name, password=self.password, db=self.db_name,
                                     charset=self.charset, cursorclass=self.cursorclass)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()

        finally:
            connection.close()

    def update_data(self, sql):
        """
        更新数据
        :param sql: "DELETE FROM `users` WHERE `username`=`mark.huang`"
        :return:
        """
        connection = pymysql.connect(host=self.host, user=self.user_name, password=self.password, db=self.db_name,
                                     charset=self.charset, cursorclass=self.cursorclass)
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
            connection.commit()

        finally:
            connection.close()


def main():
    mydb = Mydb(host='xx', user_name='root', password='xx', db_name='lssd_test1')
    search_sql = "SELECT `display_name` FROM tms_user"
    result = mydb.serach_info(search_sql, count='one')
    # print result
    insert_sql = "INSERT INTO `tms_user` (`username`,`display_name`) VALUES (%s,%s)" % ("'nick'", u"'虚拟姓名'")
    # mydb.insert_data(insert_sql)
    # delete_sql = "DELETE FROM `tms_user` WHERE `username`=%s"%"'nick'"
    # mydb.delete_data(delete_sql)
    # update_sql = "UPDATE `tms_user` SET `display_name`='哈哈哈哈哈' WHERE `username`='nick'"
    # mydb.update_data(update_sql)


if __name__ == '__main__':
    main()
