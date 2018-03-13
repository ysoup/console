# encoding=utf-8
import logging
from common.constants import CrawlerLogName
import json

# 读取配置文件
with open("../config/crawler.json", "r") as fi:
    load_dict = json.load(fi)


class Logger(object):
    def __init__(self, path=None, kind=None, name=CrawlerLogName.OPERTATION_PEEWEE_MODEL.value):
        if load_dict.__contains__('log'):
            for log_dict_key in load_dict["log"]:
                key = load_dict["log"]["%s" % log_dict_key]
                if log_dict_key == name:
                    path =key["%s" % kind]
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        fh = logging.FileHandler(path)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # 设置日志格式
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)
        # 将相应的handler添加在logger对象中
        self.logger.addHandler(ch)
        self.logger.addHandler(fh)

    def debug(self, message):
        self.logger.debug(message)

    def info(self, message):
        self.logger.info(message)

    def war(self, message):
        self.logger.warn(message)

    def error(self, message):
        self.logger.error(message)

    def cri(self, message):
        self.logger.critical(message)


