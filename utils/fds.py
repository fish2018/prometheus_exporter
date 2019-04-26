# -*- coding: utf-8 -*-
# pip install galaxy-fds-sdk
from fds import GalaxyFDSClient
from fds.fds_client_configuration import FDSClientConfiguration
import time
from retry import retry
from flask import current_app
from config.settings import APP_ENV
from datetime import datetime

class FdsDownload(object):
    '''
    从fds的bucket="xxxxxx-test"下载object="OPMS/monitor.txt",验证文件从OSS拉取到FDS的链路是否畅通，不通则切换dns解析
    '''
    def __init__(self):
        self.config = FDSClientConfiguration(
            region_name=current_app.config['FDSREGIONNAME'],
            endpoint=current_app.config['FDSENDPOINT'],
            enable_https=current_app.config['ENABLEHTTPS'],
            enable_cdn_for_upload=current_app.config['ENABLECDNFORUPLOAD'],
            enable_cdn_for_download=current_app.config['ENABLECDNFORDOWNLOAD'])
        self.client = GalaxyFDSClient(
            current_app.config['FDSACCESSKEYID'],
            current_app.config['FDSACCESSKEYSECRET'],
            config=self.config)

    # 重试三次再改域名解析
    @retry(tries=APP_ENV.TRIES, delay=APP_ENV.DELAY)
    def download(self):
        try:
            f = self.client.get_object(current_app.config['FDSBUCKETNAME'], current_app.config['FDSKEY'])
            print(datetime.now(),"monitor.txt文件存在")
            # with open("success.txt", 'wb+') as file:
            #     file.writelines(f.stream)
            time.sleep(0.5)
            self.client.delete_object(current_app.config['FDSBUCKETNAME'], current_app.config['FDSKEY'])
            print(datetime.now(),"验证文件存在，删除monitor.txt成功")
        except Exception as e:
            print(datetime.now(),"monitor.txt文件不存在")
            raise e

