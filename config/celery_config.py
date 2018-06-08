# encoding=utf-8
from datetime import timedelta
from kombu import Exchange, Queue
import json
import os

curr_dir = os.path.dirname(os.path.realpath(__file__))
config_file = curr_dir + os.sep + "crawler.json"
# 读取配置文件
with open(config_file, "r") as fi:
    load_dict = json.load(fi)

# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True

CELERY_IMPORTS = ("crawler.spider", "crawler.coin_world", "crawler.duplicate_removal", "crawler.eight_btc",
                  "crawler.bit_coin", "crawler.information_duplicate_removal", "crawler.wall_street",
                  "crawler.people_cn", "crawler.jin_shi", "crawler.okex", "crawler.binance_notice",
                  "crawler.cailianpress_new_flash", "crawler.chaindd_news", "crawler.bian_new_flash",
                  "crawler.huo_bi_new_flash", "crawler.kr_new_flash", "crawler.sina_news", "crawler.tmt_post",
                  "crawler.wall_streetcn_news", "crawler.wang_yi_information", "crawler.btc_new_flash",
                  "crawler.he_xun")

# 使用redis 作为任务队列
# BROKER_URL = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB_NUM)
if load_dict.__contains__('redis'):
    x = load_dict["redis"][0]
    if x["name"] == "spider":
        host = x["host"][0]
        port = x["port"]
        BROKER_URL = "redis://%s:%s/0" % (host, port)
        # 后端缓存设置
        CELERY_RESULT_BACKEND = "redis://%s:%s/1" % (host, port)


# 后端数据存储设置
# CELERY_RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/10'

# 并发worker数
CELERYD_CONCURRENCY = 3

# 时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'

# 非常重要,有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

CELERYD_PREFETCH_MULTIPLIER = 4

# 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 200

CELERYD_TASK_TIME_LIMIT = 36000    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死

# BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 90}

# 任务发出后，经过一段时间还未收到acknowledge , 就将任务重新交给其他worker执行
CELERY_DISABLE_RATE_LIMITS = True

# 定义任务队列
# 路由健 以"task."开头的信息都进入default
# 路由健 以"web."开头的信息进入web_tasks队列

CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
    Queue('jin_se_task', exchange=Exchange('jin_se_task'), routing_key='jin_se_info'),
    Queue('coin_wold_task', exchange=Exchange('coin_world_task'), routing_key='coin_world_info'),
    Queue('duplicate_removal_task', exchange=Exchange('duplicate_removal_task'), routing_key='duplicate_removal_info'),
    # Queue('data_syn_task', exchange=Exchange('data_syn_task'), routing_key='data_syn_info'),
    Queue('eight_btc_task', exchange=Exchange('eight_btc_task'), routing_key='eight_btc_info'),
    Queue('bit_coin_task', exchange=Exchange('bit_coin_task'), routing_key='bit_coin_info'),
    Queue('news_duplicate_removal_task', exchange=Exchange('news_duplicate_removal_task'),
          routing_key='news_duplicate_removal_info'),
    Queue('wall_street_task', exchange=Exchange('wall_street_task'), routing_key='wall_street_info'),
    Queue('people_cn_task', exchange=Exchange('people_cn_task'), routing_key='people_cn_info'),
    Queue('btc_new_flash_task', exchange=Exchange('btc_new_flash_task'), routing_key='btc_new_flash_info'),
    Queue('bian_new_flash_task', exchange=Exchange('bian_new_flash_task'), routing_key='bian_new_flash_info'),
    Queue('cailianpress_new_flash_task', exchange=Exchange('cailianpress_new_flash_task'),
          routing_key='cailianpress_new_flash_info'),
    Queue('kr_new_flash_task', exchange=Exchange('kr_new_flash_task'), routing_key='kr_new_flash_info'),
    Queue('huo_bi_new_flash_task', exchange=Exchange('huo_bi_new_flash_task'), routing_key='huo_bi_new_flash_info'),
    Queue('chaindd_task', exchange=Exchange('chaindd_task'), routing_key='chaindd_info'),
    Queue('wall_streetcn_task', exchange=Exchange('wall_streetcn_task'), routing_key='wall_streetcn_info'),
    Queue('tmt_post_task', exchange=Exchange('tmt_post_task'), routing_key='tmt_post_info'),
    Queue('wang_yi_task', exchange=Exchange('wang_yi_task'), routing_key='wang_yi_info'),
    Queue('sina_news_task', exchange=Exchange('sina_news_task'), routing_key='sina_news_info'),
    Queue('jin_shi_task', exchange=Exchange('jin_shi_task'), routing_key='jin_shi_info'),
    Queue('okex_task', exchange=Exchange('okex_task'), routing_key='okex_info'),
    Queue('binance_notice_task', exchange=Exchange('binance_notice_task'), routing_key='binance_notice_info'),
    Queue('he_xun_task', exchange=Exchange('he_xun_task'), routing_key='he_xun_info')
)

# # 路由
# CELERY_ROUTES = {
#     'crawler.spider.schudule_crawler_task': {'queue': 'task_crawler', 'routing_key': 'task_crawler'},
#     'crawler.duplicate_removal.duplicate_removal_work': {'queue': 'task_crawler_duplicate', 'routing_key': 'task_crawler_duplicate'},
#     'crawler.coin_world.schudule_coin_world_information': {'queue': 'task_crawler_coin_wold', 'routing_key': 'task_coin_world'},
# }
# # 默认的交换机名字为 tasks
# CELERY_DEFAULT_EXCHANGE = 'tasks'
# # 默认的交换机类型为 topic
# CELERY_DEFAULT_EXCHANGE_KEY = 'topic'
# # 默认的路由键是default键符合上面的 default 队列.
# CELERY_DEFAULT_ROUTING_KEY = 'default'

# 定时任务
CELERYBEAT_SCHEDULE = {
    'jinse_crawler_schedule': {
        'task': 'crawler.spider.schudule_crawler_task',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'jin_se_task', 'routing_key': 'jin_se_info'}
    },
    'crawler_duplicate_schedule': {
        'task': 'crawler.duplicate_removal.schudule_duplicate_removal_work',
        'schedule': timedelta(seconds=15),
        # 'args': (redis_db),
        'options': {'queue': 'duplicate_removal_task', 'routing_key': 'duplicate_removal_info'}
    },
    'crawler_coin_world': {
        'task': 'crawler.coin_world.schudule_coin_world_information',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'coin_wold_task', 'routing_key': 'coin_wold_info'}
    },
    # 'data_syn_work': {
    #     'task': 'crawler.data_syn.schudule_data_syn_work',
    #     'schedule': timedelta(seconds=120),
    #     # 'args': (redis_db),
    #     'options': {'queue': 'data_syn_task', 'routing_key': 'data_syn_info'}
    # },
    'crawler_eight_btc': {
        'task': 'crawler.eight_btc.schudule_eight_information',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'eight_btc_task', 'routing_key': 'eight_btc_info'}
    },
    'crawler_bit_coin': {
        'task': 'crawler.bit_coin.schudule_bit_coin_information',
        'schedule': timedelta(seconds=80),
        # 'args': (redis_db),
        'options': {'queue': 'bit_coin_task', 'routing_key': 'bit_coin_info'}
    },
    'information_duplicate_removal': {
        'task': 'crawler.information_duplicate_removal.schudule_information_duplicate_removal_work',
        'schedule': timedelta(seconds=35),
        # 'args': (redis_db),
        'options': {'queue': 'news_duplicate_removal_task', 'routing_key': 'news_duplicate_removal_info'}
    },
    'wall_street_schedule': {
        'task': 'crawler.wall_street.schudule_crawler_task',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'wall_street_task', 'routing_key': 'wall_street_info'}
    },
    'crawler_btc_new_flash': {
        'task': 'crawler.btc_new_flash.schudule_btc_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'btc_new_flash_task', 'routing_key': 'btc_new_flash_info'}
    },
    'people_cn_schedule': {
        'task': 'crawler.people_cn.schudule_people_cn_information',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'people_cn_task', 'routing_key': 'people_cn_info'}
    },
    'crawler_bian_new_flash': {
        'task': 'crawler.bian_new_flash.schudule_bianews_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'bian_new_flash_task', 'routing_key': 'bian_new_flash_info'}
    },
    'crawler_cailianpress_new_flash': {
        'task': 'crawler.cailianpress_new_flash.schudule_cailianpress_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'cailianpress_new_flash_task', 'routing_key': 'cailianpress_new_flash_info'}
    },
    'crawler_kr_new_flash': {
        'task': 'crawler.kr_new_flash.schudule_kr_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'kr_new_flash_task', 'routing_key': 'kr_new_flash_info'}
    },
    'crawler_huo_bi_new_flash': {
        'task': 'crawler.huo_bi_new_flash.schudule_huo_bi_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'huo_bi_new_flash_task', 'routing_key': 'huo_bi_new_flash_info'}
    },
    'crawler_chaindd_new_flash': {
        'task': 'crawler.chaindd_news.schudule_chaindd_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'chaindd_task', 'routing_key': 'chaindd_info'}
    },
    'crawler_wall_streetcn_new_flash': {
        'task': 'crawler.wall_streetcn_news.schudule_wall_streetcn_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'wall_streetcn_task', 'routing_key': 'wall_streetcn_info'}
    },
    'crawler_tmt_post_new_flash': {
        'task': 'crawler.tmt_post.schudule_tmt_post_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'tmt_post_task', 'routing_key': 'tmt_post_info'}
    },
    'crawler_wang_yi_new_flash': {
        'task': 'crawler.wang_yi_information.schudule_wang_yi_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'wang_yi_task', 'routing_key': 'wang_yi_info'}
    },
    'crawler_sina_new_flash': {
        'task': 'crawler.sina_news.schudule_sina_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'sina_news_task', 'routing_key': 'sina_news_info'}
    },
    'crawler_jin_shi': {
        'task': 'crawler.jin_shi.schudule_crawler_task',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'jin_shi_task', 'routing_key': 'jin_shi_info'}
    },
    'crawler_okex': {
        'task': 'crawler.okex.schudule_okex_information',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'okex_task', 'routing_key': 'okex_info'}
    },
    'crawler_binance_notice': {
        'task': 'crawler.binance_notice.schudule_binance_information',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'binance_notice_task', 'routing_key': 'binance_notice_info'}
    },
    'crawler_he_xun': {
        'task': 'crawler.he_xun.schudule_he_xun_information',
        'schedule': timedelta(seconds=70),
        # 'args': (redis_db),
        'options': {'queue': 'he_xun_task', 'routing_key': 'he_xun_info'}
    }
}
################################################
# 启动worker的命令
# *** 定时器 ***
# nohup celery beat -s /var/log/boas/celerybeat-schedule  --logfile=/var/log/boas/celerybeat.log  -l info &
# *** worker ***
# nohup celery worker -f /var/log/boas/boas_celery.log -l INFO &
################################################
