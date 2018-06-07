import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_sina_information import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import SinaInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def sina_information(url):
    logger.info("比特币咨询抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_he_xun_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_SINA_NEWS.value, data["content_id"]))
            logger.info("比特币资讯网数据缓存返回:%s" % cache_data)
            if cache_data is None:
                try:
                    SinaInformation.create(
                        content_id=data["content_id"],
                        content=data["content"],
                        source_name=data["source_name"],
                        title=data["title"],
                        author=data["author"],
                        img=data["match_img"],
                        crawler_url=data["url"]
                    )
                except Exception as e:
                    logger.error("比特币资讯网抓取持久化出错:%s" % e)
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_SINA_NEWS.value, data["content_id"]),
                                   json_convert_str(data))
            # 去重队列
            connetcredis().lpush(
                "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                json_convert_str(data))


@app.task(ignore_result=True)
def schudule_sina_information():
    app.send_task('crawler.sina_news.sina_information',
                  args=("http://roll.finance.sina.com.cn/finance/wh/btbxw/index.shtml",),
                  queue='sina_news_task',
                  routing_key='sina_news_info')


# if __name__ == "__main__":
#     sina_information("http://roll.finance.sina.com.cn/finance/wh/btbxw/index.shtml")