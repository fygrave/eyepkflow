#!/usr/bin/env python

import sys
import time
import signal
import optparse

import pylab
import pywt
import pcapy
import sys
from dateutil import parser
import matplotlib
from pylab import *


try:
  import whisper
except ImportError:
  raise SystemExit('[ERROR] Please make sure whisper is installed properly')

# Ignore SIGPIPE
signal.signal(signal.SIGPIPE, signal.SIG_DFL)

now = int( time.time() )
yesterday = now - (60 * 60 * 24)
threshold = 5
wavelet = 'haar'

option_parser = optparse.OptionParser(usage='''%prog [options] path''')
option_parser.add_option('--from', default=yesterday, type='int', dest='_from',
  help=("Unix epoch time of the beginning of "
        "your requested interval (default: 24 hours ago)"))
option_parser.add_option('--until', default=now, type='int',
  help="Unix epoch time of the end of your requested interval (default: now)")
option_parser.add_option('--json', default=False, action='store_true',
  help="Output results in JSON form")
option_parser.add_option('--pretty', default=False, action='store_true',
  help="Show human-readable timestamps instead of unix times")
option_parser.add_option('--relative', default=-1, type='int',
  help="relative 'from' time")

option_parser.add_option('--threshold', default=threshold, type='int',
  help="Threshold for spike detection")
option_parser.add_option('--wavelet', default=wavelet, type='string',
        help="Wavelet family (haar, db, sym, coif, bior, rbio or dmey, followed by num (i.e db4). default is haar\nAvailable wavelets: %s" % pywt.wavelist())


(options, args) = option_parser.parse_args()

if len(args) != 1:
  option_parser.print_help()
  sys.exit(1)

path = args[0]

from_time = int( options._from )
until_time = int( options.until )
if (int(options.relative) != -1):
    from_time = until_time - int(options.relative)
threshold = int(options.threshold)
wavelet = options.wavelet


try:
  (timeInfo, values) = whisper.fetch(path, from_time, until_time)
except whisper.WhisperException, exc:
  raise SystemExit('[ERROR] %s' % str(exc))


(start,end,step) = timeInfo
print "Start %s end %s step: %i" % (time.ctime(start), time.ctime(end), step)

if options.json:
  values_json = str(values).replace('None','null')
  print '''{
"start" : %d,
"end" : %d,
"step" : %d,
"values" : %s
}''' % (start,end,step,values_json)
  sys.exit(0)


t = start
for i in range(0, len(values)):
    #print "%s %s" % (time.ctime(t), values[i])
    t = t + step
    if values[i] == None:
        values[i] = -1


# wavelet analysis
#
# our math is simple if A spike is X times variance, we are hit by ddos
#


def detectDDOS(array):
    t  = start
    med = sum(array)/len(array)
    s = 0.0
    for i in range(0, len(array)):
        s = s + pow((array[i] - med), 2)

# variance
    var = sqrt(s/len(array))
    for i in range(1, len(array)):
        print "med %f var %f - %s %i (%i)" % (med, var, time.ctime(t), array[i], array[i] - array[i  - 1])
        if array[i]-array[i-1] > var * 2:
            print "DDOS at %s" % time.ctime(t)
        t = t + step




mode = pywt.MODES.ppd

w = pywt.Wavelet(wavelet)
a = values
d = values
ca = []
cd = []

for i in xrange(6):
    (a, d) = pywt.dwt(a, w, mode)
    print len(a)
    print len(d)
    ca.append(a)
    cd.append(d)
    step = step * 2

rec_a = []
rec_d = []
for i, coeff in enumerate(ca):
    coeff_list = [ coeff, None] + [ None ]
    rec_a.append(pywt.waverec(coeff_list, w))

for i, coeff in enumerate(cd):
    coeff_list = [ coeff, None] + [ None ]
    rec_d.append(pywt.waverec(coeff_list, w))

pylab.figure()
ax_main = pylab.subplot(len(rec_a) + 1, 1, 1)
pylab.title("timeseries")
ax_main.plot(values)
pylab.xlim(0, len(values) - 1)
for i,y in enumerate(rec_a):
    ax = pylab.subplot(len(rec_a) + 1, 2, 3 +  i *2 )
    ax.plot(y, 'r')
    pylab.xlim(0, len(y) - 1)
    #pylab.ylim(-100, 100)
    pylab.ylabel("A%d" % (i + 1))

for i, y in enumerate(rec_d):
    ax = pylab.subplot(len(rec_d) + 1, 2, 4 + i * 2)
    ax.plot(y, 'g')
    pylab.xlim(0, len(y) - 1)
    #pylab.ylim(-100, 100)
    pylab.ylabel("D%d" % (i + 1))

#    plot(d)
#    plot(a)
print a
print d
detectDDOS(a)

show()
