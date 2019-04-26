#!/usr/bin/env python
#coding=utf-8
# pip install aliyun-python-sdk-alidns
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import SetDomainRecordStatusRequest
from flask import current_app
from datetime import datetime

class UpRecordStatus(object):
    '''
    region_id需要提交工单查询，默认cn_hangzhou
    域名解析变更，把小米FDS的cname解析暂停 => 把阿里OSS的cname解析启用
    '''
    def __init__(self):
        self.clt = client.AcsClient(
            current_app.config['DNSACCESSKEYID'],
            current_app.config['DNSACCESSKEYSECRET'])
        self.request = SetDomainRecordStatusRequest.SetDomainRecordStatusRequest()
        self.request.set_accept_format('json')

    def changestatus(self):
        for recordid in current_app.config['ENABLELIST']:
            # 设置参数
            self.request.add_query_param('Status', 'Enable')
            self.request.add_query_param('RecordId', recordid)
            # 发起请求
            self.clt.do_action(self.request)
            print(datetime.now(),'启用dns'+recordid)
        for recordid in current_app.config['DISABLELIST']:
            self.request.add_query_param('Status', 'Disable')
            self.request.add_query_param('RecordId', recordid)
            self.clt.do_action(self.request)
            print(datetime.now(),'暂停dns'+recordid)