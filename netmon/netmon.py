#!/usr/bin/env python

from processing import  Process, Queue
import statsd
import pyshark
import sys
import yara
import os
import datetime
import sys
import json
import pika
import time

from pyinotify import WatchManager, Notifier, ThreadedNotifier, EventsCodes, ProcessEvent
import pyinotify



MQHOST = sys.argv[1]

yaraengine =  None

try:
    yaraengine =  yara.load_rules(rules_rootpath = "%s/yrules" % os.path.dirname(os.path.realpath(__file__)))
except:
    yaraengine =  yara.compile(filepath = "%s/yrules/web.yar" % os.path.dirname(os.path.realpath(__file__)))



PROCS = 10


def dofilter(s):
    if type(s) == list:
        s = "".join(s)
    s= s.replace(':','')
    s=s.decode('hex')
    return "".join(filter(lambda x: ord(x)<128, s))

def yarascan(data):
#    js = jsunpack.jsunpackn.jsunpack("/tmp/a", ['', data, "/tmp/a"], self.jsunpackopts)
#    print js
    rez = ''
    y = yaraengine.match_data(dofilter(data))
    for m in y.keys():
        for item in y[m]:
            if item["matches"]:
                rez ='%s %s'% (rez,item["rule"])
    return rez

def getMQchannel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=MQHOST))
    channel = connection.channel()
    channel.exchange_declare(exchange='sniffpack', type='fanout')
    channel.queue_declare(queue='sniffer', durable=False)
    return channel



def sendmsg(channel, msg):
    channel.basic_publish(exchange='sniffpack',
                      routing_key='sniffer',
                      body=msg,
                      properties=pika.BasicProperties(
                         delivery_mode = 2, # make message persistent
                      ))
    #print " [x] Sent %r" % (msg,)



def dopcap(arg):
    channel = getMQchannel()
    filename = arg
    print filename
    packs  = []
    try:
        packs = pyshark.read(filename, ['frame.time','ip.src', 'ip.dst', 'http.host', 'http.request.uri', 'http.user_agent', 'tcp.data','http.content_type', 'http.x_forwarded_for', 'http.x_real_ip'], 'ip')
    except Exception, e:
        print e
        os.unlink(filename)
        return
    os.unlink(filename)
    packs = list(packs)
    c = statsd.StatsClient(host = sys.argv[2], port = 8125)
    packs = list(packs)
    for p in packs:
        try:
            c.incr('packets')
            match = ''
            if p.has_key('tcp.data'):
                match = yarascan(p["tcp.data"])

            if p.has_key('http.request.uri') and p.has_key('http.user_agent'):
                #print p
                cc = ''
                src = p['ip.src']
                if p.has_key('http.x_forwarded_for'):
                    src = p["http.x_forwarded_for"]
                if p.has_key('http.x_real_ip'):
                    src = p["http.x_real_ip'"]

                if  p.has_key('http.content_type'):
                    cc = p["http.content_type"][0]
                uri = p["http.request.uri"][0]
                if uri.find('?') != -1:
                    uri = uri[:uri.find('?')]
                if uri.find('&') != -1:
                    uri = uri[:uri.find('&')]

                c.gauge('urllen', len(p["http.request.uri"][0]))
                c.gauge('agentlen', len(p["http.user_agent"][0]))
                message = {"host": p["http.host"][0],
                        "agent": p["http.user_agent"][0],
                        "uri": p["http.request.uri"][0],
                        "uri_norm": uri,
                        "content_type": cc,
                        "match": match,
                        "src": src,
                        "dst": p["ip.dst"],
                        "date": datetime.datetime.fromtimestamp(p["frame.time"]).strftime("%Y-%m-%dT%H:%M:%S.000Z")}
                sendmsg(channel, json.dumps(message))
        except Exception, e:
            print e

def worker(inp, outp):
    for arg in iter(inp.get, 'STOP'):
        rez = dopcap(arg)
        print "Done: %s" % arg


task_queue = Queue()
done_queue = Queue()

for i in range(PROCS):
    Process(target=worker, args=(task_queue, done_queue)).start()


class CloseEvent(ProcessEvent):
    def process_IN_CLOSE_WRITE(self, event):
        task_queue.put("%s" %  os.path.join(event.path, event.name))
        print "Received: %s" % os.path.join(event.path, event.name)


notifier = Notifier(wm, CloseEvent())
wdd = wm.add_watch('/data', pyinotify.IN_CLOSE_WRITE, rec=True)
while True:  # loop forever
    try:
        notifier.process_events()
        if notifier.check_events():
            notifier.read_events()
    except KeyboardInterrupt:
        notifier.stop()
        break
