__author__ = 'Administrator'
from peewee import *
import datetime
import yaml
import logging
from dal.DataSource import demo_database
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class UnknownField(object):
    pass


class BaseModel(Model):
    class Meta:
        database = demo_database


class TestSpider(BaseModel):
    id = IntegerField()
    title = CharField()
    content = CharField()
    author = CharField()
    source_link = CharField()
    current_time = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        db_table = 'test_spider'