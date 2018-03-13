# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from common.initRedis import connetcredis
from common.untils import *
from database.ablink_portal_summary import AblinkPortalSummary
import time
from common.constants import GetListLength, DuplicateRemovalCache


@app.task()
def async_get_data():
    date = get_current_date()
    rows = AblinkPortalSummary.select().order_by(AblinkPortalSummary.obtaindate.desc()).limit(1000)
    content_ls = []
    for row in rows:
        time_local = time.localtime(row.obtaindate)
        dt = time.strftime("%Y-%m-%d", time_local)
        if dt == date:
            content_ls.append(row.title)
    return content_ls


@app.task()
def async_create_data(title, source_name):
    obtain_date = int(time.time())
    AblinkPortalSummary.create(title=title,
                               source=source_name,
                               obtaindate=obtain_date)


@app.task()
def duplicate_removal_work():
    # 从redis集合中获取获取
    red = connetcredis()
    date = get_current_date()
    data = red.smembers("%s_%s" % ((DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE).value, date))
    if len(data) != GetListLength.GET_LIST_LENGTH.value:
        data = [str_convert_json(x) for x in data]
        i = GetListLength.GET_LIST_LENGTH.value
        while i < len(data):
            for j in range(i + 1, len(data)):
                if j >= len(data):
                    break
                str1 = data[i]["content"]
                str2 = data[j]["content"]
                distance = (Simhash(str1).distance(Simhash(str2)))
                # 相同的数据
                if distance <= GetListLength.GET_NOMBAL_NUM.value:
                    del data[j]
            i = i + 1
        # 去重数据异步入库并且查询当天数据
        # 链接服务器操作数据库
        # 异步查询
        result = async_get_data.apply_async()
        base_data = result.get()
        if len(base_data) == GetListLength.GET_LIST_LENGTH.value:
            print("aaa")
            # todo数据库操作
            # for com_data in data:
            #     AblinkPortalSummary.create(title=com_data["title"],
            #                                content=com_data["content"],
            #                                source_link=com_data["source_name"],
            #                                current_time=date)
        else:
            for com_data in data:
                for row in base_data:
                    distance = get_str_distance(com_data["content"], row.content)
                    if distance >= GetListLength.GET_NOMBAL_NUM.value:
                        async_create_data.apply_async((com_data["title"] ,com_data["source_name"]))
        # 清空数据集合
        red.delete("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date))


# if __name__ == "__main__":
#     asyn_get_data()
#     r = connetcredis()
#     r.set('name', 'junxi')
#     print(r['name'])
#     print(r.get('name'))  # 取出键name对应的值
#     print(type(r.get('name')))
#     # duplicate_removal