#!/bin/bash

# statsd + graphite
apt-get install -y  python-dev python-pip python-cairo
apt-get install -y  libapache2-mod-wsgi
git clone https://github.com/etsy/statsd.git
pip install graphite-web 
pip install  pytz python-pyparsing tagging python-memcache ldap python-rrdtool
pip install warden

pip install carbon
pip install whisper
pip install Django==1.3.1 
pip install django-tagging==0.3.1
echo '

{
  graphitePort: 2003
, graphiteHost: "localhost"
, port: 8125
, backends: [ "./backends/graphite" ]
}
' >> statsd/everlog.js
cd statsd && npm install

echo '
[program:statsd]
directory=/root/statsd/
command = node stats.js everlog.js
autostart = true
autorestart = true
' >> /etc/supervisor/conf.d/statsd.conf

echo "Listen 81" >> /etc/apache2/ports.conf

cp graphite_apache.conf /etc/apache2/conf.d/

for f in aggregation-rules.conf  carbon.conf  dashboard.conf  storage-aggregation.conf  storage-schemas.conf;
do
    cp /opt/graphite/conf/$f.example /opt/graphite/conf/$f

done
echo '
[carbon]
pattern = ^carbon\.
retentions = 60:90d

[default_1min_for_1day]
pattern = .*
retentions = 60s:395d
' > /opt/graphite/conf/storage-schemas.conf
cp /opt/graphite/conf/graphite.wsgi.example /opt/graphite/conf/graphite.wsgi


cd /opt/graphite/webapp/graphite/
sudo python manage.py syncdb
sudo chown -R www-data:www-data /opt/graphite/storage/
cd /opt/graphite/webapp/graphite
sudo cp local_settings.py.example local_settings.py
 
cd /opt/graphite/
sudo ./bin/carbon-cache.py start

/etc/init.d/apache2 restart


