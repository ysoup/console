import sys
import os
from peewee import *
import datetime

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel

jin_shi = InitDb(SpidersDataModel.MODEL_COIN_WORLD.value)
jin_shi_database = jin_shi.connect()
jin_shi.wirte_logger()

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = jin_shi_database


class JinShiInformation(BaseModel):
    id = IntegerField()
    crawler_time =CharField(null=True)
    content = CharField(null=True)
    content_id = CharField()
    title = CharField(null=True)
    author = CharField(null=True)
    source_name = CharField(null=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'jin_shi_info'
