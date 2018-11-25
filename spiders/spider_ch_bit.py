# coding:utf-8

from bs4 import BeautifulSoup
import requests
from common.untils import *


def crawler_ch_bit_information(url):
    # 数据获取
    resp_data = get_ch_bit_data()
    # 解析数据
    data = analysis_ch_bit_data(resp_data)
    return data


def get_ch_bit_data():
    respon = requests.get('https://cn.bitcoin.com/archives/category/bitebixinwen')
    return respon.text


def analysis_ch_bit_data(resp_data):
    crawler_ls = []
    soup = BeautifulSoup(resp_data, "html.parser")
    data = soup.find("td_block_template_1 widget widget_recent_entries")
    data = data.find_all("li")
    for x in data[:5]:
        dic = {}
        dic["source_name"] = "ch_bit"
        crawler_ls.append(dic)
    return crawler_ls
