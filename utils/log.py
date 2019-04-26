# -*- coding: utf8 -*-
import logging,os
from logging import handlers
from config import APP_ENV
import time
class Log:
    '''
    日志工具类，使用示例:
    from flask import current_app
    current_app.logger.info('yyyy')
    '''
    def __init__(self):
        # 创建日志目录
        log_path = APP_ENV.LOGPATH
        log_name = APP_ENV.LOGNAME + '.log'
        log_path = os.path.abspath(os.path.join(os.path.dirname(__file__),os.pardir)) + os.sep + log_path
        if not os.path.exists(log_path):
            os.mkdir(log_path)
        # 日志文件路径
        log_file = log_path + os.sep + log_name
        # 日志处理器，按时间切割
        handler = logging.handlers.TimedRotatingFileHandler(log_file, when='MIDNIGHT', interval=1, backupCount=5, delay=False, utc=False,encoding='UTF-8')
        # 日志格式
        logging_format = logging.Formatter(APP_ENV.LOGFORMAT)
        handler.setFormatter(logging_format)
        # 传入app名，设置logger
        logger = logging.getLogger('flask.app')
        # 添加处理器
        logger.addHandler(handler)
        # 日志等级
        logger.setLevel(APP_ENV.LOGLEVEL)

log = Log()
