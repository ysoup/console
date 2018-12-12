# encoding=utf-8
import os
import sys
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)

from database.article_manage import ArticleManage, ArticleUploadManage, AccountManage, ArticleUploadDetails
import traceback
from common.untils import *
import requests
import json
CLIENT_ID = "78274d6bfded051a82975cb4f4a36b58"
client_secret = "4b990a2a4235052483e4ff99115770ddf2467af8"
executable_path = "/home/ywd/.pyenv/versions/3.5.2/bin/geckodriver"


def get_task():
    # 获取上传任务
    while True:
        try:
            task_rows = ArticleUploadManage.select().where(ArticleUploadManage.send_status == 0)
            if task_rows:
                for x in task_rows:
                    account_ids_ls = (x.account_name).split(",")
                    article_list = (x.send_ids).split(",")
                    for i, y in enumerate(account_ids_ls):
                        account_rows = AccountManage.select().where(AccountManage.id == y)
                        if account_rows:
                            # 获取code
                            start = i * 2 + i
                            end = start + 2
                            if start > len(article_list): break
                            code = get_code(account_rows[0].account_name, account_rows[0].account_password,
                                            login_type=0)

                            # 获取token
                            access_token, openid = get_token(CLIENT_ID, client_secret, code)
                            if not access_token and not openid:continue
                            # 获取上传的文章
                            new_article_list = article_list[start:end]
                            for g in new_article_list:
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
                                    if data["msg"] == "SUCCESS":
                                        w = ArticleManage.update(is_send=2).where(ArticleManage.id == int(g))
                                        w.execute()
                                        ArticleUploadDetails.create(
                                            account_id=y,
                                            account_name=account_rows[0].account_name,
                                            article_id=9,
                                            article_title=rows[0].article_title,
                                            article_type=x.article_type,
                                            article_category=x.category_type,
                                            upload_id=x.id,
                                            send_status=1,
                                            desc=data["msg"]

                                        )
                                    else:
                                        w = ArticleManage.update(is_send=3).where(ArticleManage.id == int(g))
                                        w.execute()
                                        ArticleUploadDetails.create(
                                            account_id=y,
                                            account_name=account_rows[0].account_name,
                                            article_id=9,
                                            article_title=rows[0].article_title,
                                            article_type=x.article_type,
                                            article_category=x.category_type,
                                            upload_id=x.id,
                                            send_status=0,
                                            desc=data["msg"]
                                        )
                                    print(data)
                    # 更新状态
                    q = ArticleUploadManage.update(send_status=1).where(ArticleUploadManage.id == x.id)
                    q.execute()
        except Exception as e:
            print(traceback.format_exc())


if __name__ == '__main__':
    print("===服务开始启动===")
    get_task()
