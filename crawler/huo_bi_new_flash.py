import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_huo_bi import crawler_huo_bi_information
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from database.coin_world_modle import HuoBiInformation
from celerymain.main import app
from common.initlog import Logger

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def huo_bi_information(url):  # 币世界快讯
    logger.info("火币抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_huo_bi_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_HUO_BI.value, data["content_id"]))
            logger.info("火币数据缓存返回:%s" % cache_data)
            if cache_data is not None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                logger.info("火币抓取与数据缓存相似度:%s" % distance)
                # 去重队列
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                     json_convert_str(data))

                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    HuoBiInformation.update(content=data["content"]).where(HuoBiInformation.content_id == data["content_id"])
                    connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_HUO_BI.value, data["content_id"]),
                                       json_convert_str(data))

            else:
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BIAN_NEW_FLASH.value, data["content_id"]),
                                   json_convert_str(data))
                # 去重队列
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                     json_convert_str(data))
                HuoBiInformation.create(
                    content=data["content"],
                    content_id=data["content_id"],
                    source_link=data["source_link"],
                    title=data["title"],
                    author=data["author"]
                )


@app.task(ignore_result=True)
def schudule_huo_bi_information():
    app.send_task('crawler.huo_bi_new_flash.huo_bi_information',
                  args=("https://www.huobi.pro/-/x/hb/p/api/contents/pro/list_notice?r=e992j7bmlx&limit=10&language=zh-cn",),
                  queue='huo_bi_new_flash_task',
                  routing_key='huo_bi_new_flash_info')


# if __name__ == "__main__":
#     huo_bi_information("https://www.huobi.pro/-/x/hb/p/api/contents/pro/list_notice?r=e992j7bmlx&limit=10&language=zh-cn")