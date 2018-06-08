import os
import sys
from peewee import *
import datetime


currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel


wall_street = InitDb(SpidersDataModel.MODEL_COIN_WORLD.value)   #连接的coin_world数据库
wall_street_database = wall_street.connect()
#_street.wirte_logger()

class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = wall_street_database


class WallStreetInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = AutoField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'wall_street_information'










