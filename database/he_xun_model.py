import os
import sys
from peewee import *
import datetime


currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel


he_xun = InitDb(SpidersDataModel.MODEL_EIGHT_BITE.value)   #连接的eight_bite数据库
he_xun_database = he_xun.connect()
# he_xun.wirte_logger()

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = he_xun_database


class HeXunInformation(BaseModel):
    id = IntegerField()
    title = CharField(null=True)
    source_link = CharField(null=True)
    author = CharField(null=True)
    content_id = IntegerField(null=True)
    content = CharField(null=True)
    source_name = CharField(null=True)
    match_img = CharField(null=True)
    crawler_date = CharField(null=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'he_xun_information'


class PeopleCnInformation(BaseModel):
    content_id = CharField()
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = "people_cn_information"