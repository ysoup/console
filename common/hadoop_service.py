# encoding=utf-8
from hdfs.client import Client
import json
import urllib.request
import os
import urllib3
from retrying import retry

path = os.path.dirname(__file__)

# 读取配置文件
with open("../config/crawler.json", "r") as fi:
    load_dict = json.load(fi)


def retry_if_io_error(exception):
    print(exception)
    return isinstance(exception, urllib3.exceptions.NewConnectionError)


@retry(retry_on_exception=retry_if_io_error)
def upload_images_hdfs(img_url, source_name, content_id, i):
    if load_dict.__contains__('hadoop'):
        host = load_dict["hadoop"]["host"]
        port = load_dict["hadoop"]["port"]
        client = Client('{host}:{port}'.format(host=host, port=port), timeout=600)
        img_ls = []
        dir_ls = client.list("/")
        if "images" not in dir_ls:
            client.makedirs("/images")
        url = "http://www.bitcoin86.com" + img_url if source_name == "bit_coin" else img_url
        img_name = "%s_%s_%s.jpg" % (source_name, content_id, i)
        response = urllib.request.urlopen(url)
        pic = response.read()
        with open("%s/%s/%s" % (path, "images", img_name), 'wb') as f:
            f.write(pic)
        client.upload("/images", "%s/%s/%s" % (path, "images", img_name), overwrite=True)
        new_img_url = "/aibicloud/images/" + img_name
    return new_img_url





# def retry_if_io_error(exception):
#     return isinstance(exception, IOError)
#
#
# @retry(retry_on_exception=retry_if_io_error)
# def read_a_file():
#     with open("file", "r") as f:
#         return f.read()
