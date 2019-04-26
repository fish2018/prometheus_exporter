#!/usr/bin/env python
#coding=utf-8
'''
离线脚本，用于获取record_id，也可以直接在线查询
https://api.aliyun.com/?#product=Alidns&api=DescribeDomainRecords&params={%22RegionId%22:%22cn-hangzhou%22,%22DomainName%22:%22sunmi.com%22,%22PageSize%22:%22100%22,%22PageNumber%22:%221%22,%22RRKeyWord%22:%22apk.cdn%22}&tab=DEBUG&lang=PYTHON&_=r
'''
from aliyunsdkcore import client
from aliyunsdkalidns.request.v20150109 import DescribeDomainRecordsRequest
from aliyunsdkcore.profile import region_provider
#region_provider.modify_point('alidns', '<regionId>', 'alidns.<regionId>.aliyuncs.com')

clt = client.AcsClient('xxxxxx','xxxxxx','cn-hangzhou')

# 设置参数
request = DescribeDomainRecordsRequest.DescribeDomainRecordsRequest()
request.set_accept_format('json')

request.add_query_param('RegionId', 'cn-hangzhou')
request.add_query_param('DomainName', 'sunmi.com')
request.add_query_param('PageSize', 100)
request.add_query_param('PageNumber', 1)
request.add_query_param('RRKeyWord', 'cdn')

# 发起请求
response = clt.do_action(request)

print (response)
