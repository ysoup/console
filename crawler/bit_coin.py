import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.crawler_bit_coin_information import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import BitCoinInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def bit_coin_information(url):
    logger.info("比特币咨询抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_bit_coin_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_BIT_COIN.value, data["content_id"]))
            logger.info("比特币资讯网数据缓存返回:%s" % cache_data)
            if cache_data is None:
                BitCoinInformation.create(
                    content_id=data["content_id"],
                    content=data["content"],
                    source_name=data["source_name"],
                    title=data["title"],
                    author=data["author"],
                    img=data["match_img"],
                    crawler_url=data["url"]
                )
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BIT_COIN.value, data["content_id"]),
                                   json_convert_str(data))
                # 去重队列
                connetcredis().lpush(
                    "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                    json_convert_str(data))


@app.task(ignore_result=True)
def schudule_bit_coin_information():
    app.send_task('crawler.bit_coin.bit_coin_information', args=("http://www.bitcoin86.com/news/list_1_1.html",),
                  queue='bit_coin_task',
                  routing_key='bit_coin_info')


# if __name__ == "__main__":
#     bit_coin_information("http://www.bitcoin86.com/news/list_1_1.html")