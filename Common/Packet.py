from struct import *

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
