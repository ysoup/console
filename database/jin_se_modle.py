from peewee import *
import datetime
import logging
from dal.DataSource import ji_se_database
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = ji_se_database


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

