# encoding=utf-8
import redis


def connetcredis():
    #r = redis.Redis(host='127.0.0.1', port=6379, decode_responses=True)
    pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    return r
