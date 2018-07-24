# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re


def crawler_wang_yi_information(url, logger):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    data = soup.find_all("ul", "newsList")[0].find_all("li")
    ls = []
    for li in data[0:5]:
        dic = {}
        dic["title"] = li.find("h3").text
        content_url = li.find("h3").find("a").get("href")
        dic["content_id"] = content_url.split("/")[-1].split(".")[0]
        home_img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(li))
        resp = requests.get(content_url)
        content_soup = BeautifulSoup(resp.text, "html.parser")
        dic["author"] = content_soup.find("a", id="ne_article_source").text
        content = content_soup.find_all("div", "post_text")[0]
        if content.div is not None:
            content.div.extract()
        span_ls = content.find_all("span")
        if len(span_ls) != 0:
            content.span.extract()
            content.span.extract()
        img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(content))
        if len(home_img_ls) > 0:
            img_ls.insert(0, home_img_ls[0])
        dic["match_img"] = ",".join(img_ls)
        dic["url"] = content_url
        dic["source_name"] = "wang_yi"
        dic["content"] = str(content)
        ls.append(dic)

    return ls