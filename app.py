# _*_ coding:utf-8 _*_
from flask import Flask,Response,current_app,Response
from utils import FdsCheck,UrlsCheck,UploadCheck,CdnCheck,log,UpRecordStatus
import prometheus_client

app = Flask(__name__)
app.config.from_object('config.APP_ENV')

@app.route("/fds/metrics")
def check_fds():
    # 检测fds与oss
    return Response(prometheus_client.generate_latest(FdsCheck()),mimetype="text/plain")

@app.route("/cdn/metrics")
def check_fds():
    # 检测cdn文件下载速度
    return Response(prometheus_client.generate_latest(CdnCheck()),mimetype="text/plain")

@app.route("/ckurl/metrics")
def check_urls():
    # 检测url请求消耗时间
    return Response(prometheus_client.generate_latest(UrlsCheck()),mimetype="text/plain")

@app.route("/ckupload/metrics")
def check_upload():
    # 检测上传文件速度
    return Response(prometheus_client.generate_latest(UploadCheck()),mimetype="text/plain")

@app.route('/dns')
def chenge_dns():
    if not request.args.get('key') == 'eyJhbGciOiJIUzI1NiIsImV4cCI6MTQ2NDI1NzI':
        return 'key不正确'
    try:
        # 切换dns解析
        update = UpRecordStatus()
        update.changestatus()
        return 'dns切换成功'
    except Exception as e:
        return e

if __name__ == '__main__':
    app.run()

'''
背景说明：
client访问小米FDS下载文件时，如果没有该文件，小米FDS会自动从关联的阿里OSS拉取，然后再返回给client
对外提供FDS访问的域名有:
  ota.cdn.xxx.com 对应的cname解析地址：
    小米FDS: ota.cdn.xxx.com.mgslb.com 启用中 record_id 3365290800945152
    阿里OSS: ota.cdn.xxx.com.w.kunlunar.com 暂停中 record_id 4020904643089408
  apk.cdn.xxx.com 对应的cname解析地址：
    小米FDS: apk.cdn.xxx.com.wsdvs.com 启用中 record_id 3365290773025792
    阿里OSS: apk.cdn.xxx.com.w.kunlunar.com 暂停中 record_id 4040495578563584

痛点及需求:
小米FDS服务不稳定，从oss拉取文件时经常出问题，需要对其进行监控并处理，把原来小米的cname=>暂停，把阿里的cname=>启用

prometheus exporter实现逻辑:
1、往OSS上传文件，验证OSS健康，失败则报警，成功进行下一步操作
2、从FDS下载文件，验证FDS从OSS拉取文件链路是否畅通，如果尝试三次后仍失败，将变更cname解析
'''