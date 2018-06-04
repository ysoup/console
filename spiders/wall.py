import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from bs4 import BeautifulSoup
from common.get_content import Extractor
import re
from common.untils import *

def crawler_wall_street_information(url,logger):
    response = requests.get(url)
    logger.info("抓取华尔街快讯http返回状态码:%s" % response.status_code)
    data = str_convert_json(response.text)
    crawler_ls = []
    if data.__contains__('data'):
        if data["data"].__contains__("items"):
            for items_ls in data["data"]["items"]:
                title_content = items_ls["content"].strip()
                dic = {}
                title_cont = re.findall("<p>(【([\s\S]*)】)?([\s\S]*)</p>",title_content)
                title = title_cont[0][1]
                content = title_cont[0][2]
                dic["title"] = title
                dic["content"] = content
                dic["source_name"] = "wall_street"
                crawler_ls.append(dic)
    logger.info("抓取华尔街快讯返回数据:%s" % crawler_ls)
    return crawler_ls