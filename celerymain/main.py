# encoding=utf-8

from celery import Celery
from config import celery_config

app = Celery()
app.config_from_object(celery_config)