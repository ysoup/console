# encoding=utf-8

import os
from bs4 import BeautifulSoup
from urllib import parse
from pyquery import PyQuery as pq
from selenium import webdriver

import requests
import time
import re


class BaiDuEngines(object):
    def __init__(self, search_name, num, headers, page_num):
        self.search_name = parse.quote(search_name)
        self.num = num
        self.page_num = page_num
        # self.forbid_seach_name = forbid_seach_name
        self.headers = headers

    def parse_engines_data(self):
        content_ls = []
        for i in range(1, self.page_num + 1):
            page_num = 10 * i
            url = "https://www.baidu.com/baidu?wd=%s&tn=ubuntuu_cb&ie=utf-8&pn=%s&tfflag=1" % (self.search_name, page_num)
            response = requests.get(url, headers=self.headers)
            soup = BeautifulSoup(response.content, 'lxml')
            tags = soup.find_all('h3')
            for x in tags:
                href = x.find('a').get('href')
                baidu_url = requests.get(url=href, headers=self.headers, allow_redirects=False)
                baidu_content = x.find('a').text
                real_url = baidu_url.headers['Location']  # 得到网页原始地址
                if real_url.startswith('http'):
                    dic = {}
                    dic["url"] = baidu_url
                    dic["content"] = baidu_content
                    content_ls.append(dic)
        return content_ls


class SouGouEngines(object):
    def __init__(self, search_name, num, headers):
        # 构造函数
        self.search_name = parse.quote(search_name)
        self.sogou_search_url = 'http://weixin.sogou.com/weixin?type=1&query=%s&ie=utf8&s_from=input&_sug_=n&_sug_type_=' % self.search_name
        self.num = num

        # 爬虫伪装
        self.headers = headers
        # self.headers =
        # {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 FirePHP/0refox/47.0 FirePHP/0.7.4.1'}

        # 操作超时时长
        self.timeout = 5
        self.s = requests.Session()

    def get_search_result_by_search_name(self):
        self.log('搜索地址为：%s' % self.sogou_search_url)
        return self.s.get(self.sogou_search_url, headers=self.headers, timeout=self.timeout).content

    def get_wx_url_by_sougou_search_html(self, sougou_search_html):
        # 根据返回sougou_search_html，从中获取公众号主页链接
        soup = BeautifulSoup(sougou_search_html, 'lxml')
        div_ls = soup.find_all("div", "txt-box")
        content_ls = []
        for x in div_ls:
            dic = {}
            p_tag = x.find("p", "tit")
            dic["url"] = p_tag.a.get('href')
            dic["content"] = p_tag.text
            content_ls.append(dic)
        return content_ls

    def get_selenium_js_html(self, wx_url):
        # 执行js渲染内容，并返回渲染后的html内容
        browser = webdriver.PhantomJS(executable_path='/usr/phantomjs/phantomjs-2.1.1-linux-x86_64/bin/phantomjs',
                                      service_log_path="test.log")
        browser.get(wx_url)
        time.sleep(3)
        # 执行js得到整个dom
        html = browser.execute_script("return document.documentElement.outerHTML")
        return html

    def parse_wx_articles_by_html(self, selenium_html):
        # 从selenium_html中解析出微信公众号文章
        doc = pq(selenium_html)
        return doc('div[class="weui_msg_card"]')

    def switch_arctiles_to_list(self, articles, all_articles_ls):
        if articles:
            for article in articles.items():
                # self.log(u'开始整合(%d/%d)' % (i, len(articles)))
                # print(self.parse_one_article(article))
                all_articles_ls.append(self.parse_one_article(article))

    def parse_one_article(self, article):
        # 解析单篇文章

        article = article('.weui_media_box[id]')

        title = article('h4[class="weui_media_title"]').text()
        self.log('标题是： %s' % title)
        hred_url = article('h4[class="weui_media_title"]').attr('hrefs')
        url = 'http://mp.weixin.qq.com' + hred_url if hred_url else ""
        self.log('地址为： %s' % url)
        summary = article('.weui_media_desc').text()
        self.log('文章简述： %s' % summary)
        date = article('.weui_media_extra_info').text()
        self.log('发表时间为： %s' % date)
        pic = self.parse_cover_pic(article)
        try:
            content = self.parse_content_by_url(url).html()
        except Exception as e:
            content = ""

        return {
            'title': title,
            'url': url,
            'summary': summary,
            'date': date,
            'pic': pic,
            'content': content
        }

    def parse_cover_pic(self, article):
        # 解析文章封面图片
        pic = article('.weui_media_hd').attr('style')
        if pic:
            p = re.compile(r'background-image:url\((.*?)\)')
            print(pic)
            rs = p.findall(pic)
            self.log('封面图片是：%s ' % rs[0] if len(rs) > 0 else '')

            return rs[0] if len(rs) > 0 else ''
        else:
            return ''

    def parse_content_by_url(self, url):
        # 获取文章详情内容
        page_html = self.get_selenium_js_html(url)
        return pq(page_html)('#js_content')

    def save_content_file(self, title, content):
        # 页面内容写入文件
        with open(title, 'w') as f:
            f.write(content)

    def save_file(self, content):
        # 数据写入文件
        with open(self.search_name + '/' + self.search_name + '.txt', 'w') as f:
            f.write(content)

    def log(self, msg):
        # 自定义log函数
        print
        u'%s: %s' % (time.strftime('%Y-%m-%d %H:%M:%S'), msg)

    def need_verify(self, selenium_html):
        # 有时候对方会封锁ip，这里做一下判断，检测html中是否包含id=verify_change的标签，有的话，代表被重定向了，提醒过一阵子重试
        return pq(selenium_html)('#verify_change').text() != ''

    def create_dir(self):
        # 创建文件夹
        if not os.path.exists(self.search_name):
            os.makedirs(self.search_name)

    def run(self):
        sougou_search_html = self.get_search_result_by_search_name()
        all_articles_ls = self.get_wx_url_by_sougou_search_html(sougou_search_html)
        # all_articles_ls = []
        # selenium_html = self.get_selenium_js_html(wx_url)
        # if self.need_verify(selenium_html):
        #     print("爬虫被目标网站封锁，请稍后再试")
        #     # self.log(u'爬虫被目标网站封锁，请稍后再试')
        # else:
        #     articles = self.parse_wx_articles_by_html(selenium_html)
        #     self.switch_arctiles_to_list(articles, all_articles_ls)
        return all_articles_ls


if __name__ == "__main__":
    a = SouGouEngines("区块链", {'User-Agent':
                                  'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0'})
    content_js = a.run()
    print(content_js)