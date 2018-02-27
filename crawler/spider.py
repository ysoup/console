# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
# from celerymain.main import app
from common.crawlerrequest import CrawlerRequest
import celery

app = celery.Celery('cele', broker='redis://localhost:6379')


@app.task
def send():
    url = "http://www.jinse.com/lives"
    resp = CrawlerRequest.crawler_get(url)
    # resp = requests.get(url=url)
    print("正在抓取链接", resp)


app.conf.beat_schedule = {
    'send-every-10-seconds': {
        'task': 'cele.send',
        'schedule': 10.0
    },
}