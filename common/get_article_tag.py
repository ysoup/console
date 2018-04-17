# encoding=utf-8
from aip import AipNlp
from common.constants import GetBaiDuAi
import re

Regx = r'/\xa0|/\u2022'


class GetBaiduNlp(object):
    def __init__(self, title, content):
        self.app_id = GetBaiDuAi.APP_ID.value
        self.api_key = GetBaiDuAi.API_KEY.value
        self.secret_key = GetBaiDuAi.SECRET_KEY.value
        self.title = title
        self.content = content
        self.client = AipNlp(self.app_id, self.api_key, self.secret_key)

    # 文章分类
    def get_topic(self):
        return self.client.topic(re.sub(r'/\xa0', u' ', self.title), re.sub(r'\xa0', u' ', self.content))

    # 文章标签
    def get_keyword(self):
        return self.client.keyword(re.sub(r'\xa0|\u2022', u' ', self.title), re.sub(r'\xa0|\u2022', u' ', self.content))
