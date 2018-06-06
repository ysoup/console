import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_tmt_post_news import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import TmtPostInformation

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def tmt_post_information(url):
    logger.info("链得得抓取链接:%s" % url)
    date = get_current_date()
    crawler_data = crawler_tmt_post_information(url, logger)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_TMT_POST.value, data["content_id"]))
            logger.info("链得得数据缓存返回:%s" % cache_data)
            if cache_data is None:
                try:
                    TmtPostInformation.create(
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
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_TMT_POST.value, data["content_id"]),
                                   json_convert_str(data))
            # 去重队列
            connetcredis().lpush(
                "%s_%s" % (DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value, date),
                json_convert_str(data))


@app.task(ignore_result=True)
def schudule_tmt_post_information():
    app.send_task('crawler.tmt_post.tmt_post_information', args=("http://www.tmtpost.com/ajax/common/get?url=%2Fv1%2Fposts%2Flist%2Fcategory%2F3015019&data="
                         "limit%3D15%26offset%3D0%26fields%3Dthumb_image%3Bsummary%3Bnumber_of_comments%3"
                         "Btags%3Bauthors"
                         "%26thumb_image_size%3D%5B%22200_150%22%5D",),
                  queue='tmt_post_task',
                  routing_key='tmt_post_info')


# if __name__ == "__main__":
#     tmt_post_information("http://www.tmtpost.com/ajax/common/get?url=%2Fv1%2Fposts%2Flist%2Fcategory%2F3015019&data="
#                          "limit%3D15%26offset%3D0%26fields%3Dthumb_image%3Bsummary%3Bnumber_of_comments%3"
#                          "Btags%3Bauthors"
#                          "%26thumb_image_size%3D%5B%22200_150%22%5D")