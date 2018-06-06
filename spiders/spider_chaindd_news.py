# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import json

def crawler_chaindd_information(url, logger):
    headers = {
        'Host': 'www.chaindd.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.chaindd.com/column/3048842',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'ci_session=7a89d3e4e1a3f7f5128e6803088b01f2c32665f1; SERVERID=367ae40297e23f3a30ee7caaf4a99faf|1528263407|1528263407; zg_did=%7B%22did%22%3A%20%22163d303acf1120-054612ae7db1c6-77256752-384000-163d303acf25a8%22%7D; zg_dc1e574e14aa4c44b51282dca03c46f4=%7B%22sid%22%3A%201528263408.808%2C%22updated%22%3A%201528263408.808%2C%22info%22%3A%201528253623546%7D; responseTimeline=229; _ga=GA1.2.1432363460.1528253624; _gid=GA1.2.78674180.1528253624; pgv_pvi=4126479360; pgv_si=s6134532096; Hm_lvt_c2faa2e59b5c08b979ccf8a901af64a8=1528255705; Hm_lpvt_c2faa2e59b5c08b979ccf8a901af64a8=1528255705; _gat_gtag_UA_115015617_1=1',
        'Connection': 'keep-alive'
    }
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    ls = []
    for x in data["data"][0:10]:
        dic = {}
        dic["content_id"] = x["post_guid"]
        dic["author"] = x["authors"][0]["username"]
        dic["title"] = x["title"]
        details_url = x["short_url"]
        print(details_url)
        response_details = requests.get(details_url)
        if response_details.status_code == 200:
            soup = BeautifulSoup(response_details.text, "lxml")
            data = soup.find_all("article")[0]
            data.div.extract()
            data.h1.extract()
            img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(data))
            for i in x["thumb_image"]:
                home_img = x["thumb_image"][i][0]["url"]
                break
            img_ls.insert(0, home_img)
            dic["match_img"] = ",".join(img_ls)
            dic["url"] = details_url
            dic["source_name"] = "chaindd"
            dic["content"] = str(data)
            ls.append(dic)
    return ls