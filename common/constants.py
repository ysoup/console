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
    DATA_SYN_WORK = "data_syn_work"
    CRAWLER_BA_BI_TE = "crawler_ba_bi_te"
    CRAWLER_BIT_COIN = "crawler_bit_coin"
    CRAWLER_BTC_NEW_FLASH = "crawler_btc_new_flash"
    CRAWLER_WALL_STREET = "crawler_wall_street"  #华尔街快讯
    CRAWLER_BIAN_NEW_FLASH = "crawler_bian_new_flash"
    CRAWLER_CAILIANPRESS = "crawler_cailianpress"
    CRAWLER_KR = "crawler_kr"
    CRAWLER_HUO_BI = "crawler_huo_bi"
    # CRAWLER_WALL_STREET = "crawler_wall_street"  # 华尔街快讯
    CRAWLER_PEOPLE_CN = "crawler_people_cn"  # 人民网资讯


@unique
class DuplicateRemovalCache(Enum):
    # 快讯去重队列
    FIRST_DUPLICATE_REMOVAL_CACHE = "first_duplicate_removal_cache"
    SECOND_DUPLICATE_REMOVAL_CACHE = "second_duplicate_removal_cache"

    # 资讯去重队列
    FIRST_INFO_DUPLICATE_REMOVAL_CACHE = "first_info_duplicate_removal_cache"
    SECOND__INFO_DUPLICATE_REMOVAL_CACHE = "second_info_duplicate_removal_cache"


@unique
class GetListLength(Enum):
    GET_LIST_LENGTH = 0
    GET_NOMBAL_NUM = 3


@unique
class SpidersDataModel(Enum):
    MODEL_JIN_SE = "jin_se"
    MODEL_COIN_WORLD = "coin_world"
    MODEL_NEW_FLASH = "new_flash"
    MODEL_DISCUZDB = "discuzdb"
    MODEL_EIGHT_BITE = "eight_bite"
    MODEL_WALL_STREET = "wall_street"



@unique
class CrawlerLogName(Enum):
    OPERTATION_PEEWEE_MODEL = "peewee"


@unique
class GetBaiDuAi(Enum):
    APP_ID = '11092811'
    API_KEY = 'huEevuInLRqMFrNgcsK2rkxg'
    SECRET_KEY = 'KbAiQCrF78gqq3eRu6eFGrz9Vq5hBQc0'