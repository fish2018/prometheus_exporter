# -*- coding: utf-8 -*-
# pip install oss2
import oss2
from flask import current_app
from datetime import datetime

class OssUpload(object):
    '''
    往OSS的bucket="xxxxxx-test"中上传一个object="OPMS/monitor"
    '''
    def __init__(self):
        self.endpoint = current_app.config['OSSENDPOINT']
        self.auth = oss2.Auth(current_app.config['OSSACCESSKEYID'],current_app.config['OSSACCESSKEYSECRET'])
        self.bucket = oss2.Bucket(self.auth,self.endpoint,current_app.config['OSSBUCKETNAME'])
        self.key = current_app.config['OSSKEY']

    def upload(self):
        try:
            self.bucket.put_object(self.key, 'monitor dfs and oss.')
            print(datetime.now(),'monitor.txt上传成功')
        except Exception as e:
            print(datetime.now(),'monitor.txt上传失败')
            raise e
