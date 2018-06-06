import os
import sys
from peewee import *
import datetime


currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel


okex = InitDb(SpidersDataModel.MODEL_COIN_WORLD.value)   #连接的coin_world数据库
okex_database = okex.connect()
# okex.wirte_logger()

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = okex_database


class OKExInformation(BaseModel):
    id = IntegerField()
    title = CharField(null=True)
    source_link = CharField(null=True)
    content_id = CharField(null=True)
    content = CharField(null=True)
    source_name = CharField(null=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'okex_information'


