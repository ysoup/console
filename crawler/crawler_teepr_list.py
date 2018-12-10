# -*- coding=utf-8 -*-
from queue import Queue
import time
from bs4 import BeautifulSoup
import requests
from database.article_manage import ArticleManage
from common.initRedis import connetcredis
import json
from urllib import parse

all_categories = ["生活", "動物", "驚奇", "藝術", "表演", "旅遊", "女性專區", "運動"]


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
        all_data = soup.find_all("div", "categories-browse-recipe")
        if all_data:
            for x in all_data:
                dic = {}
                a_tag = x.find("a", "browse-recipe-cover-link")["href"]
                title = x.find("a", "browse-recipe-cover-link")["title"]
                print(title)
                dic["article_id"] = (str(a_tag).split("/"))[-1]
                rows = ArticleManage.select().where(ArticleManage.article_id == dic["article_id"])
                if rows:
                    print("已经存在")
                else:
                    details_url = "https://icook.tw" + str(a_tag)
                    details_content = self.send_request(details_url)
                    details_soup = BeautifulSoup(details_content, "lxml")
                    recipe_details = details_soup.find("div", "recipe-details")
                    if recipe_details:
                        dic["content"] = str(recipe_details)
                        dic["title"] = title
                        connetcredis().lpush("icook_details_url", json.dumps(dic))

    def main(self):
        base_url = 'http://www.teepr.tv/category/'
        # for x in all_categories:
        #     print(parse.quote(x))
        # 构造所有ｕｒｌ
        url_list = [base_url + parse.quote(num) + "/page/" + str(i) + "/" for num in all_categories for i in
                    range(1, 30)]
        # 创建协程并执行
        for url in url_list:
            print(url)
            connetcredis().lpush("teepr_pages_details_url", url)


if __name__=="__main__":
    start = time.time()
    douban = CookieSpider()
    douban.main()
    # for x in all_categories:
    #     cookie = CookieSpider()
    #     p = multiprocessing.Process(target=cookie.main(), args=(x,))
    #     p.start()
    print('[info]耗时：%s'%(time.time()-start))