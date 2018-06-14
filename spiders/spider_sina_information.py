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
        flite_div_img = content_soup.find("div", "ct_hqimg")
        if flite_div_img is not None:
            data[0].div.extract()
        author_tag = content_soup.find("span", "source ent-source")
        if author_tag is None:
            author_tag = content_soup.find("a", "source ent-source")
            if author_tag is None:
                dic["author"] = ""
            else:
                dic["author"] = author_tag.text
        else:
            dic["author"] = author_tag.text
        dic["url"] = source_url
        dic["source_name"] = "sina"
        dic["title"] = x.text
        dic["content_id"] = source_url.split("/")[-1].split(".")[0]

        if len(data) > 0:
            fliter_tag = data[0].find("p", "article-editor")
            data = str(data[0])
            data = data.replace(str(fliter_tag), "")
        re_a_1 = re.compile(r'<a[\s\S]*?href=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
        dic["content"] = re_a_1.sub('', str(data))
        re_a_2 = re.compile(r'</a>|<u>|</u>')
        dic["content"] = re_a_2.sub('', dic["content"])
        img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(dic["content"])
        dic["match_img"] = ",".join(img_ls)
        ls.append(dic)
    return ls