# coding:utf-8

from bs4 import BeautifulSoup
import requests
from common.untils import *


def crawler_test_bian_information(url):
    # 数据获取
    resp_data = get_test_bian_data()
    # 解析数据
    data = analysis_test_bian_data(resp_data)
    return data


def get_test_bian_data():
    respon = requests.post('https://www.bianews.com/news/news_list?channel=flash&type=1', data={'page_no': 1, 'page_size': 5, 'search': ""}, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36'})
    return respon.text


def analysis_test_bian_data(resp_data):
    crawler_ls = []
    soup = BeautifulSoup(resp_data, "html.parser")
    data = soup.find_all("li")
    for x in data[:5]:
        dic = {}
        dic["source_name"] = "test_bian"
        dic["title"] = x.find("div", "title").text
        dic["content"] = x.find("div", "content").text
        dic["content_id"] = x.get("id")
        crawler_ls.append(dic)
    return crawler_ls
