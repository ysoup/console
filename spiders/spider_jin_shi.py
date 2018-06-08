import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from common.untils import *
import requests
import re

def crawler_jin_shi_information(url, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
    }
    response = requests.get(url, headers=headers)
    logger.info("抓取金十http返回状态码:%s" % response.status_code)
    data = response.text
    crawler_ls = []
    reg = re.compile('0#1#([\s\S]*?)#([\s\S]*?)#####0###([\s\S]*?)",')
    cont_ls = reg.findall(data)
    for cont in cont_ls[:5]:
        dic = {}
        dic["crawler_time"] = cont[0]
        dic["content"] = cont[1]
        dic["content_id"] = cont[2]
        dic["title"] = ""
        dic["author"] = ""
        dic["source_name"] = "jin_shi"
        crawler_ls.append(dic)
    logger.info("抓取金十返回数据:%s" % crawler_ls)
    return crawler_ls





