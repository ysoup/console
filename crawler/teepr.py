# -*- coding=utf-8 -*-
from queue import Queue
import time
from bs4 import BeautifulSoup
import requests
from database.article_manage import ArticleManage
from common.initRedis import connetcredis
import json
import urllib

all_categories = ["生活", "动物", "惊奇", "艺术", "表演", "旅游", "女性", "运动"]


class CookieSpider(object):
    def __init__(self):
        # 创建一个队列用来保存进程获取到的数据
        self.q = Queue()
        self.headers = {
            'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
        }

    def run(self, url):
        self.parse_page(url)

    def send_request(self, url):
        '''
        用来发送请求的方法
        :return: 返回网页源码
        '''
        # 请求出错时，重复请求３次,
        i = 0
        while i <= 3:
            try:
                print(u"[INFO]请求url:"+url)
                html = requests.get(url=url, headers=self.headers).text
            except Exception as e:
                print(u'[INFO] %s%s' % (e, url))
                i += 1
            else:
                return html

    def parse_page(self, url):
        response = self.send_request(url)
        soup = BeautifulSoup(response, "lxml")
        title_tag = soup.find("div", "title")
        if not title_tag:
            all_article = soup.find_all("h2", "title front-view-title")
            if all_article:
                for x in all_article:
                    dic = {}
                    detail_url = x.find("a")["href"]
                    title = x.find("a")["title"]
                    dic["article_id"] = (str(detail_url).split("/"))[3]
                    rows = ArticleManage.select().where(ArticleManage.article_id == dic["article_id"], 
                                                        ArticleManage.source_name == "teepr")
                    if rows:
                        print("已经存在")
                    else:
                        details_content = self.send_request(detail_url)
                        details_soup = BeautifulSoup(details_content, "lxml")
                        content = details_soup.find("div", "post-single-wrapper")
                        if content:
                            dic["content"] = str(content)
                            dic["title"] = title
                            connetcredis().lpush("teepr_details_url", json.dumps(dic))
            # title_content = (title_tag.text).strip()
            # if title_content != '我們對不起你！此頁面不存在或是發生了錯誤！':


    def main(self):
        while True:
            url = connetcredis().lpop("teepr_pages_details_url")
            self.run(url)


if __name__=="__main__":
    start = time.time()
    douban = CookieSpider()
    douban.main()
    # for x in all_categories:
    #     cookie = CookieSpider()
    #     p = multiprocessing.Process(target=cookie.main(), args=(x,))
    #     p.start()
    print('[info]耗时：%s'%(time.time()-start))