# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from database.demo import TestSpider
from common.crawleranalysis import AnalysisPage
from common.crawlerrequest import CrawlerRequest
from common.initRedis import connetcredis
from common.untils import *
from common.constants import CompareResult, RedisConstantsKey


@app.task(ignore_result=True)
def send(url):
    # 读取数据缓存做增量抓取
    print("正在抓取链接", url)
    # 判断数据缓存是否存在
    cache_data = connetcredis().get(RedisConstantsKey.DEMO_CRAWLER_SAVE)
    # 抓取的数据
    crawler_data = ""
    if not cache_data:
        print("aaa")
        # 异步入库操作
    else:
        com_ret = compare_string(cache_data, crawler_data)
        # 抓取的值与缓存的值作比较,如果抓取的值与缓存的值相等,直接return,如果不相等做入库操作
        if com_ret == CompareResult.StrSame:
            return
        else:
            # 异步入库操作
            connetcredis().set(RedisConstantsKey.DEMO_CRAWLER_SAVE, str)


@app.task(ignore_result=True)
def schudule_crawler_task():
    app.send_task('crawler.spider.send', args=("http://www.jinse.com/lives",), queue='task_crawler',
                  routing_key='task_crawler')

