#!/bin/bash
#IP=`/sbin/ifconfig  | grep -E 'inet.[0-9]' | grep -v '127.0.0.1' | awk '{ print $2}'`
#file='/usr/src/app/exporter/tool_zip/country_ip.txt'
country=$COUNTRY_NAME
sed -i "s/undefinition/$country/g" '/usr/src/app/prometheus-2.3.2.linux-amd64/prometheus_global.yml'
/usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf