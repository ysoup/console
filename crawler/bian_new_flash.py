import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_bian_new_flash import crawler_bian_information
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from database.coin_world_modle import BiaNewsInformation
from database.new_flash_model import NewFlashInformation
from celerymain.main import app
from common.initlog import Logger

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def bianews_information(url):  # 币世界快讯
    logger.info("巴比特抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_bian_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_BIAN_NEW_FLASH.value, data["content_id"]))
            logger.info("鞭牛士数据缓存返回:%s" % cache_data)
            if cache_data is not None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                logger.info("鞭牛士抓取与数据缓存相似度:%s" % distance)
                # 去重队列
                query_data = public_is_exist_data(data["content_id"], data["source_name"])
                if query_data:
                    connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                         json_convert_str(data))

                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    BiaNewsInformation.update(content=data["content"]).where(BiaNewsInformation.content_id == data["content_id"])
                    connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BIAN_NEW_FLASH.value, data["content_id"]),
                                       json_convert_str(data))

            else:
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BIAN_NEW_FLASH.value, data["content_id"]),
                                   json_convert_str(data), 24*60*60*3)
                # 去重队列
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                     json_convert_str(data))
                BiaNewsInformation.create(
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


@app.task(ignore_result=True)
def schudule_bianews_information():
    app.send_task('crawler.bian_new_flash.bianews_information',
                  args=("https://www.bianews.com/news/news_list?channel=flash&type=1",),
                  queue='bian_new_flash_task',
                  routing_key='bian_new_flash_info')


# if __name__ == "__main__":
#     bianews_information("https://www.bianews.com/news/news_list?channel=flash&type=1")