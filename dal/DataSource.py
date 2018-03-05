# encoding=utf-8
import sys
import os
currentUrl = os.path.dirname(__file__)
parentUrl = os.path.abspath(os.path.join(currentUrl, os.pardir))
sys.path.append(parentUrl)
from datasource.configtools import getconnstring
from peewee import *


demo = getconnstring('demo')
demo_database = MySQLDatabase('demo', **{'host': demo.host, 'password': demo.passwd, 'port': demo.port, 'user': demo.user, 'charset': demo.charset})