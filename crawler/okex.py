import sys
import os

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)

from spiders.spider_okex import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey,GetListLength,DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.okex_model import OKExInformation



logger = Logger(kind="work_path", name="coin_world")

@app.task
def okex_information(url):
    logger.info("okex抓取链接：%s" % url)
    date = get_current_date()
    crawler_data = crawler_okex_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_OKEX.value, data["content_id"]))
            logger.info("okex数据缓存返回：%s" % cache_data)
            if cache_data is None:
                try:
                    OKExInformation.create(
                        title=data["title"],
                        source_link=data["source_link"],
                        content_id=data["content_id"],
                        content=data["content"],
                        source_name=data["source_name"],
                    )
                except Exception as e:
                    logger.error("okex抓取持久化出错：%s" % e)
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_OKEX.value,data["content_id"]),
                                   json_convert_str(data))

            # 去重队列
            connetcredis().lpush(
                "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                json_convert_str(data))

@app.task
def schudule_okex_information():
    app.send_task("crawler.okex.okex_information", args=("https://support.okex.com/hc/zh-cn/sections/115000447632-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83",),
                  queue='okex_task',
                  routing_key='okex_info')

# if __name__ == "__main__":
#     okex_information("https://support.okex.com/hc/zh-cn/sections/115000447632-%E5%85%AC%E5%91%8A%E4%B8%AD%E5%BF%83")

