__author__ = 'Administrator'
from peewee import *

from dal.DataSource import demo_database


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = demo_database


class TestSpider(BaseModel):
    id = IntegerField()
    title = IntegerField()
    content = CharField()
    author = CharField()
    source_link = CharField()
    create_time = CharField()
    update_time = CharField()

    class Meta:
        db_table = 'test_spider'