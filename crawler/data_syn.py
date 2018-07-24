# encoding=utf-8

import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celerymain.main import app
from common.initRedis import connetcredis
from database.discuzdb import AblinkPortalArticleContent,AblinkPortalArticleTitle
from common.untils import *
from common.get_article_content import Extractor
from common.initlog import Logger
import random
from hdfs.client import Client
import urllib.request
import urllib3

logger = Logger(kind="work_path", name="data_syn")
path = os.path.dirname(__file__)

# 读取配置文件
with open("../config/crawler.json", "r") as fi:
    load_dict = json.load(fi)

def retry_if_io_error(exception):
    print(exception)
    return isinstance(exception, urllib3.exceptions.NewConnectionError)


@app.task()
def data_syn_work():
    # 从redis集合中获取获取
    logger.info("=====开始数据同步服务====")
    redis = connetcredis()
    date = get_current_date()
    # 查询discuzs当天数据和历史数据数据
    # 获取5.7之前的数据
    # Employee.select().where(Employee.salary.between(50000, 60000))
    title_rows = AblinkPortalArticleTitle.select(AblinkPortalArticleTitle.aid, AblinkPortalArticleTitle.username,
                                                 AblinkPortalArticleTitle.title, AblinkPortalArticleTitle.dateline,
                                                 AblinkPortalArticleTitle.pic).where(
        AblinkPortalArticleTitle.dateline.between(0, 1525622400))
    content_rows = AblinkPortalArticleContent.select(AblinkPortalArticleContent.cid, AblinkPortalArticleContent.aid,
                                                     AblinkPortalArticleContent.content,
                                                     AblinkPortalArticleContent.dateline).where(
        AblinkPortalArticleContent.dateline.between(0, 1525622400))

    data_ls = []
    if load_dict.__contains__('hadoop'):
        host = load_dict["hadoop"]["host"]
        port = load_dict["hadoop"]["port"]
        client = Client('{host}:{port}'.format(host=host, port=port), timeout=600)
        dir_ls = client.list("/")
        if "images" not in dir_ls:
            client.makedirs("/images")
    for title_data in title_rows:
        for content_data in content_rows:
            if title_data.aid == content_data.aid:
                discuzs_dict = {}
                discuzs_dict["content"] = content_data.content
                # content_soup = BeautifulSoup(discuzs_dict["content"], "lxml")
                imgs_ls = re.compile(r'<img[\s\S]*?src=[\'|"]([\s\S]*?)[\'|"][\s\S]*?>').findall(discuzs_dict["content"])

                new_img_ls = []
                for i in range(0, len(imgs_ls)):
                    img_exist = os.path.exists("/"+imgs_ls[i])
                    if img_exist:
                        img_name = "%s_%s_%s.jpg" % ("discuzs", content_data.cid, i)
                        client.upload("/images", "/"+imgs_ls[i], overwrite=True)
                    else:
                        if "http" in imgs_ls[i]:
                            img_name = "%s_%s_%s.jpg" % ("discuzs", content_data.cid, i)
                            print(imgs_ls[i])
                            response = urllib.request.urlopen(imgs_ls[i])
                            pic = response.read()
                            with open("%s/%s/%s" % (path, "tmp_images", img_name), 'wb') as f:
                                f.write(pic)
                            client.upload("/images", "%s/%s/%s" % (path, "tmp_images", img_name), overwrite=True)
                        else:
                            default_image_ls = ["default_image_0.jpg", "default_image_1.jpg", "default_image_2.jpg",
                                                "default_image_3.jpg"]
                            i = random.randint(0, 3)
                            img_name = default_image_ls[i]
                    new_img_ls.append("/aibicloud/images/" + img_name)
                img_ls = ",".join(new_img_ls)
                discuzs_dict["title"] = title_data.title
                discuzs_dict["author"] = title_data.username
                discuzs_dict["create_time"] = content_data.dateline
                discuzs_dict["img"] = img_ls
                data_ls.append(discuzs_dict)
    # 数据去重
    i = 0
    while i < len(data_ls):
        for j in range(i + 1, len(data_ls)):
            if j >= len(data_ls):
                break
            content_1 = data_ls[i]["content"]
            content_2 = data_ls[j]["content"]
            # distance = get_content_by_reg(content_1, content_2)
            # 标题
            ext_1 = Extractor(content=content_1, blockSize=15, image=False)
            ext_1_text = ext_1.getContext()
            ext_2 = Extractor(content=content_2, blockSize=15, image=False)
            ext_2_text = ext_2.getContext()
            # 内容
            distance = get_str_distance(ext_1_text, ext_2_text)

            distance1 = get_str_distance(data_ls[i]["title"], data_ls[j]["title"])
            if distance <= 10 or distance1 <= 10:
                print("当前数据:%s" % ext_1_text)
                print("相似数据:%s" % ext_2_text)
                del data_ls[j]
        i = i + 1
    print(data_ls)


def get_content_by_reg(content_1, content_2):
    ext_1 = Extractor(content=content_1, blockSize=15, image=False)
    ext_1_text = ext_1.getContext()
    ext_2 = Extractor(content=content_2, blockSize=15, image=False)
    ext_2_text = ext_2.getContext()
    # 内容
    distance = get_str_distance(ext_1_text, ext_2_text)
    return distance
            

    # rows = AblinkPortalSummary.select().order_by(AblinkPortalSummary.id.desc()).limit(200)
    
    # for row in rows:
    #     time_array = time.localtime(row.obtaindate)
    #     crawler_time = time.strftime('%Y-%m-%d', time_array)
    #     if crawler_time == date:
    #         if row.source is not None:
    #             if row.source != "金色财经":
    #                 cache_data = redis.get("%s_%s" % (RedisConstantsKey.DATA_SYN_WORK.value, row.id))
    #                 if cache_data is not None:
    #                     dic = {}
    #                     dic["content"] = re.sub("币世界|小葱|金色财经", "爱必投", row.title)
    #                     dic["content_id"] = row.id
    #                     dic["source_link"] = ""
    #                     dic["title"] = ""
    #                     dic["author"] = ""
    #                     dic["source_name"] = "yun_cai"
    #                     redis.set("%s_%s" % (RedisConstantsKey.DATA_SYN_WORK.value, row.id), json_convert_str(dic))
    #                     redis.lpush(DuplicateRemovalCache.FIRST_DUPLICATE_REMOVAL_CACHE.value,
    #                                 json_convert_str(dic))
    logger.info("=====数据同步服务结束====")


@app.task(ignore_result=True)
def schudule_data_syn_work():
    app.send_task('crawler.data_syn.data_syn_work', queue='data_syn_task', routing_key='data_syn_info')


if __name__ == "__main__":
    data_syn_work()
    # r = connetcredis()
    # r.set('name', 'junxi')
    # print(r['name'])
    # print(r.get('name'))  # 取出键name对应的值
    # print(type(r.get('name')))
    # duplicate_removal_work()