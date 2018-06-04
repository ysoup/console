from peewee import *
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel

summary = InitDb(SpidersDataModel.MODEL_DISCUZDB.value)
summary_database = summary.connect()
summary.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = summary_database


class AblinkPortalSummary(BaseModel):
    abstractid = IntegerField()
    artificial = IntegerField()
    category = CharField()
    catid = IntegerField()
    content = TextField(null=True)
    dateline = IntegerField()
    deleted = IntegerField()
    frequency = CharField()
    grab = IntegerField()
    link = CharField()
    obtaindate = IntegerField()
    push = IntegerField()
    remarks = CharField()
    shows = IntegerField()
    source = CharField()
    sparea = CharField()
    spareb = CharField()
    summary = CharField()
    title = TextField(null=True)

    class Meta:
        table_name = 'ablink_portal_summary'


class AblinkPortalArticleContent(BaseModel):
    cid = IntegerField()
    aid = IntegerField()
    id = IntegerField()
    idtype = CharField()
    title = CharField()
    content = CharField()
    pageorder = IntegerField()
    dateline = CharField()

    class Meta:
        table_name = 'ablink_portal_article_content'


class AblinkPortalArticleTitle(BaseModel):
    aid = IntegerField()
    catid = IntegerField()
    bid = IntegerField()
    uid = IntegerField()
    username = CharField()
    title = CharField()
    highlight = CharField()
    author = CharField()
    fromurl = CharField()
    url = CharField()
    summary = CharField()
    pic = CharField()
    thumb = IntegerField()
    remote = IntegerField()
    id = IntegerField()
    idtype = CharField()
    contents = IntegerField()
    allowcomment = IntegerField()
    owncomment = IntegerField()
    tag = IntegerField()
    dateline = IntegerField()
    status = IntegerField()
    showinnernav = IntegerField()
    preaid = IntegerField()
    nextaid = IntegerField()
    htmlmade = IntegerField()
    htmlname = CharField()
    htmldir = CharField()
    asas = CharField()
    fdgdfg = IntegerField()
    abstract = IntegerField()
    deleted = IntegerField()

    class Meta:
        table_name = 'ablink_portal_article_title'








