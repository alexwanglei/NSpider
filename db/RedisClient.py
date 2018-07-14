#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : RedisClient.py
# @Author: Wanglei
# @Date  : 2018/5/2
# @Desc  :
import random
import redis

class RedisClient:
    def __init__(self, name, host, port, passwd):
        self.name = name
        self._coon = redis.Redis(host=host, port=port, db=0, password=passwd)



    def get(self):
        r = self._coon.hgetall(name=self.name)
        key = random.choice(list(r.keys())) if r else None
        if isinstance(key, bytes):
            return key.decode('utf-8')
        else:
            return key



    def put(self, key):
        return self._coon.hincrby(self.name, key, 1)


    def delete(self, key):
        self._coon.hdel(self.name, key)

    def delete_all(self):
        for key in self._coon.hgetall(self.name).keys():
            self._coon.hdel(self.name, key)


    def nums(self):
        return self._coon.hlen(self.name)

    def get_all(self):
        return [key.decode('utf-8') for key in self._coon.hgetall(self.name).keys()]

    def changeTable(self, name):
        self.name = name

if __name__ == "__main__":
    client = RedisClient("gatherproxy", '101.200.38.103', 6379, 'fromtrain!QAZ')
    # client.put('123.115.235.221:8800')
    # client.put('123.115.235.221:8801')
    # client.put('123.115.235.221:8800')
    print(client.get())
    print(client.nums())
    print(client.get_all())
