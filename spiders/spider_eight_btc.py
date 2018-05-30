# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
import requests
from bs4 import BeautifulSoup
from common.get_content import Extractor
import re


def crawler_eight_btc_information(url, logger):
    response = requests.get(url)
    # testreg = re.compile(r'<a[\s\S]*?href=[\'|"]([\s\S]*?)[\'|"][\s\S]*?')
    soup = BeautifulSoup(response.text, "lxml")
    li = soup.find_all("li", "itm itm_new")
    ls = []
    for li in li[0:1]:
        dic = {}
        url = li.a.get("href")
        content_url = "http://www.8btc.com" + url
        resp = requests.get(content_url)
        content_soup = BeautifulSoup(resp.text, "lxml")
        author_ls = content_soup.find_all("div", "single-crumbs clearfix")
        try:
            dic["author"] = author_ls[0].find_all("span")[1].text.strip()
        except Exception as e:
            logger.error("抓取巴比特出错%s" % e)
            dic["author"] = ""
        dic["title"] = content_soup.find_all("div", "article-title")[0].text.strip()
        a = content_soup.find_all("div", "article-content")[0]
        if a.div is not None:
            a.div.extract()
        if a.div is not None:
            a.div.extract()
        if a.div is not None:
            a.div.extract()
        a_ls = a.find_all('a')
        for x in a_ls:
            si_tag = x.previous_sibling
            if "strong" in str(si_tag):
                a = str(a).replace(str(si_tag), "")
                a = a.replace(str(x), "")
            else:
                if x.img is None:
                    tag_text = x.text
                    a = str(a).replace(str(x), str(tag_text))
                else:
                    a = str(a).replace(str(x), str(x.img))

        del_div = re.compile(r'<div[\s\S]*?>|</div>')
        dic["content"] = del_div.sub('', str(a)).strip()
        dic["match_img"] = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(dic["content"])
        dic["match_img"] = ",".join(dic["match_img"])
        dic["url"] = content_url
        dic["source_name"] = "eight_btc"
        logger.info("抓取巴比特http返回状态码:%s" % response.status_code)
        ls.append(dic)
        
    return ls