# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from common.untils import *
import re


def crawler_jinse(url, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.167 Safari/537.36',
        'Cookie': 'userId=eyJpdiI6InNhdlJ3Z3U2VVo4bmtTMUo5QXFKaHc9PSIsInZhbHVlIjoiMHNpNDd4XC9jZ3lnOWdSZk1oejdXMGVFRnpONmhhcHRRRU85QWpiNFFLVDlNaGxOZXVZYnhGa2xuYzVtdWV1d2c3cjZUM0Q3aTRJVjZKajBTeWNGVWJnPT0iLCJtYWMiOiI1ZjJlYTFlYTk0MmI5OTRmNTM2MDE0Njk5MTg5YmEzZTE2ZmJlNjhlN2ZkNDE5MjQwNDQzOTc5OWQxNzcyZTY0In0%3D; _ga=GA1.2.2033234795.1520214260; Hm_lvt_3b668291b682e6dc69686a3e2445e11d=1520214261,1520305984,1521512564; Hm_lpvt_3b668291b682e6dc69686a3e2445e11d=1521512564; _gid=GA1.2.134251051.1521512565; _gat=1'
    }
    response = requests.get(url, headers=headers)
    crawler_ls = []
    logger.info("抓取金色财经http返回状态码:%s" % response.status_code)
    if response.status_code == 200:
        data = str_convert_json(response.text)
        if data.__contains__('data'):
            for date_key in data["data"].keys():
                for ls in data["data"]["%s" % date_key]:
                    dic = {}
                    dic["content"] = ls["content"]
                    num = re.search("微信", dic["content"])
                    if num is not None:
                        continue
                    dic["content"] = re.sub("币世界|小葱|金色财经", "爱必投", dic["content"])
                    dic["source_link"] = ""
                    dic["content_id"] = ls["id"]
                    dic["source_name"] = "jin_se"
                    dic["title"] = ""
                    dic["author"] = ""
                    crawler_ls.append(dic)
    logger.info("抓取金色财经返回数据:%s" % crawler_ls)
    return crawler_ls