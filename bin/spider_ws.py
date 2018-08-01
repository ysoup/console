# coding:utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from database.spiders_visualization_modle import *
from common.initlog import Logger
from common.db_utils import *
from common.untils import *
logger = Logger(kind="work_path", name="duplicate_removal")


spider_template = '''# coding:utf-8

from bs4 import BeautifulSoup
import requests
from common.untils import *


def crawler_template_name_information(url):
    # 数据获取
    resp_data = get_template_name_data()
    # 解析数据
    data = analysis_template_name_data(resp_data)
    return data
'''

get_spider_template = '''
def get_template_name_data():
    respon = requests.post(target_url)
    return respon.text
'''

analysis_data = '''

def analysis_template_name_data(resp_data):
    crawler_ls = []
    for x in resp_data:
    return crawler_ls
'''


information_database_file_template = '''
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_template_name import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from database.coin_world_modle import PublicInformation
from database.new_flash_model import NewFlashInformation
from celerymain.main import app
from common.initlog import Logger

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def template_name_information(url):
    crawler_data = crawler_template_name_information(url)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s_%s" % (RedisConstantsKey.CRAWLER_PUBLIC_INFORMATION.value, data["source_name"], data["content_id"]))
            if cache_data is not None:
                str1 = str_convert_json(cache_data)
                distance = get_str_distance(data["content"], str1["content"])
                # 去重队列
                query_data = public_is_exist_data(data["content_id"], data["source_name"])
                if query_data:
                    connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                         json_convert_str(data))
                if distance > GetListLength.GET_NOMBAL_NUM.value:
                    PublicInformation.update(content=data["content"]).where(PublicInformation.content_id ==
                                                                               data["content_id"])
                    connetcredis().set("%s_%s_%s" % (RedisConstantsKey.CRAWLER_PUBLIC_INFORMATION.value, data["source_name"], data["content_id"]),
                                       json_convert_str(data))
            else:
                connetcredis().set("%s_%s_%s" % (RedisConstantsKey.CRAWLER_PUBLIC_INFORMATION.value, data["source_name"], data["content_id"]),
                                   json_convert_str(data))
                # 去重队列
                connetcredis().lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
                                     json_convert_str(data))
                PublicInformation.create(
                    content=data["content"],
                    content_id=data["content_id"],
                    title=data["title"],
                    source_name=data["source_name"]
                )


def public_is_exist_data(content_id, source_name):
    query_data = NewFlashInformation.select().where(
        NewFlashInformation.content_id == content_id,
        NewFlashInformation.source_name == source_name)
    return query_data


@app.task(ignore_result=True)
def schudule_template_name_information():
    app.send_task('crawler.template_name.template_name_information', args=("template_url",),
                  queue='template_name_task',
                  routing_key='template_name_info')
'''

news_database_file_template = '''
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from spiders.spider_template_name import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey, GetListLength, DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
from database.eight_bite_information_model import PublicNews

logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def template_name_information(url):
    crawler_data = crawler_template_name_information(url)
    if len(crawler_data) != GetListLength.GET_LIST_LENGTH.value:
        for data in crawler_data:
            cache_data = connetcredis().get("%s_%s_%s" % (RedisConstantsKey.CRAWLER_PUBLIC_NEWS.value, data["source_name"], data["content_id"]))
            if cache_data is None:
                try:
                    PublicNews.create(
                        content_id=data["content_id"],
                        content=data["content"],
                        source_name=data["source_name"],
                        title=data["title"],
                        author=data["author"],
                        img=data["match_img"],
                        crawler_url=data["url"]
                    )
                except Exception as e:
                    logger.error("比特币资讯网抓取持久化出错:%s" % e)
                connetcredis().set("%s_%s_%s" % (RedisConstantsKey.CRAWLER_PUBLIC_NEWS.value, data["source_name"], data["content_id"]),
                                   json_convert_str(data))
            # 去重队列
            connetcredis().lpush(
                DuplicateRemovalCache.FIRST_INFO_DUPLICATE_REMOVAL_CACHE.value,
                json_convert_str(data))


@app.task(ignore_result=True)
def schudule_template_name_information():
    app.send_task('crawler.template_name.template_name_information', args=("template_url",),
                  queue='template_name_task',
                  routing_key='template_name_info')
'''


# 动态生成爬虫模板
def spiders_template():
    rule_ls = spider_rule_data()

    # 生成爬虫模板
    get_spiders_template(rule_ls)

    # 生成数据库文件
    save_spiders_template(rule_ls)
    # 修改爬虫配置
    modify_spiders_template(rule_ls)


# 生成爬虫模板
def get_spiders_template(rule_ls):
    if isinstance(rule_ls, list):
        for x in rule_ls:
            # 生成数据获取方法模板
            req_headers = str_convert_json(x["req_headers"]) if x["req_headers"] else x["req_headers"]
            resopn = public_requests_method(x["req_method"], x["target_url"], req_headers, x["req_params"], x["req_code"])

            new_spider_template = spider_template.replace("template_name", x["spider_en_name"].strip())
            new_get_spider_template = get_spider_template.replace("template_name", x["spider_en_name"].strip())
            new_get_spider_template = new_get_spider_template.replace("requests.post(target_url)", resopn)

            # 获取列表
            # dom
            if x["ls_rule_type"] == 0:
                ls_rule = x["html_ls_tag"].split("=>")
                ls_rule_len = len(ls_rule)
                if ls_rule_len == 1:
                    tmp = 'soup = BeautifulSoup(resp_data, "html.parser")\n    data = soup.%s\n    for x in data[:%s]:\n        dic = {}\n        dic["source_name"] = "%s"' % (ls_rule[0], x["get_num"], x["spider_en_name"].strip())
                    colunm = ""
                    for y in x["crawler_column"]:
                        if y["get_data_way"] == 0:
                            column_tag_ls = y["get_column_rule"].split("=>")
                            if len(column_tag_ls) == 1:
                                colunm_rule = 'dic["%s"] = x.%s' % (y["en_name"], column_tag_ls[0])
                        elif y["get_data_way"] == 1:
                            column_rule_ls = y["get_column_rule"].split("=>")
                            if len(column_rule_ls) == 1:
                                if y["en_name"] == "content_id":
                                    colunm_rule = 'dic["content_id"] = dic["details_url"].%s' % column_rule_ls[0]
                                else:
                                    colunm_rule = 'response = requests.get(dic["details_url"])\n        detail = BeautifulSoup(response.text, "lxml")\n        dic["%s"] = detail.%s' % (y["en_name"], column_rule_ls[0])
                        colunm = colunm + colunm_rule + "\n        "
                    tmp = tmp + "\n        " + colunm + "crawler_ls.append(dic)"
                elif ls_rule_len == 2:
                    tmp = 'soup = BeautifulSoup(resp_data, "html.parser")\n    data = soup.%s\n    data = data.%s\n    for x in data[:%s]:\n        dic = {}\n        dic["source_name"] = "%s"' % (ls_rule[0], ls_rule[1], x["get_num"], x["spider_en_name"].strip())
                    colunm = ""
                    for y in x["crawler_column"]:
                        if y["get_data_way"] == 0:
                            column_tag_ls = y["get_column_rule"].split("=>")
                            if len(column_tag_ls) == 1:
                                colunm_rule = 'dic["%s"] = x.%s' % (y["en_name"], column_tag_ls[0])
                        elif y["get_data_way"] == 1:
                            column_rule_ls = y["get_column_rule"].split("=>")
                            if len(column_rule_ls) == 1:
                                if y["en_name"] == "content_id":
                                    colunm_rule = 'dic["content_id"] = dic["details_url"].%s' % column_rule_ls[0]
                                else:
                                    colunm_rule = 'response = requests.get(dic["details_url"])\n        detail = BeautifulSoup(response.text, "lxml")\n        dic["%s"] = detail.%s' % (y["en_name"], column_rule_ls[0])
                        colunm = colunm + colunm_rule + "\n        "
                    tmp = tmp + "\n        " + colunm + "crawler_ls.append(dic)"
                elif ls_rule_len == 2:
                    if "@" in ls_rule[0]:
                        column_tag_ls = ls_rule[0].split("@")
                        tmp = 'soup = BeautifulSoup(resp_data, "html.parser")\n    content_soup = soup.find("%s", "%s")\n    data=content_soup.find_all("%s")\n    for x in data[:%s]:\n        dic = {}\n        dic["source_name"] = "%s"' % \
                              (column_tag_ls[0], column_tag_ls[1], ls_rule[1], x["get_num"], x["spider_en_name"].strip())
                        for y in x["crawler_column"]:
                            if y["get_data_way"] == 0:
                                if y["column_rule_type"] == 0:
                                    if "=>" in y["get_column_rule"]:
                                        ls_rule = y["get_column_rule"].split("=>")
                                        ls_rule_len = len(ls_rule)
                                        if ls_rule_len == 2:
                                            print("mmmm")
                                    else:
                                        print("nnn")
                            elif y["get_data_way"] == 1:
                                print("kkkk")
            elif x["ls_rule_type"] == 1:
                ls_rule = x["html_ls_tag"].split("=>")
                ls_rule_len = len(ls_rule)
                if ls_rule_len == 2:
                    if ("{}" or "[]") not in ls_rule[0]:
                        a = 'data["%s"]' % ls_rule[0]
                    if "{}" in ls_rule[1]:
                         if "|" in ls_rule[1]:
                            ls_rule_dict = ls_rule[1].split("|")[1]
                            # 获取内容
                            tmp = '''resp_data = str_convert_json(resp_data)\n    if resp_data.__contains__("%s"):\n        for x in resp_data["%s"]["%s"]:\n            dic = {}''' % (ls_rule[0], ls_rule[0], ls_rule_dict)
                            for y in x["crawler_column"]:
                                if y["get_data_way"] == 0:
                                    if y["column_rule_type"] == 0:
                                        print("cccc")
                                    elif y["column_rule_type"] == 1:
                                        colunm = 'dic["%s"] = x["%s"]' % (y["en_name"], y["get_column_rule"])
                                        tmp = tmp + "\n            "+colunm
                            tmp = tmp + "\n            crawler_ls.append(dic)"
                         else:
                            tmp = 'resp_data = str_convert_json(resp_data)\n    for date_key in resp_data["%s"].keys():\n        ls = resp_data["%s"]' % (
                                ls_rule[0], ls_rule[0]) + '["%s" % date_key]'
                            tmp = tmp + "\n        " + 'for x in ls:\n            dic = {}'
                            for y in x["crawler_column"]:
                                if y["get_data_way"] == 0:
                                    if y["column_rule_type"] == 0:
                                        print("cccc")
                                    elif y["column_rule_type"] == 1:
                                        colunm = 'dic["%s"] = x["%s"]' % (y["en_name"], y["get_column_rule"])
                                        tmp = tmp + "\n            " + colunm
                            tmp = tmp + "\n            crawler_ls.append(dic)"
                if ls_rule_len == 3:
                    if "{}" in ls_rule[1]:
                        if "|" not in ls_rule[1]:
                            tmp = 'resp_data = str_convert_json(resp_data)\n    for date_key in resp_data["%s"].keys():\n        ls = resp_data["%s"]' % (
                                ls_rule[0], ls_rule[0]) + '["%s" % date_key]'
                    if "{}" in ls_rule[2]:
                        if "|" in ls_rule[2]:
                            ls_rule_dict = ls_rule[2].split("|")[1]
                            tmp = tmp + "\n        " + 'for x in ls["%s"]:\n            dic = {}' % (ls_rule_dict)
                            for y in x["crawler_column"]:
                                if y["get_data_way"] == 0:
                                    if y["column_rule_type"] == 0:
                                        print("cccc")
                                    elif y["column_rule_type"] == 1:
                                        colunm = 'dic["%s"] = x["%s"]' % (y["en_name"], y["get_column_rule"])
                                        tmp = tmp + "\n            "+colunm
                            tmp = tmp + "\n            crawler_ls.append(dic)"
            analysis_data_template = analysis_data.replace("template_name", x["spider_en_name"].strip())
            analysis_data_template = analysis_data_template.replace("for x in resp_data:", tmp)

            # 创建爬虫文件
            file_path = "../spiders/spider_%s.py" % x["spider_en_name"].strip()
            # if not os.path.exists(file_path):
            file_object = open(file_path, 'w')
            file_object.write(new_spider_template)
            file_object.write("\n")
            file_object.write(new_get_spider_template)
            file_object.write(analysis_data_template)
            file_object.close()


def save_spiders_template(rule_ls):
    if isinstance(rule_ls, list):
        for x in rule_ls:
            # 创建数据库文件
            if x["information_type"] == 0:
                information_template = information_database_file_template.replace("template_name", x["spider_en_name"])
                information_template = information_template.replace("template_url", x["target_url"])
            elif x["information_type"] == 1:
                information_template = news_database_file_template.replace("template_name", x["spider_en_name"])
                information_template = information_template.replace("template_url", x["target_url"])

            file_path = "../crawler/%s.py" % x["spider_en_name"].strip()
            file_object = open(file_path, 'w')
            file_object.write(information_template)
            file_object.close()


# 修改爬虫配置
def modify_spiders_template(rule_ls):
    if isinstance(rule_ls, list):
        for x in rule_ls:
            # 读取配置文件
            config_file = "../config/crawler.json"
            with open(config_file, "r") as fi:
                load_dict = json.load(fi)
                if load_dict.__contains__('celery'):
                    if "crawler.%s" % x["spider_en_name"].strip() not in load_dict["celery"]["celery_imports"]:
                        load_dict["celery"]["celery_imports"].append("crawler.%s" % x["spider_en_name"].strip())
                        load_dict["celery"]["celery_queues"].append({"exchange": "%s_task" % x["spider_en_name"],
                                                                     "routing_key": "%s_info" % x["spider_en_name"],
                                                                     "queue": "%s_task" % x["spider_en_name"]})
                        load_dict["celery"]["celerybeat_schedule"].append(
                            {"schedule_name": "crawler_%s" % x["spider_en_name"],
                             "task": "crawler.%s.schudule_%s" % (x["spider_en_name"], x["spider_en_name"]),
                             "schedule": x["time_interval"],
                             "routing_key": "%s_info" % x["spider_en_name"],
                             "queue": "%s_task" % x["spider_en_name"]})
            # 修改配置文件
            with open(config_file, "w") as fw:
                json.dump(load_dict, fw, indent=1)
                fw.close()


# 获取爬虫规则
def spider_rule_data():
    base_sql = SpidersVisualizationBase.select().where(SpidersVisualizationBase.is_userful == 1)
    base_ls = model_to_dicts(base_sql)
    for x in base_ls:
        rule_sql = SpidersVisualizationRule.select().where(SpidersVisualizationRule.base_id == x["id"])
        rule_ls = model_to_dicts(rule_sql)
        for y in rule_ls:
            data_handle_sql = SpidersVisualizationDataHandle.select().where(SpidersVisualizationDataHandle.rule == y["id"])
            data_handle_ls = model_to_dicts(data_handle_sql)
            y["data_handle"] = data_handle_ls
        x["crawler_column"] = rule_ls
    return base_ls


if __name__ == "__main__":
    spiders_template()