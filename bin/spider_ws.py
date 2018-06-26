# coding:utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
# from common.initRedis import connetcredis
# from common.untils import *
from database.spiders_visualization_modle import *
from common.initlog import Logger
from common.db_utils import *

logger = Logger(kind="work_path", name="duplicate_removal")


# 获取爬虫规则
def spider_base_rule():
    print("aaa")
    base_sql = SpidersVisualizationBase.select().where(SpidersVisualizationBase.is_userful == 1)
    base_ls = model_to_dicts(base_sql)
    for x in base_ls:
        rule_sql = SpidersVisualizationRule.select().where(SpidersVisualizationRule.base_id == x["id"])
        rule_ls = model_to_dicts(rule_sql)
        for y in rule_ls:
            data_handle_sql = SpidersVisualizationDataHandle.select().where(SpidersVisualizationDataHandle.rule == y["id"])
            data_handle_ls = model_to_dicts(data_handle_sql)
            y["data_handle"] = data_handle_ls
        x["crawler_column"] = y
        yield spiders_template(x)


# 动态生成爬虫模板
def spiders_template(rule_data):
    print("aaa")
    # 生成爬虫模板
#     get_spider_template(rule_data)
#     # 修改爬虫配置
#
#
# def get_spider_template(rule_data):
#     print("aaaa")


if __name__ == "__main__":
    spider_base_rule()