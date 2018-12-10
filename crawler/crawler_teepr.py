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
                        new_img_url = self.upload_img(y, "icook", i)
                        if new_img_url:
                            dic["content"] = dic["content"].replace(y, new_img_url)
                            new_img_ls.append(new_img_url)
                    dic["content"] = Converter('zh-hans').convert(dic["content"])
                    title = Converter('zh-hans').convert(dic["title"])
                    dic["content"] = self.parse_content(dic["content"])

                    # ArticleManage.create(
                    #     article_content=dic["content"],
                    #     article_id=dic["article_id"],
                    #     article_cover=new_img_ls[0],
                    #     article_title=title,
                    #     category_type=9,
                    #     source_name="teepr"
                    # )
                except Exception as e:
                    print(traceback.format_exc())

    def parse_content(self, tmp):
        soup = BeautifulSoup(tmp, "lxml")
        ad_ls = soup.find_all("div", "mid-post-ad-2")
        content = ""
        for x in ad_ls:
            content = content + tmp.replace(str(x), "")
        print(content)
        recipe_cover = soup.find("div", "recipe-cover")
        recipe_cover_img = recipe_cover.find("img")
        content = str(recipe_cover_img)
        header_row_description = soup.find("div", "header-row description")
        if header_row_description:
            header_row_description_p = header_row_description.find("p")
            del_header_row_description_a = header_row_description_p.find("a")
            header_row_description_p = str(header_row_description_p).replace(str(del_header_row_description_a), "")
            content = content + "<br>" + header_row_description_p

        servings_info = soup.find("div", "servings-info info-block")
        if servings_info:
            info_tag = servings_info.find("div", "info-tag").text
            content = content + info_tag

            info_content = servings_info.find("div", "info-content").text
            content = content + "<br>" + info_content

        time_info = soup.find("div", "time-info info-block")
        if time_info:
            info_tag = time_info.find("div", "info-tag").text
            content = content + "<br>" + info_tag

            info_content = time_info.find("div", "info-content").text
            content = content + "<br>" + info_content

        title_info = soup.find("div", "title").text
        content = content + "<br>" + title_info
        ingredients = soup.find_all("div", "ingredient")
        for x in ingredients:
            ingredient_name = x.find("div", "ingredient-name").text
            content = content + "<br>" + ingredient_name
            ingredient_unit = x.find("div", "ingredient-unit").text
            content = content + "<br>" + ingredient_unit

        li_info = soup.find_all("li")
        tmp_img = '<img alt="" height="600" src="icook_img" width="800" />'
        for y in li_info:
            if y.find("img"):
                img = y.find("img").get("src")
                new_img = tmp_img.replace("icook_img", img)
                content = content + "<br>" + new_img
            if y.find("big"):
                step_instruction = y.find("big").text
                content = content + "<br>" + step_instruction

            step_instruction_content = y.find("div", "step-instruction-content").text
            content = content + "<br>" + step_instruction_content
        return content


if __name__=="__main__":
    start = time.time()
    douban = CookieSpider()
    douban.parse_page()
    # for x in all_categories:
    #     cookie = CookieSpider()
    #     p = multiprocessing.Process(target=cookie.main(), args=(x,))
    #     p.start()
    print('[info]耗时：%s'%(time.time()-start))