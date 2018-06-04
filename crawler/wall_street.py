import sys
import os

currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl,os.pardir))
sys.path.append(parentUrl)

from spiders.spider_wall_street import *
from common.initRedis import connetcredis
from common.untils import *
from common.constants import RedisConstantsKey,GetListLength,DuplicateRemovalCache
from celerymain.main import app
from common.initlog import Logger
# from database.wall_street_information_module import WallStreetInformation
from spiders.wall import crawler_wall_street_information
logger = Logger(kind="work_path", name="coin_world")


@app.task(ignore_result=True)
def wall_street_information(url):
    logger.info("华尔街快讯抓取链接：%s" % url)
    date = get_current_date()
    crawler_data = crawler_wall_street_information(url,logger)
    print(crawler_data)
    # if len(crawler_data)!=GetListLength.GET_LIST_LENGTH.value:
    #     for data in crawler_data:
    #         cache_data = connetcredis().get("%s_%s" % (RedisConstantsKey.CRAWLER_BA_BI_TE.value, data["url"]))




if __name__=="__main__":
    wall_street_information("https://api-prod.wallstreetcn.com/apiv1/content/lives?channel=blockchain-channel&limit=10")