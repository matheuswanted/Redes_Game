from Packet import *
import sys


class PacketBuilder:
    def __init__(self):
        self.p = Packet()

    def buildEth(self, src_mac, dst_mac):
        self.p.eth.setSrc(src_mac)
        self.p.eth.setDst(dst_mac)
        return self

    def buildIp6(self, src_addr, dst_addr):
        self.p.ip6.setDst(dst_addr)
        self.p.ip6.setSrc(src_addr)
        return self

    def buildUdp(self):
        return self

    def buildMsg(self, message):
        size = len(message.pack())
        # sys.getsizeof(message.pack())
        #print "size: " + str(size)
        #print "msg: " + str(message)
        self.p.msg = message
        self.p.udp.length += size
        self.p.ip6.payload = self.p.udp.length
        return self

    def unpack_eth(self, data):
        data_len = len(data)
        if data_len < 14:
            raise Exception('Wrong size ethernet packet!')
        elif data_len > 14:
            data = data[0:14]
        self.p.eth.unpack(data)

    def unpack_ipv6(self, data):
        data_len = len(data)
        if data_len < 40:
            raise Exception('Wrong size ipv6 packet!')
        elif data_len > 40:
            data = data[14:54]
        self.p.ip6.unpack(data)

    def unpack_udp(self, data):
        data_len = len(data)
        if data_len < 8:
            raise Exception('Wrong size udp packet!')
        elif data_len > 8:
            data = data[54:62]
        self.p.udp.unpack(data)

    def unpack_message(self, data):
        self.p.msg.unpack(data[62:])

    def get_message(self):
        return self.p.msg

    def get_connection_info(self):
        return self.p.get_connection_info()

    def pack(self):
        return self.p.pack()
