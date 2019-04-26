FROM python:3

WORKDIR /usr/src/app

COPY . ./exporter

RUN pip install --no-cache-dir -r ./exporter/requirements.txt && \
    apt-get update && apt-get install --assume-yes supervisor vim net-tools && \
    mv ./exporter/tool_zip/*.conf /etc/supervisor/conf.d/ && \
    wget -P ./exporter/tool_zip/ https://github.com/prometheus/prometheus/releases/download/v2.3.2/prometheus-2.3.2.linux-amd64.tar.gz && \
    tar zxvf ./exporter/tool_zip/prometheus-2.3.2.linux-amd64.tar.gz -C /usr/src/app/ && \
    chmod +x /usr/src/app/exporter/tool_zip/change_config.sh && \
    mv ./exporter/tool_zip/prometheus.yml ./prometheus-2.3.2.linux-amd64/prometheus_global.yml && \
    rm -rf ./exporter/tool_zip/prometheus-2.3.2.linux-amd64.tar.gz

ENTRYPOINT ["/bin/bash","/usr/src/app/exporter/tool_zip/change_config.sh"]

#CMD [ "bash", "./tool_zip/start.sh" ]
#CMD [ "/usr/bin/supervisord", "-c", "/etc/supervisor/supervisord.conf" ]

# ENTRYPOINT ["/usr/bin/supervisord","-n","-c", "/etc/supervisor/supervisord.conf"]
