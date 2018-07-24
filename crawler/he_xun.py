import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from spiders.crawler_he_xun import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.he_xun_model import HeXunInformation

logger = Logger(kind="work_path", name="coin_world")

@app.task(ignore_result=True)
def he_xun_information(url):
    logger.info("和讯网抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_he_xun_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_HE_XUN.value, data["content_id"]))
            logger.info("和讯网数据缓存返回:%s" % cache_data)
            if cache_data is None:
                try:
                    HeXunInformation.create(
                        content_id=data["content_id"],
                        content=data["content"],
                        source_name=data["source_name"],
                        title=data["title"],
                        crawler_date=data["crawler_date"],
                        match_img=data["match_img"],
                        source_link=data["url"],
                        author = data["author"]
                    )
                except Exception as e:
                    logger.error("和讯网抓取持久化出错:%s" % e)
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_HE_XUN.value, data["content_id"]),
                                   json_convert_str(data))
            # 去重队列
            connetcredis().lpush(
                DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value,
                json_convert_str(data))

@app.task(ignore_result=True)
def schudule_he_xun_information():
    app.send_task('crawler.he_xun.he_xun_information', args=("http://iof.hexun.com/js/iofdata_160361911.js?t=1528350588427",),
                  queue='he_xun_task',
                  routing_key='he_xun_info')

# if __name__ == "__main__":
#     he_xun_information("http://iof.hexun.com/js/iofdata_160361911.js?t=1528350588427")







