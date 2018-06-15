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
                dic["title"] = re.sub("<em>|</em>", "", x["title"])
                details_url = x["uri"]
                response_details = requests.get(details_url)
                if response_details.status_code == 200:
                    soup = BeautifulSoup(response_details.text, "lxml")
                    if "weixin.qq" in details_url:
                        data = soup.find_all("div", "rich_media_content")[0]
                        data = data.find("section")

                        del_section = data.find("section", style="max-width: 100%;border-width: 0px;border-style: initial;border-color: initial;height: 2.5em;border-radius: 2em;background-color: rgb(0, 187, 236);box-sizing: border-box !important;word-wrap: break-word !important;")
                        del_section2 = data.find("section", style="max-width: 100%;border-width: 0px;border-style: initial;border-color: initial;line-height: 24px;vertical-align: top;box-sizing: border-box !important;word-wrap: break-word !important;")
                        del_em = data.find("em", style="max-width: 100%;font-size: 14px;box-sizing: border-box !important;word-wrap: break-word !important;")
                        if data is None:
                            continue
                        else:
                            section_ls = data.find_all("section")
                            if len(section_ls) == 1:
                                data.section.extract()
                            elif len(section_ls) == 2:
                                data.section.extract()
                            h2_ls = data.find_all("h2")
                            if len(h2_ls) > 0:
                                data.h2.extract()
                            img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(data))
                            img_ls.insert(0, x["image_uri"])
                            dic["match_img"] = ",".join(img_ls)
                            dic["url"] = details_url
                            dic["source_name"] = "wall_streetcn"
                            if len(section_ls) > 50:
                                new_section_ls = section_ls[-17:]
                                for x in new_section_ls:
                                    data = str(data).replace(str(x), "")
                            datas = str(data).replace(str(del_section), "").strip()
                            datas = datas.replace(str(del_em), "").strip()
                            dic["content"] = datas.replace(str(del_section2), "").strip()
                    elif "https://wallstreetcn.com" in details_url:
                        print(details_url)
                        data = soup.find_all("div", "article__content")[0]
                        img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(data))
                        img_ls.insert(0, x["image_uri"])
                        dic["match_img"] = ",".join(img_ls)
                        dic["url"] = details_url
                        dic["source_name"] = "wall_streetcn"
                        datas = str(data).replace(str(del_section), "").strip()
                        datas = datas.replace(str(del_em), "").strip()
                        dic["content"] = datas.replace(str(del_section2), "").strip()
                    else:
                        continue
                    ls.append(dic)
    return ls