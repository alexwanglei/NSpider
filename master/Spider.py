from queue import Queue
from worker.thread import *

class Spider:
    def __init__(self):
        # 种子url

        # 抓取任务队列
        self.fetch_task_queue = Queue()
        # 解析任务队列
        self.parse_task_queue = Queue()
        # 保存结果队列
        self.save_task_queue = Queue()








