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
from common.constants import GetListLength, DuplicateRemovalCache
from common.initlog import Logger
from common.db_utils import *

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
                content_str1 = data[i]["content"] if data[i]["content"] else ""
                content_str2 = data[j]["content"] if data[j]["content"] else ""

                title_str1 = data[i]["title"] if data[i]["title"] else ""
                title_str2 = data[j]["title"] if data[j]["title"] else ""

                # 内容
                distance1 = get_str_distance(content_str1, content_str2)
                # 标题
                distance2 = get_str_distance(title_str1, title_str2)
                # 内容前30个字符
                distance3 = get_str_distance(content_str1[0:25], content_str2[0:25])
                if distance1 <= 18 or distance2 <= 10 or distance3 <= 10:
                    logger.info("快讯数据去重服务重复数据:%s" % data[j])
                    del data[j]
            i = i + 1
        # 去重数据异步入库并且查询当天数据
        # 链接服务器操作数据库
        # todo 异步查询
        sql = "SELECT * FROM new_flash_information where TIMESTAMPDIFF(day, create_time, now()) <= 1"
        rows = excute_sql(NewFlashInformation, sql)
        content_ls = model_to_dicts(rows)
        logger.info("数据去重服务以后快讯:%s" % data)
        if len(content_ls) == GetListLength.GET_LIST_LENGTH.value:
            for com_data in data:
                logger.info("快讯库没有数据处理:%s" % com_data)
                query_data = NewFlashInformation.select().where(NewFlashInformation.content_id == com_data["content_id"],
                                                                NewFlashInformation.source_name == com_data["source_name"])
                if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                    category, is_show, modify_tag, content, title = check_content_type(com_data["title"],
                                                                                       com_data["content"],
                                                                                       category_data,
                                                                                       rule_data)
                    logger.info("快讯入库:%s" % com_data)
                    NewFlashInformation.create(content=content,
                                               content_id=com_data["content_id"],
                                               source_name=com_data["source_name"],
                                               category=category,
                                               is_show=is_show,
                                               re_tag=modify_tag,
                                               title=title
                                               )
        else:
            for com_data in data:
                logger.info("快讯库有数据处理:%s" % com_data)
                flag = public_compare_content(content_ls, com_data, logger)
                logger.info("快讯库有数据处理flag:%s" % flag)
                if flag == 1:
                    query_data = NewFlashInformation.select().where(
                        NewFlashInformation.content_id == com_data["content_id"],
                        NewFlashInformation.source_name == com_data["source_name"])
                    if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                        category, is_show, modify_tag, content, title = check_content_type(com_data["title"],
                                                                                           com_data["content"],
                                                                                           category_data,
                                                                                           rule_data)
                        logger.info("快讯入库:%s" % com_data)
                        sql = "SELECT * FROM new_flash_information where " \
                              "TIMESTAMPDIFF(MINUTE ,create_time,now()) <= 5 and is_show=1 order by create_time desc"
                        second_data = excute_sql(NewFlashInformation, sql)
                        second_content_ls = model_to_dicts(second_data)
                        second_flag = public_compare_content(second_content_ls, com_data, logger)
                        if second_flag == 1:
                            NewFlashInformation.create(content=content,
                                                       content_id=com_data["content_id"],
                                                       source_name=com_data["source_name"],
                                                       category=category,
                                                       is_show=is_show,
                                                       re_tag=modify_tag,
                                                       title=title
                                                       )
                        elif second_flag == 2:
                            NewFlashInformation.create(content=content,
                                                       content_id=com_data["content_id"],
                                                       source_name=com_data["source_name"],
                                                       category=category,
                                                       is_show=0,
                                                       re_tag=modify_tag,
                                                       title=title,
                                                       possible_similarity=1
                                                       )

                elif flag == 2:
                    query_data = NewFlashInformation.select().where(
                        NewFlashInformation.content_id == com_data["content_id"],
                        NewFlashInformation.source_name == com_data["source_name"])
                    if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                        category, is_show, modify_tag, content, title = check_content_type(com_data["title"],
                                                                                           com_data["content"],
                                                                                           category_data,
                                                                                           rule_data)
                        NewFlashInformation.create(content=content,
                                                   content_id=com_data["content_id"],
                                                   source_name=com_data["source_name"],
                                                   category=category,
                                                   is_show=0,
                                                   re_tag=modify_tag,
                                                   title=title,
                                                   possible_similarity=1
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