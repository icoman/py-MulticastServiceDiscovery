# Multicast Service Discovery in Python

A simple udp multicast server written in [python](https://www.python.org/) - [blog announcement](http://rainbowheart.ro/522).

Use this code as a start for service discovery in your projects. No license required.

Sample for creating a server:
```python
import mcsdisc
import time

mcsd = mcsdisc.MulticastServiceDiscovery()
mcsd.registerService("key","value")
mcsd.start()
while True:
   time.sleep(1)

```

Sample for creating a client:
```python
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
```

Instantiate service class with:
```python
import mcsdisc
HOST = "224.x.x.x"
PORT = yyyyy
mcsd = mcsdisc.MulticastServiceDiscovery(HOST, PORT)
```


A picture of service running in Linux with two servers discovered:
![MulticastServiceDiscovery in Linux](http://rainbowheart.ro/static/uploads/1/2017/1/mcsdlinux.jpg)

License-free software.
 
Feel free to use this software for both personal and commercial usage.
