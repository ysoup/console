import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

import requests
from bs4 import BeautifulSoup
# from common.get_content import Extractor
import re
from common.untils import *





def crawler_okex_information(url, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
    }
    response = requests.get(url, headers=headers)
    logger.info("抓取okex返回http状态码:%s" % response.status_code)
    soup = BeautifulSoup(response.text, "lxml")
    lis = soup.find("ul", class_="article-list").find_all("li", class_="article-list-item article-promoted")[:5]
    crawler_ls = []
    for li in lis:
        dic = {}
        title = li.a.string
        link = li.a.get("href")
        source_link = "https://support.okex.com" + link
        content_id = link.split("/")[-1].split("-")[0]
#         继续抓取内容
        resp = requests.get(source_link, headers=headers)
        cont_soup = BeautifulSoup(resp.text, "lxml")
        p_ls = cont_soup.find("div", class_="article-body").find_all("p")
        content = ""
        for p in p_ls:
            content = content + p.text
        source_name = "OKEx"
        dic["title"] = title
        dic["source_link"] = source_link
        dic["content_id"] = content_id
        dic["content"] = content
        dic["source_name"] =source_name
        crawler_ls.append(dic)
    return crawler_ls





