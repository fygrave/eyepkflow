eyepkflow
=========

EyePKFlow is an open source "Passive HTTP" collection and HTTP traffic monitoring platform. 




Installation
------------

See 'scripts/install.sh' for details. :)

Usage
-----

On sensor run netmon.py script. Arguments should be pointing to your MQ and Graphite machines i.e.

./netmon.py Rabbitmqmachine  graphitemachine

then run your workers:

./netindex.py ElasticSearch:9200 rabbitmqmachine

the data get indexed in rabbitmq.  Redis is used on workers to calculate some stats (expected to be running on localhost)

