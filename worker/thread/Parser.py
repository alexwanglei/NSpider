# coding=utf-8
from threading import Thread
import time
from bs4 import BeautifulSoup
import logging
import json
from collections import namedtuple
from task.Task import SaverTask
from db.MysqlClient import MysqlClient
import config

parse_ret = namedtuple('ParseRet', ['code', 'task'])

train_info = namedtuple("trainInfo", ['train_no',
                                                    'train_code',
                                                    'start_station_telecode',
                                                    'end_station_telecode',
                                                    'start_time',
                                                    'arrive_time',
                                                    'lishi',
                                                    'controlled_train_flag'])

logger = logging.getLogger()

class Parser(Thread):
    def __init__(self, name, master):
        Thread.__init__(self, name=name)
        self.master = master
        self.db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                                     config.mysql_db, config.mysql_charset)

    def run(self):
        logger.info("start parser thread %s at %s" % (self.name, time.strftime('%H:%M:%S')))
        time.sleep(1)
        while True:
            parse_task = self.master.parse_task_queue.get()
            parse_ret = self.parse(parse_task)

            if parse_ret.code:
                self.master.save_task_queue.put(parse_ret.task)
            # else:
            #     logger.info("parse task failed: %s", parse_task)
                # self.master.parse_task_queue.put(parse_task)

            self.master.parse_task_queue.task_done()


    def parse(self, parse_task):
        # logger.info("parse task %s" % parse_task)
        try:
            save_task = self.parse_train(parse_task.raw)
            if save_task:
                return parse_ret(1, save_task)
            else:
                # url 页面内容为空
                return parse_ret(0, None)
        except Exception as excep:
            print("parse exception:", excep)
            logger.debug("parse task %s" % parse_task)
            return parse_ret(0, None)




    def parse_train(self, text):
        train_list = []
        content = json.loads(text)
        logger.info(content)
        result = content['data']['result']
        for item in result:
            fields = item.split('|')
            logger.info(u"车次信息TrainInfo result=%s" % fields)
            # logger.info(u"fields num: %d", len(fields))
            # secretStr = fields[0]
            # buttonTextInfo = fields[1]
            train_no = fields[2]  # 车次号
            train_code = fields[3]  # 车次码
            start_station_telecode = fields[4]
            end_station_telecode = fields[5]
            from_station_telecode = fields[6]
            to_station_telecode = fields[7]
            start_time = fields[8]
            arrive_time = fields[9]
            lishi = fields[10]
            # canWebBuy = fields[11]
            # yp_info = fields[12]
            # start_train_date = fields[13]
            # train_seat_feature = fields[14]
            # location_code = fields[15]
            # from_station_no = fields[16]
            # to_station_no = fields[17]
            # is_support_card = fields[18]
            controlled_train_flag = fields[19]      # 是否停运
            # gg_num = fields[20]
            # gr_num = fields[21]         # 高级软卧
            # qt_num = fields[22]         # 其他
            # rw_num = fields[23]         # 软卧
            # rz_num = fields[24]         # 软座
            # tz_num = fields[25]
            # wz_num = fields[26]         # 无座
            # yb_num = fields[27]
            # yw_num = fields[28]         # 硬卧
            # yz_num = fields[29]         # 硬座
            # ze_num = fields[30]         # 二等座
            # zy_num = fields[31]         # 一等座
            # swz_num = fields[32]        # 商务座
            # dw_num = fields[33]         # 动卧
            # yp_ex = fields[34]
            # seat_types = fields[35]
            # is_exchange = fields[36]

            if start_station_telecode == from_station_telecode and end_station_telecode == to_station_telecode:
                train = (train_no, train_code, start_station_telecode, end_station_telecode, start_time, arrive_time, lishi, controlled_train_flag)
                train_list.append(train)
        if train_list:
            save_task = SaverTask(train_list)
        else:
            save_task = None
        return save_task







if __name__ == "__main__":
    text = "GajNLCp4tMLtV%2FJ2tNZqxM0NVXZfQHfz%2B155Tgf10qSIvlB9pV3eyZ4LcpzHeYJc3WnPsKpATFKs%0Aw3cQHgN3sA%2ByCX%2FozlooqLG3KQ9dB3GFTxIMuqMdc2rf4REmxy9DS0DciyQWn9vBLF8qfEBbJDz8%0AkatmAXMKZHla0orFL9Hh6i6QCdbg42S3Doq%2BRhtXBPAP9DSbUiSwdpuWnBrzXmcWOXLybksGcoVs%0A1R5unD1Ow0Is|预订|240000D3110L|D311|VNP|SHH|VNP|SHH|21:17|09:15|11:58|Y|3L7G%2FKDpggxgSMaL8obo7S8%2FoFy%2BtDr9|20180701|3|P2|01|04|0|0||||无||||||||||有|F040|F4|1"
    fields = text.split('|')
    for i in enumerate(fields):
        print(i)

    print(len(fields))