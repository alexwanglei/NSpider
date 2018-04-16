from threading import Thread
import time
import requests
import random
from collections import namedtuple
from task.Task import ParserTask

fetch_result = namedtuple('FetchResult', ['code', 'task'])

class HeaderFactory:
    def __init__(self, host, config):
        self.host = host
        self.config = config

    def get_header(self):
        user_agent_list = []
        with open(self.config) as f:
            for line in f:
                user_agent_list.append(line.strip())

        user_agent = random.choice(user_agent_list)
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'close',
            'Host': self.host,
            'User-Agent': user_agent
        }
        return headers




class Fetcher(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self.master = master
        self.header_factory = HeaderFactory("www.lagou.com", "user_agent.txt")

    def run(self):
        print("start fether thread %s at %s \n" % (self.name, time.strftime('%H:%M:%S')))
        while True:
            fetch_task = self.master.fetch_task_queue.get()
            # try:
            fetch_result = self.fetch(fetch_task)
            print(fetch_result)
            # except Exception as excep:
            #     print("fetch exception:", excep)
            if fetch_result.code == 1:
                self.master.parse_task_queue.put(fetch_result.task)
            else:
                print(fetch_result)
                # self.master.fetch_task_queue.put(fetch_task)
            self.master.fetch_task_queue.task_done()


    def fetch(self, task):
        print("fetch task: %s \n" % task)
        headers = self.header_factory.get_header()
        print("headers: %s" % headers)
        time.sleep(1)
        response = requests.get(url=task.url, headers=headers, cookies=None, timeout=(3, 10))
        if response.status_code == 200:
            parse_task = ParserTask(response.text)
            return fetch_result(1, parse_task)
        else:
            return fetch_result(0, None)


