# coding: utf-8
from master import ThreadSpider
import time
import logging.config
import config

logging.config.dictConfig(config.LOGCONFIG)

if __name__ == "__main__":
    start = time.time()
    spider = ThreadSpider()

    spider.run()

    end = time.time()
    print(end - start)
