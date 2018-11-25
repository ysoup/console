from peewee import *

database = MySQLDatabase('user', **{'passwd': 'soup', 'use_unicode': True, 'port': 3306, 'user': 'root', 'charset': 'utf8', 'host': '58.87.70.179'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AccountManage(BaseModel):
    account_article_num = IntegerField(null=True)
    account_index = IntegerField(null=True)
    account_name = CharField(unique=True)
    account_password = CharField(null=True)
    account_rank = IntegerField(null=True)
    account_type = IntegerField(null=True)
    category_type = IntegerField(null=True)
    create_time = DateTimeField()
    credit_score = IntegerField(null=True)
    nick_name = CharField(null=True)
    platform_type = IntegerField(null=True)
    total_play_num = IntegerField(null=True)
    total_read_num = IntegerField(null=True)
    total_subscribe_num = IntegerField(null=True)
    update_time = DateTimeField()

    class Meta:
        table_name = 'account_manage'
        schema = 'oup'

class ArticleManage(BaseModel):
    article_content = TextField(null=True)
    article_cover = CharField(null=True)
    article = CharField(column_name='article_id', null=True, unique=True)
    article_title = CharField()
    article_type = IntegerField(null=True)
    category_type = IntegerField(null=True)
    create_time = DateTimeField()
    is_send = IntegerField(null=True)
    source_name = CharField(null=True)
    update_time = DateTimeField()

    class Meta:
        table_name = 'article_manage'
        schema = 'oup'

class ArticleUploadManage(BaseModel):
    account_name = CharField()
    article = CharField(column_name='article_id', null=True)
    article_type = IntegerField(null=True)
    category_type = IntegerField(null=True)
    create_time = DateTimeField()
    platform_type = IntegerField(null=True)
    send_ids = CharField(null=True)
    send_status = IntegerField(null=True)
    send_time = CharField(null=True)
    send_type = IntegerField(null=True)
    update_time = DateTimeField()

    class Meta:
        table_name = 'article_upload_manage'
        schema = 'oup'

class InformationCategory(BaseModel):
    category_name = CharField(null=True)
    create_time = DateTimeField()
    update_time = DateTimeField()

    class Meta:
        table_name = 'information_category'
        schema = 'oup'

class InformationPlatform(BaseModel):
    create_time = DateTimeField()
    platform_name = CharField(null=True)
    update_time = DateTimeField()

    class Meta:
        table_name = 'information_platform'
        schema = 'oup'

class User(BaseModel):
    email = CharField(null=True, unique=True)
    last_seen = DateTimeField(null=True)
    password = CharField(null=True)
    phone_no = IntegerField(null=True, unique=True)

    class Meta:
        table_name = 'user'
        schema = 'oup'

