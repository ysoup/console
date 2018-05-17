# encoding=utf-8
import redis
import json

# 读取配置文件
with open("../config/crawler.json", "r") as fi:
    load_dict = json.load(fi)


def connetcredis():
    global host
    global port
    if load_dict.__contains__('redis'):
        x = load_dict["redis"][0]
        if x["name"] == "spider":
            host = x["host"][0]
            port = x["port"]
    pool = redis.ConnectionPool(host=host, port=port, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r
