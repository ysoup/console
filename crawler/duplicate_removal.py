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
    logger.info("=====开始快讯数据去重服务====")
    redis = connetcredis()
    date = get_current_date()
    # 判断队列长度
    data_len = redis.llen("%s_%s" % ((DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE).value, date))
    logger.info("快讯数据去重队列:%s" % data_len)
    category_data = redis.get("catch_infomation_categery_list")
    # 获取规则缓存
    rule_data = redis.get("catch_new_flash_rule")
    if data_len < 1:
        return
    i = 0
    data = []
    while i < data_len:
        data_str = redis.lpop("%s_%s" % ((DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE).value, date))
        data.append(str_convert_json(data_str))
        i = i + 1
    if len(data) != GetListLength.GET_LIST_LENGTH.value:
        logger.info("快讯数据去重服务集合数据:%s" % data)
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
                if distance <= 19 or distance1 <= 18 or distance2 <= 10 or distance3 <= 10:
                    print(data[j])
                    logger.info("快讯数据去重服务重复数据:%s" % data[j])
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
        logger.info("数据去重服务以后快讯:%s" % data)
        if len(content_ls) == GetListLength.GET_LIST_LENGTH.value:
            for com_data in data:
                logger.info("快讯库没有数据处理:%s" % com_data)
                query_data = NewFlashInformation.select().where(NewFlashInformation.content_id == com_data["content_id"],
                                                                NewFlashInformation.source_name == com_data["source_name"])
                if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                    category, is_show, modify_tag, content = check_content_type(com_data["content"], category_data,
                                                                                rule_data)
                    logger.info("快讯入库:%s" % com_data)
                    NewFlashInformation.create(content=content,
                                               content_id=com_data["content_id"],
                                               source_name=com_data["source_name"],
                                               category=category,
                                               is_show=is_show,
                                               re_tag=modify_tag,
                                               title=com_data["title"]
                                               )
        else:
            for com_data in data:
                flag = 1
                logger.info("快讯库有数据处理:%s" % com_data)
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
                    if distance <= 15 or distance1 <= 15 or distance2 <= 10 or distance3 <= 10:
                        logger.info("快讯库有数据处理相似度数据:%s" % row.content)
                        flag = 0
                        break
                logger.info("快讯库有数据处理flag:%s" % flag)
                if flag == 1:
                    query_data = NewFlashInformation.select().where(
                        NewFlashInformation.content_id == com_data["content_id"],
                        NewFlashInformation.source_name == com_data["source_name"])
                    if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                        category, is_show, modify_tag, content = check_content_type(com_data["content"], category_data,
                                                                                    rule_data)
                        logger.info("快讯入库:%s" % com_data)
                        NewFlashInformation.create(content=content,
                                                   content_id=com_data["content_id"],
                                                   source_name=com_data["source_name"],
                                                   category=category,
                                                   is_show=is_show,
                                                   re_tag=modify_tag,
                                                   title=com_data["title"]
                                                   )
        # 清空数据集合
        # red.delete("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date))
        logger.info("=====快讯数据去重服务结束====")


@app.task(ignore_result=True)
def schudule_duplicate_removal_work():
    app.send_task('crawler.duplicate_removal.duplicate_removal_work', queue='duplicate_removal_task', routing_key='duplicate_removal_info')


# if __name__ == "__main__":
#     duplicate_removal_work()
    # r = connetcredis()
    # r.set('name', 'junxi')
    # print(r['name'])
    # print(r.get('name'))  # 取出键name对应的值
    # print(type(r.get('name')))
    # duplicate_removal_work()