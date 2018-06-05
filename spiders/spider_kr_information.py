# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from bs4 import BeautifulSoup
import json


def crawler_kr_information(url, logger):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    logger.info("抓取36kr http返回状态码:%s" % response.status_code)
    crawler_ls = []
    data = json.loads(((soup.find_all("script")[6].text).split("var props=")[-1]).split(",locationnal=")[0])
    data = data["newsflashList|newsflash"]
    if len(data) >= 5:
        crawler_ls = [{"content_id": x["id"], "content": x["description"], "title": x["title"],
                       "source_name": "36kr", "author":"", "source_link": ""} for x in data[0:5]]
    else:
        crawler_ls = [{"content_id": x["id"], "content": x["description"], "title": x["title"],
                       "source_name": "36kr", "author":"", "source_link": ""} for x in data]
    logger.info("抓取36kr返回数据:%s" % crawler_ls)

    return crawler_ls