import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)

from spiders.spider_jin_shi import crawler_jin_shi_information
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from database.jin_shi_model import JinShiInformation
from database.new_flash_model import NewFlashInformation
from celerymain.main import app
from common.initlog import Logger

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def jin_shi_information(url):
    logger.info("金十抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_jin_shi_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SHI.value, data["content_id"]))
            logger.info("金十数据缓存返回:%s" % cache_data)
            if cache_data is not None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                logger.info("金十抓取数据与数据缓存相似度:%s" % distance)
                # 去重队列
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                     json_convert_str(data))

                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    JinShiInformation.update(content=data["content"]).where(JinShiInformation.content_id ==
                                                                            data["content_id"])
                    connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SHI.value, data["content_id"]),
                                       json_convert_str(data))

            else:
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_JIN_SHI.value, data["content_id"]),
                                   json_convert_str(data))
                # 去重队列
                query_data = public_is_exist_data(data["content_id"], data["source_name"])
                if query_data:
                    connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                         json_convert_str(data))
                JinShiInformation.create(
                    crawler_time=data["crawler_time"],
                    content=data["content"],
                    content_id=data["content_id"],
                    title=data["title"],
                    author=data["author"],
                    source_name=data["source_name"]
                )


def public_is_exist_data(content_id, source_name):
    query_data = NewFlashInformation.select().where(
        NewFlashInformation.content_id == content_id,
        NewFlashInformation.source_name == source_name)
    return query_data


@app.task(ignore_result=True)
def schudule_crawler_task():
    app.send_task('crawler.jin_shi.jin_shi_information', args=("https://www.jin10.com/newest_1.js",),
                  queue='jin_shi_task', routing_key='jin_shi_info')

# if __name__ == "__main__":
#     jin_shi_information("https://www.jin10.com/newest_1.js")
