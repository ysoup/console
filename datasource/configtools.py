# encoding=utf-8
import configparser
import os
config = configparser.ConfigParser()
path = os.path.join(os.path.split(os.path.realpath(__file__))[0], "mysql.conf")
print(path)
config.read(path)


def getconnstring(configname):
    result = __()
    result.host = config.get(configname, 'dbhost')
    result.port = config.getint(configname, 'dbport')
    result.user = config.get(configname, 'dbuser')
    result.passwd = config.get(configname, 'dbpassword')
    result.dbname = config.get(configname, 'dbname')
    result.charset = config.get(configname, 'dbcharset')
    return result


def get(section, option):
    return config.get(section, option)


class __(object):
    pass