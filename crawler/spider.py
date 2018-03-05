# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_jinse import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import CompareResult, RedisConstantsKey, DuplicateRemovalCache


# @app.task(ignore_result=True)
def send(url):
    # 读取数据缓存做增量抓取
    print("正在抓取链接", url)
    # 判断数据缓存是否存在
    crawler_data = crawler_jinse(url)
    str1 = ""
    cache_data = connetcredis().get(RedisConstantsKey.DEMO_CRAWLER_SAVE.value)
    if not cache_data:
        print("aaa")
        # todo 异步入库操作
        # 将抓取数据缓存到redis集合里面
        connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, get_current_date), str1)
    else:
        com_ret = compare_string(cache_data, crawler_data)
        # 抓取的值与缓存的值作比较,如果抓取的值与缓存的值相等,直接return,如果不相等做入库操作
        if com_ret == CompareResult.StrSame.value:
            return
        else:
            # 异步入库操作
            # todo
            # 抓取数据缓存
            connetcredis().set(RedisConstantsKey.DEMO_CRAWLER_SAVE.value, str1)
            # 将抓取数据缓存到redis集合里面
            connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, get_current_date), str1)


# @app.task(ignore_result=True)
# def schudule_crawler_task():
#     app.send_task('crawler.spider.send', args=("http://www.jinse.com/lives",), queue='task_crawler',
#                   routing_key='task_crawler')
if __name__ == "__main__":
    send("http://www.jinse.com/lives")