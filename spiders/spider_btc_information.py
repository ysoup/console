# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from bs4 import BeautifulSoup


def crawler_btc_information(url, logger):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    logger.info("抓取币世界http返回状态码:%s" % response.status_code)
    ls = soup.find_all("div", "article-title article-title_news")
    crawler_ls = []
    for x in ls[0:5]:
        dic = {}
        a_tag = x.find("a")
        dic["title"] = a_tag.text
        dic["content"] = x.find("div", "fast_news_content").text
        dic["content_id"] = str(a_tag.get("href").split("/")[-1])
        dic["source_link"] = ""
        dic["author"] = ""
        dic["source_name"] = "btc_news"
        crawler_ls.append(dic)
    logger.info("抓取币世界返回数据:%s" % crawler_ls)
    return crawler_ls