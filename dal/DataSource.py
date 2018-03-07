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

# 金色财经
jin_se = getconnstring('jin_se')
ji_se_database = MySQLDatabase('jin_se', **{'host': jin_se.host, 'password': jin_se.passwd, 'port': jin_se.port, 'user': jin_se.user, 'charset': jin_se.charset})

# 币世界
coin_world = getconnstring('coin_world')
coin_world_database = MySQLDatabase('coin_world', **{'host': coin_world.host, 'password': coin_world.passwd, 'port': coin_world.port, 'user': coin_world.user, 'charset': coin_world.charset})

# discuzdb
discuzdb = getconnstring('discuzdb')
discuzdb = MySQLDatabase('discuzdb', **{'host': discuzdb.host, 'password': discuzdb.passwd, 'port': discuzdb.port, 'user': discuzdb.user, 'charset': discuzdb.charset})

