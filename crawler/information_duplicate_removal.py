# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from common.initRedis import connetcredis
from common.untils import *
from database.new_flash_model import NewFlashExclusiveInformation
from common.constants import GetListLength, DuplicateRemovalCache
from common.initlog import Logger
from common.get_article_tag import GetBaiduNlp
from common.get_article_content import Extractor
from common.hadoop_service import upload_images_hdfs, img_cut_down
from common.db_utils import *

logger = Logger(kind="work_path", name="duplicate_removal")


@app.task()
def information_duplicate_removal_work():
    # 从redis集合中获取获取
    logger.info("=====开始资讯数据去重服务====")
    redis = connetcredis()
    date = get_current_date()
    # 判断队列长度
    data_len = redis.llen("%s_%s" % ((DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE).value, date))
    logger.info("资讯数据去重队列:%s" % data_len)
    if data_len < 1:
        return
    i = 0
    data = []
    while i < data_len:
        data_str = redis.lpop("%s_%s" % ((DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE).value, date))
        data.append(str_convert_json(data_str))
        i = i+1
    if len(data) != GetListLength.GET_LIST_LENGTH.value:
        logger.info("资讯数据去重服务集合数据:%s" % data)
        i = GetListLength.GET_LIST_LENGTH.value
        while i < len(data):
            content_1 = data[i]["content"]
            ext_1 = Extractor(content=content_1, blockSize=15, image=False).getContext()
            data[i]["category"], data[i]["is_show"] = get_content_tag(ext_1, redis)

            for j in range(i + 1, len(data)):
                if j >= len(data):
                    break
                content_2 = data[j]["content"]
                distance, ext_1_text, ext_2_text = get_content_by_reg(content_1, content_2)
                # 标题
                distance1 = get_str_distance(data[i]["title"], data[j]["title"])
                data[j]["category"], data[j]["is_show"] = get_content_tag(ext_2_text, redis)
                if distance <= 20 or distance1 <= 18:
                    del data[j]
            i = i + 1
        # 去重数据异步入库并且查询当天数据
        # 链接服务器操作数据库
        # todo 异步查询
        sql = "SELECT * FROM new_flash_exclusive_information where TIMESTAMPDIFF(day, create_time, now()) <= 3"
        rows = excute_sql(NewFlashExclusiveInformation, sql)
        content_ls = model_to_dicts(rows)
        logger.info("数据去重服务查询当天资讯:%s" % content_ls)
        if len(content_ls) == GetListLength.GET_LIST_LENGTH.value:
            for com_data in data:
                query_data = NewFlashExclusiveInformation.select().where(NewFlashExclusiveInformation.content_id == com_data["content_id"],
                                                                         NewFlashExclusiveInformation.source_name == com_data["source_name"])
                if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                    # 图片处理
                    start_img_ls = com_data["match_img"].split(",")
                    i = 1
                    res_img_ls = []
                    for img_url in start_img_ls:
                        new_img_url = upload_images_hdfs(img_url, com_data["source_name"],
                                                        com_data["content_id"], i)
                        if img_url != '':
                            com_data["content"] = com_data["content"].replace(img_url, new_img_url)
                        res_img_ls.append(new_img_url)
                        i = i + 1
                    # 内容标签
                    get_article_tag(com_data)
                    # 图片处理
                    new_img_url = img_cut_down(start_img_ls[0], com_data["source_name"], com_data["content_id"], 1)

                    save_news_data(com_data, new_img_url)

        else:
            for com_data in data:
                flag = 1
                for row in content_ls:
                    content_1 = com_data["content"]
                    content_2 = row["content"]
                    distance, ext_1_text, ext_2_text = get_content_by_reg(content_1, content_2)
                    # 标题
                    distance1 = get_str_distance(com_data["title"], row["title"])

                    if distance <= 20 or distance1 <= 18:
                        flag = 0
                        break
                    elif (distance<=25 and distance >20) or (distance<=23 and distance >18):
                        flag = 2
                        break
                if flag == 1:
                    query_data = NewFlashExclusiveInformation.select().where(
                        NewFlashExclusiveInformation.content_id == com_data["content_id"],
                        NewFlashExclusiveInformation.source_name == com_data["source_name"])
                    if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                        # 图片处理
                        start_img_ls = com_data["match_img"].split(",")
                        i = 1
                        res_img_ls = []
                        for img_url in start_img_ls:
                            new_img_url = upload_images_hdfs(img_url, com_data["source_name"],
                                                             com_data["content_id"], i)
                            if img_url != '':
                                com_data["content"] = com_data["content"].replace(img_url, new_img_url)
                            res_img_ls.append(new_img_url)
                            i = i + 1
                        # 内容标签
                        get_article_tag(com_data)

                        # 图片处理
                        new_img_url = img_cut_down(start_img_ls[0], com_data["source_name"], com_data["content_id"], 1)

                        save_news_data(com_data, new_img_url)
                elif flag == 2:
                    query_data = NewFlashExclusiveInformation.select().where(
                        NewFlashExclusiveInformation.content_id == com_data["content_id"],
                        NewFlashExclusiveInformation.source_name == com_data["source_name"])
                    if len(query_data) == GetListLength.GET_LIST_LENGTH.value:
                        # 图片处理
                        start_img_ls = com_data["match_img"].split(",")
                        i = 1
                        res_img_ls = []
                        for img_url in start_img_ls:
                            new_img_url = upload_images_hdfs(img_url, com_data["source_name"],
                                                             com_data["content_id"], i)
                            if img_url != '':
                                com_data["content"] = com_data["content"].replace(img_url, new_img_url)
                            res_img_ls.append(new_img_url)
                            i = i + 1
                        # 内容标签
                        get_article_tag(com_data)

                        # 图片处理
                        new_img_url = img_cut_down(start_img_ls[0], com_data["source_name"], com_data["content_id"], 1)

                        try:
                            NewFlashExclusiveInformation.create(content=com_data["content"],
                                                                content_id=com_data["content_id"],
                                                                source_name=com_data["source_name"],
                                                                category=com_data["category"],
                                                                img=new_img_url, title=com_data["title"],
                                                                tag=com_data["tag"], author=com_data["author"],
                                                                is_show=0,
                                                                source_url=com_data["url"],
                                                                possible_similarity=1
                                                                )
                        except Exception as e:
                            logger.error("资讯持久化出错:%s" % e)

        logger.info("=====资讯数据去重服务结束====")


def get_content_by_reg(content_1, content_2):
    ext_1 = Extractor(content=content_1, blockSize=15, image=False)
    ext_1_text = ext_1.getContext()
    ext_2 = Extractor(content=content_2, blockSize=15, image=False)
    ext_2_text = ext_2.getContext()
    # 内容
    distance = get_str_distance(ext_1_text, ext_2_text)
    return distance, ext_1_text, ext_2_text


def save_news_data(com_data, new_img_url):
    try:
        NewFlashExclusiveInformation.create(content=com_data["content"],
                                            content_id=com_data["content_id"],
                                            source_name=com_data["source_name"],
                                            category=com_data["category"],
                                            img=new_img_url, title=com_data["title"],
                                            tag=com_data["tag"], author=com_data["author"],
                                            is_show=com_data["is_show"],
                                            source_url=com_data["url"],
                                            possible_similarity=0
                                            )
    except Exception as e:
        logger.error("资讯持久化出错:%s" % e)


def get_article_tag(com_data):
    try:
        ext_1_1 = Extractor(content=com_data["content"], blockSize=15, image=False)
        content = ext_1_1.getContext()
        res_1 = GetBaiduNlp(com_data["title"], content)
        key_word_1 = res_1.get_keyword()
        logger.info("百度标签返回结果:%s" % key_word_1)
        com_data["tag"] = ",".join([x["tag"] for x in key_word_1["items"]])
    except Exception as e:
        logger.error("百度自动标签出错:%s" % e)
        com_data["tag"] = ""


def get_content_tag(content, redis):
    # 获取资讯类型缓存
    data = redis.get("catch_news_categery_list")
    tag, is_show = check_news_content_type(content, data)

    return tag, is_show


@app.task(ignore_result=True)
def schudule_information_duplicate_removal_work():
    app.send_task('crawler.information_duplicate_removal.information_duplicate_removal_work',
                  queue='news_duplicate_removal_task',
                  routing_key='news_duplicate_removal_info')


# if __name__ == "__main__":
#     information_duplicate_removal_work()
    # r = connetcredis()
    # r.set('name', 'junxi')
    # print(r['name'])
    # print(r.get('name'))  # 取出键name对应的值
    # print(type(r.get('name')))
    # duplicate_removal_work()