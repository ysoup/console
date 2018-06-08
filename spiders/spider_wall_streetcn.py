# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import json


def crawler_wall_streetcn_information(url, logger):
    response = requests.get(url)
    data = json.loads(response.text)
    ls = []
    if data["message"] == "OK":
        if data.__contains__('data'):
            for x in data["data"]["items"][:5]:
                dic = {}
                dic["content_id"] = x["id"]
                dic["author"] = x["author"]["display_name"]
                dic["title"] = x["title"]
                details_url = x["uri"]
                response_details = requests.get(details_url)
                if response_details.status_code == 200:
                    soup = BeautifulSoup(response_details.text, "lxml")
                    if "weixin.qq" in details_url:
                        data = soup.find_all("div", "rich_media_content")[0]
                        img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(data))
                        img_ls.insert(0, x["image_uri"])
                        dic["match_img"] = ",".join(img_ls)
                        dic["url"] = details_url
                        dic["source_name"] = "wall_streetcn"
                        dic["content"] = str(data)
                    elif "https://wallstreetcn.com" in details_url:
                        print(details_url)
                        data = soup.find_all("div", "article__content")[0]
                        img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(data))
                        img_ls.insert(0, x["image_uri"])
                        dic["match_img"] = ",".join(img_ls)
                        dic["url"] = details_url
                        dic["source_name"] = "wall_streetcn"
                        dic["content"] = str(data)
                    else:
                        continue
                    ls.append(dic)
    return ls