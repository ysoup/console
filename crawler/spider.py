# encoding=utf-8
import sys
import os
import requests
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from bs4 import BeautifulSoup
# from common.crawleranalysis import AnalysisPage

# from common.crawlerrequest import CrawlerRequest


@app.task
def send():
    url = "http://www.jinse.com/lives"
    print("正在抓取链接", url)
    html = requests.get(url=url)
    soup = BeautifulSoup(html.text)
    print("正在解析数据....")
    print("抓取数据", soup)
    return soup
    # AnalysisPage.analysishtml(response)
    # resp = CrawlerRequest.crawler_get(url)
    # resp = requests.get(url=url)



# app.conf.beat_schedule = {
#     'send-every-10-seconds': {
#         'task': 'spider.send',
#         'schedule': 10.0
#         # 'args': ("http://www.jinse.com/lives")
#     }
# }