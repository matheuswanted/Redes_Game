import socket
from struct import *

class Ethernet:
    def __init__(self):
        self.src = None
        self.dst = None
        self.eth_type = 34525 #86dd - ipv6

    def setSrc(self, src):
        self.src = src

    def setDst(self, dst):
        self.dst = dst

    def pack(self):
        return pack('!6s6sH', self.dst, self.src, self.eth_type)

    def unpack(self,data):
        self.dst, self.src, self.eth_type = unpack("!6s6sH",data)

class IPV6:
    def __init__(self):
        self.version = 6 << 4
        self.traffic_class = 0
        self.flow_label = 0
        self.payload = 0
        self.next_header = 17 #UDP fixed
        self.hop_limit = 64
        self.src_addr = None
        self.dst_addr = None

    def setSrc(self, addr):
        self.src_addr = addr

    def setDst(self, addr):
        self.dst_addr = addr

    def pack(self):
        return pack('!BBHHBB16s16s', self.version, self.traffic_class, self.flow_label, self.payload, self.next_header, self.hop_limit, self.src_addr, self.dst_addr)

    def unpack(self, data):
        self.version, self.traffic_class, self.flow_label, self.payload, self.next_header, self.hop_limit, self.src_addr, self.dst_addr = unpack("!BBHHBB16s16s",data)

class Udp:
    def __init__(self):
        self.src_port = 16261
        self.dst_port = 9309
        self.length = 8
        self.checksum = 0xffff

    def pack(self):
        return pack('!HHHH', self.src_port, self.dst_port, self.length, self.checksum)
    
    def unpack(self, data):
        self.src_port, self.dst_port, self.length, self.checksum = unpack('!HHHH', data)

class AppMessage:
    def __init__(self, action=None):
        self.action = action

    def pack(self):
        return pack('!B',self.action)

    def unpack(self, msg):
        self.action = unpack('!B',msg)

class Packet:
    def __init__(self):
        self.eth = Ethernet()
        self.ip6 = IPV6()
        self.udp = Udp()
        self.msg = AppMessage()
        self.ip6.payload += self.udp.length

    def pack(self):
        return self.eth.pack() + self.ip6.pack() + self.udp.pack() + self.msg.pack()

    def get_connection_info(self):
        return None