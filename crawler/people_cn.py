import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)

from spiders.spider_people_cn import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey,GetListLength,DuplicateRemovalCache
from common.initlog import Logger
from celerymain.main import app
from database.he_xun_model import PeopleCnInformation

logger = Logger(kind="work_path",name="coin_world")


@app.task(ignore_result=True)
def people_cn_information(url):
    logger.info("人民网资讯抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_people_cn_information(url,logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_PEOPLE_CN.value, data["content_id"]))
            logger.info("人民网资讯数据缓存返回：%s" % cache_data)
            if cache_data is None:
                try:
                    PeopleCnInformation.create(
                        content_id=data["content_id"],
                        author=data["author"],
                        content=data["content"],
                        source_name=data["source_name"],
                        title=data["title"],
                        img=data["match_img"],
                        crawler_url=data["url"]
                    )
                except Exception as e:
                    logger.error("人民网抓取持久化出错：%s" % e)
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_PEOPLE_CN.value, data["content_id"]),
                                   json_convert_str(data))

            # 去重队列
            connetcredis().lpush(
                "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                json_convert_str(data))


@app.task(ignore_result=True)
def schudule_people_cn_information():
    app.send_task("crawler.people_cn.people_cn_information", args=("http://capital.people.com.cn/GB/417685/index.html",),
                  queue='people_cn_task',
                  routing_key='people_cn_info')

# if __name__ == "__main__":
#     people_cn_information("http://capital.people.com.cn/GB/417685/index.html")


