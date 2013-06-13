#1/usr/bin/env python

import statsd
import pyshark
import sys


packs = pyshark.read(sys.argv[1], ['ip.src', 'ip.dst', 'http.host', 'http.request.uri', 'http.user_agent'], 'ip')

packs = list(packs)

gauge = statsd.Gauge('ddos')
raw = statsd.Raw('ddos')
useragent = statsd.Gauge('ddos.useragent')


packs = list(packs)
for p in packs:
        raw.send('pack', 1, p.timestamp)
        print p
        gauge.send('urllen', len(p["http.request.uri"]))
        gauge.send('agentlen', len(p["http.user_agent"]))

