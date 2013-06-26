#!/bin/bash

if [ x$WIRESHARK_V = x  ]
then 
    echo "wireshark version is not set.do export WIRESHARK_v=1.8.2 to compile "
    #WIRESHARK_V="1.6.7" 
    WIRESHARK_V=`wireshark -v | head -1 | cut -f 2 -d ' '`
    echo "compiling for wireshak $WIRESHARK_V (detected)"
fi
#do WIRESHARK_V="1.8.2";export WIRESHARK_V

apt-get install -y  ethtool
apt-get install -y  python-pip python-dev

apt-get install -y  flow-tools
apt-get install -y  fprobe
apt-get install -y  bridge-utils

apt-get install -y  wireshark wireshark-dev
apt-get install -y  bison flex libpcap-dev
apt-get install -y  libglib2.0-dev
#wget http://wiresharkdownloads.riverbed.com/wireshark/src/wireshark-1.10.0.tar.bz2
wget http://wiresharkdownloads.riverbed.com/wireshark/src/all-versions/wireshark-$WIRESHARK_V.tar.bz2

tar xvfj wireshark-$WIRESHARK_V.tar.bz2
cd wireshark-$WIRESHARK_V && ./configure --disable-wireshark
cd ..
git clone https://github.com/armenb/sharktools
cd sharktools && ./configure --with-wireshark-src=`pwd`/../wireshark-$WIRESHARK_V --enable-pyshark && make && make install
cp src/pyshark.so  /usr/local/lib/python2.7/dist-packages/
git clone https://code.google.com/p/pyflowtools/

apt-get install -y  netsniff-tools


# brctl addbr br0
# ip addr show
# brctl addif br0 eth0 eth1


pip install   virtualenv
pip install --upgrade distribute
pip install yara
