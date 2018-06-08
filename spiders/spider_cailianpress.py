# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from common.untils import *
import re


def crawler_cailianpress_information(url, logger):
    response = requests.get(url)
    data = str_convert_json(response.text)
    logger.info("抓取財联社http返回状态码:%s" % response.status_code)
    crawler_ls = []
    data = data["data"]["roll_data"]
    if len(data) >= 5:
        crawler_ls = [{"content_id": x["id"], "content": fliter_content(x["content"]), "title": x["title"],
                       "source_name": "cailianpress", "author":"", "source_link": ""} for x in data[0:5]]
    else:
        crawler_ls = [{"content_id": x["id"], "content": fliter_content(x["content"]), "title": x["title"],
                       "source_name": "cailianpress", "author":"", "source_link": ""} for x in data]
    logger.info("抓取財联社返回数据:%s" % crawler_ls)
    return crawler_ls


def fliter_content(content):
    if "【" in content or "】" in content:
        return content.split("【")[-1].split("】")[-1]
    else:
        return content
    # reg = re.compile(r'<a.*?>([\s\S]*?)<\/a>')
    # re.findall(reg, content)