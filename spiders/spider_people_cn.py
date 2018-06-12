import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)

import requests
from bs4 import BeautifulSoup
import re
from common.get_content import Extractor
from common.untils import *

def crawler_people_cn_information(url,logger):
    headers = {
        'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
    }
    response = requests.get(url, headers=headers)
    logger.info("爬取人民网资讯http返回状态码：%s" % response.status_code)
    response.encoding = "GB2312"
    soup = BeautifulSoup(response.text,"lxml")
    divs = soup.find_all("div",class_=" hdNews clearfix")
    ls = []
    for div in divs[:5]:
        dic = {}
        content_url = div.strong.a.get("href")
        if not re.search("http", content_url):
            content_url = "http://capital.people.com.cn" + content_url
        content_id = content_url.split("/")[-1].split(".")[0]
        img_url = div.img.get("src")
        if not re.search("http", img_url):
            img_url = "http://capital.people.com.cn" + div.img.get("src")
        title = div.strong.a.text
        # 爬取url中的内容
        resp = requests.get(content_url, headers=headers)
        resp.encoding = "GB2312"
        con_soup = BeautifulSoup(resp.text, "lxml")
        content_ls = con_soup.find("div", class_="gray box_text")
        img_link = content_ls.find_all("img")
        if len(img_link):
            for i in img_link:
                link = i.get("src")
                if not re.search("http", link):
                    link = "http://capital.people.com.cn" + link
                img_url += " , " + link
        content_p = content_ls.find_all("p")
        content = ""
        for con in content_p:
            content += con.text.strip()
        # 以下为保存的字段
        dic["url"] = content_url
        dic["content_id"] = content_id
        dic["title"] = title
        dic["match_img"] = img_url
        dic["content"] = content
        dic["author"] = ""
        dic["source_name"] ="people_cn"
        ls.append(dic)
    return ls








