from threading import Thread
import time

class Saver(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self.master = master

    def run(self):
        print("start saver thread %s at %s \n" % (self.name, time.strftime('%H:%M:%S')))
        time.sleep(1)