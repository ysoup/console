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
from common.initlog import Logger
from database.jin_se_modle import JinseInformation
from database.new_flash_model import NewFlashInformation
from celerymain.main import app

logger = Logger(kind="work_path", name="jin_se")


@app.task
def send(url):  # 金色财经快讯
    # 读取数据缓存做增量抓取
    logger.info("金色财经抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_jinse(url, logger)
    for data in crawler_data:
        # 判断数据缓存是否存在
        cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SE.value, data["content_id"]))
        logger.info("金色财经数据缓存返回:%s" % cache_data)
        if cache_data is not None:
            str1 = str_convert_json(cache_data)
            distance = get_str_distance(data["content"], str1["content"])
            logger.info("金色财经抓取与数据缓存相似度:%s" % distance)
            # 去重队列
            connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                 json_convert_str(data))
            if distance > GetListLength.GET_NOMBAL_NUM.value:
                JinseInformation.update(content=data["content"]).where(JinseInformation.content_id ==
                                                                       data["content_id"])
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SE.value, data["content_id"]),
                                   json_convert_str(data))
        else:
            connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SE.value, data["content_id"]),
                               json_convert_str(data))
            # 去重队列
            query_data = public_is_exist_data(data["content_id"], data["source_name"])
            if query_data:
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, json_convert_str(data))
            JinseInformation.create(
                content=data["content"],
                content_id=data["content_id"],
                source_link=data["source_link"],
                title=data["title"],
                author=data["author"]
            )


def public_is_exist_data(content_id, source_name):
    query_data = NewFlashInformation.select().where(
        NewFlashInformation.content_id == content_id,
        NewFlashInformation.source_name == source_name)
    return query_data


@app.task
def schudule_crawler_task():
    app.send_task('crawler.spider.send', args=("http://www.jinse.com/ajax/lives/getList?id=0&flag=up",), queue='jin_se_task',
                  routing_key='jin_se_info')


# if __name__ == "__main__":
#     send("http://www.jinse.com/ajax/lives/getList?id=0&flag=up")