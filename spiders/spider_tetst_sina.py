# coding:utf-8

from bs4 import BeautifulSoup
import requests
from common.untils import *


def crawler_tetst_sina_information(url):
    # 数据获取
    resp_data = get_tetst_sina_data()
    # 解析数据
    data = analysis_tetst_sina_data(resp_data)
    return data


def get_tetst_sina_data():
    respon = requests.get('http://roll.finance.sina.com.cn/finance/wh/btbxw/index.shtml', headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'})
    respon.encoding = 'gb2312'
    return respon.text


def analysis_tetst_sina_data(resp_data):
    crawler_ls = []
    soup = BeautifulSoup(resp_data, "html.parser")
    data = soup.find("ul", "list_009")
    data = data.find_all("li")
    for x in data[:5]:
        dic = {}
        dic["source_name"] = "tetst_sina"
        dic["details_url"] = x.find("a").get("href")
        dic["title"] = x.text
        response = requests.get(dic["details_url"])
        detail = BeautifulSoup(response.text, "lxml")
        dic["content"] = detail.find_all("div", "article")
        dic["content_id"] = dic["details_url"].split("/")[-1].split(".")[0]
        crawler_ls.append(dic)
    return crawler_ls
