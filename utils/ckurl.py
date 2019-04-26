# -*- coding: utf8 -*-
import requests
import ssl
from config import APP_ENV

class CheckUrl:
    def __init__(self):
        # 全局取消ssl
        ssl._create_default_https_context = ssl._create_unverified_context

    def ck(self,url):
        try:
            # connect到response总共消耗的时间
            # spend = requests.get(url, timeout=APP_ENV.TIMEOUT).elapsed.total_seconds()
            res = requests.get(url,timeout=APP_ENV.TIMEOUT)
            code = res.status_code
            if code < 400:
                spend = res.elapsed.total_seconds()
            else:
                spend = 0
        except Exception as e:
            raise e
        return spend