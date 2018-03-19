# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from common.untils import *


def crawler_jinse(url):
    response = requests.get(url)
    data = str_convert_json(response.text)
    crawler_ls = []
    if data.__contains__('data'):
        for date_key in data["data"].keys():
            for ls in data["data"]["%s" % date_key]:
                dic = {}
                dic["content"] = ls["content"]
                dic["content_id"] = ls["id"]
                dic["source_name"] = "jin_se"
                crawler_ls.append(dic)
    return crawler_ls