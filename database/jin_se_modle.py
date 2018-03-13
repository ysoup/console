import sys
import os
from peewee import *
import datetime

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel


jin_se = InitDb(SpidersDataModel.MODEL_JIN_SE.value)
jin_se_database = jin_se.connect()
jin_se.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = jin_se_database


class JinseInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = IntegerField()
    create_time = DateTimeField(default=datetime.datetime.now)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'jinse_information'
        indexes = (
            (('id', 'content_id'), True),
        )
        primary_key = CompositeKey('content_id', 'id')

