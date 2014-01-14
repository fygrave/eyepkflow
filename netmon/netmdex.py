#!/usr/bin/env python

import statsd
import sys
import os
import time
import datetime
import zmq
import redis
import json
from pyes import *
import sys
conn = ES([sys.argv[1]])
MQHOST = sys.argv[2]


def getindex():
    index_name = 'httpl%.4i%.2i'% (datetime.datetime.now().year, datetime.datetime.now().month)
    try:
        conn.create_index(index_name)
    except:
        pass
    return index_name


def getstamp():
    return '%.4i%.2i'% (datetime.datetime.now().year, datetime.datetime.now().month)

index_name = 'httpl%.4i%.2i'% (datetime.datetime.now().year, datetime.datetime.now().month)
mapping = {
           u'uri': {'boost': 1.0,
                 'index': 'analyzed',
                 'store': 'yes',
                 'type': u'string',
                 "term_vector" : "with_positions_offsets"},
           u'uri_norm': {'boost': 1.0,
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
          u'matches': {'boost': 1.0,
                 'index': 'analyzed',
                 'index_name': 'match',
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

conn.put_mapping("httpl-type", {'properties':mapping}, [getindex()])


def doindex(data):
    try:
        #print " [x] Received %r" % (body,)

        # add stuff to redis here.
        if isinstance(data["src"], list):
            data["src"] = data["src"][0]
        if isinstance(data["src"], list):
            data["dst"] = data["dst"][0]
        if data["src"].find(",") != -1:
            data["src"] = data["src"][:data["src"].find(",")]
        conn.index(data, getindex(), "httpl-type", bulk=True)
        #print " [x] Done"

        if (int(time.time()) % 7) == 0:
            conn.refresh()
    except Exception, e:
        ch.basic_ack(delivery_tag = method.delivery_tag)
        print "error ", e, " while parsing ", body



print ' [*] Waiting for messages. To exit press CTRL+C'


context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://127.0.0.1:3240")
socket.setsockopt(zmq.SUBSCRIBE, "http")

while True:
    data = socket.recv()
    data = data[data.find("http") + 5:]
    darr = data.split("\t")
    d = {}
    srcip = darr[0].split(':')
    dstip = darr[1].split(':')
    d["src"] =srcip[0]
    d["dst"] = dstip[0]
    uri = darr[3]

    if uri.find('?') != -1:
        uri = uri[:uri.find('?')]
    if uri.find('&') != -1:
        uri = uri[:uri.find('&')]
    d["uri"] = uri
    d["uri_norm"] = uri
    d["content-type"] = "unknown"
    d["match"] = "none"
    d["date"] =  datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z")
    d["host"] = darr[2]
    d["agent"] = "Unknown"


    doindex(d)

