import mcsdisc
import json

mcsd = mcsdisc.MulticastServiceDiscovery()
mcsd.registerService("key","value")
mcsd.start()

while True:
    L = mcsd.discover(20)
    for i in L:
        data, server = i
        d = json.loads(data.replace("'", "\""))
        print "Services from",server
        for i in d.keys():
            print i,"=",d[i]
        print "---------------"
    raw_input("Press ENTER to retry discovery.")
