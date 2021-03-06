#!/usr/bin/env python

import statsd
import sys
import os
import time
import datetime
import pika
import redis
import json
from pyes import *
import sys
conn = ES([sys.argv[1]])
MQHOST = sys.argv[2]
reclient = redis.Redis(host='localhost', port=6833)

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



connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=MQHOST))
channel = connection.channel()

channel.exchange_declare(exchange='sniffpack', type='fanout')
channel.queue_declare(queue='sniffer', durable=False)
channel.queue_bind(exchange='sniffpack', queue='sniffer')

print ' [*] Waiting for messages. To exit press CTRL+C'

def callback(ch, method, properties, body):
    try:
        #print " [x] Received %r" % (body,)
        data = json.loads(body)
        # add stuff to redis here.
        if isinstance(data["src"], list):
            data["src"] = data["src"][0]
        if isinstance(data["src"], list):
            data["dst"] = data["dst"][0]
        if data["src"].find(",") != -1:
            data["src"] = data["src"][:data["src"].find(",")]
        conn.index(data, getindex(), "httpl-type", bulk=True)
        reclient.zincrby("ipsrc%s"%getstamp(), data["src"], 0.1)
        reclient.zincrby("uri%s"%getstamp(), data["uri_norm"], 0.1)
        reclient.zincrby(data["src"], data["uri_norm"], 0.1)
        #print " [x] Done"
        ch.basic_ack(delivery_tag = method.delivery_tag)
        if (int(time.time()) % 7) == 0:
            conn.refresh()
    except Exception, e:
        ch.basic_ack(delivery_tag = method.delivery_tag)
        print "error ", e, " while parsing ", body

channel.basic_qos(prefetch_count=1)
channel.basic_consume(callback,
                      queue='sniffer')

channel.start_consuming()


