import mcsdisc
import json
import time

mcsd = mcsdisc.MulticastServiceDiscovery()
while True:
    print "\n\nDiscover:"
    L = mcsd.discover(20)
    for i in L:
       data, server = i
       d = json.loads(data.replace("'", "\""))
       print "Services from",server
       for i in d.keys():
           print i,"=",d[i]
    time.sleep(3)
