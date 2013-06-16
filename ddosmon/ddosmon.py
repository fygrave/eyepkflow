#!/usr/bin/env python

import statsd
import pyshark
import sys
import os
import datetime
from pyes import *
import sys
conn = ES([sys.argv[1]])

index_name = 'httpl%.4i%.2i'% (datetime.datetime.now().year, datetime.datetime.now().month)
try:
    conn.create_index(index_name)
except:
    pass

mapping = {
           u'uri': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'string',
                 "term_vector" : "with_positions_offsets"},
           u'host': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'string',
                 "term_vector" : "with_positions_offsets"},
           u'agent': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'string',
                 "term_vector" : "with_positions_offsets"},
           u'content_type': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'string',
                 "term_vector" : "with_positions_offsets"},
           u'src': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'ip'
                 },
           u'dst': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'ip'
                 },
	    u'date': { 'boost':1.0,
			'index': 'analyzed', 'store': 'yes', 'type': 'date', 'format': 'date_time'}
                }

conn.put_mapping("httpl-type", {'properties':mapping}, [index_name])



def dopcap(filename):
	packs = pyshark.read(filename, ['frame.time','ip.src', 'ip.dst', 'http.host', 'http.request.uri', 'http.user_agent', 'http.content_type'], 'ip')

	packs = list(packs)

	c = statsd.StatsClient(host = sys.argv[2], port = 8125)



	packs = list(packs)
	for p in packs:
	    try:
		c.incr('packets')
		if p.has_key('http.request.uri') and p.has_key('http.user_agent'):
			#print p
			cc = ''
			if  p.has_key('http.content_type'):
				cc = p["http.content_type"][0]
			c.gauge('urllen', len(p["http.request.uri"][0]))
			c.gauge('agentlen', len(p["http.user_agent"][0]))
			conn.index({"host": p["http.host"][0],
				    "agent": p["http.user_agent"][0],
				    "uri": p["http.request.uri"][0],
				    "content_type": cc,
					"src": p["ip.src"],
					"dst": p["ip.dst"],
					"date": datetime.datetime.fromtimestamp(p["frame.time"]).strftime("%Y-%m-%dT%H:%M:%S.000Z")
			}, index_name, "httpl-type")

	    except Exception, e:
		print e

	os.unlink(filename)

for dirname, dirnames, filenames in os.walk('/data/'):
	for f in filenames:
		filename = os.path.join(dirname, f)
		print filename
		dopcap(filename)



