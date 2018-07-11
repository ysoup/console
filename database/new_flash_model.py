from peewee import *
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel
import datetime

new_flash = InitDb(SpidersDataModel.MODEL_NEW_FLASH.value)
new_flash_database = new_flash.connect()
new_flash.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = new_flash_database


class NewFlashInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField(null=True)
    create_time = DateTimeField(default=datetime.datetime.now)
    source_name = CharField(null=True)
    title = CharField(null=True)
    is_show = IntegerField(default=1)
    category = CharField(default="")
    update_time = DateTimeField(default=datetime.datetime.now)
    re_tag = IntegerField(default=0)
    news_url = CharField(default="")
    possible_similarity = IntegerField(default=0)

    class Meta:
        table_name = 'new_flash_information'


class NewFlashCategory(BaseModel):
    catname = CharField(null=True, unique=True)
    keyword = CharField(default="")
    show = IntegerField(default=0)

    class Meta:
        table_name = 'new_flash_category'


class NewFlashExclusiveInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = CharField(null=True)
    source_name = CharField(null=True)
    title = CharField(null=True)
    is_show = IntegerField(default=1)
    category = CharField(default="")
    img = CharField(null=True)
    tag = CharField(null=True)
    is_delete = IntegerField(default=0)
    is_push = IntegerField(default=0)
    is_hot = IntegerField(default=0)
    remarks = TextField(null=True)
    img = CharField(null=True)
    source_url = CharField(default="")
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)
    possible_similarity = IntegerField(default=0)

    class Meta:
        table_name = 'new_flash_exclusive_information'


class NewsCategory(BaseModel):
    catname = CharField(null=True)
    is_show = IntegerField(default=0)
    is_delete = IntegerField(default=0)
    keyword = CharField(default="")

    class Meta:
        table_name = 'news_category'

