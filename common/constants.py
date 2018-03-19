# encoding=utf-8
from enum import Enum, unique


@unique
class CompareResult(Enum):
    StrSame = 1
    StrDiff = 0


@unique
class RedisConstantsKey(Enum):
    DEMO_CRAWLER_SAVE = "demo_crawler_save"
    CRAWLER_JIN_SE = "crawler_jin_se"  # 金色财经
    CRAWLER_COIN_WORLD = "crawler_coin_world"  # 币世界


@unique
class DuplicateRemovalCache(Enum):
    FIRST_DUPLICATE_REMOVAL_CACHE = "first_duplicate_removal_cache"
    SECOND_DUPLICATE_REMOVAL_CACHE = "second_duplicate_removal_cache"


@unique
class GetListLength(Enum):
    GET_LIST_LENGTH = 0
    GET_NOMBAL_NUM = 3

@unique
class SpidersDataModel(Enum):
    MODEL_JIN_SE = "jin_se"
    MODEL_COIN_WORLD = "coin_world"
    MODEL_NEW_FLASH = "new_flash"

@unique
class CrawlerLogName(Enum):
    OPERTATION_PEEWEE_MODEL = "peewee"