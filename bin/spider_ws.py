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


def crawler_template_name_information():
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


# 动态生成爬虫模板
def spiders_template():
    rule_ls = spider_rule_data()
    # 生成爬虫模板
    get_spiders_template(rule_ls)
    # 修改爬虫配置


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
                    if "." in x["html_ls_tag"]:
                        html_tag = x["html_ls_tag"].split(".")
                        extarct_html_tag = html_tag[1].split("=")
                        if extarct_html_tag[0] == "class":
                            tmp = 'soup = BeautifulSoup(resp_data, "html.parser")\n    data = soup.find_all("%s", "%s")\n    for x in data[:%s]:\n        dic = {}\n        dic["source_name"] = "%s"' % \
                                  (html_tag[0], extarct_html_tag[1], x["get_num"], x["spider_en_name"].strip())
                            for y in x["crawler_column"]:
                                if y["get_data_way"] == 0:
                                    if y["column_rule_type"] == 0:
                                        if "=>" not in y["get_column_rule"]:
                                            if "." in y["get_column_rule"]:
                                                column_tag_ls = y["get_column_rule"].split(".")
                                                if "=" not in column_tag_ls[1]:
                                                    if column_tag_ls[1] == "text":
                                                        if ("[" and "]") in column_tag_ls[0]:
                                                            get_html_tag = column_tag_ls[0].split(" ")
                                                        else:
                                                            colunm = 'dic["%s"] = x.find("%s").%s' % (y["en_name"], column_tag_ls[0], column_tag_ls[1])
                                                    elif column_tag_ls[1] == "href":
                                                        if ("[" and "]") in column_tag_ls[0]:
                                                            get_html_tag = column_tag_ls[0].split(" ")
                                                        else:
                                                            colunm = 'dic["%s"] = x.find("%s").get("%s")' % (y["en_name"], column_tag_ls[0], column_tag_ls[1])
                                        else:
                                            colunm = 'dic["%s"] = x["%s"]' % (y["en_name"], y["get_column_rule"])
                                elif y["get_data_way"] == 1:
                                    colunm = 'response = requests.get(dic["detail_url"])\n        detail = BeautifulSoup(response.text, "lxml")'
                                    if y["column_rule_type"] == 0:
                                        if "=>" not in y["get_column_rule"]:
                                            if "." in y["get_column_rule"]:
                                                column_tag_ls = y["get_column_rule"].split(".")
                                                if "=" not in column_tag_ls[1]:
                                                    if column_tag_ls[1] == "text":
                                                        if ("[" and "]") in column_tag_ls[0]:
                                                            get_html_tag = column_tag_ls[0].split(" ")
                                                            colunm = colunm + '\n        ' + 'dic["%s"] = detail.find_all("%s")%s.text' % (y["en_name"], get_html_tag[0], get_html_tag[1])
                                        else:
                                            print("jjj")
                                tmp = tmp + "\n        " + colunm
                            tmp = tmp + "\n        crawler_ls.append(dic)"
                        elif html_tag[0] == "id":
                            print("aaaa")
                    else:
                        tmp = 'soup = BeautifulSoup(resp_data, "html.parser")\n    data = soup.find_all("%s")\n    for x in data[:%s]:\n        dic = {}\n        dic["source_name"] = "%s"' % (x["html_ls_tag"], x["get_num"], x["spider_en_name"].strip())
                        for y in x["crawler_column"]:
                            if y["get_data_way"] == 0:
                                if y["column_rule_type"] == 0:
                                    if "=>" not in y["get_column_rule"]:
                                        if "." in y["get_column_rule"]:
                                            column_tag_ls = y["get_column_rule"].split(".")
                                            if "=" not in column_tag_ls[1]:
                                                if column_tag_ls[1] == "text":
                                                    if ("[" and "]") in column_tag_ls[0]:
                                                        get_html_tag = column_tag_ls[0].split(" ")
                                                    else:
                                                        colunm = 'dic["%s"] = x.find("%s").%s' % (
                                                        y["en_name"], column_tag_ls[0], column_tag_ls[1])
                                                elif column_tag_ls[1] == "href":
                                                    if ("[" and "]") in column_tag_ls[0]:
                                                        get_html_tag = column_tag_ls[0].split(" ")
                                                    else:
                                                        colunm = 'dic["%s"] = x.find("%s").get("%s")' % (
                                                        y["en_name"], column_tag_ls[0], column_tag_ls[1])
                                            else:
                                                extarct_html_tag = column_tag_ls[1].split("=")
                                                if extarct_html_tag[0] == "class":
                                                    colunm = 'dic["%s"] = x.find("%s", "%s").text' % (y["en_name"], column_tag_ls[0], extarct_html_tag[1])
                                    else:
                                        colunm = 'dic["%s"] = x["%s"]' % (y["en_name"], y["get_column_rule"])
                            elif y["get_data_way"] == 1:
                                colunm = 'response = requests.get(dic["detail_url"])\n        detail = BeautifulSoup(response.text, "lxml")'
                                if y["column_rule_type"] == 0:
                                    if "=>" not in y["get_column_rule"]:
                                        if "." in y["get_column_rule"]:
                                            column_tag_ls = y["get_column_rule"].split(".")
                                            if "=" not in column_tag_ls[1]:
                                                if column_tag_ls[1] == "text":
                                                    if ("[" and "]") in column_tag_ls[0]:
                                                        get_html_tag = column_tag_ls[0].split(" ")
                                                        colunm = colunm + '\n        ' + 'dic["%s"] = detail.find_all("%s")%s.text' % (
                                                        y["en_name"], get_html_tag[0], get_html_tag[1])
                                    else:
                                        print("jjj")
                            tmp = tmp + "\n        " + colunm
                        tmp = tmp + "\n        crawler_ls.append(dic)"
                elif ls_rule_len == 2:
                    if "@" in ls_rule[0]:
                        column_tag_ls = ls_rule[0].split("@")
                        tmp = 'soup = BeautifulSoup(resp_data, "html.parser")\n    content_soup = soup.find("%s", "%s")\n    data=content_soup.find_all("%s")\n    for x in data[:%s]:\n        dic = {}\n        dic["source_name"] = "%s"' % \
                              (column_tag_ls[0], column_tag_ls[1], ls_rule[1], x["get_num"], x["spider_en_name"].strip())
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
            file_object = open("%s.py" % x["spider_en_name"].strip(), 'w')
            file_object.write(new_spider_template)
            file_object.write("\n")
            file_object.write(new_get_spider_template)
            # file_object.write("\n")
            file_object.write(analysis_data_template)
            file_object.close()

            # print(new_spider_template)
            # print(new_get_spider_template)
            # print(x)


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