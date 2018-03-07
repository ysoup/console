import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_coin_world import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from database.coin_world_modle import CoinWorldInformation
from celerymain.main import app


@app.task(ignore_result=True)
def coin_world_information(url):  # 币世界快讯
    date = get_current_date()
    crawler_data = crawler_coin_world_information(url)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.DEMO_CRAWLER_SAVE.value, data["content_id"]))
            if not cache_data is None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    CoinWorldInformation.update(content=data["content"]).where(CoinWorldInformation.content_id ==
                                                                               data["content_id"])
                    connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_COIN_WORLD.value, data["content_id"]),
                                       json_convert_str(data))
                    connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                        json_convert_str(data))
            else:
                connetcredis().set("%s_%s" % (RedisConstantsKey.CRAWLER_COIN_WORLD.value, data["content_id"]),
                                   json_convert_str(data))
                connetcredis().sadd("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                    json_convert_str(data))
                CoinWorldInformation.create(
                    content=data["content"],
                    content_id=data["content_id"],
                    source_link=data["source_link"],
                    title=data["title"],
                    author=data["author"]
                )


@app.task(ignore_result=True)
def schudule_coin_world_information():
    app.send_task('crawler.coin_world.coin_world_information', args=("http://www.bishijie.com/api/news/?size=5",),
                  queue='task_crawler_coin_wold',
                  routing_key='task_coin_world')


def coin_world_market(url): # 行情
    crawler_data = crawler_coin_world_market(url)


# if __name__ == "__main__":
#     coin_world_market("http://www.bishijie.com/hangqing")