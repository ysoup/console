# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from common.initRedis import connetcredis
from common.untils import *
from database.new_flash_model import NewFlashInformation, NewFlashCategory
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
                # 全部
                distance = get_str_distance(str1, str2)
                str3 = str1.split("】")
                str4 = str2.split("】")
                # 内容
                distance1 = get_str_distance(str3[-1], str4[-1])
                # 标题
                distance2 = get_str_distance(str3[0], str4[0])
                # 内容前30个字符
                distance3 = get_str_distance((str3[-1])[0:25], (str4[-1])[0:25])
                if distance <= 20 or distance1 <= 18 or distance2 <= 10 or distance3 <= 10:
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
                content_ls.append(row)
        logger.info("数据去重服务查询当天快讯:%s" % content_ls)
        if len(content_ls) == GetListLength.GET_LIST_LENGTH.value:
            for com_data in data:
                query_data = NewFlashInformation.select().where(NewFlashInformation.content_id == com_data["content_id"],
                                                                NewFlashInformation.source_name == com_data["source_name"])
                if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                    category = check_content_type(com_data["content"])
                    NewFlashInformation.create(content=com_data["content"],
                                               content_id=com_data["content_id"],
                                               source_name=com_data["source_name"],
                                               category=category
                                               )
        else:
            for com_data in data:
                flag = 1
                for row in content_ls:
                    str1 = com_data["content"]
                    str2 = row.content
                    # 全部
                    distance = get_str_distance(str1, str2)
                    str3 = str1.split("】")
                    str4 = str2.split("】")
                    # 内容
                    distance1 = get_str_distance(str3[-1], str4[-1])
                    # 标题
                    distance2 = get_str_distance(str3[0], str4[0])
                    # 内容前30个字符
                    distance3 = get_str_distance((str3[-1])[0:25], (str4[-1])[0:25])
                    if distance <= 20 or distance1 <= 18 or distance2 <= 10 or distance3 <= 10:
                        flag = 0
                        break
                if flag == 1:
                    query_data = NewFlashInformation.select().where(
                        NewFlashInformation.content_id == com_data["content_id"],
                        NewFlashInformation.source_name == com_data["source_name"])
                    if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                        category = check_content_type(com_data["content"])
                        NewFlashInformation.create(content=com_data["content"],
                                                   content_id=com_data["content_id"],
                                                   source_name=com_data["source_name"],
                                                   category=category
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