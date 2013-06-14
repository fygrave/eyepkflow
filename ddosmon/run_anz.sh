#!/bin/bash

echo $ES_IP
echo $STATSD_IP
if [ -z $ES_IP ]
then
    echo "do export ES_IP=elasticsearch:9200; export STATSD_IP=statsdhost"
    exit 1
fi

while [ 1 ]; do ./ddosmon.py $ES_IP $STATSD_IP; sleep 10; done
