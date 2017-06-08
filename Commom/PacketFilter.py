import socket
import binascii
from struct import *
from ConnectionInfo import *
class PacketFilter:
    def __init__(self, filterFn, connectionInfo):
        self.filterFn = filterFn
        self.connection = connectionInfo

    def filter(self, network_data):
        #print binascii.hexlify(network_data)
        return self.filter_ipv4(network_data) and self.filter_ping(network_data)

    def filter_ipv6(self, network_data):
        return network_data[12] == 0x86 and network_data[13] == 0xDD

    def filter_ipv4(self, network_data):
        addr = unpack("!H",network_data[12:14])[0]
        return addr == 0x0800

    def filter_ping(self,network_data):
        ips = unpack("!4s4s", network_data[14+12:14+20])
        protocol = unpack("!B", network_data[23])[0]
        ip_dst = socket.inet_ntoa(ips[0])
        ip_src = socket.inet_ntoa(ips[1])
        #ips[1] = socket.inet_ntoa(ips[1])
        print protocol
        print ip_dst
        print ip_src
        return  protocol == 0x001 and self.connection.src_ip == str(ip_dst) and self.connection.dst_ip == str(ip_src)
