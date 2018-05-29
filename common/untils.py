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


def check_news_content_type(str1, data):
    category = 0
    if data is not None:
        data = json.loads(data)
        for x in data:
            for j in x["keyword"].split(","):
                if j in str1:
                    category = x["id"]
                    break

    filter_content = ["巴比特每日热聊榜"]
    is_show = 1
    for x in filter_content:
        if x in str1:
            is_show = 0
            break
    return category, is_show


def check_content_type(str1, data, rule_data):
    filter_content = ["空投", "糖果", "正式上线", "上币", "上币结果", "投票结果", "直播", "金色讲堂", "利好", "利空一览表",
                      "分享会", "公开课", "名家论市", "币市龙虎榜", "币市风云榜", "(推广)"]
    modfiy_ls = ["币世界", "小葱", "金色财经", "币 世 界", "bishijie.com", "bishijie", "《币 世 界》（bishijie.com）",
                 "《币世界》（bishijie）", "newsbtc", "Bitfinex", "bishijie"]
    category = 0
    # 文本过滤
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
    # 文本替换
    rule_data = json.loads(rule_data)if rule_data else modfiy_ls
    replace_ls = [x["origin_name"]for x in rule_data]
    modify_tag = 0
    for x in replace_ls:
        if x in str1:
            modify_tag = 1
            break
    for x in rule_data:
        str1 = re.sub(x["origin_name"], x["rule_name"], str1)
    # str1 = re.sub("币世界|小葱|金色财经|币 世 界|《币 世 界》|《币世界》", "爱必投", str1)
    # str1 = re.sub("Bitfinex", "现货", str1)
    # str1 = re.sub("newsbtc", "数资界媒体", str1)
    # str1 = re.sub("bishijie", "aibilink", str1)
    return category, is_show, modify_tag, str1


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