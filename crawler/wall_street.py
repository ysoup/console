import sys
import os

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)

from spiders.spider_wall_street import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey,GetListLength,DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.wall_street_model import WallStreetInformation
from database.new_flash_model import NewFlashInformation


logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def wall_street_information(url):
    logger.info("华尔街快讯抓取链接：%s" % url)
    date = get_current_date()
    crawler_data = crawler_wall_street_information(url,logger)
    for data in crawler_data:
        cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_WALL_STREET.value, data["content_id"]))
        logger.info("华尔街快讯数据缓存返回:%s" % cache_data)
        if cache_data is not None:
            str1 = str_convert_json(cache_data)
            distance = get_str_distance(data["content"], str1["content"])
            logger.info("华尔街快讯抓取与数据缓存相似度:%s" % distance)
            # 去重队列
            query_data = public_is_exist_data(data["content_id"], data["source_name"])
            if query_data:
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                     json_convert_str(data))
            if distance > GetListLength.GET_NOMBAL_NUM.value:
                WallStreetInformation.update(content=data["content"]).where(WallStreetInformation.content_id == data["content_id"])
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_WALL_STREET.value, data["content_id"]), json_convert_str(data))
        else:
            connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_WALL_STREET.value, data["content_id"]),
                               json_convert_str(data))
            # 去重队列
            connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                 json_convert_str(data))
            WallStreetInformation.create(
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
def schudule_crawler_task():
    app.send_task('crawler.wall_street.wall_street_information', args=("https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=blockchain-channel&limit=10",),
                  queue='wall_street_task',routing_key='wall_street_info')


# if __name__ == "__main__":
#     wall_street_information("https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=blockchain-channel&limit=10")