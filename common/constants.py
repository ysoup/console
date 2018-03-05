# encoding=utf-8
from enum import Enum, unique


@unique
class CompareResult(Enum):
    StrSame = 1
    StrDiff = 0


@unique
class RedisConstantsKey(Enum):
    DEMO_CRAWLER_SAVE = "demo_crawler_save"


@unique
class DuplicateRemovalCache(Enum):
    FIRST_DUPLICATE_REMOVAL_CACHE = "first_duplicate_removal_cache"
    SECOND_DUPLICATE_REMOVAL_CACHE = "second_duplicate_removal_cache"


@unique
class GetListLength(Enum):
    GET_LIST_LENGTH = 0
    GET_NOMBAL_NUM = 3