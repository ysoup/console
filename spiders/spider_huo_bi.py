# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from common.untils import *
from bs4 import BeautifulSoup
import re


def crawler_huo_bi_information(url, logger):
    response = requests.get(url)
    logger.info("抓取火币 http返回状态码:%s" % response.status_code)
    data = str_convert_json(response.text)
    crawler_ls = []
    if data["message"] == "success":
        if data["data"].__contains__('items'):
            data = data["data"]["items"]
            if len(data) >= 5:
                crawler_ls = [{"content_id": x["id"], "content": x["content"], "title": x["title"],
                               "source_name": "huo_bi", "author": "", "source_link": ""} for x in data[0:5]]
            else:
                crawler_ls = [{"content_id": x["id"], "content": x["description"], "title": x["title"],
                               "source_name": "huo_bi", "author": "", "source_link": ""} for x in data]
    logger.info("抓取火币返回数据:%s" % crawler_ls)
    return crawler_ls