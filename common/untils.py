# encoding=utf-8

import json


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