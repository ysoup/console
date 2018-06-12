# encoding=utf-8

import requests
from bs4 import BeautifulSoup
import re
import json


def crawler_tmt_post_information(url, logger):
    headers = {
        'Host': 'www.tmtpost.com',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'en-GB,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Referer': 'http://www.tmtpost.com/column/3015019',
        'X-Requested-With': 'XMLHttpRequest',
        'Cookie': 'acw_tc=AQAAADouugaoOg0A67N4e6yyI7iz30X2; servertime_differ=112819; pgv_pvi=4894686208; '
                  'pgv_si=s364800000; UM_distinctid=163cf6128eb3b4-0ff943fbd6b731-77256752-384000-163cf6128ec15c; '
                  'CNZZDATA5193056=cnzz_eid%3D1808423306-1528188243-%26ntime%3D1528269399; '
                  'zg_did=%7B%22did%22%3A%20%22163cf61296f11-07fa33e43aa58d8-77256752-384000-163cf6129702e0%22%7D; '
                  'zg_dc1e574e14aa4c44b51282dca03c46f4=%7B%22sid%22%3A%201528273558.256%2C%22updated%22%3A%201528273597.'
                  '213%2C%22info%22%3A%201528192641403%7D; _ga=GA1.2.1451344632.1528192642; _gid='
                  'GA1.2.1484690609.1528192642; responseTimeline=71; Hm_lvt_c2faa2e59b5c08b979ccf8a901af64a8=1528192645; '
                  'Hm_lpvt_c2faa2e59b5c08b979ccf8a901af64a8=1528273598; trc_cookie_storage=taboola%2520global%253Auser-'
                  'id%3Dda060e8f-b9ad-4d7c-8ca5-9ca4257b7b62-tuct1890b20; ci_session=64fff8e8a181374bd74c0157e8c9ae16f'
                  '1fdb2c6; lastest_num=26; _gat=1',
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
            dic["source_name"] = "tmt_post"
            dic["content"] = str(data)
            re_a_1 = re.compile(r'<a[\s\S]*?href=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>')
            dic["content"] = re_a_1.sub('', str(data))
            re_a_2 = re.compile(r'</a>|<u>|</u>')
            dic["content"] = re_a_2.sub('', dic["content"])
            ls.append(dic)
    return ls