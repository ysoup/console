# encoding=utf-8

import json
import time
from simhash import Simhash
import re


def compare_string(str1, str2):
    str1 = encode(str1)
    str2 = encode(str2)
    ret = 0
    if str1 == str2:
        ret = 1
        return ret
    else:
        return ret


def encode(str1):
    return ''.join([bin(ord(c)).replace('0b', '') for c in str1])


def json_convert_str(str1):
    return json.dumps(str1)


def str_convert_json(str1):
    return json.loads(str1)


def get_current_date():
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def get_current_time():
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))


def get_str_distance(str1, str2):
    distance = (Simhash(str1).distance(Simhash(str2)))
    return distance


def check_content_type(str1, data):
    filter_content = ["空投", "糖果", "正式上线", "上币", "上币结果", "投票结果"]
    category = 0
    if data is not None:
        data = json.loads(data)
        for x in data:
            for j in x["keyword"].split(","):
                if j in str1:
                    category = x["id"]
                    break
    is_show = 1
    for x in filter_content:
        if x in str1:
            is_show = 0
            break
    return category, is_show
    # category1 = re.search(r"监管|政策|法律|央行|实施|违法|财长|出台", str1)
    # category2 = re.search(r"\\%|下跌|上涨|涨跌|交易量|涨幅|跌幅|价格|大跌|暴跌|市值|反弹|期货|回血", str1)
    # category3 = re.search(r"发表|表示|说|宣布|认为|观点", str1)
    # category4 = re.search(r"公告|上线", str1)
    # if category1 is not None:
    #     category = 1
    # elif category2 is not None:
    #     category = 2
    # elif category3 is not None:
    #     category = 4
    # elif category4 is not None:
    #     category = 3
    # return category