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
import requests
logger = Logger(kind="work_path", name="duplicate_removal")

spider_template = '''# coding:utf-8

import requests


def crawler_template_name_information(logger):
    # 数据获取
    data = get_template_name_data()
    # 解析数据
    data = analysis_template_name_data()
    # 数据预处理
    data = handle_template_name_data()
    return data
'''

get_spider_template = '''
def get_template_name_data():
    respon = requests.post(target_url)
    return respon.text
'''

analysis_data = '''
def analysis_template_name_data():

'''



# 动态生成爬虫模板
def spiders_template():
    print("aaa")
    rule_ls = spider_rule_data()
    # 生成爬虫模板
    get_spiders_template(rule_ls)
    # 修改爬虫配置


# 生成爬虫模板
def get_spiders_template(rule_ls):
    if isinstance(rule_ls, list):
        for x in rule_ls:
            resopn = public_requests_method(x["req_method"], x["target_url"], x["req_headers"])
            # 生成数据获取方法模板
            new_spider_template = spider_template.replace("template_name", x["spider_en_name"].strip())
            new_get_spider_template = get_spider_template.replace("template_name", x["spider_en_name"].strip())
            new_get_spider_template = new_get_spider_template.replace("requests.post(target_url)", resopn)
            # 获取列表
            if x["ls_rule_type"] == 0:
                print("ffff")
            elif x["ls_rule_type"] == 1:
                ls_rule = x["html_ls_tag"].split("=>")
                ls_rule_len = len(ls_rule)
                if ls_rule_len ==2:
                    if ("{}" or "[]") not in ls_rule[0]:
                        a = 'data["%s"]' % ls_rule[0]
                    if "{}" in ls_rule[1]:
                         if "|" in ls_rule[1]:
                            ls_rule_dict = ls_rule[1].split("|")[1]
                            ls_rule_template = '''                            
                            if data.__contains__("%s"):
                                for x in data["%s"]["%s"]:
                            ''' % (ls_rule[0], ls_rule[0], ls_rule_dict)
                            if data.__contains__(ls_rule[0]):
                                b = data[ls_rule[0]][ls_rule_dict]
                                for x in data[ls_rule[0]][ls_rule_dict]:
                            # 抓取字段
                         else:
                             print("dddd")
                if ls_rule_len ==3:
                    print("cccc")
            # 获取字段内容
            for c in b:

            for column in x["crawler_column"]:
                if column["column_rule_type"] == 0:

            # 创建爬虫文件
            file_object = open("%s.py" % x["spider_en_name"].strip(), 'w')
            file_object.write(new_spider_template)
            file_object.write("\n")
            file_object.write(new_get_spider_template)
            file_object.close()

            print(new_spider_template)
            print(new_get_spider_template)
            print(x)


# 获取爬虫规则
def spider_rule_data():
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
    return base_ls


def crawler_spider_template_information():
    # 数据获取
    data = get_spider_template_data()
    # 解析数据
    data = analysis_spider_template_data()
    # 数据预处理
    data = handle_spider_template_data()

    return data


if __name__ == "__main__":
    spiders_template()