import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_cailianpress import crawler_cailianpress_information
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from database.coin_world_modle import CailianpressInformation
from celerymain.main import app
from common.initlog import Logger
import time
logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def cailianpress_information(url):  # 財联社
    logger.info("財联社抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_cailianpress_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_CAILIANPRESS.value, data["content_id"]))
            logger.info("財联社数据缓存返回:%s" % cache_data)
            if cache_data is not None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                logger.info("財联社抓取与数据缓存相似度:%s" % distance)
                # 去重队列
                connetcredis().lpush("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                     json_convert_str(data))

                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    CailianpressInformation.update(content=data["content"]).where(CailianpressInformation.content_id == data["content_id"])
                    connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BIAN_CRAWLER_CAILIANPRESSNEW_FLASH.value, data["content_id"]),
                                       json_convert_str(data))

            else:
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_CAILIANPRESS.value, data["content_id"]),
                                   json_convert_str(data))
                # 去重队列
                connetcredis().lpush("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                     json_convert_str(data))
                CailianpressInformation.create(
                    content=data["content"],
                    content_id=data["content_id"],
                    source_link=data["source_link"],
                    title=data["title"],
                    author=data["author"]
                )


@app.task(ignore_result=True)
def schudule_cailianpress_information():
    t = time.time()
    app.send_task('crawler.cailianpress_new_flash.cailianpress_information',
                  args=("https://www.cailianpress.com/nodeapi/telegraphs?last_time=%s&refresh_type=0" % int(t),),
                  queue='cailianpress_new_flash_task',
                  routing_key='cailianpress_new_flash_info')


# if __name__ == "__main__":
#     t = time.time()
#     cailianpress_information("https://www.cailianpress.com/nodeapi/telegraphs?last_time=1528176014&refresh_type=0")