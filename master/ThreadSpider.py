from master.Spider import Spider
from worker.thread import Fetcher, Parser, Saver, Monitor
from task.Task import FetchTask, ParserTask, SaverTask
from db.MysqlClient import MysqlClient
import config
import time
import logging


logger = logging.getLogger()


class ThreadSpider(Spider):
    def __init__(self, fetcher_nums=10, parser_nums=1, saver_nums=1):
        Spider.__init__(self)
        self.fetcher_list = [Fetcher("fetcher-%d" % i, self) for i in range(fetcher_nums)]
        self.parser_list = [Parser("parser-%d" % i, self) for i in range(parser_nums)]
        self.saver_list = [Saver("saver-%d" % i, self) for i in range(saver_nums)]

        self.monitor = Monitor("monitor", self)
        self.monitor.setDaemon(True)
        self.monitor.start()




    def run(self):
        thread_list = self.fetcher_list + self.parser_list + self.saver_list
        for thread in thread_list:
            thread.start()

        for thread in thread_list:
            if thread.is_alive():
                thread.join()

        # self.fetch_task_queue.join()


        return





if __name__ == "__main__":
    start = time.time()
    spider = ThreadSpider()
    spider.run()

    end = time.time()
    print(end - start)






