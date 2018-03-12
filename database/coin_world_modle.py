from peewee import *
from dal.DataSource import coin_world_database
import logging
logger = logging.getLogger('peewee')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = coin_world_database


class CoinWorldInformation(BaseModel):
    author = CharField(null=True)
    content = CharField(null=True)
    content_id = IntegerField()
    create_time = DateTimeField(null=True)
    id = IntegerField()
    source_link = CharField(null=True)
    title = CharField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'coin_world_information'
        indexes = (
            (('id', 'content_id'), True),
        )
        primary_key = CompositeKey('content_id', 'id')

