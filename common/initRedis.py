# encoding=utf-8
import redis


def connetcredis():
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    red = redis.Redis(connection_pool=pool)
    return red