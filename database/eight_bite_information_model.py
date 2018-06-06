import sys
import os
from peewee import *
import datetime

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel


eight_btc = InitDb(SpidersDataModel.MODEL_EIGHT_BITE.value)
eight_btc_database = eight_btc.connect()
eight_btc.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = eight_btc_database


class EightBiteInformation(BaseModel):
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)
    
    class Meta:
        table_name = 'eight_bite_information'


class BitCoinInformation(BaseModel):
    content_id = IntegerField()
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'bit_coin_information'


class DiscuzsInformation(BaseModel):
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'discuzs_information'


class ChainDdInformation(BaseModel):
    content_id = IntegerField()
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'chaindd_information'


class WallStreetcnInformation(BaseModel):
    content_id = IntegerField()
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'wall_streetcn_information'


class TmtPostInformation(BaseModel):
    content_id = IntegerField()
    author = CharField(null=True)
    content = TextField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    img = CharField(null=True)
    crawler_url = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)
    create_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'tmt_post_information'


class WangYiInformation(BaseModel):
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
        table_name = 'wang_yi_information'

