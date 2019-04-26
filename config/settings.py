# -*- coding: utf8 -*-

import time
class OssConfig(object):
    '''
    阿里OSS配置
    '''
    OSSENDPOINT = "http://oss-cn-hangzhou.aliyuncs.com"
    OSSACCESSKEYID = "xxxxxx"
    OSSACCESSKEYSECRET = "xxxxxx"
    OSSBUCKETNAME = "xxxxxx"
    OSSKEY = "OPSM/monitor.txt"

class FdsConfig(object):
    '''
    小米fds配置
    '''
    FDSREGIONNAME = "cnbj2"
    FDSENDPOINT= "cnbj2.fds.api.xiaomi.com"
    FDSACCESSKEYID = "xxxxxx"
    FDSACCESSKEYSECRET = "xxxxxx"
    FDSBUCKETNAME = "xxxxxx"
    FDSKEY = "OPSM/monitor.txt"
    ENABLEHTTPS = False
    ENABLECDNFORUPLOAD = False
    ENABLECDNFORDOWNLOAD = False

class AlidnsConfig(object):
    '''
    阿里云解析配置
    '''
    DNSREGIONID = "cn-hangzhou"
    DNSACCESSKEYID = "xxxxxx"
    DNSACCESSKEYSECRET = "xxxxxx"
    ENABLELIST = ['4020904643089408','4040495578563584'] # RecordId
    DISABLELIST = ['3365290800945152','3365290773025792'] # RecordId

class LogConf:
    LOGPATH = "log"
    LOGNAME = "flask"
    LOGFORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s"
    LOGLEVEL = "INFO"

class CheckUrlConfig(object):
    '''
    url检测配置
    '''
    URLS = {
        "API":"http://www.xxxxxx.com/"
    }
    TIMEOUT=5

#开发环境
class DevelopmentConfig(OssConfig,FdsConfig,AlidnsConfig,LogConf,CheckUrlConfig):
    TRIES = 3
    DELAY = 0.5

APP_ENV = DevelopmentConfig