#0!/bun.bash

apt-get install ethtool
apt-get install python-pip

apt-get install flow-tools
apt-get install fprobe
apt-get install bridge-utils

apt-get install wireshark wireshark-dev
apt-get install bison flex libpcap-dev
apt-get install libglib2.0-dev
#wget http://wiresharkdownloads.riverbed.com/wireshark/src/wireshark-1.10.0.tar.bz2
wget http://wiresharkdownloads.riverbed.com/wireshark/src/all-versions/wireshark-1.6.7.tar.bz2

tar xvfj wireshark-1.6.7.tar.bz2
cd wireshark-1.6.7 && ./configure --disable-wireshark
cd ..
git clone https://github.com/armenb/sharktools
cd sharktools && ./configure --with-wireshark-src=`pwd`/wireshark-1.6.7 --enable-pyshark && make && make install
cp src/pyshark.so  /usr/local/lib/python2.7/dist-packages/
git clone https://code.google.com/p/pyflowtools/

apt-get install netsniff-tools


# brctl addbr br0
# ip addr show
# brctl addif br0 eth0 eth1


pip install virtenv
