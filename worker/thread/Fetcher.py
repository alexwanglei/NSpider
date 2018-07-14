from threading import Thread
import os
import ssl
import time
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import random
from collections import namedtuple
from task.Task import ParserTask
from db.RedisClient import RedisClient
import config
import logging

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# context = ssl._create_unverified_context()

fetch_ret = namedtuple('FetchRet', ['code', 'task'])

logger = logging.getLogger()

class HeaderFactory:
    def __init__(self, host, agent_file):
        self.host = host
        self.user_agent_list = []
        file = os.path.join(config.ROOT_PATH, agent_file)
        with open(file, "r") as f:
            for line in f:
                self.user_agent_list.append(line.strip())

    def get_header(self):
        user_agent = random.choice(self.user_agent_list)
        headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Host': self.host,
            'User-Agent': user_agent
        }
        return headers

class ProxyFactory:
    def __init__(self):
        self.db = RedisClient(config.NAME, config.HOST, config.PORT, config.PASSWORD)

    def get_proxy(self):
        res = self.db.get()
        proxies = {"http": "http://{proxy}".format(proxy=res)}
        return proxies

    def del_proxy(self, proxies):
        key = proxies['http'].split("//")[1]
        print(key)
        return self.db.delete(key)




class Fetcher(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self._running = True
        self.master = master
        self.header_factory = HeaderFactory("kyfw.12306.cn", "user_agent.txt")
        self.proxy_factory = ProxyFactory()

    def stop(self):
        self._running = False

    def run(self):
        logger.info("start fether thread %s at %s" % (self.name, time.strftime('%H:%M:%S')))
        while self._running:
            fetch_task = self.master.fetch_task_queue.get()

            fetch_ret = self.fetch(fetch_task)

            # logger.info(fetch_ret)

            if fetch_ret.code == 1:
                self.master.parse_task_queue.put(fetch_ret.task)
            else:
                logger.info("fetch fail: %s", fetch_ret)
                self.master.fetch_task_queue.put(fetch_task)

            self.master.fetch_task_queue.task_done()


    def fetch(self, task):
        logger.info("fetch task: %s" % task)
        headers = self.header_factory.get_header()
        # logger.info("headers: %s" % headers)
        proxies = self.proxy_factory.get_proxy()
        # logger.info("proxies: %s" % proxies)
        time.sleep(random.randint(1,3))
        try:
            response = requests.get(url=task.url, headers=headers, proxies=proxies, cookies=None, timeout=(5, 10), verify=False)
            if response.status_code == 200:
                parse_task = ParserTask(task.url_id, response.text)
                return fetch_ret(1, parse_task)
            else:
                return fetch_ret(0, None)
        except Exception as excep:
            print("fetch exception:", excep)
            self.proxy_factory.del_proxy(proxies)
            logger.info("delete proxy: %s" % proxies)
            return fetch_ret(0, None)




if __name__ == "__main__":
    print(config.ROOT_PATH)