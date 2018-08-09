from peewee import *
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from common.initDb import InitDb
from common.constants import SpidersDataModel
import datetime

spiders_visualization = InitDb(SpidersDataModel.Model_SPIDERS_VISUALIZATION.value)
spiders_visualization_database = spiders_visualization.connect()
spiders_visualization.wirte_logger()


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = spiders_visualization_database


class SpidersVisualizationBase(BaseModel):
    fliter_a_tag = IntegerField(null=True)
    get_num = IntegerField(null=True)
    html_ls_tag = CharField(null=True)
    img_watermark = IntegerField(null=True)
    is_userful = IntegerField(null=True)
    ls_rule_type = IntegerField(null=True)
    req_code = CharField(null=True)
    req_headers = CharField(null=True)
    req_method = IntegerField(null=True)
    req_params = CharField(null=True)
    spider_ch_name = CharField(null=True)
    spider_en_name = CharField(null=True)
    target_url = CharField()
    time_interval = IntegerField(null=True)
    information_type = IntegerField(null=True)

    class Meta:
        table_name = 'spiders_visualization_base'


class SpidersVisualizationDataHandle(BaseModel):
    delete_tag = CharField(null=True)
    end_replace_tag = CharField(null=True)
    replace_tag = CharField(null=True)
    rule = IntegerField(column_name='rule_id')
    type = IntegerField()

    class Meta:
        table_name = 'spiders_visualization_data_handle'
        primary_key = False


class SpidersVisualizationRule(BaseModel):
    analysis_code = CharField(null=True)
    base_id = IntegerField(column_name='base_id')
    ch_name = CharField(null=True)
    column_rule_type = IntegerField(null=True)
    column_type = IntegerField(null=True)
    en_name = CharField(null=True)
    get_column_rule = CharField(null=True)
    get_data_way = IntegerField(null=True)
    start_for = IntegerField(null=True)

    class Meta:
        table_name = 'spiders_visualization_rule'


class AiSpiders(BaseModel):
    seach_type = IntegerField()
    seach_content = CharField()
    is_useful = IntegerField()
    num = IntegerField()
    page_num = IntegerField()
    headers = CharField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'ai_spiders'


class WebsiteWhite(BaseModel):
    website_name = CharField()
    website_url = CharField()
    is_useful = IntegerField()
    create_time = DateTimeField(default=datetime.datetime.now)
    update_time = DateTimeField(default=datetime.datetime.now)

    class Meta:
        table_name = 'website_white'