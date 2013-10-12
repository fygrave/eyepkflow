#!/bin/sh
ln -s /etc/apparmor.d/usr.sbin.tcpdump /etc/apparmor.d/disable/
apparmor_parser -R /etc/apparmor.d/usr.sbin.tcpdump

tcpdump -i eth1  -s 1500 -n -C 1M -G 5  -W 10   -w /data2/dumz_%s ip
