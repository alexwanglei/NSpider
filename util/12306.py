#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : 12306.py
# @Author: Wanglei
# @Date  : 2018/5/8
# @Desc  :
import requests
import time
import re
from db.MysqlClient import MysqlClient
import config
import json


station_index_url = 'https://kyfw.12306.cn/otn/leftTicket/init'
train_index_url = "https://kyfw.12306.cn/otn/queryTrainInfo/init"
station_name = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?station_version=1.9053'
stop_stations = 'https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=93000K150420&from_station_telecode=WMR&to_station_telecode=CXW&depart_date=2018-06-25'
left_ticket = 'https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=2018-06-28&leftTicketDTO.from_station=YIJ&leftTicketDTO.to_station=BJP&purpose_codes=ADULT'


def get_train_list(url):
    '''
    获取车次列表
    :param url:
    :return:
    '''
    resp = requests.get(url)
    if resp.ok:
        content = resp.text

        train_list_version = re.findall(r'train_list.js\?scriptVersion=[\d\.]*', content)[0]
        print(train_list_version)
        train_list_url = "https://kyfw.12306.cn/otn/resources/js/query/" + train_list_version
        print(train_list_url)
        resp = requests.get(train_list_url)
        if resp.ok:
            content = json.loads(resp.text.split("=")[1])
            print(len(content))
            for k, v in content.items():
                sum = 0
                date = k
                data = v
                print(date)
                filename = date + ".json"
                with open("../train_list/" + filename, "w") as file:
                    json.dump(data, file, ensure_ascii=False,indent=4)
                for label, trains in data.items():
                    print(label + ":" + str(len(trains)))
                    sum += len(trains)
                print("total train: %d" % sum)








def get_station_name(url):
    '''
    获取车站文件
    :param url:
    :return:
    '''
    # station_list = []
    resp = requests.get(url)
    if resp.ok:
        content = resp.text
        station_version = re.findall(r"station_version=[\d\.]*", content)[0]
        print(station_version)
        station_url = 'https://kyfw.12306.cn/otn/resources/js/framework/station_name.js?' + station_version
        print(station_url)
        resp = requests.get(station_url)
        if resp.ok:
            content = resp.text.split("'")[1]
            station_list = content.split('@')[1:]
            print(len(station_list))
            print(station_list[:10])
            filename = station_version + ".txt"
            station_file = open("../" + filename, "w", encoding="utf-8")
            for item in station_list:
                line = "\t".join(item.split('|')) + "\n"
                station_file.write(line)



def temp():
    station_city = {}
    with open("../stations.txt", "r", encoding="utf-8") as file:
        for line in file:
            fields = line.split()
            city = fields[1]
            code = fields[2]
            # print(city + ":" + code)
            station_city[city] = code

    location = []
    with open("../main_city.txt", "r", encoding="utf-8") as file:
        for line in file:
            location.append((line.split()[0], line.split()[1]))


    with open("../temp.txt", "r", encoding="utf-8") as file:
        for line in file:
            city = line.split("#")[0]
            # print(city)
            code = station_city.get(city)
            if code:
                t = (city, code)
                if t not in location:
                    location.append(t)

    with open("../main_city.txt", "w", encoding="utf-8") as file:
        for i in location:
            file.write(i[0] + "\t" + i[1] + "\n")


def get_station_code():
    '''
    返回车站编码字典
    :return:
    '''
    station_code = {}
    with open("../stations_station_version=1.9058.txt", "r", encoding="utf-8") as file:
        for line in file:
            # TODO 处理异常
            fields = line.split("\t")
            city = fields[1]
            code = fields[2]
            # print(city + ":" + code)
            station_code[city] = code
    return station_code





def station_to_city(station):
    '''
    车站名转城市
    :param station:
    :return:
    '''
    if len(station) < 3:
        return station
    elif station[0:2] == u"上海":
        return station[0:2]
    elif station[-1] in {u"东", u"南", u"西", u"北"}:
        return station[:-1]
    else:
        return station



def gen_train_crawl_url():
    '''
    生成要爬取的url
    :return:
    '''
    station_code = get_station_code()
    from_to_code = []
    filename = config.CRAWL_DATE + ".json"
    with open("../train_list/" + filename, "r") as file:
        data = json.load(file)
    for k, v in data.items():
        for item in v:
            fields = re.split(r'[(\-)]', item['station_train_code'])
            station_train_code = fields[0]
            from_station = fields[1]
            to_station = fields[2]
            train_no = item['train_no']

            from_station_code = station_code.get(from_station)

            to_station_code = station_code.get(to_station)
            if from_station_code and to_station_code:
                t = (from_station_code, to_station_code)
                # print(t)
                if t not in from_to_code:
                    from_to_code.append(t)
            else:
                print("can not find code: %s and %s" % (from_station, to_station))
                print("from station code: %s, to station code: %s" % (from_station_code, to_station_code))
    print(len(from_to_code))

    # 建表
    db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password, config.mysql_db, config.mysql_charset)
    table_name = config.TABLE_NAME['url']
    sql = "CREATE TABLE IF NOT EXISTS %s(id INT PRIMARY KEY AUTO_INCREMENT, url VARCHAR(256) DEFAULT NULL, crawled TINYINT DEFAULT '0', type VARCHAR(32) DEFAULT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8" % table_name
    db_client.execute(sql)
    # 车次url数据
    for item in from_to_code:
        url = "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date=%s&leftTicketDTO.from_station=%s&leftTicketDTO.to_station=%s&purpose_codes=ADULT" % (config.CRAWL_DATE, item[0], item[1])
        # print(url)
        sql = "INSERT INTO %s (`url`, `type`) VALUES ('%s', '%s')" % (table_name, url, "train")
        # print(sql)
        db_client.execute(sql)
    db_client.close()



def gen_station_crawl_url():
    '''
    生成车次停靠站url
    :return:
    '''
    db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                            config.mysql_db, config.mysql_charset)


    sql = "SELECT train_no, start_station_telecode, end_station_telecode FROM %s" % (config.TABLE_NAME['train'])
    db_client._cursor.execute(sql)
    result = db_client._cursor.fetchall()
    for item in result:
        url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s" % (item[0], item[1], item[2], config.CRAWL_DATE)
        print(url)
        sql = "INSERT INTO %s (`url`, `type`) VALUES ('%s', '%s')" % (config.TABLE_NAME['url'], url, "station")
        print(sql)
        db_client.execute(sql)

    db_client.close()





def build_table():
    db_client = MysqlClient(config.mysql_host, config.mysql_port, config.mysql_user, config.mysql_password,
                            config.mysql_db, config.mysql_charset)
    train_table_name = config.TABLE_NAME['train']
    train_table_sql = "CREATE TABLE IF NOT EXISTS %s ( " \
          "`id` int(11) NOT NULL AUTO_INCREMENT," \
          "`train_no` varchar(16)  NOT NULL," \
          "`train_code` varchar(8) DEFAULT NULL," \
          "`start_station_telecode` varchar(8) DEFAULT NULL," \
          "`end_station_telecode` varchar(8) DEFAULT NULL," \
          "`start_time` varchar(16) DEFAULT NULL," \
          "`arrive_time` varchar(16) DEFAULT NULL," \
          "`lishi` varchar(16) DEFAULT NULL," \
          "`controlled_train_flag` tinyint(11) DEFAULT NULL," \
          "PRIMARY KEY (`id`)" \
          ") ENGINE=InnoDB DEFAULT CHARSET=utf8;" % train_table_name

    db_client.execute(train_table_sql)

    station_table_name = config.TABLE_NAME['station']
    station_table_sql = "CREATE TABLE IF NOT EXISTS %s (" \
                        "`id` int(11) NOT NULL AUTO_INCREMENT," \
                        "`train_no` varchar(16) NOT NULL," \
                        "`arrive_time` varchar(8) DEFAULT NULL," \
                        "`station_name` varchar(32) DEFAULT NULL," \
                        "`start_time` varchar(8) DEFAULT NULL," \
                        "`stopover_time` varchar(16) DEFAULT NULL," \
                        "`station_no` varchar(4) DEFAULT NULL," \
                        "`distance` int(11) DEFAULT NULL," \
                        "PRIMARY KEY (`id`)" \
                        ") ENGINE=InnoDB DEFAULT CHARSET=utf8;" % station_table_name
    db_client.execute(station_table_sql)
    db_client.close()







def stat_pcr_data():
    with open("../province_city_region.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        print("provice num: %d", len(data))

        city_sum_num = 0
        for prov_id, prov_value in data.items():
            print("%s:%s" % (prov_id, prov_value['name']))
            city_num = len(prov_value['child'])
            city_sum_num += city_num
            city_list = []
            for city_id, city_value in prov_value['child'].items():
                city_list.append(city_value['name'])
            print("%d city: %s" % (city_num, city_list))
            print("sum city num: %d", city_sum_num)





if __name__ == "__main__":
    start = time.time()
    # get_station_name(station_index_url)
    # get_train_list(train_index_url)
    # gen_train_crawl_url()
    # get_station_code()
    # stat_pcr_data()
    # build_table()
    gen_station_crawl_url()
    end = time.time()
    print(end-start)

