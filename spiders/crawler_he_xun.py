import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

import requests
from bs4 import BeautifulSoup
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
        dic["url"] = data[1]
        dic["content_id"] = int(data[1].split("/")[-1].split(".")[0])
        dic["match_img"] = data[2]
        dic["crawler_date"] = data[4]
        dic["source_name"] = "he_xun"
        dic["author"] = ""

        # 抓取内容
        resp = requests.get(data[1], headers=headers)
        resp.encoding = "gb2312"
        cont_soup = BeautifulSoup(resp.text, "lxml")
        content_all = cont_soup.find("div", class_="art_contextBox")
        imgs = content_all.find_all("img")
        if len(imgs):
            for i in imgs:
                dic["match_img"] += " , " + i.get("src")

        filter_div = content_all.find("div", style="text-align:right;font-size:12px")
        dic["content"] = str(content_all).replace(str(filter_div), "")
        crawler_ls.append(dic)
    return crawler_ls







