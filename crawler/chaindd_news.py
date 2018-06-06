import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_chaindd_news import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import ChainDdInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def chaindd_information(url):
    logger.info("链得得抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_chaindd_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_CHAINDD.value, data["content_id"]))
            logger.info("链得得数据缓存返回:%s" % cache_data)
            if cache_data is None:
                try:
                    ChainDdInformation.create(
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
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_CHAINDD.value, data["content_id"]),
                                   json_convert_str(data))
            # 去重队列
            connetcredis().lpush(
                "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                json_convert_str(data))


@app.task(ignore_result=True)
def schudule_chaindd_information():
    app.send_task('crawler.chaindd_news.chaindd_information', args=("http://www.chaindd.com/ajax/common/get?url=%2Fv1%2Fposts%"
                                                                 "2Flist%2Fcategory%2F3048842&data=limit%3D15%26offset%3D0%26"
                                                                 "fields%3Dthumb_image%3Bsummary%3Bnumber_of_comments%3Bnumber_"
                                                                 "of_reads%3Btags%3Bauthors%26thumb_image_size%3D%5B%22200_150%22%5D",),
                  queue='chaindd_task',
                  routing_key='chaindd_info')


# if __name__ == "__main__":
#     chaindd_information("http://www.chaindd.com/ajax/common/get?url=%2Fv1%2Fposts%2Flist%2Fcategory%2F3048842&data=limit%3D15%26offset%3D0%26fields%3Dthumb_image%3Bsummary%3Bnumber_of_comments%3Bnumber_of_reads%3Btags%3Bauthors%26thumb_image_size%3D%5B%22200_150%22%5D")