#!/usr/bin/env python
# encoding=utf-8
import requests

# 封装爬虫请求模块


class CrawlerRequest(object):
    def __init__(self, url):
        self.url = url

    def crawler_get(self):
        response = requests.get(url=self.url)
        print('状态码', response.status_code)
        return response.text

    def crawler_post(self):
        response = requests.post(url=self.url)
        print('状态码', response.status_code)
        return response

    def crawler_post_json(self):
        response = requests.post(url=self.url)
        print('状态码', response.status_code)
        return response
    # def post(self):
    #
    # def post_json(self):
    #


