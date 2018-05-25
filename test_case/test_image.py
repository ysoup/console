from PIL import Image
import os
path = os.path.dirname(__file__)


from PIL import Image

'''
   @author:xunalove
    修改文件位置
    修改图片id

'''
def cut():
    #打开图片图片1.jpg
    name3 = "test.jpg"
    im =Image.open("%s/%s/%s" % (path, "images", "bit_coin_22481_1.jpg"))
    default_x = 419
    default_y = 360
    img_size = im.size
    crop_val = round((default_y*img_size[1])/default_x)
    im2 = im.crop((0, 0, img_size[0], crop_val))
    im2.save("%s/%s/%s" % (path, "images", "bit_coin_22481_1.jpg"))


if __name__=="__main__":

    #取图片id的后两位
    id = "1"

    #切割图片的面积 vx,vy
    #大
    res = cut()

    #中
    #res = cut(id,120,120)

    #小
    #res = cut(id,80,80)

    print(res)
