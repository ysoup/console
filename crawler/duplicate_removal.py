# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from common.initRedis import connetcredis
from common.untils import *
from database.new_flash_model import NewFlashInformation
import time
from common.constants import GetListLength, DuplicateRemovalCache
from common.initlog import Logger

logger = Logger(kind="work_path", name="duplicate_removal")


@app.task()
def duplicate_removal_work():
    # 从redis集合中获取获取
    logger.info("=====开始数据去重服务====")
    red = connetcredis()
    date = get_current_date()
    data = red.smembers("%s_%s" % ((DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE).value, date))
    if len(data) != GetListLength.GET_LIST_LENGTH.value:
        data = [str_convert_json(x) for x in data]
        logger.info("数据去重服务集合数据:%s" % data)
        i = GetListLength.GET_LIST_LENGTH.value
        while i < len(data):
            for j in range(i + 1, len(data)):
                if j >= len(data):
                    break
                str1 = data[i]["content"]
                str2 = data[j]["content"]
                distance1 = (Simhash(str1.split("】")[-1]).distance(Simhash(str2.split("】")[-1])))
                distance = (Simhash(str1).distance(Simhash(str2)))
                # 相同的数据
                if distance <= GetListLength.GET_NOMBAL_NUM.value or distance1 <= GetListLength.GET_NOMBAL_NUM.value:
                    del data[j]
            i = i + 1
        # 去重数据异步入库并且查询当天数据
        # 链接服务器操作数据库
        # todo 异步查询
        rows = NewFlashInformation.select().order_by(NewFlashInformation.create_time.desc()).limit(1000)
        content_ls = []
        for row in rows:
            init_time = time.strptime(str(row.create_time), "%Y-%m-%d %H:%M:%S")
            new_time = time.strftime("%Y-%m-%d", init_time)
            if new_time == date:
                content_ls.append(row.content)
        logger.info("数据去重服务查询当天快讯:%s" % content_ls)
        if len(content_ls) == GetListLength.GET_LIST_LENGTH.value:
            for com_data in data:
                query_data = NewFlashInformation.select().where(NewFlashInformation.content_id == com_data["content_id"],
                                                                NewFlashInformation.source_name == com_data["source_name"])
                if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                    NewFlashInformation.create(content=com_data["content"],
                                               content_id=com_data["content_id"],
                                               source_name=com_data["source_name"]
                                               )
        else:
            for com_data in data:
                for row in content_ls:
                    distance = get_str_distance(com_data["content"], row)
                    distance1 = (Simhash(com_data["content"].split("】")[-1]).distance(Simhash(row.split("】")[-1])))
                    if distance >= GetListLength.GET_NOMBAL_NUM.value and distance1 >= GetListLength.GET_NOMBAL_NUM.value:
                        query_data = NewFlashInformation.select().where(
                            NewFlashInformation.content_id == com_data["content_id"],
                            NewFlashInformation.source_name == com_data["source_name"])
                        if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                            NewFlashInformation.create(content=com_data["content"],
                                                       content_id=com_data["content_id"],
                                                       source_name=com_data["source_name"]
                                                       )
        # 清空数据集合
        red.delete("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date))
        logger.info("=====数据去重服务结束====")


@app.task(ignore_result=True)
def schudule_duplicate_removal_work():
    app.send_task('crawler.duplicate_removal.duplicate_removal_work', queue='duplicate_removal_task', routing_key='duplicate_removal_info')

# if __name__ == "__main__":
    # asyn_get_data()
    # r = connetcredis()
    # r.set('name', 'junxi')
    # print(r['name'])
    # print(r.get('name'))  # 取出键name对应的值
    # print(type(r.get('name')))
    # duplicate_removal_work()