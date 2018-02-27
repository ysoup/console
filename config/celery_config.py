# encoding=utf-8
from datetime import timedelta
from kombu import Exchange, Queue
# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True

CELERY_IMPORTS = ("crawler.spider")

# 使用redis 作为任务队列
# BROKER_URL = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB_NUM)
BROKER_URL = 'redis://localhost:6379/0'

# 后端缓存设置
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'

# 后端数据存储设置
# CELERY_RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/10'

# 并发worker数
CELERYD_CONCURRENCY = 5

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
    Queue('task_crawler', Exchange('task_crawler'), routing_key='task_crawler'),
)

# 路由
CELERY_ROUTES = {
    'crawler.spider.send': {'queue': 'task_crawler', 'routing_key': 'task_crawler'},
}
# 默认的交换机名字为 tasks
CELERY_DEFAULT_EXCHANGE = 'tasks'
# 默认的交换机类型为 topic
CELERY_DEFAULT_EXCHANGE_KEY = 'topic'
# 默认的路由键是default键符合上面的 default 队列.
CELERY_DEFAULT_ROUTING_KEY = 'default'

# 定时任务
CELERYBEAT_SCHEDULE = {
    'test': {
        'task': 'crawler.spider.send',
        'schedule': timedelta(seconds=30),
        # 'args': (redis_db),
        # 'options': {'queue': 'my_period_task'}
    },
}
################################################
# 启动worker的命令
# *** 定时器 ***
# nohup celery beat -s /var/log/boas/celerybeat-schedule  --logfile=/var/log/boas/celerybeat.log  -l info &
# *** worker ***
# nohup celery worker -f /var/log/boas/boas_celery.log -l INFO &
################################################
