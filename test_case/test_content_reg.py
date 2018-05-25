import re
import redis
import json
pool = redis.ConnectionPool(host='127.0.0.1', port=6379, decode_responses=True)
r = redis.Redis(connection_pool=pool)
data = r.get("catch_infomation_categery_list")
filter_content = ["空投", "糖果", "正式上线", "上币", "上币结果", "投票结果"]
modfiy_ls = ["币世界", "小葱", "金色财经", "币 世 界", "bishijie.com", "bishijie", "《币 世 界》（bishijie.com）",
             "《币世界》（bishijie）"]
str1 = '''
币世界今晚8点公开课！快进直播间
鳄鱼今晚8点做客币世界公开课，为币友们分享“在熊市中如何让数字资产翻5倍”。听课请关注“币世界公开课”微信公众号，回复“公开课”，获取听课链接。
'''
category = 0
if data is not None:
    data = json.loads(data)
    for x in data:
        for j in x["keyword"].split(","):
            if j in str1:
                category = x["id"]
                break
is_show = 1
for x in filter_content:
    if x in str1:
        is_show = 0
        break

modify_tag = 0
for x in modfiy_ls:
    if x in str1:
        modify_tag = 1
        break
str1 = re.sub("币世界|小葱|金色财经|币 世 界|《币 世 界》|《币世界》", "爱必投", str1)
str1 = re.sub("Bitfinex", "现货", str1)
str1 = re.sub("newsbtc", "数资界媒体", str1)
str1 = re.sub("bishijie", "aibilink", str1)
print(str1)



from PIL import Image
