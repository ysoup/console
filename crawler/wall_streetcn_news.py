import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_wall_streetcn import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import WallStreetcnInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def wall_streetcn_information(url):
    logger.info("链得得抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_wall_streetcn_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_WALL_STREETCN.value, data["content_id"]))
            logger.info("链得得数据缓存返回:%s" % cache_data)
            if cache_data is None:
                try:
                    WallStreetcnInformation.create(
                        content_id=data["content_id"],
                        content=data["content"],
                        source_name=data["source_name"],
                        title=data["title"],
                        author=data["author"],
                        img=data["match_img"],
                        crawler_url=data["url"]
                    )
                except Exception as e:
                    logger.error("链得得抓取持久化出错:%s" % e)
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_WALL_STREETCN.value, data["content_id"]),
                                   json_convert_str(data))
            # 去重队列
            connetcredis().lpush(
                "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                json_convert_str(data))


@app.task(ignore_result=True)
def schudule_wall_streetcn_information():
    app.send_task('crawler.wall_streetcn_news.wall_streetcn_information', args=("https://api-prod.wallstreetcn.com/apiv1/search/"
                                                                    "article?order_type=time&cursor=&limit=20&search_id"
                                                                    "=&query=%E5%8C%BA%E5%9D%97%E9%93%BE",),
                  queue='wall_streetcn_task',
                  routing_key='wall_streetcn_info')


# if __name__ == "__main__":
#     wall_streetcn_information("https://api-prod.wallstreetcn.com/apiv1/search/"
#                               "article?order_type=time&cursor=&limit=20&search_id"
#                               "=&query=%E5%8C%BA%E5%9D%97%E9%93%BE")