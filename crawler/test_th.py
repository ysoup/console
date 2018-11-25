#!/usr/bin/env python2
# -*- coding=utf-8 -*-

from threading import Thread
from queue import Queue
import time
import requests
from bs4 import BeautifulSoup
from database.article_manage import ArticleManage
from qiniu import Auth, put_file, etag
import os, re
all_categories = [
    '592', '593', '104', '491', '113', '10', '7', '591', '209', '217', '207', '107', '112', '111', '108',
                  '413', '208', '241', '380', '596', '28', '8', '360', '46', '200', '346', '339', '345', '347', '375',
                  '73', '23', '17', '342', '465', '341', '349', '16', '15', '521', '18', '41', '43', '394', '2', '390',
                  '3', '395', '393', '302', '6', '301', '40', '39', '38', '61', '60', '62', '83', '590', '68', '64',
                  '63', '216', '350', '219', '20', '463', '599', '462', '148', '147', '210', '206', '77', '27', '498',
                  '453', '495', '29', '30', '455', '456', '13', '25', '417', '449', '458', '459', '26', '122',
                  '436', '211', '185', '52', '71', '137', '49', '50', '602'
]

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


class CookieSpider(Thread):
    def __init__(self, url, q):
        # 重写写父类的__init__方法
        super(CookieSpider, self).__init__()
        self.url = url
        self.q = q
        self.headers = {
            'User-Agent': 'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
        }

    def run(self):
        self.parse_page()

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
                html = requests.get(url=url, headers=self.headers).content
            except Exception as e:
                print(u'[INFO] %s%s' % (e, url))
                i += 1
            else:
                return html

    def parse_page(self):
        response = self.send_request(self.url)
        soup = BeautifulSoup(response, "lxml")
        all_data = soup.find_all("div", "categories-browse-recipe")

        for x in all_data:
            dic = {}
            a_tag = x.find("a", "browse-recipe-cover-link")["href"]
            title = x.find("a", "browse-recipe-cover-link")["title"]
            print(title)
            dic["article_id"] = (str(a_tag).split("/"))[-1]
            details_url = "https://icook.tw" + str(a_tag)
            details_content = self.send_request(details_url)
            details_soup = BeautifulSoup(details_content, "lxml")
            recipe_details = details_soup.find("div", "recipe-details")
            dic["content"] = str(recipe_details)
            if recipe_details:
                tmp_tag = recipe_details.find("div", "header-col right-col")
                tmp_tag = str(tmp_tag)
                dic["content"] = dic["content"].replace(tmp_tag, "")

                ad_tag = recipe_details.find("div", "recipe-ad-placeholder")
                ad_tag = str(ad_tag)
                dic["content"] = dic["content"].replace(ad_tag, "")

                video_tag = recipe_details.find("div", "recipe-details-video recipe-details-block")
                video_tag = str(video_tag)
                dic["content"] = dic["content"].replace(video_tag, "")

                tips_tag = recipe_details.find_all("div", "recipe-details-steps-note recipe-details-block")
                if tips_tag is not None:
                    if len(tips_tag) >= 1:
                        tips_tag_1 = tips_tag[0].find("div", "recipe-details-note recipe-details-sub-block")
                        tips_tag_1 = str(tips_tag_1)
                        dic["content"] = dic["content"].replace(tips_tag_1, "")

                toolbox_tag = recipe_details.find("div", "recipe-details-toolbox recipe-details-block")
                toolbox_tag = str(toolbox_tag)
                dic["content"] = dic["content"].replace(toolbox_tag, "")

                info_content_tag = recipe_details.find("div", "calories-info info-block")
                info_content_tag = str(info_content_tag)
                dic["content"] = dic["content"].replace(info_content_tag, "")

                img_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(str(recipe_details))

                dic["content"] = dic["content"].replace("data-src", "src")
                dic["content"] = dic["content"].replace('sizes="(max-width: 767px) calc(100vw - 32px), 220px"',
                                                        'width="800px" height="600px"')
                # 上传图片
                try:
                    new_img_ls = []
                    for i, y in enumerate(img_ls):
                        new_img_url = self.upload_img(y, "icook", i)
                        dic["content"] = dic["content"].replace(y, new_img_url)
                        new_img_ls.append(new_img_url)
                    dic["content"] = Converter('zh-hans').convert(dic["content"])
                    title = Converter('zh-hans').convert(str(title))
                    dic["content"] = self.parse_content(dic["content"])

                    rows = ArticleManage.select().where(ArticleManage.article_id == dic["article_id"])
                    if rows:
                        print("已经存在")
                    else:
                        ArticleManage.create(
                            article_content=dic["content"],
                            article_id=dic["article_id"],
                            article_cover=new_img_ls[0],
                            article_title=title,
                            category_type=9,
                            source_name="icook"
                        )
                except Exception as e:
                    pass
                    # print(traceback.format_exc())

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

    def parse_content(self, tmp):
        soup = BeautifulSoup(tmp, "lxml")
        recipe_cover = soup.find("div", "recipe-cover")
        recipe_cover_img = recipe_cover.find("img")
        content = str(recipe_cover_img)
        header_row_description = soup.find("div", "header-row description")
        header_row_description_p = header_row_description.find("p")
        del_header_row_description_a = header_row_description_p.find("a")
        header_row_description_p = str(header_row_description_p).replace(str(del_header_row_description_a), "")
        content = content + "<br>" + header_row_description_p

        servings_info = soup.find("div", "servings-info info-block")
        info_tag = servings_info.find("div", "info-tag").text
        content = content + info_tag

        info_content = servings_info.find("div", "info-content").text
        content = content + "<br>" + info_content

        time_info = soup.find("div", "time-info info-block")
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
            img = y.find("img").get("src")
            new_img = tmp_img.replace("icook_img", img)
            content = content + "<br>" + new_img
            step_instruction = y.find("big").text
            content = content + "<br>" + step_instruction

            step_instruction_content = y.find("div", "step-instruction-content").text
            content = content + "<br>" + step_instruction_content
        return content


def main():
    # 创建一个队列用来保存进程获取到的数据
    q = Queue()
    base_url = 'https://icook.tw/categories/'
    # 构造所有ｕｒｌ
    url_list = [base_url + str(num) for num in all_categories]

    # 保存线程
    Thread_list = []
    # 创建并启动线程
    for url in url_list:
        p = CookieSpider(url, q)
        p.start()
        Thread_list.append(p)

    # 让主线程等待子线程执行完成
    for i in Thread_list:
        i.join()

    while not q.empty():
        print(q.get())


if __name__=="__main__":

    start = time.time()
    main()
    print('[info]耗时：%s'%(time.time()-start))

