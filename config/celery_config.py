# encoding=utf-8
from datetime import timedelta
from kombu import Exchange, Queue
# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True

CELERY_IMPORTS = ("crawler.spider", "crawler.coin_world", "crawler.duplicate_removal", "crawler.data_syn")

# 使用redis 作为任务队列
# BROKER_URL = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB_NUM)
BROKER_URL = 'redis://10.31.253.60:6379/0'

# 后端缓存设置
CELERY_RESULT_BACKEND = 'redis://10.31.253.60:6379/1'

# 后端数据存储设置
# CELERY_RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/10'

# 并发worker数
CELERYD_CONCURRENCY = 1

# 时区设置
CELERY_TIMEZONE = 'Asia/Shanghai'

# 非常重要,有些情况下可以防止死锁
CELERYD_FORCE_EXECV = True

CELERYD_PREFETCH_MULTIPLIER = 1

# 每个worker最多执行万100个任务就会被销毁，可防止内存泄露
CELERYD_MAX_TASKS_PER_CHILD = 100

# CELERYD_TASK_TIME_LIMIT = 60    # 单个任务的运行时间不超过此值，否则会被SIGKILL 信号杀死

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
    Queue('data_syn_task', exchange=Exchange('data_syn_task'), routing_key='data_syn_info'),
    Queue('eight_btc_task', exchange=Exchange('eight_btc_task'), routing_key='eight_btc_info'),
    Queue('bit_coin_task', exchange=Exchange('bit_coin_task'), routing_key='bit_coin_info'))

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
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'jin_se_task', 'routing_key': 'jin_se_info'}
    },
    'crawler_duplicate_schedule': {
        'task': 'crawler.duplicate_removal.schudule_duplicate_removal_work',
        'schedule': timedelta(seconds=75),
        # 'args': (redis_db),
        'options': {'queue': 'duplicate_removal_task', 'routing_key': 'duplicate_removal_info'}
    },
    'crawler_coin_world': {
        'task': 'crawler.coin_world.schudule_coin_world_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'coin_wold_task', 'routing_key': 'coin_wold_info'}
    },
    'data_syn_work': {
        'task': 'crawler.data_syn.schudule_data_syn_work',
        'schedule': timedelta(seconds=120),
        # 'args': (redis_db),
        'options': {'queue': 'data_syn_task', 'routing_key': 'data_syn_info'}
    },
    'eight_btc': {
        'task': 'crawler.eight_btc.schudule_eight_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'eight_btc_task', 'routing_key': 'eight_btc_info'}
    },
    'bit_coin': {
        'task': 'crawler.bit_coin.schudule_bit_coin_information',
        'schedule': timedelta(seconds=45),
        # 'args': (redis_db),
        'options': {'queue': 'bit_coin_task', 'routing_key': 'bit_coin_info'}
    }
}
################################################
# 启动worker的命令
# *** 定时器 ***
# nohup celery beat -s /var/log/boas/celerybeat-schedule  --logfile=/var/log/boas/celerybeat.log  -l info &
# *** worker ***
# nohup celery worker -f /var/log/boas/boas_celery.log -l INFO &
################################################
