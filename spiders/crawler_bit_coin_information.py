# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re


def crawler_bit_coin_information(url, logger):
    response = requests.get(url)
    # testreg = re.compile(r'<a[\s\S]*?href=[\'|"]([\s\S]*?)[\'|"][\s\S]*?')
    soup = BeautifulSoup(response.text, "lxml")
    li = soup.find_all("article", "excerpt excerpt-1")
    ls = []
    for li in li[0:9]:
        dic = {}
        url = li.a.get("href")
        content_url = "http://www.bitcoin86.com" + url
        dic["content_id"] = int(url.split("/")[-1].split(".")[0])
        #content_url = "http://www.bitcoin86.com/news/21327.html"
        resp = requests.get(content_url)
        resp.encoding = "UTF-8"
        content_soup = BeautifulSoup(resp.text, "lxml")
        # author_ls = content_soup.find_all("div", "single-crumbs clearfix")
        # dic["author"] = author_ls[0].find_all("span")[1].text.strip()
        dic["title"] = content_soup.find_all("h1", "article-title")[0].text.strip()
        a = content_soup.find_all("article", "article-content")[0]
        a.div.extract()
        ad = a.find_all("div", "ad akp-adv")
        if len(ad) != 0:
            a.div.extract()

        span_ls = a.find_all("span")
        if len(span_ls) != 0:
            a.span.extract()
        a.b.extract()
        # if len(span_obj_1) != 0:
        #     del_span_1 = re.compile(r'<span[\s\S]*?class="cc_by">[\s\S]*?|</span>')
        #     content_1 = del_span_1.sub('', str(a)).strip()
        # span_obj_2 = a.find_all("span", "source-info")
        # if len(span_obj_2) != 0:
        #     del_span_2 = re.compile(r'<span[\s\S]*?class="source-info">[\s\S]*?|</span>')
        #     del_span_2.sub('', str(a)).strip()
        del_div = re.compile(r'<article[\s\S]*?>|</article>')
        re_a_1 = re.compile(r'<a[\s\S]*?href=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
        dic["content"] = del_div.sub('', str(a)).strip()
        dic["content"] = re_a_1.sub('', dic["content"])

        re_a_2 = re.compile(r'</a>|<u>|</u>')
        dic["content"] = re_a_2.sub('', dic["content"])
        dic["match_img"] = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(dic["content"])
        dic["match_img"] = ",".join(dic["match_img"])
        dic["url"] = content_url
        dic["author"] = ""
        dic["source_name"] = "bit_coin"
        logger.info("抓取巴比特http返回状态码:%s" % response.status_code)
        ls.append(dic)

    return ls