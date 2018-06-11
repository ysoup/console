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
    headers = {
        'Host': 'www.huobi.pro',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN',
        'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.huobi.pro/zh-cn/notice/',
        'Connection': 'keep-alive',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'Cookie': 'cfduid=d3cf431d2b210181950519de3134cb2391528187007; gr_user_id=8e2c422d-33c2-434c-852f-f861e0706afa; _'
                  'ga=GA1.2.1144911038.1528187027; __zlcmid=mlhOSSHaEhm9Ih; SESSION=6c1f7ac1-b2a4-48c2-8743-95966f490624; '
                  '8838a5745a973a12_gr_session_id=45473dca-d234-4571-a1c4-ee5af4c37115_true; _'
                  'gid=GA1.2.1157397748.1528708624; _gat_UA-108346576-1=1'
    }
    response = requests.get(url, headers=headers)
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