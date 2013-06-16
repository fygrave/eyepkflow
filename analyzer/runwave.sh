#!/bin/bash

./wavelyzer.py /opt/graphite/storage/whisper/stats/flow/bytes/total.wsp  --wavelet haar --relative 7200 --es localhost:9200 --statsd localhost --relative $[ 60 * 60 * 2 ]

