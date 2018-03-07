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
from database.demo import TestSpider
from celerymain.main import app
import logging


@app.task(ignore_result=True)
def send(url):  # 金色财经快讯
    # 读取数据缓存做增量抓取
    print("正在抓取链接", url)
    # 判断数据缓存是否存在
    date = get_current_date()
    crawler_data = crawler_jinse(url)
    cache_data = connetcredis().get(RedisConstantsKey.DEMO_CRAWLER_SAVE.value)
    if not cache_data:
        # todo 异步入库操作
        for data in crawler_data:
            row = TestSpider.select().where(TestSpider.content_id == data["content_id"])
            if len(row) == 0:
                TestSpider.create(
                    content=data["content"],
                    content_id=data["content_id"],
                    current_time=get_current_date())
                # 将抓取数据缓存到redis集合里面
                connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date), json_convert_str(data))
    else:
        com_ret = compare_string(cache_data, json_convert_str(crawler_data))
        # 抓取的值与缓存的值作比较,如果抓取的值与缓存的值相等,直接return,如果不相等做入库操作
        if com_ret == CompareResult.StrSame.value:
            return
        else:
            # todo 异步入库操作
            for data in crawler_data:
                row = TestSpider.select().where(TestSpider.content_id == data["content_id"])
                if len(row) == 0:
                    TestSpider.create(
                        content=data["content"],
                        content_id=data["content_id"],
                        current_time=get_current_date())
                else:
                    TestSpider.update(content=data["content"]).where(TestSpider.content_id == data["content_id"])
                # 将抓取数据缓存到redis集合里面
                connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date), json_convert_str(data))
    # 抓取数据缓存
    connetcredis().set(RedisConstantsKey.DEMO_CRAWLER_SAVE.value, json_convert_str(crawler_data))


@app.task(ignore_result=True)
def schudule_crawler_task():
    app.send_task('crawler.spider.send', args=("http://www.jinse.com/ajax/lives/getList?id=0&flag=up",), queue='task_crawler',
                  routing_key='task_crawler')
# if __name__ == "__main__":
#     send("http://www.jinse.com/ajax/lives/getList?id=0&flag=up")