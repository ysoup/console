# encoding=utf-8
from enum import Enum,unique


@unique
class CompareResult(Enum):
    StrSame = 1
    StrDiff = 0


@unique
class RedisConstantsKey(Enum):
    DEMO_CRAWLER_SAVE = "demo_crawler_save"