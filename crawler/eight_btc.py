import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_eight_btc import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import EightBiteInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def eight_information(url):
    logger.info("巴比特抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_eight_btc_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_BA_BI_TE.value, data["url"]))
            logger.info("巴比特数据缓存返回:%s" % cache_data)
            if cache_data is None:
                EightBiteInformation.create(
                    content=data["content"],
                    crawler_url=data["url"],
                    title=data["title"],
                    author=data["author"],
                    img=data["match_img"],
                    source_name=data["source_name"]
                )
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_BA_BI_TE.value, data["url"]),
                                   json_convert_str(data))
                # 去重队列
                rows = EightBiteInformation.select().where(EightBiteInformation.crawler_url == data["url"])
                for row in rows:
                    data["content_id"] = row.id
                    connetcredis().lpush(
                        "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                        json_convert_str(data))


@app.task(ignore_result=True)
def schudule_eight_information():
    app.send_task('crawler.eight_btc.eight_information', args=("http://www.8btc.com/sitemap?pg=1",),
                  queue='eight_btc_task',
                  routing_key='eight_btc_info')


# if __name__ == "__main__":
#     eight_information("http://www.8btc.com/sitemap?pg=1")