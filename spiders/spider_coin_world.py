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


def crawler_coin_world_information(url, logger):
    response = requests.get(url)
    logger.info("抓取币世界http返回状态码:%s" % response.status_code)
    data = str_convert_json(response.text)
    crawler_ls = []
    modfiy_ls = ["币世界", "小葱", "金色财经", "币 世 界"]
    if data.__contains__('data'):
        for date_key in data["data"].keys():
            coin_world_ls = data["data"]["%s" % date_key]
            if coin_world_ls.__contains__('buttom'):
                for coin_world_data in coin_world_ls["buttom"]:
                    dic = {}
                    dic["content"] = coin_world_data["content"]
                    num = re.search("微信", dic["content"])
                    if num is not None:
                        continue
                    dic["modify_tag"] = 0
                    for x in modfiy_ls:
                        if x in dic["content"]:
                            dic["modify_tag"] = 1
                            break
                    dic["content"] = re.sub("币世界|小葱|金色财经|币 世 界|bishijie.com|bishijie|《币 世 界》（bishijie.com）|"
                                            "《币世界》（bishijie）", "爱必投", dic["content"])
                    dic["content_id"] = coin_world_data["newsflash_id"]
                    dic["source_link"] = ""
                    dic["title"] = ""
                    dic["author"] = ""
                    dic["source_name"] = "coin_world"
                    crawler_ls.append(dic)
    logger.info("抓取币世界返回数据:%s" % crawler_ls)
    return crawler_ls


def crawler_coin_world_market(url):
    response = requests.get(url)
    data = BeautifulSoup(response.text, "html.parser")
    # print(data.find(id="coinTable"))