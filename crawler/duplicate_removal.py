# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from simhash import Simhash
# from celerymain.main import app
from common.initRedis import connetcredis
from common.constants import *
from common.untils import *
from database.demo import TestSpider


# @app.task()
def duplicate_removal():
    # 从redis集合中获取获取
    red = connetcredis()
    date = get_current_date()
    data = red.smembers("%s_%s" % ((DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE).value, date))
    if len(data) != GetListLength.GET_LIST_LENGTH.value:
        data = [str_convert_json(x) for x in data]
        i = GetListLength.GET_LIST_LENGTH
        while i < len(data):
            for j in range(i + 1, len(data)):
                if j >= len(data):
                    break
                str1 = data[i]["content"]
                str2 = data[j]["content"]
                distance = (Simhash(str1).distance(Simhash(str2)))
                # 相同的数据
                if distance <= GetListLength.GET_NOMBAL_NUM.value:
                    del data[i]
            i = i + 1
        # 去重数据异步入库并且查询当天数据
        rows = TestSpider.select().where(TestSpider.current_time == date)
        if len(rows) == GetListLength.GET_LIST_LENGTH.value:
            # 数据库操作
            TestSpider.create(title=com_data["title"],
                              content=com_data["content"],
                              source_link=com_data["source_name"],
                              current_time=date)
        else:
            for com_data in data:
                for row in rows:
                    distance = (Simhash(com_data["content"]).distance(Simhash(row.content)))
                    if distance >= GetListLength.GET_NOMBAL_NUM.value:
                        TestSpider.create(title=com_data["title"],
                                          content=com_data["content"],
                                          source_link=com_data["source_name"],
                                          current_time=date)
        # 清空数据集合
        red.delete("%s_%s" % (DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value, date))



# if __name__ == "__main__":
#     duplicate_removal()
#     r = connetcredis()
#     r.set('name', 'junxi')
#     print(r['name'])
#     print(r.get('name'))  # 取出键name对应的值
#     print(type(r.get('name')))
#     # duplicate_removal