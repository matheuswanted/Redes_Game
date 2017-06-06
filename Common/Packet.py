from struct import *

class Ethernet:
    def __init__(self):
        self.src = None
        self.dst = None
        self.eth_type = 34525 #86DD - ipv6
    
    def setSrc(self,src):
        self.src = src

    def setDst(self,dst):
        self.dst = dst

    def pack(self):
        return pack('!6B6BH',self.src,self.dst,self.eth_type)

class IPV6:
    def __init__(self):
        self.version = 6
        self.traffic_class = 0
        self.flow_label = 0
        self.payload = 0
        self.next_header = 17 #UDP fixed
        self.hop_limit = 64
        self.src_addr = None
        self.dst_addr = None

    def setSrc(self,addr):
        self.src_addr = socket.inet_pton(addr,AF_INET6)

    def setDst(self,addr):
        self.dst_addr = socket.inet_pton(addr,AF_INET6)

    def pack(self):
        return pack('!BHBIIHH16s16s',self.version,self.traffic_class,self.flow_label,self.flow_label,self.payload,self.next_header,self.hop_limit,self.src_addr,self.dst_addr)

class Udp:
    def __init__(self):
        self.src_port = 0
        self.dst_port = 0
        self.length = 0
        self.checksum = 0
        self.size = 8


    def setSrc(self,addr):
        self.src_addr = socket.inet_pton(addr,AF_INET6)

    def setDst(self,addr):
        self.dst_addr = socket.inet_pton(addr,AF_INET6)
    
    def pack(self):
        return pack('!IIII',self.src_port,self.dst_port,self.length,self.checksum)

class Packet:
    def __init__(self):
        self.eth = None
        self.ip6 = None
        self.udp = None
        self.msg = None

    def pack(self):
        return self.eth.pack() + self.ip6.pack() + self.udp.pack() + self.msg.pack()

    def unpack(self, eth, ip6, udp, msg):
        #self.eth = Eth().unpack(eth)
        #self.ip6 = Ip6().unpack(ip6)
        #self.udp = Udp().unpack(udp)
        #self.msg = Msg().unpack(msg)
        return self
