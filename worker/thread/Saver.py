from threading import Thread
import time
import logging
from db.MysqlClient import MysqlClient
import config


logger = logging.getLogger()



class Saver(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self.master = master
        self.db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                                config.mysql_db, config.mysql_charset)

    def run(self):
        print("start saver thread %s at %s \n" % (self.name, time.strftime('%H:%M:%S')))
        time.sleep(1)

        while True:
            save_task = self.master.save_task_queue.get()
            save_ret = self.save(save_task)
            # logger.info("save ret %s" % save_ret)

            if save_ret:
                logger.info("save success")
            else:
                logger.info("save task failed: %s" % save_task)

            self.master.save_task_queue.task_done()


    def save(self, save_task):
        try:
            self.save_train(save_task.results)
            return 1
        except Exception as excep:
            print("save exception:", excep)
            return 0


    def save_train(self, train_list):
        for train in train_list:
            logger.info("save train: %s", train)
            sql = "SELECT * FROM %s WHERE train_code='%s'" % (config.TABLE_NAME['train'], train[1])
            self.db_client._cursor.execute(sql)
            result = self.db_client._cursor.fetchone()
            if not result:
                sql = "INSERT INTO %s (train_no, train_code, start_station_telecode, end_station_telecode, start_time, arrive_time, lishi, controlled_train_flag) VALUES ('%s','%s','%s','%s','%s','%s','%s','%s')" % ((config.TABLE_NAME['train'], ) + train)
                self.db_client.execute(sql)


if __name__ == "__main__":
    pass