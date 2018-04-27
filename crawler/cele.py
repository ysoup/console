# cele.py
import celery


app = celery.Celery('cele', broker='redis://127.0.0.1:6379')


@app.task
def send(message):
    return message


app.conf.beat_schedule = {
    'send-every-10-seconds': {
        'task': 'cele.send',
        'schedule': 10.0,
        'args': ('Hello World', )
    },
}