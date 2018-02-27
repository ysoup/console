# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from celery import Celery
from config import celery_config

app = Celery()
app.config_from_object(celery_config)
