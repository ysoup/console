# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from database.spiders_visualization_modle import AiSpiders, WebsiteWhite
from common.db_utils import *
from common.engines_until import *


@app.task()
def seach_engines():
    search_rows = AiSpiders.select().where(AiSpiders.is_useful == 1)
    seach_ls = model_to_dicts(search_rows)
    # 获取抓取网站黑白名单
    website_rows = WebsiteWhite.select().where(WebsiteWhite.is_useful == 1)
    website_ls = model_to_dicts(website_rows)
    for x in seach_ls:
        if x["seach_type"] == 0:
            data = BaiDuEngines(x["seach_name"], x["num"], x["headers"], x["page_num"])
            engines_content_ls = data.parse_engines_data()
        elif x["seach_type"] == 1:
            data = SouGouEngines(x["seach_name"], x["headers"])
            engines_content_ls = data.run()
        new_engines_content_ls = public_forbid_website(website_ls, engines_content_ls)


def public_forbid_website(website_ls, engines_content_ls):
    new_engines_content_ls = []
    for x in engines_content_ls:
        engines_url_ls = y["website_url"].split("/")
        for st in engines_url_ls:
            if ".com" in st or ".cn" in st:
                engines_url_name = st
                break
        for y in website_ls:
            url_ls = x["url"].split("/")
            for sr in url_ls:
                if ".com" in sr or ".cn" in sr:
                    url_name = sr
                    break
            if engines_url_name != url_name:
                new_engines_content_ls.append(x)
    return new_engines_content_ls


@app.task(ignore_result=True)
def schudule_seach_engines():
    app.send_task('crawler.duplicate_removal.duplicate_removal_work', queue='duplicate_removal_task', routing_key='duplicate_removal_info')


# if __name__ == "__main__":
#     seach_engines()