from threading import Thread
import time
from bs4 import BeautifulSoup

class Parser(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self.master = master

    def run(self):
        print("start parser thread %s at %s \n" % (self.name, time.strftime('%H:%M:%S')))
        time.sleep(1)
        while True:
            parse_task = self.master.parse_task_queue.get()
            parse_result = self.parse(parse_task)
            print(parse_result)

            if parse_result:
                self.master.save_task_queue.put(parse_result)

            self.master.parse_task_queue.task_done()


    def parse(self, parse_task):
        print("parse task %s\n" % parse_task)
        soup = BeautifulSoup(parse_task.raw)

