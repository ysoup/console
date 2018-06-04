# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from bs4 import BeautifulSoup
import json


def crawler_bian_information(url, logger):
    payload = {'page_no': 1, 'page_size': 5, 'search': ""}
    response = requests.post(url, data=json.dumps(payload))
    soup = BeautifulSoup(response.text, "lxml")
    logger.info("抓取鞭牛士http返回状态码:%s" % response.status_code)
    crawler_ls = []
    ls = soup.find_all("li")
    for x in ls[0:5]:
        dic = {}
        dic["title"] = x.find("div", "title").text
        dic["content"] = x.find("div", "content").text
        dic["content_id"] = x.get("id")
        dic["source_link"] = ""
        dic["author"] = ""
        dic["source_name"] = "bianews"
        crawler_ls.append(dic)
    logger.info("抓取鞭牛士返回数据:%s" % crawler_ls)
    return crawler_ls