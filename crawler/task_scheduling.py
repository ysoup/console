# encoding=utf-8
import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from database.article_manage import ArticleManage, ArticleUploadManage, AccountManage
from selenium import webdriver
import time
from common.untils import *
import requests
import json
CLIENT_ID = "78274d6bfded051a82975cb4f4a36b58"
client_secret = "4b990a2a4235052483e4ff99115770ddf2467af8"
executable_path = "/home/ywd/.pyenv/versions/3.5.2/bin/geckodriver"


def get_task():
    # 获取上传任务
    task_rows = ArticleUploadManage.select().where(ArticleUploadManage.send_status == 0)
    if task_rows:
        for x in task_rows:
            account_rows = AccountManage.select().where(AccountManage.account_type == x.article_type,
                                                        AccountManage.platform_type == x.platform_type,
                                                        AccountManage.category_type == x.category_type)
            if account_rows:
                for y in account_rows:
                    # 获取code
                    code = get_code(y.account_name, y.account_password)

                    # 获取token
                    access_token, openid = get_token(CLIENT_ID, client_secret, code)

                    # 获取上传的文章
                    article_list = (x.send_ids).split(",")
                    for g in article_list:
                        rows = ArticleManage.select().where(ArticleManage.id == int(g))
                        if len(rows) >= 1:
                            # 发送
                            data = {
                                "access_token": access_token,
                                "openid": openid,
                                "title": rows[0].article_title,
                                "content": rows[0].article_content,
                                "cover_pic": rows[0].article_cover,
                                "category": x.category_type

                            }
                            url = "https://api.om.qq.com/article/authpubpic"
                            response = requests.post(url, data=data)
                            data = json.loads(response.text)
                            print(data)



if __name__ == '__main__':
    get_task()
