import socket
import inspect
from struct import *
from ConnectionInfo import *
from Commom.Utils import *

class Ethernet:
    def __init__(self):
        self.src = None
        self.dst = None
        self.eth_type = 34525  # 86dd - ipv6

    def setSrc(self, src):
        self.src = src

    def setDst(self, dst):
        self.dst = dst

    def pack(self):
        return pack('!6s6sH', self.dst, self.src, self.eth_type)

    def unpack(self, data):
        self.dst, self.src, self.eth_type = unpack("!6s6sH", data)


class IPV6:
    def __init__(self):
        self.version = 6 << 4
        self.traffic_class = 0
        self.flow_label = 0
        self.payload = 0
        self.next_header = 17  # UDP fixed
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
        self.version, self.traffic_class, self.flow_label, self.payload, self.next_header, self.hop_limit, self.src_addr, self.dst_addr = unpack(
            "!BBHHBB16s16s", data)


class Udp:
    def __init__(self):
        self.src_port = 16261
        self.dst_port = 9309
        self.length = 8
        self.checksum = 0xffff

    def pack(self):
        return pack('!HHHH', self.src_port, self.dst_port, self.length, self.checksum)

    def unpack(self, data):
        self.src_port, self.dst_port, self.length, self.checksum = unpack(
            '!HHHH', data)


class GameMessage:
    def __init__(self, action=None, status=None, msg=''):
        self.action = action
        self.status = status
        self.message = msg

    def pack(self):
        p = str(self.action) + ';' + str(self.status) + ';'
        
        if type(self.message) is not str or type(self.message) is list:
            p += encode_json(self.message)
        else:
            p += str(self.message)
            
        return p

    def unpack(self, msg):
        arr_msg = msg.split(';')

        self.action = int(arr_msg[0])
        self.status = int(arr_msg[1])

        if '{' in arr_msg[2]:
            self.message = decode_json(arr_msg[2])
        else:
            self.message = arr_msg[2]

class Packet:
    def __init__(self):
        self.eth = Ethernet()
        self.ip6 = IPV6()
        self.udp = Udp()
        self.msg = GameMessage()
        self.ip6.payload += self.udp.length

    def pack(self):
        return self.eth.pack() + self.ip6.pack() + self.udp.pack() + self.msg.pack()

    # envia informacoes com origem e destinos ja alterados, facilitando consulta
    def get_connection_info(self):
        return ConnectionInfo(self.eth.dst, self.eth.src, self.ip6.dst_addr, self.ip6.src_addr)
