from peewee import *
from playhouse.shortcuts import model_to_dict


# 支持原生sql
def excute_sql(table, sql):
    query_result = table.raw(sql)
    return query_result.execute()


# model转换为dict
def model_to_dicts(rows):
    content_ls = [model_to_dict(x) for x in rows]
    return content_ls