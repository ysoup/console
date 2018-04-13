# -*- coding: utf-8 -*-
from aip import AipNlp
from common.constants import GetBaiDuAi


class GetBaiduNlp(object):
    def __init__(self, title, content):
        self.app_id = GetBaiDuAi.APP_ID.value
        self.api_key = GetBaiDuAi.API_KEY.value
        self.secret_key = GetBaiDuAi.SECRET_KEY.value
        self.title = title
        self.content = content
        self.client = AipNlp(self.app_id, self.api_key, self.secret_key)

    def get_topic(self):
        return self.client.topic(self.title, self.content)

    def get_keyword(self):
        return self.client.keyword(self.title, self.content)
