from common.initRedis import connetcredis
from queue import Queue
import time
from bs4 import BeautifulSoup
import requests
import gevent
import re
import os
import traceback
from qiniu import Auth, put_file, etag
from gevent import monkey
from crawler.langconv import *
from database.article_manage import ArticleManage
import json

path = os.path.dirname(__file__)


class QiNiuServer(object):
    def __init__(self):
        self.ak = "odWsvYrynNMRBcCTeTEgw0tQDCoa3TAz4_Dp2RRK"
        self.ck = "aQ2DOlSO3quHfC2IivOr5-414euUSDn2M53Om21D"
        self.q = None

    def start_server(self):
        self.q = Auth(self.ak, self.ck)

    def upload_files(self, bucket_name, file_name, path):
        token = self.q.upload_token(bucket_name, file_name, 3600)
        # 要上传文件的本地路径
        ret, info = put_file(token, file_name, path)


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

    def upload_img(self, img_url, source_name, index):
        i = 0
        try:
            img_name = "%s_%s_%s.jpg" % (source_name, str(int(time.time())), index)
            response = requests.get(img_url)
            file_path = "%s/%s/%s" % (path, "images", img_name)
            with open(file_path, 'wb') as f:
                f.write(response.content)

            qi_niu = QiNiuServer()
            qi_niu.start_server()
            qi_niu.upload_files("icook", img_name, file_path)
            new_img_url = "http://pih1wob2b.bkt.clouddn.com/" + img_name
            return new_img_url
        except Exception:
            print(u'[INFO] %s%s' % (traceback.format_exc(), img_url))
            i += 1

    def parse_page(self):
        while True:
            details_url = connetcredis().lpop("teepr_details_url")
            if details_url:
                dic = json.loads(details_url)
                recipe_details = BeautifulSoup(dic["content"], "lxml")
                img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(recipe_details))

                # 上传图片
                try:
                    new_img_ls = []
                    for i, y in enumerate(img_ls):
                        new_img_url = self.upload_img(y, "teepr", i)
                        if new_img_url:
                            dic["content"] = dic["content"].replace(y, new_img_url)
                            new_img_ls.append(new_img_url)
                    dic["content"] = Converter('zh-hans').convert(dic["content"])
                    title = Converter('zh-hans').convert(dic["title"])
                    dic["content"] = self.parse_content(dic["content"])

                    ArticleManage.create(
                        article_content=dic["content"],
                        article_id=dic["article_id"],
                        article_cover=new_img_ls[0],
                        article_title=title,
                        category_type=9,
                        source_name="teepr"
                    )
                except Exception as e:
                    print(traceback.format_exc())

    def parse_content(self, tmp):
        soup = BeautifulSoup(tmp, "lxml")
        ad_ls = soup.find_all("div", "mid-post-ad-2")
        for x in ad_ls:
            tmp = tmp.replace(str(x), "")
        script_ls = soup.find_all("script")
        for x in script_ls:
            tmp = tmp.replace(str(x), "")
        img_ls = soup.find_all("img")
        for x in img_ls:
            tmp_img = '<img alt="" height="tmp_height" src="icook_img" width="tmp_width" />'
            if "height" in str(x):
                tmp_img = tmp_img.replace("tmp_height", x["height"])
            if "width" in str(x):
                tmp_img = tmp_img.replace("tmp_width", x["width"])
            tmp_img = tmp_img.replace("icook_img", x["src"])
            tmp = tmp.replace(str(x), tmp_img)
        iframe_ls = soup.find_all("iframe")
        for x in iframe_ls:
            tmp = tmp.replace(str(x), "")
        return tmp


if __name__=="__main__":
    start = time.time()
    douban = CookieSpider()
    douban.parse_page()
    # for x in all_categories:
    #     cookie = CookieSpider()
    #     p = multiprocessing.Process(target=cookie.main(), args=(x,))
    #     p.start()
    print('[info]耗时：%s'%(time.time()-start))