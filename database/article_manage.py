from peewee import *
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel
import datetime

article = InitDb(SpidersDataModel.Model_SPIDERS_ARTICLE.value)
article_database = article.connect()
article.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = article_database


class ArticleManage(BaseModel):
    article_content = TextField(null=True)
    article_cover = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    article_id = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    article_title = CharField(constraints=[SQL("DEFAULT ''")])
    source_name = CharField(constraints=[SQL("DEFAULT ''")])
    article_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    category_type = IntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    is_send = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'article_manage'


class ArticleUploadManage(BaseModel):
    account_name = CharField()
    article = CharField(column_name='article_id', null=True)
    article_type = IntegerField(null=True)
    category_type = IntegerField(null=True)
    create_time = DateTimeField()
    platform_type = IntegerField(null=True)
    send_ids = CharField(null=True)
    send_status = IntegerField(null=True)
    send_time = CharField(null=True)
    send_type = IntegerField(null=True)
    update_time = DateTimeField()

    class Meta:
        table_name = 'article_upload_manage'


class AccountManage(BaseModel):
    account_article_num = IntegerField(null=True)
    account_index = IntegerField(null=True)
    account_name = CharField(unique=True)
    account_password = CharField(null=True)
    account_rank = IntegerField(null=True)
    account_type = IntegerField(null=True)
    category_type = IntegerField(null=True)
    create_time = DateTimeField()
    credit_score = IntegerField(null=True)
    nick_name = CharField(null=True)
    platform_type = IntegerField(null=True)
    total_play_num = IntegerField(null=True)
    total_read_num = IntegerField(null=True)
    total_subscribe_num = IntegerField(null=True)
    update_time = DateTimeField()

    class Meta:
        table_name = 'account_manage'


class ArticleUploadDetails(BaseModel):
    account_id = IntegerField(null=True)
    account_name = CharField(null=True)
    article_id = IntegerField(null=True)
    article_title = CharField(null=True)
    article_type = IntegerField(null=True)
    article_category = IntegerField(null=True)
    create_time = DateTimeField()
    send_status = IntegerField(null=True)
    upload_id = IntegerField(null=True)
    desc = CharField(null=True)

    class Meta:
        table_name = 'article_upload_details'

