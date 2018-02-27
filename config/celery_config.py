# encoding=utf-8
from datetime import timedelta
# from settings import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD, REDIS_DB_NUM


# 某个程序中出现的队列，在broker中不存在，则立刻创建它
CELERY_CREATE_MISSING_QUEUES = True

CELERY_IMPORTS = ("async_task.tasks", "async_task.notify")

# 使用redis 作为任务队列
# BROKER_URL = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/' + str(REDIS_DB_NUM)
BROKER_URL = 'redis：//localhost:6379/0'


# CELERY_RESULT_BACKEND = 'redis://:' + REDIS_PASSWORD + '@' + REDIS_HOST + ':' + str(REDIS_PORT) + '/10'

# 并发worker数
CELERYD_CONCURRENCY = 20

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

# 定时任务
CELERYBEAT_SCHEDULE = {
    'msg_notify': {
        'task': 'async_task.notify.msg_notify',
        'schedule': timedelta(seconds=10),
        # 'args': (redis_db),
        'options': {'queue': 'my_period_task'}
    },
    'report_result': {
        'task': 'async_task.tasks.report_result',
        'schedule': timedelta(seconds=10),
      # 'args': (redis_db),
        'options': {'queue': 'my_period_task'}
    },
    # 'report_retry': {
    #    'task': 'async_task.tasks.report_retry',
    #    'schedule': timedelta(seconds=60),
    #    'options' : {'queue':'my_period_task'}
    # },
}
################################################
# 启动worker的命令
# *** 定时器 ***
# nohup celery beat -s /var/log/boas/celerybeat-schedule  --logfile=/var/log/boas/celerybeat.log  -l info &
# *** worker ***
# nohup celery worker -f /var/log/boas/boas_celery.log -l INFO &
################################################
