# encoding=utf-8
from hdfs.client import Client
import json
import urllib.request
import os
import urllib3
from retrying import retry
import random
from PIL import Image

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
        dir_ls = client.list("/")
        if "images" not in dir_ls:
            client.makedirs("/images")
        if img_url:
            url = "http://www.bitcoin86.com" + img_url if source_name == "bit_coin" else img_url
            img_name = "%s_%s_%s.jpg" % (source_name, content_id, i)
            response = urllib.request.urlopen(url)
            pic = response.read()
            with open("%s/%s/%s" % (path, "images", img_name), 'wb') as f:
                f.write(pic)
        else:
            default_image_ls = ["default_image_0.jpg", "default_image_1.jpg", "default_image_2.jpg",
                                "default_image_3.jpg"]
            i = random.randint(0, 3)
            img_name = default_image_ls[i]
        if source_name == "bit_coin":
            im = Image.open("%s/%s/%s" % (path, "images", img_name))
            default_x = 419
            default_y = 360
            img_size = im.size
            crop_val = round((default_y * img_size[1]) / default_x)
            im2 = im.crop((0, 0, img_size[0], crop_val))
            im2.save("%s/%s/%s" % (path, "images", img_name))

        client.upload("/images", "%s/%s/%s" % (path, "images", img_name), overwrite=True)
        new_img_url = "/aibicloud/images/" + img_name
    return new_img_url


def img_cut_down(img_url, source_name, content_id, i):
    if load_dict.__contains__('hadoop'):
        host = load_dict["hadoop"]["host"]
        port = load_dict["hadoop"]["port"]
        client = Client('{host}:{port}'.format(host=host, port=port), timeout=600)
        dir_ls = client.list("/")
        if "images" not in dir_ls:
            client.makedirs("/images")
        if img_url:
            url = "http://www.bitcoin86.com" + img_url if source_name == "bit_coin" else img_url
            img_name = "%s_%s_%s.jpg" % (source_name, content_id, i)
            response = urllib.request.urlopen(url)
            pic = response.read()
            with open("%s/%s/%s" % (path, "images", img_name), 'wb') as f:
                f.write(pic)
        else:
            default_image_ls = ["default_image_0.jpg", "default_image_1.jpg", "default_image_2.jpg",
                                "default_image_3.jpg"]
            i = random.randint(0, 3)
            img_name = default_image_ls[i]
        if source_name == "bit_coin":
            im = Image.open("%s/%s/%s" % (path, "images", img_name))
            default_x = 419
            default_y = 360
            img_size = im.size
            crop_val = round((default_y * img_size[1]) / default_x)
            im2 = im.crop((0, 0, img_size[0], crop_val))
            im2.save("%s/%s/%s" % (path, "images", img_name))

        im = Image.open("%s/%s/%s" % (path, "images", img_name))
        img_size = im.size
        if img_size[0] > 568 and img_size[1] > 360:
            new_img = im.resize((568, 360), Image.ANTIALIAS)
            rgb_im = new_img.convert('RGB')
            rgb_im.save("%s/%s/%s" % (path, "images", img_name))
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
