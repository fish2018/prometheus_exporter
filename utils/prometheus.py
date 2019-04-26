# -*- coding: utf8 -*-
from prometheus_client.core import GaugeMetricFamily
from urllib import request
from datetime import datetime
from utils import log,CheckUrl,MyThread,CheckUpload
from flask import current_app,Flask

'''
urllib.urlretrieve 的回调函数：
def callbackfunc(blocknum, blocksize, totalsize):
    @blocknum:  已经下载的数据块
    @blocksize: 数据块的大小
    @totalsize: 远程文件的大小
'''

class CdnCheck(object):
    def __init__(self):
        self.filename = 'data.zip'
        self.url = 'http://ota.cdn.xxxxxx.com/Monitor/monitor.pdf'

    def collect(self):
        try:
            start_time = datetime.now()
            def Schedule(blocknum, blocksize, totalsize):
                global speed,spend
                spend = (datetime.now() - start_time).total_seconds()
                if spend > 30:
                    spend = 30
                    speed = (blocknum * blocksize / 1024) / spend  # kb/秒
                    raise Exception("timeout", spend)
                speed = (blocknum * blocksize / 1024) / spend  # kb/秒
            request.urlretrieve(self.url, self.filename, Schedule)
        except Exception as e:
            pass
        finally:
            result = float('%.2f' % speed)

        current_app.logger.info("下载速度: %s kb/s，用时：%s s" % (result,spend))
        yield GaugeMetricFamily('cdn_check','check cdn download speed ',value=result)

class UrlsCheck(object):
    '''
    批量检测url，超时5秒
    '''
    def __init__(self):
        self.urls = current_app.config['URLS'].items()
        self.ckurl = CheckUrl()

    def check(self,remark,url):
        try:
            spend = self.ckurl.ck(url)
        except Exception as e:
            spend = 0
        Flask(__name__).logger.info("%s用时%s" % (remark,spend))
        return GaugeMetricFamily('%s_check' % remark, 'elapsed for %s' % remark, value=spend)

    def collect(self):
        li = []
        for remark,url in self.urls:
            t = MyThread(self.check,args=(remark,url))
            li.append(t)
            t.start()
        for t in li:
            t.join()
            yield t.get_result()

class UploadCheck(object):
    '''
    检测文件上传速度
    '''
    def __init__(self):
        self.url = 'https://webapi.xxxxxx.com/webapi/monitorupload/upload-file/'
        self.file = 'UPFILE'

    def collect(self):
        time = 0
        res = 0
        try:
            print(self.url,self.file)
            res,time = CheckUpload(self.url,self.file).ck()
        except Exception as e:
            print(e)
        Flask(__name__).logger.info("上传速度: %s kb/s，用时：%s s" % (res,time))
        yield GaugeMetricFamily('upload_check','check upload speed ',value=res)

class FdsCheck(object):
    '''
    promethues指标采集：
    1、上传文件验证OSS是否健康
    2、下载验证FDS从OSS拉取文件链路是否畅通
    3、成功返回metric值随机数
    4、失败返回metric值0，并切换dns解析
    '''
    def __init__(self):
        self.oss = OssUpload()
        self.fds = FdsDownload()

    def collect(self):
        try:
            self.oss.upload()
            self.fds.download()
            num = random.randrange(100, 150, 2) * 1000
            result = float('%.2f' % (num / 1024.0))
        except Exception as e:
            result = float('%.2f' % (0 / 1024.0))
        print("prometheus指标：%s" % result)
        yield GaugeMetricFamily('fds_check','check whether fds dead ',value=result)