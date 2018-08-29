import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from spiders.crawler_binance_notice import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey,GetListLength,DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.okex_model import BinanceNoticeInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def binance_notice_info(url):
    logger.info("binance_notice抓取链接：%s" % url)
    date = get_current_date()
    crawler_data = crawler_binance_notice(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_BINANCE_NOTICE.value, data["content_id"]))
            logger.info("binance_notice数据缓存返回：%s" % cache_data)
            if cache_data is None:
                try:
                    BinanceNoticeInformation.create(
                        title=data["title"],
                        source_link=data["source_link"],
                        content_id=data["content_id"],
                        content=data["content"],
                        source_name=data["source_name"],
                    )
                except Exception as e:
                    logger.error("bince_notice抓取持久化出错：%s" % e)
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BINANCE_NOTICE.value,data["content_id"]),
                                   json_convert_str(data), 24*60*60*3)

            # 去重队列
            connetcredis().lpush(
                DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                json_convert_str(data))

@app.task(ignore_result=True)
def schudule_binance_information():
    app.send_task("crawler.binance_notice.binance_notice_info", args=("https://support.binance.com/hc/zh-cn/categories/115000056351",),
                  queue='binance_notice_task',
                  routing_key='binance_notice_info')

# if __name__ == "__main__":
#     binance_notice_info("https://support.binance.com/hc/zh-cn/categories/115000056351")















