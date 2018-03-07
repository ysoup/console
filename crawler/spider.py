# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_jinse import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, DuplicateRemovalCache, GetListLength
from database.jin_se_modle import JinseInformation
from celerymain.main import app
import logging


@app.task(ignore_result=True)
def send(url):  # 金色财经快讯
    # 读取数据缓存做增量抓取
    print("正在抓取链接", url)
    # 判断数据缓存是否存在
    date = get_current_date()
    crawler_data = crawler_jinse(url)
    if len(cache_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SE.value, data["content_id"]))
            if not cache_data is None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    JinseInformation.update(content=data["content"]).where(JinseInformation.content_id ==
                                                                           data["content_id"])
                    connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SE.value, data["content_id"]),
                                       json_convert_str(data))
                    connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                        json_convert_str(data))

            else:
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SE.value, data["content_id"]),
                                   json_convert_str(data))
                connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                    json_convert_str(data))
                JinseInformation.create(
                    content=data["content"],
                    content_id=data["content_id"],
                    source_link=data["source_link"],
                    title=data["title"],
                    author=data["author"]
                )


@app.task(ignore_result=True)
def schudule_crawler_task():
    app.send_task('crawler.spider.send', args=("http://www.jinse.com/ajax/lives/getList?id=0&flag=up",), queue='task_crawler',
                  routing_key='task_crawler')
# if __name__ == "__main__":
#     send("http://www.jinse.com/ajax/lives/getList?id=0&flag=up")