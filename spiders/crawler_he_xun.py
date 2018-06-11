import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

import requests
import re
from common.untils import *


def crawler_he_xun_information(url, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
    }
    response = requests.get(url, headers=headers)
    logger.info("抓取和讯网http返回状态码: %s" % response.status_code)
    data_ls = response.text
    regx = re.compile("TradeTab_JsonData=|\[|\]")
    data_ls = regx.sub("", data_ls)
    reg = re.compile("title:'([\s\S]*?)',titleLink:'([\s\S]*?)',[\s\S]*?imgSrc:'([\s\S]*?)',[\s\S]*?newsInf:'([\s\S]*?)',dateInf:([\s\S]*?)}")
    data_ls = reg.findall(data_ls)
    crawler_ls = []
    for data in data_ls[:5]:
        dic = {}
        dic["title"] = data[0]
        dic["source_link"] = data[1]
        dic["content_id"] = int(data[1].split("/")[-1].split(".")[0])
        dic["img_link"] = data[2]
        dic["content"] = data[3]
        dic["crawler_date"] = data[4]
        dic["source_name"] = "he_xun"
        crawler_ls.append(dic)
    return crawler_ls







