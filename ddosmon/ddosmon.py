#1/usr/bin/env python

import statsd
import pyshark
import sys


packs = pyshark.read(sys.argv[1], ['ip.src', 'ip.dst', 'http.host', 'http.request.uri', 'http.user_agent'], 'ip')

packs = list(packs)
for p in packs:
        print p

