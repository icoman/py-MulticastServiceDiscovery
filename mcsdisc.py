"""

Multicast service discovery

"""

import threading, time, socket, struct, json

class MulticastServiceDiscovery(threading.Thread):
    """
    Client and server
    """
    def __init__(self, addr = "224.3.4.5", port=45566):
        threading.Thread.__init__(self)
        self.addr = addr
        self.port = port
        self.services = {}
        self.serverip = ""
        self.daemon = True

    #client section
    def discover(self, ttlval=10):
        """
            Send discover message to all servers from
            multicast group and return a list
            of servers with services
        """
        multicast_group = (self.addr, self.port)
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        #People have the misconception that binding is only for listening on a socket,
        #but this is also true for connecting, and its just that in normal usage the binding is chosen for you.
        #select ethernet interface according to self.serverip
        sock.bind((self.serverip, 0))

        sock.settimeout(1.5)
        ttl = struct.pack("b", ttlval)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
        message = "discover"
        L = []
        sent = sock.sendto(message, multicast_group)
        while True:
            try:
                data, server = sock.recvfrom(1024)
            except socket.timeout:
                break
            else:
                L.append((data, server))
        return L

    def registerService(self, key, value):
        #Update service list
        self.services[key] = value

    def run(self):
        #Thread function
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((self.serverip, self.port))
        group = socket.inet_aton(self.addr)
        mreq = struct.pack("4sL", group, socket.INADDR_ANY)
        sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
        sock.settimeout(0.5)
        while True:
            try:
                data, address = sock.recvfrom(1024)
                #it doesn't matter the data received, send always the service list
                servicelist = json.dumps(self.services)
                sock.sendto(servicelist, address)
            except socket.timeout:
                #ignore
                pass
            except Exception as ex:
                print ex



if __name__ == "__main__":
    """
        Test module
    """
    print "Test module host =",socket.gethostname()
    hostname, aliaslist, ipaddrlist = socket.gethostbyname_ex(socket.gethostname())
    print "ipaddrlist=",ipaddrlist
    mcsd_list = []
    for serverip in ipaddrlist:
        #if we have multiple ethernet interfaces
        #create an MulticastServiceDiscovery instance for each interface
        print "Add server on",serverip
        mcsd = MulticastServiceDiscovery()
        #mcsd.serverip should keep selected interface
        #IP address, but on Linux is not working. Default is "".
        #mcsd.serverip = serverip #test this on windows

        #register a service according the interface IP address
        mcsd.registerService("DSN","mssql+pymssql://webuser:userweb@{}/WWWDB".format(serverip))
        mcsd.registerService("RPC","http://{}:4001".format(serverip))
        mcsd.registerService("WEB","http://{}:8080".format(serverip))
        iplist=""
        for i in ipaddrlist:
            if iplist:
                iplist += ", "
            iplist += i
        mcsd.registerService("ipaddrlist",iplist)
        mcsd_list.append(mcsd)
        mcsd.start()
        del mcsd
        time.sleep(1)
    try:
        while True:
            #time.sleep(2)
            print "=========================="
            for ix,mcsd in enumerate(mcsd_list):
                if mcsd.serverip:
                    print "\n\n\nClient{} on {} discover:".format(ix, mcsd.serverip)
                else:
                    #On Linux?
                    print "\n\n\nClient{} discover:".format(ix)
                L = mcsd.discover(20)
                for i in L:
                    data, server = i
                    d = json.loads(data.replace("'", "\""))
                    print "Services from",server
                    for i in d.keys():
                        print i,"=",d[i]
                    print "---------------"
            raw_input("Press ENTER to retry discovery.")
    except KeyboardInterrupt:
        #print "KeyboardInterrupt"
        pass
    except Exception as ex:
        print ex
    raw_input("\nProgram ends. Press ENTER")

