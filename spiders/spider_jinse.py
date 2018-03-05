# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.crawleranalysis import AnalysisPage
from common.crawlerrequest import CrawlerRequest


def crawler_jinse(url):
    t = CrawlerRequest(url)
    crawler_html = t.crawler_get
    f = AnalysisPage(crawler_html)
    data = f.analysishtml()
    print(data)