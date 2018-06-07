# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import json


def crawler_sina_information(url, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    response = requests.get(url, headers=headers)
    response.encoding = 'gb2312'
    soup = BeautifulSoup(response.text, "html.parser")
    ul = soup.find("ul", "list_009")
    li_ls = ul.find_all("li")
    ls = []
    for x in li_ls:
        dic = {}
        source_url = x.find("a").get("href")
        resp = requests.get(source_url)
        resp.encoding = 'utf-8'
        content_soup = BeautifulSoup(resp.text, "html.parser")
        data = content_soup.find_all("div", "article")
        dic["author"] = content_soup.find("span", "source ent-source").text
        dic["url"] = source_url
        dic["source_name"] = "sina"
        dic["title"] = x.text
        dic["content_id"] = source_url.split("/")[-1].split(".")[0]
        fliter_tag = data[0].find("p", "article-editor")
        data = str(data[0])
        img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(data)
        dic["match_img"] = ",".join(img_ls)
        dic["content"] = data.replace(str(fliter_tag), "")
        ls.append(dic)
    return ls