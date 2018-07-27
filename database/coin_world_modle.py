from peewee import *
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel
import datetime

coin_world = InitDb(SpidersDataModel.MODEL_COIN_WORLD.value)
coin_world_database = coin_world.connect()
coin_world.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = coin_world_database


class CoinWorldInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = AutoField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'coin_world_information'


class BtcInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'btc_information'


class BiaNewsInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'bianews_information'


class CailianpressInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'cailianpress_information'


class KrInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'kr_information'


class HuoBiInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'huo_bi_information'


class PublicInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = AutoField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    source_name = CharField(null=True)

    class Meta:
        table_name = 'public_information'

