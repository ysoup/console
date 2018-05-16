# encoding=utf-8
import redis
import json

# 读取配置文件
with open("../config/crawler.json", "r") as fi:
    load_dict = json.load(fi)


def connetcredis():
    if load_dict.__contains__('redis'):
        for x in load_dict["redis"]:
            if x["name"] == "spider":
                pool = redis.ConnectionPool(host=x["host"][0], port=x["port"], decode_responses=True)
                r = redis.Redis(connection_pool=pool)
    return r
