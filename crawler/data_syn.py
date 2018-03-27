# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from common.initRedis import connetcredis
from database.discuzdb import AblinkPortalSummary
from common.untils import *
import time
from common.constants import DuplicateRemovalCache, RedisConstantsKey
from common.initlog import Logger
logger = Logger(kind="work_path", name="data_syn")


@app.task()
def data_syn_work():
    # 从redis集合中获取获取
    logger.info("=====开始数据同步服务====")
    redis = connetcredis()
    date = get_current_date()
    # 查询当前的数据
    rows = AblinkPortalSummary.select().order_by(AblinkPortalSummary.id.desc()).limit(200)
    for row in rows:
        time_array = time.localtime(row.obtaindate)
        crawler_time = time.strftime('%Y-%m-%d', time_array)
        if crawler_time == date:
            if row.source is not None:
                if row.source != "金色财经":
                    cache_data = redis.get("%s_%s" % (RedisConstantsKey.DATA_SYN_WORK.value, row.id))
                    if cache_data is not None:
                        dic = {}
                        dic["content"] = re.sub("币世界|小葱|金色财经", "爱必投", row.title)
                        dic["content_id"] = row.id
                        dic["source_link"] = ""
                        dic["title"] = ""
                        dic["author"] = ""
                        dic["source_name"] = "yun_cai"
                        redis.set("%s_%s" % (RedisConstantsKey.DATA_SYN_WORK.value, row.id), json_convert_str(dic))
                        redis.lpush("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date),
                                    json_convert_str(dic))
    logger.info("=====数据同步服务结束====")


@app.task(ignore_result=True)
def schudule_data_syn_work():
    app.send_task('crawler.data_syn.data_syn_work', queue='data_syn_task', routing_key='data_syn_info')


# if __name__ == "__main__":
#     data_syn_work()
    # r = connetcredis()
    # r.set('name', 'junxi')
    # print(r['name'])
    # print(r.get('name'))  # 取出键name对应的值
    # print(type(r.get('name')))
    # duplicate_removal_work()