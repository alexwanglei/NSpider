#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : config.py
# @Author: Wanglei
# @Date  : 2018/4/29
# @Desc  :
import os
from configparser import ConfigParser

MINNUM_PROXY = 100  # 当有效的代理数目小于该值 需要启动爬虫进行爬取

PAGE_PROXY = 10

FLUSH_TIME = 600   # 刷新代理的周期

'''
数据库的配置
'''
HOST = "101.200.38.103"
PORT = 6379
NAME = "gatherproxy"
PASSWORD = "fromtrain!QAZ"

DB_CONFIG = {
    'MYSQL_DB_URL': 'mysql+mysqldb://root:root@localhost/proxy?charset=utf8',
    'REDIS_DB_URL': 'redis://:fromtrain!QAZ@101.200.38.103:6379/9',
}


mysql_host="101.200.38.103"
mysql_port=3306
mysql_db="dev_ticket"
mysql_user="dev"
mysql_password="dev@WSX"
mysql_charset="utf8mb4"

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

CRAWL_DATE = "2018-07-07"

TABLE_NAME = {
    "url": "crawler_url_" + CRAWL_DATE.replace("-", ""),
    "train": "crawler_train_info_" + CRAWL_DATE.replace("-", ""),
    "station": "crawler_stop_station_" + CRAWL_DATE.replace("-", "")
}



MAX_DOWNLOAD_CONCURRENT = 10
PROXY_MINNUM = 500
UPDATE_TIME = 30 * 60

CHECK_TARGET = 'https://kyfw.12306.cn/otn/leftTicket/init'



LOGCONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(name)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'stream': 'ext://sys.stderr'
        },
        'info_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'INFO',
            'formatter': 'default',
            'filename': 'log/info.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf8'
        },
        'debug_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'default',
            'filename': 'log/debug.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf8'
        },
        'error_file_handler': {
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'default',
            'filename': 'log/error.log',
            'when': 'D',
            'interval': 1,
            'backupCount': 10,
            'encoding': 'utf8'
        }
    },
    'loggers': {
        'proxy': {
            'handlers': ['console'],
            'level': 'DEBUG'
        },
        'crawl': {
            'handlers': ['debug_file_handler', 'error_file_handler'],
            'level': 'DEBUG'
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console', 'info_file_handler']
    }
}



"""
12306
"""


class Config:
    def __init__(self):
        self.pwd = os.path.split(os.path.realpath(__file__))[0]
        self.config_path = os.path.join(self.pwd, 'dev.cfg')
        self.config_file = ConfigParser()
        self.config_file.read(self.config_path)


    def proxy_getter_funs(self):
        return self.config_file.options('ProxyGetter')


if __name__ == "__main__":
    config = Config()
    print(config.pwd)