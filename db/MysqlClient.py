#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : MysqlClient.py
# @Author: Wanglei
# @Date  : 2018/6/25
# @Desc  :


import pymysql
import config

class MysqlClient:
    def __init__(self, host, port, user, passwd, db, charset):
        self._coon = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=db, charset=charset)
        self._cursor = self._coon.cursor()


    def execute(self, sql):
        self._cursor.execute(sql)
        self._coon.commit()


    def close(self):
        self._cursor.close()
        self._coon.close()





if __name__ == "__main__":
    db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                            config.mysql_db, config.mysql_charset)
    print(db_client)