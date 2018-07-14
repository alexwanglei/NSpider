#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : Monitor.py
# @Author: Wanglei
# @Date  : 2018/6/28
# @Desc  :

from threading import Thread
import time
import logging
import config
from db.MysqlClient import MysqlClient
from task.Task import FetchTask

logger = logging.getLogger()

class Monitor(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self.master = master
        self.start_index = 0
        self.batch_num = 100

    def run(self):
        print("start monitor thread %s at %s \n" % (self.name, time.strftime('%H:%M:%S')))
        while True:
            self.monitoring()



    def monitoring(self):
        fetch_task_num = self.master.fetch_task_queue.qsize()
        parse_task_num = self.master.parse_task_queue.qsize()
        save_task_num = self.master.save_task_queue.qsize()
        logger.info("****************************************************************")
        logger.info("Fetch task num:%d, Parse task num:%d, Save task num:%d" % (fetch_task_num, parse_task_num, save_task_num))

        if fetch_task_num == 0:
            if self.feed_fetch_task(config.TABLE_NAME['url'], "train", self.start_index, self.batch_num):
                self.start_index += self.batch_num
        time.sleep(10)



    def feed_fetch_task(self, table_name, task_type, start_index, batch_num):
        logger.info("feed fetch task: table_name=%s, task_type=%s, start_index=%d, batch_num=%d" % (table_name, task_type, start_index, batch_num))
        db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                                config.mysql_db, config.mysql_charset)
        sql = "SELECT id, url, crawled from %s WHERE type='%s' and id >= %d limit %d" % (table_name, task_type, start_index, batch_num)
        db_client._cursor.execute(sql)
        result = db_client._cursor.fetchall()

        if result:
            for item in result:
                if item[2] == 0:
                    id = item[0]
                    url = item[1]
                    task = FetchTask(id, url, task_type)
                    self.master.fetch_task_queue.put(task)
            return 1
        else:
            return 0