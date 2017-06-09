import socket
import binascii
from struct import *
from ConnectionInfo import *
from Packet import *
from PacketBuilder import *
class PacketFilter:
    def __init__(self, connectionInfo):
        self.connection = connectionInfo

    def filter(self, pack_builder, network_data):
        #print binascii.hexlify(network_data)
        pack_builder.unpack_eth(network_data)
        if not self.filter_ipv4(pack_builder.p.eth):
            return False

        pack_builder.unpack_ipv6(network_data)
        if not self.filter_dst_src(pack_builder.p.ip6) or not self.filter_udp(pack_builder.p.ip6):
            return False

        pack_builder.unpack_udp(network_data)
        if not self.filter_game_packet(pack_builder.p.udp):
            return False
        pack_builder.unpack_game_packet(network_data)
        return True

    def filter_ipv6(self, ethernet):
        return ethernet.eth_type == 0x86DD

    def filter_ipv4(self, ethernet):
        return ethernet.eth_type == 0x0800

    def filter_udp(self, ipv6):
        return ipv6.next_header == 17

    def filter_game_packet(self, udp):
        return udp.src_port == 16261 and udp.dst_port == 9309

    def filter_dst_src(self, ip6):
        #ips = unpack("!4s4s", network_data[14+12:14+20])
        #ip_dst = socket.inet_ntoa(ips[0])
        #ip_src = socket.inet_ntoa(ips[1])
        #print ip_dst
        #print ip_src
        return self.connection.src_ip == ip6.dst_addr and self.connection.dst_ip == ip6.src_addr

    def filter_ping(self,pack_builder):
        protocol = unpack("!B", network_data[23])[0]
        #ips[1] = socket.inet_ntoa(ips[1])
        print protocol
        return  protocol == 0x001

