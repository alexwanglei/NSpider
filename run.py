# coding: utf-8
from master import ThreadSpider

if __name__ == "__main__":
    spider = ThreadSpider()
    spider.setup_fetch_task(["https://www.lagou.com/zhaopin/Python/?labelWords=label"])
    spider.run()
