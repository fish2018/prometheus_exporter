# -*- coding: utf8 -*-
import requests
from retry import retry
from config import APP_ENV

class CheckUpload:
    def __init__(self,url,file):
        self.url = url
        self.files = {"file": open(file, "rb")}
        self.data = None

    @retry(tries=APP_ENV.TRIES, delay=APP_ENV.DELAY)
    def ck(self):
        try:
            res = requests.post(self.url, files=self.files ,data=self.data)
            code = res.status_code
            spend = res.elapsed.total_seconds()
            if code is 200:
                speed = float('%.2f' % (1024 / spend))
            else:
                speed = 0
        except Exception as e:
            raise (e)
        return speed,spend

# CheckUpload('xxxx','../UPFILE').ck()