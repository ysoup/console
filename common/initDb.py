# encoding=utf-8

from peewee import *
import json
from common.initlog import Logger

# 读取配置文件
with open("../config/crawler.json", "r") as fi:
    load_dict = json.load(fi)


class InitDb(object):
    def __init__(self, database):
        if load_dict.__contains__('db'):
            for db_dict_key in load_dict["db"]:
                key = load_dict["db"]["%s" % db_dict_key]
                if db_dict_key == database:
                    self.database = key["database"]
                    self.host = key["host"]
                    self.password = key["password"]
                    self.port = key["port"]
                    self.user = key["user"]
                    self.charset = key["charset"]
                    self.dblogger = key["logger"]

    def connect(self):
        init_database = MySQLDatabase(self.database, **{'host': self.host, 'password': self.password, 'port': self.port,
                                                        'user': self.user, 'charset': self.charset})
        return init_database

    def wirte_logger(self):
        Logger(self.dblogger)



